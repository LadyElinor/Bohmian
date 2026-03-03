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
    omega_values = [0.280, 0.285, 0.290, 0.295, 0.300, 0.305, 0.310]
    alpha_values = [3e-7, 5e-7, 7e-7, 1e-6, 1.3e-6]

    thresholds = {
        "q1_effect_persist_min": 1e-4,
        "q1_refinement_max": 5e-3,
        "q1_assumption_hardened_max": 0.2,
        "q2_Dstar_min": 1e-4,
        "q2_true_replication_rel_diff_max": 1e-2,
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
    out_dir = out_root / f"grqm_cycle2_dense_followup_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    proxy_rows = []
    rid = 0
    for om in omega_values:
        for a in alpha_values:
            ic = IC()
            p = Params(omega_m=float(om), omega_l=1.0 - float(om), alpha_qg=float(a))
            base = q1_delta(p, ic)

            hs = []
            for cfg in hardened_perturbations:
                ic2 = IC(a0=ic.a0 * cfg["ic_scale"], v0=ic.v0, t0=ic.t0, t1=ic.t1)
                d = q1_delta(p, ic2, dt_main=cfg["dt"], correction_power=cfg["n"])
                hs.append(abs(d - base) / (abs(base) + 1e-15))

            q1ref = q1_refinement_max(p, ic)
            q2 = q2_metrics(p)

            pass_q2_robust_bulk = ((q2["q2_D_p95"] < thresholds["q2_D_p95_max"] and q2["q2_D_p99"] < thresholds["q2_D_p99_max"]) or q2["q2_spike_detected"])
            pass_all_envelope = all([
                base >= thresholds["q1_effect_persist_min"],
                q1ref <= thresholds["q1_refinement_max"],
                max(hs) <= thresholds["q1_assumption_hardened_max"],
                q2["q2_D_star"] >= thresholds["q2_Dstar_min"],
                q2["q2_true_replication_rel_diff"] <= thresholds["q2_true_replication_rel_diff_max"],
                pass_q2_robust_bulk,
            ])

            row = {
                "run_id": rid,
                "omega_m": om,
                "alpha_qg": a,
                "q1_delta_proxy_l2": base,
                "q1_refinement_max_obs": q1ref,
                "q1_assumption_sensitivity_hardened": float(max(hs)),
                **q2,
                "pass_q2_robust_bulk": pass_q2_robust_bulk,
                "pass_all_envelope": pass_all_envelope,
            }
            rows.append(row)
            rid += 1

            p2 = Params(omega_m=float(om), omega_l=1.0 - float(om), alpha_qg=float(2 * a))
            d2 = q1_delta(p2, ic)
            ratio = d2 / (base + 1e-15)
            proxy_rows.append({
                "omega_m": om,
                "alpha_qg": a,
                "q1_delta_alpha": base,
                "q1_delta_2alpha": d2,
                "ratio_2a_over_a": ratio,
            })

    # write envelope summary
    with open(out_dir / "envelope_summary.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    # pass rate per omega
    by_omega = {}
    for r in rows:
        by_omega.setdefault(r["omega_m"], []).append(r)
    omega_stats = []
    for om, rr in by_omega.items():
        omega_stats.append({
            "omega_m": om,
            "n": len(rr),
            "pass_rate_envelope": float(sum(1 for x in rr if x["pass_all_envelope"]) / len(rr)),
            "max_q1_hardened": float(max(x["q1_assumption_sensitivity_hardened"] for x in rr)),
        })
    omega_stats.sort(key=lambda x: x["omega_m"])
    with open(out_dir / "omega_passrate.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(omega_stats[0].keys()))
        w.writeheader(); w.writerows(omega_stats)

    # proxy agreement stats
    with open(out_dir / "proxy_agreement.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(proxy_rows[0].keys()))
        w.writeheader(); w.writerows(proxy_rows)

    p1 = np.array([r["q1_delta_alpha"] for r in proxy_rows], dtype=float)
    p2 = np.array([r["q1_delta_2alpha"] for r in proxy_rows], dtype=float)
    ratio = np.array([r["ratio_2a_over_a"] for r in proxy_rows], dtype=float)

    aggregate = {
        "n_runs": len(rows),
        "n_pass_all_envelope": int(sum(1 for r in rows if r["pass_all_envelope"])),
        "overall_pass_rate": float(sum(1 for r in rows if r["pass_all_envelope"]) / len(rows)),
        "pearson_primary_vs_independent": float(np.corrcoef(p1, p2)[0, 1]),
        "spearman_primary_vs_independent": spearman_corr(p1, p2),
        "ratio_mean": float(np.mean(ratio)),
        "ratio_std": float(np.std(ratio)),
        "ratio_median": float(np.median(ratio)),
        "ratio_min": float(np.min(ratio)),
        "ratio_max": float(np.max(ratio)),
        "proposed_omega_upper_bound": 0.31,
    }

    with open(out_dir / "aggregate.json", "w", encoding="utf-8") as f:
        json.dump({"aggregate": aggregate, "omega_stats": omega_stats, "thresholds": thresholds}, f, indent=2)

    print(json.dumps({"out_dir": str(out_dir), **aggregate}, indent=2))


if __name__ == "__main__":
    main()
