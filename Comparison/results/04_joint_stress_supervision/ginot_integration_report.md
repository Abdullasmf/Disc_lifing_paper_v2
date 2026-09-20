# GINOT integration report

- notebook: `Comparison/04_joint_stress_supervision.ipynb`
- date/run environment: `2026-09-20`; static checkpoint/configuration validation only in sandbox (production HDF5 assets unavailable)
- GINOT checkpoint paths:
  - joint stress–life: `Zonal/Edge/GINOT/Trained_models/ginot_a_match_250k_35ccca67.pt`
  - life only: `Zonal/Edge_no_stress/GINOT/Trained_models/ginot_a_match_250k_25c02577.pt`
- selected GINOT preset: `MATCH_250K`
- architecture token resolution: `MATCH_250K`; `128 FPS geometry tokens`; `16 neighbors`; `244,946 trainable parameters for the standard joint model`
- split seed: `42` (verified from colocated training scripts)
- validation fraction: `0.20` (verified from colocated training scripts)
- validation geometry count: not executed in this sandbox
- evaluated node count: not executed in this sandbox
- strict checkpoint-load status: passed for both joint and life-only checkpoints via direct `GINOT_A` reconstruction from each ablation directory
- notebook execution actually completed: `false`
- regression checks for prior models passed: not run in this sandbox
- MATCH_250K_HIRES included in main outputs: `false`
