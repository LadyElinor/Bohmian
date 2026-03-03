# GRQM Delta Autopsy

- Passing: `C:\Users\arren\.openclaw\workspace\Physics\notebooks\outputs\grqm_cycle3_core_confirm_20260302_172931`
- Failed: `C:\Users\arren\.openclaw\workspace\Physics\notebooks\outputs\grqm_cycle4_inpolicy_confirm_20260302_180311`
- Compared points: 20

## Smoking gun
- First gate flip at omega_m=0.285, alpha_qg=3e-07: q1_assumption_sensitivity_hardened delta=0.846982, pass_all_envelope True -> False.

## Top contributors by effect size (mean |delta|)
1. q1_assumption_sensitivity_hardened: mean|delta|=0.811807, max|delta|=0.846982
2. q1_delta_proxy_l2: mean|delta|=0, max|delta|=0
3. q1_refinement_max_obs: mean|delta|=0, max|delta|=0

## Config/assumption knobs changed
- [aggregate.json] pass_rate_envelope: 1.0 -> 0.0
- [aggregate.json] policy_bounds.correction_power_allowed: None -> [4, 5]
- [aggregate.json] policy_bounds.dt_main_max: None -> 0.0012
- [aggregate.json] policy_bounds.dt_main_min: None -> 0.0008
- [aggregate.json] policy_bounds.ic_scale_max: None -> 1.0009
- [aggregate.json] policy_bounds.ic_scale_min: None -> 0.9993
- [runner_script] hardened_perturbations: [{'ic_scale': 0.999, 'dt': 0.001, 'n': 5}, {'ic_scale': 1.001, 'dt': 0.001, 'n': 5}, {'ic_scale': 1.0, 'dt': 0.0009, 'n': 5}, {'ic_scale': 1.0, 'dt': 0.0011, 'n': 5}] -> None
- [runner_script] policy_perturbations: None -> [{'ic_scale': 0.9993, 'dt': 0.0008, 'n': 4}, {'ic_scale': 1.0009, 'dt': 0.0008, 'n': 4}, {'ic_scale': 0.9993, 'dt': 0.0012, 'n': 5}, {'ic_scale': 1.0009, 'dt': 0.0012, 'n': 5}]
