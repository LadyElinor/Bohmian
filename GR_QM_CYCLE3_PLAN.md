# GR↔QM Cycle-3 Plan

Goal: Confirm core corridor (Ω_m ≤ 0.300), reduce Q2 method sensitivity via pivot, attempt first PROVEN claim  
Cycle duration target: 3–7 days  
Start date: 2026-03-02 (or next available)  
Canonical artifact runner: `notebooks/grqm_batch_runner_tiered.py` (patched with robust Q2)

## Target Gates & Promotion Criteria

- G-PROXY, G-REFINE, G-ROBUST-Q1, G-REPLICATION, G-ENVELOPE: ≥90% pass rate in core corridor
- G-ROBUST-Q2: bulk p95 <0.5 (or ≥20% relative improvement vs Cycle-2 baseline)
- G-PROMOTION (full):
  - 3 consecutive cycles passing all gates in same envelope
  - No unresolved high-impact ACTIVE assumptions
  - Independent proxy corroboration: Spearman ≥0.995 AND ratio std ≤0.15
- G-PROMOTION (provisional fallback): Spearman >0.99 AND ratio std <0.25 → "PROVISIONALLY PROVEN in-core"

## Actions (Sequential)

1. Core Corridor Confirmation Run
- Ω_m = [0.285, 0.290, 0.295, 0.300]
- α_qg = [3e-7, 5e-7, 7e-7, 1e-6, 1.3e-6]
- ~20 runs total
- Include independent proxy on all points
- dt ≤2.5e-4 or RK family for approx
- Exit: ≥90% pass_all_envelope; hardened sensitivity ≤0.18

2. Q2 Method Pivot
- Select 6–8 points from step 1 (highest/lowest α at Ω_m=0.295/0.300)
- Test alternative approx family: DOP853 (higher-order adaptive)
- Metrics: new t_first_1pct, robust divergence (p95, trimmed mean)
- Success: ≥20% relative improvement in p95 and/or later t_first_1pct vs Cycle-2 baseline
- If achieved → adopt as default for future runs

3. Independent Proxy Strengthening & Promotion Draft
- Compute full agreement stats on step-1 data
- If needed, add 2–4 runs with proxy variant
- Draft PROVEN / PROVISIONALLY PROVEN wording if gates met
- Update `CLAIM_STATUS_MATRIX.md` & monthly draft

## Deliverables

- `cycle3_core_confirm_summary.csv`
- `cycle3_q2_pivot_summary.csv`
- `proxy_agreement_v3.csv`
- Updated `CLAIM_STATUS_MATRIX.md`, `RESEARCH_ASSUMPTION_REGISTER.md`
- Cycle-3 close note (½ page)

## Exit Decisions

- Success: ≥90% pass + Q2 pivot ≥20% improvement + strong corroboration → PROVEN / PROVISIONALLY PROVEN
- Partial: 70–90% pass → OPEN with refined envelope; Cycle-4
- Failure: <70% or new pathology → BLOCK in current envelope; Pause & rebuild

Bottom line: confirm, pivot lightly, promote if criteria met — keep conservative and envelope-tight.
