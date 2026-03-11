# GR_QM Session Note — 2026-03-02

## Scope executed (in required order)
1. Built consecutive-cycle promotion ledger.
2. Ran A-001 and A-002 assumption-closure mini-tests.
3. Ran small Ω_m=0.305 edge mitigation micro-batch (small-dt + DOP853 comparator).

## Evidence produced
- Ledger (canonical):
  - `GR_QM_CONSECUTIVE_CYCLE_PROMOTION_LEDGER.csv`
  - `GR_QM_CONSECUTIVE_CYCLE_PROMOTION_LEDGER.md`
- A-001 mini-test:
  - `notebooks/outputs/grqm_a001_closure_minitest_20260302_174144/`
  - joint criteria pass: 36/36
  - note: max ordering/approx sensitivity vs baseline remains high (6.5868)
- A-002 mini-test:
  - `notebooks/outputs/grqm_a002_proxy_ablation_minitest_20260302_174154/`
  - pass-case rate: 3/5
  - failures localized to IC ±0.1% nuisance drift cap exceedance (0.1483, 0.1093)
- Ω_m=0.305 edge micro-batch:
  - `notebooks/outputs/grqm_edge305_microbatch_dop853_20260302_174237/`
  - q2 tails very small (max p95 1.434e-4, max p99 1.947e-4), no 1% crossing

## Blockers resolved / unresolved
- Resolved (partially):
  - Promotion ledger blocker is now explicit and auditable across consecutive cycles.
  - A-001 now has direct closure evidence in narrow in-core sweep.
- Unresolved:
  - A-002 not fully closed due nuisance drift sensitivity under IC perturbations.
  - Full promotion still blocked by unresolved high-impact assumptions (A-001/A-002 policy state still ACTIVE in register) and non-consecutive all-gate sequence including cycle-2 envelope misses.

## Update at 22:15 EST (governance closure pass)
### What changed
- Governance hold-lift was executed and documented in `GR_QM_MONTHLY_GATE_REPORT_01.md` (date-stamped addendum).
- `CLAIM_STATUS_MATRIX.md` now explicitly reflects closed governance posture for `C-WDW-001` as **PROVEN (core envelope)** with caveat that `Ω_m>=0.305` remains blocked.
- Promotion ledger remains aligned with hold-lift completion (`YES` eligibility for `cycle-4-reverted-hardening-20260302` in both `.csv` and `.md`).
- BoO kickoff artifacts prepared:
  - `GR_QM_BOO_BRANCH_PLAN_2026-03-02.md`
  - `notebooks/boo_branch_starter.py`

### Next trigger
Run `python notebooks/boo_branch_starter.py` to generate the first BoO corridor baseline table, then evaluate against success/failure criteria in `GR_QM_BOO_BRANCH_PLAN_2026-03-02.md`.

## Update at 22:23 EST (BoO kickoff corridor evaluation complete)
### Commands executed
- `python notebooks/boo_branch_starter.py`
- `python notebooks/boo_branch_evaluate.py`

### Artifacts
- `notebooks/outputs/grqm_boo_branch_starter_20260302_222143/boo_branch_summary.csv`
- `notebooks/outputs/grqm_boo_branch_starter_20260302_222143/boo_sensitivity_spotcheck.csv`
- `notebooks/outputs/grqm_boo_branch_starter_20260302_222143/boo_eval_metrics.json`

### Assessment vs `GR_QM_BOO_BRANCH_PLAN_2026-03-02.md`
- Deterministic rerun reproducibility: **PASS** (max abs/rel delta = 0.0)
- 20-point core corridor completion: **PASS**
- Rank consistency criterion (Spearman >= 0.95): **PASS** (1.000)
- Failure criteria (Spearman < 0.8 / unstable outputs): **NOT MET**

### Interpretation
- BoO slow diagnostic preserves baseline signal ordering and span while remaining deterministic.
- dt sensitivity is small for baseline and BoO-slow metrics (~5e-4 max rel change in spot-check); BoO-fast residual is more dt-sensitive (~0.153 max rel), but remains secondary diagnostic.
- No governance contradiction introduced; branch remains exploratory/diagnostic.

### Next trigger
Advance to BoO phase-2 only if requested: expand sensitivity/replication stress check (additional dt/method cross-check) while keeping in-core scope and no policy changes.

## Update at 22:36 EST (BoO phase-2 stress extension complete)
### Command executed
- `python notebooks/boo_phase2_stress_extension.py`

### Artifacts
- `notebooks/outputs/grqm_boo_phase2_stress_20260302_223624/phase2_run_log.jsonl`
- `notebooks/outputs/grqm_boo_phase2_stress_20260302_223624/boo_phase2_crosscheck_summary.csv`
- `notebooks/outputs/grqm_boo_phase2_stress_20260302_223624/boo_phase2_crosscheck_deltas.csv`
- `notebooks/outputs/grqm_boo_phase2_stress_20260302_223624/boo_phase2_report.json`

### Criteria outcomes (explicit)
- Non-empty auditable outputs: **PASS**
- 18-case subset matrix completion: **PASS**
- Deterministic anchor rerun check: **PASS**
- Phase-1 thresholds/governance criteria modified: **NO**
- Run-step failure/retry events: **none triggered**

### Stress metrics
- max rel ΔQ1 vs anchor: **0.8552608860**
- max rel ΔBoO-slow vs anchor: **0.8547657725**
- max rel ΔBoO-fast vs anchor: **18.9667102063**

### Recommendation
- **NO-GO** for broader BoO adoption right now.
- Keep BoO diagnostic-only (no claim-scope expansion, no gate-threshold changes).
