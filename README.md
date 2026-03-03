# LadyElinor / GRQM

Governance-first computational physics workflow for GR↔QM proxy research.

This repo is primarily a **methodology product**: explicit envelopes, gate-driven cycles, null tests, and conservative claim promotion (`OPEN -> PROVEN`) with auditable artifacts.

## 30-second purpose
- Validate a disciplined research workflow on a minisuperspace-inspired toy ODE.
- Keep physics claims scoped and falsifiable.
- Separate **workflow validation** from **physics conclusions**.

## 2-minute quickstart

```bash
cd Physics
python -m pip install -e .[dev]
python scripts/run_toy_model.py --out-dir outputs
```

Expected outputs:
- `outputs/grqm_proxy_results_v1.json`
- `outputs/grqm_proxy_results_v1_summary.csv`

### Success criteria (toy-model smoke run)
- `q1.baseline_refinement_error < 5e-3`
- `q1.corrected_refinement_error < 5e-3`
- deterministic rerun reproduces key metrics (tests enforce this)

Run tests:

```bash
pytest
```

## Project map
- Start here: `README.md`
- Toy model spec: `GR_QM_TOY_MODEL_SPEC.md`
- Numerics protocol: `GR_QM_NUMERICS_PROTOCOL.md`
- Action plan: `GR_QM_ACTION_PLAN.md`
- Proxy rationale bridge: `docs/PROXY_RATIONALE.md`
- Governance/reporting:
  - `CLAIM_STATUS_MATRIX.md`
  - `GR_QM_MONTHLY_GATE_REPORT_01.md`
  - `GR_QM_CONSECUTIVE_CYCLE_PROMOTION_LEDGER.md`

## Layout
- `src/grqm/` — core integrators/metrics + CLI
- `scripts/` — runnable entrypoints/regeneration helpers
- `tests/` — invariant tests
- `notebooks/` — exploration + cycle scripts
- `notebooks/outputs/golden_run_20260302/` — pinned reference artifact

## Reproducibility policy
- Dependencies pinned in `pyproject.toml`
- CI smoke check runs toy-model invariants on each push/PR
- Bulk timestamped outputs are not committed by default; regenerate as needed
