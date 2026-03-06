# GR_QM C-WDW-001 Symbolic Derivation Receipt — 2026-03-05

Purpose: compact, auditable receipt connecting the implemented correction channel in `src/grqm/core.py` to a symbolic small-`a` scaling derivation.

## Scope + links
- Primary derivation scaffold: `docs/C-WDW-001_CORRECTION_DERIVATION.md`
- Toy-model spec linkage: `GR_QM_TOY_MODEL_SPEC.md`
- Numerics protocol linkage: `GR_QM_NUMERICS_PROTOCOL.md`
- Claim governance linkage: `CLAIM_STATUS_MATRIX.md`

## Implemented symbolic pass
- Code: `src/grqm/symbolic.py`
- Entry point: `validate_correction_term_symbolic(correction_power=5)`
- Integrated metadata hook: `src/grqm/core.py` (`run_cycle()` now emits symbolic validation receipt under `metadata.symbolic_validation`).

## Compact derivation receipt
Model channel used in code:
\[
\ddot a = -\frac{\Omega_m}{2a^2} + \Omega_\Lambda a + \frac{\alpha}{a^n}
\]
with production default `n=5`.

1. Correction term leading behavior:
\[
\frac{\alpha}{a^n} \sim a^{-n} \quad (a\to0^+)
\]
Symbolic check returns leading exponent `-n` (`-5` at default).

2. Relative-to-classical matter-dominated behavior (small `a`):
\[
\text{classical} \sim -\frac{\Omega_m}{2a^2}
\quad\Rightarrow\quad
\frac{\alpha/a^n}{\text{classical}} \sim -\frac{2\alpha}{\Omega_m}a^{2-n}
\]
Symbolic check returns ratio exponent `2-n` (`-3` at default), so absolute ratio diverges as `a\to0^+` for `n>2`.

3. Interpretation in this toy envelope:
- For default `n=5`, correction dominance increases rapidly toward small `a`.
- This is consistent with prior edge-stiffness diagnostics and motivates keeping edge lane separately governed.

## Run-level diagnostic output
- Repro script: `notebooks/wdw_symbolic_correction_ratio_receipt.py`
- Output artifact (timestamped):
  - `notebooks/outputs/grqm_symbolic_ratio_receipt_<timestamp>/symbolic_correction_ratio_rows.csv`
  - `notebooks/outputs/grqm_symbolic_ratio_receipt_<timestamp>/symbolic_correction_ratio_summary.json`

## Governance posture
- Diagnostic/traceability enhancement only.
- No threshold edits, no claim status mutation, no envelope expansion.
