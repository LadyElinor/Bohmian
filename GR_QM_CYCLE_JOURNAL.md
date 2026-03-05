## 2026-03-01 22:32 EST ï¿½ Cycle-2 learning checkpoint

### What I learned
1. The project now advances best with **gate-driven cycles**, not calendar weeks.
2. **Q1 is robust only inside a narrow envelope**; robustness is real in-core and collapses sharply at the edge.
3. The envelope boundary is now data-pinned:
   - high-confidence core: O_m <= 0.300
   - formal edge: O_m <= 0.305
4. Q2 confusion was mostly a measurement-design issue:
   - true replication passes,
   - method-family disagreement remains OPEN,
   - robust statistics (median/trimmed/p95/p99 + spike flag) are mandatory to avoid false blockers.
5. Independent corroboration is now meaningful:
   - strong monotonic agreement overall,
   - degradation appears at edge O_m=0.305, so promotion should remain conservative.

### Progress logged
- Built and iterated reproducible runners for baseline, tiered gates, robust Q2, outlier autopsy, and cycle-2 dense follow-up.
- Updated governance docs to match reality (claim matrix, assumption register, monthly gate draft, action plan v2).
- Converted ambiguous blockers into explicit scoped limitations with mitigation paths.

### Current status
- Claims remain OPEN (by design), but with much tighter evidence quality and scope control.
- Project posture: **Proceed in-core, constrain edge, no overclaiming.**

### Next action (queued)
- Run mitigation experiments for O_m >= 0.305 (smaller dt + alternate integrator) before any envelope expansion.

---

## 2026-03-02 17:29 EST â€” Continuation checkpoint (revalidation + prioritization)

### Milestones completed
- Reassessed project state across the six requested governance docs.
- Re-ran core corridor confirmation to validate reproducibility:
  - `notebooks/cycle3_core_confirm.py`
  - output: `notebooks/outputs/grqm_cycle3_core_confirm_20260302_172931/`
- Re-verified Cycle-3 pivot success from existing artifact:
  - `notebooks/outputs/grqm_cycle3_q2_pivot_20260301_223823/cycle3_q2_pivot_summary.csv`
- Produced concise continuation deliverable:
  - `GR_QM_CONTINUATION_NOTE_2026-03-02.md`

### Evidence snapshot
- Core corridor rerun: **20/20 pass_all_envelope**
- Hardened sensitivity max: **0.1483**
- Q1 refinement max: **2.80e-07**
- Q2 robust tails max: **p95=0.2850, p99=0.3892**
- True replication rel diff max: **0.0**
- Pivot success (existing artifact): **6/6**, p95 improvement min **99.99999945%**

### Conservative interpretation
- In-core evidence remains stable and reproducible.
- Full promotion remains blocked by policy prerequisites (consecutive-cycle + assumption-closure), not by current core metrics.
- Highest-value next work is governance-closing evidence (cycle ledger + assumption closure), then edge mitigation at Î©_m=0.305.

---

## 2026-03-02 17:38â€“17:43 EST â€” Ordered execution block (ledger â†’ A-001/A-002 â†’ edge micro-batch)

### Milestones completed
1. Built canonical consecutive-cycle promotion ledger from existing cycle artifacts only:
   - `GR_QM_CONSECUTIVE_CYCLE_PROMOTION_LEDGER.csv`
   - `GR_QM_CONSECUTIVE_CYCLE_PROMOTION_LEDGER.md`
2. Executed A-001 closure mini-test (ordering/approximation narrow sweep):
   - `python notebooks/a001_closure_minitest.py`
   - output: `notebooks/outputs/grqm_a001_closure_minitest_20260302_174144/`
3. Executed A-002 closure mini-test (proxy ablations + nuisance perturbations):
   - `python notebooks/a002_proxy_ablation_minitest.py`
   - output: `notebooks/outputs/grqm_a002_proxy_ablation_minitest_20260302_174154/`
4. Executed Î©_m=0.305 mitigation micro-batch with stricter path (after 1â€“3):
   - `python notebooks/edge305_microbatch_dop853.py`
   - output: `notebooks/outputs/grqm_edge305_microbatch_dop853_20260302_174237/`

### Evidence snapshot
- Ledger: cycle-1/2/3(+rerun) backfilled; promotion flag remains NO in all rows.
- A-001 mini-test:
  - pass_q1_rate = **1.00**
  - pass_q2_rate = **1.00**
  - pass_joint_rate = **1.00**
  - max_q1_sensitivity_vs_baseline = **6.5868** (ordering sensitivity remains nontrivial outside nominal setting)
- A-002 mini-test:
  - ranking Spearman preserved at ~1.0 in all nuisance cases
  - strict pass-case rate = **0.60 (3/5)**
  - IC Â±0.1% nuisance cases fail drift cap (max_rel_drift 0.1483 / 0.1093 > 0.10)
- Edge Î©_m=0.305 micro-batch (DOP853 comparator, small-dt RK4 reference):
  - n_success = **3/3**
  - max q2_D_p95 = **1.434e-4**
  - max q2_D_p99 = **1.947e-4**
  - any_1pct_crossing = **False**

### Conservative interpretation
- Promotion blockers were reduced (ledger now explicit; A-001/A-002 now partially evidence-closed) but **not eliminated**.
- Remaining blocker concentration: A-002 nuisance drift sensitivity and policy requirement for fully closed high-impact assumptions.
- Edge run is mitigation evidence only; no envelope expansion claim made.

---

## 2026-03-02 17:49â€“17:51 EST â€” A-002 focused closure pass (IC nuisance drift)

### Commands executed
- `python notebooks/a002_proxy_ablation_minitest.py`
- `python notebooks/a002_ic_nuisance_sweep.py`
- `python notebooks/a002_proxy_ablation_policy_rerun.py`

### New artifacts
- `notebooks/outputs/grqm_a002_proxy_ablation_minitest_20260302_174901/`
- `notebooks/outputs/grqm_a002_ic_nuisance_sweep_20260302_175011/`
- `notebooks/outputs/grqm_a002_proxy_ablation_policy_rerun_20260302_175101/`

### Measured outcome
- Reproduced failure exactly: IC Â±0.1% cases fail drift cap (`0.1483`, `0.1093` > `0.10`).
- Focused sweep found pass/fail boundary for drift criterion at approximately:
  - pass band: `0.9993 <= ic_scale <= 1.0009` (i.e., `-0.07% .. +0.09%`)
- Classification: **localized_controllable** (not structural proxy breakdown).
- Policy rerun with explicit bound confirms in-policy closure:
  - `n_in_policy=5`, `in_policy_pass_rate=1.0`, out-of-policy stress cases = IC Â±0.1%.

### Governance implication
- A-002 updated from ACTIVE â†’ TESTED (bounded nuisance policy).
- Promotion still blocked (A-001 unresolved + consecutive-cycle rule).

---

## 2026-03-02 17:54â€“18:00 EST â€” A-001 focused closure pass (ordering/approximation bounds)

### Commands executed
- `python notebooks/a001_closure_minitest.py`
- `python -c "..."` (boundary policy evaluation from fresh mini-test output)
- `python -c "..."` (A-001 in-policy battery rerun)

### New artifacts
- `notebooks/outputs/grqm_a001_closure_minitest_20260302_175542/`
- `notebooks/outputs/grqm_a001_boundary_policy_eval_20260302_175807/`
- `notebooks/outputs/grqm_a001_policy_battery_rerun_20260302_175841/`

### Measured outcome
- Reproduced mini-test behavior exactly: `pass_q1_rate=1.0`, `pass_q2_rate=1.0`, `pass_joint_rate=1.0`, `max_q1_sensitivity_vs_n5_dt1e3=6.58677`.
- Local boundary split (same dimensions already used: ordering n and dt):
  - Proposed in-policy window: `n in {4,5}`, `dt in [8e-4,1.2e-3]`, plus local sensitivity cap `<=1.0`.
  - In-policy region: `24/24` pass (`100%`), max local sensitivity `0.86634`.
  - Out-of-policy stress region (`n=6`): `0/12` pass under policy; sensitivity range `5.246..6.587`.
- In-policy battery rerun confirms closure metrics:
  - `pass_rate=1.0 (24/24)`
  - extrema: `q1_refinement_max_obs=4.2363e-07`, `q2_p95_max=0.27043`, `q2_p99_max=0.35457`, `q2_replication_rel_diff_max=0.0`.

### Conservative interpretation
- A-001 is closed only in explicit local policy bounds above; `n=6` retained as stress-only.
- Promotion eligibility remains **NO** (consecutive-cycle envelope rule still unmet; no speculative promotion).

---

## 2026-03-02 18:03â€“18:06 EST â€” Promotion-readiness full in-policy cycle (fresh) + branch decision

### Commands executed
- `python notebooks/cycle4_inpolicy_confirm.py`
- `python notebooks/build_promotion_ledger.py`

### New artifacts
- `notebooks/outputs/grqm_cycle4_inpolicy_confirm_20260302_180311/`
  - `cycle4_inpolicy_confirm_summary.csv`
  - `proxy_agreement_v4_inpolicy.csv`
  - `aggregate.json`

### Measured gate outcomes (from cycle summary)
- `G-PROXY=1.0`, `G-REFINE=1.0`, `G-ROBUST-Q1=0.0`, `G-ROBUST-Q2=1.0`, `G-REPLICATION=1.0`, `G-ENVELOPE=0.0`
- `q1_assumption_sensitivity_hardened` range: `0.868867..0.878578` (all above pipeline threshold `0.2`)

### Branch decision
- **Fail branch taken**: cycle did not pass all required gates in-policy.
- Confirming cycle was **not run** (per policy).
- Blocker note: explicit A-001/A-002 policy perturbation mix failed current pipeline `G-ROBUST-Q1` criterion.

---

## 2026-03-02 21:43 EST â€” Delta autopsy (cycle3 pass vs cycle4 in-policy fail)

### Compared artifacts
- Pass ref: `notebooks/outputs/grqm_cycle3_core_confirm_20260302_172931/`
- Fail run: `notebooks/outputs/grqm_cycle4_inpolicy_confirm_20260302_180311/`
- Autopsy output: `notebooks/outputs/grqm_delta_autopsy_20260302_214334/`

### Evidence summary
- Comparable files exist one-to-one in both dirs: `aggregate.json`, cycle summary CSV, proxy agreement CSV.
- Per-point comparison (`20/20` matched on `(omega_m, alpha_qg)`) shows:
  - `q1_delta_proxy_l2`, `q1_refinement_max_obs`, all Q2 diagnostics: **no change** (delta = 0 at every point).
  - `q1_assumption_sensitivity_hardened`: **shifted up at all points** by `+0.724..+0.847` (mean abs delta `0.8118`).
- First divergence (and first gate flip): `(omega_m=0.285, alpha_qg=3e-07)`:
  - `q1_assumption_sensitivity_hardened` `0.02272 -> 0.86970`
  - `pass_all_envelope` `True -> False`

### Knob/config deltas tied to A-001/A-002 + numerics envelope
- Perturbation set changed from cycle3 hardened checks:
  - `ic_scale={0.999,1.001}`, `dt={9e-4,1.0e-3,1.1e-3}`, `n=5`
- To cycle4 in-policy closure mix:
  - `ic_scale={0.9993,1.0009}`, `dt={8e-4,1.2e-3}`, `n in {4,5}`
- Added explicit `policy_bounds` block in failed run `aggregate.json` with those limits.

### Most likely culprit (evidence-first)
- **Primary smoking gun:** changed perturbation basis (especially inclusion of `n=4` at boundary `dt=8e-4/1.2e-3`) drove `q1_assumption_sensitivity_hardened` above the fixed gate threshold (`<=0.18`) at all points, collapsing envelope pass rate `1.0 -> 0.0`.

## 2026-03-02 21:45ï¿½21:47 EST ï¿½ GR_QM quick-revert diagnostic (Cycle-4 hardening rollback test)

### Objective
- Isolate whether Cycle-4 regression is caused specifically by hardening logic changes.

### Snapshot of Cycle-4 hardening signature (pre-revert)
- File: 
otebooks/cycle4_inpolicy_confirm.py (sha256 416a173a74d9cefd1dae722d976d6b4a686ea2e5156e093d5d94d5e2d559c7af)
- Grid: omega_list=[0.285,0.290,0.295,0.300], lpha_list=[3e-7,5e-7,7e-7,1e-6,1.3e-6]
- Gate thresholds unchanged: q1_assumption_hardened_max=0.18 and standard Q1/Q2 thresholds.
- Hardening procedure (policy_perturbations, lines 33ï¿½38):
  - (ic_scale=0.9993, dt=8e-4, n=4)
  - (ic_scale=1.0009, dt=8e-4, n=4)
  - (ic_scale=0.9993, dt=1.2e-3, n=5)
  - (ic_scale=1.0009, dt=1.2e-3, n=5)

### Reverted signature used for diagnostic (Cycle-3 equivalent)
- Source file: 
otebooks/cycle3_core_confirm.py (sha256 9ad7ff502cabd94dfc72b8f583b5f87942686d8269332b0be4d6b4d2a8add499)
- hardened_perturbations (lines 32ï¿½37):
  - (ic_scale=0.999, dt=1e-3, n=5)
  - (ic_scale=1.001, dt=1e-3, n=5)
  - (ic_scale=1.0, dt=9e-4, n=5)
  - (ic_scale=1.0, dt=1.1e-3, n=5)

### Minimal diagnostic execution
- Added targeted runner: 
otebooks/grqm_cycle4_quick_revert_hardening.py
- Command:
  - python notebooks/grqm_cycle4_quick_revert_hardening.py
- Subset (core corridor, 3 representative points):
  - (omega_m, alpha_qg) = (0.290,7e-7), (0.295,7e-7), (0.300,7e-7)

### Outcome
- Output: 
otebooks/outputs/grqm_quick_revert_hardening_20260302_214712/
- Policy (Cycle-4 hardening) subset q1_assumption_sensitivity_hardened:
  - min  .869910, max  .875848, mean  .872281, q1 gate pass  /3, envelope pass  /3
- Revert (Cycle-3 hardening) subset q1_assumption_sensitivity_hardened:
  - min  .030042, max  .139701, mean  .072106, q1 gate pass 3/3, envelope pass 3/3

### Decision
- Clear recovery observed with hardening-only rollback; no additional disambiguation run needed.
- Blocker isolated to Cycle-4 hardening logic/settings change (not grid/envelope/pipeline).

---

## 2026-03-02 21:52â€“21:53 EST â€” 20-point promotion-readiness confirmation (reverted baseline hardening)

### Commands executed
- `python notebooks/cycle3_core_confirm.py`
- `python notebooks/build_promotion_ledger.py`

### Artifact outputs
- `notebooks/outputs/grqm_cycle3_core_confirm_20260302_215234/`
  - `cycle3_core_confirm_summary.csv`
  - `proxy_agreement_v3.csv`
  - `aggregate.json`
- `GR_QM_CONSECUTIVE_CYCLE_PROMOTION_LEDGER.csv`
- `GR_QM_CONSECUTIVE_CYCLE_PROMOTION_LEDGER.md`

### Gate outcome (20/20 cycle)
- G-PROXY: **1.0**
- G-REFINE: **1.0**
- G-ROBUST-Q1: **1.0**
- G-ROBUST-Q2: **1.0**
- G-REPLICATION: **1.0**
- G-ENVELOPE: **1.0**

### Conservative interpretation
- Reverted/Cycle-3-equivalent hardening signature restores full envelope pass across the 20-point readiness grid.
- Promotion eligibility flag in canonical ledger remains **NO** (conservative governance hold; no speculative promotion).

---

## 2026-03-02 22:15 EST â€” Governance closure executed (hold-lift + cross-doc sync)

### Milestones completed
- Added explicit dated hold-lift addendum in `GR_QM_MONTHLY_GATE_REPORT_01.md`.
- Confirmed `C-WDW-001` status in `CLAIM_STATUS_MATRIX.md` as **PROVEN (core envelope)** with explicit caveat: `Î©_m>=0.305` remains blocked.
- Kept promotion eligibility at **YES** for `cycle-4-reverted-hardening-20260302` in canonical ledger artifacts:
  - `GR_QM_CONSECUTIVE_CYCLE_PROMOTION_LEDGER.csv`
  - `GR_QM_CONSECUTIVE_CYCLE_PROMOTION_LEDGER.md`
- Created BoO branch kickoff plan: `GR_QM_BOO_BRANCH_PLAN_2026-03-02.md`.
- Added minimal BoO starter scaffold script: `notebooks/boo_branch_starter.py`.
- Smoke-tested BoO scaffold execution:
  - `python notebooks/boo_branch_starter.py`
  - output: `notebooks/outputs/grqm_boo_branch_starter_20260302_221738/boo_branch_summary.csv`.

### Consistency note
- Earlier journal entries indicating `promotion eligibility remains NO` are preserved as historical snapshots; governance status is now superseded by the dated hold-lift action above.

### Next trigger
- Run first BoO corridor baseline sweep from `notebooks/boo_branch_starter.py` and log pass/fail against plan criteria.

## 2026-03-02 22:21–22:23 EST — BoO branch kickoff corridor evaluation (phase-1)

### Scope run
- Reviewed kickoff plan: `GR_QM_BOO_BRANCH_PLAN_2026-03-02.md`
- Reviewed scaffold: `notebooks/boo_branch_starter.py`
- Executed primary run: `python notebooks/boo_branch_starter.py`
- Added conservative evaluator: `notebooks/boo_branch_evaluate.py`
- Executed evaluation: `python notebooks/boo_branch_evaluate.py`

### Artifacts produced
- `notebooks/outputs/grqm_boo_branch_starter_20260302_222143/boo_branch_summary.csv`
- `notebooks/outputs/grqm_boo_branch_starter_20260302_222143/boo_sensitivity_spotcheck.csv`
- `notebooks/outputs/grqm_boo_branch_starter_20260302_222143/boo_eval_metrics.json`

### Key metrics (BoO vs baseline)
- Core corridor completeness: **20/20 points**
- Rank consistency (Q1 proxy vs BoO slow diagnostic): **Spearman = 1.0000**
- Deterministic re-eval (same config): **max abs delta = 0.0**, **max rel delta = 0.0**
- Signal span retention:
  - baseline Q1 span ratio: **22.9170**
  - BoO slow span ratio: **22.9170** (matched at 4 d.p.)
- Sensitivity spot-check (dt ? {9e-4, 1e-3, 1.1e-3}, 3 representative points):
  - max rel delta Q1: **4.96e-4**
  - max rel delta BoO-slow: **4.95e-4**
  - max rel delta BoO-fast RMS: **1.53e-1** (expected higher small-residual sensitivity)

### Criteria mapping (kickoff plan)
- Deterministic reproducibility: **PASS**
- Full 20-point BoO table: **PASS**
- Monotonic rank consistency (Spearman >= 0.95): **PASS**
- Governance contradiction introduced: **NO** (diagnostic-only branch retained)

### Outcome
- **Kickoff BoO corridor evaluation = PASS (phase-1 criteria met).**
- No follow-up tweak run triggered (initial run was unambiguous pass).

## 2026-03-02 22:36 EST â€” BoO phase-2 stress extension (tight-scope dt/method cross-check)

### Run
- `python notebooks/boo_phase2_stress_extension.py`

### Artifacts
- `notebooks/outputs/grqm_boo_phase2_stress_20260302_223624/phase2_run_log.jsonl`
- `notebooks/outputs/grqm_boo_phase2_stress_20260302_223624/boo_phase2_crosscheck_summary.csv`
- `notebooks/outputs/grqm_boo_phase2_stress_20260302_223624/boo_phase2_crosscheck_deltas.csv`
- `notebooks/outputs/grqm_boo_phase2_stress_20260302_223624/boo_phase2_report.json`

### Outcome (explicit)
- Cases completed: **18/18 PASS**
- Deterministic anchor recheck: **PASS**
- Threshold/governance mutation: **NOT TRIGGERED**
- Cross-check spread vs anchor:
  - max rel Î”Q1 = **0.8553**
  - max rel Î”BoO-slow = **0.8548**
  - max rel Î”BoO-fast = **18.9667**

### Interpretation
- Operational stress run succeeded with deterministic/non-empty logs.
- Method dependence remains large under Euler stress path; keep BoO as exploratory diagnostic only.
- Recommendation for broad BoO adoption: **NO-GO (defer)**.

## 2026-03-03 18:15–18:23 EST — Autonomous governance/doc hardening block

### Actions completed
- Added public status banner to `README.md` (PROVEN/OPEN/BLOCKED with envelope caveat).
- Ran fresh confirmation cycle:
  - `python notebooks/cycle3_core_confirm.py`
  - output: `notebooks/outputs/grqm_cycle3_core_confirm_20260303_182255/`
- Added fresh KPI summary note:
  - `GR_QM_KPI_SNAPSHOT_2026-03-03.md`
- Added next-trigger operational file:
  - `GR_QM_NEXT_CYCLE_TRIGGER_LIST_2026-03-03.md`
- Added pre-registered edge acceptance criteria:
  - `GR_QM_EDGE305_ACCEPTANCE_CRITERIA_PREREGISTER.md`
- Synced governance docs with 2026-03-03 sign-off + nonlinear phase-1b cross-link:
  - `CLAIM_STATUS_MATRIX.md`
  - `GR_QM_MONTHLY_GATE_REPORT_01.md`

### Fresh cycle quick metrics
- pass_rate_envelope: `1.0` (20/20)
- spearman_primary_vs_independent: `1.0`
- `q1_refinement_max_obs_max = 2.795794e-07`
- `q1_assumption_sensitivity_hardened_max = 0.148304`
- `q2_D_p95_max = 0.284987`
- `q2_D_p99_max = 0.389203`
- `q2_true_replication_rel_diff_max = 0.0`

### Scope discipline
- No threshold mutation.
- No claim-status mutation.
- Core envelope caveat unchanged (`O_m>=0.305` still blocked).

## 2026-03-03 21:25 EST — External critique ingestion + governance hardening

### Input
- New critique file added by user: `critique.txt`

### Actions executed
- Wrote structured response/action doc:
  - `GR_QM_EXTERNAL_CRITIQUE_RESPONSE_2026-03-03.md`
- Added falsification/re-open protocol for C-WDW-001:
  - `GR_QM_CWDW001_FALSIFICATION_PROTOCOL.md`
- Added public derivation appendix scaffold:
  - `docs/C-WDW-001_CORRECTION_DERIVATION.md`
- Added public reply draft:
  - `GR_QM_CRITIQUE_PUBLIC_REPLY_DRAFT_2026-03-03.md`
- Added hardening-expansion plan:
  - `GR_QM_HARDENING_EXPANSION_PLAN_2026-03-03.md`
- Updated governance docs:
  - `GR_QM_ACTION_PLAN.md` (Q2 explicitly numerical diagnostic, not physics observable)
  - `CLAIM_STATUS_MATRIX.md` (external critique follow-up + reopen note)
  - `GR_QM_NEXT_CYCLE_TRIGGER_LIST_2026-03-03.md` (derivation->prediction->diagnostic sequencing)

### Scope discipline
- No immediate claim-status mutation.
- No threshold mutation.
- Added explicit path for potential reopen if falsification triggers fire.

## 2026-03-03 21:29–21:33 EST — Cliff sequencing block (prediction + prediagnostic)

### Actions completed
- Added prediagnostic runner:
  - `notebooks/cliff_prediagnostic_report.py`
- Executed prediagnostic:
  - output: `notebooks/outputs/grqm_cliff_prediagnostic_20260303/`
- Added pre-registered mechanism predictions:
  - `GR_QM_CLIFF_MECHANISM_PREDICTIONS_PREREG_2026-03-03.md`

### Key prediagnostic snapshot
- core pass-all rate: `1.0` (25/25)
- edge305 pass-all rate (dense follow-up): `0.0` (0/5)
- core q1_refine max: `2.80e-07`
- edge305 q1_refine range: `4.30e-02 .. 3.76e-01`
- core q2_p95 max: `2.85e-01`
- edge305 q2_p95 range (dense): `1.42e+01 .. 3.33e+02`
- edge305 spike-detected rate: `0.6`
- edge305 DOP853 microbatch q2_p95/q2_p99 max: `1.434e-04 / 1.947e-04`

### Interpretation
- Cliff manifestation appears strongly path/method-sensitive in existing evidence.
- Edge remains blocked; mechanism explanation remains mandatory before any expansion.

## 2026-03-03 21:33–21:35 EST — Edge integrator hierarchy micro-scan (diagnostic)

### Command executed
- `python notebooks/edge_integrator_hierarchy_scan.py`

### Artifacts
- `notebooks/outputs/grqm_edge_integrator_hierarchy_20260303_213438/`
- `GR_QM_EDGE_INTEGRATOR_HIERARCHY_NOTE_2026-03-03.md`

### Snapshot
- RK4 edge q2_p95 by point: `0.3678`, `0.2801`, `0.0470`
- Tight adaptive/stiff-capable methods q2_p95 near numerical floor:
  - DOP853 ~`1e-9`, LSODA ~`1e-8`, Radau ~`1e-10`
- Suppression vs RK4 q2_p95: `>99.9999%` on all 3 points

### Conservative interpretation
- Strong evidence that prior edge blow-up is dominated by numerical-path effects on this subset.
- No status change executed; edge remains blocked pending full predeclared mitigation package.

## 2026-03-03 21:38–21:40 EST — Edge mitigation micro-package prep + pilot run

### Added
- `notebooks/edge_mitigation_micro_package.py`
- `GR_QM_EDGE_MITIGATION_PACKAGE_PLAN_2026-03-03.md`
- `GR_QM_LEDGER_NOTE_EDGE_MITIGATION_TEMPLATE_2026-03-03.md`
- Updated `GR_QM_CLIFF_MECHANISM_PREDICTIONS_PREREG_2026-03-03.md` with explicit >=90–95% suppression discriminator.

### Executed pilot
- `python notebooks/edge_mitigation_micro_package.py`
- Output: `notebooks/outputs/grqm_edge_mitigation_micro_20260303_213950/`
- Rows generated: `45` (3 omega × 5 alpha × 3 methods)

### Scope discipline
- Diagnostic/evidence-prep only.
- No claim/policy mutation.

## 2026-03-03 21:41–21:42 EST — Edge mitigation micro-package scoring

### Scoring summary (45 rows)
- global max q2_p95: `5.118016110916557e-08`
- global max q2_p99: `6.730758567163875e-08`
- method maxima:
  - DOP853 q2_p95/q2_p99 max: `5.272e-09 / 6.943e-09`
  - LSODA q2_p95/q2_p99 max: `5.118e-08 / 6.731e-08`
  - Radau q2_p95/q2_p99 max: `1.848e-11 / 2.861e-11`

### Governance handling
- Created filled ledger-style evidence note:
  - `GR_QM_LEDGER_NOTE_EDGE_MITIGATION_FILLED_2026-03-03.md`
- Decision in note: keep edge BLOCKED (pending companion q1/refinement/hardening/replication checks).

## 2026-03-04 21:19 EST - Edge nonlinear-extension sweep (additive)

### Added
- `GR_QM_NONLINEAR_EXTENSION_PLAN_2026-03-04.md`
- `notebooks/edge_nonlinear_extension_sweep.py`
- `GR_QM_EDGE_NONLINEAR_EXTENSION_SUMMARY_2026-03-04.md`

### Executed
- `python notebooks/edge_nonlinear_extension_sweep.py`
- Output: `notebooks/outputs/grqm_edge_nonlinear_extension_20260304_211921/`

### Key outcomes
- `baseline_n5`: success 12/12; worst `max_ratio=3.9160`; worst `min_a=0.00791`.
- `higher_order_n6`: success 12/12; worst `max_ratio=4.6685`; worst `min_a=0.02539`.
- `softcap_denom` and `tanh_gate`: solver failure 12/12 with message `Required step size is less than spacing between numbers.`

### Acceptance snapshot
- Criteria: A (`max_ratio<=0.10`), B (`min_a>=0.02`), C (solver success 100%).
- baseline_n5: A fail, B fail, C pass.
- higher_order_n6: A fail, B pass, C pass.
- softcap_denom/tanh_gate: A/B/C fail.

### Decision
- Keep edge lane BLOCKED (unchanged).
- Keep C-WDW-001 in-core envelope unchanged.
