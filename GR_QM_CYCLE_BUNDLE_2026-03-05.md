# GR_QM Cycle Bundle — 2026-03-05

Purpose: externally reviewable compact receipt for the 2026-03-05 confirmation and robustness work.

## Scope
- C-GRQM-001 fresh confirmation cycle
- C-GRQM-002 RK-family robustness mini-pack + independent repeat
- No edge-lane status change in this bundle

## Artifact index

### 1) C-GRQM-001 core confirmation run
- Run command: `python notebooks/cycle3_core_confirm.py`
- Artifact dir: `notebooks/outputs/grqm_cycle3_core_confirm_20260305_171322/`
- Key files:
  - `cycle3_core_confirm_summary.csv`
  - `cycle3_core_confirm_rows.csv`

Key outcomes:
- pass rate: `20/20` (`1.0`)
- `q1_refinement_max_obs_max = 2.795794461483881e-07`
- `q1_assumption_sensitivity_hardened_max = 0.1483037867483375`
- `q2_D_p95_max = 0.2849869470187435`
- `q2_D_p99_max = 0.3892032151943856`
- `q2_true_replication_rel_diff_max = 0.0`

### 2) C-GRQM-002 RK-family mini-pack (run 1)
- Run command: `python notebooks/cgrqm002_rk_family_minipack.py`
- Artifact dir: `notebooks/outputs/grqm_cgrqm002_rk_family_minipack_20260305_171537/`
- Key files:
  - `rk_family_method_rows.csv`
  - `rk_family_point_summary.csv`
  - `summary.json`

### 3) C-GRQM-002 RK-family mini-pack (independent repeat)
- Run command: `python notebooks/cgrqm002_rk_family_minipack.py`
- Artifact dir: `notebooks/outputs/grqm_cgrqm002_rk_family_minipack_20260305_184849/`
- Key files:
  - `rk_family_method_rows.csv`
  - `rk_family_point_summary.csv`
  - `summary.json`

Repeat-level outcomes (decision metrics):
- `all_points_pass = true`
- `global_max_q2_D_p95 = 6.2207088369348185e-09`
- `global_max_q2_D_p99 = 7.576536509290577e-09`
- `global_max_rk_family_abs_spread_p95 = 4.713609946804809e-09`
- `global_max_replication_rel_diff = 0.0`

### 4) C-GRQM-002 dual-receipt consistency audit (new validation)
- Run command: `python notebooks/cgrqm002_dual_receipt_audit.py`
- Artifact dir: `notebooks/outputs/grqm_cgrqm002_dual_receipt_audit_20260305_185746/`
- Key files:
  - `dual_receipt_audit_report.json`
  - `dual_receipt_point_compare.csv`

Audit outcomes:
- `both_runs_acceptance_pass = true`
- `point_pass_identical = true`
- `decision = PASS`

## Decision paragraph
- **C-GRQM-001:** confirmation remains strong and reproducible for current in-core envelope assumptions.
- **C-GRQM-002:** robustness mini-pack acceptance criteria passed, reproduced in an independent same-day repeat, and now independently cross-audited (PASS); evidence quality improved materially.
- **Governance recommendation:** keep `C-GRQM-002` as `OPEN` pending formal governance close / promotion vote timing, but mark readiness as high based on dual receipts + audit.
- **Edge lane (`Ω_m >= 0.305`):** unchanged; remains blocked pending execution under pre-registered acceptance and mandatory falsification/governance sequence.
