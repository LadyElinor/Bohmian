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

## Notes
- Pass rates are computed directly from each cycle artifact CSV.
- Where a pass flag was absent, documented gate thresholds from current plan/scripts were applied deterministically.
- Promotion eligibility is conservative: consecutive all-gate cycles in same envelope + no unresolved high-impact assumptions.