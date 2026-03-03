import csv
import json
from datetime import datetime
from pathlib import Path

import numpy as np

from grqm_proxy_toymodel_v1 import IC, Params, RunConfig, integrate, interp_to_grid


def first_crossing_time(t, rel_err, threshold=1e-2):
    idx = np.where(rel_err >= threshold)[0]
    return None if len(idx) == 0 else float(t[idx[0]])


def run_point(alpha_qg, omega_m=0.30):
    p = Params(omega_m=omega_m, omega_l=1.0 - omega_m, alpha_qg=float(alpha_qg))
    ic = IC()
    eps = 1e-15

    # references
    t_ref1, a_ref1, _ = integrate(ic, p, RunConfig(dt=2.5e-4, method="rk4", corrected=True))
    t_ref2, a_ref2, _ = integrate(ic, p, RunConfig(dt=1.25e-4, method="rk4", corrected=True))

    # approximations
    t_eu, a_eu, _ = integrate(ic, p, RunConfig(dt=1e-3, method="euler", corrected=True))
    t_rk4c, a_rk4c, _ = integrate(ic, p, RunConfig(dt=2e-3, method="rk4", corrected=True))

    a_eu_ref1 = interp_to_grid(t_eu, a_eu, t_ref1)
    a_rk4c_ref1 = interp_to_grid(t_rk4c, a_rk4c, t_ref1)
    a_ref2_on_ref1 = interp_to_grid(t_ref2, a_ref2, t_ref1)

    # method disagreement against ref1
    D_star_euler_ref1 = float(np.mean(np.abs(a_eu_ref1 - a_ref1)))
    D_star_rk4c_ref1 = float(np.mean(np.abs(a_rk4c_ref1 - a_ref1)))
    method_disagreement_rel_diff = float(abs(D_star_rk4c_ref1 - D_star_euler_ref1) / (abs(D_star_euler_ref1) + eps))

    rel_eu_ref1 = np.abs(a_eu_ref1 - a_ref1) / (np.abs(a_ref1) + eps)
    t_first_1pct = first_crossing_time(t_ref1, rel_eu_ref1, 1e-2)

    # reference hierarchy consistency
    ref_hierarchy_rel = float(np.mean(np.abs(a_ref2_on_ref1 - a_ref1) / (np.abs(a_ref2_on_ref1) + eps)))

    return {
        "alpha_qg": float(alpha_qg),
        "omega_m": omega_m,
        "q2_D_star_euler_ref1": D_star_euler_ref1,
        "q2_D_star_rk4c_ref1": D_star_rk4c_ref1,
        "q2_method_disagreement_rel_diff": method_disagreement_rel_diff,
        "q2_t_first_method_disagreement_1pct": t_first_1pct,
        "q2_ref_hierarchy_rel_ref2_vs_ref1": ref_hierarchy_rel,
    }


def main():
    alpha_values = [1.0e-7, 1.5e-7, 2.1544346900318822e-7, 3.0e-7, 4.6415888336127725e-7, 7.0e-7, 1.0e-6, 1.5e-6, 2.0e-6, 3.0e-6]

    root = Path(__file__).resolve().parents[1]
    out_root = root / "notebooks" / "outputs"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = out_root / f"grqm_q2_calibration_extended_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = [run_point(a) for a in alpha_values]

    with open(out_dir / "summary.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    # quick trend stats
    a = np.array([r["alpha_qg"] for r in rows], dtype=float)
    t = np.array([r["q2_t_first_method_disagreement_1pct"] if r["q2_t_first_method_disagreement_1pct"] is not None else np.nan for r in rows], dtype=float)
    valid = ~np.isnan(t)
    corr = float(np.corrcoef(a[valid], t[valid])[0, 1]) if valid.sum() > 2 else None

    manifest = {
        "out_dir": str(out_dir),
        "n_runs": len(rows),
        "alpha_values": alpha_values,
        "corr_alpha_vs_t_first": corr,
    }
    with open(out_dir / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
