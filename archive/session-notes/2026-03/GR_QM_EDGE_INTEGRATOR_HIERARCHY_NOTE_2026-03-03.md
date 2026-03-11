# GR_QM Edge Integrator Hierarchy Note — 2026-03-03

## Run executed
Command:
- `python notebooks/edge_integrator_hierarchy_scan.py`

Outputs:
- `notebooks/outputs/grqm_edge_integrator_hierarchy_20260303_213438/edge_integrator_hierarchy.csv`
- `notebooks/outputs/grqm_edge_integrator_hierarchy_20260303_213438/edge_integrator_suppression.csv`
- `notebooks/outputs/grqm_edge_integrator_hierarchy_20260303_213438/edge_integrator_hierarchy_summary.json`

## Scope
- Points: `(Ω_m, α_qg) in {(0.305,3e-7), (0.305,7e-7), (0.305,1.3e-6)}`
- Comparators: `RK4 fixed dt=1e-3` vs `DOP853`, `LSODA`, `Radau`
- Adaptive refs: DOP853 (`rtol=1e-11`, `atol=1e-13`) on shared nominal evaluation grid

## Key results
- RK4 edge q2_p95 by point: `0.3678`, `0.2801`, `0.0470`
- Tight adaptive q2_p95 are near numerical floor:
  - DOP853 (`1e-10/1e-12`): `~1e-9`
  - LSODA (`1e-10/1e-12`): `~1e-8`
  - Radau (`1e-10/1e-12`): `~1e-10`
- Suppression vs RK4 q2_p95 (tight tolerance):
  - DOP853: `0.99999998 .. 0.999999997`
  - LSODA: `0.99999977 .. 0.99999997`
  - Radau: `0.999999997 .. 0.9999999997`

## Conservative interpretation
- On this narrow edge subset, >99.9999% of RK4-vs-reference spread is suppressed by higher-order/adaptive/stiff-capable integrators.
- This supports the hypothesis that a major component of observed edge blow-up in prior dense packs is numerical-path dominated.
- This does **not** unblock edge claims yet. It motivates a policy-consistent edge mitigation package with predeclared gates before any status change.
