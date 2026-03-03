import csv
import json
from datetime import datetime
from pathlib import Path

import numpy as np

from grqm_proxy_toymodel_v1 import IC, Params, RunConfig, integrate, interp_to_grid


def first_crossing_time(t, rel_err, threshold=1e-2):
    idx = np.where(rel_err >= threshold)[0]
    return None if len(idx) == 0 else float(t[idx[0]])


def trimmed_mean(x, trim=0.05):
    x = np.sort(np.asarray(x))
    n = len(x)
    k = int(n * trim)
    if 2 * k >= n:
        return float(np.mean(x))
    return float(np.mean(x[k:n-k]))


def run_point(alpha_qg, dt_euler=1e-3, omega_m=0.30):
    p = Params(omega_m=omega_m, omega_l=1.0 - omega_m, alpha_qg=float(alpha_qg))
    ic = IC()
    eps = 1e-15

    t_ref, a_ref, _ = integrate(ic, p, RunConfig(dt=1.25e-4, method="rk4", corrected=True))
    t_eu, a_eu, _ = integrate(ic, p, RunConfig(dt=dt_euler, method="euler", corrected=True))
    t_rk4c, a_rk4c, _ = integrate(ic, p, RunConfig(dt=2e-3, method="rk4", corrected=True))

    a_eu_ref = interp_to_grid(t_eu, a_eu, t_ref)
    a_rk4c_ref = interp_to_grid(t_rk4c, a_rk4c, t_ref)

    abs_err = np.abs(a_eu_ref - a_ref)
    rel_err = abs_err / (np.abs(a_ref) + eps)

    D_star = float(np.mean(abs_err))
    D_median = float(np.median(abs_err))
    D_trim = trimmed_mean(abs_err, 0.05)
    D_p95 = float(np.percentile(abs_err, 95))
    D_p99 = float(np.percentile(abs_err, 99))
    D_max = float(np.max(abs_err))

    D_star_rk4c = float(np.mean(np.abs(a_rk4c_ref - a_ref)))
    method_disagreement_rel_diff = float(abs(D_star_rk4c - D_star) / (abs(D_star) + eps))

    spike_ratio = D_max / (D_median + eps)
    q2_spike_detected = spike_ratio > 1000.0

    return {
        "alpha_qg": float(alpha_qg),
        "dt_euler": float(dt_euler),
        "q2_D_star": D_star,
        "q2_D_median": D_median,
        "q2_D_trimmed_mean": D_trim,
        "q2_D_p95": D_p95,
        "q2_D_p99": D_p99,
        "q2_D_max": D_max,
        "q2_spike_ratio_max_over_median": float(spike_ratio),
        "q2_spike_detected": bool(q2_spike_detected),
        "q2_t_first_method_disagreement_1pct": first_crossing_time(t_ref, rel_err, 1e-2),
        "q2_method_disagreement_rel_diff": method_disagreement_rel_diff,
    }


def main():
    alpha_values = [1e-7, 1.2e-7, 1.5e-7, 1.8e-7, 2.1544346900318822e-7, 3e-7, 4.6415888336127725e-7, 7e-7, 1e-6, 1.5e-6, 2e-6, 3e-6]

    root = Path(__file__).resolve().parents[1]
    out_root = root / "notebooks" / "outputs"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = out_root / f"grqm_q2_calibration_robust_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = [run_point(a, dt_euler=1e-3) for a in alpha_values]

    with open(out_dir / "summary.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    with open(out_dir / "manifest.json", "w", encoding="utf-8") as f:
        json.dump({"out_dir": str(out_dir), "n_runs": len(rows), "alpha_values": alpha_values}, f, indent=2)

    print(json.dumps({"out_dir": str(out_dir), "n_runs": len(rows)}, indent=2))


if __name__ == "__main__":
    main()
