import csv
import json
from datetime import datetime
from pathlib import Path

import numpy as np

from grqm_proxy_toymodel_v1 import IC, Params, RunConfig, integrate, interp_to_grid


def first_crossing_time(t, rel_err, threshold=1e-2):
    idx = np.where(rel_err >= threshold)[0]
    return None if len(idx) == 0 else float(t[idx[0]])


def run_case(alpha_qg, dt_euler):
    p = Params(omega_m=0.30, omega_l=0.70, alpha_qg=float(alpha_qg))
    ic = IC()
    eps = 1e-15

    t_ref, a_ref, _ = integrate(ic, p, RunConfig(dt=1.25e-4, method="rk4", corrected=True))
    t_eu, a_eu, _ = integrate(ic, p, RunConfig(dt=dt_euler, method="euler", corrected=True))

    a_eu_on_ref = interp_to_grid(t_eu, a_eu, t_ref)
    abs_err = np.abs(a_eu_on_ref - a_ref)
    rel_err = abs_err / (np.abs(a_ref) + eps)

    D_star = float(np.mean(abs_err))
    D_max = float(np.max(abs_err))
    t_first_1pct = first_crossing_time(t_ref, rel_err, 1e-2)

    return {
        "alpha_qg": float(alpha_qg),
        "dt_euler": float(dt_euler),
        "D_star": D_star,
        "D_max": D_max,
        "t_first_1pct": t_first_1pct,
        "rel_err_p50": float(np.percentile(rel_err, 50)),
        "rel_err_p95": float(np.percentile(rel_err, 95)),
        "rel_err_p99": float(np.percentile(rel_err, 99)),
    }, {
        "t": t_ref,
        "a_ref": a_ref,
        "a_eu_on_ref": a_eu_on_ref,
        "abs_err": abs_err,
        "rel_err": rel_err,
    }


def main():
    alphas = [1.2e-7, 1.5e-7, 1.8e-7, 2.1544346900318822e-7]
    dts = [1e-3, 5e-4, 2.5e-4]

    root = Path(__file__).resolve().parents[1]
    out_root = root / "notebooks" / "outputs"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = out_root / f"grqm_q2_outlier_autopsy_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    for a in alphas:
        for dt in dts:
            metrics, series = run_case(a, dt)
            rows.append(metrics)

            tag = f"alpha_{a:.3e}_dt_{dt:.1e}"
            csv_path = out_dir / f"{tag}_timeseries.csv"
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["t", "a_ref", "a_eu_on_ref", "abs_err", "rel_err"])
                for i in range(len(series["t"])):
                    w.writerow([
                        float(series["t"][i]),
                        float(series["a_ref"][i]),
                        float(series["a_eu_on_ref"][i]),
                        float(series["abs_err"][i]),
                        float(series["rel_err"][i]),
                    ])

    with open(out_dir / "summary.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    with open(out_dir / "manifest.json", "w", encoding="utf-8") as f:
        json.dump({"out_dir": str(out_dir), "alphas": alphas, "dts": dts, "n_rows": len(rows)}, f, indent=2)

    print(json.dumps({"out_dir": str(out_dir), "n_rows": len(rows)}, indent=2))


if __name__ == "__main__":
    main()
