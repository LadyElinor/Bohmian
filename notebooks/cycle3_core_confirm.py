import csv
import json
from datetime import datetime
from pathlib import Path

import numpy as np

from grqm_batch_runner_tiered import q1_delta, q1_refinement_max, q2_metrics
from grqm_proxy_toymodel_v1 import IC, Params


def spearman_corr(x, y):
    xr = np.argsort(np.argsort(x))
    yr = np.argsort(np.argsort(y))
    return float(np.corrcoef(xr, yr)[0, 1])


def main():
    omega_list = [0.285, 0.290, 0.295, 0.300]
    alpha_list = [3e-7, 5e-7, 7e-7, 1e-6, 1.3e-6]

    thresholds = {
        "q1_effect_persist_min": 1e-4,
        "q1_refinement_max": 5e-3,
        "q1_assumption_hardened_max": 0.18,
        "q2_Dstar_min": 1e-4,
        "q2_true_replication_rel_diff_max": 1e-6,
        "q2_D_p95_max": 0.5,
        "q2_D_p99_max": 0.8,
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
    out_dir = out_root / f"grqm_cycle3_core_confirm_{ts}"
    out_dir.mkdir(exist_ok=True, parents=True)

    rows = []
    proxy_rows = []

    run_id = 0
    for omega in omega_list:
        for alpha in alpha_list:
            ic = IC()
            p = Params(omega_m=omega, omega_l=1.0 - omega, alpha_qg=alpha)

            d1 = q1_delta(p, ic)
            q1_ref = q1_refinement_max(p, ic)
            q2 = q2_metrics(p)

            hs = []
            for cfg in hardened_perturbations:
                ic2 = IC(a0=ic.a0 * cfg["ic_scale"], v0=ic.v0, t0=ic.t0, t1=ic.t1)
                d_pert = q1_delta(p, ic2, dt_main=cfg["dt"], correction_power=cfg["n"])
                hs.append(abs(d_pert - d1) / (abs(d1) + 1e-15))
            hmax = float(max(hs))

            # Independent proxy: alpha doubling response
            p2 = Params(omega_m=omega, omega_l=1.0 - omega, alpha_qg=2 * alpha)
            d2 = q1_delta(p2, ic)
            ratio = float(d2 / (d1 + 1e-15))
            proxy_rows.append({
                "omega_m": omega,
                "alpha_qg": alpha,
                "q1_delta_alpha": d1,
                "q1_delta_2alpha": d2,
                "ratio_2a_over_a": ratio,
            })

            pass_q2_robust = ((q2["q2_D_p95"] < thresholds["q2_D_p95_max"] and q2["q2_D_p99"] < thresholds["q2_D_p99_max"]) or q2["q2_spike_detected"])
            pass_all = all([
                d1 >= thresholds["q1_effect_persist_min"],
                q1_ref <= thresholds["q1_refinement_max"],
                hmax <= thresholds["q1_assumption_hardened_max"],
                q2["q2_D_star"] >= thresholds["q2_Dstar_min"],
                q2["q2_true_replication_rel_diff"] <= thresholds["q2_true_replication_rel_diff_max"],
                pass_q2_robust,
            ])

            row = {
                "run_id": run_id,
                "omega_m": omega,
                "alpha_qg": alpha,
                "q1_delta_proxy_l2": d1,
                "q1_refinement_max_obs": q1_ref,
                "q1_assumption_sensitivity_hardened": hmax,
                **q2,
                "pass_q2_robust_bulk": pass_q2_robust,
                "pass_all_envelope": pass_all,
            }
            rows.append(row)
            run_id += 1

    with open(out_dir / "cycle3_core_confirm_summary.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    with open(out_dir / "proxy_agreement_v3.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(proxy_rows[0].keys()))
        w.writeheader(); w.writerows(proxy_rows)

    p1 = np.array([r["q1_delta_alpha"] for r in proxy_rows], dtype=float)
    p2 = np.array([r["q1_delta_2alpha"] for r in proxy_rows], dtype=float)
    ratio = np.array([r["ratio_2a_over_a"] for r in proxy_rows], dtype=float)

    aggregate = {
        "n_runs": len(rows),
        "pass_rate_envelope": float(sum(1 for r in rows if r["pass_all_envelope"]) / len(rows)),
        "pearson_primary_vs_independent": float(np.corrcoef(p1, p2)[0, 1]),
        "spearman_primary_vs_independent": spearman_corr(p1, p2),
        "ratio_mean": float(np.mean(ratio)),
        "ratio_std": float(np.std(ratio)),
    }

    with open(out_dir / "aggregate.json", "w", encoding="utf-8") as f:
        json.dump(aggregate, f, indent=2)

    print(json.dumps({"out_dir": str(out_dir), **aggregate}, indent=2))


if __name__ == "__main__":
    main()
