# GR_QM Edge Package Note — 2026-03-06 (Autonomous run log)

## Status
- Run 1 complete: edge mitigation micro-package
- Run 2 complete: edge integrator hierarchy scan
- Run 3 launched: edge companion full packet (in progress at note creation)

## Run 1 receipt
- Command: `python notebooks/edge_mitigation_micro_package.py`
- Artifact: `notebooks/outputs/grqm_edge_mitigation_micro_20260306_211144/`
- Files:
  - `edge_mitigation_micro_summary.csv`
  - `edge_mitigation_policy.json`

### Key findings (q2 diagnostics)
Across edge points `Ω_m in {0.305, 0.3075, 0.31}` and tested `α_qg` set:
- Observed `q2_D_p95` values are O(1e-9 to 1e-8), far below prereg hold threshold 0.50 and micro-package target 0.01.
- Observed `q2_D_p99` values are O(1e-9 to 1e-7), far below prereg hold threshold 0.80 and micro-package target 0.05.

### Important caveat
Per `edge_mitigation_policy.json`, this script only computes q2-style method diagnostics.
Companion q1/hardening checks are required from separate run artifacts before any edge-lane pass/fail determination.

## Run 2 receipt
- Command: `python notebooks/edge_integrator_hierarchy_scan.py`
- Artifact: `notebooks/outputs/grqm_edge_integrator_hierarchy_20260306_211213/`
- File:
  - `edge_integrator_hierarchy_summary.json`

### Key findings (method-risk diagnostic)
- `suppression_vs_rk4_p95` is extremely high for DOP853/LSODA/Radau against RK4 baseline:
  - min suppression by method: DOP853 `0.9999999776`, LSODA `0.9999997695`, Radau `0.9999999974`
  - max suppression by method near 1.0
- This strongly indicates edge spikes in this diagnostic lane are predominantly numerical-path effects under the scanned setup.

## Governance posture (unchanged)
- Edge lane (`Ω_m >= 0.305`) remains BLOCKED pending full prereg sequence completion:
  1) complete companion packet,
  2) apply falsification protocol,
  3) record governance close.
- No claim status changed in this note.
