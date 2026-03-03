import csv
import json
from datetime import datetime
from pathlib import Path

import numpy as np

from grqm_proxy_toymodel_v1 import IC, Params, RunConfig, integrate, interp_to_grid, l2_rel_err


def q1_delta(params: Params, ic: IC, dt_main=1e-3, correction_power=5):
    t_b, a_b, _ = integrate(ic, params, RunConfig(dt=dt_main, method="rk4", corrected=False))
    t_c, a_c, _ = integrate(ic, params, RunConfig(dt=dt_main, method="rk4", corrected=True, correction_power=correction_power))
    return float(l2_rel_err(a_c - a_b, a_b))


def q1_refinement_max(params: Params, ic: IC, dt_main=1e-3, correction_power=5):
    dt_ref = dt_main / 2.0
    t_b, a_b, _ = integrate(ic, params, RunConfig(dt=dt_main, method="rk4", corrected=False))
    t_c, a_c, _ = integrate(ic, params, RunConfig(dt=dt_main, method="rk4", corrected=True, correction_power=correction_power))
    t_b_ref, a_b_ref, _ = integrate(ic, params, RunConfig(dt=dt_ref, method="rk4", corrected=False))
    t_c_ref, a_c_ref, _ = integrate(ic, params, RunConfig(dt=dt_ref, method="rk4", corrected=True, correction_power=correction_power))
    a_b_main_on_ref = interp_to_grid(t_b, a_b, t_b_ref)
    a_c_main_on_ref = interp_to_grid(t_c, a_c, t_c_ref)
    e1 = l2_rel_err(a_b_main_on_ref - a_b_ref, a_b_ref)
    e2 = l2_rel_err(a_c_main_on_ref - a_c_ref, a_c_ref)
    return float(max(e1, e2))


def first_crossing_time(t, rel_err, threshold=1e-2):
    idx = np.where(rel_err >= threshold)[0]
    return None if len(idx) == 0 else float(t[idx[0]])


def trimmed_mean(x, trim=0.05):
    x = np.sort(np.asarray(x))
    n = len(x)
    k = int(n * trim)
    if 2 * k >= n:
        return float(np.mean(x))
    return float(np.mean(x[k:n-k]))


def q2_metrics(params: Params):
    ic = IC()
    dt_main = 1e-3
    dt_exact = 2.5e-4
    dt_coarse = 2e-3
    eps = 1e-15

    t_exact, a_exact, _ = integrate(ic, params, RunConfig(dt=dt_exact, method="rk4", corrected=True))
    t_approx, a_approx, _ = integrate(ic, params, RunConfig(dt=dt_main, method="euler", corrected=True))
    t_alt, a_alt, _ = integrate(ic, params, RunConfig(dt=dt_coarse, method="rk4", corrected=True))

    a_approx_on_exact = interp_to_grid(t_approx, a_approx, t_exact)
    a_alt_on_exact = interp_to_grid(t_alt, a_alt, t_exact)

    abs_err = np.abs(a_approx_on_exact - a_exact)
    D_t_alt = np.abs(a_alt_on_exact - a_exact)
    D_star = float(np.mean(abs_err))
    D_star_alt = float(np.mean(D_t_alt))

    D_median = float(np.median(abs_err))
    D_trimmed = trimmed_mean(abs_err, 0.05)
    D_p95 = float(np.percentile(abs_err, 95))
    D_p99 = float(np.percentile(abs_err, 99))
    D_max = float(np.max(abs_err))

    spike_ratio = float(D_max / (D_median + eps))
    spike_detected = bool(spike_ratio > 1000.0)

    t_approx_rep2, a_approx_rep2, _ = integrate(ic, params, RunConfig(dt=dt_main, method="euler", corrected=True))
    a_approx_rep2_on_exact = interp_to_grid(t_approx_rep2, a_approx_rep2, t_exact)
    rel_true_rep = np.abs(a_approx_rep2_on_exact - a_approx_on_exact) / (np.abs(a_approx_on_exact) + eps)

    rel_exact_vs_approx = np.abs(a_approx_on_exact - a_exact) / (np.abs(a_exact) + eps)

    return {
        "q2_D_star": D_star,
        "q2_D_median": D_median,
        "q2_D_trimmed_mean": D_trimmed,
        "q2_D_p95": D_p95,
        "q2_D_p99": D_p99,
        "q2_D_max": D_max,
        "q2_spike_ratio_max_over_median": spike_ratio,
        "q2_spike_detected": spike_detected,
        "q2_true_replication_rel_diff": float(np.mean(rel_true_rep)),
        "q2_method_disagreement_rel_diff": float(abs(D_star_alt - D_star) / (abs(D_star) + eps)),
        "q2_t_first_method_disagreement_1pct": first_crossing_time(t_exact, rel_exact_vs_approx, 1e-2),
    }


def main():
    alpha_values = [2.1544346900318822e-7, 3e-7, 4.6415888336127725e-7, 7e-7, 1e-6, 1.5e-6]
    omega_m = 0.30

    thresholds = {
        "q1_effect_persist_min": 1e-4,
        "q1_refinement_max": 5e-3,
        "q1_assumption_sensitivity_hardened_max": 0.2,
        "q2_Dstar_min": 1e-4,
        "q2_true_replication_rel_diff_max": 1e-2,
        "q2_method_disagreement_rel_diff_max": 0.5,
    }

    wide_perturbations = [
        ("n", 4, dict(ic_scale=1.0, dt=1e-3, n=4)),
        ("n", 6, dict(ic_scale=1.0, dt=1e-3, n=6)),
        ("a0", 0.98, dict(ic_scale=0.98, dt=1e-3, n=5)),
        ("a0", 1.02, dict(ic_scale=1.02, dt=1e-3, n=5)),
        ("dt", 8e-4, dict(ic_scale=1.0, dt=8e-4, n=5)),
        ("dt", 1.2e-3, dict(ic_scale=1.0, dt=1.2e-3, n=5)),
    ]
    hardened_perturbations = [
        ("a0", 0.999, dict(ic_scale=0.999, dt=1e-3, n=5)),
        ("a0", 1.001, dict(ic_scale=1.001, dt=1e-3, n=5)),
        ("dt", 9e-4, dict(ic_scale=1.0, dt=9e-4, n=5)),
        ("dt", 1.1e-3, dict(ic_scale=1.0, dt=1.1e-3, n=5)),
    ]

    root = Path(__file__).resolve().parents[1]
    out_root = root / "notebooks" / "outputs"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = out_root / f"grqm_batch_tiered_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    for i, alpha_qg in enumerate(alpha_values):
        p = Params(omega_m=omega_m, omega_l=1.0 - omega_m, alpha_qg=alpha_qg)
        base_ic = IC()
        base_delta = q1_delta(p, base_ic, dt_main=1e-3, correction_power=5)

        wide_sens = []
        for _, _, cfg in wide_perturbations:
            ic = IC(a0=base_ic.a0 * cfg["ic_scale"], v0=base_ic.v0, t0=base_ic.t0, t1=base_ic.t1)
            d = q1_delta(p, ic, dt_main=cfg["dt"], correction_power=cfg["n"])
            wide_sens.append(abs(d - base_delta) / (abs(base_delta) + 1e-15))

        hard_sens = []
        for _, _, cfg in hardened_perturbations:
            ic = IC(a0=base_ic.a0 * cfg["ic_scale"], v0=base_ic.v0, t0=base_ic.t0, t1=base_ic.t1)
            d = q1_delta(p, ic, dt_main=cfg["dt"], correction_power=cfg["n"])
            hard_sens.append(abs(d - base_delta) / (abs(base_delta) + 1e-15))

        q1_ref = q1_refinement_max(p, base_ic, dt_main=1e-3, correction_power=5)
        q2 = q2_metrics(p)

        pass_q1_effect = base_delta >= thresholds["q1_effect_persist_min"]
        pass_q1_refinement = q1_ref <= thresholds["q1_refinement_max"]
        pass_q1_assumption_hardened = max(hard_sens) <= thresholds["q1_assumption_sensitivity_hardened_max"]
        pass_q2_Dstar = q2["q2_D_star"] >= thresholds["q2_Dstar_min"]
        pass_q2_true_replication = q2["q2_true_replication_rel_diff"] <= thresholds["q2_true_replication_rel_diff_max"]
        pass_q2_method_disagreement = q2["q2_method_disagreement_rel_diff"] <= thresholds["q2_method_disagreement_rel_diff_max"]

        row = {
            "run_id": i,
            "alpha_qg": alpha_qg,
            "omega_m": omega_m,
            "q1_delta_proxy_l2": base_delta,
            "q1_refinement_max_obs": q1_ref,
            "q1_assumption_sensitivity_wide": float(max(wide_sens)),
            "q1_assumption_sensitivity_hardened": float(max(hard_sens)),
            **q2,
            "pass_q1_effect": pass_q1_effect,
            "pass_q1_refinement": pass_q1_refinement,
            "pass_q1_assumption_hardened": pass_q1_assumption_hardened,
            "pass_q2_Dstar": pass_q2_Dstar,
            "pass_q2_true_replication": pass_q2_true_replication,
            "pass_q2_method_disagreement": pass_q2_method_disagreement,
            "pass_all_strict": all([
                pass_q1_effect, pass_q1_refinement, pass_q1_assumption_hardened,
                pass_q2_Dstar, pass_q2_true_replication, pass_q2_method_disagreement
            ]),
            "pass_all_envelope": all([
                pass_q1_effect, pass_q1_refinement, pass_q1_assumption_hardened,
                pass_q2_Dstar, pass_q2_true_replication
            ]),
        }
        rows.append(row)

        with open(out_dir / f"run_{i:03d}_alpha_{alpha_qg:.3e}.json", "w", encoding="utf-8") as f:
            json.dump(row, f, indent=2)

    with open(out_dir / "summary.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    with open(out_dir / "manifest.json", "w", encoding="utf-8") as f:
        json.dump({"out_dir": str(out_dir), "thresholds": thresholds, "n_runs": len(rows)}, f, indent=2)

    print(json.dumps({"out_dir": str(out_dir), "n_runs": len(rows)}, indent=2))


if __name__ == "__main__":
    main()
