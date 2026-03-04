# Claim Status Matrix

Created: 2026-02-28  
Updated: 2026-03-03 (governance sign-off finalized; in-core promotion retained with edge block caveat)

Purpose: enforce disciplined claim handling using **PROVEN / OPEN / BLOCKED** states.

---

## Status Definitions

- **PROVEN**: supported by pinned citation(s) and/or completed falsification protocol with stable inference.
- **OPEN**: plausible but incomplete; missing either citation hardening, proxy validation, or robustness checks.
- **BLOCKED**: cannot proceed due to missing prerequisites, failed assumptions, or unstable inference.

---

## Claim Table

| Claim ID | Claim Statement | Area | Status | Evidence Type | Evidence Link | Key Assumptions | Blocker (if any) | Next Action | Last Updated |
|---|---|---|---|---|---|---|---|---|---|
| C-CORE-001 | Physics mastery improves when sequence follows prerequisites + error feedback loops | Study OS | PROVEN | Operational outcomes + system design consistency | MASTER_DASHBOARD.md, MISTAKE_INTELLIGENCE_SYSTEM.md | — | — | Continue tracking weekly metrics | 2026-02-28 |
| C-GRQM-001 | EFT-first discipline improves testability of GR↔QM research programs | GR↔QM | OPEN | Proxy workflow execution + governance consistency | GR_QM_TESTABILITY_BLUEPRINT.md, GR_QM_EXECUTION_LOG_8H.md | A-002, A-003, A-004 | Empirical KPI trend not yet established | Run cycle-2 with improved replication discipline | 2026-03-01 |
| C-GRQM-002 | Exact-vs-approx divergence can provide robust test signal in this toy setting | GR↔QM numerics | OPEN (provisional in-core support) | Tiered + robust proxy test + Cycle-3 DOP853 pivot confirmation | Q1_Q2_GATE_UPDATE.md, notebooks/outputs/grqm_q2_calibration_extended_20260301_192247/summary.csv, notebooks/outputs/grqm_q2_calibration_robust_20260301_193233/summary.csv, notebooks/outputs/grqm_cycle3_q2_pivot_20260301_223823/cycle3_q2_pivot_summary.csv | A-004 | Remaining blocker for full PROVEN is multi-cycle promotion policy, not current core-metric failure | Keep OPEN at global level; adopt DOP853 pivot as preferred approx family in core and require repeated-cycle confirmation | 2026-03-01 |
| C-WDW-001 | A semiclassical WDW-inspired correction can induce a persistent low-energy toy proxy signal | WDW proxy | PROVEN (core envelope) | Tiered-gate simulation evidence + uncertainty accounting + cycle-2 boundary mapping + cycle-3 core confirmation + A-002 IC nuisance closure sweep + A-001 bounded ordering/approx closure pass + quick-revert isolation + full reverted-hardening confirmation + explicit null-test log | Q1_Q2_GATE_UPDATE.md, notebooks/outputs/grqm_cycle2_dense_followup_20260301_215901/envelope_summary.csv, notebooks/outputs/grqm_cycle2_dense_followup_20260301_215901/proxy_agreement.csv, notebooks/outputs/grqm_cycle2_boundarycheck_20260301_222955/boundary_fit.json, notebooks/outputs/grqm_cycle2_edge305_proxycheck_20260301_223008/aggregate.json, notebooks/outputs/grqm_cycle3_core_confirm_20260301_223742/cycle3_core_confirm_summary.csv, notebooks/outputs/grqm_cycle3_core_confirm_20260302_172931/cycle3_core_confirm_summary.csv, notebooks/outputs/grqm_cycle3_core_confirm_20260302_215234/cycle3_core_confirm_summary.csv, notebooks/outputs/grqm_quick_revert_hardening_20260302_214712/aggregate.json, GR_QM_NULL_TEST_LOG.md, GR_QM_CONSECUTIVE_CYCLE_PROMOTION_LEDGER.md, GR_QM_MONTHLY_GATE_REPORT_01.md | A-003, A-005, A-006 | Scope-limited caveat: PROVEN status applies only to core envelope Ω_m<=0.300 with Cycle-3-equivalent hardening baseline; edge corridor Ω_m>=0.305 remains blocked pending dedicated mitigation evidence. | Preserve envelope guardrails; keep widened dt hardening probes exploratory-only unless policy-promoted; open next lane after monthly governance close. | 2026-03-02 |
| C-WDW-002 | Generic equivalence-principle violation follows directly from WDW | WDW | BLOCKED | None (overgeneralized) | — | A-002 | Model dependence not specified | Keep blocked unless model class + test path are explicit | 2026-02-28 |

---

## Milestone Promotion Decision – 2026-03-02 (Post-Cycle-4-reverted-hardening)

Cycle pair: `cycle-3-rerun-20260302` + `cycle-4-reverted-hardening-20260302`

- All gates: PASS (consecutive, same envelope)
- Null-tests: explicitly passed and logged (`GR_QM_NULL_TEST_LOG.md`)
- Assumptions: A-001/A-002 TESTED and closed under Cycle-3 baseline hardening policy
- High-impact unresolved assumptions: none active

**Verdict: PROMOTE to PROVEN** for the core Q1 proxy claim in the declared envelope.

Promotion scope and caveat:
- Applies to stable in-core envelope only (`Ω_m <= 0.300`, declared α corridor, Cycle-3-equivalent hardening signature).
- Does not apply to edge expansion; `Ω_m >= 0.305` remains blocked pending dedicated mitigation evidence.

Cross-refs:
- `GR_QM_MONTHLY_GATE_REPORT_01.md`
- `GR_QM_CONSECUTIVE_CYCLE_PROMOTION_LEDGER.md`

## Diagnostic branch receipt (non-promoting)
- Nonlinear scalar branch phase-1b method-controlled micro-check completed with RK-family comparator and tiny dt anchor:
  - `GR_QM_NONLINEAR_PHASE1B_NOTE_2026-03-03.md`
  - `notebooks/outputs/grqm_nonlinear_scalar_phase1b_20260303_175346/nonlinear_phase1b_metrics.json`
- Interpretation: contracts prior Euler-vs-RK spread for this narrow diagnostic lane; does not mutate claim status, thresholds, or envelope scope.

## External critique follow-up (2026-03-03)
- External critique ingested from `critique.txt`; response + actions logged in:
  - `GR_QM_EXTERNAL_CRITIQUE_RESPONSE_2026-03-03.md`
  - `GR_QM_CWDW001_FALSIFICATION_PROTOCOL.md`
  - `docs/C-WDW-001_CORRECTION_DERIVATION.md`
- Governance note: C-WDW-001 remains PROVEN in-core, but edge-cliff investigation is explicitly allowed to reopen status if falsification triggers fire.

## Claim Hygiene Checklist

- [x] Does the claim have explicit scope and validity range?
- [x] Are assumptions linked by ID?
- [x] Is there a falsification path (if empirical claim)?
- [x] Is uncertainty/robustness stated?
- [x] Is status set conservatively?

---

## Escalation Rule

Claim promotion requires:
- OPEN → PROVEN: evidence hardening + no unresolved high-impact assumption conflict.
- BLOCKED → OPEN: blocker explicitly resolved and logged in failure/assumption registers.
