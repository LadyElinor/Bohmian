# GR_QM_SN_SWEEP_NOTE_2026-03-11

## Scope (continuation of 2026-03-10 SN lane)
Executed the requested short-horizon extension first:
- `kappa = 1e-3`
- `C in {0.0, 0.01, 0.05}`
- `t_max in {20, 30}`

Numerically stable exploratory profile used (runtime-controlled):
- baseline `dt=2e-3`, `n_grid=128`
- targeted retighten `dt=1e-3`, `n_grid=256` when `q1_refinement > 0.8e-6`
- `sigma0=5.0`, `mass=1.0`, dynamic-vacuum enabled (`A=-0.5`)

## Receipts
Output root:
- `notebooks/outputs/sn_diagnostic_lane_20260311_091839/`

Primary artifacts:
- `run_receipt.json`
- `stage1_tmax_extension_summary.csv`
- `stage1_tmax_extension_aggregate.json`

## Stage-1 aggregate
From `stage1_tmax_extension_aggregate.json`:
- `n_rows = 6`
- `n_retightened = 2`
- `max_q1_signal = 0.06457426995231064`
- `max_q1_refinement = 1.2921487024441287e-06`
- `max_norm_drift = 3.000965711076331e-04`
- `loc_ratio_range = [1.0721094936411533, 1.4680726917519977]`
- `ipr_delta_range = [-0.01681251343586429, -0.003659609011542754]`
- `status_counts = PASS:0, WATCH:0, FAIL:6`
- `detect_pass_rate = 0.5`
- `refine_pass_rate = 0.6667`
- `norm_practical_pass_rate = 0.0`

## Threshold evaluation (governance framing)
Thresholds checked:
- q1_signal detect: `>0.05`
- q1_refinement: `<1e-6`
- norm drift: strict `<1e-10`, practical `<1e-5`
- localization ratio expected range: `1.00–1.05`
- ipr shift sanity: small negative shift expected

Observed verdict:
- q1_signal detect: **WATCH/PARTIAL PASS** (3/6 above 0.05)
- q1_refinement: **WATCH** (4/6 pass, 2/6 fail)
- norm drift strict: **FAIL** (0/6)
- norm drift practical: **FAIL** (0/6)
- localization ratio: **FAIL** (all rows above 1.05)
- ipr shift sanity: **PASS** (all rows negative, moderate magnitude)

## Stage-2 trigger decision
Per run logic, stronger-`kappa` stage was set to trigger only if stage-1 remained fully sub-threshold on detection.
- Stage-1 crossed detect threshold (`max_q1_signal > 0.05`), so stage-2 was **not auto-triggered** in this packet.

## Interpretation discipline
- Diagnostic-only result: yes, the `t_max` extension can produce detectable q1 signal at `kappa=1e-3` in this exploratory profile.
- Publishable claim status: **not upgraded**.
- Blocking issues remain material: norm drift and localization-ratio governance failures across all stage-1 rows.

## Next trigger recommendation
Run a controlled stronger-`kappa` probe (`kappa in {3e-3, 1e-2}`) **only with tighter numerics** and/or reduced horizon to avoid conflating genuine signal growth with numerical drift/localization artifacts.
