import csv
import json
from datetime import datetime
from pathlib import Path

import numpy as np

from grqm_proxy_toymodel_v1 import IC, Params, RunConfig, integrate, interp_to_grid, l2_rel_err


def trimmed_mean(x, trim=0.05):
    x = np.sort(np.asarray(x))
    n = len(x)
    k = int(n * trim)
    if 2 * k >= n:
        return float(np.mean(x))
    return float(np.mean(x[k:n - k]))


def q1_delta(params: Params, ic: IC, dt_main=1e-3, correction_power=5):
    t_b, a_b, _ = integrate(ic, params, RunConfig(dt=dt_main, method="rk4", corrected=False))
    t_c, a_c, _ = integrate(ic, params, RunConfig(dt=dt_main, method="rk4", corrected=True, correction_power=correction_power))
    return t_b, a_b, a_c, float(l2_rel_err(a_c - a_b, a_b))


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


def q2_metrics(params: Params, ic: IC):
    dt_main = 1e-3
    dt_exact = 5e-4
    dt_coarse = 2e-3
    eps = 1e-15

    t_exact, a_exact, _ = integrate(ic, params, RunConfig(dt=dt_exact, method="rk4", corrected=True))
    t_approx, a_approx, _ = integrate(ic, params, RunConfig(dt=dt_main, method="euler", corrected=True))
    t_alt, a_alt, _ = integrate(ic, params, RunConfig(dt=dt_coarse, method="rk4", corrected=True))

    a_approx_on_exact = interp_to_grid(t_approx, a_approx, t_exact)
    a_alt_on_exact = interp_to_grid(t_alt, a_alt, t_exact)

    abs_err = np.abs(a_approx_on_exact - a_exact)
    d_star = float(np.mean(abs_err))
    d_star_alt = float(np.mean(np.abs(a_alt_on_exact - a_exact)))

    d_median = float(np.median(abs_err))
    d_trim = trimmed_mean(abs_err, 0.05)
    d_p95 = float(np.percentile(abs_err, 95))
    d_p99 = float(np.percentile(abs_err, 99))
    d_max = float(np.max(abs_err))

    spike_ratio = float(d_max / (d_median + eps))
    spike_detected = bool(spike_ratio > 1000.0)

    t_rep, a_rep, _ = integrate(ic, params, RunConfig(dt=dt_main, method="euler", corrected=True))
    a_rep_on_exact = interp_to_grid(t_rep, a_rep, t_exact)
    rel_true_rep = np.abs(a_rep_on_exact - a_approx_on_exact) / (np.abs(a_approx_on_exact) + eps)

    return {
        "q2_D_star": d_star,
        "q2_D_median": d_median,
        "q2_D_trimmed_mean": d_trim,
        "q2_D_p95": d_p95,
        "q2_D_p99": d_p99,
        "q2_D_max": d_max,
        "q2_spike_ratio_max_over_median": spike_ratio,
        "q2_spike_detected": spike_detected,
        "q2_true_replication_rel_diff": float(np.mean(rel_true_rep)),
        "q2_method_disagreement_rel_diff": float(abs(d_star_alt - d_star) / (abs(d_star) + eps)),
    }


def independent_proxy_metrics(omega_m: float, alpha_qg: float, correction_power=5):
    """
    Independent corroboration path: local linear-response scaling check.
    Compare Δ(2α) vs 2*Δ(α) at identical omega_m.
    """
    ic = IC()
    p_a = Params(omega_m=omega_m, omega_l=1.0 - omega_m, alpha_qg=alpha_qg)
    p_2a = Params(omega_m=omega_m, omega_l=1.0 - omega_m, alpha_qg=2.0 * alpha_qg)

    t_a, a_b_a, a_c_a, _ = q1_delta(p_a, ic, correction_power=correction_power)
    t_2a, a_b_2a, a_c_2a, _ = q1_delta(p_2a, ic, correction_power=correction_power)

    delta_a = a_c_a - a_b_a
    delta_2a = interp_to_grid(t_2a, a_c_2a - a_b_2a, t_a)
    delta_pred = 2.0 * delta_a

    rel_residual = l2_rel_err(delta_2a - delta_pred, delta_2a)
    corr = float(np.corrcoef(delta_2a, delta_pred)[0, 1])
    amp_ratio = float((np.sqrt(np.mean(delta_2a ** 2)) + 1e-15) / (np.sqrt(np.mean(delta_a ** 2)) + 1e-15))

    return {
        "proxy_linear_response_rel_residual": float(rel_residual),
        "proxy_linear_response_corr": corr,
        "proxy_linear_response_amp_ratio_2a_over_a": amp_ratio,
    }


def main():
    alpha_values = np.logspace(np.log10(2e-7), np.log10(2e-6), 9).tolist()
    omega_values = np.linspace(0.28, 0.32, 5).tolist()

    thresholds = {
        "q1_effect_persist_min": 1e-4,
        "q1_refinement_max": 5e-3,
        "q1_assumption_sensitivity_hardened_max": 0.2,
        "q2_Dstar_min": 1e-4,
        "q2_true_replication_rel_diff_max": 1e-2,
        "q2_method_disagreement_rel_diff_max": 0.5,
        "q2_D_p95_max": 0.5,
        "q2_D_p99_max": 0.8,
        "proxy_linear_response_rel_residual_max": 0.05,
        "proxy_linear_response_corr_min": 0.999,
    }

    hardened_perturbations = [
        dict(ic_scale=0.999, dt=1e-3, n=5),
        dict(ic_scale=1.001, dt=1e-3, n=5),
        dict(ic_scale=1.0, dt=9e-4, n=5),
        dict(ic_scale=1.0, dt=1.1e-3, n=5),
    ]

    root = Path(__file__).resolve().parents[1]
    out_root = root / "notebooks" / "outputs"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = out_root / f"grqm_cycle2_envelope_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    run_id = 0
    for omega_m in omega_values:
        for alpha_qg in alpha_values:
            ic = IC()
            p = Params(omega_m=float(omega_m), omega_l=float(1.0 - omega_m), alpha_qg=float(alpha_qg))
            _, _, _, base_delta = q1_delta(p, ic, dt_main=1e-3, correction_power=5)

            hard_sens = []
            for cfg in hardened_perturbations:
                ic_h = IC(a0=ic.a0 * cfg["ic_scale"], v0=ic.v0, t0=ic.t0, t1=ic.t1)
                _, _, _, d = q1_delta(p, ic_h, dt_main=cfg["dt"], correction_power=cfg["n"])
                hard_sens.append(abs(d - base_delta) / (abs(base_delta) + 1e-15))

            q1_ref = q1_refinement_max(p, ic, dt_main=1e-3, correction_power=5)
            q2 = q2_metrics(p, ic)
            proxy = independent_proxy_metrics(omega_m=float(omega_m), alpha_qg=float(alpha_qg), correction_power=5)

            row = {
                "run_id": run_id,
                "alpha_qg": float(alpha_qg),
                "omega_m": float(omega_m),
                "q1_delta_proxy_l2": base_delta,
                "q1_refinement_max_obs": q1_ref,
                "q1_assumption_sensitivity_hardened": float(max(hard_sens)),
                **q2,
                **proxy,
            }

            row["pass_q1_effect"] = row["q1_delta_proxy_l2"] >= thresholds["q1_effect_persist_min"]
            row["pass_q1_refinement"] = row["q1_refinement_max_obs"] <= thresholds["q1_refinement_max"]
            row["pass_q1_assumption_hardened"] = row["q1_assumption_sensitivity_hardened"] <= thresholds["q1_assumption_sensitivity_hardened_max"]
            row["pass_q2_Dstar"] = row["q2_D_star"] >= thresholds["q2_Dstar_min"]
            row["pass_q2_true_replication"] = row["q2_true_replication_rel_diff"] <= thresholds["q2_true_replication_rel_diff_max"]
            row["pass_q2_method_disagreement"] = row["q2_method_disagreement_rel_diff"] <= thresholds["q2_method_disagreement_rel_diff_max"]
            row["pass_q2_robust_bulk"] = (
                (row["q2_D_p95"] < thresholds["q2_D_p95_max"] and row["q2_D_p99"] < thresholds["q2_D_p99_max"])
                or row["q2_spike_detected"]
            )
            row["pass_proxy_linear_response"] = (
                row["proxy_linear_response_rel_residual"] <= thresholds["proxy_linear_response_rel_residual_max"]
                and row["proxy_linear_response_corr"] >= thresholds["proxy_linear_response_corr_min"]
            )
            row["pass_all_envelope"] = all([
                row["pass_q1_effect"],
                row["pass_q1_refinement"],
                row["pass_q1_assumption_hardened"],
                row["pass_q2_Dstar"],
                row["pass_q2_true_replication"],
                row["pass_q2_robust_bulk"],
            ])

            rows.append(row)
            run_id += 1

    with open(out_dir / "summary.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    aggregates = {
        "n_runs": len(rows),
        "n_pass_all_envelope": int(sum(r["pass_all_envelope"] for r in rows)),
        "n_pass_proxy_linear_response": int(sum(r["pass_proxy_linear_response"] for r in rows)),
        "q1_delta_min": float(min(r["q1_delta_proxy_l2"] for r in rows)),
        "q1_delta_max": float(max(r["q1_delta_proxy_l2"] for r in rows)),
        "q1_refinement_max": float(max(r["q1_refinement_max_obs"] for r in rows)),
        "q2_D_p95_max": float(max(r["q2_D_p95"] for r in rows)),
        "q2_D_p99_max": float(max(r["q2_D_p99"] for r in rows)),
        "q2_spike_any": bool(any(r["q2_spike_detected"] for r in rows)),
        "proxy_rel_residual_max": float(max(r["proxy_linear_response_rel_residual"] for r in rows)),
        "proxy_corr_min": float(min(r["proxy_linear_response_corr"] for r in rows)),
    }

    with open(out_dir / "aggregate.json", "w", encoding="utf-8") as f:
        json.dump(aggregates, f, indent=2)

    with open(out_dir / "manifest.json", "w", encoding="utf-8") as f:
        json.dump({
            "out_dir": str(out_dir),
            "alpha_values": alpha_values,
            "omega_values": omega_values,
            "thresholds": thresholds,
            "aggregates": aggregates,
        }, f, indent=2)

    print(json.dumps({"out_dir": str(out_dir), "n_runs": len(rows), "aggregates": aggregates}, indent=2))


if __name__ == "__main__":
    main()
