# GR_QM Nonlinear Scalar Quick Probe Note (2026-03-08)

## Scope
- Boundary-focused diagnostic at `Ω_m = 0.31`
- Sweep grid:
  - `λ in {0, 1e-5, 1e-4, 1e-3}`
  - `α_qg in {3e-7, 7e-7, 1.3e-6}`
- Script: `notebooks/nonlinear_scalar_boundary_probe.py`
- Receipt: `notebooks/outputs/grqm_nonlinear_scalar_probe_20260308_144718/nonlinear_scalar_probe_summary.json`

## Aggregate outcome
- `n_cases = 12` (all valid)
- `best_max_ratio = 3.795233992964208`
- `any_ratio_below_1 = false`
- `best_q1_refinement_proxy = 6.325536279551366e-07`

## Interpretation
- In this toy λ-sweep, simple quartic-style nonlinear damping at tested scales does **not** suppress transient correction/classical dominance below 1.
- Non-perturbative transient behavior remains present across all sampled cases at `Ω_m = 0.31`.
- Numerical refinement proxy remains strong (best observed below `1e-6`), but physical caveat is unchanged.

## Governance posture
- Diagnostic-only result; no claim promotion.
- Core envelope status unchanged.
- Edge lane caveat remains mandatory for physical interpretation.
