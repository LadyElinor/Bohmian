# Phase-2 Bohmian Envelope Comparison (alpha_qg vs Bohmian-Q)

- Recommendation: **HOLD_FOUNDATION**
- Rationale: At least one extended gate failed; retain HOLD pending tighter numerics or narrower operating region.

## Extended Gates
- Max refinement L2 (target <= 1.0e-06): 4.997e-02
- Max |correction|/|classical| (target <= 1.0): 3.890e+00
- Max null-check L2 (target <= 1.0e-08): 1.340e+00
- Unstable/blowup rate (target 0): 0.448

## Envelope Width (final_a spread across amplitude grid)
- omega_m=0.2950: alpha=3.945e-02, Q(gaussian)=3.592e-05, rel(Q/alpha)=9.105e-04
- omega_m=0.2975: alpha=4.357e-02, Q(gaussian)=3.981e-05, rel(Q/alpha)=9.136e-04
- omega_m=0.3000: alpha=4.946e-02, Q(gaussian)=4.551e-05, rel(Q/alpha)=9.203e-04
- omega_m=0.3025: alpha=5.901e-02, Q(gaussian)=5.529e-05, rel(Q/alpha)=9.369e-04
- omega_m=0.3050: alpha=7.967e-02, Q(gaussian)=7.986e-05, rel(Q/alpha)=1.002e-03
- omega_m=0.3075: alpha=9.973e-02, Q(gaussian)=0.000e+00, rel(Q/alpha)=0.000e+00
- omega_m=0.3100: alpha=3.446e-02, Q(gaussian)=0.000e+00, rel(Q/alpha)=0.000e+00
- omega_m=0.3125: alpha=5.062e-02, Q(gaussian)=0.000e+00, rel(Q/alpha)=0.000e+00
- omega_m=0.3150: alpha=6.273e-02, Q(gaussian)=3.237e-04, rel(Q/alpha)=5.160e-03

## Caveats
- 'unified_dmde_proxy' is used because an exact unified symbolic lane is not yet available.
- Numerical diagnostics are governance-facing quality checks, not observational confirmation.
