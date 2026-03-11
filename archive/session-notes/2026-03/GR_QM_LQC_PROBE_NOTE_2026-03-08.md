# LQC-style Boundary Probe Note (2026-03-08)

## Scope
- Diagnostic-only LQC-style micro probe at `Ω_m = 0.31`
- Script: `notebooks/lqc_boundary_probe.py`
- Cases: 6 (`α_qg in {3e-7, 7e-7, 1.3e-6}` × `rho_crit in {0.41, 1.0}`)
- Receipt: `notebooks/outputs/grqm_lqc_boundary_probe_20260308_150329/lqc_boundary_probe_summary.json`

## Aggregate outcome
- `n_cases = 6`, `n_valid = 6`
- `best_max_ratio = 310.03`
- `worst_max_ratio = 756.4146`
- `any_ratio_below_1 = false`
- `q1_refinement_pass_rate = 1.0`
- `min_of_min_a = 0.1`

## Interpretation
- Under this toy LQC-style suppression implementation and chosen `rho_crit` values, the correction/classical ratio remains far above 1 in all cases.
- Dynamics stayed near the initial boundary (`min_a = 0.1` across cases), indicating this specific parameterization is not yet physically comparable to prior edge-collapse diagnostics.
- Result is still useful: this first-pass LQC parameterization does not produce a clean suppression signal in the current normalization.

## Governance posture
- Diagnostic-only result; no claim promotion.
- No envelope/status changes.
- Core C-WDW-001 and edge caveat posture unchanged.
