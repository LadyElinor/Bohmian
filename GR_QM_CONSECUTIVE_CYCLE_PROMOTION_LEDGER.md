# GR_QM Consecutive-Cycle Promotion Ledger (Canonical)

Updated from auditable artifacts only. Unknowns are marked explicitly.

| cycle_id | envelope scope | G-PROXY | G-REFINE | G-ROBUST-Q1 | G-ROBUST-Q2 | G-REPLICATION | G-ENVELOPE | unresolved high-impact assumptions | promotion eligible | blocker notes |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| cycle-1 | Omega_m≈0.300 corridor; alpha 2.154e-7..1.5e-6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | A-001|A-002 | NO | Q2 method-disagreement gate failed (0/6); assumption closure pending |
| cycle-2 | Omega_m 0.280..0.310 dense follow-up; alpha 3e-7..1.3e-6 | 100.0% | 71.4% | 77.1% | 91.4% | 100.0% | 71.4% | A-001|A-002 | NO | Envelope pass 25/35; not all-gate consecutive in same envelope |
| cycle-3 | Omega_m 0.285..0.300 core corridor; alpha 3e-7..1.3e-6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | A-001|A-002 | NO | Consecutive-cycle rule unmet due cycle-2 envelope miss and unresolved assumptions |
| cycle-3-rerun-20260302 | Omega_m 0.285..0.300 core corridor; alpha 3e-7..1.3e-6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | A-001|A-002 | NO | Reproducibility strong; still not promotable without A-001/A-002 closure |
| cycle-3-a001-policy-20260302 | A-001 local policy battery over prior closure points (Omega_m 0.295/0.300; alpha 5e-7/1e-6; n in {4,5}; dt 8e-4..1.2e-3) | 100.0% | 100.0% | NA | 100.0% | 100.0% | NA |  | NO | A-001 bounded closure demonstrated in-policy; promotion still blocked by consecutive-cycle envelope rule only |
| cycle-4-inpolicy-20260302 | Omega_m 0.285..0.300 core corridor; alpha 3e-7..1.3e-6; explicit A-001/A-002 policy perturbations | 100.0% | 100.0% | 0.0% | 100.0% | 100.0% | 0.0% |  | NO | G-ROBUST-Q1 failed under explicit in-policy perturbation mix (20/20 over threshold) |
| cycle-4-reverted-hardening-20260302 | Omega_m 0.285..0.300 core corridor; alpha 3e-7..1.3e-6; reverted Cycle-3-equivalent hardening signature | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |  | YES | Governance hold resolved on 2026-03-02: promotion decision executed in CLAIM_STATUS_MATRIX.md. Eligibility upgraded to YES for core-envelope Q1 claim; edge expansion remains blocked at Ω_m>=0.305 |
| governance-close-cgrqm002-20260305 | C-GRQM-002 in-core toy corridor; RK-family mini-pack dual receipt + audit | 100.0% | NA | NA | 100.0% | 100.0% | 100.0% |  | YES | Option A selected on 2026-03-05: C-GRQM-002 promoted OPEN→PROVEN (in-core only). Edge lane Ω_m>=0.305 remains blocked. |
| shoulder-causality-20260323 | Omega_m 0.305..0.317 shoulder causality attribution packet (alpha_qg + Bohmian-Q) | NA | NA | 63.6% (invariance) | NA | NA | NA |  | NO | Attribution result: Intrinsic (0.81), shoulder ~0.3070, form-shift delta 0.0000. Non-promoting diagnostic lane; methods-note prioritized. |

## Notes
- Pass rates are computed directly from each cycle artifact CSV.
- Where a pass flag was absent, documented gate thresholds from current plan/scripts were applied deterministically.
- Promotion eligibility is conservative: consecutive all-gate cycles in same envelope + no unresolved high-impact assumptions.

## Addendum (2026-03-11, SN diagnostics lane)

`t_max` extension packet receipt:
- `notebooks/outputs/sn_diagnostic_lane_20260311_091839/run_receipt.json`
- summary: `.../stage1_tmax_extension_summary.csv`
- continuation note: `GR_QM_SN_SWEEP_NOTE_2026-03-11.md`

Status-normalized snapshot (stage-1 only, `kappa=1e-3`, `C={0,0.01,0.05}`, `t_max in {20,30}`):
- `q1_signal` max `0.06457` vs detect `>0.05` → **WATCH/PARTIAL PASS** (`3/6` rows)
- `q1_refinement_proxy` max `1.29e-6` vs `<1e-6` → **WATCH** (`4/6` rows pass)
- `norm_drift` max `3.00e-4` vs strict `<1e-10` / practical `<1e-5` → **FAIL**
- `loc_sigma_ratio` range `[1.072,1.468]` vs expected `1.00–1.05` → **FAIL**
- `ipr_delta` range `[-1.68e-2,-3.66e-3]` (negative-shift sanity) → **PASS**

Overall verdict: detection crossed in exploratory numerics, but governance-quality stability failed; claim status unchanged (diagnostic only, not publishable evidence).

Next trigger: controlled stronger-`kappa` probe (`kappa in {3e-3,1e-2}`) with tighter numerics and bounded sweep size.