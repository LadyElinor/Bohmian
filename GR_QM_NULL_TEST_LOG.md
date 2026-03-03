# GR_QM Null-Test Log

Date: 2026-03-02
Scope: Core in-envelope corridor (Ω_m 0.285..0.300; α_qg 3e-7..1.3e-6)

## Null definitions (operational)

### Q1 null (proxy signal)
H0: Semiclassical WDW-inspired correction produces no reproducible proxy deviation beyond numerical/refinement artifact in the declared envelope.

Reject H0 when all are true:
- `q1_delta_proxy_l2` is nontrivial across the grid,
- refinement residual remains small (`q1_refinement_max_obs` below gate),
- effect remains reproducible across confirmation cycles.

### Q2 null (divergence robustness)
H0: Exact-vs-approx divergence does not show reproducible, bounded robust-tail behavior in the declared envelope.

Reject H0 when all are true:
- robust tails satisfy current gates (`q2_D_p95 < 0.5`, `q2_D_p99 < 0.8`),
- true like-vs-like replication is stable (`q2_true_replication_rel_diff <= 1e-6`),
- behavior repeats across consecutive confirmation cycles.

## Consecutive-cycle records

### cycle-3-rerun-20260302
Artifact: `notebooks/outputs/grqm_cycle3_core_confirm_20260302_172931/cycle3_core_confirm_summary.csv`

- Q1 evidence:
  - `q1_delta_proxy_l2`: min 0.005314, max 0.121789
  - `q1_refinement_max_obs`: max 2.795794e-07
  - Verdict: Q1 null rejected in-envelope (signal above numerical artifact floor).
- Q2 evidence:
  - `q2_D_p95`: max 0.284987
  - `q2_D_p99`: max 0.389203
  - `q2_true_replication_rel_diff`: max 0.0
  - Verdict: Q2 null rejected in-envelope (stable, reproducible bounded divergence behavior).

### cycle-4-reverted-hardening-20260302
Artifact: `notebooks/outputs/grqm_cycle3_core_confirm_20260302_215234/cycle3_core_confirm_summary.csv`

- Q1 evidence:
  - `q1_delta_proxy_l2`: min 0.005314, max 0.121789
  - `q1_refinement_max_obs`: max 2.795794e-07
  - Verdict: Q1 null rejected again (same envelope behavior).
- Q2 evidence:
  - `q2_D_p95`: max 0.284987
  - `q2_D_p99`: max 0.389203
  - `q2_true_replication_rel_diff`: max 0.0
  - Verdict: Q2 null rejected again (same envelope behavior).

## Compliance note
These records are intended to explicitly satisfy the gate-policy requirement that proxy claims include declared null tests and pass/reject outcomes across consecutive qualifying cycles.
