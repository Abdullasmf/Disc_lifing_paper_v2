# GINOT integration report

- notebook: `Comparison/03_data_efficiency.ipynb`
- date/run environment: `2026-09-20`; static checkpoint/configuration validation only in sandbox (production HDF5 assets unavailable)
- GINOT checkpoint paths:
  - `Zonal/Edge_10/GINOT/Trained_models/ginot_a_match_250k_35ccca67_0.10.pt`
  - `Zonal/Edge_25/GINOT/Trained_models/ginot_a_match_250k_35ccca67_0.25.pt`
  - `Zonal/Edge_50/GINOT/Trained_models/ginot_a_match_250k_35ccca67_0.50.pt`
  - `Zonal/Edge_75/GINOT/Trained_models/ginot_a_match_250k_35ccca67_0.75.pt`
  - `Zonal/Edge/GINOT/Trained_models/ginot_a_match_250k_35ccca67.pt`
- selected GINOT preset: `MATCH_250K`
- architecture token resolution: `MATCH_250K`; `128 FPS geometry tokens`; `16 neighbors`; `244,946 trainable parameters for the standard joint model`
- split seed: `42` (verified from colocated training scripts)
- validation fraction: `0.20` (verified from colocated training scripts)
- validation geometry count: not executed in this sandbox
- evaluated node count: not executed in this sandbox
- strict checkpoint-load status: passed for all five fraction checkpoints via direct `GINOT_A` reconstruction from each ablation directory
- notebook execution actually completed: `false`
- regression checks for prior models passed: not run in this sandbox
- MATCH_250K_HIRES included in main outputs: `false`
