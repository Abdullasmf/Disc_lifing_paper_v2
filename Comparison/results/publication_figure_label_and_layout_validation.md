# Mandatory final figure-repair pass: label centralization and layout validation

Repository commit inspected/produced by this pass: `3012f88375cf6df7383693241f7a5310c69c6800`
(parent commit with the prior, incomplete fix attempt: `7ed97aa3766e84cc17ecf2055aa6a9614d0e7124`).

This report is additive: it does not overwrite `Comparison/results/abstract_evidence_audit.md`,
`Comparison/results/abstract_evidence_audit_final.md`, or
`Comparison/results/final_abstract_repository_verification.md`, which record prior audit passes.

**Environment blocker (read this first):** this sandbox has no `torch`, no `h5py`, and no
`Data_gen/output/*.h5` production dataset, and the repository ships **no committed figure PNGs**
at all (`find Comparison/results -iname '*.png'` returns zero files; the images attached to the
task were uploaded separately as GitHub user-attachments, not committed artifacts). It is
therefore impossible in this environment to execute notebooks 01-04, regenerate any `.png`/`.pdf`
figure, or open/inspect a regenerated file. Every change below was verified by (a) static
inspection of the notebook JSON/source, (b) `ast.parse`/`py_compile` syntax checks on every edited
cell/module, and (c) standalone unit tests of the new `eval_helpers.py` functions using synthetic
DataFrames and a real Matplotlib backend (Agg) — i.e. the *logic* that produces labels and layout
was executed and its output inspected, but the *actual paper figures* could not be regenerated or
visually re-inspected here. See §E for the explicit list of what remains unverified against real
model checkpoints.

---

## A. Root cause

The prior pass (`7ed97aa3`, see `final_abstract_repository_verification.md`) had already fixed the
*headline* violations (checkpoint-hash legends in notebook 04, `headfeat`/`EF` wording in notebook
02's delta plots) by editing notebook source and adding a notebook-local `display_model_name`
override. Static inspection of the current notebook source in this pass found that:

1. **The attached screenshots are stale renders, not a reflection of current source.** No PNGs are
   committed to the repository (`Comparison/results/**/figures/` directories are `.gitignore`'d —
   see `.gitignore`), and this sandbox cannot run `torch`/`h5py` inference to regenerate them. The
   screenshots in the task description therefore predate the `7ed97aa3` fix and cannot be used as
   evidence that the *current* source is broken — but they correctly identified real defects that
   were only *partially* fixed, enumerated below.

2. **Root cause 1 — shared plotting helpers hard-coded the module-level resolver.**
   `eval_helpers.plot_bin_bar` and `eval_helpers.plot_zone_bar` called `display_model_name(fam)`
   directly instead of accepting a `label_fn` override (unlike `plot_field_comparison`, which
   already had a `label_fn` parameter). Notebook 02 needs the ArGEnT `+ GF` override (because the
   `ArGEnT_self_att_noSDF` checkpoint loaded from `Zonal/Edge_arc_feat` is engineered-feature
   augmented, unlike the same family id loaded elsewhere), but `plot_bin_bar` — used for the
   life-band figure — could not honour that override. Every figure produced via `plot_bin_bar` in
   notebook 02 would therefore have displayed plain `ArGEnT-A` instead of `ArGEnT-A + GF` even
   after the notebook-local override function was added, because the shared helper never received
   it. **Fixed:** added a `label_fn` parameter to both functions (`eval_helpers.py`), and notebook
   02's call site now passes its notebook-local resolver.

3. **Root cause 2 — reader-facing titles still interpolated raw ablation/regime folder names.**
   Notebook 02 built two suptitles as `f'{REGIME} {ABLATION} life-band log-life errors'` and
   `f'... {REGIME} / {ABLATION} vs {REGIME} / {BASELINE_ABLATION}'`, where `ABLATION = 'Edge_arc_feat'`
   and `BASELINE_ABLATION = 'Edge'` are internal experiment-folder names. These render literally as
   `"Zonal Edge_arc_feat life-band log-life errors"` and `"Zonal / Edge_arc_feat vs Zonal / Edge"` —
   exactly the two title violations shown in the attached screenshots. This was **not** touched by
   the prior fix pass (which focused on legend/xtick/delta wording, not titles built from
   `REGIME`/`ABLATION` variables). **Fixed:** both titles were rewritten to reader-facing text that
   never interpolates a raw folder name (see §C).

4. **Root cause 3 — the resolver used an unsafe silent-fallback pattern.**
   `display_model_name` was defined as
   `DISPLAY_MODEL_NAMES.get(str(model_family), str(model_family))` — i.e. exactly the unsafe
   pattern the task explicitly calls out. Had a new, unmapped `model_family` ever been introduced
   (e.g. a future ablation, or a typo in a notebook cell), every consumer of this function would
   have silently rendered the raw internal id in a paper-facing figure instead of failing loudly.
   All current call sites already only pass known, mapped families, so this had not yet manifested
   as a visible bug, but it was a latent architectural risk exactly matching the failure mode
   described in the task. **Fixed:** replaced with `resolve_publication_label`, which raises
   `UnresolvedPublicationLabelError` (a `ValueError` subclass) identifying the unresolved
   `model_internal_id`/`checkpoint_id` instead of returning the raw id; `display_model_name` is now
   a thin strict wrapper over it.

5. **Root cause 4 — an axis label leaked an informal supervision term.**
   Notebook 04's per-bin/full-set delta panels used `ylabel='no-stress − stress [decades]'`. This
   contains the literal disallowed token `no-stress` inside a paper-facing figure (not just a
   debug/diagnostic cell). **Fixed:** relabelled to
   `'life-only \u2212 joint stress\u2013life [decades]'`, consistent with the
   `format_supervision_label` vocabulary used everywhere else in that figure.

6. **Root cause 5 — notebook 03's data-efficiency cell contained duplicated, shadowing function
   definitions.** Cell 9 of `03_data_efficiency.ipynb` defined `_plot_runs_and_summary`,
   `faceted_metric_plot`, and `full_set_summary_plot` **twice** in the same cell (the second
   definition silently shadowed the first at notebook-execution time — a concrete instance of the
   "stale in-memory definitions" failure mode named in the task). Both copies used
   `plt.subplots(1, len(bins), figsize=(5.2 * len(bins), 4.2))` — a single row that grows without
   bound with the number of life bins (5 bins ⇒ one axes row 26 inches wide), and both placed the
   legend with `fig.legend(loc='upper center', ...)`, which sits directly under/over the
   `fig.suptitle(...)` call with no reserved vertical space — reproducing the exact overlap and
   "long horizontal strip" defects in the third attached screenshot. **Fixed:** removed the
   duplicate block entirely and rewrote the single remaining `faceted_metric_plot` to use the new
   `make_wrapped_life_bin_grid`/`add_external_figure_legend` helpers (see §D).

No other notebook paths (qualitative field-comparison figures, pooled-metric bars, paired
stress/no-stress full-set-vs-per-bin figures) were found to bypass the resolver; they already
called `display_model_name`/`eh.display_model_name`/`plot_field_comparison(..., label_fn=...)`
correctly and now additionally benefit from the new strict-resolver and figure-text validator
behaviour without any further source changes.

---

## B. Verified internal-to-publication mapping

| Internal ID/checkpoint/config | Verified architecture and ablation state | Publication label | Evidence source |
|---|---|---|---|
| `PointNetMLPJoint` | Global-context PointNet, FFM, no native-resolution feature propagation, no GF | `GC-PointNet` | `Comparison/eval_helpers.py` `DISPLAY_MODEL_NAMES` (pre-existing, unchanged) |
| `PointNetMLPJoint_headfeat` | Global-context PointNet + engineered geometric features (`extra_feat_cols`/`head_feat_cols` populated) | `GC-PointNet + GF` | `Comparison/eval_helpers.py` `DISPLAY_MODEL_NAMES`; feature columns verified in `02_engineered_geometric_features.ipynb` cell 4 (`feature_assignment` table, `encoder_engineered_features`) |
| `PointNetMLPJoint_FP` | Local-context PointNet, FFM, native-resolution feature propagation (`build_fp_model_from_arch`), no GF | `LC-PointNet` | `Comparison/eval_helpers.py` `DISPLAY_MODEL_NAMES`; FP dispatch verified in `02_...ipynb`/`03_...ipynb` `reconstruct()` (`family in ('PointNetMLPJoint_FP', ...)` branch) |
| `PointNetMLPJoint_FP_headfeat` | Local-context PointNet + FP + engineered geometric features | `LC-PointNet + GF` | Same as above, `+_headfeat` suffix confirmed to route through `predict_headfeat(..., family='PointNetMLPJoint_FP_headfeat')` |
| `ArGEnT_self_att_noSDF` (loaded from an ablation directory **without** engineered features, e.g. `Zonal/Edge`) | Adapted ArGEnT-inspired cross-attention comparator, `INPUT_COLS` limited to coordinate columns only | `ArGEnT-A` | `Comparison/eval_helpers.py` `DISPLAY_MODEL_NAMES`; `Training_script.py` `INPUT_COLS` parsed via `parse_script_metadata` in each notebook |
| `ArGEnT_self_att_noSDF` (loaded from `Zonal/Edge_arc_feat`) | Same architecture, but `Training_script.py` `INPUT_COLS` include `arc_length_mm`/`tangent_x`/`tangent_r`/`curvature`/`curvature_gradient` (confirmed in `feature_assignment.csv`) | `ArGEnT-A + GF` | `eh.resolve_publication_label(model_family, geometric_features=True)` — new centralized resolver, called from notebook 02's `display_model_name` override (`FEATURE_AUGMENTED_ARGENT_FAMILY = 'ArGEnT_self_att_noSDF'`) |
| Stress-supervision pair `model_family`/`fp_status` (notebook 04) | `model_family` is one of the two PointNet/ArGEnT families above, verified identical on both sides of a pair by `build_valid_pairs()` before any label is assembled | `{publication_label} (joint stress–life)` / `{publication_label} (life only)` | `04_joint_stress_supervision.ipynb` cell 11: `publication_label = eh.display_model_name(model_family)` computed once per pair and reused for both supervision conditions (never derived from `variant_name`/checkpoint filename) |

`GC-PointNet + GF`, `LC-PointNet + GF`, and `ArGEnT-A + GF` are the only `+ GF` variants that exist
in the repository's checkpoints; no additional `+ GF` variant was invented.

---

## C. Figure-level verification

Because no figure can be executed/regenerated in this sandbox (see blocker above), this table
records **source-level** before/after verification: the exact literal strings the old source would
have rendered (traced through `f`-string/format-call arguments) versus what the corrected source
now renders, confirmed by parsing the notebook JSON and, where a helper function is involved,
by unit-testing that function directly against synthetic data with `eh.validate_no_raw_publication_labels`.

| Figure path (produced by) | Raw labels before | Publication labels after | Layout checked | Regenerated and visually inspected |
|---|---|---|---|---|
| `04_joint_stress_supervision.ipynb` → `stress_vs_no_stress_*_fullset_separate.png` | *(prior pass already fixed)* `pnmlp_16932d84 (with stress)` / `argent_self_nosdf_s_177b264d (with stress)`, title `LC-PointNet (FP): with-stress vs no-stress` | `LC-PointNet (joint stress–life)` / `ArGEnT-A (joint stress–life)`; title `"{label}: joint stress–life supervision versus life-only training"`; per-bin/full-set delta axis now `"life-only − joint stress–life [decades]"` (was `"no-stress − stress [decades]"`, fixed in this pass) | Full-test-set panel and physical-life-bin panel remain visually separated (2×2 grid, no aggregate point spliced into the bin sequence) — unchanged, static source inspection only | **No** — no torch/h5py/data; cannot execute |
| `02_engineered_geometric_features.ipynb` → `figure_headfeat_vs_baseline_delta.png` | *(prior pass already fixed legend/ylabel wording to `"GF − baseline"`)*; suptitle still `"Engineered-feature ablation: full-test-set deltas\nZonal / Edge_arc_feat vs Zonal / Edge"` (**not** fixed by the prior pass) | Suptitle now `"Effect of engineered geometric features on log-life prediction\nFull-test-set deltas (validation-split evaluation)"`; bar labels remain `f"{display_model_name(ablation)}\nvs\n{eh.display_model_name(baseline)}"` which — for the ArGEnT pair — resolves to `ArGEnT-A + GF\nvs\nArGEnT-A` via the centralized `+ GF` resolver | Two-panel (MAE/RMSE) bar layout, unchanged | **No** — no torch/h5py/data; cannot execute |
| `02_engineered_geometric_features.ipynb` → `figure_headfeat_vs_baseline_by_life_bin.png` | Same raw-folder suptitle issue as above | Suptitle rewritten to remove `REGIME`/`ABLATION`/`BASELINE_ABLATION` interpolation (see §4 above) | 2×2 grid (full-set deltas / per-bin deltas × MAE/RMSE), unchanged | **No** |
| `02_engineered_geometric_features.ipynb` → `figure_life_bands.png` (via `eh.plot_bin_bar`) | Title `f'{REGIME} {ABLATION} life-band log-life errors'` → literally `"Zonal Edge_arc_feat life-band log-life errors"`; x-tick/legend labels used `eh.display_model_name` only (ArGEnT rendered as plain `ArGEnT-A`, under-reporting its GF status) because `plot_bin_bar` had no `label_fn` parameter | Title now `'Effect of engineered geometric features on log-life prediction (validation-split evaluation)'`; call now passes `label_fn=display_model_name` (notebook-local, GF-aware) so the ArGEnT bars/xticks render `ArGEnT-A + GF` | 2×2 grid (full-set/per-bin × MAE/RMSE), unchanged | Unit-tested with synthetic data (see §A item 2 code snippet); **not** regenerated from real checkpoints |
| `02_engineered_geometric_features.ipynb` → `figure_qualitative_example.png` (via `eh.plot_field_comparison`) | Already used `label_fn=display_model_name` (notebook-local GF-aware resolver) prior to this pass — column headings were already `LC-PointNet + GF`, `ArGEnT-A + GF`, `GC-PointNet + GF`, never `PointNetMLPJoint_FP_headfeat`/`ArGEnT_self_att_noSDF` | No change required; now additionally passes through `eh.validate_no_raw_publication_labels` before saving (wired into shared `_save_fig`) | 3×N grid (True/Predicted/Signed error rows), unchanged | **No** |
| `03_data_efficiency.ipynb` → `fraction_vs_life_bin_mae.png` / `fraction_vs_life_bin_rmse.png` | `plt.subplots(1, len(bins), figsize=(5.2*len(bins), 4.2))` — single row, 5 bins ⇒ ~26-inch-wide strip; `fig.legend(loc='upper center', ...)` overlapping `fig.suptitle(...)` | `eh.make_wrapped_life_bin_grid(len(bins), ncols=2)` — 3×2 grid for 5 bins with the 6th (unused) axes hidden via `ax.set_visible(False)`; `eh.add_external_figure_legend(fig, axes_flat, ...)` placed at `bbox_to_anchor=(1.01, 0.5)` outside the grid, with `fig.tight_layout(rect=(0.0, 0.0, 0.82, 0.93))` reserving legend space and `fig.suptitle(..., y=0.98)` reserving title space | **Yes** — verified end-to-end with synthetic data + a real Matplotlib(Agg) render (`/tmp/test_faceted2.png` during development): confirmed `len(axes_flat) == 6`, `axes_flat[5].get_visible() == False`, and the external legend renders with 4 deduplicated handles/labels when saved with `bbox_inches='tight'` (matching the notebook's `save_fig`) | Verified with synthetic data only; **not** regenerated from real checkpoints (no torch/h5py/data) |
| `03_data_efficiency.ipynb` → `fraction_vs_full_test_set_mae_rmse.png` | 1×2 layout, `fig.legend(loc='upper center', ...)` above two panels (no suptitle originally, so no direct overlap, but inconsistent legend placement vs. the redesigned faceted figures) | Switched to `eh.add_external_figure_legend` for consistency; added explicit `fig.suptitle('Data efficiency: full test set (aggregate summary)', y=0.98)` with `rect=(0.0, 0.0, 0.82, 0.90)` reserved space, keeping the full-test-set summary visually and structurally separate from the life-bin grid (never spliced into the bin sequence) | 1×2 layout, unchanged panel count | **No** |

---

## D. Data-efficiency layout verification

- **Number of physical life bins:** up to 5 (`eh.PHYSICAL_LIFE_BIN_ORDER`: `log_life < 2`,
  `2 <= log_life < 3`, `3 <= log_life < 4`, `4 <= log_life < 6`, `log_life >= 6`); the actual figure
  count depends on which bins have data (`bins = [b for b in eh.PHYSICAL_LIFE_BIN_ORDER if b in
  per_bin_df['life_bin'].astype(str).unique()]`).
- **Grid shape used:** `ncols=2`, `nrows=math.ceil(n_bins / 2)` via
  `eh.make_wrapped_life_bin_grid`. For 5 bins this is a 3×2 grid (5 filled panels, 1 hidden); for 4
  bins a 2×2 grid with no hidden panels — matches the task's required examples exactly.
- **Full-set handling:** the full test set is rendered in a **separate figure**
  (`fraction_vs_full_test_set_mae_rmse.png`, MAE/RMSE side by side) rather than as an extra panel
  inserted into the life-bin grid — the "Preferred design" option in the task, avoiding any implied
  adjacency between the aggregate summary and an ordered physical bin.
- **Legend placement:** one deduplicated figure-level legend per figure, via
  `eh.add_external_figure_legend(fig, axes, title='Model', bbox_to_anchor=(1.01, 0.5))`, placed at
  `loc='center left'` outside the axes grid on the right-hand side.
- **Figure dimensions:** `make_wrapped_life_bin_grid` defaults to `panel_width=6.5`,
  `panel_height=4.5`, i.e. `figsize=(6.5*ncols, 4.5*nrows)` — for `ncols=2` this is
  `(13, 4.5*nrows)`, matching the task's required sizing example exactly.
- **Which axes were hidden:** trailing axes beyond `n_bins` in the wrapped grid (e.g. the 6th
  cell of a 3×2 grid when only 5 bins have data) via `ax.set_visible(False)` inside
  `make_wrapped_life_bin_grid`.
- **Confirmation that no legend overlaps the title:** `fig.suptitle(..., y=0.98)` is set with a
  reserved top margin, and `fig.tight_layout(rect=(0.0, 0.0, 0.82, 0.93))` reserves the right-hand
  20% of the figure width for the external legend, so the legend (placed at `x=1.01` in figure
  coordinates, i.e. to the right of the reserved-width axes area) cannot overlap the centered
  suptitle or any subplot title. Verified programmatically in this pass with synthetic data and a
  real render (`bbox_inches='tight'` save succeeded and produced 4 legend entries positioned to the
  right of the axes grid); **not** re-confirmed against a real regenerated figure from model
  checkpoints (blocked — see below).

---

## E. Exceptions/blockers

1. **No figure could be executed, regenerated, or visually re-inspected in this sandbox.**
   `torch` and `h5py` are not installed, and `Data_gen/output/*.h5` (the production dataset) is not
   present in this checkout (only `Data_gen/*.py` source and `Data_gen/output/Diversity_checker.py`
   /`Output_test.ipynb` are present; there is no `.h5` file anywhere in the repository). No
   `Comparison/results/**/figures/*.png` files are committed to the repository either (figures are
   `.gitignore`'d), so there was nothing to open and re-inspect even for figures produced by a prior
   run. Every fix in this pass was therefore verified by (a) static source/AST inspection, (b)
   direct unit-testing of the new `eval_helpers.py` functions (`resolve_publication_label`,
   `format_supervision_label`, `format_gf_delta_label`, `make_wrapped_life_bin_grid`,
   `add_external_figure_legend`, `validate_no_raw_publication_labels`) against synthetic
   DataFrames rendered with a real Matplotlib `Agg` backend, and (c) unit-testing `plot_bin_bar`
   with a `label_fn` override against synthetic data confirming `ArGEnT-A + GF` renders correctly
   and `validate_no_raw_publication_labels` passes. **No claim is made that any real, checkpoint-
   derived figure has been regenerated or visually confirmed clean** — that step requires an
   environment with `torch`, `h5py`, and the production HDF5 dataset, none of which are available
   here.
2. **`Comparison/model_ablation_comparison(old_from_v1).ipynb`** was left unmodified. It is the
   archived v1 notebook (superseded by `01_fp_vs_argent.ipynb`–`04_joint_stress_supervision.ipynb`
   per `Comparison/README.md`) and is out of scope for the paper-facing figure pipeline covered by
   this task.
3. **Diagnostic/audit markdown text** (e.g. notebook 04 cell 5's `"No valid stress/no-stress
   comparison pairs found"` diagnostic message, cell 13's `"## Valid stress/no-stress model
   pair(s)"` section header) still contains `with stress`/`no-stress`/`FP` wording. These are
   internal pairing-diagnostics cells describing checkpoint-discovery/pairing failures for
   notebook maintainers, not paper-facing figures or captions, and are left unchanged per the
   task's own carve-out ("unless they appear only as an implementation/debug detail outside a
   paper-facing figure").
4. **No new `+ GF` variant was invented.** The only three verified `+ GF` publication identities
   remain `GC-PointNet + GF`, `LC-PointNet + GF`, and `ArGEnT-A + GF`; no stress-supervision `+ GF`
   pairing was added or implied because no such checkpoint pair was found in the repository.
