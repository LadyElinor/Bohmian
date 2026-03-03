# PROXY_RATIONALE

## Why Q1 and Q2 exist

This project’s toy model is a workflow test bed, not a final cosmology model.

- **Q1 (effect existence + scaling):**
  Checks whether a declared correction channel produces a persistent, numerically stable signal inside a declared validity envelope.
- **Q2 (numerical divergence/instability signature):**
  Measures disagreement between approximation paths to detect method fragility before claims are promoted.

Together, Q1+Q2 separate “there is a signal” from “the signal is trustworthy under numerical stress.”

## What should remain invariant across model-class swaps
When moving from this toy ODE to a richer minisuperspace WDW reduction (or other family), the workflow keeps these structural invariants:

1. **Explicit envelope** (where statements are allowed)
2. **Predeclared gates/thresholds** (promotion is not post-hoc)
3. **Refinement checks + cross-method checks**
4. **Null-test discipline**
5. **Conservative claim state machine** (`OPEN`, `BLOCKED`, `PROVEN`)

Model equations can change; this governance scaffold should not.

## What would falsify the proxies themselves
- Q1 fails to persist above predeclared floor under refinement and local perturbations.
- Q1 ranking/sign behavior flips non-locally with small method/step changes.
- Q2 cannot distinguish robust vs fragile approximation families in controlled tests.
- Null tests that should pass repeatedly fail in-envelope.

If these happen, proxy definitions need revision before any claim advancement.
