# Phase-2 Bohmian Envelope Comparison (alpha_qg vs Bohmian-Q)

- Recommendation: **HOLD_FOUNDATION**
- Rationale: At least one extended gate failed; retain HOLD pending tighter numerics or narrower operating region.

## Extended Gates
- Max refinement L2 (target <= 1.0e-06): 1.099e-01
- Max |correction|/|classical| (target <= 1.0): 3.894e+00
- Max null-check L2 (target <= 1.0e-08): 1.340e+00
- Unstable/blowup rate (target 0): 0.833

## Envelope Width (final_a spread across amplitude grid)
- omega_m=0.3050: alpha=7.967e-02, Q(gaussian)=7.986e-05, rel(Q/alpha)=1.002e-03
- omega_m=0.3055: alpha=8.786e-02, Q(gaussian)=9.176e-05, rel(Q/alpha)=1.044e-03
- omega_m=0.3060: alpha=9.999e-02, Q(gaussian)=1.136e-04, rel(Q/alpha)=1.136e-03
- omega_m=0.3065: alpha=1.219e-01, Q(gaussian)=1.894e-04, rel(Q/alpha)=1.554e-03
- omega_m=0.3070: alpha=1.384e-01, Q(gaussian)=3.713e-04, rel(Q/alpha)=2.683e-03
- omega_m=0.3075: alpha=9.973e-02, Q(gaussian)=0.000e+00, rel(Q/alpha)=0.000e+00
- omega_m=0.3080: alpha=1.208e-01, Q(gaussian)=0.000e+00, rel(Q/alpha)=0.000e+00
- omega_m=0.3085: alpha=7.746e-02, Q(gaussian)=0.000e+00, rel(Q/alpha)=0.000e+00
- omega_m=0.3090: alpha=5.700e-02, Q(gaussian)=0.000e+00, rel(Q/alpha)=0.000e+00
- omega_m=0.3095: alpha=4.366e-02, Q(gaussian)=0.000e+00, rel(Q/alpha)=0.000e+00
- omega_m=0.3100: alpha=3.446e-02, Q(gaussian)=0.000e+00, rel(Q/alpha)=0.000e+00
- omega_m=0.3105: alpha=2.778e-02, Q(gaussian)=0.000e+00, rel(Q/alpha)=0.000e+00
- omega_m=0.3110: alpha=2.229e-02, Q(gaussian)=0.000e+00, rel(Q/alpha)=0.000e+00
- omega_m=0.3115: alpha=2.464e-02, Q(gaussian)=0.000e+00, rel(Q/alpha)=0.000e+00
- omega_m=0.3120: alpha=2.666e-02, Q(gaussian)=0.000e+00, rel(Q/alpha)=0.000e+00
- omega_m=0.3125: alpha=5.062e-02, Q(gaussian)=0.000e+00, rel(Q/alpha)=0.000e+00
- omega_m=0.3130: alpha=3.793e-02, Q(gaussian)=0.000e+00, rel(Q/alpha)=0.000e+00
- omega_m=0.3135: alpha=6.328e-02, Q(gaussian)=0.000e+00, rel(Q/alpha)=0.000e+00
- omega_m=0.3140: alpha=7.496e-02, Q(gaussian)=0.000e+00, rel(Q/alpha)=0.000e+00
- omega_m=0.3145: alpha=8.588e-02, Q(gaussian)=0.000e+00, rel(Q/alpha)=0.000e+00
- omega_m=0.3150: alpha=6.273e-02, Q(gaussian)=3.237e-04, rel(Q/alpha)=5.160e-03
- omega_m=0.3155: alpha=7.755e-02, Q(gaussian)=0.000e+00, rel(Q/alpha)=0.000e+00
- omega_m=0.3160: alpha=7.733e-02, Q(gaussian)=0.000e+00, rel(Q/alpha)=0.000e+00
- omega_m=0.3165: alpha=1.173e-01, Q(gaussian)=0.000e+00, rel(Q/alpha)=0.000e+00
- omega_m=0.3170: alpha=1.391e-01, Q(gaussian)=0.000e+00, rel(Q/alpha)=0.000e+00

## Caveats
- 'unified_dmde_proxy' is used because an exact unified symbolic lane is not yet available.
- Numerical diagnostics are governance-facing quality checks, not observational confirmation.
