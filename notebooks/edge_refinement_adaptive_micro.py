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


def integrate_dense(omega_m: float, alpha_qg: float, corrected: bool, rtol=1e-10, atol=1e-12):
    def event_stop(_t, y):
        return y[0] - 1e-7

    event_stop.terminal = True
    event_stop.direction = -1

    sol = solve_ivp(
        fun=lambda t, y: rhs(t, y, omega_m, alpha_qg, corrected),
        t_span=(IC.t0, IC.t1),
        y0=[IC.a0, IC.v0],
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


def q1_refine_adaptive(omega_m: float, alpha_qg: float, dt_main=1e-4):
    t_m = np.linspace(IC.t0, IC.t1, int(round((IC.t1 - IC.t0) / dt_main)) + 1)
    t_r = np.linspace(IC.t0, IC.t1, int(round((IC.t1 - IC.t0) / (dt_main / 2))) + 1)

    b = integrate_dense(omega_m, alpha_qg, corrected=False)
    c = integrate_dense(omega_m, alpha_qg, corrected=True)

    a_b_m = b.sol(t_m)[0]
    a_c_m = c.sol(t_m)[0]
    a_b_r = b.sol(t_r)[0]
    a_c_r = c.sol(t_r)[0]

    a_b_m_on_r = np.interp(t_r, t_m, a_b_m)
    a_c_m_on_r = np.interp(t_r, t_m, a_c_m)

    e1 = l2_rel_err(a_b_m_on_r - a_b_r, a_b_r)
    e2 = l2_rel_err(a_c_m_on_r - a_c_r, a_c_r)
    return float(max(e1, e2))


def main():
    root = Path(__file__).resolve().parents[1]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = root / "notebooks" / "outputs" / f"grqm_edge_refinement_adaptive_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    targets = [
        (0.3075, 7e-7),
        (0.3075, 1e-6),
        (0.31, 7e-7),
        (0.31, 1e-6),
    ]

    threshold = 1e-6
    rows = []
    for om, aq in targets:
        r = q1_refine_adaptive(om, aq, dt_main=1e-4)
        rows.append({
            "omega_m": om,
            "alpha_qg": aq,
            "q1_refine_adaptive_dt1e4": r,
            "pass": r <= threshold,
        })

    with (out_dir / "edge_refinement_adaptive_summary.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    agg = {
        "n_rows": len(rows),
        "max_q1_refine": float(max(r["q1_refine_adaptive_dt1e4"] for r in rows)),
        "threshold": threshold,
        "pass_rate": float(sum(1 for r in rows if r["pass"]) / len(rows)),
    }
    (out_dir / "edge_refinement_adaptive_aggregate.json").write_text(json.dumps(agg, indent=2), encoding="utf-8")
    print(json.dumps({"out_dir": str(out_dir), **agg}, indent=2))


if __name__ == "__main__":
    main()
