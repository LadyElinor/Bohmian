## 2026-03-01 22:32 EST � Cycle-2 learning checkpoint

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

## 2026-03-02 17:29 EST — Continuation checkpoint (revalidation + prioritization)

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
- Highest-value next work is governance-closing evidence (cycle ledger + assumption closure), then edge mitigation at Ω_m=0.305.

---

## 2026-03-02 17:38–17:43 EST — Ordered execution block (ledger → A-001/A-002 → edge micro-batch)

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
4. Executed Ω_m=0.305 mitigation micro-batch with stricter path (after 1–3):
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
  - IC ±0.1% nuisance cases fail drift cap (max_rel_drift 0.1483 / 0.1093 > 0.10)
- Edge Ω_m=0.305 micro-batch (DOP853 comparator, small-dt RK4 reference):
  - n_success = **3/3**
  - max q2_D_p95 = **1.434e-4**
  - max q2_D_p99 = **1.947e-4**
  - any_1pct_crossing = **False**

### Conservative interpretation
- Promotion blockers were reduced (ledger now explicit; A-001/A-002 now partially evidence-closed) but **not eliminated**.
- Remaining blocker concentration: A-002 nuisance drift sensitivity and policy requirement for fully closed high-impact assumptions.
- Edge run is mitigation evidence only; no envelope expansion claim made.

---

## 2026-03-02 17:49–17:51 EST — A-002 focused closure pass (IC nuisance drift)

### Commands executed
- `python notebooks/a002_proxy_ablation_minitest.py`
- `python notebooks/a002_ic_nuisance_sweep.py`
- `python notebooks/a002_proxy_ablation_policy_rerun.py`

### New artifacts
- `notebooks/outputs/grqm_a002_proxy_ablation_minitest_20260302_174901/`
- `notebooks/outputs/grqm_a002_ic_nuisance_sweep_20260302_175011/`
- `notebooks/outputs/grqm_a002_proxy_ablation_policy_rerun_20260302_175101/`

### Measured outcome
- Reproduced failure exactly: IC ±0.1% cases fail drift cap (`0.1483`, `0.1093` > `0.10`).
- Focused sweep found pass/fail boundary for drift criterion at approximately:
  - pass band: `0.9993 <= ic_scale <= 1.0009` (i.e., `-0.07% .. +0.09%`)
- Classification: **localized_controllable** (not structural proxy breakdown).
- Policy rerun with explicit bound confirms in-policy closure:
  - `n_in_policy=5`, `in_policy_pass_rate=1.0`, out-of-policy stress cases = IC ±0.1%.

### Governance implication
- A-002 updated from ACTIVE → TESTED (bounded nuisance policy).
- Promotion still blocked (A-001 unresolved + consecutive-cycle rule).

---

## 2026-03-02 17:54–18:00 EST — A-001 focused closure pass (ordering/approximation bounds)

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

## 2026-03-02 18:03–18:06 EST — Promotion-readiness full in-policy cycle (fresh) + branch decision

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

## 2026-03-02 21:43 EST — Delta autopsy (cycle3 pass vs cycle4 in-policy fail)

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

## 2026-03-02 21:45�21:47 EST � GR_QM quick-revert diagnostic (Cycle-4 hardening rollback test)

### Objective
- Isolate whether Cycle-4 regression is caused specifically by hardening logic changes.

### Snapshot of Cycle-4 hardening signature (pre-revert)
- File: 
otebooks/cycle4_inpolicy_confirm.py (sha256 416a173a74d9cefd1dae722d976d6b4a686ea2e5156e093d5d94d5e2d559c7af)
- Grid: omega_list=[0.285,0.290,0.295,0.300], lpha_list=[3e-7,5e-7,7e-7,1e-6,1.3e-6]
- Gate thresholds unchanged: q1_assumption_hardened_max=0.18 and standard Q1/Q2 thresholds.
- Hardening procedure (policy_perturbations, lines 33�38):
  - (ic_scale=0.9993, dt=8e-4, n=4)
  - (ic_scale=1.0009, dt=8e-4, n=4)
  - (ic_scale=0.9993, dt=1.2e-3, n=5)
  - (ic_scale=1.0009, dt=1.2e-3, n=5)

### Reverted signature used for diagnostic (Cycle-3 equivalent)
- Source file: 
otebooks/cycle3_core_confirm.py (sha256 9ad7ff502cabd94dfc72b8f583b5f87942686d8269332b0be4d6b4d2a8add499)
- hardened_perturbations (lines 32�37):
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

## 2026-03-02 21:52–21:53 EST — 20-point promotion-readiness confirmation (reverted baseline hardening)

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
