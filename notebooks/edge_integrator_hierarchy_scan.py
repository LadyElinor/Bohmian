from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

from grqm.core import IC, Params, RunConfig, integrate


def integrate_adaptive(ic: IC, p: Params, method: str, corrected: bool, correction_power: int, t_eval, rtol: float, atol: float):
    def rhs(_t, y):
        a, v = y
        if a <= 0:
            return [0.0, 0.0]
        base = -(p.omega_m) / (2.0 * a * a) + p.omega_l * a
        corr = p.alpha_qg / (a**correction_power) if corrected else 0.0
        return [v, base + corr]

    sol = solve_ivp(
        rhs,
        t_span=(ic.t0, ic.t1),
        y0=np.array([ic.a0, ic.v0], dtype=float),
        method=method,
        t_eval=t_eval,
        rtol=rtol,
        atol=atol,
    )
    if not sol.success:
        raise RuntimeError(f"{method} failed: {sol.message}")
    return sol.y[0]


def q2_metrics(a_approx: np.ndarray, a_exact: np.ndarray, t: np.ndarray):
    d = np.abs(a_approx - a_exact)
    p95 = float(np.quantile(d, 0.95))
    p99 = float(np.quantile(d, 0.99))
    dstar = float(np.mean(d))
    idx = np.where(d > 0.01)[0]
    t_first = float(t[idx[0]]) if len(idx) else None
    return dstar, p95, p99, t_first


def main():
    root = Path(__file__).resolve().parents[1]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = root / "notebooks" / "outputs" / f"grqm_edge_integrator_hierarchy_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    ic = IC()
    edge_points = [(0.305, 3e-7), (0.305, 7e-7), (0.305, 1.3e-6)]
    dt_nominal = 1e-3
    t_eval = np.linspace(ic.t0, ic.t1, int(round((ic.t1 - ic.t0) / dt_nominal)) + 1)

    ref_rtol, ref_atol = 1e-11, 1e-13
    compare_tol_sets = [(1e-8, 1e-10), (1e-10, 1e-12)]

    rows = []

    for omega_m, alpha_qg in edge_points:
        p = Params(omega_m=omega_m, omega_l=1.0 - omega_m, alpha_qg=alpha_qg)

        a_ref = integrate_adaptive(ic, p, "DOP853", corrected=True, correction_power=5, t_eval=t_eval, rtol=ref_rtol, atol=ref_atol)

        # RK4 fixed-step at nominal dt
        _, a_rk4, _ = integrate(ic, p, RunConfig(dt=dt_nominal, method="rk4", corrected=True, correction_power=5))
        dstar, p95, p99, tf = q2_metrics(a_rk4, a_ref, t_eval)
        rows.append({
            "omega_m": omega_m,
            "alpha_qg": alpha_qg,
            "solver": "rk4_fixed",
            "rtol": None,
            "atol": None,
            "q2_D_star": dstar,
            "q2_D_p95": p95,
            "q2_D_p99": p99,
            "q2_t_first_1pct": tf,
        })

        for method in ("DOP853", "LSODA", "Radau"):
            for rtol, atol in compare_tol_sets:
                a_cmp = integrate_adaptive(ic, p, method, corrected=True, correction_power=5, t_eval=t_eval, rtol=rtol, atol=atol)
                dstar, p95, p99, tf = q2_metrics(a_cmp, a_ref, t_eval)
                rows.append({
                    "omega_m": omega_m,
                    "alpha_qg": alpha_qg,
                    "solver": method,
                    "rtol": rtol,
                    "atol": atol,
                    "q2_D_star": dstar,
                    "q2_D_p95": p95,
                    "q2_D_p99": p99,
                    "q2_t_first_1pct": tf,
                })

    # suppression vs rk4 per point (using tight tolerance rows)
    suppress = []
    for omega_m, alpha_qg in edge_points:
        rk = next(r for r in rows if r["omega_m"] == omega_m and r["alpha_qg"] == alpha_qg and r["solver"] == "rk4_fixed")
        rk_p95 = rk["q2_D_p95"]
        for method in ("DOP853", "LSODA", "Radau"):
            tight = next(r for r in rows if r["omega_m"] == omega_m and r["alpha_qg"] == alpha_qg and r["solver"] == method and r["rtol"] == 1e-10)
            sup = 1.0 - (tight["q2_D_p95"] / (rk_p95 + 1e-30))
            suppress.append({
                "omega_m": omega_m,
                "alpha_qg": alpha_qg,
                "method": method,
                "suppression_vs_rk4_p95": float(sup),
            })

    with (out_dir / "edge_integrator_hierarchy.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    with (out_dir / "edge_integrator_suppression.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(suppress[0].keys()))
        w.writeheader()
        w.writerows(suppress)

    summary = {
        "timestamp": datetime.now().isoformat(),
        "edge_points": edge_points,
        "reference": {"method": "DOP853", "rtol": ref_rtol, "atol": ref_atol, "t_eval_dt": dt_nominal},
        "criterion_hint": ">=0.90 suppression_vs_rk4_p95 indicates dominant numerical-path contribution",
        "max_suppression_by_method": {
            m: float(max(r["suppression_vs_rk4_p95"] for r in suppress if r["method"] == m))
            for m in ("DOP853", "LSODA", "Radau")
        },
        "min_suppression_by_method": {
            m: float(min(r["suppression_vs_rk4_p95"] for r in suppress if r["method"] == m))
            for m in ("DOP853", "LSODA", "Radau")
        },
    }

    (out_dir / "edge_integrator_hierarchy_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps({"out_dir": str(out_dir), "summary": summary}, indent=2))


if __name__ == "__main__":
    main()
