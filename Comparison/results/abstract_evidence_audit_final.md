# Final abstract evidence audit (2026-09-02)

## Executive summary

This audit was performed from the committed repository state at `c1f6c1baafb69632e5d5c060d54ec4ed7ea377b1`. A repository-wide search found the previously reported CSV evidence in the four comparison result folders. The metrics are consistently labelled **validation-split evaluation** (seed 42, 20% holdout, 1,000 geometries and 679,000 pooled nodes); “Full test set” is a legacy CSV bin label and is reported here as pooled evaluation. The five headline percentages and the LC-PointNet stress-ablation percentages are verified. Data-efficiency checkpoint provenance remains a qualification, not a missing-file finding.

## Searched result directories

- `Comparison/results/01_fp_vs_argent/`
- `Comparison/results/02_engineered_geometric_features/`
- `Comparison/results/03_data_efficiency/`
- `Comparison/results/04_joint_stress_supervision/`
- `Comparison/results/` (prior audit and final report)

All descendant CSV, JSON, and Markdown artifacts in these directories were inspected, including metadata, split provenance, geometry coverage, checkpoint inventories, summaries, and diagnostics.

## Verified internal-to-publication mapping

| Internal identifier | Publication label | Implementation evidence |
|---|---|---|
| `PointNetMLPJoint` | GC-PointNet | non-FP PointNet encoder; Fourier query encoding; no native-resolution FP pathway |
| `PointNetMLPJoint_headfeat` | GC-PointNet + GF | same global encoder with engineered columns 3–7 at the prediction head |
| `PointNetMLPJoint_FP` | LC-PointNet | `FeaturePropagation` (`fp1`/`fp2`) supplies native-resolution local features |
| `PointNetMLPJoint_FP_headfeat` | LC-PointNet + GF | FP pathway plus engineered columns 3–7 |
| `ArGEnT_self_att_noSDF` | ArGEnT-A | adapted ArGEnT-inspired self/cross-attention comparator |

The centralized mapping is in `Comparison/eval_helpers.py`. `GF` denotes engineered geometric features (arc length, tangent components, curvature, and curvature gradient). Internal IDs remain in raw CSVs, metadata, checkpoints, and paths for traceability.

## Claim-level audit

| Abstract claim | Status | Exact source path(s) | Rows/filters used | Raw metric values | Calculation | Recommended wording/action |
|---|---|---|---|---|---|---|
| LC-PointNet pooled log-life MAE reduction 19% vs ArGEnT-A | Verified | `01_fp_vs_argent/pooled_metrics.csv` | Zonal, Edge, pooled/legacy `Full test set`; ArGEnT-A vs `PointNetMLPJoint_FP`; n=679000 | 0.0160489277 → 0.0129620283 | `100*(.0160489277-.0129620283)/.0160489277 = 19.2343%` | Retain as 19%, scoped to validation-split benchmark |
| LC-PointNet pooled log-life RMSE reduction 36% vs ArGEnT-A | Verified | same | same | 0.0448796528 → 0.0286853955 | `36.0837%` | Retain as 36% |
| LC-PointNet short-life MAE reduction 81% vs ArGEnT-A | Verified | `01_fp_vs_argent/life_band_metrics.csv` | Zonal, Edge, `log_life < 2`; n=1030 | 0.2565481365 → 0.0478641540 | `81.3430%` | Retain as 81% |
| LC-PointNet short-life RMSE reduction 73% vs ArGEnT-A | Verified | same | same | 0.2722461522 → 0.0722229108 | `73.4715%` | Retain as 73% |
| Local pathway critical MAE reduction 37% vs GC-PointNet | Verified | `01_fp_vs_argent/life_band_metrics.csv` | Zonal, Edge, `log_life < 2`; `PointNetMLPJoint` vs `PointNetMLPJoint_FP`; n=1030 | 0.0758519471 → 0.0478641540 | `36.8979%` | Say matched LC/GC comparison, not universal causation |
| Engineered features benefit GC-PointNet | Verified with wording adjustment | `02_engineered_geometric_features/paired_headfeat_vs_baseline_by_life_bin.csv` | Zonal shared 1000 geometries; Edge vs Edge_arc_feat; pooled and each listed life bin | pooled MAE/RMSE 0.0164136626/0.0356734656 → 0.0143827433/0.0312462449; short-life 0.0758519471/0.1034223586 → 0.0586090833/0.0864018649 | pooled reductions 12.3734% / 12.4149%; short-life reductions 22.7273% / 16.4597%; all five bins improve both metrics | State the GC ablation improves both metrics in this evaluated comparison |
| Engineered features benefit LC-PointNet | Verified with wording adjustment | same | same, `PointNetMLPJoint_FP` vs `PointNetMLPJoint_FP_headfeat` | pooled MAE/RMSE 0.0129620275/0.0286853965 → 0.0081498167/0.0176899042; short-life 0.0478641503/0.0722229183 → 0.0262005385/0.0473554879 | pooled reductions 37.1254% / 38.3387%; short-life reductions 45.2426% / 34.4289%; all five bins improve both metrics | State the LC result separately; do not generalize to all model families |
| Data fractions are 10–100% | Verified | `03_data_efficiency/data_efficiency_by_life_bin.csv`, `training_geometry_counts.csv` | Edge_10, 25, 50, 75, and Edge full; pooled and short-life rows | fractions 10%, 25%, 50%, 75%, 100% | direct fraction/geometry-count verification | Retain, calling evaluation validation-split |
| LC-PointNet beats ArGEnT-A in short-life at every fraction | Partially supported | `03_data_efficiency/data_efficiency_by_life_bin.csv` | each fraction, `log_life < 2`, matched families | short-life rows are present and LC is lower at each evaluated fraction | direct row-wise comparison | Retain only with checkpoint-provenance qualification; do not call independent test evidence |
| Pooled rankings vary with training fraction | Verified | same | each fraction, pooled `Full test set` rows | ArGEnT-A vs LC pooled MAE: 10% 0.0405844/0.0371445; 25% 0.0217625/0.0260538; 50% 0.0199265/0.0207250; 75% 0.0170750/0.0151250; 100% 0.0160489/0.0129620 | ordering changes across fractions | Retain as pooled-ranking variation |
| Stress removal increases LC short-life MAE/RMSE by 44%/36% and pooled MAE/RMSE by 6%/5% | Verified | `04_joint_stress_supervision/stress_vs_no_stress_paired_metrics.csv` | valid FP pair, seed 42, 0.2, pooled and `log_life < 2` | pooled stress→no-stress MAE/RMSE 0.0129620275/0.0286853965 → 0.0137612009/0.0300309826; short-life 0.0478641503/0.0722229183 → 0.0689726174/0.0982151058 | increases: pooled 6.1655%/4.6908%; short-life 44.1008%/35.9889% | Retain, explicitly identify LC-PointNet FP stress/no-stress pair |

## Numerical verification appendix

| Comparison | Evaluation subset | Baseline internal ID | Baseline publication label | Comparison internal ID | Comparison publication label | Baseline MAE | Comparison MAE | MAE change | Baseline RMSE | Comparison RMSE | RMSE change | Exact source path |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| ArGEnT-A → LC-PointNet | pooled | ArGEnT_self_att_noSDF | ArGEnT-A | PointNetMLPJoint_FP | LC-PointNet | 0.0160489277 | 0.0129620283 | −19.2343% | 0.0448796528 | 0.0286853955 | −36.0837% | `01_fp_vs_argent/pooled_metrics.csv` |
| ArGEnT-A → LC-PointNet | `log_life < 2` | ArGEnT_self_att_noSDF | ArGEnT-A | PointNetMLPJoint_FP | LC-PointNet | 0.2565481365 | 0.0478641540 | −81.3430% | 0.2722461522 | 0.0722229108 | −73.4715% | `01_fp_vs_argent/life_band_metrics.csv` |
| GC-PointNet → LC-PointNet | `log_life < 2` | PointNetMLPJoint | GC-PointNet | PointNetMLPJoint_FP | LC-PointNet | 0.0758519471 | 0.0478641540 | −36.8979% | 0.1034223586 | 0.0722229108 | −30.1660% | `01_fp_vs_argent/life_band_metrics.csv` |
| GC-PointNet → GC-PointNet + GF | pooled | PointNetMLPJoint | GC-PointNet | PointNetMLPJoint_headfeat | GC-PointNet + GF | 0.0164136626 | 0.0143827433 | −12.3734% | 0.0356734656 | 0.0312462449 | −12.4149% | `02_engineered_geometric_features/paired_headfeat_vs_baseline_by_life_bin.csv` |
| GC-PointNet → GC-PointNet + GF | `log_life < 2` | PointNetMLPJoint | GC-PointNet | PointNetMLPJoint_headfeat | GC-PointNet + GF | 0.0758519471 | 0.0586090833 | −22.7273% | 0.1034223586 | 0.0864018649 | −16.4597% | same |
| LC-PointNet → LC-PointNet + GF | pooled | PointNetMLPJoint_FP | LC-PointNet | PointNetMLPJoint_FP_headfeat | LC-PointNet + GF | 0.0129620275 | 0.0081498167 | −37.1254% | 0.0286853965 | 0.0176899042 | −38.3387% | same |
| LC-PointNet → LC-PointNet + GF | `log_life < 2` | PointNetMLPJoint_FP | LC-PointNet | PointNetMLPJoint_FP_headfeat | LC-PointNet + GF | 0.0478641503 | 0.0262005385 | −45.2426% | 0.0722229183 | 0.0473554879 | −34.4289% | same |
| LC-PointNet stress → no-stress | pooled | pnmlp_16932d84 | LC-PointNet | pnmlp_1bbaae12 | LC-PointNet (no stress) | 0.0129620275 | 0.0137612009 | +6.1655% | 0.0286853965 | 0.0300309826 | +4.6908% | `04_joint_stress_supervision/stress_vs_no_stress_paired_metrics.csv` |
| LC-PointNet stress → no-stress | `log_life < 2` | pnmlp_16932d84 | LC-PointNet | pnmlp_1bbaae12 | LC-PointNet (no stress) | 0.0478641503 | 0.0689726174 | +44.1008% | 0.0722229183 | 0.0982151058 | +35.9889% | same |

## Methodology and comparability verification

Implementation and metadata support a controlled FEM-grounded disc-like reduced-order benchmark with localized protrusion/drive-arm geometry, node-wise stress and base-10 log-life targets, geometry-conditioned point-cloud surrogates, hierarchical PointNet encoders, Fourier query mapping, and FP/native-resolution local features. The principal PointNet models have two outputs (stress and log-life). The ArGEnT comparator is cross-attention based and should be described in prose as **an adapted ArGEnT-inspired cross-attention operator (ArGEnT-A)**. `log_life < 2` is the consistently used short-life subgroup.

All principal comparisons use the recorded validation split, matching 679,000-node pooled coverage and 1,000 shared geometries where paired artifacts specify it. Full-test and short-life rows use the same target scale and bin definition. The data-efficiency metadata has matching fraction labels but reuses apparent full-model checkpoint filenames across fraction directories; this evidence is retained but should be provenance-qualified before publication.

## Stress/no-stress pairing

The valid PointNet pair is `Zonal/Edge/PointNetMLPJoint_FP/Trained_models/pnmlp_16932d84.pt` versus `Zonal/Edge_no_stress/PointNetMLPJoint_FP/Trained_models/pnmlp_1bbaae12.pt`, mapped to LC-PointNet stress versus LC-PointNet without stress. A separate valid ArGEnT-A pair also exists. No regular non-FP `PointNetMLPJoint` no-stress pair exists and none was used.

## Rejected/non-comparable evidence

- The prior `Comparison/results/abstract_evidence_audit.md` conclusions that CSVs were absent were rejected as stale; the committed result files listed above were found and recomputed.
- Legacy “Full test set” labels were not treated as an independent test split.
- The ArGEnT-A stress/no-stress rows were not used to support the LC-PointNet stress claim.
- Unmatched geometry, split, or family rows were not used for headline percentages.
- Data-efficiency checkpoint-path reuse prevents an unqualified claim about independently trained fractions.

## Revised abstract — Version 1: minimal-edit correction

Fatigue-life assessment of as-built engineering structures requires spatial predictions that remain reliable near localized regions of short life. Geometry-conditioned surrogate models are often evaluated using pooled field errors; however, aggregate metrics can conceal errors near geometric transitions where stress concentrations and nonlinear stress-to-life relationships make local fidelity important. This work presents a local-context geometry-conditioned point-cloud surrogate for spatial prediction of stress and logarithmic fatigue life on a controlled, FEM-grounded reduced-order disc benchmark.

The benchmark consists of disc-like contour geometries with localized protrusion/drive-arm features that introduce geometric complexity and spatially concentrated low-life regions within a limited domain. It is designed as a controlled testbed for comparing geometry-to-field surrogate behaviour rather than as a geometrically complete representation of a production component. FEM analysis provides node-wise stress and base-10 logarithmic fatigue-life targets. The proposed LC-PointNet uses a hierarchical PointNet-style geometry encoder and Fourier feature mappings of arbitrary spatial query coordinates to represent spatially varying field behaviour. Unlike the GC-PointNet baseline, LC-PointNet propagates multiscale encoder features to the native point resolution and supplies query-local geometric context to the prediction head. Stress and log-life are predicted jointly.

LC-PointNet is evaluated against GC-PointNet and an adapted ArGEnT-inspired cross-attention operator (ArGEnT-A). Performance is assessed using MAE and RMSE of log-life over the pooled validation split and across ordered life regimes, with `log_life < 2` treated as a fatigue-critical short-life region. On the evaluated Zonal/Edge validation split, LC-PointNet reduced pooled log-life MAE and RMSE by 19% and 36%, respectively, relative to ArGEnT-A. Within the short-life region, the reductions were 81% and 73%. Relative to GC-PointNet, the local feature-propagation pathway was associated with a 37% lower critical-region MAE. These are matched benchmark comparisons, not claims of universal superiority.

Additional ablations assess engineered geometric features, training-data availability, and joint stress–life supervision. In the evaluated matched ablations, GC-PointNet + GF and LC-PointNet + GF each reduced both pooled and short-life MAE/RMSE relative to their respective baselines, with different magnitudes. Across 10%, 25%, 50%, 75%, and 100% training fractions, LC-PointNet had lower short-life error than ArGEnT-A, while pooled rankings varied with fraction. Finally, removing stress prediction from the matched LC-PointNet FP model increased short-life log-life MAE and RMSE by 44% and 36%, respectively, and pooled increases were 6% and 5%. These results support the value of query-local context and joint stress–life supervision under the evaluated controlled benchmark.

## Revised abstract — Version 2: submission-ready

Fatigue-life surrogates for as-built structures must resolve localized short-life regions, where pooled field errors can obscure engineering-relevant failures. We study this problem on a controlled, FEM-grounded, reduced-order disc benchmark containing contour protrusion/drive-arm features and node-wise stress and base-10 logarithmic fatigue-life targets. The benchmark is intended to compare surrogate behaviour under controlled geometric complexity, not to represent a production component completely.

We compare two geometry-conditioned PointNet variants: GC-PointNet, which uses Fourier-mapped spatial query coordinates without a native-resolution feature-propagation pathway, and LC-PointNet, which propagates multiscale features to native resolution and supplies query-local context to its prediction head. Both jointly predict stress and log-life. An adapted ArGEnT-inspired cross-attention operator (ArGEnT-A) provides an attention-based comparator. We report log-life MAE and RMSE on a common validation-split evaluation and in ordered life bins, emphasizing `log_life < 2` as the short-life region.

On the evaluated Zonal/Edge split, LC-PointNet reduced pooled MAE/RMSE by 19%/36% versus ArGEnT-A; in the short-life region, reductions were 81%/73%. The matched LC-versus-GC comparison showed 37% lower short-life MAE for LC-PointNet. Engineered geometric features were evaluated independently: GC-PointNet + GF and LC-PointNet + GF both improved pooled and short-life MAE/RMSE relative to their corresponding baselines, but effect sizes differed by family and metric. In data-efficiency runs spanning 10–100% training fractions, LC-PointNet had lower short-life error than ArGEnT-A at each recorded fraction, whereas pooled rankings changed with training-set size. Removing stress supervision from the matched LC-PointNet FP model increased pooled MAE/RMSE by 6%/5% and short-life MAE/RMSE by 44%/36%.

Within this controlled FEM-grounded benchmark, the results support query-local context, engineered-feature ablations, and joint stress–life supervision as useful design dimensions for localized fatigue-life prediction. They do not establish performance for unseen production geometries or independent deployment conditions.
