# GR_QM Astropy Background Validation Note — 2026-03-05

Purpose: add a diagnostic-only cross-check against `astropy.cosmology.FlatLambdaCDM` for classical background trajectory behavior at core and edge Ω_m points.

## What was added
- New script: `notebooks/wdw_astropy_background_validation.py`
- Dependency updates:
  - `requirements.txt` → `astropy>=6.0.0`
  - `pyproject.toml` dependencies → `astropy>=6.0.0`

## Run receipt
Command:
- `python notebooks/wdw_astropy_background_validation.py`

Output:
- `notebooks/outputs/grqm_astropy_background_validation_20260305_192643/`
  - `astropy_background_validation.json`
  - `astropy_background_validation_summary.csv`

## Method notes (important)
- This check is **shape-only diagnostic**, not a unit-identical equivalence test.
- Comparison is done with normalized time and normalized amplitude trajectories.
- No claim/policy/gate thresholds were modified by this run.

## Headline observations
- `Ω_m=0.285`: lower shape mismatch than higher Ω_m cases.
- `Ω_m=0.300` and `Ω_m=0.3075`: larger mismatch in this diagnostic framing, with model monotonicity departure while Astropy reference remains monotonic.
- Interpretation: useful as a background sanity probe and edge-behavior context, not as a direct falsifier by itself.

## Sensitivity repeat receipt (stability check)
Command:
- `python notebooks/wdw_astropy_background_sensitivity_sweep.py`

Output:
- `notebooks/outputs/grqm_astropy_background_sensitivity_20260305_192913/`
  - `astropy_background_sensitivity.json`
  - `astropy_background_sensitivity_summary.csv`
  - `astropy_background_sensitivity_aggregate.json`

Key stability metrics (aggregate envelope):
- `0.285`: `l2_min=0.1076`, `l2_max=2.8109`
- `0.300`: `l2_min=0.1278`, `l2_max=1.3315`
- `0.3075`: `l2_min=0.1176`, `l2_max=2.3324`

Interpretation:
- Diagnostic signal persists across small `dt/a0/v0` perturbations (non-zero mismatch retained), but magnitude is setup-sensitive.
- This supports use as a governance context probe, not a standalone decision metric.

## Governance posture
- Diagnostic-only addition.
- Edge lane block posture remains unchanged (`Ω_m>=0.305` still blocked pending separate preregistered sequence).
