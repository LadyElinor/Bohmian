import csv
import json
from datetime import datetime
from pathlib import Path

from grqm_batch_runner_tiered import q1_delta, q1_refinement_max, q2_metrics
from grqm_proxy_toymodel_v1 import IC, Params


def main():
    points = [
        {"omega_m": 0.295, "alpha_qg": 5e-7},
        {"omega_m": 0.300, "alpha_qg": 5e-7},
        {"omega_m": 0.295, "alpha_qg": 1.0e-6},
        {"omega_m": 0.300, "alpha_qg": 1.0e-6},
    ]

    orderings = [4, 5, 6]
    dts = [8e-4, 9e-4, 1e-3, 1.1e-3, 1.2e-3]

    # Candidate least-invasive A-001 policy bound (data-checked):
    # keep prior dt mini-test window; classify n=6 as stress-only.
    proposed_policy = {
        "ordering_n_allowed": [4, 5],
        "dt_main_min": 8e-4,
        "dt_main_max": 1.2e-3,
        "max_local_sensitivity_vs_n5_dt1e3": 1.0,
        "q1_refine_max": 5e-3,
        "q2_p95_max": 0.5,
        "q2_p99_max": 0.8,
        "q2_replication_rel_diff_max": 1e-6,
    }

    root = Path(__file__).resolve().parents[1]
    out_root = root / "notebooks" / "outputs"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = out_root / f"grqm_a001_local_boundary_sweep_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    for pt in points:
        p = Params(omega_m=pt["omega_m"], omega_l=1.0 - pt["omega_m"], alpha_qg=pt["alpha_qg"])
        ic = IC()
        base_q1 = q1_delta(p, ic, dt_main=1e-3, correction_power=5)
        q2 = q2_metrics(p)

        for n in orderings:
            for dt in dts:
                q1 = q1_delta(p, ic, dt_main=dt, correction_power=n)
                q1_ref = q1_refinement_max(p, ic, dt_main=dt, correction_power=n)
                sens = abs(q1 - base_q1) / (abs(base_q1) + 1e-15)

                in_policy = (
                    n in proposed_policy["ordering_n_allowed"]
                    and proposed_policy["dt_main_min"] <= dt <= proposed_policy["dt_main_max"]
                )
                pass_local_stability = sens <= proposed_policy["max_local_sensitivity_vs_n5_dt1e3"]
                pass_q1_ref = q1_ref <= proposed_policy["q1_refine_max"]
                pass_q2 = (
                    q2["q2_D_p95"] <= proposed_policy["q2_p95_max"]
                    and q2["q2_D_p99"] <= proposed_policy["q2_p99_max"]
                    and q2["q2_true_replication_rel_diff"] <= proposed_policy["q2_replication_rel_diff_max"]
                )

                rows.append({
                    "omega_m": pt["omega_m"],
                    "alpha_qg": pt["alpha_qg"],
                    "correction_power_n": n,
                    "dt_main": dt,
                    "q1_delta_proxy_l2": q1,
                    "q1_refinement_max_obs": q1_ref,
                    "q1_local_sensitivity_vs_n5_dt1e3": sens,
                    "q2_D_p95": q2["q2_D_p95"],
                    "q2_D_p99": q2["q2_D_p99"],
                    "q2_true_replication_rel_diff": q2["q2_true_replication_rel_diff"],
                    "in_policy": in_policy,
                    "pass_local_stability": pass_local_stability,
                    "pass_q1_refinement": pass_q1_ref,
                    "pass_q2": pass_q2,
                    "pass_a001_policy": in_policy and pass_local_stability and pass_q1_ref and pass_q2,
                })

    with open(out_dir / "a001_local_boundary_sweep.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    n_total = len(rows)
    in_policy = [r for r in rows if r["in_policy"]]
    out_policy = [r for r in rows if not r["in_policy"]]

    agg = {
        "n_runs": n_total,
        "n_in_policy": len(in_policy),
        "n_out_of_policy": len(out_policy),
        "proposed_policy": proposed_policy,
        "in_policy_pass_rate": sum(1 for r in in_policy if r["pass_a001_policy"]) / max(len(in_policy), 1),
        "out_of_policy_pass_rate": sum(1 for r in out_policy if r["pass_a001_policy"]) / max(len(out_policy), 1),
        "in_policy_max_local_sensitivity": max(r["q1_local_sensitivity_vs_n5_dt1e3"] for r in in_policy),
        "out_of_policy_min_local_sensitivity": min(r["q1_local_sensitivity_vs_n5_dt1e3"] for r in out_policy),
        "out_of_policy_max_local_sensitivity": max(r["q1_local_sensitivity_vs_n5_dt1e3"] for r in out_policy),
        "global_q1_refinement_max_obs": max(r["q1_refinement_max_obs"] for r in rows),
        "global_q2_p95_max": max(r["q2_D_p95"] for r in rows),
        "global_q2_p99_max": max(r["q2_D_p99"] for r in rows),
        "global_q2_replication_rel_diff_max": max(r["q2_true_replication_rel_diff"] for r in rows),
    }

    with open(out_dir / "aggregate.json", "w", encoding="utf-8") as f:
        json.dump(agg, f, indent=2)

    print(json.dumps({"out_dir": str(out_dir), **agg}, indent=2))


if __name__ == "__main__":
    main()
