# GINOT integration report

- notebook: `Comparison/02_engineered_geometric_features.ipynb`
- date/run environment: `2026-09-20`; static checkpoint/configuration validation only in sandbox (production HDF5 assets unavailable)
- GINOT checkpoint paths:
  - baseline: `Zonal/Edge/GINOT/Trained_models/ginot_a_match_250k_35ccca67.pt`
  - engineered geometric features: `Zonal/Edge_arc_feat/GINOT/Trained_models/ginot_a_match_250k_3f22269e.pt`
- selected GINOT preset: `MATCH_250K`
- architecture token resolution: `MATCH_250K`; `128 FPS geometry tokens`; `16 neighbors`; `244,946 trainable parameters for the standard joint model`
- split seed: `42` (verified from colocated training scripts)
- validation fraction: `0.20` (verified from colocated training scripts)
- validation geometry count: not executed in this sandbox
- evaluated node count: not executed in this sandbox
- strict checkpoint-load status: passed for both plain and GF checkpoints via direct `GINOT_A` reconstruction from each ablation directory
- GF feature columns verified: `arc_length_mm`, `tangent_x`, `tangent_r`, `curvature`, `curvature_gradient`
- notebook execution actually completed: `false`
- regression checks for prior models passed: not run in this sandbox
- MATCH_250K_HIRES included in main outputs: `false`
