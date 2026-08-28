# Comparison notebook suite

This directory contains notebook-driven, paper-facing evaluation for the trained disc-lifing checkpoints. The notebooks are designed to **reconstruct models from saved checkpoints, run validation-split inference on local HDF5 assets, and save tables/figures under `Comparison/results/`**.

## 1. Purpose of paper-results evaluation

The goal of the paper-results notebooks is not to retrain models; it is to produce a transparent, checkpoint-auditable comparison of node-level stress and fatigue-life prediction quality. The emphasis is on **local fatigue-critical behaviour** (minimum-life regions, lower-transition performance, and representative geometry maps), not only pooled global fit.

## 2. Notebook suite

The suite is organized around four paper analyses:

1. **`01_fp_vs_argent.ipynb`** – compares `PointNetMLPJoint_FP`, `PointNetMLPJoint`, and `ArGEnT_self_att_noSDF` on Uniform/Edge and Zonal/Edge.
2. **`02_engineered_geometric_features.ipynb`** – intended for the `Edge_arc_feat` ablation (`PointNetMLPJoint_headfeat`, `PointNetMLPJoint_FP_headfeat`, and ArGEnT counterpart where applicable).
3. **`03_data_efficiency.ipynb`** – intended for the `Edge_10`, `Edge_25`, `Edge_50`, and `Edge_75` subset comparison.
4. **`04_joint_stress_supervision.ipynb`** – intended for the `Edge_no_stress` / weighted-loss supervision study.

In this repository snapshot, notebook 01 is created explicitly; the other notebook names define the paper suite structure and expected follow-on analyses.

## 3. Example HDF5 files

Small illustrative/example files referenced by this suite should live at:

- `Comparison/Examples/disc_example_edge_deriv_uniform.h5`
- `Comparison/Examples/disc_example_edge_deriv_zonal.h5`

These examples are useful for schema inspection and demonstration, but they are **not a substitute** for the full local datasets needed to regenerate paper-scale tables.

## 4. Instructions for running notebooks

1. Open Jupyter from the repository root, or from `Comparison/` with the repository as the working tree parent.
2. Activate a kernel that has `torch`, `h5py`, `numpy`, `pandas`, and `matplotlib` installed.
3. Ensure the required HDF5 assets exist in `Data_gen/output/`.
4. Run the notebook from a **clean kernel** from top to bottom.
5. Inspect `Comparison/results/<notebook_name>/` for saved CSV, JSON, PNG, and PDF artifacts.

Notebook 01 auto-discovers checkpoints; it does not require manual editing of checkpoint paths when run in the tracked repository layout.

## 5. Required local assets

Paper-result notebooks rely on local assets that are usually not committed to Git:

- `Data_gen/output/disc_dataset_edge_deriv_uniform.h5`
- `Data_gen/output/disc_dataset_edge_deriv_zonal.h5`
- The trained checkpoint `.pt` files already present under the regime/model folders
- A valid Git checkout so the notebook can record `git rev-parse HEAD`

Optional/example-only assets:

- `Comparison/Examples/disc_example_edge_deriv_uniform.h5`
- `Comparison/Examples/disc_example_edge_deriv_zonal.h5`

## 6. Result provenance labels

All outputs from the current suite should be labelled **validation-split evaluation** unless you can independently prove that the evaluated geometries were not involved in training-time model selection, validation, or checkpoint choice. Notebook 01 writes this label into saved provenance and summary artifacts.

## 7. Principal metric definitions

The helper module `eval_helpers.py` computes the main paper diagnostics:

- **Pooled metrics**: node-level pooled stress and log-life MSE / RMSE / MAE / R².
- **Low-life bin metrics**: log-life errors for all nodes, `LogLife<4`, `LogLife<3`, and `LogLife<2` subsets.
- **Subzone metrics**: MAE / RMSE over principal subzones such as `lower_transition`, `front_cgroove`, and rear-arm regions.
- **Geometry-level metrics**: per-geometry minimum-life error, critical-node localisation distance, maximum-stress error, and same-zone agreement.
- **Paired comparisons**: geometry-by-geometry differences between competing families so sign conventions stay explicit.

## 8. Why pooled R² and raw-life Max_PE must not be interpreted alone

A very high pooled **R²** can coexist with poor behaviour in the fatigue-critical tail because most nodes are easier than the minimum-life region. Likewise, raw-life **`Max_PE (%)`** can be dominated by a small number of very low true-life values, making it too volatile to rank models by itself.

For this reason, the notebooks treat pooled metrics as necessary but insufficient evidence. Low-life bins, lower-transition/subzone metrics, paired minimum-life comparisons, and representative field maps must all be checked before drawing conclusions about local fatigue-critical usefulness.

## 9. Output artifact structure under `Comparison/results/`

Each notebook writes into its own subdirectory, for example:

```text
Comparison/results/
  01_fp_vs_argent/
    checkpoint_integrity.json
    evaluation_split_provenance.json
    node_results.csv
    pooled_metrics.csv
    low_life_bins.csv
    subzone_metrics.csv
    geometry_level_metrics.csv
    geometry_level_summary.csv
    paired_argent_minus_fp.csv
    paired_pointnet_minus_fp.csv
    representative_geometry_ids.json
    run_metadata.json
    artifact_listing.json
    figures/
      uniform/
      zonal/
```

The exact file list can grow as new figures or summaries are added, but the notebook should always emit an artifact listing for traceability.

## 10. Scope exclusions

These notebooks do **not**:

- train or fine-tune models,
- change checkpoints,
- certify physical validity beyond the stored datasets,
- replace independent test-set evaluation,
- or claim deployment readiness.

They are paper-support tools for transparent comparison of already trained research models.
