# GR_QM Process Debt + Fixes — 2026-03-06

## Scope
Retroactive PM review of recent GR_QM cycles using the new playbook (`projectmanagement/PM_AGENT_PLAYBOOK.md`).

## One-line verdict
Technical execution quality is high, but governance packaging and gate-coupling discipline are the main process debts.

---

## Process Debt Register

### D1) Split acceptance layers (prereg thresholds vs micro-package thresholds)
- **Symptom:** Edge prereg (`q2 p95<=0.50, p99<=0.80`) and micro-package targets (`p95<0.01, p99<0.05`) coexist without a single declared decision hierarchy.
- **Risk:** Ambiguous pass/fail narratives and governance friction.
- **Fix:** Declare 2-tier policy in one canonical file:
  - Tier A = governance gate (promotion/hold)
  - Tier B = stretch target (quality signal only)
- **Owner:** PM/gov layer
- **ETA:** immediate

### D2) Companion-gate incompleteness surfaced late
- **Symptom:** q2 micro-package looked excellent, but full packet later failed on q1 refinement.
- **Risk:** false confidence and wasted cycle time.
- **Fix:** Add preflight rule: no edge interpretation before all companion gates (q1/q2/replication) are present in same packet.
- **Owner:** run orchestration
- **ETA:** immediate

### D3) Artifact sprawl across many timestamped outputs
- **Symptom:** many outputs exist; latest canonical decision packet requires manual reconstruction.
- **Risk:** reviewer fatigue, audit mistakes, slower governance close.
- **Fix:** enforce cycle bundle index file each run-day:
  - canonical artifact paths,
  - single aggregate JSON,
  - decision paragraph.
- **Owner:** reporting layer
- **ETA:** next cycle

### D4) Decision-state lag after new evidence
- **Symptom:** strong diagnostics landed quickly, but formal state updates trail and are scattered across notes/addenda.
- **Risk:** stale mental model, inconsistent communication.
- **Fix:** single “state of lane” block updated every run day in monthly gate report:
  - status, blocker, next action, no-change clause.
- **Owner:** governance docs
- **ETA:** immediate

### D5) Missing explicit run-stop conditions in execution scripts
- **Symptom:** runs continue even when a hard blocker threshold is already blown (e.g., q1 refinement).
- **Risk:** avoidable compute burn and delayed pivot.
- **Fix:** add Jidoka stop hooks:
  - fail-fast flag when hard gate breached,
  - emit `stop_reason` in aggregate.
- **Owner:** notebook/script layer
- **ETA:** next script edit pass

### D6) Weak ownership map in documents
- **Symptom:** technical and governance tasks are clear, but ownership labels are implicit.
- **Risk:** missed handoffs.
- **Fix:** append owner tags to next-step checklist (Run owner / Analysis owner / Governance owner).
- **Owner:** PM docs
- **ETA:** immediate

---

## What is already working well (keep)
- Conservative governance posture (no premature edge promotion).
- Strong reproducibility discipline (replication checks, dual-receipt audits).
- Clear scope caveats (in-core vs edge lane).
- Robust diagnostics emphasis (method hierarchy, suppression checks).

---

## Priority Fix Plan (next 72 hours)
1. **Unify gate hierarchy doc** (Tier A vs Tier B acceptance semantics).
2. **Patch edge workflow checklist** to require full companion gates before interpretation.
3. **Publish canonical edge bundle index** for 2026-03-06 run set.
4. **Add daily state block** in `GR_QM_MONTHLY_GATE_REPORT_01.md`.
5. **Implement fail-fast hooks** in edge packet scripts (or wrapper).

---

## Current lane status (after 2026-03-06 runs)
- Edge packet does **not** pass all gates (`pass_all_packet_rate = 0.0`).
- Primary blocker: `q1_refinement` exceeds threshold.
- q2 and replication indicators are strong.
- Required posture: edge lane remains blocked pending mitigation on q1 refinement and governance-close sequence.
