# Golden receipt: LQC boundary probe v2 (recalibrated `rho_crit`) — diagnostic only

Date: 2026-03-08

## Provenance
- Script: `notebooks/lqc_boundary_probe_v2.py`
- Aggregate: `lqc_boundary_probe_v2_summary.json`

## Parameters
- `Ω_m = 0.31`
- `α_qg in {3e-7, 7e-7, 1.3e-6}`
- `rho_crit_mult in {0.5, 1.0, 2.0}`
- `rho_crit = rho_crit_mult * rho_scale`
- `rho_scale ≈ 269954.5386849377` (calibrated to `rho_at_min_a` from semiclassical reference at `α_ref=7e-7`)

## Aggregate metrics
- `n_cases = 9`, `n_valid = 9`
- `best_max_ratio = 3.230739459675965`
- `worst_max_ratio = 4.036933887240834`
- `any_ratio_below_1 = false`
- `q1_refinement_pass_rate = 0.0`
- `min_of_min_a = 0.005665633933605737`

## Interpretation
Recalibration restored deep-collapse regime comparability (`min_a ≈ 0.0057`), but this LQC-style parameterization still fails to suppress transient dominance (`ratio > 3` for all cases). Refinement stability also degrades (`pass_rate = 0.0`).

## Governance posture
- Pure diagnostic branch — no claim promotion
- No envelope/status change
- C-WDW-001 core status and edge caveat remain unchanged
