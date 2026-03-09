# Claim Status Matrix

Created: 2026-02-28  
Updated: 2026-03-08 (edge extension governance addendum logged; core status unchanged)

Purpose: enforce disciplined claim handling using **PROVEN / OPEN / BLOCKED** states.

Quick status anchor: `docs/CURRENT_TRUTH_2026-03.md`.

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
| C-GRQM-002 | Exact-vs-approx divergence can provide robust test signal in this toy setting | GR↔QM numerics | PROVEN (in-core toy envelope) | Tiered + robust proxy test + Cycle-3 DOP853 pivot confirmation + dual RK-family mini-pack receipts + dual-receipt audit + governance close package | Q1_Q2_GATE_UPDATE.md, notebooks/outputs/grqm_q2_calibration_extended_20260301_192247/summary.csv, notebooks/outputs/grqm_q2_calibration_robust_20260301_193233/summary.csv, notebooks/outputs/grqm_cycle3_q2_pivot_20260301_223823/cycle3_q2_pivot_summary.csv, notebooks/outputs/grqm_cgrqm002_rk_family_minipack_20260305_171537/summary.json, notebooks/outputs/grqm_cgrqm002_rk_family_minipack_20260305_184849/summary.json, notebooks/outputs/grqm_cgrqm002_dual_receipt_audit_20260305_185746/dual_receipt_audit_report.json, GR_QM_CGRQM002_GOVERNANCE_DECISION_PACKAGE_2026-03-05.md, GR_QM_CGRQM002_CLOSURE_NOTE_2026-03-05.md | A-004 | Scope caveat: promotion applies only to current in-core toy envelope/protocol; edge lane Ω_m>=0.305 remains blocked and out of scope. | Maintain in-core monitoring cadence; route any envelope expansion through separate preregistered edge-governance sequence. | 2026-03-05 |
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
- Symbolic consistency + core/edge diagnostic pack receipt (late 2026-03-05):
  - `GR_QM_SYMBOLIC_VALIDATION_NOTE_2026-03-05.md`
  - `notebooks/outputs/grqm_core_edge_diag_pack_20260305_214242/core_edge_diag_summary.json`
  - `notebooks/outputs/grqm_symbolic_ratio_receipt_20260305_214243/symbolic_correction_ratio_summary.json`
- Interpretation: improves derivation/diagnostic traceability; does not mutate claim status, thresholds, or envelope scope.

## External critique follow-up (2026-03-03)
- External critique ingested from `critique.txt`; response + actions logged in:
  - `GR_QM_EXTERNAL_CRITIQUE_RESPONSE_2026-03-03.md`
  - `GR_QM_CWDW001_FALSIFICATION_PROTOCOL.md`
  - `docs/C-WDW-001_CORRECTION_DERIVATION.md`
- Governance note: C-WDW-001 remains PROVEN in-core, but edge-cliff investigation is explicitly allowed to reopen status if falsification triggers fire.

## C-GRQM-001 confirmation trend (new row)

| Run Date | Artifact | Envelope Pass | q1_refinement_max_obs_max | q1_assumption_sensitivity_hardened_max | q2_D_p95_max | q2_D_p99_max | q2_true_replication_rel_diff_max | Note |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 2026-03-05 | `notebooks/outputs/grqm_cycle3_core_confirm_20260305_171322/cycle3_core_confirm_summary.csv` + `aggregate.json` | 20/20 (1.0) | 2.795794461483881e-07 | 0.1483037867483375 | 0.2849869470187435 | 0.3892032151943856 | 0.0 | Fresh confirmation reproducibly matches prior core-cycle maxima; supports keeping C-GRQM-001 OPEN while trend hardening continues. |

## C-GRQM-002 Governance Close Decision – 2026-03-05

Decision selected: **Option A (Promote now, in-core only)**.

- Status transition executed: `C-GRQM-002` moved **OPEN → PROVEN (in-core toy envelope)**.
- Basis: two independent same-day RK-family mini-pack receipts + dual-receipt audit PASS against predeclared acceptance criteria.
- Scope caveat: promotion does **not** apply to edge lane; `Ω_m >= 0.305` remains blocked and unchanged.

Cross-refs:
- `GR_QM_CGRQM002_GOVERNANCE_DECISION_PACKAGE_2026-03-05.md`
- `GR_QM_CGRQM002_CLOSURE_NOTE_2026-03-05.md`
- `GR_QM_MONTHLY_GATE_REPORT_01.md`
- `GR_QM_CONSECUTIVE_CYCLE_PROMOTION_LEDGER.md`

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

## Edge extension governance update (2026-03-08)

- New receipt (full completion):
  - `notebooks/outputs/grqm_edge_companion_inpolicy_adaptive_checkpointed_20260307_132048/edge_companion_aggregate.json`
- Packet outcome:
  - `completed_cases=20/20`, `pass_all_packet_rate=1.0`
  - `max_q1_refinement=1.0475384872639079e-08` (threshold 1e-6)
  - `max_q1_hardened=0.1483037382017592` (threshold 0.18)
  - `max_q2_p95=0.0`, `max_q2_p99=0.0`, `max_replication=0.0`

Governance decision:
- C-WDW-001 core status remains **PROVEN (core envelope)**.
- Edge region (`Ω_m <= 0.31`) is now numerically tractable and passes all proxy gates under mandatory constraints: adaptive refinement + stiff solver (Radau baseline) + overlapping-time interpolation for refinement metrics.
- Exploratory inclusion is approved under those constraints.
- Physical claims in this lane require a mandatory semiclassical validity caveat: transient non-perturbative dominance (`correction/classical ratio > 1` near `min_a ≈ 0.01`) means this lane is outside the perturbative semiclassical validity assumed by C-WDW-001.
