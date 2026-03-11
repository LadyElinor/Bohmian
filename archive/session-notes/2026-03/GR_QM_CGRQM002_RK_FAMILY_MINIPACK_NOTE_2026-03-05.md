# C-GRQM-002 RK-Family Robustness Mini-Pack Note — 2026-03-05

## Predeclared acceptance text (declared for this pack before decision)
For core-corridor points `(Ω_m, α_qg) in {(0.295,3e-7), (0.295,7e-7), (0.295,1.3e-6), (0.300,3e-7), (0.300,7e-7), (0.300,1.3e-6)}` and RK-family comparators `{RK23, RK45, DOP853}` against a tight DOP853 reference (`rtol=1e-12`, `atol=1e-14`), accept mini-pack if all are true:

1. `max_q2_D_p95 <= 0.50`
2. `max_q2_D_p99 <= 0.80`
3. `rk_family_abs_spread_p95 <= 1e-8` (absolute spread gate; relative spread tracked as diagnostic only)
4. `q2_true_replication_rel_diff <= 1e-6`
5. no solver failures in declared methods

## Run executed
Command:
- `python notebooks/cgrqm002_rk_family_minipack.py`

Artifact:
- `notebooks/outputs/grqm_cgrqm002_rk_family_minipack_20260305_171537/`
  - `rk_family_method_rows.csv`
  - `rk_family_point_summary.csv`
  - `summary.json`

## Outcome summary
- `n_points = 6`
- `all_points_pass = true`
- `global_max_q2_D_p95 = 6.2207088369348185e-09`
- `global_max_q2_D_p99 = 7.576536509290577e-09`
- `global_max_rk_family_abs_spread_p95 = 4.713609946804809e-09`
- `global_max_replication_rel_diff = 0.0`

## Decision recommendation
- **Mini-pack decision: PASS** (acceptance criteria met).
- **Claim-level recommendation for C-GRQM-002:** keep global status `OPEN` for now; evidence is materially stronger but should be repeated in one additional independent cycle package before any promotion request.

## Independent repeat run (same day, fresh timestamp)
Command:
- `python notebooks/cgrqm002_rk_family_minipack.py`

Artifact:
- `notebooks/outputs/grqm_cgrqm002_rk_family_minipack_20260305_184849/`
  - `rk_family_method_rows.csv`
  - `rk_family_point_summary.csv`
  - `summary.json`

Repeat outcome summary:
- `n_points = 6`
- `all_points_pass = true`
- `global_max_q2_D_p95 = 6.2207088369348185e-09`
- `global_max_q2_D_p99 = 7.576536509290577e-09`
- `global_max_rk_family_abs_spread_p95 = 4.713609946804809e-09`
- `global_max_replication_rel_diff = 0.0`

Interpretation:
- Independent repeat reproduces the first mini-pack result at the decision-relevant metric level.
- C-GRQM-002 robustness evidence now includes two same-day independent run receipts; still conservative to keep claim status `OPEN` until governance chooses promotion timing.
