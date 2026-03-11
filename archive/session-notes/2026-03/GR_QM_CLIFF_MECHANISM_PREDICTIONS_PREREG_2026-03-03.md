# GR_QM Cliff Mechanism Predictions (Pre-Registered) — 2026-03-03

Purpose: satisfy sequencing rule (derivation -> prediction -> diagnostic).

## Candidate mechanisms to test
1. **Method-path amplification hypothesis**
   - Prediction: low-order/stress paths show apparent cliff signatures much earlier/larger than RK-family high-order paths.
   - Observable: large separation in edge diagnostics between Euler-including packs and RK4/DOP853-controlled packs.

2. **Local stiffness transition hypothesis near Ω_m≈0.305**
   - Prediction: error/statistics jump sharply at edge while remaining low in-core, with potential spike-channel activation.
   - Observable: q1 refinement and q2 p95/p99 exhibit order-of-magnitude jump across 0.300 -> 0.305.

2b. **Integrator-dominance discriminator (explicit)**
   - Prediction: if high-order/adaptive/stiff-capable solvers suppress edge spread by >=90-95% vs RK4 baseline (q2_p95 basis), dominant contribution is numerical-path/truncation.
   - If suppression remains weak, prioritize model-mechanism breakdown analysis.

3. **Non-penetration hypothesis (core robustness remains isolated)**
   - Prediction: in-core corridor remains stable under same policy; edge instability does not back-propagate into current core envelope metrics.
   - Observable: fresh in-core pass-all remains 20/20 while edge remains blocked.

## Falsification link
Apply `GR_QM_CWDW001_FALSIFICATION_PROTOCOL.md` after diagnostic runs.

## Initial evidence snapshot (non-final)
- `notebooks/outputs/grqm_cliff_prediagnostic_20260303/cliff_prediagnostic_metrics.json`
- Integrator hierarchy micro-check receipt:
  - `GR_QM_EDGE_INTEGRATOR_HIERARCHY_NOTE_2026-03-03.md`
  - `notebooks/outputs/grqm_edge_integrator_hierarchy_20260303_213438/edge_integrator_hierarchy_summary.json`
- Observed clue: on the tested 3-point edge subset, adaptive/stiff-capable methods suppress RK4 edge spread by >99.9999% (q2_p95 basis).
- This snapshot is preparatory and does not alter claim states.
