# GR_QM Replication Report v1

Date: 2026-03-01  
Primary artifact: `outputs/grqm_proxy_results_v1.json`

---

## Objective

Test whether exact-vs-approx divergence pattern (Q2) is reproducible under a second computational path.

---

## Replication design

### Shared fixed components
- Same model equations and parameters
- Same initial conditions
- Same time window
- Same deterministic seed lock

### Path A (primary)
- Exact proxy: RK4, \(\Delta t=2.5\times10^{-4}\)
- Approximation: Euler, \(\Delta t=10^{-3}\)
- Output: \(D_* = 0.0717111063\)

### Path B (secondary)
- Exact proxy: RK4, \(\Delta t=2.5\times10^{-4}\)
- Approximation: RK4 coarse, \(\Delta t=2\times10^{-3}\)
- Output: \(D_*^{alt}=6.017751\times10^{-7}\)

---

## Divergence comparison

| Quantity | Path A | Path B | Relative difference |
|---|---:|---:|---:|
| \(D_*\) | 7.171111e-02 | 6.017751e-07 | 9.999916e-01 |
| \(D_{max}\) | 4.727969e-01 | 7.241862e-06 | — |

Predeclared replication tolerance: relative difference < 0.5  
Observed: 0.9999916 (**fail**)

---

## Interpretation (conservative)

- The apparent divergence in Path A is primarily a **method-order artifact** (Euler truncation) rather than a stable, model-level divergence structure.
- Replication criterion is not met.
- Q2 cannot be promoted beyond BLOCKED in this cycle.

---

## Logged failure mode

- Category: F-REPL / F-INFER
- Description: divergence claim not path-stable due to approximation mismatch.
- Recovery: replace Euler with controlled RK hierarchy and compare like-for-like truncation families.

---

## Next replication protocol (v2)

1. Define approximation family: RK1 vs RK2 vs RK4 at matched timesteps.
2. Require monotonic convergence in \(D_*\) with increasing order/decreasing \(\Delta t\).
3. Add one independent script-level implementation with identical equations but different code structure.
4. Promote Q2 only if path-to-path relative disagreement < 0.2 across two runs.
