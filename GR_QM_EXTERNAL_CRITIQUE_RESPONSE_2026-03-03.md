# GR_QM External Critique Response — 2026-03-03

Source file reviewed: `critique.txt`

## Executive disposition
The critique is accepted as high-signal and largely correct on physical-interpretation gaps.
No in-core claim rollback is executed in this response. However, follow-up diagnostics are now explicitly framed as potentially claim-reopening if predeclared falsification conditions trigger.

## Point-by-point disposition

1. **Ω_m cliff (>=0.305) is a red flag, not just a boundary**
- Disposition: **Accepted**.
- Action: edge-lane diagnostics are now treated as potentially claim-reopening if instability mechanism implies in-envelope non-robustness.

2. **Linear α_qg scaling may be tautological**
- Disposition: **Accepted**.
- Action: document that scaling is interpreted as numerical faithfulness, not standalone physical novelty.

3. **"WDW-inspired" needs explicit derivation**
- Disposition: **Accepted (priority-1)**.
- Action: add public derivation appendix requirement before next promotion event.

4. **Q2 conflates numerical artifact and physics signal**
- Disposition: **Accepted (full)**.
- Action: relabel Q2 as numerical validity diagnostic, not direct physics observable.

5. **n=5 hardening directions are sparse**
- Disposition: **Accepted**.
- Action: add bias-reduced hardening expansion (Sobol/LHS style sampling) to next cycle backlog.

## Governance deltas (process-only)
- Add predeclared falsification condition for C-WDW-001 maintenance:
  - if edge diagnostic demonstrates correction-term pathology that mathematically implies expected instability intrudes into current in-core envelope under accepted dt/method policy, then C-WDW-001 status reopens from PROVEN -> OPEN pending revalidation.
- Add sequencing rule for cliff work:
  - derivation appendix -> pre-run prediction of instability mechanism -> diagnostic run -> governance decision.

## Immediate autonomous follow-up tasks
1. Add `docs/C-WDW-001_CORRECTION_DERIVATION.md` scaffold (public-facing derivation plan and required equations/choices).
2. Add `GR_QM_CWDW001_FALSIFICATION_PROTOCOL.md` with explicit re-open triggers.
3. Update action plan wording for Q2 to remove physics-observable framing.
4. Add next-cycle item for hardening-direction expansion.
