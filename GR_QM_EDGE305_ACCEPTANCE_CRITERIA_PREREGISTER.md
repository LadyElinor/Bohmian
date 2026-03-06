# GR_QM Edge (Ω_m >= 0.305) Acceptance Criteria — Pre-Registered v1

Status: pre-registered v1 (2026-03-05), not yet executed as promotion evidence.

## Scope
This applies only to edge-lane mitigation attempts at and above `Ω_m = 0.305`.
No impact on current in-core PROVEN status.

## Required run pack
1. Edge grid:
   - `Ω_m in {0.305, 0.3075, 0.310}`
   - declared α corridor consistent with current core lane.
2. dt ladder:
   - at least `{5e-4, 7.5e-4, 1e-3}`
3. method comparators:
   - RK4 + DOP853 mandatory
   - Euler allowed only as stress diagnostic (non-promoting)
4. replication path:
   - true like-vs-like rerun for deterministic check

## Pass conditions (all required)
- `q2_D_p95 <= 0.50`
- `q2_D_p99 <= 0.80`
- `q2_true_replication_rel_diff <= 1e-6`
- no unresolved null-test failure in-edge
- no hard instability requiring ad-hoc exclusions beyond predeclared policy

## Hold / fail conditions
- any gate above fails at any declared edge point
- method disagreement (RK4 vs DOP853) exceeds predeclared tolerance and is not localized/mitigated
- new exclusions introduced post-hoc without prior registration

## Governance rule
Even if technical pass occurs, edge claim remains BLOCKED until:
- evidence is logged in ledger/matrix,
- assumptions impacted are updated,
- explicit governance close is recorded in monthly gate report.

## Sequencing alignment (mandatory)
Execute edge-lane work strictly in this order:
1. `docs/C-WDW-001_CORRECTION_DERIVATION.md` (derivation basis)
2. `GR_QM_CLIFF_MECHANISM_PREDICTIONS_PREREG_2026-03-03.md` (prediction prereg)
3. this acceptance prereg (`GR_QM_EDGE305_ACCEPTANCE_CRITERIA_PREREGISTER.md`)
4. run package (`GR_QM_EDGE_MITIGATION_PACKAGE_PLAN_2026-03-03.md` + script artifacts)
5. apply `GR_QM_CWDW001_FALSIFICATION_PROTOCOL.md`
6. governance close in `GR_QM_MONTHLY_GATE_REPORT_01.md` and `CLAIM_STATUS_MATRIX.md`

No out-of-order edge claim updates are allowed.
