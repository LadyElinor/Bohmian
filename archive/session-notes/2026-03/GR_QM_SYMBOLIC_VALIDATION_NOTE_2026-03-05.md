# GR_QM Symbolic Validation Note — 2026-03-05

Purpose: record a diagnostic-only symbolic validation pass for the correction term used in `src/grqm/core.py`.

## Added
- `src/grqm/symbolic.py`
  - `validate_correction_term_symbolic(correction_power=5)`
  - Verifies leading correction scaling and small-`a` correction/classical scaling analytically via SymPy.
- `src/grqm/core.py`
  - `run_cycle()` now includes `metadata.symbolic_validation` in output receipt JSON.
- Tests:
  - `tests/test_symbolic_validation.py`

## Reproducible ratio receipt
Command:
- `python notebooks/wdw_symbolic_correction_ratio_receipt.py`

Outputs:
- `notebooks/outputs/grqm_symbolic_ratio_receipt_20260305_193500/`
- `notebooks/outputs/grqm_symbolic_ratio_receipt_20260305_214243/`
  - `symbolic_correction_ratio_rows.csv`
  - `symbolic_correction_ratio_summary.json`

## Extended symbolic consistency checks (late addendum)
- `src/grqm/symbolic.py` now includes explicit symbolic decomposition checks against the implemented acceleration form in `src/grqm/core.py`:
  - correction-channel exact-match check (`correction_match_zero`)
  - classical-channel exact-match check (`classical_match_zero`)
  - full-expression exact-match check (`full_accel_match_zero`)
- Test coverage extended in `tests/test_symbolic_validation.py`:
  - verifies all three exact-match checks for `n=5` and `n=4`
  - adds nonpositive-power rejection checks (`n<=0`)

## Key diagnostic results
- For default correction power `n=5`:
  - leading correction exponent = `-5`
  - correction/classical ratio exponent = `-3`
- Absolute ratio grows sharply toward small `a` (core and edge points), consistent with expected small-`a` dominance behavior.

## Governance posture
- Diagnostic + traceability update only.
- No claim-status, threshold, or edge-lane policy changes.
