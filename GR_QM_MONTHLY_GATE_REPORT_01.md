# GR_QM Monthly Gate Report 01

Date: 2026-03-02
Cycle Window: Cycle-3 rerun through Cycle-4 reverted-hardening confirmation
Decision Mode: Evidence-first, conservative governance

## KPI Summary
- Two consecutive full-cycle in-envelope passes under reverted baseline hardening.
- High-impact assumptions A-001/A-002 now TESTED with explicit policy bounds.
- Technical blocker isolated and mitigated (Cycle-4 widened dt hardening mix identified as regression source).

## Gate Snapshot (core envelope)
For both consecutive confirmation cycles (`cycle-3-rerun-20260302`, `cycle-4-reverted-hardening-20260302`):
- G-PROXY: PASS
- G-REFINE: PASS
- G-ROBUST-Q1: PASS
- G-ROBUST-Q2: PASS
- G-REPLICATION: PASS
- G-ENVELOPE: PASS

## Null-Test Compliance
Explicit null definitions and cycle-level reject outcomes are now documented in:
- `GR_QM_NULL_TEST_LOG.md`

## Governance Interpretation
- Technical/numerical blocker status: **cleared in-core**.
- Edge expansion (Ω_m >= 0.305): **still blocked** pending dedicated mitigation evidence.
- Governance hold-lift for in-core promotion: **executed** (see addendum below).

## Decision
**Proceed (conservative, post hold-lift):**
1. Keep Cycle-3-equivalent hardening signature as gate baseline.
2. Treat widened dt hardening probes as exploratory-only unless explicitly promoted into gate policy.
3. Maintain promoted in-core claim posture in ledger/matrix with explicit scope caveat.
4. Keep Ω_m >= 0.305 as blocked edge lane until dedicated mitigation evidence clears expansion criteria.

## Governance Hold-Lift Addendum (2026-03-02)
Date-stamped governance action: **2026-03-02 (EST)**

- Hold-lift scope: in-core Q1 proxy claim only (`Ω_m <= 0.300`, declared α corridor, Cycle-3-equivalent hardening signature).
- Promotion action executed across canonical governance artifacts:
  - `CLAIM_STATUS_MATRIX.md`: `C-WDW-001` retained as **PROVEN (core envelope)** with explicit edge block caveat.
  - `GR_QM_CONSECUTIVE_CYCLE_PROMOTION_LEDGER.csv/.md`: promotion eligibility flipped to **YES** for `cycle-4-reverted-hardening-20260302`.
- Explicit non-expansion caveat: **`Ω_m >= 0.305` remains blocked** pending dedicated mitigation evidence and separate governance close.

## Canonical artifacts
- `notebooks/outputs/grqm_cycle3_core_confirm_20260302_172931/`
- `notebooks/outputs/grqm_cycle3_core_confirm_20260302_215234/`
- `GR_QM_CONSECUTIVE_CYCLE_PROMOTION_LEDGER.csv`
- `GR_QM_CONSECUTIVE_CYCLE_PROMOTION_LEDGER.md`
- `GR_QM_NULL_TEST_LOG.md`

## Main-Lane Governance Sign-off Addendum (2026-03-03)
Date-stamped governance action: **2026-03-03 (EST)**

- Main-lane governance lift/sign-off is confirmed and finalized.
- No main-lane thresholds or claim statuses changed in this addendum.
- Bounded nonlinear branch receipt linked as method-risk closure context (non-promoting):
  - `GR_QM_NONLINEAR_PHASE1B_NOTE_2026-03-03.md`
  - `notebooks/outputs/grqm_nonlinear_scalar_phase1b_20260303_175346/nonlinear_phase1b_metrics.json`
- Scope caveat unchanged: **`Ω_m >= 0.305` remains blocked** pending dedicated mitigation evidence.

## C-GRQM-002 Governance-Close Addendum (2026-03-05)
Date-stamped governance review packet readiness: **2026-03-05 (EST)**

- New evidence ingested for C-GRQM-002:
  - RK-family mini-pack run 1: `notebooks/outputs/grqm_cgrqm002_rk_family_minipack_20260305_171537/summary.json`
  - Independent repeat run: `notebooks/outputs/grqm_cgrqm002_rk_family_minipack_20260305_184849/summary.json`
  - Cross-receipt consistency audit: `notebooks/outputs/grqm_cgrqm002_dual_receipt_audit_20260305_185746/dual_receipt_audit_report.json`
- Both mini-pack receipts satisfy the predeclared acceptance envelope; audit decision = **PASS**.
- No edge-lane expansion requested or implied by this addendum; **`Ω_m >= 0.305` remains blocked**.

### Explicit decision options for governance close
1. **Option A — Promote now (in-core only):** reclassify C-GRQM-002 to PROVEN for current in-core toy envelope and keep edge lane blocked.
2. **Option B — Conditional hold (default conservative):** keep C-GRQM-002 OPEN until one additional independent-cycle receipt is logged, then auto-escalate for promotion vote.

Governance decision executed: **Option A**.

Execution outcomes (2026-03-05):
- `C-GRQM-002` promoted to **PROVEN (in-core toy envelope)**.
- Closure note issued: `GR_QM_CGRQM002_CLOSURE_NOTE_2026-03-05.md`.
- Scope caveat preserved: **`Ω_m >= 0.305` remains blocked** and unchanged.

## Astropy Background Diagnostic Receipt Addendum (2026-03-05)
Date-stamped diagnostic receipt: **2026-03-05 (EST)**

Objective:
- Add independent library-backed background sanity context (FlatΛCDM via Astropy) without changing claims/gates.

Receipts:
- Baseline diagnostic:
  - `notebooks/outputs/grqm_astropy_background_validation_20260305_192643/astropy_background_validation_summary.csv`
- Sensitivity repeat (`dt`, `a0`, `v0` perturbations):
  - `notebooks/outputs/grqm_astropy_background_sensitivity_20260305_192913/astropy_background_sensitivity_aggregate.json`
- Interpretation note:
  - `GR_QM_ASTROPY_BACKGROUND_VALIDATION_NOTE_2026-03-05.md`

Two tracked metrics:
1. Shape mismatch envelope (`shape_l2_error`) by Ω_m across sensitivity sweep:
   - Ω_m=0.285: min 0.1076, max 2.8109
   - Ω_m=0.300: min 0.1278, max 1.3315
   - Ω_m=0.3075: min 0.1176, max 2.3324
2. Monotonicity diagnostic:
   - Astropy reference monotonic in baseline receipt; toy classical trajectory monotonicity can break under some sweep settings.

Governance effect:
- **No claim-status or threshold changes.**
- Keep as diagnostic context only; edge lane block remains unchanged (`Ω_m >= 0.305`).

## Symbolic Correction Validation Addendum (2026-03-05)
Date-stamped diagnostic receipt: **2026-03-05 (EST)**

Objective:
- Add symbolic auditability for correction-term scaling in `src/grqm/core.py` and provide a reproducible correction/classical ratio receipt across core+edge Ω_m points.

Receipts:
- Symbolic validator implementation: `src/grqm/symbolic.py`
- Run-level metadata integration: `src/grqm/core.py`
- Compact derivation receipt: `GR_QM_CWDW001_SYMBOLIC_DERIVATION_RECEIPT_2026-03-05.md`
- Diagnostic note: `GR_QM_SYMBOLIC_VALIDATION_NOTE_2026-03-05.md`
- Ratio scan output (timestamped run): `notebooks/outputs/grqm_symbolic_ratio_receipt_*/`

Tracked diagnostic checks:
1. Leading correction exponent (default `n=5`) verified as `-5`.
2. Small-`a` correction/classical ratio exponent verified as `-3` (`2-n`).

Governance effect:
- **Diagnostic-only traceability improvement; no status/policy/threshold changes.**
- Existing scope caveat remains: edge lane `Ω_m >= 0.305` still blocked.
