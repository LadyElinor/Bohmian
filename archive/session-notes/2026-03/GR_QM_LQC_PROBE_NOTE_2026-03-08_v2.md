# LQC-style Boundary Probe Note v2 (2026-03-08)

## Scope
- Diagnostic-only recalibrated LQC micro probe at `Ω_m = 0.31`
- Script: `notebooks/lqc_boundary_probe_v2.py`
- Cases: 9 (`α_qg in {3e-7, 7e-7, 1.3e-6}` × `rho_crit_mult in {0.5, 1.0, 2.0}`)
- Receipt: `notebooks/outputs/grqm_lqc_boundary_probe_v2_20260308_151423/lqc_boundary_probe_v2_summary.json`

## Calibration
- `rho_scale` calibrated from semiclassical boundary reference at `α_ref = 7e-7`
- `rho_scale_used = 269954.5386849377` (toy units)
- `rho_crit = rho_crit_mult * rho_scale`

## Aggregate outcome
- `n_cases = 9`, `n_valid = 9`
- `best_max_ratio = 3.230739459675965`
- `worst_max_ratio = 4.036933887240834`
- `any_ratio_below_1 = false`
- `q1_refinement_pass_rate = 0.0`
- `min_of_min_a = 0.005665633933605737`

## Interpretation
- Recalibration restored deep-collapse comparability (`min_a` in the same edge-collapse regime), but transient dominance still persists (`ratio > 3` in every case).
- This parameterization does not produce a perturbative boundary recovery at `Ω_m = 0.31`.
- Refinement stability worsened relative to the adaptive semiclassical path (`q1_refinement_pass_rate = 0`).

## Governance posture
- Diagnostic-only result; no claim promotion.
- No envelope/status mutation.
- Core C-WDW-001 and edge caveat posture unchanged.
