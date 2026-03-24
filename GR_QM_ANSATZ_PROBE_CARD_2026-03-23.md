# GR_QM Ansatz Probe Card (bounded quick test) — 2026-03-23

## Objective
Run exactly one low-cost re-ansatz check to test whether shoulder pinning is specific to additive/plateau/gaussian families.

## Variant
**Curvature-coupled damping ansatz (bounded)**
- Replace additive correction term with a bounded curvature-coupled modifier:
  - schematic: `corr_eff = alpha_qg * f(a,H,ddot_a)` where `f` is saturating (`tanh`/rational cap), not pure `a^-5` additive.
- Constraint: preserve null equivalence at `alpha_qg=0` and avoid denominator singular forms.

## Fixed controls
- Keep existing shoulder grid: `Omega_m in [0.3050, 0.3170], step 0.0005`.
- Keep phase2 numerics controls unchanged (`dt_main`, `dt_ref`, stress methods).
- Keep decision gates unchanged.

## Pass/fail interpretation
- **Meaningful move**: shoulder shift `>= 0.0020` with stable null checks.
- **No meaningful move**: shoulder shift `< 0.0020` and similar invariance profile.

## Artifacts required
- `outputs/ansatz_probe_YYYYMMDD_HHMMSS/decision.json`
- `.../boundary_delta.csv`
- `.../null_checks.csv`
- `.../receipt.json`

## Governance constraint
- Non-promoting diagnostic lane only.
- No claim-status mutation unless two consecutive confirmatory packets reproduce shift with unchanged gates.

## Stop condition
- Single packet only in this cycle; if null checks fail or stability collapses globally, terminate and record HOLD.
