from __future__ import annotations

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


def classical_accel(a: float, omega_m: float) -> float:
    return -(omega_m) / (2.0 * a * a) + (1.0 - omega_m) * a


def rho_toy(a: float, omega_m: float, alpha_qg: float) -> float:
    return omega_m / (a**3) + alpha_qg / (a**5)


def run_semiclassical_reference(omega_m: float, alpha_qg: float):
    def rhs(_t, y):
        a, v = y
        if a <= 0:
            return [0.0, 0.0]
        cls = classical_accel(a, omega_m)
        corr = alpha_qg / (a**5)
        return [v, cls + corr]

    def event_stop(_t, y):
        return y[0] - 1e-7

    event_stop.terminal = True
    event_stop.direction = -1

    sol = solve_ivp(
        rhs,
        (IC.t0, IC.t1),
        [IC.a0, IC.v0],
        method="Radau",
        rtol=1e-9,
        atol=1e-11,
        max_step=1e-4,
        first_step=2e-6,
        dense_output=True,
        events=event_stop,
    )
    if not sol.success:
        raise RuntimeError(sol.message)

    t = np.linspace(IC.t0, float(sol.t[-1]), 6000)
    a = np.clip(sol.sol(t)[0], 1e-12, None)
    rho = rho_toy(a, omega_m, alpha_qg)
    i_min = int(np.argmin(a))
    return {
        "min_a": float(a[i_min]),
        "rho_at_min_a": float(rho[i_min]),
        "rho_peak": float(np.max(rho)),
    }


def run_lqc_case(omega_m: float, alpha_qg: float, rho_crit: float):
    def rhs(_t, y):
        a, v = y
        if a <= 0:
            return [0.0, 0.0]
        cls = classical_accel(a, omega_m)
        rho = rho_toy(a, omega_m, alpha_qg)
        factor = 1.0 - rho / rho_crit
        return [v, cls * factor]

    def event_stop(_t, y):
        return y[0] - 1e-7

    event_stop.terminal = True
    event_stop.direction = -1

    sol = solve_ivp(
        rhs,
        (IC.t0, IC.t1),
        [IC.a0, IC.v0],
        method="Radau",
        rtol=1e-9,
        atol=1e-11,
        max_step=1e-4,
        first_step=2e-6,
        dense_output=True,
        events=event_stop,
    )
    if not sol.success:
        return {"ok": False, "error": str(sol.message)}

    t = np.linspace(IC.t0, float(sol.t[-1]), 6000)
    a = np.clip(sol.sol(t)[0], 1e-12, None)
    cls = np.abs(classical_accel(a, omega_m))
    rho = rho_toy(a, omega_m, alpha_qg)
    corr_like = np.abs(classical_accel(a, omega_m) * (-rho / rho_crit))
    ratio = corr_like / (cls + 1e-18)

    i_peak = int(np.argmax(ratio))
    i_min = int(np.argmin(a))

    tm = np.linspace(IC.t0, IC.t1, int(round((IC.t1 - IC.t0) / 2e-4)) + 1)
    tr = np.linspace(IC.t0, IC.t1, int(round((IC.t1 - IC.t0) / 1e-4)) + 1)
    am = sol.sol(tm)[0]
    ar = sol.sol(tr)[0]
    am_on_r = np.interp(tr, tm, am)
    q1_ref = float(np.sqrt(np.mean((am_on_r - ar) ** 2)) / (np.sqrt(np.mean(ar**2)) + 1e-15))

    return {
        "ok": True,
        "max_ratio_correction_over_classical": float(ratio[i_peak]),
        "a_at_peak_ratio": float(a[i_peak]),
        "rho_at_peak_ratio": float(rho[i_peak]),
        "min_a": float(a[i_min]),
        "rho_at_min_a": float(rho[i_min]),
        "rho_peak": float(np.max(rho)),
        "q1_refinement_proxy": q1_ref,
        "pass_ratio_lt_1": bool(float(ratio[i_peak]) < 1.0),
        "pass_q1_refinement": bool(q1_ref <= 1e-6),
    }


def main():
    root = Path(__file__).resolve().parents[1]
    out_dir = root / "notebooks" / "outputs" / f"grqm_lqc_boundary_probe_v2_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    out_dir.mkdir(parents=True, exist_ok=True)

    omega_m = 0.31
    alpha_vals = [3e-7, 7e-7, 1.3e-6]

    # calibrate rho scale from semiclassical reference at boundary mid alpha
    alpha_ref = 7e-7
    ref = run_semiclassical_reference(omega_m, alpha_ref)
    rho_scale = ref["rho_at_min_a"]
    rho_mults = [0.5, 1.0, 2.0]

    rows = []
    for m in rho_mults:
        rho_crit = m * rho_scale
        for aq in alpha_vals:
            r = run_lqc_case(omega_m, aq, rho_crit)
            row = {
                "omega_m": omega_m,
                "alpha_qg": aq,
                "rho_scale": rho_scale,
                "rho_crit_mult": m,
                "rho_crit": rho_crit,
                **r,
            }
            rows.append(row)
            if r.get("ok"):
                print(
                    f"done mult={m:.1f} aq={aq:.1e} max_ratio={r['max_ratio_correction_over_classical']:.3f} min_a={r['min_a']:.4f} q1_ref={r['q1_refinement_proxy']:.3e}",
                    flush=True,
                )
            else:
                print(f"fail mult={m:.1f} aq={aq:.1e} err={r.get('error')}", flush=True)

    valid = [r for r in rows if r.get("ok")]
    summary = {
        "omega_m": omega_m,
        "n_cases": len(rows),
        "n_valid": len(valid),
        "rho_scale_calibration": {
            "alpha_ref": alpha_ref,
            **ref,
            "rho_scale_used": rho_scale,
        },
        "rho_crit_multipliers": rho_mults,
        "best_max_ratio": float(min(r["max_ratio_correction_over_classical"] for r in valid)) if valid else None,
        "worst_max_ratio": float(max(r["max_ratio_correction_over_classical"] for r in valid)) if valid else None,
        "any_ratio_below_1": bool(any(r["pass_ratio_lt_1"] for r in valid)),
        "q1_refinement_pass_rate": float(sum(1 for r in valid if r["pass_q1_refinement"]) / len(valid)) if valid else 0.0,
        "min_of_min_a": float(min(r["min_a"] for r in valid)) if valid else None,
        "out_dir": str(out_dir),
        "rows": rows,
    }

    (out_dir / "lqc_boundary_probe_v2_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
