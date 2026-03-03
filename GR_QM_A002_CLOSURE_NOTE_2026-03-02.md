# GR_QM A-002 Closure Note — 2026-03-02

## Scope
Focused conservative closure pass for A-002 (proxy mapping nuisance-drift blocker), using existing A-002 mini-test metrics/comparators.

## Commands run
1. `python notebooks/a002_proxy_ablation_minitest.py`
2. `python notebooks/a002_ic_nuisance_sweep.py`
3. `python notebooks/a002_proxy_ablation_policy_rerun.py`

## Artifacts
- Reproduction:
  - `notebooks/outputs/grqm_a002_proxy_ablation_minitest_20260302_174901/`
- Focused sweep:
  - `notebooks/outputs/grqm_a002_ic_nuisance_sweep_20260302_175011/`
- Policy rerun:
  - `notebooks/outputs/grqm_a002_proxy_ablation_policy_rerun_20260302_175101/`

## Measured results
- Reproduced known failures:
  - `nuisance_ic_minus_0p1pct`: `max_rel_drift_primary_l2=0.1483037867` (FAIL)
  - `nuisance_ic_plus_0p1pct`: `max_rel_drift_primary_l2=0.1092943006` (FAIL)
- Focused IC nuisance boundary map (same criteria):
  - passing band: `0.9993 <= ic_scale <= 1.0009`
  - equivalent: `-0.07% <= IC perturbation <= +0.09%`
  - classification: `localized_controllable`
- Policy rerun with explicit nuisance bounds:
  - policy: `ic_scale in [0.9993, 1.0009]`, `dt_main in [9e-4, 1.1e-3]`
  - in-policy cases: `5/5 pass` (`in_policy_pass_rate=1.0`)
  - out-of-policy stress retained and flagged: IC ±0.1%

## Decision
- Less-invasive path selected: **explicit nuisance-bound policy** (no proxy definition change).
- A-002 status updated to: **TESTED (localized, controllable via explicit nuisance bounds)**.

## Governance updates applied
- `RESEARCH_ASSUMPTION_REGISTER.md` (A-002 ACTIVE -> TESTED + bound notes)
- `GR_QM_CONSECUTIVE_CYCLE_PROMOTION_LEDGER.csv`
- `GR_QM_CONSECUTIVE_CYCLE_PROMOTION_LEDGER.md`
- `CLAIM_STATUS_MATRIX.md` (only blocker language adjusted to reflect A-002 bounded closure)
- `GR_QM_CYCLE_JOURNAL.md`
- `GR_QM_EXECUTION_LOG_8H.md`

## Conservative residuals
- Promotion remains **NOT eligible**.
- Remaining high-impact blocker: **A-001** and consecutive-cycle promotion rule.

## Exact next action
Run a mirrored focused closure pass for A-001 with the same conservative standard (local boundary map + explicit in-policy criteria), then refresh the promotion ledger from measured artifacts only.
