# GR_QM Numerics Protocol (v1)

Date: 2026-03-01

---

## 1) Solvers and implementation

Language: Python (plain NumPy, no exotic dependencies).  
Equation type: deterministic coupled first-order ODE for \((a,v)\).

Implemented steppers:
- **RK4** (primary production integrator)
- **Euler** (intentionally low-order comparator for divergence stress test)

File:
- `notebooks/grqm_proxy_toymodel_v1.py`

---

## 2) Discretization choices (v1 lock)

- Main step: \(\Delta t_{main}=10^{-3}\)
- Refinement step: \(\Delta t_{ref}=5\times10^{-4}\)
- Exact-reference proxy step: \(\Delta t_{exact}=2.5\times10^{-4}\)
- Alternate replication path step: \(\Delta t_{coarse}=2\times10^{-3}\)

Time window: \([0,3]\)

---

## 3) Convergence / consistency checks

For both baseline and corrected models:
1. Run RK4 at main grid.
2. Run RK4 at refinement grid.
3. Interpolate main-grid trajectory to refinement grid.
4. Compute relative L2 refinement residual
\[
\epsilon_{ref}=\frac{\|a_{main\to ref}-a_{ref}\|_2}{\|a_{ref}\|_2}
\]

Pass threshold (predeclared):
\[
\epsilon_{ref} < 5\times10^{-3}
\]

Observed (v1):
- Baseline: \(2.80\times10^{-7}\)
- Corrected: \(2.76\times10^{-7}\)
- Both pass.

---

## 4) Reproducibility policy

- Seed policy: deterministic lock `seed=42` declared and recorded.
- Determinism: no stochastic terms in v1 model, but seed retained for forward compatibility.
- Required output artifacts per run:
  - JSON full metrics
  - CSV summary metrics
  - human-readable markdown interpretation files

Re-run command:
```powershell
python notebooks/grqm_proxy_toymodel_v1.py
```

---

## 5) Uncertainty decomposition method

Decompose into:
- **Statistical** \(u_{stat}\): sampling/resampling variance (v1 deterministic -> 0)
- **Systematic** \(u_{sys}\): discretization/method-choice effects
- **Epistemic** \(u_{epi}\): assumption-modeling fragility (ordering sensitivity in v1)

Total (quadrature):
\[
u_{tot}=\sqrt{u_{stat}^2+u_{sys}^2+u_{epi}^2}
\]

v1 implementation:
- Q1:
  - \(u_{sys}=\max(\epsilon_{ref}^{base},\epsilon_{ref}^{corr})\)
  - \(u_{epi}=|\Delta_{proxy}(n=4)-\Delta_{proxy}(n=5)|\)
- Q2:
  - \(u_{sys}=|D_*^{alt}-D_*^{primary}|\)
  - \(u_{epi}=0\) in v1 (no model-class perturbation done)

---

## 6) Failure safeguards and no-go rules

- If \(a\le0\), mark run nonphysical for this model branch.
- If refinement tolerance fails, no claim promotion.
- If replication relative disagreement > 0.5, Q2 inference remains BLOCKED.

---

## 7) v2 protocol upgrades (pre-registered)

- Replace Euler comparator with RK2/RK4 hierarchy for cleaner approximation-family diagnostics.
- Add multi-\(\alpha_{QG}\) sweep and fit monotonic response.
- Add alternate IC set to test envelope dependence.
