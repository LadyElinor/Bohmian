# GR_QM KPI Snapshot — 2026-03-05

## Fresh confirmation run (C-GRQM-001 trigger)
Command:
- `python notebooks/cycle3_core_confirm.py`

Artifact:
- `notebooks/outputs/grqm_cycle3_core_confirm_20260305_171322/`

## Core-envelope summary (20-point corridor)
- points run: `20`
- envelope pass count: `20/20`
- envelope pass rate: `1.0`

### Gate-critical maxima (from `cycle3_core_confirm_summary.csv`)
- `q1_refinement_max_obs_max = 2.795794461483881e-07`
- `q1_assumption_sensitivity_hardened_max = 0.1483037867483375`
- `q2_D_p95_max = 0.2849869470187435`
- `q2_D_p99_max = 0.3892032151943856`
- `q2_true_replication_rel_diff_max = 0.0`

## Interpretation
- Fresh cycle reproduces prior in-core envelope behavior with no drift in policy-critical maxima.
- This satisfies the trigger requirement for an additional confirmation cycle + KPI update for `C-GRQM-001`.
- Governance recommendation unchanged: keep `C-GRQM-001` OPEN pending additional externally reviewable cycle packaging.
