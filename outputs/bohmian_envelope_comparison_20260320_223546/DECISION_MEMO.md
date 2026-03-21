# Decision Memo — Bohmian Envelope Comparison

- **Timestamp:** 2026-03-21 19:26 EDT
- **Artifact Directory:** `C:\Users\arren\.openclaw\workspace\repos\GRQM\outputs\bohmian_envelope_comparison_20260320_223546`
- **Recommendation:** **HOLD_FOUNDATION**
- **Decision Status:** **Do not advance Bohmian-Q widening claim from this run**

---

## 1) Executive Summary
This run does **not** support the hypothesis that Bohmian-Q widens the envelope near \(\Omega_m \approx 0.30\). The observed width is dramatically smaller than `alpha_qg` by the current width metric, and overall instability is high.

---

## 2) Core Evidence (Pass/Fail + Stability)
- **Total cases:** 540
- **Failed cases:** 242
- **Passed cases:** 298
- **Unstable rate:** 0.4481 (44.81%)

Interpretation: nearly half the sweep fails stability criteria, limiting confidence in any positive-effect claim.

---

## 3) Target-Region Result (\(\Omega_m \approx 0.30\))
**Metric:** `final_a spread` (Bohmian-Q gaussian vs `alpha_qg`)

At \(\Omega_m = 0.3000\):
- `alpha_qg` width: **4.9457e-02**
- Bohmian-Q width: **4.5514e-05**
- Delta (Q − alpha): **-4.9411e-02**
- Relative ratio (Q/alpha): **9.2028e-04** (~0.092%)

Neighbor points:
- \(\Omega_m = 0.2975\): delta **-4.3531e-02**
- \(\Omega_m = 0.3025\): delta **-5.8958e-02**

Interpretation: Bohmian-Q envelope is sharply narrower than `alpha_qg` in and around the target region under this metric.

---

## 4) Decision Logic (Why HOLD_FOUNDATION)
The run fails the widening criterion in the target neighborhood and exhibits substantial instability. Therefore, the evidence threshold for promoting Bohmian-Q as an envelope-widening improvement is not met.

---

## 5) Confidence + Caveats
- **Confidence in this run-level decision:** **High**
- **Caveat:** This conclusion is conditional on current implementation and metric definition (`final_a spread`). If metric parity or filtering differs between branches, re-audit is required before final rejection.

---

## 6) Required Follow-Up (Before Any Policy Change)
1. **Metric parity audit**
   - Verify identical width definition, filtering, and sample support across `alpha_qg` and Bohmian-Q.
2. **Failure segmentation**
   - Cluster failed cases by parameter region and solver regime.
3. **Robustness metrics**
   - Recompute with IQR, 90% span, and MAD-scaled width to test sensitivity to metric choice.
4. **Gate for advancement**
   - Require consistent positive delta near \(\Omega_m \approx 0.30\) plus acceptable instability before changing recommendation.

---

## 7) Standardized Memo Template (for future runs)
Use this block for future artifact directories so run-to-run comparisons stay uniform:

```md
# Decision Memo — <Experiment Name>

- Timestamp: <YYYY-MM-DD HH:mm TZ>
- Artifact Directory: <path>
- Recommendation: <ADVANCE | HOLD_FOUNDATION | REJECT>
- Decision Status: <one-line conclusion>

## Executive Summary
<2–4 sentences with the core result>

## Core Evidence (Pass/Fail + Stability)
- Total cases: <n>
- Failed cases: <n>
- Passed cases: <n>
- Unstable rate: <float>

## Target-Region Result (<parameter neighborhood>)
- Baseline width: <value>
- Candidate width: <value>
- Delta (candidate − baseline): <value>
- Relative ratio: <value>
- Neighbor checks: <values>

## Decision Logic
<Explicit criteria mapping from evidence to recommendation>

## Confidence + Caveats
- Confidence: <Low/Med/High>
- Caveats: <assumptions / known limits>

## Required Follow-Up
1. <check>
2. <check>
3. <check>

## Repro Notes
- Commit / branch: <id>
- Script/command: <cmd>
- Random seeds: <seeds>
- Environment hash: <hash>
```

---

## 8) One-line Call
**Current action:** keep foundation model/path as default; do not promote Bohmian-Q widening on this evidence.
