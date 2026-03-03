# GR↔QM Cycle-3 Close Note (Concise)

Date: 2026-03-01 (late)

Cycle-3 targeted the Ω_m<=0.300 core corridor and a Q2 method pivot.

## What was executed
- `notebooks/cycle3_core_confirm.py`
- `notebooks/cycle3_q2_pivot.py` (patched for `t_first_1pct=None` handling)

## Key outputs
- `notebooks/outputs/grqm_cycle3_core_confirm_20260301_223742/cycle3_core_confirm_summary.csv`
- `notebooks/outputs/grqm_cycle3_core_confirm_20260301_223742/proxy_agreement_v3.csv`
- `notebooks/outputs/grqm_cycle3_core_confirm_20260301_223742/aggregate.json`
- `notebooks/outputs/grqm_cycle3_q2_pivot_20260301_223823/cycle3_q2_pivot_summary.csv`

## Headline metrics
- Core pass rate: **20/20 (100%)**
- Proxy agreement (core): **Pearson 0.99985, Spearman 1.00000, ratio std 0.0314**
- Q1 hardened sensitivity max: **0.1483** (within 0.18 gate)
- Q1 refinement max: **2.80e-07** (well within 5e-3 gate)
- Q2 robust tails (core batch): **p95 max 0.2850**, **p99 max 0.3892**
- Replication: `q2_true_replication_rel_diff=0.0` for all core runs
- Q2 pivot (DOP853): **6/6 points pass 20% criterion via p95; observed ~99.9999995% p95 reduction**

## Gate snapshot
- G-PROXY: PASS
- G-REFINE: PASS
- G-ROBUST-Q1: PASS
- G-ROBUST-Q2: PASS
- G-REPLICATION: PASS
- G-ENVELOPE: PASS (core corridor)
- G-PROMOTION (provisional): PASS in-core
- G-PROMOTION (full): NOT YET (consecutive-cycle + assumption-closure policy not satisfied)

## Conservative claim posture
Use wording: **"PROVISIONALLY PROVEN in-core (Ω_m<=0.300)"**.
Keep full claim status OPEN until full-promotion criteria are met.
