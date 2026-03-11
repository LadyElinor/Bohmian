# GR_QM Born-Oppenheimer (BoO) Branch Kickoff Plan

Date: 2026-03-02 (EST)
Status: kickoff plan (conservative, no broad refactors)

## Objective
Open a bounded BoO branch to test whether a slow/fast split improves interpretability and stability of the existing proxy workflow **without changing governance baselines for promoted in-core claim scope**.

## Minimal derivation assumptions
1. Keep current toy baseline dynamics and correction structure from `notebooks/grqm_proxy_toymodel_v1.py`.
2. Introduce a two-timescale decomposition only as a diagnostic layer:
   - slow variable: envelope-like scale evolution,
   - fast variable: correction response around slow background.
3. Use first-order adiabatic closure (fast mode solved on frozen slow background over short windows).
4. No claim of physical completeness; branch is numerical/diagnostic and scoped to in-core corridor.
5. Preserve current envelope guardrails (`Ω_m<=0.300` for claim-bearing runs).

## Implementation sketch (tied to current notebooks)
- Reuse parameter grid conventions from:
  - `notebooks/cycle3_core_confirm.py`
  - `notebooks/grqm_proxy_toymodel_v1.py`
- Add starter branch script:
  - `notebooks/boo_branch_starter.py`
- Script responsibilities (phase-1):
  1. build core corridor grid (same Ω_m and α ranges as cycle-3 core confirm),
  2. compute baseline proxy metrics with existing solver paths,
  3. compute BoO diagnostic proxies (slow trend + fast residual amplitude),
  4. export one auditable CSV under `notebooks/outputs/`.

## First corridor experiment set
Run a minimal three-stage set:
1. **BoO-baseline map (core corridor)**
   - grid: Ω_m = {0.285, 0.290, 0.295, 0.300}
   - α = {3e-7, 5e-7, 7e-7, 1e-6, 1.3e-6}
2. **Numerical sensitivity spot-check**
   - fixed subset: 3 representative points
   - dt in {9e-4, 1.0e-3, 1.1e-3}
3. **Comparator check vs existing proxy metric**
   - rank consistency between existing Q1 proxy and BoO diagnostic score.

## Success / failure criteria
### Success criteria (kickoff stage)
- Deterministic rerun reproducibility on identical seeds/config.
- BoO output table complete for full 20-point core corridor.
- Rank consistency with existing proxy signal is monotonic (Spearman >= 0.95) on core grid.
- No governance contradiction with current promoted scope language.

### Failure criteria (kickoff stage)
- Missing/unstable outputs across reruns.
- Large rank inversions vs current proxy ordering (Spearman < 0.8).
- Diagnostics require changes to canonical gate thresholds or baseline hardening policy.

## Risk controls
- Keep BoO branch isolated from promotion ledger and claim matrix until criteria are met.
- Label all BoO artifacts as exploratory.
- Do not modify cycle-3-equivalent hardening gate baseline from this branch.
- If rank consistency fails, log failure and halt branch expansion pending review.

## Immediate next action
Execute:
- `python notebooks/boo_branch_starter.py`
Then append one short result note to journal/log with pass/fail against kickoff criteria.
