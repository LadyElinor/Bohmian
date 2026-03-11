# GR_QM Edge Mitigation Micro-Package Plan — 2026-03-03

## Objective
Run the smallest predeclared package that can separate numerical-path artifact from potential physical breakdown at the edge (`Ω_m >= 0.305`) without changing governance policy.

## Planned run
- Script: `notebooks/edge_mitigation_micro_package.py`
- Grid: `Ω_m in {0.305, 0.3075, 0.31}` and `α_qg in {3e-7, 5e-7, 7e-7, 1e-6, 1.3e-6}`
- Solvers:
  - primary reference: DOP853 (`rtol=1e-12`, `atol=1e-14`)
  - comparators: DOP853/LSODA/Radau (`rtol=1e-10`, `atol=1e-12`)

## Pass targets (for mitigation evidence package)
- `q2_D_p95 < 0.01`
- `q2_D_p99 < 0.05`
- companion checks required in same package:
  - `q1_refine < 1e-6`
  - `q1_assumption_sensitivity_hardened <= 0.18`

## Governance handling
- Passing package can support **exploratory** edge inclusion request only.
- No automatic claim promotion or envelope lift.
- Final disposition requires explicit monthly-gate governance close.
