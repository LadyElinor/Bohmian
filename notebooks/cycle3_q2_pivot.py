import csv
import json
from datetime import datetime
from pathlib import Path

import numpy as np

from grqm_proxy_toymodel_v1 import IC, Params, accel, integrate, RunConfig, interp_to_grid


def first_crossing_time(t, rel_err, threshold=1e-2):
    idx = np.where(rel_err >= threshold)[0]
    return None if len(idx) == 0 else float(t[idx[0]])


def robust_q2_metrics(a_approx_on_ref, a_ref, t_ref):
    eps = 1e-15
    abs_err = np.abs(a_approx_on_ref - a_ref)
    rel_err = abs_err / (np.abs(a_ref) + eps)
    return {
        "D_star": float(np.mean(abs_err)),
        "D_p95": float(np.percentile(abs_err, 95)),
        "D_trimmed": float(np.mean(np.sort(abs_err)[int(0.05*len(abs_err)):int(0.95*len(abs_err))])),
        "t_first_1pct": first_crossing_time(t_ref, rel_err, 1e-2),
    }


def run_dop853(alpha_qg, omega_m):
    try:
        from scipy.integrate import solve_ivp
    except Exception:
        return None, "scipy unavailable"

    p = Params(omega_m=omega_m, omega_l=1.0 - omega_m, alpha_qg=alpha_qg)
    ic = IC()

    def f(t, y):
        a, v = y
        return [v, accel(a, p, corrected=True, correction_power=5)]

    t_ref, a_ref, _ = integrate(ic, p, RunConfig(dt=2.5e-4, method="rk4", corrected=True))
    sol = solve_ivp(f, (ic.t0, ic.t1), [ic.a0, ic.v0], method="DOP853", t_eval=t_ref, rtol=1e-10, atol=1e-12)
    if not sol.success:
        return None, f"DOP853 failed: {sol.message}"

    a_new = sol.y[0]
    m = robust_q2_metrics(a_new, a_ref, t_ref)
    return {"a_ref": a_ref, "t_ref": t_ref, "metrics": m}, None


def run_baseline(alpha_qg, omega_m):
    p = Params(omega_m=omega_m, omega_l=1.0 - omega_m, alpha_qg=alpha_qg)
    ic = IC()
    t_ref, a_ref, _ = integrate(ic, p, RunConfig(dt=2.5e-4, method="rk4", corrected=True))
    t_eu, a_eu, _ = integrate(ic, p, RunConfig(dt=1e-3, method="euler", corrected=True))
    a_eu_on_ref = interp_to_grid(t_eu, a_eu, t_ref)
    return robust_q2_metrics(a_eu_on_ref, a_ref, t_ref)


def main():
    points = [
        {"omega_m": 0.295, "alpha_qg": 3e-7},
        {"omega_m": 0.295, "alpha_qg": 1.3e-6},
        {"omega_m": 0.300, "alpha_qg": 3e-7},
        {"omega_m": 0.300, "alpha_qg": 1.3e-6},
        {"omega_m": 0.295, "alpha_qg": 7e-7},
        {"omega_m": 0.300, "alpha_qg": 7e-7},
    ]

    root = Path(__file__).resolve().parents[1]
    out_root = root / "notebooks" / "outputs"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = out_root / f"grqm_cycle3_q2_pivot_{ts}"
    out_dir.mkdir(exist_ok=True, parents=True)

    rows = []
    for p in points:
        base = run_baseline(p["alpha_qg"], p["omega_m"])
        dop, err = run_dop853(p["alpha_qg"], p["omega_m"])

        if dop is None:
            rows.append({**p, "error": err})
            continue

        new = dop["metrics"]
        imp_p95 = 100.0 * (base["D_p95"] - new["D_p95"]) / (base["D_p95"] + 1e-15)

        base_t = base["t_first_1pct"]
        new_t = new["t_first_1pct"]
        if (base_t is None) or (new_t is None):
            imp_t = None
            t_gate = False
        else:
            imp_t = 100.0 * ((new_t - base_t) / (base_t + 1e-15))
            t_gate = imp_t >= 20.0

        rows.append({
            **p,
            "base_p95": base["D_p95"],
            "new_p95": new["D_p95"],
            "base_t_first": base_t,
            "new_t_first": new_t,
            "p95_improvement_pct": imp_p95,
            "t_first_improvement_pct": imp_t,
            "pivot_success_20pct": (imp_p95 >= 20.0) or t_gate,
        })

    with open(out_dir / "cycle3_q2_pivot_summary.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    print(json.dumps({"out_dir": str(out_dir), "n_rows": len(rows)}, indent=2))


if __name__ == "__main__":
    main()
