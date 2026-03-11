# GR/QM Nonlinear-Extension Plan (Post Edge Validity-Boundary)

Date: 2026-03-04
Status: preregistered experiment plan (edge lane only; additive)

## Scope and guardrails
- This plan applies **only** to exploratory edge-lane work at `Ω_m >= 0.305`.
- `C-WDW-001` in-core proven envelope remains unchanged (`Ω_m <= 0.300`).
- No mutation of baseline proven pipeline; all work is in additive scripts/artifacts.

## Motivation
Observed edge behavior includes transient non-perturbative episodes (`max |correction/classical| > 1`) at small `a`, suggesting semiclassical breakdown of the current leading-order correction closure. This plan tests whether minimal nonlinear regularizations can restore perturbative control in edge sweeps.

## Candidate extension families (minimal/reversible)
1. **Baseline (reference):**
   - `corr(a) = alpha_qg / a^5`
2. **Soft denominator regularization (NL-A):**
   - `corr(a) = alpha_qg / (a^5 + a_cut^5)`
3. **Smooth gate regularization (NL-B):**
   - `corr(a) = (alpha_qg / a^5) * tanh((a / a_cut)^k)`

Fixed initial candidate knobs for this cycle:
- `a_cut = 0.02`
- `k = 6`

## Falsifiable acceptance criteria (edge package)
All criteria evaluated on declared edge grid (`Ω_m in {0.305, 0.3075, 0.310}` and `alpha_qg in {3e-7, 7e-7, 1e-6, 1.3e-6}`):

### A) Perturbative ratio control
- **A-pass:** `max |correction/classical| <= 0.10` for every edge point.
- **A-fail:** any edge point with `max |correction/classical| > 0.10`.

### B) Minimum-scale guard
- **B-pass:** `min_a >= 0.020` for every edge point in successful solver runs.
- **B-fail:** any successful edge point with `min_a < 0.020`.

### C) Solver robustness gate
- **C-pass:** solver success rate = 100% on edge grid, no un-attributed crashes.
- **C-fail:** any failed case lacking traceable attribution.

## Decision logic
- **Accept extension candidate as edge-mitigation candidate** only if A+B+C all pass.
- Otherwise retain edge lane as blocked and recommend either:
  - tighter regularization parameter scan, and/or
  - explicit policy-level `min_a` cutoff framing.

## Planned outputs
- CSV/JSON tables containing per-case:
  - `(omega_m, alpha_qg, min_a, max_ratio, peak_t, solver outcome)`
- Aggregate comparison vs baseline.
- Recommendation note with caveats.
