# Bohmian

Minimal artifact repository for the **Bohmian / de Broglie–Bohm lane** of GRQM.

This repo is intentionally slim: it stores exportable run artifacts for review/citation without exposing the full GRQM development workspace.

## Included artifact
- `outputs/bohmian_envelope_comparison_20260320_223546`

## What this artifact concluded (important)
This snapshot corresponds to the Phase-2 envelope comparison run (**alpha_qg vs Bohmian-Q**) and concluded:

- **Recommendation:** `HOLD_FOUNDATION`
- **Decision:** Do **not** promote Bohmian-Q widening from this run
- **Stability:** 242 failed / 540 total (unstable rate: **44.81%**)
- **Target region (Omega_m ~ 0.30):** Bohmian-Q width was much smaller than alpha_qg by the run’s width metric

For details, see:
- `outputs/bohmian_envelope_comparison_20260320_223546/DECISION_MEMO.md`
- `outputs/bohmian_envelope_comparison_20260320_223546/summary.md`
- `outputs/bohmian_envelope_comparison_20260320_223546/decision.json`

## Scope and relationship to GRQM
- This is an **artifact lane**, not the primary source-code repo.
- Core implementation remains in the GRQM workspace (e.g., `src/grqm/bohmian_probe/`).
- Artifacts here should be treated as dated evidence snapshots.

## Notes for future artifacts
When adding new runs, include a decision memo and explicit recommendation so readers can quickly distinguish:
- promising exploratory results,
- neutral/inconclusive results,
- and negative results requiring a hold.
