# GR↔QM A-001 Closure Note — 2026-03-02

## Scope
Focused closure pass for Assumption A-001 using only measured artifacts and previously used sensitivity dimensions (ordering `n`, approximation timestep `dt_main`).

## Commands executed
1. Reproduce latest A-001 mini-test behavior:
   - `python notebooks/a001_closure_minitest.py`
2. Local boundary evaluation from fresh mini-test artifact:
   - `python -c "...boundary policy eval from grqm_a001_closure_minitest_20260302_175542/a001_minitest_summary.csv..."`
3. A-001 in-policy battery rerun:
   - `python -c "...a001 policy battery rerun (n in {4,5}, dt in [8e-4,1.2e-3])..."`

## New artifacts
- `notebooks/outputs/grqm_a001_closure_minitest_20260302_175542/`
  - `a001_minitest_summary.csv`
  - `aggregate.json`
- `notebooks/outputs/grqm_a001_boundary_policy_eval_20260302_175807/`
  - `a001_boundary_policy_eval.csv`
  - `aggregate.json`
- `notebooks/outputs/grqm_a001_policy_battery_rerun_20260302_175841/`
  - `a001_policy_battery_summary.csv`
  - `aggregate.json`

## Measured findings
- Reproduction (36 runs):
  - `pass_q1_rate=1.0`, `pass_q2_rate=1.0`, `pass_joint_rate=1.0`
  - `max_q1_sensitivity_vs_n5_dt1e3=6.58677`
- Boundary split (same dimensions only):
  - Candidate in-policy: `n in {4,5}`, `dt_main in [8e-4,1.2e-3]`, local sensitivity cap `<=1.0`.
  - In-policy: `24/24` pass (`100%`), `max_sensitivity=0.86634`.
  - Out-of-policy stress (`n=6`): sensitivity `5.246..6.587`; `0/12` policy-pass.
- In-policy battery rerun (24 runs):
  - `pass_rate=1.0`
  - extrema: `q1_refinement_max_obs=4.2363e-07`, `q2_p95_max=0.27043`, `q2_p99_max=0.35457`, `q2_replication_rel_diff_max=0.0`.

## Decision (conservative)
- **A-001 is cleared only under explicit local policy bounds**:
  - `correction_power_n in {4,5}`
  - `dt_main in [8e-4,1.2e-3]`
  - `q1_local_sensitivity_vs_n5_dt1e3 <= 1.0`
- `n=6` remains an explicit out-of-policy stress case; not used for promotion-supporting inference.

## Promotion impact
- Promotion eligibility remains **NO**.
- Reason: consecutive-cycle envelope policy still not satisfied; no speculative promotion applied.
