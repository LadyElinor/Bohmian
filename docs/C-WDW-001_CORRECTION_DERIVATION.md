# C-WDW-001 Correction Derivation (Public Appendix)

Status: scaffold (to be completed before next promotion event touching C-WDW-001 scope)

## Purpose
Make the "WDW-inspired" correction term explicit and auditable so C-WDW-001 rests on a visible derivation path, not only governance outcomes.

## Required contents

1. **Starting equation and model class**
- State the minisuperspace WDW form used.
- Declare variable reductions and assumptions.

2. **Ordering choice and rationale**
- Explicitly state factor ordering selected.
- State alternatives considered and why excluded.

3. **Semiclassical approximation steps**
- Show WKB/semi-classical expansion order retained.
- Show dropped terms and justification.

4. **Effective correction term mapping**
- Derive the ODE correction channel used in code.
- Provide symbolic form and parameter mapping into implementation.

5. **Consistency limits**
- Regime where approximation is expected valid.
- Regime where approximation is expected to fail.

6. **Testable predictions from derivation**
- Pre-run predictions for scaling/sign/trend behavior.
- Predicted instability/stiffness mechanism near edge if applicable.

## Implementation link targets
- Toy-model spec: `GR_QM_TOY_MODEL_SPEC.md`
- Numerics protocol: `GR_QM_NUMERICS_PROTOCOL.md`
- Claim matrix: `CLAIM_STATUS_MATRIX.md`

## Governance note
This appendix is mandatory for maintaining interpretation strength of C-WDW-001. Until completed, C-WDW-001 remains scope-limited and interpretation-conservative.
