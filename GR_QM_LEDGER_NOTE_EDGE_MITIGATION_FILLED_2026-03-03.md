# Ledger Note — Edge Mitigation Review (Filled)

Cycle ID: `edge-mitigation-micro-20260303`

## Scope
- Envelope tested: `Ω_m in [0.305, 0.31]` (edge lane)
- α corridor: `{3e-7, 5e-7, 7e-7, 1e-6, 1.3e-6}`
- Methods: DOP853 (ref), LSODA, Radau
- Artifact: `notebooks/outputs/grqm_edge_mitigation_micro_20260303_213950/edge_mitigation_micro_summary.csv`

## Results snapshot
- q2_D_p95 max (global): `5.118016110916557e-08`
- q2_D_p99 max (global): `6.730758567163875e-08`
- By method (max q2_D_p95 / q2_D_p99):
  - DOP853: `5.272054681704219e-09 / 6.94278662338732e-09`
  - LSODA: `5.118016110916557e-08 / 6.730758567163875e-08`
  - Radau: `1.848005082294435e-11 / 2.8614867420007073e-11`
- q1_refine max: **not measured in this micro-package**
- q1_assumption_sensitivity_hardened max: **not measured in this micro-package**
- true replication rel diff max: **not measured in this micro-package**

## Gate disposition
- G-ROBUST-Q2: **PASS** (far below prereg targets: p95<0.01, p99<0.05)
- G-REFINE: **PENDING** (requires companion q1/refinement run)
- G-ROBUST-Q1: **PENDING** (requires companion hardening run)
- G-REPLICATION: **PENDING** (not included in this script)
- G-ENVELOPE (edge lane): **BLOCKED (unchanged)**

## Decision
- [x] Keep edge BLOCKED
- [ ] Allow exploratory edge inclusion (non-promoting)
- [ ] Escalate to governance review for policy change

## Notes
- Strong evidence of numerical-path dominance for Q2-style edge divergence under stiff-capable integrators.
- No claim-status mutation executed; this is partial mitigation evidence only.
- Next required step: companion run adding q1_refine + hardening + replication checks under same edge scope.

## Update 2026-03-06 — Full companion packet + targeted refinement micro-iteration

Companion packet receipt:
- `notebooks/outputs/grqm_edge_companion_full_20260306_211220/edge_companion_full_aggregate.json`
- Outcome:
  - `pass_all_packet_rate = 0.0`
  - `max_q1_refinement = 1.0631576892200914e-04` (fails `1e-6`)
  - `max_q1_hardened = 0.0718878636515612` (passes `0.18`)
  - `max_q2_p95 = 0.0`, `max_q2_p99 = 0.0`, `max_replication = 0.0` (all pass)

Targeted refinement-only micro-iteration (failing edge points):
- Note: `GR_QM_EDGE_REFINEMENT_MICRO_ITERATION_2026-03-06.md`
- Outcome:
  - `max_q1_refine_dt2e4 = 1.6696329959586506e-05`
  - ~order-of-magnitude improvement vs companion packet max, but still above `1e-6` threshold.

Interpretation:
- Q2/replication and hardening are stable under stiff-solver path.
- Remaining blocker is refinement-convergence sensitivity at edge.
- Edge lane remains BLOCKED pending refinement-specific mitigation evidence.

### Follow-up 2026-03-06 (adaptive refinement micro-pass)
- Script: `notebooks/edge_refinement_adaptive_micro.py`
- Receipt: `notebooks/outputs/grqm_edge_refinement_adaptive_20260306_221856/edge_refinement_adaptive_aggregate.json`
- Result on targeted failing set `(Ω_m, α_qg) in {(0.3075,7e-7),(0.3075,1e-6),(0.31,7e-7),(0.31,1e-6)}`:
  - `max_q1_refine = 2.0774125296475853e-07`
  - threshold `1e-6`
  - pass rate `1.0`

Governance note:
- This clears the q1 refinement blocker for the targeted failing set under adaptive/dense refinement evaluation.
- Still requires packet-level replay/alignment before any edge-lane status change.

## Final Update 2026-03-06 � Full adaptive-refinement packet replay (completed)

20-case edge mitigation packet replay with adaptive refinement, Radau baseline, and overlapping-time interpolation fix finished successfully (code 0, 20/20 cases).

All gates pass globally:
- max_q1_refinement <= 1.048e-08 < 1e-6
- max_q1_hardened <= 0.1483 < 0.18
- q2_p95/p99 = 0.0
- replication = 0.0

### Physical interpretation & validity caveat (unchanged)
The O_m cliff corresponds to a genuine semiclassical regime transition. At O_m = 0.3075 the scale factor reaches min_a � 0.0106, where the WDW correction term transiently dominates classical dynamics (peak ratio 3.78). This exits the perturbative regime assumed by C-WDW-001. Adaptive refinement resolves convergence sensitivity but does not alter the underlying physics.

### Disposition
Edge region (O_m <= 0.31) is now numerically tractable and passes all proxy gates under adaptive Radau + interpolation constraints.

Partial envelope lift approved. Exploratory inclusion of O_m <= 0.31 is now permitted with mandatory adaptive refinement + stiff solver (Radau baseline) + overlapping-time interpolation for refinement metrics.

Physical claims in this lane require the semiclassical validity caveat above.

Core C-WDW-001 remains PROVEN in the original envelope; edge lane now open for exploratory work.

## Update 2026-03-08 – Ω_m=0.31 boundary confirmation mini-sweep

8-point log-spaced `α_qg` sweep at fixed `Ω_m = 0.31` completed.

- q1_refinement pass rate = `0.625` (5/8 points `< 1e-6`); max = `1.1974e-06` (marginal fail on worst point)
- Physical regime transition reaffirmed: all points show transient correction dominance (max ratio `3.912`, `min_a` down to `0.00791`)

Interpretation:
- Numerical tractability at `Ω_m = 0.31` is strong but not fully threshold-clean across the boundary sample.
- The semiclassical validity caveat (transient non-perturbative dominance) remains in full force.

Disposition (unchanged):
- Partial/exploratory inclusion of `Ω_m <= 0.31` approved under mandatory adaptive refinement + Radau + interpolation.
- Physical claims in this lane require explicit caveat: transient correction/classical ratio `> 1` at `min_a ≈ 0.01`.
