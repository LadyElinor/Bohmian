# GR_QM Toy Model Specification (v1)

Date: 2026-03-01  
Scope: auditable first-cycle proxy model for GR↔QM testability workflow

---

## 1) Model class and intent

This is a **minisuperspace-inspired ODE toy model** for testing workflow mechanics (null tests, convergence, uncertainty decomposition, replication), not a direct cosmological fit.

State vector:
\[
y(t)=\begin{bmatrix}a(t)\\v(t)\end{bmatrix},\quad v=\dot a
\]

Domain used in v1:
\[
t\in[0,3],\ a(t)>0
\]

---

## 2) Baseline equation (M0)

\[
\dot a=v,
\qquad
\dot v=-\frac{\Omega_m}{2a^2}+\Omega_\Lambda a
\]

Locked parameters:
- \(\Omega_m=0.3\)
- \(\Omega_\Lambda=0.7\)

Initial conditions:
- \(a(0)=0.1\)
- \(v(0)=1.5\)

---

## 3) Semiclassical-correction variant (M1)

\[
\dot a=v,
\qquad
\dot v=-\frac{\Omega_m}{2a^2}+\Omega_\Lambda a + \frac{\alpha_{QG}}{a^n}
\]

Locked correction settings for primary run:
- \(\alpha_{QG}=10^{-7}\)
- \(n=5\)

Assumption perturbation for sensitivity:
- keep all else fixed, switch \(n=5\to4\)

Interpretation: \(\alpha_{QG}/a^n\) is a phenomenological semiclassical proxy term (not derived from a unique UV completion).

---

## 4) Observable definitions

Q1 proxy amplitude:
\[
\Delta_{proxy}=\frac{\|a_{M1}-a_{M0}\|_2}{\|a_{M0}\|_2}
\]

Q2 divergence metrics:
\[
D(t)=|a_{approx}(t)-a_{exact}(t)|,
\qquad
D_*=\langle D(t)\rangle_t
\]

---

## 5) Validity range and assumptions

### Intended validity (v1)
- Positive-scale-factor branch only: \(a(t)>0\)
- Moderate-time horizon only: \(t\le3\)
- Deterministic ODE proxy; no stochastic forcing

### Explicit non-claims
- No claim of realistic late-time cosmological prediction.
- No claim that chosen correction form uniquely represents Wheeler–DeWitt physics.
- No claim of EFT matching to specific observational channel in v1.

### Key assumptions linked
- A-001: semiclassical emergent-time proxy is usable in this reduced setting.
- A-002: trajectory-level proxy captures meaningful correction effect.
- A-003: validity envelope above is not violated by chosen IC/parameters.
- A-005 (new): ordering exponent shift \(n=5\to4\) is a minimally informative sensitivity probe.

---

## 6) Run outputs (v1)

Primary machine-readable outputs:
- `outputs/grqm_proxy_results_v1.json`
- `outputs/grqm_proxy_results_v1_summary.csv`

Implementation:
- `notebooks/grqm_proxy_toymodel_v1.py`
- `notebooks/grqm_proxy_toymodel_v1.ipynb`
