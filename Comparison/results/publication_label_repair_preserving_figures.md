# Publication-label repair (preserving figures): additive report

Repository commit inspected/produced by this pass: `a279bc8226959e9da791ca4d6161c188ba954be8`
(the merged `copilot/mandatory-final-figure-repair-pass` state, which itself claimed to fix
the `Zonal Edge_arc_feat` life-band title and add the strict `resolve_publication_label`
resolver — see `Comparison/results/publication_figure_label_and_layout_validation.md`).

This report is additive: it does not overwrite `publication_figure_label_and_layout_validation.md`,
`abstract_evidence_audit.md`, `abstract_evidence_audit_final.md`, or
`final_abstract_repository_verification.md`, which record prior audit passes.

**Environment blocker (read this first, unchanged from the prior pass):** this sandbox has no
`torch`, no `h5py`, and no `Data_gen/output/*.h5` production dataset, and the repository ships no
committed figure PNGs (`Comparison/results/**/figures/` is `.gitignore`'d). It is therefore
impossible in this environment to execute notebooks 01/02/04 end to end or open a regenerated
`.png`/`.pdf`. Every change below was verified by (a) static inspection of the notebook JSON/
source, (b) `json.load`/`ast.parse` syntax checks on every edited notebook/module, and (c)
standalone unit tests of the new/changed `eval_helpers.py` functions using synthetic DataFrames
and a real Matplotlib `Agg` backend (`resolve_publication_label`, `ordered_model_families`,
`presentation_table`, and `validate_no_raw_publication_labels` were all executed directly on
representative inputs and their outputs inspected — see §D for the exact commands/output). The
*logic* that produces labels was executed; the *actual paper figures* could not be regenerated
against real model checkpoints in this sandbox.

---

## A. Preservation verification

No filtering, DataFrame-selection, model-inclusion, or plotted-value logic was touched anywhere
in this pass. Every change below is a reader-facing string (resolver mapping, figure title/ylabel
text, or notebook Markdown). Model sets, orderings (aside from adding new order entries — see §B),
panel structure, life bins, full-set-vs-per-bin separation, checkpoint discovery, and output
filenames are unchanged.

| Notebook / figure | Models before repair | Models after repair | Metric data changed? | Filters changed? | Plot structure changed? | Text-only repair confirmed? |
|---|---|---|---|---|---|---|
| `04_joint_stress_supervision.ipynb` — `stress_vs_no_stress_<model_family>_<fp_status>_fullset_separate` (any pair where `model_family == 'PointNetMLPJoint_weighted'`) | Same discovered stress/no-stress checkpoint pair (unchanged discovery/pairing logic) | Identical pair; only `publication_label = eh.display_model_name(model_family)` now resolves instead of raising | No | No | No | Yes — only the resolved label text changes |
| `02_engineered_geometric_features.ipynb` — `figure_headfeat_vs_baseline_delta` | `ArGEnT_self_att_noSDF` (+GF), `PointNetMLPJoint_headfeat`, `PointNetMLPJoint_FP_headfeat` vs their baselines | Identical set/order (`FAMILIES`/`ABLATION_TO_BASELINE_FAMILY` untouched) | No | No | No | Yes — only the `(GF − baseline)` title and `'GF − baseline [decades]'` ylabels changed to `(GF − no-GF)` / `'GF − no-GF [decades]'` |
| `02_engineered_geometric_features.ipynb` — `figure_headfeat_vs_baseline_by_life_bin` | Same as above | Same as above | No | No | No | Yes — same ylabel-only substitution (4 occurrences total across both figures) |
| `01_fp_vs_argent.ipynb` — `figure_qualitative_example_regular` | Every family present in `zonal_selected`/`by_model` after successful `reconstruct()` (unchanged: still `ArGEnT_self_att_noSDF`, `PointNetMLPJoint`, `PointNetMLPJoint_FP`, whichever load without exception) | Identical `by_model` dict and iteration; only the `fig.suptitle(...)` string and the "saved" Markdown line changed | No | No | No | Yes — column-per-model panels, per-panel titles (already resolved via `plot_field_comparison`'s default `label_fn=display_model_name`), true/pred/error scatter data, extrema markers, and output path are byte-for-byte the same logic as before |

No row required removing, hiding, or reordering a plotted model. `PointNetMLPJoint_weighted` in
particular remains fully included wherever it was already discovered/plotted; only its display
string changed (from raising `UnresolvedPublicationLabelError` to `GC-PointNet (weighted loss)`).

---

## B. Complete model identity mapping

All identities are now expressed as a structured `PublicationModelIdentity` (architecture + GF
status + training condition) in `Comparison/eval_helpers.py::MODEL_IDENTITIES`, and formatted
centrally by `format_publication_model_label()`, replacing the previous flat
`DISPLAY_MODEL_NAMES` string table (which is now *derived* from `MODEL_IDENTITIES` for
backward-compatible call sites, not hand-maintained).

| Internal model ID | Architecture | GF status | Training condition | Supervision state | Final publication label | Evidence source |
|---|---|---|---|---|---|---|
| `PointNetMLPJoint` | GC-PointNet | no GF | standard | not_applicable (resolved per-notebook via `format_supervision_label`) | `GC-PointNet` | `pn.build_model_from_arch` (non-FP) in every notebook's `reconstruct()`; e.g. `Comparison/02_engineered_geometric_features.ipynb` cell 8, `Comparison/01_fp_vs_argent.ipynb` `reconstruct()` |
| `PointNetMLPJoint_headfeat` | GC-PointNet | + GF | standard | n/a | `GC-PointNet + GF` | same `build_model_from_arch` path, `_headfeat` suffix routes through `predict_headfeat`/`extra_feat_cols` in `02_engineered_geometric_features.ipynb` |
| `PointNetMLPJoint_FP` | LC-PointNet | no GF | standard | n/a | `LC-PointNet` | `pn.build_fp_model_from_arch` (native-resolution FP propagation) in every notebook's `reconstruct()` |
| `PointNetMLPJoint_FP_headfeat` | LC-PointNet | + GF | standard | n/a | `LC-PointNet + GF` | `build_fp_model_from_arch` + `_headfeat` suffix, `02_engineered_geometric_features.ipynb` |
| `PointNetMLPJoint_weighted` | GC-PointNet | no GF | weighted_loss | n/a | `GC-PointNet (weighted loss)` | Loaded via the exact same `pn.build_model_from_arch` (non-FP) path as plain `PointNetMLPJoint` in every notebook's `reconstruct()` (`elif family in ('PointNetMLPJoint', 'PointNetMLPJoint_weighted', ...)`). Confirmed directly against the checkpoint directory: `Zonal/Edge/PointNetMLPJoint_weighted/pn_models.py` defines only `build_model_from_arch` (no `build_fp_model_from_arch`), and `Training_script_weighted.py` sets `EXTRA_FEAT_COLS: List[int] = []` (no engineered geometric features). Only its (weighted) training loss differs from plain `PointNetMLPJoint`. |
| `ArGEnT_self_att_noSDF` | ArGEnT-A | ablation-directory dependent (`geometric_features` override) | standard | n/a | `ArGEnT-A` or `ArGEnT-A + GF` | `bench.ArGEnTDeepONet` build path; `02_engineered_geometric_features.ipynb`'s `FEATURE_AUGMENTED_ARGENT_FAMILY` comment documents that the checkpoint loaded from `Edge_arc_feat` is the GF-augmented comparator, resolved via `resolve_publication_label(..., geometric_features=True)` |
| checkpoint/hash aliases (`pnmlp_*`, `argent_self_*`) | n/a | n/a | n/a | n/a | Never rendered in a paper-facing figure | These are prohibited tokens in `PROHIBITED_PUBLICATION_TOKENS`; no notebook cell in 01/02/04 constructs a paper-facing string from a checkpoint hash or `Path.stem` — all resolved labels go through `display_model_name`/`resolve_publication_label` |

`format_publication_model_label` composes exactly `architecture [+ GF] [(weighted loss)]`, so
adding the `PointNetMLPJoint_weighted` entry required no change to the formatting function itself,
only a new `MODEL_IDENTITIES` row — confirming the resolver is now a structured composition rather
than a short fixed dictionary that must be extended per-string.

---

## C. Text replacement verification

| Figure | Raw text removed | Final publication-facing text | Figure regenerated and inspected |
|---|---|---|---|
| `04_joint_stress_supervision.ipynb` weighted-loss pair figure(s) | `UnresolvedPublicationLabelError: model_internal_id='PointNetMLPJoint_weighted'` (figure generation halted before any text was rendered) | `GC-PointNet (weighted loss)` used everywhere `publication_label` is interpolated (bar/line legend labels, `fig.suptitle`) | Not regenerated (no torch/h5py/dataset in this sandbox); resolver logic unit-tested (see §D) and cross-checked against the actual `PointNetMLPJoint_weighted` checkpoint directory (see §B) |
| `02_engineered_geometric_features.ipynb` `figure_headfeat_vs_baseline_delta` | `ax.set_title(..."(GF − baseline)"...)`, `ax.set_ylabel('GF − baseline [decades]')` — contains the prohibited token `baseline` | `(GF − no-GF)` title suffix; `'GF − no-GF [decades]'` ylabel | Not regenerated (env blocker); `validate_no_raw_publication_labels` unit-tested to reject the old ylabel and accept the new one (see §D) |
| `02_engineered_geometric_features.ipynb` `figure_headfeat_vs_baseline_by_life_bin` | Same `'GF − baseline [decades]'` ylabel (2 occurrences: full-set delta panel, per-bin delta panel) | Same `'GF − no-GF [decades]'` substitution | Not regenerated (env blocker); same unit test as above |
| `01_fp_vs_argent.ipynb` `figure_qualitative_example_regular` | `'Regular-model inference illustration — Zonal / Edge regimemodels (ArGEnT, PointNetMLPJoint, PointNetMLPJoint_FP).\n...'` — contains `regular`, `PointNetMLPJoint`, `PointNetMLPJoint_FP` | `'Qualitative log-life field predictions on a representative geometry\nIllustrative FEM-generated example; quantitative comparisons use the geometry-level held-out validation split.\nModels: <resolved labels for the models actually present in by_model>'` | Not regenerated (env blocker); title string statically inspected, contains no prohibited token, and `qualitative_model_labels` is built from `eh.display_model_name`/`eh.ordered_model_families` over `by_model.keys()` (never a hard-coded model list), so it always matches the models actually shown |
| `01_fp_vs_argent.ipynb` completion Markdown | `'**Regular-model illustration saved** — ...'` | `'**Qualitative illustration saved** — ...'` | Notebook Markdown only; no figure impact |
| Stress-supervision figures (`04_joint_stress_supervision.ipynb`) | N/A — already used `format_supervision_label`-equivalent `(joint stress–life)`/`(life only)` wording and `'life-only − joint stress–life [decades]'` ylabels before this pass | Unchanged (already correct); confirmed no raw `with stress`/`no stress`/`with-stress`/`no-stress` token present | Statically re-verified in this pass; no change needed |
| Engineered-GF figures (`02_engineered_geometric_features.ipynb`) | See `figure_headfeat_vs_baseline_delta`/`_by_life_bin` rows above | Delta labels for tick labels/legends already used `display_model_name(...)`-resolved pairs (e.g. `GC-PointNet + GF\nvs\nGC-PointNet`); only the two ylabel/title strings above needed fixing | Not regenerated (env blocker) |
| All qualitative plots (`plot_field_comparison` call sites in 01/02) | N/A — per-panel titles already used the default `label_fn=display_model_name` resolver | Unchanged; only the notebook 01 qualitative suptitle needed fixing (see above) | Not regenerated (env blocker) |

---

## D. Execution status

- **Kernels restarted:** not applicable in this sandbox — no Jupyter kernel/runtime is available
  (no `torch`, no `h5py`, no `Data_gen/output/*.h5`). This is the same environment blocker recorded
  in the prior pass's report.
- **Cells/notebooks run:** notebooks 01/02/04 could **not** be executed end to end in this
  sandbox. Instead:
  - Every edited notebook (`01_fp_vs_argent.ipynb`, `02_engineered_geometric_features.ipynb`) was
    parsed with `json.load(...)` after editing to confirm well-formed notebook JSON.
  - `Comparison/eval_helpers.py` was checked with `ast.parse(...)`.
  - The changed/added `eval_helpers.py` functions were unit-tested directly against synthetic
    inputs with a real Matplotlib `Agg` backend:
    ```
    PointNetMLPJoint -> GC-PointNet
    PointNetMLPJoint_headfeat -> GC-PointNet + GF
    PointNetMLPJoint_FP -> LC-PointNet
    PointNetMLPJoint_FP_headfeat -> LC-PointNet + GF
    PointNetMLPJoint_weighted -> GC-PointNet (weighted loss)
    ArGEnT_self_att_noSDF -> ArGEnT-A
    ArGEnT+GF -> ArGEnT-A + GF
    correctly raised: Unresolved publication label for a plotted model. model_internal_id='SomeUnknown...'
    ['PointNetMLPJoint', 'PointNetMLPJoint_weighted', 'ArGEnT_self_att_noSDF']   # ordered_model_families
    validator passed for clean text
    correctly rejected baseline token
    ```
    and `presentation_table` was confirmed to resolve `PointNetMLPJoint_weighted` to
    `GC-PointNet (weighted loss)` in a rendered table instead of raising.
- **Figures saved and visually inspected:** not possible in this sandbox (no committed PNGs, no
  ability to run inference). All three fixes were verified by static inspection of the exact
  strings that will populate the figure's suptitle/axes-title/ylabel, cross-checked against
  `PROHIBITED_PUBLICATION_TOKENS` by running the real `validate_no_raw_publication_labels`
  function on synthetic figures containing those strings (see above).
- **Exact output paths (unchanged filenames/directories):**
  - `Comparison/results/01_fp_vs_argent/figures/zonal/figure_qualitative_example_regular.png`
  - `Comparison/results/02_engineered_geometric_features/figures/figure_headfeat_vs_baseline_delta.png`
  - `Comparison/results/02_engineered_geometric_features/figures/figure_headfeat_vs_baseline_by_life_bin.png`
  - `Comparison/results/04_joint_stress_supervision/figures/stress_vs_no_stress_<model_family>_<fp_status>_fullset_separate.png`
- **Unresolved mapping:** none remaining after inspecting the `PointNetMLPJoint_weighted`
  checkpoint directory's own `pn_models.py`/`Training_script_weighted.py`. All internal ids
  enumerated in the task (`PointNetMLPJoint`, `PointNetMLPJoint_FP`, `PointNetMLPJoint_headfeat`,
  `PointNetMLPJoint_FP_headfeat`, `PointNetMLPJoint_weighted`, `ArGEnT_self_att_noSDF`) are present
  in `MODEL_IDENTITIES` and resolve without falling back to a raw identifier. The strict
  `UnresolvedPublicationLabelError` remains enabled for any truly unmapped id.

---

## E. What changed in `Comparison/eval_helpers.py`

- Added `PublicationModelIdentity` (frozen dataclass: `architecture`, `has_geometric_features`,
  `training_condition`, `supervision`) and `format_publication_model_label(identity)`.
- Replaced the flat `DISPLAY_MODEL_NAMES` literal with `MODEL_IDENTITIES: Dict[str,
  PublicationModelIdentity]` (one verified entry per internal id, including the new
  `PointNetMLPJoint_weighted -> GC-PointNet (weighted loss)` entry) plus a derived
  `DISPLAY_MODEL_NAMES` dict for any call site that only needs the flat string.
- Extended `DISPLAY_MODEL_ORDER` with the three weighted-loss labels actually reachable via
  `MODEL_IDENTITIES` (`GC-PointNet (weighted loss)`, `LC-PointNet (weighted loss)`) so
  `ordered_model_families` places them deterministically instead of falling through to the
  unranked tail bucket.
- `resolve_publication_label` now looks up `MODEL_IDENTITIES` and raises
  `UnresolvedPublicationLabelError` (unchanged strict behaviour, still never falls back to the raw
  id) for anything not in the verified table; the `ArGEnT_self_att_noSDF` + `geometric_features`
  override path is preserved exactly as before.
- No change to `PROHIBITED_PUBLICATION_TOKENS`, `validate_no_raw_publication_labels`,
  `format_supervision_label`, or `format_gf_delta_label` — the strict validator remains fully
  enabled and unweakened.
