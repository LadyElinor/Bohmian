# GR_QM Monthly Gate Report 01 (Draft)

Date: 2026-03-01  
Cycle: first runnable GR↔QM toy-model testability loop (closed under gate-driven v2 plan)

---

## 1) Cycle objective

Execute an auditable end-to-end loop from question lock → runnable simulation → uncertainty accounting → replication/method checks → governance updates.

Status: **Completed**.

---

## 2) Canonical Cycle-1 close artifacts

Primary close artifact (unified tiered + robust columns):
- `notebooks/outputs/grqm_batch_tiered_20260301_193522/summary.csv`

Supporting artifacts:
- `Q1_Q2_GATE_UPDATE.md`
- `notebooks/outputs/grqm_q2_calibration_extended_20260301_192247/summary.csv`
- `notebooks/outputs/grqm_q2_calibration_robust_20260301_193233/summary.csv`
- `notebooks/outputs/grqm_q2_outlier_autopsy_20260301_192904/summary.csv`
- Governance files updated:
  - `CLAIM_STATUS_MATRIX.md`
  - `RESEARCH_ASSUMPTION_REGISTER.md`
  - `GR_QM_ACTION_PLAN.md` (refactored to gate-driven v2)

---

## 3) Gate outcomes (v2 naming)

### G-PROXY
- Passed in current envelope.
- `q1_delta_proxy_l2` scales monotonically with α in corridor.

### G-REFINE
- Passed in corridor (`q1_refinement_max_obs ~ 2.8e-7`).

### G-ROBUST-Q1 (tiered)
- Hardened gate passed across corridor (`q1_assumption_sensitivity_hardened ~ 0.127–0.150`).
- Wide stress sensitivity remains high and is logged as out-of-envelope behavior.

### G-ROBUST-Q2
- Robust statistics now included directly in tiered summary:
  - `q2_D_median`, `q2_D_trimmed_mean`, `q2_D_p95`, `q2_D_p99`, `q2_spike_detected`.
- Outlier at α=1.5e-7 under Euler dt=1e-3 identified as localized spike pathology; robust bulk metrics remain normal.

### G-REPLICATION
- True like-vs-like replication passes (`q2_true_replication_rel_diff = 0.0` in deterministic reruns).

### G-ENVELOPE
- Envelope explicitly used and logged (Ω_m≈0.30 corridor; hardened perturbations; pathology-aware handling).

### G-PROMOTION
- Not yet eligible for OPEN→PROVEN (needs consecutive cycle pass + independent proxy corroboration).

---

## 4) Technical interpretation (conservative)

- Q1 is now **robust-in-envelope** (not globally robust).
- Q2 replication failure was resolved as a metric-design issue; remaining limitation is method-family disagreement plus localized Euler spike windows.
- RK reference hierarchy consistency is extremely strong (~1e-10), supporting reference stability.

---

## 5) Decision

### Proceed / Pivot / Pause
- **Proceed:** yes (inside declared envelope)
- **Pivot:** yes (continue reducing method-family dependence and extending envelope)
- **Pause:** no

---

## 6) Cycle-2 queued actions (aligned to v2 gates)

1. Extend envelope: Ω_m ∈ [0.28, 0.32], finer α grid in [2e-7, 2e-6].
2. Keep robust Q2 metrics as mandatory gate inputs.
3. Add independent proxy corroboration path for G-PROMOTION eligibility.
4. Re-evaluate gate outcomes for two-consecutive-cycle promotion logic.

---

## 7) Cycle-2 execution update (2026-03-01, autonomous run)

### New artifacts
- Envelope extension run:
  - `notebooks/outputs/grqm_cycle2_envelope_20260301_194432/summary.csv`
  - `notebooks/outputs/grqm_cycle2_envelope_20260301_194432/aggregate.json`
- Independent proxy corroboration run (alpha-doubling linearity check):
  - `notebooks/outputs/grqm_cycle2_proxycheck_20260301_194409/summary.csv`
  - `notebooks/outputs/grqm_cycle2_proxycheck_20260301_194409/aggregate.json`
- Dense follow-up run (recommended boundary pinning):
  - `notebooks/outputs/grqm_cycle2_dense_followup_20260301_215901/envelope_summary.csv`
  - `notebooks/outputs/grqm_cycle2_dense_followup_20260301_215901/omega_passrate.csv`
  - `notebooks/outputs/grqm_cycle2_dense_followup_20260301_215901/proxy_agreement.csv`
  - `notebooks/outputs/grqm_cycle2_dense_followup_20260301_215901/aggregate.json`

### Concrete results
- Initial envelope batch: **12 runs total**, **8/12 pass_all_envelope**; failures clustered at Ω_m=0.32.
- Dense follow-up: **35 runs total**, **25/35 pass** (71.4%).
- Sharp Ω_m boundary from `omega_passrate.csv`:
  - Ω_m = 0.280–0.300: **5/5 pass each**
  - Ω_m = 0.305 and 0.310: **0/5 pass each**
- Interpretation: current defensible envelope for this stack is **Ω_m <= 0.300**.

### Independent proxy (corroboration path)
- Primary vs independent proxy agreement (dense follow-up):
  - Pearson ≈ **0.935**
  - Spearman ≈ **0.993**
- Alpha-doubling ratio `q1_delta(2α)/q1_delta(α)`:
  - mean ≈ **1.889**, median ≈ **1.981**, min ≈ **0.976**, max ≈ **3.054**
- Interpretation: strong monotonic corroboration with non-uniform tail behavior outside stable core.

### Gate interpretation
- G-ROBUST-Q2 remains mandatory and useful; broad-tail degradation appears in failing Ω_m slices.
- G-ENVELOPE now explicitly tightened to **Ω_m <= 0.300** under current dt/method stack.
- G-PROMOTION still unmet (needs second consecutive cycle pass plus tighter corroboration tails).

### Blockers / next hardening moves
1. Probe Ω_m >= 0.305 with smaller dt and alternate integrator before any envelope expansion.
2. Keep robust Q2 tail metrics mandatory in all cycle summaries.
3. Keep claim status OPEN until two consecutive in-envelope cycles pass with corroboration stability.

---

## 8) Boundary fit + edge corroboration confirmation

Additional follow-up artifacts:
- `notebooks/outputs/grqm_cycle2_boundarycheck_20260301_222955/boundary_fit.json`
- `notebooks/outputs/grqm_cycle2_edge305_proxycheck_20260301_223008/aggregate.json`

Results:
- Hardened-sensitivity boundary interpolation (`sens=0.2`) gives **Ω_m ≈ 0.30003**.
- Working envelope convention now formalized as:
  - **formal edge:** Ω_m <= 0.305
  - **high-confidence core corridor:** Ω_m <= 0.300
- Independent proxy at Ω_m=0.305 degrades vs core corridor:
  - Pearson ≈ 0.855
  - ratio mean ≈ 1.636, std ≈ 0.518, range ≈ [1.009, 2.235]

Interpretation:
- Boundary remains sharp and data-consistent.
- Core corridor corroboration is strong; edge corridor still unstable and not promotable without mitigation.

---

## 9) Cycle-3 execution update (2026-03-01 late run; core confirmation + Q2 pivot)

### Executed scripts
- `notebooks/cycle3_core_confirm.py`
- `notebooks/cycle3_q2_pivot.py` (patched to handle `t_first_1pct=None` safely when no 1% crossing occurs)

### New Cycle-3 artifacts
- Core confirmation batch:
  - `notebooks/outputs/grqm_cycle3_core_confirm_20260301_223742/cycle3_core_confirm_summary.csv`
  - `notebooks/outputs/grqm_cycle3_core_confirm_20260301_223742/proxy_agreement_v3.csv`
  - `notebooks/outputs/grqm_cycle3_core_confirm_20260301_223742/aggregate.json`
- Q2 pivot batch:
  - `notebooks/outputs/grqm_cycle3_q2_pivot_20260301_223823/cycle3_q2_pivot_summary.csv`

### Core metrics (Cycle-3)
- Runs: **20/20** (Ω_m = 0.285..0.300, α = 3e-7..1.3e-6)
- `pass_all_envelope`: **20/20 = 1.00**
- Proxy corroboration:
  - Pearson(primary, independent): **0.99985**
  - Spearman(primary, independent): **1.00000**
  - ratio mean (`Δ(2α)/Δ(α)`): **1.9678**
  - ratio std: **0.0314**
- Q1 robustness and refinement remained within gate limits for all points:
  - `q1_refinement_max_obs` max: **2.80e-07**
  - `q1_assumption_sensitivity_hardened` max: **0.1483**
- Replication and Q2 robust diagnostics in core:
  - `q2_true_replication_rel_diff`: **0.0** for all runs
  - `q2_D_p95` range: **0.0883..0.2850** (<0.5 gate)
  - `q2_D_p99` range: **0.0987..0.3892** (<0.8 gate)

### Q2 pivot result (DOP853 alternative approx family)
- 6-point pivot set (Ω_m in {0.295,0.300}; α in {3e-7,7e-7,1.3e-6})
- `D_p95` improved from O(1e-1) to O(1e-9) on all points
- `p95_improvement_pct`: **~99.9999995%** on all 6/6 points
- `t_first_1pct` for pivot method: **no crossing observed (`None`)** in all 6/6 points (consistent with extremely small error)
- Pivot gate (`>=20%` relative improvement): **6/6 pass** via `p95` criterion

### Gate decision snapshot (Cycle-3 core corridor)
- G-PROXY: **PASS**
- G-REFINE: **PASS**
- G-ROBUST-Q1: **PASS**
- G-ROBUST-Q2: **PASS** (bulk robust tails + pivot success)
- G-REPLICATION: **PASS**
- G-ENVELOPE: **PASS** (core corridor Ω_m<=0.300)
- G-PROMOTION (full): **NOT MET** (3 consecutive all-gate cycles in same envelope not yet established; high-impact ACTIVE assumptions remain)
- G-PROMOTION (provisional fallback): **MET IN-CORE** (Spearman>0.99 and ratio std<0.25 with full core pass)

Conservative interpretation:
- Evidence now supports **"PROVISIONALLY PROVEN in-core"** wording for the currently declared core corridor only.
- Full promotion to PROVEN remains pending consecutive-cycle consistency and assumption hardening.
