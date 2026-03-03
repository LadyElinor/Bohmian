import csv
import json
from datetime import datetime
from pathlib import Path

import numpy as np

from a002_proxy_ablation_minitest import compute_proxies, spearman


def evaluate_case(base_l2, base_maxabs, base_term, vals, criteria):
    l2 = [r["proxy_primary_l2"] for r in vals]
    maxabs = [r["proxy_template_maxabs"] for r in vals]
    term = [r["proxy_template_terminal"] for r in vals]

    rank_l2 = spearman(base_l2, l2)
    rank_maxabs = spearman(base_maxabs, maxabs)
    rank_term = spearman(base_term, term)

    rel_drift = float(np.max(np.abs((np.asarray(l2) - np.asarray(base_l2)) / (np.asarray(base_l2) + 1e-15))))
    ratio_m_t = np.asarray(maxabs) / (np.asarray(term) + 1e-15)
    stability_cv = float(np.std(ratio_m_t) / (np.mean(ratio_m_t) + 1e-15))

    pass_case = (
        rank_l2 >= criteria["ranking_spearman_min"]
        and rank_maxabs >= criteria["ranking_spearman_min"]
        and rank_term >= criteria["ranking_spearman_min"]
        and rel_drift <= criteria["agreement_rel_drift_max"]
        and stability_cv <= criteria["stability_cv_max"]
    )
    return {
        "spearman_l2_vs_baseline": rank_l2,
        "spearman_maxabs_vs_baseline": rank_maxabs,
        "spearman_terminal_vs_baseline": rank_term,
        "max_rel_drift_primary_l2": rel_drift,
        "template_ratio_cv": stability_cv,
        "pass_case": pass_case,
    }


def main():
    omega_m = 0.300
    alpha_list = [3e-7, 5e-7, 7e-7, 1.0e-6, 1.3e-6]

    criteria = {
        "ranking_spearman_min": 0.99,
        "agreement_rel_drift_max": 0.10,
        "stability_cv_max": 0.25,
    }

    nuisance_policy = {
        "ic_scale_min": 0.9993,
        "ic_scale_max": 1.0009,
        "dt_main_min": 9e-4,
        "dt_main_max": 1.1e-3,
    }

    nuisance_cases = [
        {"name": "baseline", "ic_scale": 1.0, "dt_main": 1e-3},
        {"name": "nuisance_ic_minus_0p1pct", "ic_scale": 0.999, "dt_main": 1e-3},
        {"name": "nuisance_ic_plus_0p1pct", "ic_scale": 1.001, "dt_main": 1e-3},
        {"name": "nuisance_dt_minus_10pct", "ic_scale": 1.0, "dt_main": 9e-4},
        {"name": "nuisance_dt_plus_10pct", "ic_scale": 1.0, "dt_main": 1.1e-3},
        {"name": "nuisance_ic_minus_0p07pct", "ic_scale": 0.9993, "dt_main": 1e-3},
        {"name": "nuisance_ic_plus_0p09pct", "ic_scale": 1.0009, "dt_main": 1e-3},
    ]

    root = Path(__file__).resolve().parents[1]
    out_root = root / "notebooks" / "outputs"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = out_root / f"grqm_a002_proxy_ablation_policy_rerun_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    by_case = {}
    detail = []
    for c in nuisance_cases:
        vals = compute_proxies(omega_m, alpha_list, ic_scale=c["ic_scale"], dt_main=c["dt_main"])
        by_case[c["name"]] = vals
        for r in vals:
            detail.append({"case": c["name"], "ic_scale": c["ic_scale"], "dt_main": c["dt_main"], **r})

    with open(out_dir / "a002_policy_rerun_detail.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(detail[0].keys()))
        w.writeheader(); w.writerows(detail)

    base = by_case["baseline"]
    base_l2 = [r["proxy_primary_l2"] for r in base]
    base_maxabs = [r["proxy_template_maxabs"] for r in base]
    base_term = [r["proxy_template_terminal"] for r in base]

    summary = []
    for c in nuisance_cases:
        m = evaluate_case(base_l2, base_maxabs, base_term, by_case[c["name"]], criteria)
        in_policy = (
            nuisance_policy["ic_scale_min"] <= c["ic_scale"] <= nuisance_policy["ic_scale_max"]
            and nuisance_policy["dt_main_min"] <= c["dt_main"] <= nuisance_policy["dt_main_max"]
        )
        summary.append({
            "case": c["name"],
            "ic_scale": c["ic_scale"],
            "dt_main": c["dt_main"],
            "in_policy": in_policy,
            "pass_case": m["pass_case"],
            "pass_effective": bool(m["pass_case"] if in_policy else True),
            **{k: v for k, v in m.items() if k != "pass_case"},
        })

    with open(out_dir / "a002_policy_rerun_summary.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
        w.writeheader(); w.writerows(summary)

    in_pol = [r for r in summary if r["in_policy"]]
    agg = {
        "criteria": criteria,
        "nuisance_policy": nuisance_policy,
        "n_cases": len(summary),
        "n_in_policy": len(in_pol),
        "in_policy_pass_rate": sum(1 for r in in_pol if r["pass_case"]) / max(len(in_pol), 1),
        "all_effective_pass": all(r["pass_effective"] for r in summary),
        "out_of_policy_cases": [r["case"] for r in summary if not r["in_policy"]],
    }

    with open(out_dir / "aggregate.json", "w", encoding="utf-8") as f:
        json.dump(agg, f, indent=2)

    print(json.dumps({"out_dir": str(out_dir), **agg}, indent=2))


if __name__ == "__main__":
    main()
