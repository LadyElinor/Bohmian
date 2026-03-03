# GR↔QM Action Plan – Gate-Driven Edition (v2 – March 2026)

Created: 2026-02-28  
Last major revision: 2026-03-01 (gate-based refactor + robust stats + envelope first-class)

## 0) Mission and Operating Constraint (unchanged)

**Mission:** increase falsifiable progress on GR↔QM interfaces without drifting into non-testable abstraction.  
**Constraint:** every theory step must map to an observable proxy or a clearly logged BLOCKED status.

## 1) Core Operating Mode – Gate-Driven Cycles

Abandon fixed week structure. Work in **short, outcome-gated cycles** (typically 3–10 days). Each cycle ends when one or more of the following gates is passed / failed with rationale.

### Mandatory Gates per Cycle (all must be addressed)

**G-PROXY** – Proxy existence & scaling
- q1_delta_proxy_l2 monotonic / scaling with α_qg in envelope
- pass_q1_effect = True across ≥ 80% of sampled points

**G-REFINE** – Numerical stability
- pass_q1_refinement = True (max_obs under refinement < threshold, currently ~1e-6)

**G-ROBUST-Q1** – Assumption robustness (tiered)
- pass_q1_assumption_hardened (< 0.20 relative sensitivity under ±0.1–1% perturbations)
- Wide sensitivity logged but does not block if hardened passes

**G-ROBUST-Q2** – Divergence metric robustness (new – mandatory)
- Require robust statistics: q2_D_median, q2_D_trimmed_mean, q2_D_p95, q2_D_p99, q2_spike_detected
- Mean-only metrics (q2_D_star) cannot alone block claims
- pass if q2_D_p95 < 0.5 AND q2_D_p99 < 0.8 (tuneable) OR spike_detected=True but bulk metrics normal

**G-REPLICATION** – True reproducibility
- pass_q2_true_replication (< 1e-6 max rel diff on like-vs-like reruns)

**G-ENVELOPE** – Validity envelope declaration (first-class – mandatory for any claim)

Every partial/proven status must list:
- parameter bounds (α_qg min/max, Ω_m range, etc.)
- solver / integrator bounds (dt max, method family)
- excluded pathology windows (e.g. α ≈ 1.5e-7 with Euler dt=1e-3)
- mitigation for exclusions (smaller dt, alternate method)

**G-PROMOTION** – OPEN → PROVEN criteria (hard thresholds)

Requires **all** of:
- 2 consecutive cycles passing G-PROXY, G-REFINE, G-ROBUST-Q1, G-ROBUST-Q2, G-REPLICATION within same envelope
- no unresolved high-impact ACTIVE assumptions (from REGISTER)
- at least one independent proxy corroboration (different minisuperspace reduction, different observable, or analytic cross-check)
- explicit null-test definition passed in both cycles

## 2) Integrator & Method Policy (new section)

- **RK hierarchy** (coarse → fine RK4 or higher) = primary reference ladder (truth proxy)
- **Euler** = stress test / lower-order comparator only — never used for final claims unless hardened with small dt
- Method disagreement (Euler vs RK) treated as OPEN quantified limitation, not replication failure
- When disagreement used as proxy metric, report robust statistics (median/p95/etc.) + t_first_1pct

## 3) Outlier / Pathology Policy (new)

- Single-point or narrow-window spikes flagged via q2_spike_detected (max / median > 1e4)
- Pathology windows explicitly excluded from envelope with logged mitigation
- Never silently averaged away or down-weighted without rationale

## 4) Governance Rules (updated & tightened)

1. No claim without declared validity envelope (G-ENVELOPE mandatory).
2. No proxy claim without null-test definition.
3. No promotion to PROVEN with unresolved high-impact assumptions.
4. If result sensitive to minor pipeline changes → classify OPEN or BLOCKED.
5. Prefer explicit null results over ambiguous positive claims.
6. Mean-based metrics alone cannot block when robust alternatives (median/p95) are normal.

## 5) Cycle Cadence & Deliverables

- Cycle length: until ≥3 gates ready for decision (typically 3–10 days)
- Daily: 30–90 min theory/computation + logging
- Cycle close: update CLAIM_STATUS_MATRIX.md + short cycle report (1/2 page)
- Monthly gate report: consolidate cycle outcomes + hard decision (Proceed / Pivot / Pause)

## 6) Immediate Next Cycle (Cycle-2 queued)

1. Apply this gate-based refactor to GR_QM_ACTION_PLAN.md
2. Run unified tiered batch (current patched runner) as canonical Cycle-1 close artifact
3. Extend envelope: Ω_m ∈ [0.28, 0.32], α_qg log-spaced finer in [2e-7, 2e-6]
4. Add one independent proxy check (e.g. different observable or analytic bound comparison)
5. Target: first PROVEN candidate if promotion criteria met

Bottom line: fast, auditable loop — define narrowly, simulate minimally, test aggressively (with robust stats), decide explicitly, update envelope ruthlessly.
