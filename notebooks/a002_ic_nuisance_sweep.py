import csv
import json
from datetime import datetime
from pathlib import Path

import numpy as np

from a002_proxy_ablation_minitest import compute_proxies, spearman


def main():
    omega_m = 0.300
    alpha_list = [3e-7, 5e-7, 7e-7, 1.0e-6, 1.3e-6]
    dt_main = 1e-3

    criteria = {
        "ranking_spearman_min": 0.99,
        "agreement_rel_drift_max": 0.10,
        "stability_cv_max": 0.25,
    }

    # Focused local sweep around known failing IC nuisance region near +/-0.1%
    ic_scales = [
        0.9988, 0.9990, 0.9991, 0.9992, 0.9993, 0.9994, 0.9995, 0.9996,
        0.9997, 0.9998, 0.9999, 1.0000,
        1.0001, 1.0002, 1.0003, 1.0004, 1.0005, 1.0006, 1.0007, 1.0008,
        1.0009, 1.0010, 1.0011, 1.0012,
    ]

    root = Path(__file__).resolve().parents[1]
    out_root = root / "notebooks" / "outputs"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = out_root / f"grqm_a002_ic_nuisance_sweep_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    base = compute_proxies(omega_m, alpha_list, ic_scale=1.0, dt_main=dt_main)
    base_l2 = np.asarray([r["proxy_primary_l2"] for r in base], dtype=float)
    base_maxabs = [r["proxy_template_maxabs"] for r in base]
    base_term = [r["proxy_template_terminal"] for r in base]

    rows = []
    detail_rows = []

    for s in ic_scales:
        vals = compute_proxies(omega_m, alpha_list, ic_scale=s, dt_main=dt_main)
        for r in vals:
            detail_rows.append({"ic_scale": s, **r})

        l2 = np.asarray([r["proxy_primary_l2"] for r in vals], dtype=float)
        maxabs = [r["proxy_template_maxabs"] for r in vals]
        term = [r["proxy_template_terminal"] for r in vals]

        rank_l2 = spearman(base_l2, l2)
        rank_maxabs = spearman(base_maxabs, maxabs)
        rank_term = spearman(base_term, term)

        rel_drift = float(np.max(np.abs((l2 - base_l2) / (base_l2 + 1e-15))))
        ratio_m_t = np.asarray(maxabs) / (np.asarray(term) + 1e-15)
        stability_cv = float(np.std(ratio_m_t) / (np.mean(ratio_m_t) + 1e-15))

        pass_case = (
            rank_l2 >= criteria["ranking_spearman_min"]
            and rank_maxabs >= criteria["ranking_spearman_min"]
            and rank_term >= criteria["ranking_spearman_min"]
            and rel_drift <= criteria["agreement_rel_drift_max"]
            and stability_cv <= criteria["stability_cv_max"]
        )

        rows.append({
            "ic_scale": s,
            "ic_delta_pct": (s - 1.0) * 100.0,
            "spearman_l2_vs_baseline": rank_l2,
            "spearman_maxabs_vs_baseline": rank_maxabs,
            "spearman_terminal_vs_baseline": rank_term,
            "max_rel_drift_primary_l2": rel_drift,
            "template_ratio_cv": stability_cv,
            "pass_case": pass_case,
        })

    with open(out_dir / "a002_ic_sweep_detail.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(detail_rows[0].keys()))
        w.writeheader(); w.writerows(detail_rows)

    with open(out_dir / "a002_ic_sweep_summary.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    passing = [r for r in rows if r["pass_case"]]
    lower = min(r["ic_scale"] for r in passing)
    upper = max(r["ic_scale"] for r in passing)

    agg = {
        "n_scales": len(rows),
        "criteria": criteria,
        "pass_count": len(passing),
        "pass_rate": len(passing) / len(rows),
        "pass_band_ic_scale": [lower, upper],
        "pass_band_ic_delta_pct": [(lower - 1.0) * 100.0, (upper - 1.0) * 100.0],
        "classification": "localized_controllable" if len(passing) > 0 else "structural",
    }

    with open(out_dir / "aggregate.json", "w", encoding="utf-8") as f:
        json.dump(agg, f, indent=2)

    print(json.dumps({"out_dir": str(out_dir), **agg}, indent=2))


if __name__ == "__main__":
    main()
