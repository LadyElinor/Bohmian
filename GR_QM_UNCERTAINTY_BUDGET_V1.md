# GR_QM Uncertainty Budget v1

Date: 2026-03-01  
Source run: `outputs/grqm_proxy_results_v1.json`

---

## Summary table

| Question | Primary Metric | Value | u_stat | u_sys | u_epi | u_total | Conservative Interpretation |
|---|---:|---:|---:|---:|---:|---:|---|
| Q1 | \(\Delta_{proxy}\) | 1.007662e-02 | 0 | 2.795794e-07 | 8.730266e-03 | 8.730266e-03 | Effect present, but dominated by epistemic fragility (OPEN) |
| Q2 | \(D_*\) | 7.171111e-02 | 0 | 7.171050e-02 | 0 | 7.171050e-02 | Divergence dominated by method/path choice, not robust (BLOCKED) |

---

## Q1 decomposition details

- Metric definition:
\[
\Delta_{proxy}=\frac{\|a_{corr}-a_{base}\|_2}{\|a_{base}\|_2}
\]
- Measured: `0.010076623804269946`
- Numerical refinement checks:
  - baseline `2.7957944614838807e-07`
  - corrected `2.763248735938505e-07`
- Assumption perturbation (ordering proxy):
  - \(n=5\): `0.010076623804269946`
  - \(n=4\): `0.0013463576092608515`
  - induced relative sensitivity: `0.8663880248569763`

Interpretation: numerical discretization uncertainty is negligible; assumption choice dominates uncertainty envelope.

---

## Q2 decomposition details

- Metric definition:
\[
D_*=\langle|a_{approx}-a_{exact}|\rangle_t
\]
- Primary path (Euler vs fine RK4):
  - `D_star = 0.07171110629475136`
- Replication path (coarse RK4 vs fine RK4):
  - `D_star_alt = 6.017751406781911e-07`
- Path disagreement:
  - relative diff = `0.9999916083411236`
- Assigned systematic uncertainty:
  - `u_sys = |D_star_alt - D_star| = 0.07171050451961068`

Interpretation: Q2 signal is not stable across approximation path definitions; cannot support robust physical inference in v1.

---

## Decision impact

- Q1: keep **OPEN**; not promotable due to high epistemic share.
- Q2: set **BLOCKED** pending redesigned approximation-family comparison.
