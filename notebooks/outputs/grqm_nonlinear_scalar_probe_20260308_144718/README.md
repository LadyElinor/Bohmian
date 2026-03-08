# Golden Diagnostic Receipt — Nonlinear Scalar Quick Probe (2026-03-08)

This folder is the canonical receipt for the nonlinear scalar boundary probe at `Ω_m = 0.31`.

## Provenance
- Script: `notebooks/nonlinear_scalar_boundary_probe.py`
- Aggregate: `nonlinear_scalar_probe_summary.json`

## Sweep definition
- `λ in {0, 1e-5, 1e-4, 1e-3}`
- `α_qg in {3e-7, 7e-7, 1.3e-6}`
- Total cases: `12`

## Aggregate snapshot
- `n_valid = 12`
- `best_max_ratio = 3.795233992964208`
- `any_ratio_below_1 = false`
- `best_q1_refinement_proxy = 6.325536279551366e-07`

## Interpretation
- The tested nonlinear term does not restore perturbative behavior at the boundary (`correction/classical` remains `> 1` in all sampled cases).
- This is a useful negative diagnostic result and narrows subsequent model-search directions.

## Governance posture
- Diagnostic-only lane; no claim-status mutation.
- Core claim scope unchanged.
- Edge physical caveat remains mandatory.
