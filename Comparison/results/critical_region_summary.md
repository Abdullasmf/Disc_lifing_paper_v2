# Critical-region model comparison summary

Repository commit: `ae6197d15a5a23c99f72ca45fd14f3cfb8e66df5`

Evaluation label: **validation-split evaluation**. The 80/20 geometry split uses seed 42; independence from training, validation, early stopping, checkpoint selection, and hyperparameter selection is not proved.

## Compatibility

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

## Selected Zonal representatives

| selection          |   sample_id |   true_min_loglife |   true_min_life_cycles |   true_max_stress_mpa | governing_zone   | governing_subzone   |
|:-------------------|------------:|-------------------:|-----------------------:|----------------------:|:-----------------|:--------------------|
| median             |        1716 |            1.67306 |                47.1044 |               1179.31 | lower_transition | lower_transition    |
| critical_life      |        2809 |            1.13825 |                13.7482 |               1296.48 | lower_transition | lower_transition    |
| model_disagreement |        2146 |            2.03746 |               109.007  |               1105.59 | lower_transition | lower_transition    |

## Uniform results

Pooled metrics:

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

Low-life bins:

| regime   | ablation   | model_family              | bin       |   n_nodes |         MAE |        RMSE |   signed_mean_error |   max_abs_error | unstable   |
|:---------|:-----------|:--------------------------|:----------|----------:|------------:|------------:|--------------------:|----------------:|:-----------|
| Uniform  | Edge       | ArGEnT_self_att_noSDF     | all       |    679000 |   0.0137403 |   0.0336741 |        -0.00027612  |        1.1831   | False      |
| Uniform  | Edge       | ArGEnT_self_att_noSDF     | LogLife<4 |      6280 |   0.12525   |   0.151409  |         0.0088143   |        0.507604 | False      |
| Uniform  | Edge       | ArGEnT_self_att_noSDF     | LogLife<3 |      1414 |   0.155946  |   0.169619  |         0.0956192   |        0.437625 | False      |
| Uniform  | Edge       | ArGEnT_self_att_noSDF     | LogLife<2 |         0 | nan         | nan         |       nan           |      nan        | True       |
| Uniform  | Edge       | PointNetMLPJoint          | all       |    679000 |   0.014685  |   0.0298034 |         0.00151263  |        1.39359  | False      |
| Uniform  | Edge       | PointNetMLPJoint          | LogLife<4 |      6280 |   0.0549738 |   0.0789244 |         0.00563482  |        1.18119  | False      |
| Uniform  | Edge       | PointNetMLPJoint          | LogLife<3 |      1414 |   0.0509933 |   0.0733406 |         0.0198922   |        0.453522 | False      |
| Uniform  | Edge       | PointNetMLPJoint          | LogLife<2 |         0 | nan         | nan         |       nan           |      nan        | True       |
| Uniform  | Edge       | PointNetMLPJoint_FP       | all       |    679000 |   0.0105979 |   0.021929  |         0.000419853 |        1.50803  | False      |
| Uniform  | Edge       | PointNetMLPJoint_FP       | LogLife<4 |      6280 |   0.0340503 |   0.0547056 |         0.00378029  |        0.812903 | False      |
| Uniform  | Edge       | PointNetMLPJoint_FP       | LogLife<3 |      1414 |   0.031299  |   0.0491981 |         0.00659523  |        0.528033 | False      |
| Uniform  | Edge       | PointNetMLPJoint_FP       | LogLife<2 |         0 | nan         | nan         |       nan           |      nan        | True       |
| Uniform  | Edge       | PointNetMLPJoint_weighted | all       |    679000 |   0.0143998 |   0.0293475 |         0.00035537  |        1.38579  | False      |
| Uniform  | Edge       | PointNetMLPJoint_weighted | LogLife<4 |      6280 |   0.0565887 |   0.0785322 |         0.00919543  |        0.657222 | False      |
| Uniform  | Edge       | PointNetMLPJoint_weighted | LogLife<3 |      1414 |   0.057139  |   0.076437  |         0.0148467   |        0.326222 | False      |
| Uniform  | Edge       | PointNetMLPJoint_weighted | LogLife<2 |         0 | nan         | nan         |       nan           |      nan        | True       |

Lower-transition and subzone metrics:

| regime   | ablation   | model_family              | subzone_name     |   n_nodes |       MAE |      RMSE | status   |
|:---------|:-----------|:--------------------------|:-----------------|----------:|----------:|----------:|:---------|
| Uniform  | Edge       | ArGEnT_self_att_noSDF     | lower_transition |     66662 | 0.0361894 | 0.0731438 | ok       |
| Uniform  | Edge       | PointNetMLPJoint          | lower_transition |     66662 | 0.0217321 | 0.0419574 | ok       |
| Uniform  | Edge       | PointNetMLPJoint_FP       | lower_transition |     66662 | 0.0151365 | 0.029172  | ok       |
| Uniform  | Edge       | PointNetMLPJoint_weighted | lower_transition |     66662 | 0.0224272 | 0.0428382 | ok       |

Geometry-level critical summary:

| regime   | ablation   | model_family              |   n_geometries |   absolute_min_loglife_error_decades_median |   absolute_max_stress_error_mpa_median |   fraction_correct_critical_zone |   fraction_correct_critical_subzone |
|:---------|:-----------|:--------------------------|---------------:|--------------------------------------------:|---------------------------------------:|---------------------------------:|------------------------------------:|
| Uniform  | Edge       | ArGEnT_self_att_noSDF     |           1000 |                                   0.152185  |                               46.4321  |                            0.988 |                               0.988 |
| Uniform  | Edge       | PointNetMLPJoint          |           1000 |                                   0.0341077 |                                9.56665 |                            0.995 |                               0.995 |
| Uniform  | Edge       | PointNetMLPJoint_FP       |           1000 |                                   0.0219874 |                                5.80707 |                            0.995 |                               0.995 |
| Uniform  | Edge       | PointNetMLPJoint_weighted |           1000 |                                   0.0392729 |                               11.7866  |                            0.997 |                               0.997 |

FP versus regular PointNet: helps (median paired difference 0.01102; better on 63.6% of shared geometries). FP versus ArGEnT: helps (median paired difference 0.12545; better on 95.8% of shared geometries).
 Weighted versus regular PointNet: does not consistently help (median paired difference -0.00327; better on 46.1%).

## Zonal results

Pooled metrics:

| regime   | ablation   | model_family              | target   |          MSE |      RMSE |       MAE |   R2 (log) |   MAPE (%) |    MPE (%) |   Max_PE (%) |      RMSE_raw |   MSE_raw_life |   R2_raw_life |
|:---------|:-----------|:--------------------------|:---------|-------------:|----------:|----------:|-----------:|-----------:|-----------:|-------------:|--------------:|---------------:|--------------:|
| Zonal    | Edge       | ArGEnT_self_att_noSDF     | LogLife  |  0.00201418  | 0.0448797 | 0.0160489 |   0.999002 |    3.83921 |   0.507221 |      1262.77 |   2.12325e+07 |    4.50818e+14 |      0.99744  |
| Zonal    | Edge       | ArGEnT_self_att_noSDF     | Stress   | 36.9148      | 6.07576   | 2.02581   |   0.998903 |  nan       | nan        |       nan    | nan           |  nan           |    nan        |
| Zonal    | Edge       | PointNetMLPJoint          | LogLife  |  0.0012726   | 0.0356735 | 0.0164137 |   0.999369 |    3.8508  |   0.672409 |      2437.37 |   3.02602e+07 |    9.15681e+14 |      0.994801 |
| Zonal    | Edge       | PointNetMLPJoint          | Stress   | 19.2555      | 4.38811   | 1.97455   |   0.999428 |  nan       | nan        |       nan    | nan           |  nan           |    nan        |
| Zonal    | Edge       | PointNetMLPJoint_FP       | LogLife  |  0.000822852 | 0.0286854 | 0.012962  |   0.999592 |    3.0437  |   0.305034 |      2151.8  |   2.15815e+07 |    4.65761e+14 |      0.997356 |
| Zonal    | Edge       | PointNetMLPJoint_FP       | Stress   | 12.2557      | 3.50082   | 1.57427   |   0.999636 |  nan       | nan        |       nan    | nan           |  nan           |    nan        |
| Zonal    | Edge       | PointNetMLPJoint_weighted | LogLife  |  0.00124753  | 0.0353204 | 0.0166509 |   0.999382 |    3.88386 |   0.163403 |      1221.65 |   3.91131e+07 |    1.52983e+15 |      0.991314 |
| Zonal    | Edge       | PointNetMLPJoint_weighted | Stress   | 18.0945      | 4.25376   | 1.96901   |   0.999462 |  nan       | nan        |       nan    | nan           |  nan           |    nan        |

Low-life bins:

| regime   | ablation   | model_family              | bin       |   n_nodes |       MAE |      RMSE |   signed_mean_error |   max_abs_error | unstable   |
|:---------|:-----------|:--------------------------|:----------|----------:|----------:|----------:|--------------------:|----------------:|:-----------|
| Zonal    | Edge       | ArGEnT_self_att_noSDF     | all       |    679000 | 0.0160489 | 0.0448797 |        -0.000273757 |        1.65016  | False      |
| Zonal    | Edge       | ArGEnT_self_att_noSDF     | LogLife<4 |     13244 | 0.132626  | 0.180986  |         0.0169345   |        0.835135 | False      |
| Zonal    | Edge       | ArGEnT_self_att_noSDF     | LogLife<3 |      4521 | 0.204171  | 0.238482  |         0.0355005   |        0.70595  | False      |
| Zonal    | Edge       | ArGEnT_self_att_noSDF     | LogLife<2 |      1030 | 0.256548  | 0.272246  |         0.209851    |        0.561794 | False      |
| Zonal    | Edge       | PointNetMLPJoint          | all       |    679000 | 0.0164137 | 0.0356735 |         0.00138736  |        1.53254  | False      |
| Zonal    | Edge       | PointNetMLPJoint          | LogLife<4 |     13244 | 0.0765463 | 0.106805  |         0.00928888  |        1.1234   | False      |
| Zonal    | Edge       | PointNetMLPJoint          | LogLife<3 |      4521 | 0.07501   | 0.106181  |        -0.000228712 |        1.00626  | False      |
| Zonal    | Edge       | PointNetMLPJoint          | LogLife<2 |      1030 | 0.0758519 | 0.103422  |         0.017005    |        0.564409 | False      |
| Zonal    | Edge       | PointNetMLPJoint_FP       | all       |    679000 | 0.012962  | 0.0286854 |         0.000291688 |        1.41677  | False      |
| Zonal    | Edge       | PointNetMLPJoint_FP       | LogLife<4 |     13244 | 0.0527191 | 0.0813865 |         0.00436791  |        1.19859  | False      |
| Zonal    | Edge       | PointNetMLPJoint_FP       | LogLife<3 |      4521 | 0.0512473 | 0.0776518 |         0.00509563  |        0.975023 | False      |
| Zonal    | Edge       | PointNetMLPJoint_FP       | LogLife<2 |      1030 | 0.0478642 | 0.0722229 |         0.00593963  |        0.526988 | False      |
| Zonal    | Edge       | PointNetMLPJoint_weighted | all       |    679000 | 0.0166509 | 0.0353204 |        -0.000789489 |        1.30183  | False      |
| Zonal    | Edge       | PointNetMLPJoint_weighted | LogLife<4 |     13244 | 0.0687239 | 0.0979521 |         0.00944443  |        1.12112  | False      |
| Zonal    | Edge       | PointNetMLPJoint_weighted | LogLife<3 |      4521 | 0.0682828 | 0.0994022 |         0.0052805   |        1.12112  | False      |
| Zonal    | Edge       | PointNetMLPJoint_weighted | LogLife<2 |      1030 | 0.0700967 | 0.0975783 |         0.00813307  |        0.635679 | False      |

Lower-transition and subzone metrics:

| regime   | ablation   | model_family              | subzone_name     |   n_nodes |       MAE |      RMSE | status   |
|:---------|:-----------|:--------------------------|:-----------------|----------:|----------:|----------:|:---------|
| Zonal    | Edge       | ArGEnT_self_att_noSDF     | lower_transition |     66662 | 0.0494939 | 0.108841  | ok       |
| Zonal    | Edge       | PointNetMLPJoint          | lower_transition |     66662 | 0.0262196 | 0.0564096 | ok       |
| Zonal    | Edge       | PointNetMLPJoint_FP       | lower_transition |     66662 | 0.0193853 | 0.0434326 | ok       |
| Zonal    | Edge       | PointNetMLPJoint_weighted | lower_transition |     66662 | 0.0258517 | 0.0535673 | ok       |

Geometry-level critical summary:

| regime   | ablation   | model_family              |   n_geometries |   absolute_min_loglife_error_decades_median |   absolute_max_stress_error_mpa_median |   fraction_correct_critical_zone |   fraction_correct_critical_subzone |
|:---------|:-----------|:--------------------------|---------------:|--------------------------------------------:|---------------------------------------:|---------------------------------:|------------------------------------:|
| Zonal    | Edge       | ArGEnT_self_att_noSDF     |           1000 |                                   0.238401  |                               47.9099  |                            0.99  |                               0.99  |
| Zonal    | Edge       | PointNetMLPJoint          |           1000 |                                   0.055509  |                               10.6924  |                            0.996 |                               0.996 |
| Zonal    | Edge       | PointNetMLPJoint_FP       |           1000 |                                   0.0355375 |                                6.72443 |                            0.997 |                               0.997 |
| Zonal    | Edge       | PointNetMLPJoint_weighted |           1000 |                                   0.0497031 |                                9.66266 |                            0.996 |                               0.996 |

FP versus regular PointNet: helps (median paired difference 0.01518; better on 62.8% of shared geometries). FP versus ArGEnT: helps (median paired difference 0.19626; better on 95.9% of shared geometries).
 Weighted versus regular PointNet: helps (median paired difference 0.00257; better on 52.1% of shared geometries).

## Interpretation and limitations

FP improves pooled LogLife MAE and the available critical-region paired summaries in the reported data, but the conclusion is not universal and should be checked across bins, lower transition, localisation, and maximum stress. Pooled metrics and critical-region metrics can rank models differently. Raw-life MAPE/MPE/Max_PE are secondary diagnostics; raw-life Max_PE can be dominated by small true-life values. These are validation-split diagnostics, not independent test performance or certification evidence. Weighted-loss conclusions are based on paired critical metrics and do not assume LogLife-only weighting without code/checkpoint evidence.