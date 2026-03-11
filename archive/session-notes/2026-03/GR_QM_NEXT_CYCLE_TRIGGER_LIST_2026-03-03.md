# GR_QM Next Trigger List — 2026-03-03

## Priority order (post governance sign-off)

1. **Public status visibility (complete)**
   - Added README status banner with PROVEN/OPEN/BLOCKED snapshot and envelope caveat.

2. **C-GRQM-001 hardening (executed 2026-03-05)**
   - ✅ Fresh confirmation cycle run + KPI table updated:
     - `GR_QM_KPI_SNAPSHOT_2026-03-05.md`
     - `notebooks/outputs/grqm_cycle3_core_confirm_20260305_171322/`
   - ✅ Trend row added in `CLAIM_STATUS_MATRIX.md`.
   - Status remains OPEN pending additional externally reviewable cycle packaging.

3. **C-GRQM-002 robustness mini-pack (executed 2026-03-05)**
   - ✅ RK-family-only comparator checks across core corridor completed.
   - ✅ Predeclared acceptance text + decision recommendation recorded:
     - `GR_QM_CGRQM002_RK_FAMILY_MINIPACK_NOTE_2026-03-05.md`
     - `notebooks/outputs/grqm_cgrqm002_rk_family_minipack_20260305_171537/`
   - Status remains OPEN; recommendation is one additional independent repeat before promotion request.

4. **Edge lane criteria pre-registration (updated v1 on 2026-03-05 before any Ω_m>=0.305 claim work)**
   - Define explicit acceptance for edge mitigation package:
     - grid density and dt ladder,
     - method comparators,
     - p95/p99 and replication caps,
     - null-test conditions,
     - fail/hold conditions.
   - Keep edge corridor blocked until criteria are passed and governance-closed.

5. **Cliff investigation sequencing rule (new)**
   - Execute strictly as: derivation appendix -> mechanism prediction -> diagnostic run -> governance decision.
   - Apply `GR_QM_CWDW001_FALSIFICATION_PROTOCOL.md` after run.

6. **Exploratory branch discipline (ongoing)**
   - Nonlinear and BoO lanes remain diagnostic-only unless they pass their own gates and receive separate promotion decision.
