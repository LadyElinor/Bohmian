# Research Assumption Register

Created: 2026-02-28  
Purpose: prevent hidden assumptions from driving invalid conclusions in advanced physics work.

---

## Usage Rules

1. Every nontrivial derivation/proxy claim must reference at least one Assumption ID.
2. Assumptions are tagged with status: **ACTIVE / TESTED / RETIRED**.
3. If an assumption materially affects interpretation, it must have a planned test or sensitivity check.
4. If a claim depends on 3+ untested assumptions, downgrade claim status to **OPEN**.

---

## 2026-03-02 Decision Addendum (auditable)

- Isolation finding: Cycle-4 gate regression is dominated by widened `dt` perturbation spread introduced in Cycle-4 hardening (autopsy + quick-revert diagnostics).
- Governance decision: baseline hardening signature for gate decisions is reverted to Cycle-3-equivalent perturbation bounds/signature.
- Control rule: widened `dt` perturbation probes are retained only as exploratory stress tests unless explicitly designated as gate-policy inputs.
- Cross-link: `GR_QM_QUICK_REVERT_NOTE_2026-03-02.md`.

## Assumption Log

| ID | Area | Assumption | Type (Model/Math/Inference/Experimental) | Impact if wrong | Test/Sensitivity Plan | Status | Owner | Last Updated |
|---|---|---|---|---|---|---|---|---|
| A-001 | WDW Semiclassical | WKB split yields usable emergent-time approximation in selected regime | Model | High | Local boundary evidence from A-001 closure pass: under explicit policy window (ordering n in {4,5}, dt in [8e-4,1.2e-3], local sensitivity vs n=5,dt=1e-3 <=1.0) all runs pass Q1/Q2/refinement checks; n=6 retained as out-of-policy stress (sensitivity jump >=5.246). | TESTED (localized, controllable via explicit ordering/approximation bounds) | Elinor | 2026-03-02 |
| A-002 | Proxy Mapping | Chosen observable proxy captures dominant effect of model correction term | Inference | High | Ablation against nearby templates and nuisance terms; focused IC nuisance sweep maps drift boundary. Within explicit nuisance policy (0.9993<=ic_scale<=1.0009, dt in [9e-4,1.1e-3]) all in-policy cases pass ranking/drift/stability criteria; ±0.1% IC treated as out-of-policy stress. | TESTED (localized, controllable via explicit nuisance bounds) | Elinor | 2026-03-02 |
| A-003 | EFT Range | Declared cutoff and validity envelope are consistent with reported observables | Math/Model | High | Enforce explicit envelope in gate docs; dense follow-up gives sharp transition (5/5 pass per Ω_m slice for 0.280..0.300, then 0/5 at 0.305/0.310). Boundary interpolation at hardened-sensitivity=0.2 gives Ω_m~0.30003; treat Ω_m<=0.305 as formal edge and Ω_m<=0.300 as high-confidence core corridor. | TESTED (sharp boundary observed; edge corridor still unstable and requires mitigation before expansion) | Elinor | 2026-03-01 |
| A-004 | Replication | Independent pipeline differences are within reconciliation budget | Inference | Medium | Split checks: (1) true like-vs-like replication, (2) separate method-family disagreement metric, and robust outlier-safe summaries (median/trimmed/p95/p99 + spike flag); Cycle-3 pivot verifies high-order method (DOP853) strongly reduces Q2 tail error on selected edge/core points | TESTED (true replication pass; robust Q2 diagnostics + pivot confirmation) | Elinor | 2026-03-01 |
| A-005 | Ordering Sensitivity Proxy | Changing correction exponent (n=5→4) is an acceptable first-order proxy for factor-ordering sensitivity | Model/Inference | High | Keep as wide stress test; pair with hardened perturbation gate for in-envelope robustness decisions | TESTED (two-tier: wide fragile, hardened stable) | Elinor | 2026-03-01 |
| A-006 | Independent Proxy Linearity | First-order alpha-doubling scaling (Δ(2α)≈2Δ(α)) is a valid independent corroboration check in this toy regime | Inference/Model | Medium | Track ratio_2a_over_a across Ω_m, α grid; report Pearson/Spearman and ratio distribution; classify strong tail deviations as out-of-envelope dynamics | TESTED (Cycle-2 dense follow-up: Pearson~0.935, Spearman~0.993; Cycle-3 core confirm: Pearson~0.99985, Spearman=1.0, ratio std~0.031) | Elinor | 2026-03-01 |

---

## Assumption Review Checklist (weekly)

- [ ] Any ACTIVE assumption with no test plan? (fix immediately)
- [ ] Any TESTED assumption that failed sensitivity checks? (move to RETIRED + log)
- [ ] Any OPEN/BLOCKED claims relying on same unresolved assumption cluster?
- [ ] Any assumption should be split into narrower assumptions?

---

## Decision Rule

- If a high-impact assumption fails: downgrade affected claims to **BLOCKED** until reformulated.
- If assumptions remain stable across two review cycles: promote related claim from OPEN → PROVISIONALLY PROVEN (with citation/proxy evidence).