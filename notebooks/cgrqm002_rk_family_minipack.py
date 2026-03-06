from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

from grqm.core import IC, Params, RunConfig, integrate


def integrate_adaptive(ic: IC, p: Params, method: str, t_eval: np.ndarray, rtol: float, atol: float) -> np.ndarray:
    def rhs(_t, y):
        a, v = y
        if a <= 0:
            return [0.0, 0.0]
        base = -(p.omega_m) / (2.0 * a * a) + p.omega_l * a
        corr = p.alpha_qg / (a**5)
        return [v, base + corr]

    sol = solve_ivp(
        rhs,
        (ic.t0, ic.t1),
        [ic.a0, ic.v0],
        method=method,
        t_eval=t_eval,
        rtol=rtol,
        atol=atol,
    )
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol.y[0]


def metrics(a_cmp: np.ndarray, a_ref: np.ndarray) -> dict:
    d = np.abs(a_cmp - a_ref)
    med = float(np.median(d))
    p95 = float(np.quantile(d, 0.95))
    p99 = float(np.quantile(d, 0.99))
    dstar = float(np.mean(d))
    spike = float((np.max(d) + 1e-30) / (med + 1e-30))
    return {
        "q2_D_star": dstar,
        "q2_D_median": med,
        "q2_D_p95": p95,
        "q2_D_p99": p99,
        "q2_spike_ratio": spike,
    }


def main():
    root = Path(__file__).resolve().parents[1]
    out_root = root / "notebooks" / "outputs"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = out_root / f"grqm_cgrqm002_rk_family_minipack_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    ic = IC()
    points = [
        (0.295, 3e-7),
        (0.295, 7e-7),
        (0.295, 1.3e-6),
        (0.300, 3e-7),
        (0.300, 7e-7),
        (0.300, 1.3e-6),
    ]

    dt_eval = 1e-3
    t_eval = np.linspace(ic.t0, ic.t1, int(round((ic.t1 - ic.t0) / dt_eval)) + 1)

    ref_method = "DOP853"
    ref_rtol, ref_atol = 1e-12, 1e-14
    rk_family = [("RK23", 1e-10, 1e-12), ("RK45", 1e-10, 1e-12), ("DOP853", 1e-10, 1e-12)]

    rows = []
    point_summary = []

    for omega_m, alpha_qg in points:
        p = Params(omega_m=omega_m, omega_l=1.0 - omega_m, alpha_qg=alpha_qg)
        a_ref = integrate_adaptive(ic, p, ref_method, t_eval, ref_rtol, ref_atol)

        per_method = []
        for method, rtol, atol in rk_family:
            a_cmp = integrate_adaptive(ic, p, method, t_eval, rtol, atol)
            m = metrics(a_cmp, a_ref)
            m.update({"omega_m": omega_m, "alpha_qg": alpha_qg, "method": method, "rtol": rtol, "atol": atol})
            rows.append(m)
            per_method.append(m)

        p95_vals = [r["q2_D_p95"] for r in per_method]
        p99_vals = [r["q2_D_p99"] for r in per_method]
        abs_spread_p95 = max(p95_vals) - min(p95_vals)
        rel_spread_p95 = (max(p95_vals) - min(p95_vals)) / (max(p95_vals) + 1e-30)

        # deterministic replication check via fixed-step RK4 rerun equivalence on same point
        _, a1, _ = integrate(ic, p, RunConfig(dt=1e-3, method="rk4", corrected=True, correction_power=5))
        _, a2, _ = integrate(ic, p, RunConfig(dt=1e-3, method="rk4", corrected=True, correction_power=5))
        rep = float(np.max(np.abs(a1 - a2)) / (np.max(np.abs(a1)) + 1e-30))

        point_summary.append(
            {
                "omega_m": omega_m,
                "alpha_qg": alpha_qg,
                "max_q2_D_p95": float(max(p95_vals)),
                "max_q2_D_p99": float(max(p99_vals)),
                "rk_family_abs_spread_p95": float(abs_spread_p95),
                "rk_family_rel_spread_p95": float(rel_spread_p95),
                "q2_true_replication_rel_diff": rep,
                "pass_acceptance": bool(max(p95_vals) <= 0.5 and max(p99_vals) <= 0.8 and abs_spread_p95 <= 1e-8 and rep <= 1e-6),
            }
        )

    with (out_dir / "rk_family_method_rows.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    with (out_dir / "rk_family_point_summary.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(point_summary[0].keys()))
        w.writeheader()
        w.writerows(point_summary)

    summary = {
        "out_dir": str(out_dir),
        "n_points": len(points),
        "all_points_pass": bool(all(r["pass_acceptance"] for r in point_summary)),
        "global_max_q2_D_p95": float(max(r["max_q2_D_p95"] for r in point_summary)),
        "global_max_q2_D_p99": float(max(r["max_q2_D_p99"] for r in point_summary)),
        "global_max_rk_family_abs_spread_p95": float(max(r["rk_family_abs_spread_p95"] for r in point_summary)),
        "global_max_rk_family_rel_spread_p95": float(max(r["rk_family_rel_spread_p95"] for r in point_summary)),
        "global_max_replication_rel_diff": float(max(r["q2_true_replication_rel_diff"] for r in point_summary)),
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
