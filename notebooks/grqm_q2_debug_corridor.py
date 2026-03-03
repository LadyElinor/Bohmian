import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

import numpy as np

from grqm_proxy_toymodel_v1 import IC, Params, RunConfig, integrate, interp_to_grid


CORRIDOR = [
    {"run_id": 19, "alpha_qg": 1.0e-6, "omega_m": 0.30},
    {"run_id": 16, "alpha_qg": 4.6415888336127725e-7, "omega_m": 0.30},
    {"run_id": 13, "alpha_qg": 2.1544346900318822e-7, "omega_m": 0.30},
]

THRESHOLDS = [1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1]


def first_crossing_time(t, rel_err, threshold):
    idx = np.where(rel_err >= threshold)[0]
    if len(idx) == 0:
        return None
    return float(t[idx[0]])


def run_q2_debug_for_params(params: Params):
    ic = IC()
    dt_main = 1e-3
    dt_exact = 2.5e-4
    dt_coarse = 2e-3

    # exact / approx / alt (same as production metrics)
    t_exact, a_exact, _ = integrate(ic, params, RunConfig(dt=dt_exact, method="rk4", corrected=True))
    t_approx, a_approx, _ = integrate(ic, params, RunConfig(dt=dt_main, method="euler", corrected=True))
    t_alt, a_alt, _ = integrate(ic, params, RunConfig(dt=dt_coarse, method="rk4", corrected=True))

    a_approx_on_exact = interp_to_grid(t_approx, a_approx, t_exact)
    a_alt_on_exact = interp_to_grid(t_alt, a_alt, t_exact)

    abs_diff_exact_approx = np.abs(a_approx_on_exact - a_exact)
    abs_diff_exact_alt = np.abs(a_alt_on_exact - a_exact)
    abs_diff_approx_alt = np.abs(a_approx_on_exact - a_alt_on_exact)

    eps = 1e-15
    rel_diff_exact_approx = abs_diff_exact_approx / (np.abs(a_exact) + eps)
    rel_diff_exact_alt = abs_diff_exact_alt / (np.abs(a_exact) + eps)
    rel_diff_approx_alt = abs_diff_approx_alt / (np.abs(a_exact) + eps)

    q2 = {
        "D_star": float(np.mean(abs_diff_exact_approx)),
        "D_max": float(np.max(abs_diff_exact_approx)),
        "D_star_alt": float(np.mean(abs_diff_exact_alt)),
        "D_max_alt": float(np.max(abs_diff_exact_alt)),
        "replication_rel_diff": float(abs(float(np.mean(abs_diff_exact_alt)) - float(np.mean(abs_diff_exact_approx))) / (abs(float(np.mean(abs_diff_exact_approx))) + eps)),
    }

    crossing = {
        "exact_vs_approx": {str(th): first_crossing_time(t_exact, rel_diff_exact_approx, th) for th in THRESHOLDS},
        "exact_vs_alt": {str(th): first_crossing_time(t_exact, rel_diff_exact_alt, th) for th in THRESHOLDS},
        "approx_vs_alt": {str(th): first_crossing_time(t_exact, rel_diff_approx_alt, th) for th in THRESHOLDS},
    }

    series = {
        "t": t_exact.tolist(),
        "a_exact": a_exact.tolist(),
        "a_approx_on_exact": a_approx_on_exact.tolist(),
        "a_alt_on_exact": a_alt_on_exact.tolist(),
        "abs_diff_exact_approx": abs_diff_exact_approx.tolist(),
        "abs_diff_exact_alt": abs_diff_exact_alt.tolist(),
        "abs_diff_approx_alt": abs_diff_approx_alt.tolist(),
        "rel_diff_exact_approx": rel_diff_exact_approx.tolist(),
        "rel_diff_exact_alt": rel_diff_exact_alt.tolist(),
        "rel_diff_approx_alt": rel_diff_approx_alt.tolist(),
    }

    return q2, crossing, series


def main():
    root = Path(__file__).resolve().parents[1]
    out_root = root / "notebooks" / "outputs"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = out_root / f"grqm_q2_debug_corridor_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    summary = []

    for item in CORRIDOR:
        p = Params(omega_m=item["omega_m"], omega_l=1.0 - item["omega_m"], alpha_qg=item["alpha_qg"])
        q2, crossing, series = run_q2_debug_for_params(p)

        tag = f"run_{item['run_id']:03d}_alpha_{item['alpha_qg']:.3e}_om_{item['omega_m']:.3f}"

        with open(out_dir / f"{tag}_q2_debug.json", "w", encoding="utf-8") as f:
            json.dump(
                {
                    "params": asdict(p),
                    "q2": q2,
                    "crossing_times": crossing,
                },
                f,
                indent=2,
            )

        # write compact CSV for quick plotting
        header = [
            "t",
            "a_exact",
            "a_approx_on_exact",
            "a_alt_on_exact",
            "abs_diff_exact_approx",
            "abs_diff_exact_alt",
            "abs_diff_approx_alt",
            "rel_diff_exact_approx",
            "rel_diff_exact_alt",
            "rel_diff_approx_alt",
        ]
        csv_path = out_dir / f"{tag}_timeseries.csv"
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write(",".join(header) + "\n")
            n = len(series["t"])
            for i in range(n):
                row = [
                    series["t"][i],
                    series["a_exact"][i],
                    series["a_approx_on_exact"][i],
                    series["a_alt_on_exact"][i],
                    series["abs_diff_exact_approx"][i],
                    series["abs_diff_exact_alt"][i],
                    series["abs_diff_approx_alt"][i],
                    series["rel_diff_exact_approx"][i],
                    series["rel_diff_exact_alt"][i],
                    series["rel_diff_approx_alt"][i],
                ]
                f.write(",".join(f"{x:.17g}" for x in row) + "\n")

        summary.append(
            {
                "run_id": item["run_id"],
                "alpha_qg": item["alpha_qg"],
                "omega_m": item["omega_m"],
                "omega_l": 1.0 - item["omega_m"],
                **q2,
                "first_t_rel_exact_vs_approx_ge_1e-2": crossing["exact_vs_approx"]["0.01"],
                "first_t_rel_exact_vs_alt_ge_1e-2": crossing["exact_vs_alt"]["0.01"],
                "first_t_rel_approx_vs_alt_ge_1e-2": crossing["approx_vs_alt"]["0.01"],
            }
        )

    summary_csv = out_dir / "summary.csv"
    fields = list(summary[0].keys())
    with open(summary_csv, "w", encoding="utf-8") as f:
        f.write(",".join(fields) + "\n")
        for r in summary:
            f.write(",".join(str(r[k]) for k in fields) + "\n")

    with open(out_dir / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "created_at": ts,
                "corridor": CORRIDOR,
                "thresholds": THRESHOLDS,
                "summary_csv": str(summary_csv),
                "out_dir": str(out_dir),
            },
            f,
            indent=2,
        )

    print(json.dumps({"out_dir": str(out_dir), "summary_csv": str(summary_csv), "n_runs": len(summary)}, indent=2))


if __name__ == "__main__":
    main()
