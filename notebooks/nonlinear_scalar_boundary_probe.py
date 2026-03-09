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


def rhs(_t, y, omega_m: float, alpha_qg: float, lam: float):
    a, v = y
    if a <= 0:
        return [0.0, 0.0]
    classical = -(omega_m) / (2.0 * a * a) + (1.0 - omega_m) * a
    # exploratory nonlinear scalar-inspired damping term (toy)
    nonlinear = -lam * (a ** 3)
    corr = alpha_qg / (a**5) + nonlinear
    return [v, classical + corr]


def run_case(omega_m: float, alpha_qg: float, lam: float):
    def event_stop(_t, y):
        return y[0] - 1e-7

    event_stop.terminal = True
    event_stop.direction = -1

    sol = solve_ivp(
        fun=lambda t, y: rhs(t, y, omega_m, alpha_qg, lam),
        t_span=(IC.t0, IC.t1),
        y0=[IC.a0, IC.v0],
        method="Radau",
        rtol=1e-9,
        atol=1e-11,
        max_step=1e-4,
        first_step=2e-6,
        dense_output=True,
        events=event_stop,
        jac=None,
    )
    if not sol.success:
        return {"ok": False, "error": str(sol.message)}

    t = np.linspace(IC.t0, float(sol.t[-1]), 6000)
    a = np.clip(sol.sol(t)[0], 1e-12, None)
    classical = np.abs(-(omega_m) / (2.0 * a * a) + (1.0 - omega_m) * a)
    corr = np.abs(alpha_qg / (a**5) - lam * (a ** 3))
    ratio = corr / (classical + 1e-18)

    # lightweight refinement proxy (adaptive two-grid eval)
    tm = np.linspace(IC.t0, IC.t1, int(round((IC.t1 - IC.t0) / 2e-4)) + 1)
    tr = np.linspace(IC.t0, IC.t1, int(round((IC.t1 - IC.t0) / 1e-4)) + 1)
    am = sol.sol(tm)[0]
    ar = sol.sol(tr)[0]
    am_on_r = np.interp(tr, tm, am)
    q1_ref = float(np.sqrt(np.mean((am_on_r - ar) ** 2)) / (np.sqrt(np.mean(ar**2)) + 1e-15))

    return {
        "ok": True,
        "max_ratio": float(np.max(ratio)),
        "min_a": float(np.min(a)),
        "q1_refinement_proxy": q1_ref,
    }


def main():
    root = Path(__file__).resolve().parents[1]
    out_dir = root / "notebooks" / "outputs" / f"grqm_nonlinear_scalar_probe_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    out_dir.mkdir(parents=True, exist_ok=True)

    omega_m = 0.31
    alpha_vals = [3e-7, 7e-7, 1.3e-6]
    lambda_vals = [0.0, 1e-5, 1e-4, 1e-3]

    rows = []
    for lam in lambda_vals:
        for aq in alpha_vals:
            r = run_case(omega_m, aq, lam)
            row = {"omega_m": omega_m, "alpha_qg": aq, "lambda": lam, **r}
            rows.append(row)
            if r.get("ok"):
                print(f"done lam={lam:.1e} aq={aq:.1e} max_ratio={r['max_ratio']:.3f} q1_ref={r['q1_refinement_proxy']:.3e}", flush=True)
            else:
                print(f"fail lam={lam:.1e} aq={aq:.1e} err={r.get('error')}", flush=True)

    valid = [r for r in rows if r.get("ok")]
    summary = {
        "omega_m": omega_m,
        "n_cases": len(rows),
        "n_valid": len(valid),
        "best_max_ratio": float(min(r["max_ratio"] for r in valid)) if valid else None,
        "any_ratio_below_1": bool(any(r["max_ratio"] < 1.0 for r in valid)),
        "best_q1_refinement_proxy": float(min(r["q1_refinement_proxy"] for r in valid)) if valid else None,
        "out_dir": str(out_dir),
        "rows": rows,
    }

    (out_dir / "nonlinear_scalar_probe_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
