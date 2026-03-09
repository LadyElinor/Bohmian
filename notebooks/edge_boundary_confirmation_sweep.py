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


def rhs(_t, y, omega_m: float, alpha_qg: float, corrected: bool, correction_power: int = 5):
    a, v = y
    if a <= 0:
        return [0.0, 0.0]
    base = -(omega_m) / (2.0 * a * a) + (1.0 - omega_m) * a
    corr = alpha_qg / (a**correction_power) if corrected else 0.0
    return [v, base + corr]


def l2_rel_err(err, ref, eps=1e-15):
    num = float(np.sqrt(np.mean(err**2)))
    den = float(np.sqrt(np.mean(ref**2)) + eps)
    return num / den


def integrate_dense(omega_m, alpha_qg, corrected, rtol=1e-10, atol=1e-12, a0=IC.a0, v0=IC.v0):
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
        dense_output=True,
        events=event_stop,
        jac=None,
    )
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol


def q1_refine_adaptive(omega_m: float, alpha_qg: float, dt_main=2e-4):
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


def ratio_diagnostic(omega_m: float, alpha_qg: float):
    sol = integrate_dense(omega_m, alpha_qg, True, rtol=1e-11, atol=1e-13)
    t = np.linspace(IC.t0, float(sol.t[-1]), 12000)
    a = np.clip(sol.sol(t)[0], 1e-12, None)
    base_mag = np.abs(-(omega_m) / (2.0 * a * a) + (1.0 - omega_m) * a)
    corr_mag = np.abs(alpha_qg / (a**5))
    ratio = corr_mag / (base_mag + 1e-18)
    i = int(np.argmin(a))
    return float(np.max(ratio)), float(a[i])


def main():
    root = Path(__file__).resolve().parents[1]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = root / "notebooks" / "outputs" / f"grqm_edge_boundary_sweep_omega031_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    omega_m = 0.31
    alpha_vals = np.geomspace(3e-7, 1.3e-6, 8)
    q1_threshold = 1e-6

    rows = []
    for aq in alpha_vals:
        q1r = q1_refine_adaptive(omega_m, float(aq), dt_main=2e-4)
        ratio_max, min_a = ratio_diagnostic(omega_m, float(aq))
        row = {
            "omega_m": omega_m,
            "alpha_qg": float(aq),
            "q1_refinement_max_obs": q1r,
            "ratio_correction_over_classical_max": ratio_max,
            "min_a": min_a,
            "pass_q1_refinement": q1r <= q1_threshold,
            "ratio_exceeds_1": ratio_max > 1.0,
        }
        rows.append(row)
        print(
            f"done om={omega_m:.3f} aq={aq:.3e} q1_ref={q1r:.3e} ratio_max={ratio_max:.3f} pass_ref={row['pass_q1_refinement']}",
            flush=True,
        )

    with (out_dir / "edge_boundary_sweep_summary.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    agg = {
        "omega_m": omega_m,
        "n_rows": len(rows),
        "q1_refinement_threshold": q1_threshold,
        "pass_q1_refinement_rate": float(sum(1 for r in rows if r["pass_q1_refinement"]) / len(rows)),
        "max_q1_refinement": float(max(r["q1_refinement_max_obs"] for r in rows)),
        "min_q1_refinement": float(min(r["q1_refinement_max_obs"] for r in rows)),
        "max_ratio_correction_over_classical": float(max(r["ratio_correction_over_classical_max"] for r in rows)),
        "min_ratio_correction_over_classical": float(min(r["ratio_correction_over_classical_max"] for r in rows)),
        "min_of_min_a": float(min(r["min_a"] for r in rows)),
        "all_ratio_exceeds_1": bool(all(r["ratio_exceeds_1"] for r in rows)),
    }
    (out_dir / "edge_boundary_sweep_aggregate.json").write_text(json.dumps(agg, indent=2), encoding="utf-8")

    print(json.dumps({"out_dir": str(out_dir), **agg}, indent=2), flush=True)


if __name__ == "__main__":
    main()
