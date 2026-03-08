# Golden Boundary Receipt — Ω_m = 0.31 (2026-03-08)

This folder is the canonical receipt for the boundary confirmation mini-sweep at `Ω_m = 0.31`.

## Provenance
- Script: `notebooks/edge_boundary_confirmation_sweep.py`
- Aggregate: `edge_boundary_sweep_aggregate.json`
- Summary rows: `edge_boundary_sweep_summary.csv`

## Aggregate snapshot
- `n_rows = 8` (log-spaced `α_qg` in `[3e-7, 1.3e-6]`)
- `q1_refinement_threshold = 1e-6`
- `pass_q1_refinement_rate = 0.625` (5/8)
- `max_q1_refinement = 1.1974288492057357e-06`
- `min_q1_refinement = 6.325536276250695e-07`
- `max_ratio_correction_over_classical = 3.912248034016738`
- `min_ratio_correction_over_classical = 3.85322455364174`
- `min_of_min_a = 0.007908996390581277`
- `all_ratio_exceeds_1 = true`

## Interpretation
- Numerical tractability at the `Ω_m = 0.31` boundary is strong but marginal under strict `q1_refinement <= 1e-6` (5/8 pass, worst point slightly above threshold).
- Physical caveat is reaffirmed across the entire sample: transient non-perturbative dominance persists (`correction/classical > 1` at all points).

## Governance posture
- Keep `Ω_m <= 0.31` as exploratory/partial inclusion under mandatory constraints:
  1) adaptive refinement,
  2) Radau baseline stiff solver,
  3) overlapping-time interpolation for refinement metrics.
- Physical interpretation in this lane requires explicit semiclassical validity caveat.
