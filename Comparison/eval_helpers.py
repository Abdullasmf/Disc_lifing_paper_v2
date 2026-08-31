"""Analysis/plotting helpers for model_ablation_comparison.ipynb.

This module contains no model-loading, checkpoint, or torch inference code —
that logic stays in the notebook for auditability. Everything here operates on
plain pandas/numpy data produced by the notebook's inference loop.

Expected "node_results" DataFrame schema (one row per evaluated query node):
    regime, ablation, model_family, sample_key, sample_id, node_idx,
    x_mm, r_mm, zone_id, zone_name, subzone_id, subzone_name, arc_length_mm,
    true_stress, pred_stress, true_loglife, pred_loglife
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

ZONE_ID_TO_NAME: Dict[int, str] = {
    0: "bore", 1: "lower_transition", 2: "web", 3: "upper_transition", 4: "rim",
}
SUBZONE_ID_TO_NAME: Dict[int, str] = {
    0: "bore", 1: "lower_transition", 2: "web", 3: "upper_transition", 4: "rim_main",
    5: "front_face", 6: "front_cgroove", 7: "rear_arm_neck", 8: "rear_arm_land",
    9: "rear_arm_corner", 10: "rear_arm_end_face",
}
GROUPED_REGION_DEFS: Dict[str, List[str]] = {
    "Critical lower transition": ["lower_transition"],
    "Rim features": ["rim_main", "front_cgroove", "rear_arm_neck", "rear_arm_land", "rear_arm_corner"],
    "Remaining contour": ["bore", "web", "upper_transition"],
}

MIN_BIN_NODES = 30  # below this a bin's aggregate is flagged unstable
MIN_ZONE_NODES = 20

GROUP_COLS = ["regime", "ablation", "model_family"]


# ---------------------------------------------------------------------------
# Pooled metrics (reproduces the notebook's original pooled-metric behaviour)
# ---------------------------------------------------------------------------

def _mse(t, p):
    t, p = np.asarray(t, np.float64), np.asarray(p, np.float64)
    return float(np.mean((t - p) ** 2))


def _rmse(t, p):
    return float(np.sqrt(_mse(t, p)))


def _mae(t, p):
    t, p = np.asarray(t, np.float64), np.asarray(p, np.float64)
    return float(np.mean(np.abs(t - p)))


def _r2(t, p):
    t, p = np.asarray(t, np.float64), np.asarray(p, np.float64)
    ss_res = float(np.sum((t - p) ** 2))
    ss_tot = float(np.sum((t - np.mean(t)) ** 2))
    return float(1.0 - ss_res / ss_tot) if ss_tot > 1e-12 else np.nan


def loglife_to_raw_life(loglife) -> np.ndarray:
    x = np.asarray(loglife, dtype=np.float64)
    return np.power(10.0, np.clip(x, -30.0, 30.0))


def percentage_metrics(y_true_raw, y_pred_raw) -> Dict[str, float]:
    y_true_raw = np.asarray(y_true_raw, np.float64)
    y_pred_raw = np.asarray(y_pred_raw, np.float64)
    denom = np.clip(y_true_raw, 1e-12, None)
    pe = (y_pred_raw - y_true_raw) / denom * 100.0
    ape = np.abs(pe)
    return {"MAPE (%)": float(np.mean(ape)), "MPE (%)": float(np.mean(pe)), "Max_PE (%)": float(np.max(ape))}


def pooled_metrics_from_nodes(node_df: pd.DataFrame) -> pd.DataFrame:
    """Pooled Stress / LogLife metrics per (regime, ablation, model_family).

    Raw-life MAPE/MPE/Max_PE are retained as SECONDARY diagnostics only.
    """
    if node_df.empty:
        return pd.DataFrame()
    records: List[Dict[str, Any]] = []
    for keys, g in node_df.groupby(GROUP_COLS):
        regime, ablation, model_family = keys
        for target, tcol, pcol in [("Stress", "true_stress", "pred_stress"), ("LogLife", "true_loglife", "pred_loglife")]:
            t, p = g[tcol].to_numpy(), g[pcol].to_numpy()
            rec: Dict[str, Any] = {
                "regime": regime, "ablation": ablation, "model_family": model_family, "target": target,
                "MSE": _mse(t, p), "RMSE": _rmse(t, p), "MAE": _mae(t, p), "R2 (log)": _r2(t, p),
                "MAPE (%)": np.nan, "MPE (%)": np.nan, "Max_PE (%)": np.nan,
                "RMSE_raw": np.nan, "MSE_raw_life": np.nan, "R2_raw_life": np.nan,
            }
            if target == "LogLife":
                t_raw, p_raw = loglife_to_raw_life(t), loglife_to_raw_life(p)
                raw_mse = _mse(t_raw, p_raw)
                rec.update(percentage_metrics(t_raw, p_raw))
                rec["MSE_raw_life"] = raw_mse
                rec["RMSE_raw"] = float(np.sqrt(raw_mse))
                rec["R2_raw_life"] = _r2(t_raw, p_raw)
            records.append(rec)
    return pd.DataFrame(records).sort_values(GROUP_COLS + ["target"]).reset_index(drop=True)


# ---------------------------------------------------------------------------
# LogLife criticality bins
# ---------------------------------------------------------------------------

BIN_DEFS: List[Tuple[str, Optional[float], Optional[float]]] = [
    ("LogLife < 2", None, 2.0),
    ("2 <= LogLife < 3", 2.0, 3.0),
    ("3 <= LogLife < 4", 3.0, 4.0),
    ("4 <= LogLife < 6", 4.0, 6.0),
    ("LogLife >= 6", 6.0, None),
]


def loglife_bin_metrics(node_df: pd.DataFrame) -> pd.DataFrame:
    if node_df.empty:
        return pd.DataFrame()
    records: List[Dict[str, Any]] = []
    for keys, g in node_df.groupby(GROUP_COLS):
        regime, ablation, model_family = keys
        t_all = g["true_loglife"].to_numpy()
        p_all = g["pred_loglife"].to_numpy()
        for bin_name, lo, hi in BIN_DEFS:
            mask = np.ones_like(t_all, dtype=bool)
            if lo is not None:
                mask &= (t_all >= lo)
            if hi is not None:
                mask &= (t_all < hi)
            n = int(mask.sum())
            err = p_all[mask] - t_all[mask]
            unstable = n < MIN_BIN_NODES
            records.append({
                "regime": regime, "ablation": ablation, "model_family": model_family,
                "bin": bin_name, "n_nodes": n,
                "MAE": float(np.mean(np.abs(err))) if n else np.nan,
                "RMSE": float(np.sqrt(np.mean(err ** 2))) if n else np.nan,
                "signed_mean_error": float(np.mean(err)) if n else np.nan,
                "median_abs_error": float(np.median(np.abs(err))) if n else np.nan,
                "unstable": bool(unstable),
            })
    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# Zone / subzone metrics
# ---------------------------------------------------------------------------

def zone_metrics_from_nodes(node_df: pd.DataFrame, label_col: str = "subzone_name",
                             required_labels: Optional[Sequence[str]] = None) -> pd.DataFrame:
    """Compatibility wrapper that now returns grouped physical-region metrics.

    `label_col` and `required_labels` are ignored to preserve old call sites.
    """
    _ = label_col, required_labels
    return grouped_region_metrics_from_nodes(node_df)


def grouped_region_metrics_from_nodes(node_df: pd.DataFrame) -> pd.DataFrame:
    if node_df.empty:
        return pd.DataFrame()
    subzone_to_group = {
        subzone: group
        for group, subzones in GROUPED_REGION_DEFS.items()
        for subzone in subzones
    }
    node_df = node_df.copy()
    node_df["grouped_region"] = node_df["subzone_name"].map(subzone_to_group)
    records: List[Dict[str, Any]] = []
    for keys, g in node_df.groupby(GROUP_COLS):
        regime, ablation, model_family = keys
        for label, subzones in GROUPED_REGION_DEFS.items():
            sub = g[g["subzone_name"].isin(subzones)]
            if sub.empty:
                records.append({
                    "regime": regime, "ablation": ablation, "model_family": model_family,
                    "grouped_region": label, "n_nodes": 0,
                    "LogLife_MAE": np.nan, "LogLife_RMSE": np.nan,
                    "signed_mean_LogLife_error": np.nan, "median_abs_LogLife_error": np.nan,
                    "Stress_MAE": np.nan, "Stress_RMSE": np.nan, "status": "missing",
                })
                continue
            tl, pl = sub["true_loglife"].to_numpy(), sub["pred_loglife"].to_numpy()
            ts, ps = sub["true_stress"].to_numpy(), sub["pred_stress"].to_numpy()
            err_l = pl - tl
            finite_stress = np.isfinite(ts) & np.isfinite(ps)
            records.append({
                "regime": regime, "ablation": ablation, "model_family": model_family,
                "grouped_region": label, "n_nodes": int(len(sub)),
                "LogLife_MAE": _mae(tl, pl), "LogLife_RMSE": _rmse(tl, pl),
                "signed_mean_LogLife_error": float(np.mean(err_l)),
                "median_abs_LogLife_error": float(np.median(np.abs(err_l))),
                "Stress_MAE": _mae(ts[finite_stress], ps[finite_stress]) if finite_stress.any() else np.nan,
                "Stress_RMSE": _rmse(ts[finite_stress], ps[finite_stress]) if finite_stress.any() else np.nan,
                "status": "ok" if len(sub) >= MIN_ZONE_NODES else "unstable_low_count",
            })
    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# Geometry-level (per-sample) metrics
# ---------------------------------------------------------------------------

def geometry_level_metrics(node_df: pd.DataFrame) -> pd.DataFrame:
    if node_df.empty:
        return pd.DataFrame()
    records: List[Dict[str, Any]] = []
    for keys, g in node_df.groupby(GROUP_COLS + ["sample_id"]):
        regime, ablation, model_family, sample_id = keys
        g = g.reset_index(drop=True)
        true_life = g["true_loglife"].to_numpy()
        pred_life = g["pred_loglife"].to_numpy()
        true_stress = g["true_stress"].to_numpy()
        pred_stress = g["pred_stress"].to_numpy()

        true_crit_idx = int(np.argmin(true_life))
        pred_crit_idx = int(np.argmin(pred_life))
        true_max_s_idx = int(np.argmax(true_stress))
        pred_max_s_idx = int(np.argmax(pred_stress))

        dx = g["x_mm"].iloc[pred_crit_idx] - g["x_mm"].iloc[true_crit_idx]
        dr = g["r_mm"].iloc[pred_crit_idx] - g["r_mm"].iloc[true_crit_idx]
        crit_dist_mm = float(np.hypot(dx, dr))

        same_zone = bool(g["zone_id"].iloc[pred_crit_idx] == g["zone_id"].iloc[true_crit_idx])
        same_subzone = bool(g["subzone_id"].iloc[pred_crit_idx] == g["subzone_id"].iloc[true_crit_idx]) \
            if g["subzone_id"].notna().any() else None

        min_life_err = float(pred_life[true_crit_idx] - true_life[true_crit_idx])
        records.append({
            "regime": regime, "ablation": ablation, "model_family": model_family, "sample_id": sample_id,
            "whole_geometry_loglife_mae": _mae(true_life, pred_life),
            "whole_geometry_stress_mae": _mae(true_stress, pred_stress),
            "true_min_loglife": float(true_life[true_crit_idx]),
            "pred_min_loglife": float(pred_life[pred_crit_idx]),
            "min_loglife_error_decades": min_life_err,
            "abs_min_loglife_error_decades": float(abs(min_life_err)),
            "true_crit_x_mm": float(g["x_mm"].iloc[true_crit_idx]), "true_crit_r_mm": float(g["r_mm"].iloc[true_crit_idx]),
            "pred_crit_x_mm": float(g["x_mm"].iloc[pred_crit_idx]), "pred_crit_r_mm": float(g["r_mm"].iloc[pred_crit_idx]),
            "crit_node_distance_mm": crit_dist_mm,
            "true_max_stress": float(true_stress[true_max_s_idx]),
            "pred_max_stress": float(pred_stress[pred_max_s_idx]),
            "max_stress_error": float(pred_stress[pred_max_s_idx] - true_stress[true_max_s_idx]),
            "abs_max_stress_error": float(abs(pred_stress[pred_max_s_idx] - true_stress[true_max_s_idx])),
            "same_zone_critical": same_zone,
            "same_subzone_critical": same_subzone,
            "true_crit_zone": ZONE_ID_TO_NAME.get(int(g["zone_id"].iloc[true_crit_idx])),
            "true_crit_subzone": g["subzone_name"].iloc[true_crit_idx] if g["subzone_id"].notna().any() else None,
        })
    return pd.DataFrame(records)


def geometry_metrics_summary(geom_df: pd.DataFrame) -> pd.DataFrame:
    """Median / p90 / worst-case summary across geometries, per (regime, ablation, model)."""
    if geom_df.empty:
        return pd.DataFrame()
    cols = ["min_loglife_error_decades", "crit_node_distance_mm", "max_stress_error"]
    records = []
    for keys, g in geom_df.groupby(GROUP_COLS):
        regime, ablation, model_family = keys
        rec = {"regime": regime, "ablation": ablation, "model_family": model_family, "n_geometries": len(g)}
        for c in cols:
            vals = g[c].abs().to_numpy()
            rec[f"{c}_median_abs"] = float(np.median(vals))
            rec[f"{c}_p90_abs"] = float(np.percentile(vals, 90))
            rec[f"{c}_worst_abs"] = float(np.max(vals))
        rec["frac_same_zone_critical"] = float(g["same_zone_critical"].mean())
        records.append(rec)
    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# Representative geometry selection
# ---------------------------------------------------------------------------

def select_representative_geometries(geom_df: pd.DataFrame, regime: str, ablation: str,
                                      argent_family: str = "ArGEnT_self_att_noSDF",
                                      disagreement_family: str = "PointNetMLPJoint_FP") -> Dict[str, Any]:
    """Deterministically pick median / critical-life / model-disagreement sample_ids.

    Uses only geometries evaluated for all requested model families (shared IDs).
    """
    sub = geom_df[(geom_df["regime"] == regime) & (geom_df["ablation"] == ablation)]
    if sub.empty:
        return {}
    families = sorted(sub["model_family"].unique().tolist())
    shared_ids = set(sub["sample_id"].unique())
    for fam in families:
        shared_ids &= set(sub.loc[sub["model_family"] == fam, "sample_id"].unique())
    shared_ids = sorted(shared_ids)
    if not shared_ids:
        return {}
    sub = sub[sub["sample_id"].isin(shared_ids)]

    # Composite joint error per geometry, averaged across model families present.
    per_geom = sub.groupby("sample_id").apply(
        lambda g: float(np.mean(np.abs(g["min_loglife_error_decades"]).to_numpy()
                                 / max(np.abs(g["min_loglife_error_decades"]).to_numpy().std() or 1.0, 1e-6)
                                 + np.abs(g["max_stress_error"]).to_numpy()
                                 / max(np.abs(g["max_stress_error"]).to_numpy().std() or 1.0, 1e-6)))
    )
    median_val = per_geom.median()
    median_id = int((per_geom - median_val).abs().idxmin())

    true_min_by_geom = sub.groupby("sample_id")["true_min_loglife"].first()
    critical_id = int(true_min_by_geom.idxmin())

    disagreement_id = None
    if argent_family in families and disagreement_family in families:
        a = sub[sub["model_family"] == argent_family].set_index("sample_id")["min_loglife_error_decades"].abs()
        f = sub[sub["model_family"] == disagreement_family].set_index("sample_id")["min_loglife_error_decades"].abs()
        common = a.index.intersection(f.index)
        if len(common):
            diff = (a.loc[common] - f.loc[common]).abs()
            disagreement_id = int(diff.idxmax())

    return {"median": median_id, "critical_life": critical_id, "model_disagreement": disagreement_id}


def paired_argent_fp_diff(geom_df: pd.DataFrame,
                           argent_family: str = "ArGEnT_self_att_noSDF",
                           fp_family: str = "PointNetMLPJoint_FP") -> pd.DataFrame:
    """Per-geometry ArGEnT-minus-FP |min-LogLife error| difference.

    Sign convention: positive => FP has smaller absolute critical-life error than ArGEnT
    (i.e. FP is better for that geometry). Negative => ArGEnT is better.
    """
    records = []
    for (regime, ablation), g in geom_df.groupby(["regime", "ablation"]):
        a = g[g["model_family"] == argent_family].set_index("sample_id")["min_loglife_error_decades"].abs()
        f = g[g["model_family"] == fp_family].set_index("sample_id")["min_loglife_error_decades"].abs()
        common = a.index.intersection(f.index)
        for sid in common:
            records.append({
                "regime": regime, "ablation": ablation, "sample_id": sid,
                "argent_abs_error": float(a.loc[sid]), "fp_abs_error": float(f.loc[sid]),
                "argent_minus_fp": float(a.loc[sid] - f.loc[sid]),
            })
    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def _save_fig(fig, out_dir: Path, name: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_dir / f"{name}.png", dpi=150, bbox_inches="tight")
    try:
        fig.savefig(out_dir / f"{name}.pdf", bbox_inches="tight")
    except Exception:
        pass


def robust_signed_limit(err_arrays: Sequence[np.ndarray], pct: float = 99.0, floor: float = 1e-6) -> float:
    all_abs = np.concatenate([np.abs(np.asarray(a)) for a in err_arrays if len(a)])
    if all_abs.size == 0:
        return floor
    return float(max(np.percentile(all_abs, pct), floor))


def plot_field_comparison(geom_nodes_by_model: Dict[str, pd.DataFrame], field_true_col: str, field_pred_col: str,
                           error_unit: str, title_prefix: str, fixed_error_limit: Optional[float] = None,
                           mark_extrema: str = "min", out_dir: Optional[Path] = None, filename: Optional[str] = None):
    """Common true/pred colour limits and one common symmetric error limit across models."""
    models = list(geom_nodes_by_model.keys())
    all_true = np.concatenate([geom_nodes_by_model[m][field_true_col].to_numpy() for m in models])
    all_pred = np.concatenate([geom_nodes_by_model[m][field_pred_col].to_numpy() for m in models])
    vmin, vmax = float(min(all_true.min(), all_pred.min())), float(max(all_true.max(), all_pred.max()))

    errs = [geom_nodes_by_model[m][field_pred_col].to_numpy() - geom_nodes_by_model[m][field_true_col].to_numpy() for m in models]
    err_limit = fixed_error_limit if fixed_error_limit is not None else robust_signed_limit(errs)
    enorm = TwoSlopeNorm(vmin=-err_limit, vcenter=0.0, vmax=err_limit)

    fig, axes = plt.subplots(3, len(models), figsize=(5.2 * len(models), 13.5), squeeze=False)
    for j, m in enumerate(models):
        d = geom_nodes_by_model[m]
        x, r = d["x_mm"].to_numpy(), d["r_mm"].to_numpy()
        t, p = d[field_true_col].to_numpy(), d[field_pred_col].to_numpy()
        err = p - t

        ax = axes[0, j]
        sc = ax.scatter(x, r, c=t, vmin=vmin, vmax=vmax, cmap="viridis", s=10)
        ax.set_title(f"{m}\nTrue"); fig.colorbar(sc, ax=ax)

        ax = axes[1, j]
        sc = ax.scatter(x, r, c=p, vmin=vmin, vmax=vmax, cmap="viridis", s=10)
        ax.set_title("Predicted"); fig.colorbar(sc, ax=ax)

        ax = axes[2, j]
        sc = ax.scatter(x, r, c=err, cmap="RdBu_r", norm=enorm, s=10)
        ax.set_title(f"Signed error ({error_unit})"); fig.colorbar(sc, ax=ax)

        if mark_extrema == "min":
            ti, pi = int(np.argmin(t)), int(np.argmin(p))
        else:
            ti, pi = int(np.argmax(t)), int(np.argmax(p))
        # Compute equal-aspect bounds from the coordinate data so the disc
        # reads as a disc rather than an I-beam-like elongated shape.
        x_c = float(np.nanmean([x.min(), x.max()]))
        r_c = float(np.nanmean([r.min(), r.max()]))
        half_range = max(
            float(np.nanmax(np.abs(x - x_c))),
            float(np.nanmax(np.abs(r - r_c))),
        ) * 1.05 + 1e-6
        for ax in axes[:, j]:
            ax.scatter([x[ti]], [r[ti]], marker="*", s=160, edgecolor="k", facecolor="lime", label="true extremum", zorder=5)
            ax.scatter([x[pi]], [r[pi]], marker="X", s=120, edgecolor="k", facecolor="orange", label="pred extremum", zorder=5)
            ax.set_xlabel("x (mm)"); ax.set_ylabel("r (mm)")
            ax.set_aspect("equal", adjustable="box")
            ax.set_xlim(x_c - half_range, x_c + half_range)
            ax.set_ylim(r_c - half_range, r_c + half_range)
        axes[0, j].legend(loc="upper right", fontsize=7)

    fig.suptitle(title_prefix)
    fig.tight_layout()
    if out_dir is not None and filename:
        _save_fig(fig, out_dir, filename)
    return fig


def plot_arc_length_error(geom_nodes_by_model: Dict[str, pd.DataFrame], title_prefix: str,
                           out_dir: Optional[Path] = None, filename: Optional[str] = None):
    models = list(geom_nodes_by_model.keys())
    fig, axes = plt.subplots(3, 1, figsize=(10, 9), sharex=True)
    for m in models:
        d = geom_nodes_by_model[m].sort_values("arc_length_mm")
        if d["arc_length_mm"].isna().all():
            continue
        s = d["arc_length_mm"].to_numpy()
        axes[0].plot(s, d["pred_stress"] - d["true_stress"], label=m, alpha=0.8)
        axes[1].plot(s, d["pred_loglife"] - d["true_loglife"], label=m, alpha=0.8)
        axes[2].plot(s, d["true_loglife"], label=m, alpha=0.8)

    # zone boundaries from the first model's data (zones are geometry properties, model-independent)
    ref = geom_nodes_by_model[models[0]].sort_values("arc_length_mm")
    if ref["arc_length_mm"].notna().any():
        boundaries = ref.groupby("subzone_name")["arc_length_mm"].agg(["min", "max"]).dropna()
        for name, row in boundaries.iterrows():
            for ax in axes:
                ax.axvspan(row["min"], row["max"], alpha=0.04)

    axes[0].set_ylabel("Signed Stress error (MPa)")
    axes[1].set_ylabel("Signed LogLife error (decades)")
    axes[2].set_ylabel("True LogLife")
    axes[2].set_xlabel("Arc length (mm)")
    for ax in axes:
        ax.legend(fontsize=7)
        ax.axhline(0, color="k", lw=0.6)
    fig.suptitle(title_prefix)
    fig.tight_layout()
    if out_dir is not None and filename:
        _save_fig(fig, out_dir, filename)
    return fig


def plot_zone_bar(zone_df: pd.DataFrame, title: str, out_dir: Optional[Path] = None, filename: Optional[str] = None):
    d = zone_df.copy()
    d = d[d["status"] != "missing"]
    if d.empty:
        return None
    fig, ax = plt.subplots(figsize=(11, 5))
    labels = sorted(d["subzone_name"].unique(), key=lambda z: PRINCIPAL_SUBZONES.index(z) if z in PRINCIPAL_SUBZONES else 99)
    families = sorted(d["model_family"].unique())
    x = np.arange(len(labels), dtype=float)
    width = 0.8 / max(1, len(families))
    for i, fam in enumerate(families):
        sub = d[d["model_family"] == fam].set_index("subzone_name")
        vals = [sub.loc[l, "MAE"] if l in sub.index else np.nan for l in labels]
        counts = [sub.loc[l, "n_nodes"] if l in sub.index else 0 for l in labels]
        bars = ax.bar(x + (i - (len(families) - 1) / 2) * width, vals, width=width, label=fam)
        for b, n in zip(bars, counts):
            ax.text(b.get_x() + b.get_width() / 2, (b.get_height() or 0), f"n={int(n)}", ha="center", va="bottom", fontsize=6, rotation=90)
    ax.set_xticks(x); ax.set_xticklabels(labels, rotation=30, ha="right")
    ax.set_ylabel("LogLife MAE"); ax.set_title(title); ax.legend(fontsize=7)
    fig.tight_layout()
    if out_dir is not None and filename:
        _save_fig(fig, out_dir, filename)
    return fig


def plot_bin_bar(bin_df: pd.DataFrame, title: str, out_dir: Optional[Path] = None, filename: Optional[str] = None):
    if bin_df.empty:
        return None
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))
    bins = [b for b, _, _ in BIN_DEFS]
    families = sorted(bin_df["model_family"].unique())
    for ax, metric in zip(axes, ["MAE", "RMSE"]):
        x = np.arange(len(bins), dtype=float)
        width = 0.8 / max(1, len(families))
        for i, fam in enumerate(families):
            sub = bin_df[bin_df["model_family"] == fam].set_index("bin")
            vals = [sub.loc[b, metric] if b in sub.index else np.nan for b in bins]
            unstable = [sub.loc[b, "unstable"] if b in sub.index else True for b in bins]
            bars = ax.bar(x + (i - (len(families) - 1) / 2) * width, vals, width=width, label=fam)
            for b_, u in zip(bars, unstable):
                if u:
                    ax.text(b_.get_x() + b_.get_width() / 2, (b_.get_height() or 0), "unstable", ha="center", va="bottom", fontsize=6, color="red", rotation=90)
        ax.set_xticks(x); ax.set_xticklabels(bins, rotation=20)
        ax.set_ylabel(f"LogLife {metric}"); ax.legend(fontsize=7)
    fig.suptitle(title)
    fig.tight_layout()
    if out_dir is not None and filename:
        _save_fig(fig, out_dir, filename)
    return fig


def plot_geometry_scatter(geom_df: pd.DataFrame, out_dir: Optional[Path] = None, filename_prefix: Optional[str] = None):
    figs = []
    families = sorted(geom_df["model_family"].unique())

    fig, ax = plt.subplots(figsize=(6, 6))
    for fam in families:
        d = geom_df[geom_df["model_family"] == fam]
        ax.scatter(d["true_min_loglife"], d["pred_min_loglife"], s=14, alpha=0.6, label=fam)
    lims = [geom_df["true_min_loglife"].min(), geom_df["true_min_loglife"].max()]
    ax.plot(lims, lims, "k--", lw=1)
    ax.set_xlabel("True minimum LogLife"); ax.set_ylabel("Predicted minimum LogLife")
    ax.legend(fontsize=7); fig.tight_layout()
    if out_dir is not None and filename_prefix:
        _save_fig(fig, out_dir, f"{filename_prefix}_min_loglife_scatter")
    figs.append(fig)

    fig, ax = plt.subplots(figsize=(6, 6))
    for fam in families:
        d = geom_df[geom_df["model_family"] == fam]
        ax.scatter(d["true_max_stress"], d["pred_max_stress"], s=14, alpha=0.6, label=fam)
    lims = [geom_df["true_max_stress"].min(), geom_df["true_max_stress"].max()]
    ax.plot(lims, lims, "k--", lw=1)
    ax.set_xlabel("True maximum stress (MPa)"); ax.set_ylabel("Predicted maximum stress (MPa)")
    ax.legend(fontsize=7); fig.tight_layout()
    if out_dir is not None and filename_prefix:
        _save_fig(fig, out_dir, f"{filename_prefix}_max_stress_scatter")
    figs.append(fig)

    fig, ax = plt.subplots(figsize=(7, 5))
    for fam in families:
        d = geom_df[geom_df["model_family"] == fam]
        ax.hist(d["min_loglife_error_decades"], bins=20, alpha=0.5, label=fam)
    ax.set_xlabel("Per-geometry min-LogLife error (decades)"); ax.set_ylabel("Count")
    ax.legend(fontsize=7); ax.axvline(0, color="k", lw=0.8); fig.tight_layout()
    if out_dir is not None and filename_prefix:
        _save_fig(fig, out_dir, f"{filename_prefix}_min_loglife_error_hist")
    figs.append(fig)
    return figs


def plot_geometry_error_distributions(
    geom_df: pd.DataFrame,
    title: str,
    out_dir: Optional[Path] = None,
    filename: Optional[str] = None,
):
    if geom_df.empty:
        return None
    families = sorted(geom_df["model_family"].unique())
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    for fam in families:
        d = geom_df[geom_df["model_family"] == fam]
        axes[0].hist(d["whole_geometry_loglife_mae"], bins=20, alpha=0.45, label=fam)
        axes[1].hist(d["abs_min_loglife_error_decades"], bins=20, alpha=0.45, label=fam)
    axes[0].set_title("A. Per-geometry whole-field LogLife MAE")
    axes[0].set_xlabel("MAE (decades)")
    axes[0].set_ylabel("Count")
    axes[1].set_title("B. Per-geometry absolute minimum-LogLife error")
    axes[1].set_xlabel("|error| (decades)")
    axes[1].set_ylabel("Count")
    for ax in axes:
        ax.legend(fontsize=7)
    fig.suptitle(title)
    fig.tight_layout()
    if out_dir is not None and filename:
        _save_fig(fig, out_dir, filename)
    return fig


def save_table(df: pd.DataFrame, out_dir: Path, name: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_dir / f"{name}.csv", index=False)


def save_json(obj: Any, out_dir: Path, name: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / f"{name}.json", "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, default=str)
