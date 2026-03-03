import csv
import json
from datetime import datetime
from pathlib import Path

import numpy as np

from grqm_batch_runner_tiered import q1_delta, q1_refinement_max, q2_metrics
from grqm_proxy_toymodel_v1 import IC, Params


def evaluate_point(omega, alpha, hardening_perturbations, thresholds):
    ic = IC()
    p = Params(omega_m=omega, omega_l=1.0 - omega, alpha_qg=alpha)

    d1 = q1_delta(p, ic)
    q1_ref = q1_refinement_max(p, ic)
    q2 = q2_metrics(p)

    hs = []
    for cfg in hardening_perturbations:
        ic2 = IC(a0=ic.a0 * cfg["ic_scale"], v0=ic.v0, t0=ic.t0, t1=ic.t1)
        d_pert = q1_delta(p, ic2, dt_main=cfg["dt"], correction_power=cfg["n"])
        hs.append(abs(d_pert - d1) / (abs(d1) + 1e-15))
    hmax = float(max(hs))

    pass_q2_robust = ((q2["q2_D_p95"] < thresholds["q2_D_p95_max"] and q2["q2_D_p99"] < thresholds["q2_D_p99_max"]) or q2["q2_spike_detected"])
    pass_all = all([
        d1 >= thresholds["q1_effect_persist_min"],
        q1_ref <= thresholds["q1_refinement_max"],
        hmax <= thresholds["q1_assumption_hardened_max"],
        q2["q2_D_star"] >= thresholds["q2_Dstar_min"],
        q2["q2_true_replication_rel_diff"] <= thresholds["q2_true_replication_rel_diff_max"],
        pass_q2_robust,
    ])

    return {
        "omega_m": omega,
        "alpha_qg": alpha,
        "q1_delta_proxy_l2": d1,
        "q1_refinement_max_obs": q1_ref,
        "q1_assumption_sensitivity_hardened": hmax,
        **q2,
        "pass_q2_robust_bulk": pass_q2_robust,
        "pass_all_envelope": pass_all,
    }


def summarize(rows, gate=0.18):
    arr = np.array([r["q1_assumption_sensitivity_hardened"] for r in rows], dtype=float)
    return {
        "n": int(len(rows)),
        "q1_assumption_sensitivity_hardened_min": float(arr.min()),
        "q1_assumption_sensitivity_hardened_max": float(arr.max()),
        "q1_assumption_sensitivity_hardened_mean": float(arr.mean()),
        "pass_fraction_q1_gate": float(np.mean(arr <= gate)),
        "pass_fraction_all_envelope": float(np.mean([bool(r["pass_all_envelope"]) for r in rows])),
    }


def main():
    # Keep cycle-4 grid/envelope pipeline; only swap hardening to cycle-3 logic.
    subset_points = [
        (0.290, 7e-7),
        (0.295, 7e-7),
        (0.300, 7e-7),
    ]

    thresholds = {
        "q1_effect_persist_min": 1e-4,
        "q1_refinement_max": 5e-3,
        "q1_assumption_hardened_max": 0.18,
        "q2_Dstar_min": 1e-4,
        "q2_true_replication_rel_diff_max": 1e-6,
        "q2_D_p95_max": 0.5,
        "q2_D_p99_max": 0.8,
    }

    cycle4_policy_perturbations = [
        dict(ic_scale=0.9993, dt=8e-4, n=4),
        dict(ic_scale=1.0009, dt=8e-4, n=4),
        dict(ic_scale=0.9993, dt=1.2e-3, n=5),
        dict(ic_scale=1.0009, dt=1.2e-3, n=5),
    ]

    cycle3_hardening_perturbations = [
        dict(ic_scale=0.999, dt=1e-3, n=5),
        dict(ic_scale=1.001, dt=1e-3, n=5),
        dict(ic_scale=1.0, dt=9e-4, n=5),
        dict(ic_scale=1.0, dt=1.1e-3, n=5),
    ]

    root = Path(__file__).resolve().parents[1]
    out_root = root / "notebooks" / "outputs"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = out_root / f"grqm_quick_revert_hardening_{ts}"
    out_dir.mkdir(exist_ok=True, parents=True)

    rows_policy = []
    rows_revert = []
    for omega, alpha in subset_points:
        rows_policy.append(evaluate_point(omega, alpha, cycle4_policy_perturbations, thresholds))
        rows_revert.append(evaluate_point(omega, alpha, cycle3_hardening_perturbations, thresholds))

    # Write row-level comparison
    compare_rows = []
    for p, r in zip(rows_policy, rows_revert):
        compare_rows.append({
            "omega_m": p["omega_m"],
            "alpha_qg": p["alpha_qg"],
            "policy_q1_assumption_sensitivity_hardened": p["q1_assumption_sensitivity_hardened"],
            "revert_q1_assumption_sensitivity_hardened": r["q1_assumption_sensitivity_hardened"],
            "delta_revert_minus_policy": r["q1_assumption_sensitivity_hardened"] - p["q1_assumption_sensitivity_hardened"],
            "policy_pass_all_envelope": p["pass_all_envelope"],
            "revert_pass_all_envelope": r["pass_all_envelope"],
        })

    with open(out_dir / "subset_policy_rows.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_policy[0].keys()))
        w.writeheader(); w.writerows(rows_policy)

    with open(out_dir / "subset_revert_rows.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_revert[0].keys()))
        w.writeheader(); w.writerows(rows_revert)

    with open(out_dir / "subset_compare.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(compare_rows[0].keys()))
        w.writeheader(); w.writerows(compare_rows)

    payload = {
        "subset_points": [{"omega_m": o, "alpha_qg": a} for o, a in subset_points],
        "thresholds": thresholds,
        "cycle4_policy_signature": cycle4_policy_perturbations,
        "cycle3_revert_signature": cycle3_hardening_perturbations,
        "policy_summary": summarize(rows_policy, gate=thresholds["q1_assumption_hardened_max"]),
        "revert_summary": summarize(rows_revert, gate=thresholds["q1_assumption_hardened_max"]),
    }

    with open(out_dir / "aggregate.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(json.dumps({"out_dir": str(out_dir), **payload}, indent=2))


if __name__ == "__main__":
    main()
