# Model comparison summary

Repository commit: `ae6197d15a5a23c99f72ca45fd14f3cfb8e66df5`

Evaluation label: **validation-split evaluation**. The split is a deterministic 20% geometry holdout (seed 42); independence from checkpoint selection cannot be proved.

## Availability and compatibility

| regime   | model_family              | status     | checkpoint_path                                                                                                                  |
|:---------|:--------------------------|:-----------|:---------------------------------------------------------------------------------------------------------------------------------|
| Uniform  | ArGEnT_self_att_noSDF     | discovered | c:\Users\abfat\Desktop\Disc_lifing_paper_v2\Uniform\Edge\ArGEnT_self_att_noSDF\Trained_models\argent_self_nosdf_s_177b264d.pt    |
| Uniform  | PointNetMLPJoint          | discovered | c:\Users\abfat\Desktop\Disc_lifing_paper_v2\Uniform\Edge\PointNetMLPJoint\Trained_models\pn_s_full_ln_pos12_78193d0f.pt          |
| Uniform  | PointNetMLPJoint_FP       | discovered | c:\Users\abfat\Desktop\Disc_lifing_paper_v2\Uniform\Edge\PointNetMLPJoint_FP\Trained_models\pnmlp_16932d84.pt                    |
| Uniform  | PointNetMLPJoint_weighted | discovered | c:\Users\abfat\Desktop\Disc_lifing_paper_v2\Uniform\Edge\PointNetMLPJoint_weighted\Trained_models\pn_s_full_ln_pos12_78193d0f.pt |
| Zonal    | ArGEnT_self_att_noSDF     | discovered | c:\Users\abfat\Desktop\Disc_lifing_paper_v2\Zonal\Edge\ArGEnT_self_att_noSDF\Trained_models\argent_self_nosdf_s_177b264d.pt      |
| Zonal    | PointNetMLPJoint          | discovered | c:\Users\abfat\Desktop\Disc_lifing_paper_v2\Zonal\Edge\PointNetMLPJoint\Trained_models\pn_s_full_ln_pos12_78193d0f.pt            |
| Zonal    | PointNetMLPJoint_FP       | discovered | c:\Users\abfat\Desktop\Disc_lifing_paper_v2\Zonal\Edge\PointNetMLPJoint_FP\Trained_models\pnmlp_16932d84.pt                      |
| Zonal    | PointNetMLPJoint_weighted | discovered | c:\Users\abfat\Desktop\Disc_lifing_paper_v2\Zonal\Edge\PointNetMLPJoint_weighted\Trained_models\pn_s_full_ln_pos12_78193d0f.pt   |

## Principal metrics

| regime   | ablation   | model_family              | target   |          MSE |      RMSE |       MAE |   R2 (log) |   MAPE (%) |    MPE (%) |   Max_PE (%) |      RMSE_raw |   MSE_raw_life |   R2_raw_life |
|:---------|:-----------|:--------------------------|:---------|-------------:|----------:|----------:|-----------:|-----------:|-----------:|-------------:|--------------:|---------------:|--------------:|
| Uniform  | Edge       | ArGEnT_self_att_noSDF     | LogLife  |  0.00113394  | 0.0336741 | 0.0137403 |   0.999429 |    3.22282 |   0.250998 |      1424.41 |   1.31083e+07 |    1.71828e+14 |      0.999404 |
| Uniform  | Edge       | ArGEnT_self_att_noSDF     | Stress   | 36.7985      | 6.06617   | 2.04841   |   0.998906 |  nan       | nan        |       nan    | nan           |  nan           |    nan        |
| Uniform  | Edge       | PointNetMLPJoint          | LogLife  |  0.000888242 | 0.0298034 | 0.014685  |   0.999553 |    3.43521 |   0.592429 |      1417.72 |   2.12234e+07 |    4.50432e+14 |      0.998437 |
| Uniform  | Edge       | PointNetMLPJoint          | Stress   | 21.069       | 4.5901    | 2.02515   |   0.999374 |  nan       | nan        |       nan    | nan           |  nan           |    nan        |
| Uniform  | Edge       | PointNetMLPJoint_FP       | LogLife  |  0.000480881 | 0.021929  | 0.0105979 |   0.999758 |    2.46685 |   0.231972 |      3121.28 |   2.05032e+07 |    4.20382e+14 |      0.998541 |
| Uniform  | Edge       | PointNetMLPJoint_FP       | Stress   | 10.8539      | 3.29452   | 1.43805   |   0.999677 |  nan       | nan        |       nan    | nan           |  nan           |    nan        |
| Uniform  | Edge       | PointNetMLPJoint_weighted | LogLife  |  0.000861275 | 0.0293475 | 0.0143998 |   0.999566 |    3.34617 |   0.315118 |      2331.02 |   2.38367e+07 |    5.68188e+14 |      0.998028 |
| Uniform  | Edge       | PointNetMLPJoint_weighted | Stress   | 20.2414      | 4.49905   | 1.97708   |   0.999398 |  nan       | nan        |       nan    | nan           |  nan           |    nan        |
| Zonal    | Edge       | ArGEnT_self_att_noSDF     | LogLife  |  0.00201418  | 0.0448797 | 0.0160489 |   0.999002 |    3.83921 |   0.507221 |      1262.77 |   2.12325e+07 |    4.50818e+14 |      0.99744  |
| Zonal    | Edge       | ArGEnT_self_att_noSDF     | Stress   | 36.9148      | 6.07576   | 2.02581   |   0.998903 |  nan       | nan        |       nan    | nan           |  nan           |    nan        |
| Zonal    | Edge       | PointNetMLPJoint          | LogLife  |  0.0012726   | 0.0356735 | 0.0164137 |   0.999369 |    3.8508  |   0.672409 |      2437.37 |   3.02602e+07 |    9.15681e+14 |      0.994801 |
| Zonal    | Edge       | PointNetMLPJoint          | Stress   | 19.2555      | 4.38811   | 1.97455   |   0.999428 |  nan       | nan        |       nan    | nan           |  nan           |    nan        |
| Zonal    | Edge       | PointNetMLPJoint_FP       | LogLife  |  0.000822852 | 0.0286854 | 0.012962  |   0.999592 |    3.0437  |   0.305034 |      2151.8  |   2.15815e+07 |    4.65761e+14 |      0.997356 |
| Zonal    | Edge       | PointNetMLPJoint_FP       | Stress   | 12.2557      | 3.50082   | 1.57427   |   0.999636 |  nan       | nan        |       nan    | nan           |  nan           |    nan        |
| Zonal    | Edge       | PointNetMLPJoint_weighted | LogLife  |  0.00124753  | 0.0353204 | 0.0166509 |   0.999382 |    3.88386 |   0.163403 |      1221.65 |   3.91131e+07 |    1.52983e+15 |      0.991314 |
| Zonal    | Edge       | PointNetMLPJoint_weighted | Stress   | 18.0945      | 4.25376   | 1.96901   |   0.999462 |  nan       | nan        |       nan    | nan           |  nan           |    nan        |

## Interpretation: Uniform

FP versus regular PointNet pooled LogLife MAE: improves. Pooled R2 alone is not used to declare a winner.

## Interpretation: Zonal

FP versus regular PointNet pooled LogLife MAE: improves. Pooled R2 alone is not used to declare a winner.

## Limitations

Results are limited to discovered checkpoints and compatible clean-Edge schemas. Missing or failed models remain listed above. Raw-life percentage metrics are secondary diagnostics and may be inflated by small true-life values. Critical-node and subzone comparisons are evaluation-split diagnostics, not certification evidence.