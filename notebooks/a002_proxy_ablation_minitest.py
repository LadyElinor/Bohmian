import csv
import json
from datetime import datetime
from pathlib import Path

import numpy as np

from grqm_proxy_toymodel_v1 import IC, Params, RunConfig, integrate, l2_rel_err


def proxy_primary(a_b, a_c):
    return float(l2_rel_err(a_c - a_b, a_b))


def proxy_template_maxabs(a_b, a_c):
    return float(np.max(np.abs(a_c - a_b)))


def proxy_template_terminal(a_b, a_c):
    return float(abs(a_c[-1] - a_b[-1]))


def spearman(x, y):
    xr = np.argsort(np.argsort(np.asarray(x)))
    yr = np.argsort(np.argsort(np.asarray(y)))
    return float(np.corrcoef(xr, yr)[0, 1])


def compute_proxies(omega_m, alpha_list, ic_scale=1.0, dt_main=1e-3):
    rows = []
    for a in alpha_list:
        ic = IC(a0=IC().a0 * ic_scale, v0=IC().v0, t0=IC().t0, t1=IC().t1)
        p = Params(omega_m=omega_m, omega_l=1.0 - omega_m, alpha_qg=a)
        _, a_b, _ = integrate(ic, p, RunConfig(dt=dt_main, method="rk4", corrected=False))
        _, a_c, _ = integrate(ic, p, RunConfig(dt=dt_main, method="rk4", corrected=True, correction_power=5))
        rows.append({
            "alpha_qg": a,
            "proxy_primary_l2": proxy_primary(a_b, a_c),
            "proxy_template_maxabs": proxy_template_maxabs(a_b, a_c),
            "proxy_template_terminal": proxy_template_terminal(a_b, a_c),
        })
    return rows


def main():
    omega_m = 0.300
    alpha_list = [3e-7, 5e-7, 7e-7, 1.0e-6, 1.3e-6]

    nuisance_cases = [
        {"name": "baseline", "ic_scale": 1.0, "dt_main": 1e-3},
        {"name": "nuisance_ic_minus_0p1pct", "ic_scale": 0.999, "dt_main": 1e-3},
        {"name": "nuisance_ic_plus_0p1pct", "ic_scale": 1.001, "dt_main": 1e-3},
        {"name": "nuisance_dt_minus_10pct", "ic_scale": 1.0, "dt_main": 9e-4},
        {"name": "nuisance_dt_plus_10pct", "ic_scale": 1.0, "dt_main": 1.1e-3},
    ]

    criteria = {
        "ranking_spearman_min": 0.99,
        "agreement_rel_drift_max": 0.10,
        "stability_cv_max": 0.25,
    }

    root = Path(__file__).resolve().parents[1]
    out_root = root / "notebooks" / "outputs"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = out_root / f"grqm_a002_proxy_ablation_minitest_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    detail = []
    by_case = {}
    for c in nuisance_cases:
        vals = compute_proxies(omega_m, alpha_list, ic_scale=c["ic_scale"], dt_main=c["dt_main"])
        by_case[c["name"]] = vals
        for r in vals:
            detail.append({"case": c["name"], **r})

    with open(out_dir / "a002_proxy_ablation_detail.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(detail[0].keys()))
        w.writeheader(); w.writerows(detail)

    base = by_case["baseline"]
    base_l2 = [r["proxy_primary_l2"] for r in base]
    base_maxabs = [r["proxy_template_maxabs"] for r in base]
    base_term = [r["proxy_template_terminal"] for r in base]

    summary_rows = []
    for name, vals in by_case.items():
        l2 = [r["proxy_primary_l2"] for r in vals]
        maxabs = [r["proxy_template_maxabs"] for r in vals]
        term = [r["proxy_template_terminal"] for r in vals]

        rank_l2 = spearman(base_l2, l2)
        rank_maxabs = spearman(base_maxabs, maxabs)
        rank_term = spearman(base_term, term)

        rel_drift = np.max(np.abs((np.asarray(l2) - np.asarray(base_l2)) / (np.asarray(base_l2) + 1e-15)))

        ratio_m_t = np.asarray(maxabs) / (np.asarray(term) + 1e-15)
        stability_cv = float(np.std(ratio_m_t) / (np.mean(ratio_m_t) + 1e-15))

        pass_case = (
            rank_l2 >= criteria["ranking_spearman_min"] and
            rank_maxabs >= criteria["ranking_spearman_min"] and
            rank_term >= criteria["ranking_spearman_min"] and
            rel_drift <= criteria["agreement_rel_drift_max"] and
            stability_cv <= criteria["stability_cv_max"]
        )

        summary_rows.append({
            "case": name,
            "spearman_l2_vs_baseline": rank_l2,
            "spearman_maxabs_vs_baseline": rank_maxabs,
            "spearman_terminal_vs_baseline": rank_term,
            "max_rel_drift_primary_l2": float(rel_drift),
            "template_ratio_cv": stability_cv,
            "pass_case": pass_case,
        })

    with open(out_dir / "a002_proxy_ablation_summary.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
        w.writeheader(); w.writerows(summary_rows)

    agg = {
        "n_cases": len(summary_rows),
        "criteria": criteria,
        "pass_rate": sum(1 for r in summary_rows if r["pass_case"]) / len(summary_rows),
    }
    with open(out_dir / "aggregate.json", "w", encoding="utf-8") as f:
        json.dump(agg, f, indent=2)

    print(json.dumps({"out_dir": str(out_dir), **agg}, indent=2))


if __name__ == "__main__":
    main()
