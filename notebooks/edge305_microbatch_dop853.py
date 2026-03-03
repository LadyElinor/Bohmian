import csv
import json
from datetime import datetime
from pathlib import Path

import numpy as np

from grqm_proxy_toymodel_v1 import IC, Params, accel, integrate, RunConfig


def first_crossing_time(t, rel_err, threshold=1e-2):
    idx = np.where(rel_err >= threshold)[0]
    return None if len(idx) == 0 else float(t[idx[0]])


def robust_metrics(a_cmp, a_ref, t_ref):
    eps = 1e-15
    abs_err = np.abs(a_cmp - a_ref)
    rel_err = abs_err / (np.abs(a_ref) + eps)
    return {
        "D_star": float(np.mean(abs_err)),
        "D_median": float(np.median(abs_err)),
        "D_p95": float(np.percentile(abs_err, 95)),
        "D_p99": float(np.percentile(abs_err, 99)),
        "t_first_1pct": first_crossing_time(t_ref, rel_err, 1e-2),
    }


def run_point(alpha_qg, omega_m=0.305):
    try:
        from scipy.integrate import solve_ivp
    except Exception as e:
        return {"alpha_qg": alpha_qg, "error": f"scipy unavailable: {e}"}

    ic = IC()
    p = Params(omega_m=omega_m, omega_l=1.0 - omega_m, alpha_qg=alpha_qg)

    # Small-dt RK4 reference
    t_ref, a_ref, _ = integrate(ic, p, RunConfig(dt=1.25e-4, method="rk4", corrected=True))

    def f(t, y):
        a, v = y
        return [v, accel(a, p, corrected=True, correction_power=5)]

    sol = solve_ivp(
        f,
        (ic.t0, ic.t1),
        [ic.a0, ic.v0],
        method="DOP853",
        t_eval=t_ref,
        rtol=1e-10,
        atol=1e-12,
    )

    if not sol.success:
        return {"alpha_qg": alpha_qg, "error": f"DOP853 failed: {sol.message}"}

    m = robust_metrics(sol.y[0], a_ref, t_ref)
    return {
        "alpha_qg": alpha_qg,
        "omega_m": omega_m,
        "ref_dt": 1.25e-4,
        "cmp_method": "DOP853",
        "cmp_rtol": 1e-10,
        "cmp_atol": 1e-12,
        "q2_D_star": m["D_star"],
        "q2_D_median": m["D_median"],
        "q2_D_p95": m["D_p95"],
        "q2_D_p99": m["D_p99"],
        "q2_t_first_1pct": m["t_first_1pct"],
    }


def main():
    alpha_list = [3e-7, 7e-7, 1.3e-6]

    root = Path(__file__).resolve().parents[1]
    out_root = root / "notebooks" / "outputs"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = out_root / f"grqm_edge305_microbatch_dop853_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = [run_point(a) for a in alpha_list]

    with open(out_dir / "edge305_microbatch_summary.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    ok_rows = [r for r in rows if "error" not in r]
    agg = {
        "n_points": len(rows),
        "n_success": len(ok_rows),
        "max_q2_D_p95": (max(r["q2_D_p95"] for r in ok_rows) if ok_rows else None),
        "max_q2_D_p99": (max(r["q2_D_p99"] for r in ok_rows) if ok_rows else None),
        "any_1pct_crossing": any(r["q2_t_first_1pct"] is not None for r in ok_rows) if ok_rows else None,
        "note": "Mitigation evidence only; does not expand envelope by itself.",
    }

    with open(out_dir / "aggregate.json", "w", encoding="utf-8") as f:
        json.dump(agg, f, indent=2)

    print(json.dumps({"out_dir": str(out_dir), **agg}, indent=2))


if __name__ == "__main__":
    main()
