# GR_QM Edge Nonlinear Extension Summary (2026-03-04)

## What changed
1. Added preregistered edge-only nonlinear extension plan:
   - `GR_QM_NONLINEAR_EXTENSION_PLAN_2026-03-04.md`
2. Added additive experiment sweep script (no mutation of core pipeline):
   - `notebooks/edge_nonlinear_extension_sweep.py`
3. Ran controlled edge sweep and produced artifacts:
   - `notebooks/outputs/grqm_edge_nonlinear_extension_20260304_211921/`

## What was tested
Edge grid:
- `Ω_m in {0.305, 0.3075, 0.310}`
- `alpha_qg in {3e-7, 7e-7, 1e-6, 1.3e-6}`

Variants:
- `baseline_n5`: `alpha/a^5`
- `higher_order_n6`: `alpha/a^6`
- `softcap_denom`: `alpha/(a^5 + a_cut^5)`, `a_cut=0.02`
- `tanh_gate`: `(alpha/a^5)*tanh((a/a_cut)^k)`, `a_cut=0.02`, `k=6`

Solver:
- `solve_ivp(method='Radau', rtol=1e-9, atol=1e-11, max_step=1e-3)`

## Key quantitative outcomes
Aggregate (`edge_nonlinear_extension_summary.json`):
- baseline_n5
  - success_rate: `1.0`
  - worst max_ratio: `3.9160`
  - worst min_a: `0.00791`
- higher_order_n6
  - success_rate: `1.0`
  - worst max_ratio: `4.6685`
  - worst min_a: `0.02539`
- softcap_denom
  - success_rate: `0.0` (all failed)
- tanh_gate
  - success_rate: `0.0` (all failed)

Failure attribution captured:
- `edge_nonlinear_extension_failures.log`
- Repeated solver failure message for nonlinear regularizers:
  - `Required step size is less than spacing between numbers.`

## Requested concise table/json outputs
Generated with columns:
- `(omega_m, alpha_qg, min_a, max_ratio, peak_t, solver outcome)`

Files:
- `edge_nonlinear_extension_table.json`
- `edge_nonlinear_extension_sweep.csv`

## Acceptance criteria evaluation (from prereg plan)
Criteria:
- A: `max_ratio <= 0.10`
- B: `min_a >= 0.020`
- C: `solver success rate = 100%`

Results:
- `baseline_n5`: fails A, fails B, passes C
- `higher_order_n6`: fails A, passes B, passes C
- `softcap_denom`: fails A/B/C (C fails via 0% success)
- `tanh_gate`: fails A/B/C (C fails via 0% success)

No candidate achieved all-pass.

## Recommendation
- Keep edge lane `Ω_m >= 0.305` **BLOCKED** (unchanged).
- Do not alter `C-WDW-001` in-core proven envelope.
- Next iteration should use a two-stage protocol:
  1. strict event guard (`stop when a <= a_min_policy`) to avoid singular-collapse segments,
  2. parameter scan over regularizers (`a_cut`, `k`) with explicit solver-family cross-check (Radau + DOP853), retaining the same falsifiable A/B/C gates.
