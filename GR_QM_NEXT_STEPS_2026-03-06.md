# GR_QM Next Steps — 2026-03-06

## Goal
Advance the project autonomously while preserving governance constraints:
- keep edge lane (`Ω_m >= 0.305`) blocked until preregistered criteria are passed and governance-closed,
- generate externally reviewable receipts,
- prepare a clean decision packet for the next gate call.

## Next 3 runs (in order)

### Run 1 — Edge mitigation micro-package (primary)
- Command: `python notebooks/edge_mitigation_micro_package.py`
- Purpose: execute the smallest preregistered mitigation package for edge lane diagnostics.
- Expected artifact folder:
  - `notebooks/outputs/grqm_edge_mitigation_micro_<timestamp>/`
- Expected key files:
  - `edge_mitigation_micro_summary.csv`
  - `edge_mitigation_micro_rows.csv` (if emitted)
  - `aggregate.json` (if emitted)
- Primary checks:
  - q2_D_p95 and q2_D_p99 behavior across `{0.305, 0.3075, 0.31}`
  - q1_refine, q1_assumption_sensitivity_hardened companion gates

### Run 2 — Edge integrator hierarchy scan (method-risk cross-check)
- Command: `python notebooks/edge_integrator_hierarchy_scan.py`
- Purpose: quantify solver-family agreement/disagreement at edge points.
- Expected artifact folder:
  - `notebooks/outputs/grqm_edge_integrator_hierarchy_<timestamp>/`
- Expected key files:
  - `edge_integrator_hierarchy_summary.json`
  - method-level comparison CSV/rows (if emitted)
- Primary checks:
  - RK4 vs DOP853 consistency windows
  - instability localization vs broad failure pattern

### Run 3 — Edge companion full packet (decision-ready bundle)
- Command: `python notebooks/edge_companion_full_packet.py`
- Purpose: produce decision-friendly combined packet for prereg + falsification handoff.
- Expected artifact folder:
  - `notebooks/outputs/grqm_edge_companion_full_<timestamp>/`
- Expected key files:
  - packet summary JSON/CSV
  - any linked diagnostic tables for governance notes

## Immediate outputs to generate after runs
1. `Physics/GR_QM_EDGE_PACKAGE_NOTE_2026-03-06.md`
   - concise results summary, pass/fail per prereg gate, caveats.
2. Addendum in `Physics/GR_QM_MONTHLY_GATE_REPORT_01.md`
   - edge-lane diagnostic addendum only (no status mutation unless criteria clearly met).
3. Optional matrix update in `Physics/CLAIM_STATUS_MATRIX.md`
   - only if governance-ready evidence justifies a status discussion.

## Guardrails (must keep)
- No out-of-order edge claim updates.
- No silent post-hoc exclusions.
- Keep nonlinear/BoO branches diagnostic-only unless separately promoted.
