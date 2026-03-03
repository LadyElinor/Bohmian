import argparse
import csv
import json
import math
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

import numpy as np

from grqm_proxy_toymodel_v1 import IC, Params, RunConfig, integrate, interp_to_grid, l2_rel_err


THRESHOLDS = {
    "q1_effect_persist_min": 1e-4,
    "q1_refinement_max": 5e-3,
    "q1_assumption_sensitivity_max": 0.5,
    "q2_Dstar_min": 1e-4,
    "q2_true_replication_rel_diff_max": 1e-2,
    "q2_method_disagreement_rel_diff_max": 0.5,
}


def first_crossing_time(t, rel_err, threshold=1e-2):
    idx = np.where(rel_err >= threshold)[0]
    if len(idx) == 0:
        return None
    return float(t[idx[0]])


def evaluate_run(params: Params, seed: int = 42):
    np.random.seed(seed)
    ic = IC()

    dt_main = 1e-3
    dt_ref = 5e-4
    dt_exact = 2.5e-4
    dt_coarse = 2e-3

    t_b, a_b, _ = integrate(ic, params, RunConfig(dt=dt_main, method="rk4", corrected=False))
    t_c, a_c, _ = integrate(ic, params, RunConfig(dt=dt_main, method="rk4", corrected=True))

    delta_proxy_l2 = l2_rel_err(a_c - a_b, a_b)
    delta_proxy_max_abs = float(np.max(np.abs(a_c - a_b)))
    delta_proxy_sign_final = float(np.sign((a_c - a_b)[-1]))

    t_b_ref, a_b_ref, _ = integrate(ic, params, RunConfig(dt=dt_ref, method="rk4", corrected=False))
    t_c_ref, a_c_ref, _ = integrate(ic, params, RunConfig(dt=dt_ref, method="rk4", corrected=True))

    a_b_main_on_ref = interp_to_grid(t_b, a_b, t_b_ref)
    a_c_main_on_ref = interp_to_grid(t_c, a_c, t_c_ref)

    baseline_refinement_error = l2_rel_err(a_b_main_on_ref - a_b_ref, a_b_ref)
    corrected_refinement_error = l2_rel_err(a_c_main_on_ref - a_c_ref, a_c_ref)

    t_c_n4, a_c_n4, _ = integrate(ic, params, RunConfig(dt=dt_main, method="rk4", corrected=True, correction_power=4))
    delta_proxy_n4_l2 = l2_rel_err(a_c_n4 - a_b, a_b)
    assumption_sensitivity_rel = abs(delta_proxy_n4_l2 - delta_proxy_l2) / (abs(delta_proxy_l2) + 1e-15)

    # Q2 paths
    t_exact, a_exact, _ = integrate(ic, params, RunConfig(dt=dt_exact, method="rk4", corrected=True))
    t_approx, a_approx, _ = integrate(ic, params, RunConfig(dt=dt_main, method="euler", corrected=True))
    t_alt, a_alt, _ = integrate(ic, params, RunConfig(dt=dt_coarse, method="rk4", corrected=True))

    a_approx_on_exact = interp_to_grid(t_approx, a_approx, t_exact)
    a_alt_on_exact = interp_to_grid(t_alt, a_alt, t_exact)

    D_t = np.abs(a_approx_on_exact - a_exact)
    D_star = float(np.mean(D_t))
    D_max = float(np.max(D_t))

    D_t_alt = np.abs(a_alt_on_exact - a_exact)
    D_star_alt = float(np.mean(D_t_alt))
    D_max_alt = float(np.max(D_t_alt))

    eps = 1e-15

    # True replication: like-vs-like rerun for same approx family (deterministic expectation ~0)
    t_approx_rep2, a_approx_rep2, _ = integrate(ic, params, RunConfig(dt=dt_main, method="euler", corrected=True))
    a_approx_rep2_on_exact = interp_to_grid(t_approx_rep2, a_approx_rep2, t_exact)
    rel_true_rep = np.abs(a_approx_rep2_on_exact - a_approx_on_exact) / (np.abs(a_approx_on_exact) + eps)
    true_replication_rel_diff = float(np.mean(rel_true_rep))

    # Method disagreement (previously mislabeled as replication)
    method_disagreement_rel_diff = float(abs(D_star_alt - D_star) / (abs(D_star) + eps))

    rel_exact_vs_approx = np.abs(a_approx_on_exact - a_exact) / (np.abs(a_exact) + eps)
    rel_exact_vs_alt = np.abs(a_alt_on_exact - a_exact) / (np.abs(a_exact) + eps)
    t_first_method_1pct = first_crossing_time(t_exact, rel_exact_vs_approx, threshold=1e-2)
    t_first_alt_1pct = first_crossing_time(t_exact, rel_exact_vs_alt, threshold=1e-2)

    stat_u = 0.0
    sys_u_q1 = float(max(baseline_refinement_error, corrected_refinement_error))
    epi_u_q1 = float(assumption_sensitivity_rel * abs(delta_proxy_l2))
    total_u_q1 = float(math.sqrt(stat_u**2 + sys_u_q1**2 + epi_u_q1**2))

    sys_u_q2 = float(abs(D_star_alt - D_star))
    epi_u_q2 = 0.0
    total_u_q2 = float(math.sqrt(stat_u**2 + sys_u_q2**2 + epi_u_q2**2))

    results = {
        "metadata": {
            "seed": seed,
            "units": "dimensionless",
            "model": "FRW-inspired minisuperspace toy ODE",
            "ic": asdict(ic),
            "params": asdict(params),
        },
        "thresholds": THRESHOLDS,
        "q1": {
            "delta_proxy_l2": delta_proxy_l2,
            "delta_proxy_max_abs": delta_proxy_max_abs,
            "delta_proxy_sign_final": delta_proxy_sign_final,
            "baseline_refinement_error": baseline_refinement_error,
            "corrected_refinement_error": corrected_refinement_error,
            "delta_proxy_n4_l2": delta_proxy_n4_l2,
            "assumption_sensitivity_rel": assumption_sensitivity_rel,
            "uncertainty": {
                "stat": stat_u,
                "sys": sys_u_q1,
                "epi": epi_u_q1,
                "total": total_u_q1,
            },
        },
        "q2": {
            "D_star": D_star,
            "D_max": D_max,
            "D_star_alt": D_star_alt,
            "D_max_alt": D_max_alt,
            "true_replication_rel_diff": true_replication_rel_diff,
            "method_disagreement_rel_diff": method_disagreement_rel_diff,
            "replication_rel_diff_legacy": method_disagreement_rel_diff,
            "t_first_method_disagreement_1pct": t_first_method_1pct,
            "t_first_alt_disagreement_1pct": t_first_alt_1pct,
            "uncertainty": {
                "stat": stat_u,
                "sys": sys_u_q2,
                "epi": epi_u_q2,
                "total": total_u_q2,
            },
        },
    }

    return results


def pass_fail_flags(results):
    q1 = results["q1"]
    q2 = results["q2"]
    t = THRESHOLDS

    return {
        "pass_q1_effect": q1["delta_proxy_l2"] >= t["q1_effect_persist_min"],
        "pass_q1_refinement": max(q1["baseline_refinement_error"], q1["corrected_refinement_error"]) <= t["q1_refinement_max"],
        "pass_q1_assumption": q1["assumption_sensitivity_rel"] <= t["q1_assumption_sensitivity_max"],
        "pass_q2_Dstar": q2["D_star"] >= t["q2_Dstar_min"],
        "pass_q2_true_replication": q2["true_replication_rel_diff"] <= t["q2_true_replication_rel_diff_max"],
        "pass_q2_method_disagreement": q2["method_disagreement_rel_diff"] <= t["q2_method_disagreement_rel_diff_max"],
    }


def linspace(a, b, n):
    return np.linspace(a, b, n).tolist()


def logspace(a, b, n):
    return np.logspace(np.log10(a), np.log10(b), n).tolist()


def main():
    parser = argparse.ArgumentParser(description="Batch runner for grqm_proxy_toymodel_v1")
    parser.add_argument("--alpha-min", type=float, default=1e-8)
    parser.add_argument("--alpha-max", type=float, default=1e-6)
    parser.add_argument("--alpha-n", type=int, default=7)
    parser.add_argument("--omega-m-min", type=float, default=0.25)
    parser.add_argument("--omega-m-max", type=float, default=0.35)
    parser.add_argument("--omega-m-n", type=int, default=3)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    outputs_root = root / "notebooks" / "outputs"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    batch_dir = outputs_root / f"grqm_batch_{ts}"
    batch_dir.mkdir(parents=True, exist_ok=True)

    alpha_values = logspace(args.alpha_min, args.alpha_max, args.alpha_n)
    omega_m_values = linspace(args.omega_m_min, args.omega_m_max, args.omega_m_n)

    rows = []
    run_idx = 0
    for alpha_qg in alpha_values:
        for omega_m in omega_m_values:
            omega_l = 1.0 - omega_m
            p = Params(omega_m=float(omega_m), omega_l=float(omega_l), alpha_qg=float(alpha_qg))
            result = evaluate_run(p, seed=args.seed)
            flags = pass_fail_flags(result)

            run_name = f"run_{run_idx:03d}_alpha_{alpha_qg:.3e}_om_{omega_m:.3f}"
            out_file = batch_dir / f"{run_name}.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)

            rows.append({
                "run_id": run_idx,
                "json_file": out_file.name,
                "alpha_qg": p.alpha_qg,
                "omega_m": p.omega_m,
                "omega_l": p.omega_l,
                "q1_delta_proxy_l2": result["q1"]["delta_proxy_l2"],
                "q1_refinement_max_obs": max(result["q1"]["baseline_refinement_error"], result["q1"]["corrected_refinement_error"]),
                "q1_assumption_sensitivity_rel": result["q1"]["assumption_sensitivity_rel"],
                "q2_D_star": result["q2"]["D_star"],
                "q2_true_replication_rel_diff": result["q2"]["true_replication_rel_diff"],
                "q2_method_disagreement_rel_diff": result["q2"]["method_disagreement_rel_diff"],
                "q2_replication_rel_diff_legacy": result["q2"]["replication_rel_diff_legacy"],
                "q2_t_first_method_disagreement_1pct": result["q2"]["t_first_method_disagreement_1pct"],
                **flags,
                "pass_all": all(flags.values()),
            })
            run_idx += 1

    summary_csv = batch_dir / "summary.csv"
    fieldnames = list(rows[0].keys()) if rows else ["run_id"]
    with open(summary_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    manifest = {
        "batch_dir": str(batch_dir),
        "n_runs": len(rows),
        "alpha_values": alpha_values,
        "omega_m_values": omega_m_values,
        "summary_csv": str(summary_csv),
        "thresholds": THRESHOLDS,
    }
    with open(batch_dir / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
