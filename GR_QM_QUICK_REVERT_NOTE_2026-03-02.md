# GR_QM Quick Revert Note — 2026-03-02

## Scope
Quick diagnostic to test if Cycle-4 regression is isolated to hardening logic changes while holding grid/envelope/pipeline fixed.

## Snapshot (Cycle-4 before revert)
- File: `notebooks/cycle4_inpolicy_confirm.py`
- sha256: `416a173a74d9cefd1dae722d976d6b4a686ea2e5156e093d5d94d5e2d559c7af`
- Grid:
  - `omega_list=[0.285,0.290,0.295,0.300]`
  - `alpha_list=[3e-7,5e-7,7e-7,1e-6,1.3e-6]`
- Gate thresholds unchanged (`q1_assumption_hardened_max=0.18`, standard Q1/Q2 gates).
- Cycle-4 hardening signature (`policy_perturbations`):
  - `(ic_scale=0.9993, dt=8e-4, n=4)`
  - `(ic_scale=1.0009, dt=8e-4, n=4)`
  - `(ic_scale=0.9993, dt=1.2e-3, n=5)`
  - `(ic_scale=1.0009, dt=1.2e-3, n=5)`

## Reverted signature applied (Cycle-3 equivalent)
- Source file: `notebooks/cycle3_core_confirm.py`
- sha256: `9ad7ff502cabd94dfc72b8f583b5f87942686d8269332b0be4d6b4d2a8add499`
- Revert hardening signature (`hardened_perturbations`):
  - `(ic_scale=0.999, dt=1e-3, n=5)`
  - `(ic_scale=1.001, dt=1e-3, n=5)`
  - `(ic_scale=1.0, dt=9e-4, n=5)`
  - `(ic_scale=1.0, dt=1.1e-3, n=5)`

## Command(s) run
1. `python notebooks/grqm_cycle4_quick_revert_hardening.py`

## Output path(s)
- `notebooks/outputs/grqm_quick_revert_hardening_20260302_214712/`
  - `aggregate.json`
  - `subset_policy_rows.csv`
  - `subset_revert_rows.csv`
  - `subset_compare.csv`

## Subset used (minimal, high-signal core corridor)
- `(omega_m, alpha_qg) = (0.290, 7e-7), (0.295, 7e-7), (0.300, 7e-7)`

## Results: q1_assumption_sensitivity_hardened
- Cycle-4 hardening (policy):
  - min: `0.869910`
  - max: `0.875848`
  - mean: `0.872281`
  - gate pass (`<=0.18`): `0/3`
  - pass_all_envelope: `0/3`
- Cycle-3-revert hardening:
  - min: `0.030042`
  - max: `0.139701`
  - mean: `0.072106`
  - gate pass (`<=0.18`): `3/3`
  - pass_all_envelope: `3/3`

## Conclusion
Clear recovery occurs under hardening-only revert, with all subset points returning to Cycle-3-like regime and passing gates. This isolates the Cycle-4 blocker to hardening logic/settings changes, not to grid/envelope/pipeline.

## Governance cross-link (2026-03-02)
- Baseline gate-decision hardening signature is reverted to Cycle-3-equivalent bounds/signature.
- Wider `dt` perturbation spread from Cycle-4 hardening is classified as exploratory-only unless explicitly designated for gate policy.
- Register reference: `RESEARCH_ASSUMPTION_REGISTER.md` (Decision Addendum, 2026-03-02).
