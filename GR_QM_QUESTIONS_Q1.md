# GR↔QM Questions Q1 (Refined Lock)

Updated: 2026-03-01  
Status: first runnable cycle completed (conservative interpretation)

---

## Locked Variable Conventions

- Time: \(t\in[0,3]\), dimensionless.
- Scale factor proxy: \(a(t)>0\), dimensionless.
- Velocity: \(v(t)=\dot a(t)\).
- Cosmology-like coefficients: \(\Omega_m=0.3\), \(\Omega_\Lambda=0.7\).
- Semiclassical proxy parameter: \(\alpha_{QG}=10^{-7}\).
- Correction power (ordering proxy): baseline corrected run uses \(n=5\); perturbation run uses \(n=4\).
- Initial condition (locked for v1):
  - \(a(0)=0.1\)
  - \(\dot a(0)=1.5\)

## Toy Equations Used in Cycle-1

### Baseline
\[
\ddot a = -\frac{\Omega_m}{2a^2}+\Omega_\Lambda a
\]

### Semiclassical-corrected variant
\[
\ddot a = -\frac{\Omega_m}{2a^2}+\Omega_\Lambda a + \frac{\alpha_{QG}}{a^n},\quad n=5
\]

System form:
\[
\dot a=v,\qquad \dot v=f(a)
\]

---

## Q1 — Semiclassical correction proxy detectability

### Question
Does the \(\alpha_{QG}/a^n\) term create a persistent nonzero trajectory deviation proxy after numerical and assumption checks?

### Primary metric
\[
\Delta_{proxy}=\frac{\|a_{corr}-a_{base}\|_2}{\|a_{base}\|_2}
\]

### Predeclared tolerances
- Effect persistence threshold: \(\Delta_{proxy} > 10^{-4}\)
- Refinement tolerance: relative refinement residual \(<5\times10^{-3}\)
- Assumption fragility tolerance: relative shift under \(n=5\to4\), \(<0.5\)

### Cycle-1 measured values
- \(\Delta_{proxy}=1.0077\times10^{-2}\) (passes persistence threshold)
- Baseline refinement residual: \(2.80\times10^{-7}\) (passes)
- Corrected refinement residual: \(2.76\times10^{-7}\) (passes)
- Ordering sensitivity: \(0.866\) (fails fragility tolerance)

### Conservative status
**OPEN** (signal exists and numerics converge, but assumption sensitivity is too high for stronger claim).

---

## Q2 — Exact-vs-approx divergence reproducibility

### Question
Is the divergence between high-accuracy reference and approximate evolution reproducible across a second implementation path?

### Metrics
- Pointwise divergence: \(D(t)=|a_{approx}(t)-a_{exact}(t)|\)
- Summary scalar: \(D_*=\langle D(t)\rangle_t\)

### Predeclared tolerances
- Nontrivial divergence threshold: \(D_*>10^{-4}\)
- Replication consistency threshold: relative difference between path-A and path-B \(<0.5\)

### Cycle-1 measured values
- Path-A (Euler vs exact RK4): \(D_*=7.1711\times10^{-2}\)
- Path-B (coarse RK4 vs exact RK4): \(D_*^{alt}=6.02\times10^{-7}\)
- Relative path disagreement: \(0.99999\) (fails)

### Conservative status
**BLOCKED** (divergence is method-choice dominated; replication disagreement too large for inference).

---

## Shared Uncertainty Snapshot (Cycle-1)

| Question | Metric | Statistical | Systematic | Epistemic | Total | Status |
|---|---:|---:|---:|---:|---:|---|
| Q1 | \(\Delta_{proxy}\) | 0 | \(2.80\times10^{-7}\) | \(8.73\times10^{-3}\) | \(8.73\times10^{-3}\) | OPEN |
| Q2 | \(D_*\) | 0 | \(7.17\times10^{-2}\) | 0 | \(7.17\times10^{-2}\) | BLOCKED |

---

## Immediate next lock for Cycle-2
- Keep same baseline equation and ICs.
- Replace Euler comparator in Q2 with controlled low-order truncation family (RK2/RK4-pair) to avoid trivial method artifact.
- Add small grid of \(\alpha_{QG}\in\{3\times10^{-8},10^{-7},3\times10^{-7}\}\) and require monotonic response in \(\Delta_{proxy}\).
