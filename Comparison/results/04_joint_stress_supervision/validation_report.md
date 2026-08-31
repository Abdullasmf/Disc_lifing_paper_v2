# Joint stress supervision validation report

Repository commit: `ddaee34d2731dcfd06546c32f62b0ec9d863f9bf`

Evaluation label: **validation-split evaluation**.

Checkpoint pairing now uses verified metadata instead of the previous brittle `fair_families` rule.
The prior empty-summary failure was caused by the old pairing pipeline treating missing checkpoint split metadata as `NaN` rather than missing and by relying on hard-coded family pairing assumptions.

## Valid stress/no-stress model pair(s)
| model_family          | fp_status   | stress_variant               | no_stress_variant            | stress_checkpoint_path                                                                                                                      | no_stress_checkpoint_path                                                                                                                             |
|:----------------------|:------------|:-----------------------------|:-----------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------|
| ArGEnT_self_att_noSDF | non-FP      | argent_self_nosdf_s_177b264d | argent_self_nosdf_s_cf025919 | /home/runner/work/Disc_lifing_paper_v2/Disc_lifing_paper_v2/Zonal/Edge/ArGEnT_self_att_noSDF/Trained_models/argent_self_nosdf_s_177b264d.pt | /home/runner/work/Disc_lifing_paper_v2/Disc_lifing_paper_v2/Zonal/Edge_no_stress/ArGEnT_self_att_noSDF/Trained_models/argent_self_nosdf_s_cf025919.pt |
| PointNetMLPJoint_FP   | FP          | pnmlp_16932d84               | pnmlp_1bbaae12               | /home/runner/work/Disc_lifing_paper_v2/Disc_lifing_paper_v2/Zonal/Edge/PointNetMLPJoint_FP/Trained_models/pnmlp_16932d84.pt                 | /home/runner/work/Disc_lifing_paper_v2/Disc_lifing_paper_v2/Zonal/Edge_no_stress/PointNetMLPJoint_FP/Trained_models/pnmlp_1bbaae12.pt                 |

- No nonexistent regular `PointNetMLPJoint` no-stress model was included.
- Delta convention used everywhere: `delta = no_stress - stress`; positive means the stress-supervised model has lower error.

## Quantitative outcome
- Full test set MAE: insufficient evidence (median Δ `+nan` decades).
- Full test set RMSE: insufficient evidence (median Δ `+nan` decades).
- Critical short-life bin `log_life < 2`: insufficient evidence (median Δ `+nan` decades).

## Limitation
- Dataset unavailable: `/home/runner/work/Disc_lifing_paper_v2/Disc_lifing_paper_v2/Data_gen/output/disc_dataset_edge_deriv_zonal.h5`. Notebook execution still completed and saved checkpoint, pairing, and empty schema-stable result artifacts, but no inference figures/metrics could be regenerated in this environment.
