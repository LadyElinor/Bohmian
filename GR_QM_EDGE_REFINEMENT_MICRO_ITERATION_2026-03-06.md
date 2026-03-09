# GR_QM Edge Refinement Micro-Iteration — 2026-03-06

## Objective
Target the isolated blocker (`q1_refinement`) on failing edge points without rerunning the full packet.

## Command
- `python -c "... import edge_companion_full_packet as e; ... q1_refine(..., dt_main=2e-4) ..."`

## Target points
- `(Ω_m, α_qg) = (0.3075, 7e-7)`
- `(Ω_m, α_qg) = (0.3075, 1e-6)`
- `(Ω_m, α_qg) = (0.31, 7e-7)`
- `(Ω_m, α_qg) = (0.31, 1e-6)`

## Results
- `max_q1_refine_dt2e4 = 1.6696329959586506e-05`
- per-point `q1_refine_dt2e4`:
  - 0.3075,7e-7: `8.07241935176775e-06`
  - 0.3075,1e-6: `8.07241935176775e-06`
  - 0.31,7e-7: `1.6696329959586506e-05`
  - 0.31,1e-6: `1.6696329959586506e-05`
- pass rate vs threshold `1e-6`: `0.0`

## Interpretation
- This micro-iteration improves refinement error by roughly an order of magnitude vs prior full-packet max (`1.063e-4 -> 1.67e-5`), but still fails the hard threshold (`1e-6`).
- Blocker remains refinement-specific and concentrated at edge points.

## Follow-up adaptive refinement (same session)
- Script: `notebooks/edge_refinement_adaptive_micro.py`
- Output: `notebooks/outputs/grqm_edge_refinement_adaptive_20260306_221856/`
- Aggregate:
  - `max_q1_refine = 2.0774125296475853e-07`
  - threshold `= 1e-6`
  - pass rate `= 1.0 (4/4)`

## Updated interpretation
- Targeted adaptive/dense refinement closes the q1 refinement blocker for the tested failing edge points.
- This converts the prior partial-improvement result into a local pass for the micro target set.
- Next step: fold this refinement mode into the companion packet path (or run a mini companion replay on same points) before governance disposition.
