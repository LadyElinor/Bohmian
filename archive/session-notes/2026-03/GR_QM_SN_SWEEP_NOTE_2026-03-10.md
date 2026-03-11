# GR_QM_SN_SWEEP_NOTE_2026-03-10

## Scope
Ran a first SN signal sweep across:
- `kappa ∈ {1e-5, 3e-5, 1e-4, 3e-4, 1e-3}`
- `C ∈ {0.0, 0.01, 0.05}`
- with dynamic-vacuum mode on (`A=-0.5`) and baseline comparison.

Output folder:
- `Physics/notebooks/outputs/grqm_edge_companion_sn_signal_sweep_20260310_175621`

Files:
- `sn_signal_sweep_summary.csv`
- `sn_signal_sweep_aggregate.json`

## Runtime profile used
This run used a fast-map profile to keep turnaround short:
- `sigma0=5.0`, `mass=1.0`
- `t_max=2.0`
- `coarse_dt=1e-3`, `coarse_n_grid=128`
- retighten path configured (`dt/2`, `grid*2`) but not triggered.

## Aggregate
- `n_rows = 15`
- `n_retightened = 0`
- `pass_all_rate = 0.0`
- `max_q1_signal = 3.1620135340570954e-04`
- `max_q1_refinement_proxy = 9.061477411193756e-08` (strong pass)
- `max_norm_drift = 5.87577978761189e-06`
- `max_replication_rel_diff = 0.0`
- `max_localization_sigma_ratio = 1.0020288663235881`
- `min_ipr_delta = -7.241758375442497e-05`
- Classification: green=0, yellow=0, red=15

## Interpretation
- In this low-κ fast-map band, the SN signal remains weak (`Q1 << 0.05` across all cases).
- Refinement and replication are strong; no instability signature detected.
- Norm drift exceeds the strict `1e-10` governance threshold in this quick profile, so `pass_all_rate` is 0.0.

## Next
If physics detection is the priority, increase coupling/time horizon (e.g., higher `kappa`, longer `t_max`) while preserving refinement controls.
If governance pass-rate is the priority, rerun with stricter numerics (higher grid, smaller dt) and/or relax norm-drift gate for exploratory sweeps.
