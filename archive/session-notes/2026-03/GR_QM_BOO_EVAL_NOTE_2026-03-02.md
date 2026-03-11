# GR_QM BoO Kickoff Evaluation Note — 2026-03-02

## Scope
Execute first Born–Oppenheimer (BoO) corridor evaluation from current scaffold and assess pass/fail against:
- `GR_QM_BOO_BRANCH_PLAN_2026-03-02.md`

## Inputs reviewed
- `GR_QM_BOO_BRANCH_PLAN_2026-03-02.md`
- `notebooks/boo_branch_starter.py`

## Runs executed
1. Primary corridor run
   - `python notebooks/boo_branch_starter.py`
2. Conservative evaluator run (metrics + spot-checks)
   - `python notebooks/boo_branch_evaluate.py`

## Output artifacts
- `notebooks/outputs/grqm_boo_branch_starter_20260302_222143/boo_branch_summary.csv`
- `notebooks/outputs/grqm_boo_branch_starter_20260302_222143/boo_sensitivity_spotcheck.csv`
- `notebooks/outputs/grqm_boo_branch_starter_20260302_222143/boo_eval_metrics.json`

## Key BoO-vs-baseline metrics
- Core corridor rows: **20/20**
- Rank consistency (Q1 proxy vs BoO slow diagnostic): **Spearman = 1.0000**
- Deterministic reproducibility (same config, recomputed full corridor):
  - max abs delta: **0.0**
  - max rel delta: **0.0**
- Signal retention (span ratio):
  - baseline Q1: **22.9170284**
  - BoO slow: **22.9169947**
- Numerical sensitivity spot-check (3 points; dt={9e-4,1e-3,1.1e-3}):
  - max rel delta Q1: **4.9589e-4**
  - max rel delta BoO slow: **4.9480e-4**
  - max rel delta BoO fast RMS: **1.5323e-1**

## Criteria mapping (explicit)
### Success criteria (kickoff stage)
1. Deterministic rerun reproducibility on identical config: **PASS**
2. Full 20-point BoO output table: **PASS**
3. Monotonic rank consistency Spearman >= 0.95: **PASS** (1.0000)
4. No governance contradiction with promoted scope language: **PASS** (diagnostic-only branch retained)

### Failure criteria (kickoff stage)
1. Missing/unstable outputs across reruns: **NOT TRIGGERED**
2. Large rank inversions / Spearman < 0.8: **NOT TRIGGERED**
3. Need to change canonical thresholds/hardening policy: **NOT TRIGGERED**

## Pass/Fail verdict
**PASS (BoO kickoff corridor evaluation).**

## Follow-up tweak requirement check
Initial run is not failed/ambiguous; therefore the required contingency step (single-factor follow-up tweak and rerun subset) was **not invoked**.

## Conservative recommendation
Keep BoO branch isolated as exploratory diagnostics. Next trigger should be a small phase-2 stress pass (method + dt cross-check) only if explicitly requested, with no policy/gate changes.

## Phase-2 stress extension (dt/method cross-check) — 2026-03-02 22:36 EST

### Command executed
- `python notebooks/boo_phase2_stress_extension.py`

### Phase-2 artifacts
- `notebooks/outputs/grqm_boo_phase2_stress_20260302_223624/phase2_run_log.jsonl`
- `notebooks/outputs/grqm_boo_phase2_stress_20260302_223624/boo_phase2_crosscheck_summary.csv`
- `notebooks/outputs/grqm_boo_phase2_stress_20260302_223624/boo_phase2_crosscheck_deltas.csv`
- `notebooks/outputs/grqm_boo_phase2_stress_20260302_223624/boo_phase2_report.json`

### Scope lock and criteria handling
- Corridor subset only (3 representative points): `(Ω_m, α) = (0.285,3e-7), (0.295,7e-7), (0.300,1.3e-6)`.
- Cross-check matrix: `dt ∈ {9e-4,1e-3,1.1e-3}`, `method ∈ {rk4,euler}` (18 cases).
- Governance thresholds/claim criteria were **not changed**; phase-1 criteria status carried forward unchanged.

### Explicit pass/fail outputs
- Run matrix non-empty: **PASS**
- All cases completed: **PASS** (18/18)
- Deterministic anchor recheck (`dt=1e-3,rk4`) abs delta < 1e-14: **PASS**
- Phase-1 Spearman criterion status retained (>=0.95 from prior full-corridor eval): **PASS (unchanged)**
- Governance threshold mutation: **FAIL condition NOT triggered** (`false`)

### Stress deltas (vs anchor at each point)
- max rel delta Q1: `0.8552608860`
- max rel delta BoO slow: `0.8547657725`
- max rel delta BoO fast: `18.9667102063`

### Phase-2 interpretation
- Execution robustness and auditability criteria passed; no retries were needed, and retry path remains implemented/logged per case.
- Method-induced spread (Euler vs RK4) is large in this stress extension, so BoO diagnostics should remain exploratory and **not** be used to widen claim scope.

### Recommendation (broader BoO adoption)
- **NO-GO for broader adoption at this stage**.
- Keep BoO branch diagnostic-only and RK4-anchored pending a stricter method-harmonized extension.
