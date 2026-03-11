# GR_QM Edge Boundary Sweep Note (2026-03-08)

## Scope
- Boundary check at `Ω_m = 0.31`
- `α_qg` sampled at 8 log-spaced points in `[3e-7, 1.3e-6]`
- Method path: adaptive refinement + Radau dense solve
- Script: `notebooks/edge_boundary_confirmation_sweep.py`
- Artifact: `notebooks/outputs/grqm_edge_boundary_sweep_omega031_20260308_122537/`

## Aggregate results
- `n_rows = 8`
- `q1_refinement_threshold = 1e-6`
- `pass_q1_refinement_rate = 0.625` (5/8 pass)
- `max_q1_refinement = 1.1974288492057357e-06`
- `min_q1_refinement = 6.325536276250695e-07`
- `max_ratio_correction_over_classical = 3.912248034016738`
- `min_ratio_correction_over_classical = 3.85322455364174`
- `min_of_min_a = 0.007908996390581277`
- `all_ratio_exceeds_1 = true`

## Interpretation
- Numerical tractability is strong but not uniformly below the strict `1e-6` q1-refinement threshold at `Ω_m = 0.31` across this 8-point sample.
- Physical caveat remains strongly confirmed at the boundary: correction/classical ratio exceeds 1 for all sampled points, with peak around 3.91 and `min_a` near `0.008`.

## Governance implication
- Treat `Ω_m = 0.31` as exploratory/conditional boundary pending either:
  1) tightened adaptive settings that recover full-threshold pass at this boundary, or
  2) explicit policy wording that records boundary partial-pass behavior.
