# Abstract evidence audit

## Scope and conventions

This audit uses only tracked artifacts in this checkout.  The principal source is
the Zonal/Edge validation-split evaluation: 1,000 geometries and 679,000 nodes
(`01_fp_vs_argent/life_band_metrics.csv`, rows 20--37).  `Comparison/README.md`
states that this is a deterministic 20% geometry holdout (seed 42) and must not
be called an independent test set.  All errors below are log10-life errors in
decades, pooled at node level; no fold or seed aggregation is present.

`percent_reduction = 100 * (baseline_error - proposed_error) / baseline_error`
and `percent_increase = 100 * (ablation_error - reference_error) / reference_error`.
Rows in each comparison share regime, representation, split, target scale, and
node count.  “Full test set” is a legacy CSV bin label, not evaluation provenance.

## Claim-by-claim evidence

| Abstract location / claim | Status | Repository evidence | Exact source file(s) / table(s) | Verification calculation or method | Required action |
|---|---|---|---|---|---|
| FEM-grounded controlled reduced-order disc benchmark | Verified with wording adjustment | The generator creates a 2-D axisymmetric disc and solves FEM before life calculation. | `README.md:20-31`; `Data_gen/physics.py`; `Data_gen/sample_generator.py` | Code inspection. “Reduced-order” is defensible for the benchmark, but not a claim of production representativeness. | Say “controlled 2-D axisymmetric FEM-grounded benchmark.” |
| Disc-like geometry has localized protrusion/drive-arm features | Verified with wording adjustment | Geometry includes bore, transitions, web, rim, front C-groove, and rear annular drive arm. | `README.md:20-22`; `Data_gen/geometry.py`; `Data_gen/config.py` | Code/documentation inspection. | Replace vague “protrusion” with the documented C-groove and rear drive-arm features. |
| FEM supplies node-wise stress and base-10 log-life targets | Verified with wording adjustment | FEM produces node-wise stress and raw life; evaluation converts/uses `true_loglife`. | `README.md:30`; `Data_gen/physics.py:528-660`; `Data_gen/sample_generator.py:47-87`; `Comparison/eval_helpers.py:69-107` | Trace targets through generation and evaluation. | Say base-10 log-life is the evaluation target derived from raw-life targets. |
| Geometry-conditioned point-cloud surrogate | Verified | Point-set encoders consume geometry/query points and predict fields. | `Zonal/Edge/PointNetMLPJoint/pn_models.py`; `Zonal/Edge/PointNetMLPJoint_FP/pn_models.py`; `Comparison/01_fp_vs_argent.ipynb` | Code inspection. | Retain. |
| LC-PointNet has a hierarchical PointNet-style encoder and Fourier query encoding | Verified | FP checkpoint metadata has two SA blocks and `head_posenc: {n_freqs: 12, scale: 1.0}`. | `01_fp_vs_argent/checkpoint_integrity.json` (FP Zonal/Edge entry); `Zonal/Edge/PointNetMLPJoint_FP/pn_models.py` | Checkpoint/configuration and model-code inspection. | Retain, using the publication name. |
| LC-PointNet propagates multiscale features to native resolution and query-local context | Verified | `fp2` and `fp1` propagate features back to geometry points, then nearest point features are gathered for queries with global latent and query encoding. | `Zonal/Edge/PointNetMLPJoint_FP/pn_models.py:629-715` | Code inspection. | Retain as architectural description, not causal proof. |
| GC-PointNet has the same FFM encoding and no FP local pathway | Verified | Non-FP checkpoint has matching positional and head positional encodings; FP configuration is absent. | `01_fp_vs_argent/checkpoint_integrity.json` (Zonal `PointNetMLPJoint` and FP entries); `Zonal/Edge/PointNetMLPJoint/pn_models.py` | Compare saved configs and forwards. | Retain. |
| Stress and log-life are jointly predicted in principal comparison | Verified | All principal entries have `out_dim: 2`; feature notebook records targets `Stress`, `LogLife`. | `01_fp_vs_argent/checkpoint_integrity.json`; `02_engineered_geometric_features/checkpoint_integrity.json` | Checkpoint metadata. | Retain. |
| Attention comparator is “adapted ArGEnT-inspired attention operator” | Verified with wording adjustment | It is an ArGEnT/DeepONet-style model with `attention_type: cross`, not self-attention. | `README.md:50-52`; `01_fp_vs_argent/checkpoint_integrity.json`; `Zonal/Edge/ArGEnT_self_att_noSDF/benchmarks.py:805-816` | Code/configuration inspection. | Use the specified wording; do not call it self-attention. |
| `log_life < 2` is a short-life benchmark subgroup | Verified with wording adjustment | It is a predefined physical life bin with 1,030 Zonal nodes. No repository artifact establishes real-world criticality. | `Comparison/eval_helpers.py:116-129`; `01_fp_vs_argent/life_band_metrics.csv` rows 20--37 | Bin definition and count check. | Say “evaluated short-life subset (`log_life < 2`)”; qualify “fatigue-critical” as benchmark-specific. |
| Engineered features are geometric and improve error | Partially supported | Five extra geometry-derived columns are supplied; paired feature results exist. Comparisons use separately trained checkpoints. | `02_engineered_geometric_features/feature_assignment.csv`; `02_engineered_geometric_features/paired_headfeat_vs_baseline_by_life_bin.csv` | Inspect feature wiring and paired table. | State results separately by family; avoid a general causal conclusion. |
| Data efficiency covers 10%--100% | Not verifiable from repository | Notebook code names 10/25/50/75/100%, but no `03_data_efficiency` results/metadata are tracked. | `Comparison/03_data_efficiency.ipynb`; absent `Comparison/results/03_data_efficiency/` | Required output table/checkpoints were not available. | Do not include quantitative data-efficiency findings. |
| Valid stress/no-stress comparison | Partially supported | Only ArGEnT and FP pairs are documented; regular PointNet has no life-only checkpoint. No Notebook 04 result CSV is tracked. | `Comparison/04_joint_stress_supervision.ipynb`; `README.md:40`; absence of `Comparison/results/04_joint_stress_supervision/` | Check notebook pair declaration and result availability. | Do not quantify or attribute this ablation to LC-PointNet without the FP paired output. |
| Pooled LC-PointNet reduction: 19% MAE and 36% RMSE vs attention comparator | Verified with wording adjustment | Zonal/Edge is the scientifically appropriate primary source because it is the stated principal zonal comparison. | `01_fp_vs_argent/pooled_metrics.csv` rows 8 and 12 | MAE: `(0.016048927698289875 - 0.012962028309944277)/0.016048927698289875*100 = 19.234303%`; RMSE: `(0.04487965278047202 - 0.02868539552817829)/0.04487965278047202*100 = 36.084339%`. | Keep 19%/36%; say validation-split rather than test set. |
| Short-life LC-PointNet reduction: 81% MAE and 73% RMSE vs attention comparator | Verified with wording adjustment | Both rows are Zonal/Edge, `log_life < 2`, n=1,030. | `01_fp_vs_argent/life_band_metrics.csv` rows 21 and 33 | MAE: `(0.256548136472702 - 0.0478641539812088)/0.256548136472702*100 = 81.342784%`; RMSE: `(0.2722461521625519 - 0.07222291082143784)/0.2722461521625519*100 = 73.470712%`. | Keep 81%/73%; call it the evaluated short-life subset. |
| LC-PointNet critical-region MAE reduction: 37% vs GC-PointNet | Verified with wording adjustment | The abstract’s intended threshold subgroup is the direct comparison; both rows have n=1,030. | `01_fp_vs_argent/life_band_metrics.csv` rows 27 and 33 | `(0.07585194706916809 - 0.0478641539812088)/0.07585194706916809*100 = 36.898952%`. | Keep 37%, but say FP pathway “was associated with” lower error. |
| LC-PointNet remains lower through 10%--100%; pooled ranks vary | Not verifiable from repository | No data-efficiency CSV, run metadata, or figures are tracked. | Absent `Comparison/results/03_data_efficiency/` | No rows exist to check fractions, model pairing, or metrics. | Remove pending regeneration and archival of Notebook 03 outputs. |
| Removing stress raises short-life MAE/RMSE 44%/36% and pooled 6%/5% for LC-PointNet | Not verifiable from repository | No Notebook 04 result tables are tracked; only the FP and ArGEnT pair definitions are available. | Absent `Comparison/results/04_joint_stress_supervision/`; `Comparison/04_joint_stress_supervision.ipynb` | Cannot reproduce values or establish split/pair correspondence. | Remove; if regenerated, report only the verified FP stress/no-stress pair. |

## Numerical verification appendix

| Comparison | Evaluation subset | Baseline model | Baseline MAE | Other MAE | MAE change | Baseline RMSE | Other RMSE | RMSE change | Exact CSV/table source |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| Attention comparator (`ArGEnT_self_att_noSDF`) vs LC-PointNet (`PointNetMLPJoint_FP`) | Zonal/Edge, pooled, n=679,000 | 0.016048928 | 0.016048928 | 0.012962028 | -19.234303% | 0.044879653 | 0.028685396 | -36.084339% | `01_fp_vs_argent/pooled_metrics.csv`, rows 8, 12 |
| Attention comparator (`ArGEnT_self_att_noSDF`) vs LC-PointNet (`PointNetMLPJoint_FP`) | Zonal/Edge, `log_life < 2`, n=1,030 | 0.256548136 | 0.256548136 | 0.047864154 | -81.342784% | 0.272246152 | 0.072222911 | -73.470712% | `01_fp_vs_argent/life_band_metrics.csv`, rows 21, 33 |
| GC-PointNet (`PointNetMLPJoint`) vs LC-PointNet (`PointNetMLPJoint_FP`) | Zonal/Edge, `log_life < 2`, n=1,030 | 0.075851947 | 0.075851947 | 0.047864154 | -36.898952% | 0.103422359 | 0.072222911 | -30.167997% | `01_fp_vs_argent/life_band_metrics.csv`, rows 27, 33 |

## Causal-language audit

The results demonstrate associations on this controlled benchmark, not that local
context is necessary for production fatigue assessment or that a result is “most
consequential” in practical engineering. Replace “indicating that explicit
query-local geometric context improves prediction” with “the FP ablation was
associated with lower error in the evaluated short-life subset.” Replace broad
“can improve” conclusions with “improved performance on this controlled
FEM-grounded benchmark.”

## Revised abstract: minimal correction version

Fatigue-life assessment benefits from spatial predictions that remain accurate in
localized short-life regions. Geometry-conditioned surrogates are often evaluated
using pooled field errors, which can conceal errors near geometric transitions.
This work presents LC-PointNet, a local-context geometry-conditioned point-cloud
surrogate for stress and base-10 logarithmic fatigue-life prediction on a
controlled 2-D axisymmetric FEM-grounded disc benchmark.

The benchmark comprises disc geometries with bore, transition, web, rim,
front C-groove, and rear drive-arm features. FEM supplies node-wise stress and
raw-life targets, from which log-life is evaluated. LC-PointNet uses a
hierarchical PointNet-style encoder, Fourier feature mappings of spatial query
coordinates, and feature propagation to native point resolution. Its prediction
head combines query-local propagated features, global context, and query
encoding. LC-PointNet jointly predicts stress and log-life. It is compared with
GC-PointNet, which uses the same Fourier query encoding but lacks the
native-resolution propagated pathway, and with an adapted ArGEnT-inspired
attention operator.

On the Zonal/Edge validation-split evaluation (1,000 geometries; 679,000 nodes),
LC-PointNet reduced pooled log-life MAE and RMSE by 19% and 36%, respectively,
relative to the adapted attention operator. In the evaluated short-life subset
(`log_life < 2`, 1,030 nodes), reductions were 81% for MAE and 73% for RMSE.
Relative to GC-PointNet, LC-PointNet reduced short-life MAE by 37%. These
results show that the feature-propagation pathway was associated with lower
error in the evaluated short-life subset on this benchmark. Engineered-feature,
data-efficiency, and stress-supervision results are not included because the
tracked artifacts do not permit their numerical verification.

## Revised abstract: submission-ready concise version (282 words)

Spatial fatigue-life surrogates must resolve localized short-life regions, yet
pooled field metrics can obscure errors near geometric transitions. We evaluate
geometry-conditioned point-cloud surrogates on a controlled 2-D axisymmetric,
FEM-grounded disc benchmark. The generated geometries include bore, transition,
web, rim, front C-groove, and rear drive-arm features. FEM supplies node-wise
stress and fatigue-life targets; performance is evaluated on base-10 log-life.

We introduce LC-PointNet, a hierarchical PointNet-style surrogate that uses
Fourier-mapped spatial query coordinates and propagates multiscale encoder
features to native point resolution. The prediction head combines global context,
query encoding, and propagated query-local geometric features to jointly predict
stress and log-life. We compare LC-PointNet with GC-PointNet, a matching
global-context PointNet that retains the Fourier query encoding but omits the
native-resolution propagated pathway, and with an adapted ArGEnT-inspired
attention operator.

Evaluation uses a deterministic validation-split geometry holdout (seed 42,
20%; 1,000 geometries and 679,000 nodes), rather than an independent test set.
On the principal Zonal/Edge comparison, LC-PointNet reduced pooled log-life MAE
from 0.01605 to 0.01296 decades (19%) and RMSE from 0.04488 to 0.02869 decades
(36%) relative to the adapted attention operator. In the evaluated short-life
subset, `log_life < 2` (1,030 nodes), MAE fell from 0.25655 to 0.04786 decades
(81%) and RMSE from 0.27225 to 0.07222 decades (73%). Against GC-PointNet,
LC-PointNet reduced short-life MAE from 0.07585 to 0.04786 decades (37%).

These results demonstrate, under the studied conditions, that the
feature-propagation pathway was associated with lower log-life error, especially
in the evaluated short-life subset. They support further study of query-local
geometric context for spatial fatigue-life surrogate modelling, without implying
production-component validation or certification readiness.

## Publication-readiness checklist

| Item | Status | Reason |
|---|---|---|
| All comparison figures use publication display nomenclature | Incomplete | Code paths were updated; existing tracked figures could not be regenerated without local HDF5 assets. |
| Internal folder/file/checkpoint/result IDs were not renamed | Complete | Mapping is presentation-only. |
| Figure labels are readable at intended paper size | Blocked | Static widening/external legends applied; visual execution was unavailable. |
| Figure legends use consistent model ordering | Complete | Shared helper orders mapped names explicitly. |
| Full test set is visually distinct from physical log-life bins | Complete | Existing split plot separates the aggregate panel from ordered physical bins. |
| MAE and RMSE are consistently presented where required | Complete | Shared bin plot renders both metrics. |
| All claimed results trace to an exact output table/CSV | Incomplete | Data-efficiency and joint-supervision artifacts are absent. |
| No unsupported stress/no-stress comparison is presented | Complete | Revised abstracts omit it. |
| Abstract numerical claims were recomputed and verified | Incomplete | Three main claims verified; claims requiring missing Notebook 03/04 outputs are omitted. |
| Abstract method descriptions match the implementation | Complete | Revised descriptions follow code and checkpoint metadata. |
| Figure filenames and result filenames remain unchanged | Complete | No artifact path/name was modified. |
