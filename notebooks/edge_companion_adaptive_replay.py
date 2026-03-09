from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


class IC:
    t0 = 0.0
    t1 = 3.0
    a0 = 0.1
    v0 = 1.5


def l2_rel_err(err, ref, eps=1e-15):
    num = float(np.sqrt(np.mean((err) ** 2)))
    den = float(np.sqrt(np.mean(ref**2)) + eps)
    return num / den


def rhs(_t, y, omega_m: float, alpha_qg: float, corrected: bool, correction_power: int = 5):
    a, v = y
    if a <= 0:
        return [0.0, 0.0]
    base = -(omega_m) / (2.0 * a * a) + (1.0 - omega_m) * a
    corr = alpha_qg / (a**correction_power) if corrected else 0.0
    return [v, base + corr]


def integrate_dense(omega_m, alpha_qg, corrected, rtol=1e-10, atol=1e-12, a0=0.1, v0=1.5):
    def event_stop(_t, y):
        return y[0] - 1e-7

    event_stop.terminal = True
    event_stop.direction = -1

    sol = solve_ivp(
        fun=lambda t, y: rhs(t, y, omega_m, alpha_qg, corrected),
        t_span=(IC.t0, IC.t1),
        y0=[a0, v0],
        method="Radau",
        rtol=rtol,
        atol=atol,
        max_step=1e-4,
        first_step=2e-6,
        events=event_stop,
        dense_output=True,
    )
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol


def q1_delta(omega_m: float, alpha_qg: float, dt_eval: float, a0=0.1, v0=1.5):
    t = np.linspace(IC.t0, IC.t1, int(round((IC.t1 - IC.t0) / dt_eval)) + 1)
    b = integrate_dense(omega_m, alpha_qg, False, a0=a0, v0=v0)
    c = integrate_dense(omega_m, alpha_qg, True, a0=a0, v0=v0)
    a_b = b.sol(t)[0]
    a_c = c.sol(t)[0]
    return float(l2_rel_err(a_c - a_b, a_b)), t, a_b, a_c


def q1_refine_adaptive(omega_m: float, alpha_qg: float, dt_main=1e-4):
    t_m = np.linspace(IC.t0, IC.t1, int(round((IC.t1 - IC.t0) / dt_main)) + 1)
    t_r = np.linspace(IC.t0, IC.t1, int(round((IC.t1 - IC.t0) / (dt_main / 2))) + 1)

    b = integrate_dense(omega_m, alpha_qg, False)
    c = integrate_dense(omega_m, alpha_qg, True)

    a_b_m = b.sol(t_m)[0]
    a_c_m = c.sol(t_m)[0]
    a_b_r = b.sol(t_r)[0]
    a_c_r = c.sol(t_r)[0]

    a_b_m_on_r = np.interp(t_r, t_m, a_b_m)
    a_c_m_on_r = np.interp(t_r, t_m, a_c_m)

    e1 = l2_rel_err(a_b_m_on_r - a_b_r, a_b_r)
    e2 = l2_rel_err(a_c_m_on_r - a_c_r, a_c_r)
    return float(max(e1, e2))


def q2_robust_radau_only(omega_m: float, alpha_qg: float, dt_eval=1e-3):
    t = np.linspace(IC.t0, IC.t1, int(round((IC.t1 - IC.t0) / dt_eval)) + 1)
    r1 = integrate_dense(omega_m, alpha_qg, True, rtol=1e-10, atol=1e-12)
    r2 = integrate_dense(omega_m, alpha_qg, True, rtol=1e-10, atol=1e-12)
    a1 = r1.sol(t)[0]
    a2 = r2.sol(t)[0]
    d = np.abs(a2 - a1)
    return float(np.quantile(d, 0.95)), float(np.quantile(d, 0.99))


def replication_rel_diff(omega_m: float, alpha_qg: float, dt_eval=1e-3):
    t = np.linspace(IC.t0, IC.t1, int(round((IC.t1 - IC.t0) / dt_eval)) + 1)
    r1 = integrate_dense(omega_m, alpha_qg, True, rtol=1e-10, atol=1e-12)
    r2 = integrate_dense(omega_m, alpha_qg, True, rtol=1e-10, atol=1e-12)
    a1 = r1.sol(t)[0]
    a2 = r2.sol(t)[0]
    rel = np.abs(a2 - a1) / (np.abs(a1) + 1e-15)
    return float(np.mean(rel))


def main():
    root = Path(__file__).resolve().parents[1]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = root / "notebooks" / "outputs" / f"grqm_edge_companion_adaptive_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    omega_vals = [0.305, 0.3075, 0.31]
    alpha_vals = [3e-7, 5e-7, 7e-7, 1e-6, 1.3e-6]

    thresholds = {
        "q1_refinement_max": 1e-6,
        "q1_assumption_sensitivity_hardened_max": 0.18,
        "q2_D_p95_max": 0.01,
        "q2_D_p99_max": 0.05,
        "q2_true_replication_rel_diff_max": 1e-6,
    }

    hardening = [
        dict(ic_scale=0.999, dt=1e-3),
        dict(ic_scale=1.001, dt=1e-3),
        dict(ic_scale=1.0, dt=9e-4),
        dict(ic_scale=1.0, dt=1.1e-3),
    ]

    rows = []
    for om in omega_vals:
        for aq in alpha_vals:
            d_base, _, _, _ = q1_delta(om, aq, 1e-3)
            q1r = q1_refine_adaptive(om, aq, dt_main=1e-4)

            hs = []
            for h in hardening:
                d_pert, _, _, _ = q1_delta(om, aq, h["dt"], a0=IC.a0 * h["ic_scale"], v0=IC.v0)
                hs.append(abs(d_pert - d_base) / (abs(d_base) + 1e-15))
            hmax = float(max(hs))

            p95, p99 = q2_robust_radau_only(om, aq)
            rep = replication_rel_diff(om, aq)

            row = {
                "omega_m": om,
                "alpha_qg": aq,
                "q1_delta_proxy_l2": d_base,
                "q1_refinement_max_obs": q1r,
                "q1_assumption_sensitivity_hardened": hmax,
                "q2_D_p95_worst_method": p95,
                "q2_D_p99_worst_method": p99,
                "q2_true_replication_rel_diff": rep,
                "pass_q1_refinement": q1r <= thresholds["q1_refinement_max"],
                "pass_q1_hardened": hmax <= thresholds["q1_assumption_sensitivity_hardened_max"],
                "pass_q2_robust": (p95 <= thresholds["q2_D_p95_max"] and p99 <= thresholds["q2_D_p99_max"]),
                "pass_q2_replication": rep <= thresholds["q2_true_replication_rel_diff_max"],
            }
            row["pass_all_packet"] = all([
                row["pass_q1_refinement"],
                row["pass_q1_hardened"],
                row["pass_q2_robust"],
                row["pass_q2_replication"],
            ])
            rows.append(row)

    with (out_dir / "edge_companion_adaptive_summary.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    agg = {
        "n_rows": len(rows),
        "pass_all_packet_rate": float(sum(1 for r in rows if r["pass_all_packet"]) / len(rows)),
        "max_q1_refinement": float(max(r["q1_refinement_max_obs"] for r in rows)),
        "max_q1_hardened": float(max(r["q1_assumption_sensitivity_hardened"] for r in rows)),
        "max_q2_p95": float(max(r["q2_D_p95_worst_method"] for r in rows)),
        "max_q2_p99": float(max(r["q2_D_p99_worst_method"] for r in rows)),
        "max_replication": float(max(r["q2_true_replication_rel_diff"] for r in rows)),
        "thresholds": thresholds,
    }
    (out_dir / "edge_companion_adaptive_aggregate.json").write_text(json.dumps(agg, indent=2), encoding="utf-8")

    print(json.dumps({"out_dir": str(out_dir), **agg}, indent=2))


if __name__ == "__main__":
    main()
