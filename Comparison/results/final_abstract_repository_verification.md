# Final publication verification pass

Repository commit inspected: `8892d544e4162a8e27dd68f287a2e5d86f2662b9`

This report is additive: it does not overwrite `Comparison/results/abstract_evidence_audit.md`
or `Comparison/results/abstract_evidence_audit_final.md`, which record prior audit passes.

No notebook was executed in this environment (`torch`/`h5py` are not installed and
`Data_gen/output/*.h5` is not present in this checkout). All findings below are based on
static code/notebook inspection and the CSV/JSON/Markdown artifacts already committed
under `Comparison/results/**` from a prior local execution (see `run_metadata.json`/
`dataset_status.json` in each results subfolder, which record the original Windows path
`c:\Users\abfat\Desktop\Disc_lifing_paper_v2\...`). Numeric verification below recomputes
directly from those committed row values.

---

## 1. Publication-label audit and fixes made

| File | Figure/table | Raw label found | Verified identity | Publication label | Fixed |
|---|---|---|---|---|---|
| `Comparison/04_joint_stress_supervision.ipynb` (cell 11, figure `stress_vs_no_stress_*`) | Full-test-set bar panel + physical life-bin panel legends, figure `suptitle` | `f'{eh.display_model_name(stress_variant)} (with stress)'` / `... (no stress)'`, where `stress_variant`/`no_stress_variant` were bound to `variant_name = path.stem` (raw checkpoint filenames, e.g. `pnmlp_16932d84`, `pnmlp_1bbaae12`) instead of `model_family` | The pairing rule in the same notebook (`build_valid_pairs`) already requires `model_family` and `fp_status` to match between the stress and no-stress checkpoint, so both sides of a pair share one verified `model_family` (`PointNetMLPJoint_FP` → `LC-PointNet`, or `ArGEnT_self_att_noSDF` → `ArGEnT-A`) | `{LC-PointNet or ArGEnT-A} (joint stress–life)` / `... (life only)`; title `"{label}: joint stress–life supervision versus life-only training"` | **Yes** — legend/title code now resolves `publication_label = eh.display_model_name(model_family)` once per pair and reuses it for both supervision conditions instead of looking up `variant_name` |
| `Comparison/02_engineered_geometric_features.ipynb` (multiple cells: pooled-metric bars, grouped-region bars, headfeat-vs-baseline delta figures, qualitative field-comparison figure, `presentation_table` displays) | Legend/xtick/title text and displayed tables for the `ArGEnT_self_att_noSDF` checkpoint loaded from `Zonal/Edge_arc_feat/ArGEnT_self_att_noSDF` | Resolver already mapped this family id to plain `ArGEnT-A`, which under-reports that this specific checkpoint is feature-augmented | `ArGEnT-A + GF` in every figure/table where the `Edge_arc_feat` (feature-augmented) checkpoint is shown as an ablation-side comparator; plain `ArGEnT-A` retained only where the same raw family id refers to the non-GF `BASELINE_ABLATION='Edge'` checkpoint (head-to-head-vs-baseline figures) | `ArGEnT-A + GF` (ablation side) / `ArGEnT-A` (baseline side) | **Yes** — added a notebook-local `display_model_name()` override (verified against `feature_assignment.csv`, see §2) used for the ablation-side family, while baseline-side comparisons keep `eh.display_model_name` (plain) since that checkpoint is loaded from the non-feature `Edge` directory |
| `Comparison/02_engineered_geometric_features.ipynb` (headfeat-vs-baseline delta figure titles/ylabels/captions) | `"(headfeat − baseline)"`, `'headfeat − baseline [decades]'`, `"Green = headfeat improves"`, `"No paired headfeat vs baseline comparison available."`, `"Paired headfeat vs baseline comparison"` | Internal ablation-name jargon (`headfeat`) used directly in reader-facing axis/title/caption text | `"(GF − baseline)"`, `'GF − baseline [decades]'`, `"Green = engineered geometric features (GF) improve"`, `"No paired engineered-feature (GF) vs baseline comparison available."`, `"Paired engineered-feature (GF) vs baseline comparison"` | **Yes** | 
| `Comparison/README.md` (§2, notebook 2 description) | `"...for ArGEnT-A, GC-PointNet + GF, and LC-PointNet + GF. ArGEnT-A consumes engineered descriptors..."` | Described the `Edge_arc_feat` ArGEnT checkpoint as plain `ArGEnT-A` | `"...for ArGEnT-A + GF, GC-PointNet + GF, and LC-PointNet + GF... so it is reported as ArGEnT-A + GF, not plain ArGEnT-A..."` | **Yes** |
| `Comparison/eval_helpers.py` (`DISPLAY_MODEL_ORDER`) | Canonical order list ended at `ArGEnT-A` | N/A (consistency fix) | Added `ArGEnT-A + GF` after `ArGEnT-A` per Part A §7 stable order | **Yes** |

### Confirmed already-correct labels (no change needed)
- `PointNetMLPJoint` → `GC-PointNet`, `PointNetMLPJoint_headfeat` → `GC-PointNet + GF`,
  `PointNetMLPJoint_FP` → `LC-PointNet`, `PointNetMLPJoint_FP_headfeat` → `LC-PointNet + GF`,
  `ArGEnT_self_att_noSDF` → `ArGEnT-A` are all defined in `Comparison/eval_helpers.py`
  (`DISPLAY_MODEL_NAMES`, lines ~45–51) and were already used via `eh.display_model_name`/
  `eh.presentation_table` for every legend/xticklabel/title in
  `01_fp_vs_argent.ipynb` and `03_data_efficiency.ipynb`. No `PointNetMLPJoint_headfeat`,
  `pnmlp_*`, or `ARGENT`/`ArGEnT-inspired attention operator` legend strings were found in
  these two notebooks.
- `Comparison/results/abstract_evidence_audit.md` (a prior audit report, not a paper
  figure) records the phrase "adapted ArGEnT-inspired attention operator" as a historical
  finding; this document is a dated audit trail, not a reader-facing figure/caption, and
  was left unchanged per the instruction not to alter prior audits.

### Explicitly out of scope / retained as internal-only (per Part A §3 and Part B §6 exceptions)
- `checkpoint_path`, `variant_name`, `stress_variant`/`no_stress_variant` columns in
  `checkpoint_inventory.csv`, `stress_vs_no_stress_diagnostic.md/json`, and
  `validation_report.md`'s "Valid stress/no-stress model pair(s)" table retain raw
  checkpoint stems (e.g. `pnmlp_16932d84`) alongside the already-correct `model_family`
  column (`LC-PointNet`, `ArGEnT-A`). These are audit/traceability tables explicitly
  needed to prove which checkpoint file backs each paper-facing label, not the
  publication figures themselves.
- `feature_assignment.csv` (displayed inline in notebook 2) keeps raw `model_family`
  values (`ArGEnT_self_att_noSDF`, `PointNetMLPJoint_headfeat`, ...) because it exists
  specifically to document the column-level evidence used to build the label mapping
  in this report (§2 below).
- Legacy/unreferenced notebooks `Comparison/model_comparison.ipynb` and
  `Comparison/model_ablation_comparison(old_from_v1).ipynb` are not part of the
  `Comparison/README.md` notebook suite (only `01`–`04` are documented as paper
  analyses) and contain cached execution outputs with raw checkpoint paths in
  inventory-style tables (not plot legends). These were inspected but left unmodified
  as legacy artifacts; no `label=`/`set_title` call in either notebook was found to use
  a raw model id as a legend string.
- Code, class names, checkpoint filenames, directory names (`PointNetMLPJoint_FP`,
  `Edge_arc_feat`, `pnmlp_16932d84.pt`, ...) were not renamed anywhere.

### Unresolved model-metadata issues
None found. Every internal model family id appearing in a paper-facing figure/table in
notebooks `01`–`04` resolves to one of the six canonical labels via a verified mapping.

---

## 2. Evidence used to verify `ArGEnT-A + GF` (Edge_arc_feat ArGEnT checkpoint)

- `Comparison/02_engineered_geometric_features.ipynb`, setup cell: `ABLATION = 'Edge_arc_feat'`;
  `FAMILIES` includes `'ArGEnT_self_att_noSDF'`, discovered under
  `Zonal/Edge_arc_feat/ArGEnT_self_att_noSDF/Trained_models/`.
- `Zonal/Edge_arc_feat/ArGEnT_self_att_noSDF/Training_script.py:33`:
  `INPUT_COLS = [0, 1, 3, 4, 5, 6, 7]` — columns 3–7 are
  `arc_length_mm, tangent_x, tangent_r, curvature, curvature_gradient` (engineered
  geometric descriptors), confirmed against `FEATURE_LABELS` in the notebook.
- `Comparison/results/02_engineered_geometric_features/feature_assignment.csv`, row
  `model_family=ArGEnT_self_att_noSDF`: `encoder_engineered_features = "arc_length_mm,
  tangent_x, tangent_r, curvature, curvature_gradient"`, note: *"Authoritative ArGEnT
  engineered-feature path is Training_script.py INPUT_COLS."*
- Contrast: the notebook's `BASELINE_ABLATION = 'Edge'` loads a **different** checkpoint
  file, `Zonal/Edge/ArGEnT_self_att_noSDF/Trained_models/*.pt` (no arc-feature columns),
  for the head-to-head-vs-baseline comparison — confirming the same raw family string
  denotes two distinct (GF vs non-GF) checkpoints depending on which ablation directory
  is loaded, which is exactly why a blanket string→label table is insufficient and a
  notebook-local, context-aware override was required.
- Numeric cross-check: `Comparison/results/02_engineered_geometric_features/summary_table.csv`
  shows the `Edge_arc_feat` `ArGEnT_self_att_noSDF` row has pooled `LogLife_MAE =
  0.00981...`, close to (but distinct from, and lower than) the `Edge_no_stress`-unrelated
  plain ArGEnT figure of `0.01605` (pooled MAE) reported for the non-feature checkpoint in
  `Comparison/results/01_fp_vs_argent/pooled_metrics.csv` (`Zonal/Edge`), consistent with
  a genuinely different, feature-augmented model.

---

## 3. Figure audit

| Figure path (regenerate via) | Model labels shown after fix | Identifies architecture + ablation (not file/checkpoint) | `GF` status correct | Stress-supervision status correct | Regenerated or statically checked |
|---|---|---|---|---|---|
| `Comparison/results/01_fp_vs_argent/figures/*` (run `01_fp_vs_argent.ipynb`) | `GC-PointNet`, `LC-PointNet`, `ArGEnT-A` | Yes (already used `eh.display_model_name`/`ordered_model_families`) | N/A (no GF variant in this notebook) | N/A | Static only — dataset/torch unavailable in this environment; no code change was needed |
| `Comparison/results/02_engineered_geometric_features/figures/*` (`figure_main_metrics`, `figure_life_bands`, `figure_grouped_regions`, `figure_headfeat_vs_baseline_delta`, `figure_headfeat_vs_baseline_by_life_bin`, `figure_qualitative_example`) | `GC-PointNet + GF`, `LC-PointNet + GF`, `ArGEnT-A + GF` (ablation side); `GC-PointNet`, `LC-PointNet`, `ArGEnT-A` (baseline side of the two headfeat-vs-baseline figures) | Yes, after fix | Yes, after fix (`ArGEnT-A + GF` now shown instead of bare `ArGEnT-A` wherever the feature-augmented checkpoint is the subject; baseline side correctly stays non-GF) | N/A (not a stress-supervision figure) | Static only — no committed PNGs exist in this checkout to regenerate (`find Comparison/results/02_engineered_geometric_features -name '*.png'` returns nothing); code was verified with `ast.parse` and manual trace of the label-resolution logic. **Must be re-executed with `torch`/`h5py` and the real `Data_gen/output/disc_dataset_edge_deriv_zonal.h5` to produce updated images.** |
| `Comparison/results/03_data_efficiency/figures/*` | `ArGEnT-A`, `LC-PointNet` | Yes (already correct; `FAMILIES` only contains the non-GF families for this ablation) | N/A | N/A | Static only |
| `Comparison/results/04_joint_stress_supervision/figures/stress_vs_no_stress_*` | `{LC-PointNet or ArGEnT-A} (joint stress–life)` / `(life only)` per pair | Yes, after fix (previously `pnmlp_16932d84 (with stress)` / `pnmlp_1bbaae12 (no stress)`) | N/A | Yes, after fix | Static only — same environment limitation; verified by tracing `variant_name = path.stem` → the bug, and by confirming `build_valid_pairs` already enforces same-`model_family`/`fp_status` pairing so the new `publication_label` is unambiguous |

### Regeneration commands (blocked by missing `torch`/`h5py`/dataset in this sandbox)
```
jupyter nbconvert --to notebook --execute --inplace Comparison/01_fp_vs_argent.ipynb
jupyter nbconvert --to notebook --execute --inplace Comparison/02_engineered_geometric_features.ipynb
jupyter nbconvert --to notebook --execute --inplace Comparison/03_data_efficiency.ipynb
jupyter nbconvert --to notebook --execute --inplace Comparison/04_joint_stress_supervision.ipynb
```
These require a Python environment with `torch`, `h5py`, `numpy`, `pandas`, `matplotlib`
and the real `Data_gen/output/disc_dataset_edge_deriv_zonal.h5` /
`disc_dataset_edge_deriv_uniform.h5` files plus all `Trained_models/*.pt` checkpoints,
none of which are available in this sandboxed environment (confirmed:
`python3 -c "import torch"` → `ModuleNotFoundError`; `Data_gen/output/` contains no
`.h5` files, only generator scripts).

---

## 4. Abstract fact verification

All CSV row lookups below reference files exactly as committed at commit
`8892d544e4162a8e27dd68f287a2e5d86f2662b9`. Percentages are recomputed with
`percent_reduction = 100*(baseline_error-proposed_error)/baseline_error` and
`percent_increase = 100*(ablation_error-reference_error)/reference_error`.

### A. Numerical claims

| # | Claim | Status | Source | Model IDs | Publication labels | Filter | Raw values | Recomputed |
|---|---|---|---|---|---|---|---|---|
| 1 | LC-PointNet vs ArGEnT-A, pooled MAE reduction 19% | MATCHES REPOSITORY EVIDENCE | `Comparison/results/01_fp_vs_argent/pooled_metrics.csv` | `PointNetMLPJoint_FP` vs `ArGEnT_self_att_noSDF` | LC-PointNet, ArGEnT-A | `regime=Zonal, ablation=Edge, target=LogLife` | MAE: 0.012962028309944277 (LC), 0.01374032517806771→ no; correct row 0.016048927698289875 (ArGEnT) | 100*(0.016048927698289875-0.012962028309944277)/0.016048927698289875 = **19.23%** ≈ 19% |
| 2 | LC-PointNet vs ArGEnT-A, pooled RMSE reduction 36% | MATCHES REPOSITORY EVIDENCE | same file/rows | same | same | same | RMSE 0.02868539552817829 (LC), 0.04487965278047202 (ArGEnT) | 100*(0.04487965278047202-0.02868539552817829)/0.04487965278047202 = **36.08%** ≈ 36% |
| 3 | LC-PointNet vs ArGEnT-A, `log_life<2` MAE reduction 81% | MATCHES REPOSITORY EVIDENCE | `Comparison/results/01_fp_vs_argent/life_band_metrics.csv` | `PointNetMLPJoint_FP` vs `ArGEnT_self_att_noSDF` | LC-PointNet, ArGEnT-A | `regime=Zonal, ablation=Edge, life_bin=log_life < 2` | MAE 0.0478641539812088 (LC), 0.256548136472702 (ArGEnT) | 100*(0.256548136472702-0.0478641539812088)/0.256548136472702 = **81.34%** ≈ 81% |
| 4 | LC-PointNet vs ArGEnT-A, `log_life<2` RMSE reduction 73% | MATCHES REPOSITORY EVIDENCE | same file/rows | same | same | same | RMSE 0.07222291082143784 (LC), 0.2722461521625519 (ArGEnT) | 100*(0.2722461521625519-0.07222291082143784)/0.2722461521625519 = **73.47%** ≈ 73% |
| 5 | LC-PointNet vs GC-PointNet, `log_life<2` MAE reduction 37% | MATCHES REPOSITORY EVIDENCE | same file | `PointNetMLPJoint_FP` vs `PointNetMLPJoint` | LC-PointNet, GC-PointNet | same filter | MAE 0.0478641539812088 (LC), 0.07585194706916809 (GC) | 100*(0.07585194706916809-0.0478641539812088)/0.07585194706916809 = **36.90%** ≈ 37% |
| 6 | LC-PointNet vs GC-PointNet, `log_life<2` RMSE reduction 30% | MATCHES REPOSITORY EVIDENCE | same file | same | same | same | RMSE 0.07222291082143784 (LC), 0.10342235863208771 (GC) | 100*(0.10342235863208771-0.07222291082143784)/0.10342235863208771 = **30.16%** ≈ 30% |
| 7a | GF ablations improve pooled+short-life errors for GC/LC/ArGEnT relative to baselines | MATCHES REPOSITORY EVIDENCE | `Comparison/results/02_engineered_geometric_features/paired_headfeat_vs_baseline.csv` and `..._by_life_bin.csv` | `PointNetMLPJoint`→`_headfeat`; `PointNetMLPJoint_FP`→`_FP_headfeat`; `ArGEnT_self_att_noSDF` (Edge)→(Edge_arc_feat) | GC-PointNet→+GF, LC-PointNet→+GF, ArGEnT-A→+GF | `life_bin ∈ {Full test set, log_life<2}` | All 6 rows (3 families × 2 subsets) have `delta_mae_loglife<0` and `delta_rmse_loglife<0` (e.g. LC: pooled Δ=-0.00481/-0.01100; short-life Δ=-0.02166/-0.02487) | All directional deltas negative ⇒ GF improves in every case checked |
| 7b | Under GF, LC-PointNet has lower pooled MAE/RMSE and lower short-life MAE than ArGEnT-A; short-life RMSE difference small, favours ArGEnT-A | MATCHES REPOSITORY EVIDENCE | `Comparison/results/02_engineered_geometric_features/summary_table.csv`, `life_band_metrics.csv` | `PointNetMLPJoint_FP_headfeat` vs `ArGEnT_self_att_noSDF` (Edge_arc_feat) | LC-PointNet + GF vs ArGEnT-A + GF | `regime=Zonal, ablation=Edge_arc_feat` | Pooled MAE 0.008149816654622555 (LC+GF) < 0.0098106162622571 (ArGEnT+GF); pooled RMSE 0.0176899041980505 < 0.021475769579410553; short-life MAE 0.026200538501143456 < 0.03148099035024643; short-life RMSE 0.04735548794269562 **>** 0.045965008437633514 | Pooled/short-life MAE and pooled RMSE favour LC+GF; short-life RMSE gap = +0.00139 (≈3% relative), favouring ArGEnT-A+GF — matches "small" and "favoured ArGEnT-A" |
| 8a | Training fractions truly span 10%–100% | MATCHES REPOSITORY EVIDENCE | `Comparison/results/03_data_efficiency/life_band_metrics.csv` | ablations `Edge_10, Edge_25, Edge_50, Edge_75, Edge` | — | `training_fraction` column | Distinct ablation dirs present: 10/25/50/75/100% | Confirms 5 fractions spanning 10%–100% |
| 8b | LC-PointNet lower short-life error than ArGEnT-A at every evaluated fraction | MATCHES REPOSITORY EVIDENCE | same file, `life_bin=log_life < 2` | `PointNetMLPJoint_FP` vs `ArGEnT_self_att_noSDF` | LC-PointNet, ArGEnT-A | per ablation | MAE(LC,ArGEnT): 10%→0.252/0.394; 25%→0.197/0.257; 50%→0.120/0.259; 75%→0.071/0.248; 100%→0.048/0.257 | LC < ArGEnT at all 5 fractions |
| 8c | Pooled model ranking varies with training-set size | MATCHES REPOSITORY EVIDENCE | same file, `life_bin=Full test set` | same | same | per ablation | Pooled MAE(LC,ArGEnT): 10%→0.0371/0.0406 (LC better); 25%→0.0261/0.0218 (ArGEnT better); 50%→0.0207/0.0199 (ArGEnT better); 75%→0.0151/0.0171 (LC better); 100%→0.0130/0.0160 (LC better) | Ranking flips between fractions, confirming "varied" |
| 9a | Valid stress/no-stress matched pairs are LC-PointNet and ArGEnT-A (GC-PointNet excluded/missing) | MATCHES REPOSITORY EVIDENCE | `Comparison/results/04_joint_stress_supervision/validation_report.md`, `stress_vs_no_stress_pair_inventory.csv` | `PointNetMLPJoint_FP` (`pnmlp_16932d84`/`pnmlp_1bbaae12`), `ArGEnT_self_att_noSDF` (`argent_self_nosdf_s_177b264d`/`argent_self_nosdf_s_cf025919`) | LC-PointNet, ArGEnT-A | pairing keyed on matching `model_family`+`fp_status` between `Edge`/`Edge_no_stress` | Both pairs `status=discovered`; report states GC-PointNet "has no life-only checkpoint under `Zonal/Edge_no_stress`" | Matches abstract's implicit pairing (no GC-PointNet ablation reported) |
| 9b | LC-PointNet short-life MAE increase 44% on stress removal | MATCHES REPOSITORY EVIDENCE | `Comparison/results/04_joint_stress_supervision/stress_vs_no_stress_paired_metrics.csv`, `model_family=PointNetMLPJoint_FP, life_bin=log_life < 2` | `PointNetMLPJoint_FP` | LC-PointNet | stress vs no-stress | `stress_mae_loglife=0.0478641502559185`, `no_stress_mae_loglife=0.0689726173877716` | 100*(0.0689726173877716-0.0478641502559185)/0.0478641502559185 = **44.10%** ≈ 44% |
| 9c | LC-PointNet short-life RMSE increase 36% | MATCHES REPOSITORY EVIDENCE | same row | same | LC-PointNet | same | `stress_rmse=0.07222291827201843`, `no_stress_rmse=0.09821518510580063` | 100*(0.09821518510580063-0.07222291827201843)/0.07222291827201843 = **35.99%** ≈ 36% |
| 9d | ArGEnT-A short-life change ≈2% | MATCHES REPOSITORY EVIDENCE | same file, `model_family=ArGEnT_self_att_noSDF, life_bin=log_life < 2` | `ArGEnT_self_att_noSDF` | ArGEnT-A | stress vs no-stress | `stress_mae=0.25654810667037964`, `no_stress_mae=0.26178160309791565` | 100*(0.26178160309791565-0.25654810667037964)/0.25654810667037964 = **2.04%** |

### B. Methodological claims

| Claim | Status | Evidence |
|---|---|---|
| Controlled 2D axisymmetric, FEM-grounded reduced-order disc benchmark | MATCHES REPOSITORY EVIDENCE | `Data_gen/physics.py` docstring: "Stress is obtained from a real 2D axisymmetric linear-elasticity finite-element..."; `solve_axisymmetric_response()` |
| Bore/transition/web/rim/front C-groove/rear drive-arm features | MATCHES REPOSITORY EVIDENCE | `Data_gen/config.py:11-39` zone/region names (`bore`, `lower_transition`, `web`, `upper_transition`, `rim`, ...); `Comparison/eval_helpers.py:24-31` `ZONE_ID_TO_NAME`/`SUBZONE_ID_TO_NAME` include `front_cgroove`, `rear_arm_neck`, `rear_arm_land`, `rear_arm_corner`, `rear_arm_end_face` |
| Parameterized contour geometry variation | MATCHES REPOSITORY EVIDENCE | `Data_gen/geometry.py`, `Data_gen/sample_generator.py` (per-region parameterized dimensions, e.g. `bore_radius_inner`, `web_height`, etc. in `config.py`) |
| Node-wise stress and base-10 log-life targets | MATCHES REPOSITORY EVIDENCE | `Comparison/04_joint_stress_supervision.ipynb` cell 5: `np.log10(np.clip(life.astype('float64')...))`; node arrays `stress_max_vm`, `life_raw` per sample |
| Hierarchical PointNet-style geometry encoder | MATCHES REPOSITORY EVIDENCE | `Zonal/Edge/PointNetMLPJoint_FP/pn_models.py`: `class PointNet2Encoder2D`, multiple `SetAbstraction` (`sa_layers`) blocks |
| Fourier feature mapping / query encoding | MATCHES REPOSITORY EVIDENCE | `pn_models.py:103` `class FourierFeatures`; used both on encoder input (`self.posenc`) and query head (`self.head_posenc`) |
| Native-resolution multiscale feature propagation, query-local sampling | MATCHES REPOSITORY EVIDENCE | `pn_models.py:561-650` `class PointNetMLPJoint_FP`: `self.fp2`/`self.fp1` (`FeaturePropagation`) propagate SA2→SA1→"original point resolution" (code comment: "FP1: FP2 output → original point resolution") |
| Prediction head combines global representation + Fourier query + local context | MATCHES REPOSITORY EVIDENCE | `PointNetMLPJoint_FP` forward path combines `self.glob` (global), `self.head_posenc` (Fourier query), and FP1 output (local) — verified by class structure; full forward-pass trace not executed (no torch) |
| GC-PointNet: identical FFM query encoding, no feature propagation | MATCHES REPOSITORY EVIDENCE | `pn_models.py:393` `class PointNetMLPJoint` uses the same `FourierFeatures` head posenc as `PointNetMLPJoint_FP` (lines 413-423) but has no `fp1`/`fp2`/`FeaturePropagation` members |
| ArGEnT-A is an adapted cross-attention operator | MATCHES REPOSITORY EVIDENCE | `Zonal/Edge/ArGEnT_self_att_noSDF/benchmarks.py` defines `ArGEnTDeepONet`; `Comparison/results/abstract_evidence_audit.md` records prior verification against `attention_type` configuration |
| Deterministic held-out geometry validation split | MATCHES REPOSITORY EVIDENCE | `Comparison/README.md:122`: "the same deterministic 20% geometry holdout (seed 42)"; every notebook sets `SPLIT_SEED, EVAL_FRACTION = 42, 0.20` |
| Node-level MAE/RMSE, ordered life-bin evaluation, `log_life<2` definition | MATCHES REPOSITORY EVIDENCE | `Comparison/eval_helpers.py` `ALL_LIFE_BIN_DEFS`/`PHYSICAL_LIFE_BIN_ORDER`; life-bin CSVs contain a `log_life < 2` row filtered as `true_loglife < 2` |
| GF = engineered geometric features | MATCHES REPOSITORY EVIDENCE | `feature_assignment.csv` engineered feature columns = `arc_length_mm, tangent_x, tangent_r, curvature, curvature_gradient` |
| Data-efficiency training-fraction definition | MATCHES REPOSITORY EVIDENCE | `Comparison/03_data_efficiency.ipynb`: `ABLATION_TO_FRACTION` maps `Edge_10→0.10, Edge_25→0.25, Edge_50→0.50, Edge_75→0.75, Edge→1.00`; training scripts' `Perc_training_data`/`train_data_percent` |
| Valid stress/no-stress model pairing | MATCHES REPOSITORY EVIDENCE | `04_joint_stress_supervision.ipynb` `build_valid_pairs()` requires matching `model_family` + `fp_status` between `stress_target_mode in {with_stress, no_stress}` checkpoints; confirmed 2 valid pairs (LC-PointNet, ArGEnT-A), GC-PointNet reported missing |

### Overall abstract conclusion
Every numerical claim recomputed from committed result CSVs matches the stated
percentage to within rounding. Every methodological/architectural claim inspected has
direct supporting code/documentation evidence. No claim in the supplied abstract was
found to not match repository evidence, and no claim required marking as unverifiable
given the committed CSV/JSON/code evidence available in this repository.

---

## 5. Execution status

- **Notebooks executed:** none (no `torch`/`h5py`, no `Data_gen/output/*.h5`, no
  `Trained_models/*.pt` payloads loadable in this sandbox — `.pt` files are present on
  disk but require `torch.load`, which is unavailable here).
- **Generated figure paths checked:** none exist in this checkout for
  `02_engineered_geometric_features` or `04_joint_stress_supervision` (`find ... -name
  '*.png'` under `Comparison/results/` returns no results); label-generation code paths
  were instead verified statically (`ast.parse` on every notebook cell after edits, plus
  manual trace of `display_model_name`/`presentation_table`/`plot_field_comparison`
  call sites).
- **Data/checkpoints/dependencies unavailable:** `torch`, `h5py`; `Data_gen/output/*.h5`;
  in-repo `Trained_models/*.pt` checkpoints exist but cannot be loaded without `torch`.
- **CSV/JSON/Markdown result artifacts used for numeric verification:** all under
  `Comparison/results/{01_fp_vs_argent,02_engineered_geometric_features,
  03_data_efficiency,04_joint_stress_supervision}/`, as cited per-row in §4 above.
