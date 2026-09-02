# Joint stress supervision validation report

Repository commit: `7c844bffb553985f439f49c8d69e0b46bdc6a61d`

Evaluation label: **validation-split evaluation**.

Checkpoint pairing now uses verified metadata instead of the previous brittle `fair_families` rule.
The prior empty-summary failure was caused by the old pairing pipeline treating missing checkpoint split metadata as `NaN` rather than missing and by relying on hard-coded family pairing assumptions.

## Valid stress/no-stress model pair(s)
| model_family          | fp_status   | stress_variant               | no_stress_variant            | stress_checkpoint_path                                                                                                      | no_stress_checkpoint_path                                                                                                             |
|:----------------------|:------------|:-----------------------------|:-----------------------------|:----------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------|
| ArGEnT-A              | non-FP      | argent_self_nosdf_s_177b264d | argent_self_nosdf_s_cf025919 | c:\Users\abfat\Desktop\Disc_lifing_paper_v2\Zonal\Edge\ArGEnT_self_att_noSDF\Trained_models\argent_self_nosdf_s_177b264d.pt | c:\Users\abfat\Desktop\Disc_lifing_paper_v2\Zonal\Edge_no_stress\ArGEnT_self_att_noSDF\Trained_models\argent_self_nosdf_s_cf025919.pt |
| LC-PointNet           | FP          | pnmlp_16932d84               | pnmlp_1bbaae12               | c:\Users\abfat\Desktop\Disc_lifing_paper_v2\Zonal\Edge\PointNetMLPJoint_FP\Trained_models\pnmlp_16932d84.pt                 | c:\Users\abfat\Desktop\Disc_lifing_paper_v2\Zonal\Edge_no_stress\PointNetMLPJoint_FP\Trained_models\pnmlp_1bbaae12.pt                 |

- No nonexistent regular `PointNetMLPJoint` no-stress model was included.
- Delta convention used everywhere: `delta = no_stress - stress`; positive means the stress-supervised model has lower error.

## Quantitative outcome
- Full test set MAE: suggests improvement from stress supervision (median Δ `+0.0010` decades).
- Full test set RMSE: suggests improvement from stress supervision (median Δ `+0.0010` decades).
- Critical short-life bin `log_life < 2`: suggests improvement from stress supervision (median Δ `+0.0132` decades).
