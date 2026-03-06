# C-GRQM-002 Governance Decision Package — 2026-03-05

## Purpose
Governance-close-ready packet for claim `C-GRQM-002` using existing dual RK-family mini-pack receipts and one independent cross-receipt audit.

## Claim in scope
`C-GRQM-002`: Exact-vs-approx divergence can provide robust test signal in this toy setting.

Status entering this package: **OPEN**.

## Decision evidence (receipts)
Primary receipts:
- `notebooks/outputs/grqm_cgrqm002_rk_family_minipack_20260305_171537/summary.json`
- `notebooks/outputs/grqm_cgrqm002_rk_family_minipack_20260305_184849/summary.json`

Validation receipt (new high-leverage check):
- `notebooks/outputs/grqm_cgrqm002_dual_receipt_audit_20260305_185746/dual_receipt_audit_report.json`
- `notebooks/outputs/grqm_cgrqm002_dual_receipt_audit_20260305_185746/dual_receipt_point_compare.csv`

Context bundle:
- `GR_QM_CGRQM002_RK_FAMILY_MINIPACK_NOTE_2026-03-05.md`
- `GR_QM_CYCLE_BUNDLE_2026-03-05.md`

## Predeclared acceptance criteria
Mini-pack acceptance criteria (from predeclared note):
1. `max_q2_D_p95 <= 0.50`
2. `max_q2_D_p99 <= 0.80`
3. `rk_family_abs_spread_p95 <= 1e-8`
4. `q2_true_replication_rel_diff <= 1e-6`
5. No solver failures in declared methods.

## Measured results (run-level)
Both receipts report:
- `n_points = 6`
- `all_points_pass = true`
- `global_max_q2_D_p95 = 6.2207088369348185e-09`
- `global_max_q2_D_p99 = 7.576536509290577e-09`
- `global_max_rk_family_abs_spread_p95 = 4.713609946804809e-09`
- `global_max_replication_rel_diff = 0.0`

## Independent consistency audit result
`cgrqm002_dual_receipt_audit.py` compared both receipts at run-level and point-level.

Audit verdict:
- `both_runs_acceptance_pass = true`
- `point_pass_identical = true`
- `decision = PASS`
- max absolute cross-run metric deltas: all zero at reported precision.

## Risk and scope posture
- Evidence supports promotion readiness **in-core** for this toy setting.
- No edge-lane implication in this package.
- `Ω_m >= 0.305` remains blocked and unchanged.

## Governance decision options
1. **Option A — Promote now (in-core only):**
   - Move `C-GRQM-002` from OPEN -> PROVEN (scope-limited to in-core envelope and current protocol).
   - Keep edge lane blocked.
2. **Option B — Conditional hold (conservative):**
   - Keep `C-GRQM-002` OPEN.
   - Require one additional independent-cycle receipt before promotion vote.

## Recommended option
**Option A selected by governance (2026-03-05)** — promote now, in-core only.

## Governance execution receipt
Executed actions:
1. Recorded option choice and status transition in `CLAIM_STATUS_MATRIX.md`.
2. Issued closure note with scope caveat: `GR_QM_CGRQM002_CLOSURE_NOTE_2026-03-05.md`.
3. Updated monthly report + promotion ledger to reflect close decision.
