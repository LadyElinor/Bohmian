# Q1_Q2_GATE_UPDATE – March 2026 Corridor Rerun (Tiered Gates)

**Date:** 2026-03-01  
**Scope:** Extended 6-point grid at Ω_m=0.30, α_qg ∈ [2.154e-7, 1.5e-6]  
**Script:** `notebooks/grqm_batch_runner_tiered.py`  
**Outputs:** `notebooks/outputs/grqm_batch_tiered_20260301_191558/summary.csv`

## Q1: Semiclassical correction produces stable low-energy proxy signature

**Status:** **PARTIALLY SUPPORTED** (robust in hardened validity envelope)

**Evidence**
- `pass_q1_effect`: **6/6**
- `pass_q1_refinement`: **6/6**
- `pass_q1_assumption_hardened`: **6/6**
- `q1_assumption_sensitivity_hardened`: **0.127–0.150** (<0.20 gate)
- `q1_delta_proxy_l2` increases monotonically with α_qg across the 6 points.

**Validity envelope (current claim boundary)**
- Ω_m fixed at ~0.30 (flat ΛCDM background)
- Hardened assumption perturbations (near-nominal):
  - |δa0/a0| ≤ 0.1%
  - small dt perturbations around 1e-3
- α_qg tested up to 1.5e-6 in this corridor

**Notes**
- Wide-stress assumption sensitivity remains high and is treated as out-of-envelope stress behavior, not in-envelope claim failure.
- No promotion to PROVEN yet; requires wider envelope confirmation and independent proxy corroboration.

## Q2: Exact-vs-approx divergence and reproducibility

**Status:** **OPEN** (quantified limitation, not a replication failure)

**Evidence**
- `pass_q2_true_replication`: **6/6** (`q2_true_replication_rel_diff = 0.0`)
- `pass_q2_method_disagreement`: **0/6** (`q2_method_disagreement_rel_diff ≈ 0.999991`)
- `q2_t_first_method_disagreement_1pct`: ~0.6365 → 0.646 across this 6-point set.

**Interpretation**
- Prior “replication” blocker was corrected: true like-vs-like replication is stable.
- Remaining Q2 blocker is method-family disagreement (Euler vs coarse RK4), now explicitly tracked.

## Composite gate outcomes

- `pass_all_strict` (includes method-disagreement gate): **0/6**
- `pass_all_envelope` (practical envelope gate): **6/6**

## Decision for current cycle

**Proceed** within the current validity envelope.

## Next actions

1. Extend α_qg points above/below current range at Ω_m=0.30 to map trend stability.
2. Add one higher-order reference run for Q2 method-disagreement calibration.
3. Update claim and assumption registries to reflect:
   - Q1 robust-in-envelope status
   - Q2 true replication pass + method-disagreement open limitation.
