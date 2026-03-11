# GRQM (Governance-First Toy Proxy)

A scoped computational-physics workflow for testing **process reliability** and a narrow **WDW-inspired toy correction signal**.

Canonical status source: `CLAIM_STATUS_MATRIX.md`.

## Current Truth (status at a glance)
Read `docs/CURRENT_TRUTH_2026-03.md` for proven claims, envelope, caveats, and active lanes.

## Minimal mental model
- This repo is a **methodology + toy-model** stack.
- We run a tiny FRW-inspired ODE with/without a correction term.
- We treat outputs as **in-core evidence only** (not broad physical confirmation).
- Governance files track what is OPEN/PROVEN/BLOCKED and why.

## 60-second quickstart
```bash
cd Physics
python -m pip install -e .[dev]
python scripts/run_toy_model.py --out-dir outputs
pytest
```

## Reproduce the edge lift + boundary check
```bash
cd Physics
# edge packet closure receipt (in-policy adaptive packet)
python notebooks/edge_companion_global_adaptive_packet.py --mode inpolicy --resume --out-dir notebooks/outputs/grqm_edge_companion_inpolicy_adaptive_checkpointed_20260307_132048

# boundary confirmation mini-sweep at Ω_m=0.31
python notebooks/edge_boundary_confirmation_sweep.py
```

Canonical boundary receipt:
`notebooks/outputs/grqm_edge_boundary_sweep_omega031_20260308_122537/README.md`

Expected artifacts:
- `outputs/grqm_proxy_results_v1.json`
- `outputs/grqm_proxy_results_v1_summary.csv`

## Architecture sketch
```text
src/grqm/core.py
  ├─ integrate() + accel() + metrics
  └─ run_cycle()
       ├─ symbolic receipt call (src/grqm/symbolic.py)
       ├─ writes canonical JSON + summary CSV
       └─ returned dict consumed by tests/scripts

scripts/run_toy_model.py
  └─ thin CLI wrapper around run_cycle()

tests/
  ├─ toy-model invariants (refinement, signal persistence, determinism)
  └─ symbolic scaling checks

notebooks/
  └─ diagnostic/governance support scripts (non-canonical unless promoted)
```

## Canonical JSON example
From `grqm_proxy_results_v1.json`:

```json
{
  "metadata": {
    "seed": 42,
    "model": "FRW-inspired minisuperspace toy ODE",
    "params": {"omega_m": 0.3, "omega_l": 0.7, "alpha_qg": 1e-7},
    "symbolic_validation": {"derivation_ok": true}
  },
  "q1": {
    "delta_proxy_l2": 0.001,
    "baseline_refinement_error": 0.000001,
    "corrected_refinement_error": 0.000001
  },
  "q2": {
    "D_star": 0.002,
    "replication_rel_diff": 0.01
  }
}
```

(Values above are schema-shaped examples; run locally for exact values.)

## Artifact map + reproducibility
- Canonical vs archival map: `CANONICAL_ARTIFACTS.md`
- Dependency/repro tiers: `docs/REPRODUCIBILITY_TIERS.md`
- Strict lockfile path (for governed reruns): `requirements-lock.txt`

## Edge lane governance language (canonical)
Edge region (`Ω_m <= 0.31`) is now numerically tractable and passes all proxy gates under mandatory constraints: adaptive refinement + stiff solver (Radau baseline) + overlapping-time interpolation for refinement metrics.

Exploratory inclusion is approved under those constraints.

Physical claims in this lane require the semiclassical validity caveat: transient non-perturbative dominance (`correction/classical ratio > 1` near `min_a ≈ 0.01`).

## Session notes location
Dated working notes were moved out of root for navigability:
- `archive/session-notes/2026-03/`

Canonical governance/status files remain in root.

## Repository layout
- `src/grqm/` — core model, symbolic receipts, package CLI
- `scripts/` — stable entrypoints
- `tests/` — automated smoke/invariant tests
- `notebooks/` — exploratory + diagnostic scripts
- `docs/` — rationale, derivation, and reproducibility guidance
- `archive/session-notes/` — dated narrative notes and interim packets
