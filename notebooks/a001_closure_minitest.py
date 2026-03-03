import csv
import json
from datetime import datetime
from pathlib import Path

from grqm_batch_runner_tiered import q1_delta, q1_refinement_max, q2_metrics
from grqm_proxy_toymodel_v1 import IC, Params


def main():
    # Narrow in-core sweep for A-001 closure evidence
    points = [
        {"omega_m": 0.295, "alpha_qg": 5e-7},
        {"omega_m": 0.300, "alpha_qg": 5e-7},
        {"omega_m": 0.295, "alpha_qg": 1.0e-6},
        {"omega_m": 0.300, "alpha_qg": 1.0e-6},
    ]

    orderings = [4, 5, 6]
    dts = [8e-4, 1e-3, 1.2e-3]

    criteria = {
        "q1_delta_min": 1e-4,
        "q1_refine_max": 5e-3,
        "q2_p95_max": 0.5,
        "q2_p99_max": 0.8,
        "q2_replication_rel_diff_max": 1e-6,
    }

    root = Path(__file__).resolve().parents[1]
    out_root = root / "notebooks" / "outputs"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = out_root / f"grqm_a001_closure_minitest_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    for pt in points:
        p = Params(omega_m=pt["omega_m"], omega_l=1.0 - pt["omega_m"], alpha_qg=pt["alpha_qg"])
        ic = IC()
        for n in orderings:
            for dt in dts:
                q1 = q1_delta(p, ic, dt_main=dt, correction_power=n)
                q1_ref = q1_refinement_max(p, ic, dt_main=dt, correction_power=n)
                q2 = q2_metrics(p)

                pass_q1 = (q1 >= criteria["q1_delta_min"]) and (q1_ref <= criteria["q1_refine_max"])
                pass_q2 = (
                    (q2["q2_D_p95"] <= criteria["q2_p95_max"]) and
                    (q2["q2_D_p99"] <= criteria["q2_p99_max"]) and
                    (q2["q2_true_replication_rel_diff"] <= criteria["q2_replication_rel_diff_max"])
                )

                rows.append({
                    "omega_m": pt["omega_m"],
                    "alpha_qg": pt["alpha_qg"],
                    "correction_power_n": n,
                    "dt_main": dt,
                    "q1_delta_proxy_l2": q1,
                    "q1_refinement_max_obs": q1_ref,
                    "q2_D_p95": q2["q2_D_p95"],
                    "q2_D_p99": q2["q2_D_p99"],
                    "q2_true_replication_rel_diff": q2["q2_true_replication_rel_diff"],
                    "pass_q1": pass_q1,
                    "pass_q2": pass_q2,
                    "pass_joint": pass_q1 and pass_q2,
                })

    fields = list(rows[0].keys())
    with open(out_dir / "a001_minitest_summary.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    n = len(rows)
    agg = {
        "n_runs": n,
        "criteria": criteria,
        "pass_q1_rate": sum(1 for r in rows if r["pass_q1"]) / n,
        "pass_q2_rate": sum(1 for r in rows if r["pass_q2"]) / n,
        "pass_joint_rate": sum(1 for r in rows if r["pass_joint"]) / n,
        "max_q1_sensitivity_vs_n5_dt1e3": None,
    }

    # sensitivity relative to local baseline n=5, dt=1e-3 per point
    sens = []
    for pt in points:
        base = [r for r in rows if r["omega_m"] == pt["omega_m"] and r["alpha_qg"] == pt["alpha_qg"] and r["correction_power_n"] == 5 and abs(r["dt_main"] - 1e-3) < 1e-15][0]
        b = abs(base["q1_delta_proxy_l2"]) + 1e-15
        for r in [x for x in rows if x["omega_m"] == pt["omega_m"] and x["alpha_qg"] == pt["alpha_qg"]]:
            sens.append(abs(r["q1_delta_proxy_l2"] - base["q1_delta_proxy_l2"]) / b)
    agg["max_q1_sensitivity_vs_n5_dt1e3"] = max(sens)

    with open(out_dir / "aggregate.json", "w", encoding="utf-8") as f:
        json.dump(agg, f, indent=2)

    print(json.dumps({"out_dir": str(out_dir), **agg}, indent=2))


if __name__ == "__main__":
    main()
