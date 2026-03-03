import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

import numpy as np

from grqm_proxy_toymodel_v1 import IC, Params, RunConfig, integrate, interp_to_grid, l2_rel_err


# Focus corridor (best available region)
CORRIDOR = [
    {"run_id": 19, "alpha_qg": 1.0e-6, "omega_m": 0.30},
    {"run_id": 16, "alpha_qg": 4.6415888336127725e-7, "omega_m": 0.30},
    {"run_id": 13, "alpha_qg": 2.1544346900318822e-7, "omega_m": 0.30},
]

# Assumption knobs (proxy choices)
ASSUMPTIONS = {
    "correction_power_n": [4, 5, 6],
    "ic_a0_scale": [0.98, 1.00, 1.02],
    "dt_main": [8e-4, 1e-3, 1.2e-3],
}


def q1_metrics(params: Params, ic: IC, dt_main=1e-3, correction_power=5):
    dt_ref = dt_main / 2.0

    t_b, a_b, _ = integrate(ic, params, RunConfig(dt=dt_main, method="rk4", corrected=False))
    t_c, a_c, _ = integrate(ic, params, RunConfig(dt=dt_main, method="rk4", corrected=True, correction_power=correction_power))

    delta_proxy_l2 = l2_rel_err(a_c - a_b, a_b)
    delta_proxy_max_abs = float(np.max(np.abs(a_c - a_b)))

    t_b_ref, a_b_ref, _ = integrate(ic, params, RunConfig(dt=dt_ref, method="rk4", corrected=False))
    t_c_ref, a_c_ref, _ = integrate(ic, params, RunConfig(dt=dt_ref, method="rk4", corrected=True, correction_power=correction_power))

    a_b_main_on_ref = interp_to_grid(t_b, a_b, t_b_ref)
    a_c_main_on_ref = interp_to_grid(t_c, a_c, t_c_ref)

    baseline_refinement_error = l2_rel_err(a_b_main_on_ref - a_b_ref, a_b_ref)
    corrected_refinement_error = l2_rel_err(a_c_main_on_ref - a_c_ref, a_c_ref)

    return {
        "delta_proxy_l2": float(delta_proxy_l2),
        "delta_proxy_max_abs": delta_proxy_max_abs,
        "refinement_max_obs": float(max(baseline_refinement_error, corrected_refinement_error)),
    }


def rel_change(new, base, eps=1e-15):
    return abs(new - base) / (abs(base) + eps)


def main():
    root = Path(__file__).resolve().parents[1]
    out_root = root / "notebooks" / "outputs"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = out_root / f"grqm_q1_assumption_ablation_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = []

    for item in CORRIDOR:
        p = Params(omega_m=item["omega_m"], omega_l=1.0 - item["omega_m"], alpha_qg=item["alpha_qg"])
        ic_base = IC()

        base = q1_metrics(p, ic_base, dt_main=1e-3, correction_power=5)

        # one-at-a-time perturbations
        for n in ASSUMPTIONS["correction_power_n"]:
            m = q1_metrics(p, ic_base, dt_main=1e-3, correction_power=n)
            rows.append({
                "run_id": item["run_id"],
                "alpha_qg": item["alpha_qg"],
                "omega_m": item["omega_m"],
                "assumption": "correction_power_n",
                "setting": n,
                "delta_proxy_l2": m["delta_proxy_l2"],
                "refinement_max_obs": m["refinement_max_obs"],
                "sens_rel_vs_base": rel_change(m["delta_proxy_l2"], base["delta_proxy_l2"]),
            })

        for s in ASSUMPTIONS["ic_a0_scale"]:
            ic = IC(a0=IC().a0 * s, v0=IC().v0, t0=IC().t0, t1=IC().t1)
            m = q1_metrics(p, ic, dt_main=1e-3, correction_power=5)
            rows.append({
                "run_id": item["run_id"],
                "alpha_qg": item["alpha_qg"],
                "omega_m": item["omega_m"],
                "assumption": "ic_a0_scale",
                "setting": s,
                "delta_proxy_l2": m["delta_proxy_l2"],
                "refinement_max_obs": m["refinement_max_obs"],
                "sens_rel_vs_base": rel_change(m["delta_proxy_l2"], base["delta_proxy_l2"]),
            })

        for dtm in ASSUMPTIONS["dt_main"]:
            m = q1_metrics(p, ic_base, dt_main=dtm, correction_power=5)
            rows.append({
                "run_id": item["run_id"],
                "alpha_qg": item["alpha_qg"],
                "omega_m": item["omega_m"],
                "assumption": "dt_main",
                "setting": dtm,
                "delta_proxy_l2": m["delta_proxy_l2"],
                "refinement_max_obs": m["refinement_max_obs"],
                "sens_rel_vs_base": rel_change(m["delta_proxy_l2"], base["delta_proxy_l2"]),
            })

        # combined perturbation stress test (non-baseline choices)
        ic_combo = IC(a0=IC().a0 * 1.02, v0=IC().v0, t0=IC().t0, t1=IC().t1)
        combo = q1_metrics(p, ic_combo, dt_main=1.2e-3, correction_power=4)
        rows.append({
            "run_id": item["run_id"],
            "alpha_qg": item["alpha_qg"],
            "omega_m": item["omega_m"],
            "assumption": "combined_stress",
            "setting": "n=4,a0*1.02,dt=1.2e-3",
            "delta_proxy_l2": combo["delta_proxy_l2"],
            "refinement_max_obs": combo["refinement_max_obs"],
            "sens_rel_vs_base": rel_change(combo["delta_proxy_l2"], base["delta_proxy_l2"]),
        })

        # baseline row for clarity
        rows.append({
            "run_id": item["run_id"],
            "alpha_qg": item["alpha_qg"],
            "omega_m": item["omega_m"],
            "assumption": "baseline",
            "setting": "n=5,a0*1.00,dt=1e-3",
            "delta_proxy_l2": base["delta_proxy_l2"],
            "refinement_max_obs": base["refinement_max_obs"],
            "sens_rel_vs_base": 0.0,
        })

    # write detailed CSV
    csv_path = out_dir / "q1_assumption_ablation.csv"
    fields = list(rows[0].keys())
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write(",".join(fields) + "\n")
        for r in rows:
            f.write(",".join(str(r[k]) for k in fields) + "\n")

    # aggregate ranking by assumption family (exclude baseline)
    agg = {}
    for r in rows:
        a = r["assumption"]
        if a == "baseline":
            continue
        agg.setdefault(a, [])
        agg[a].append(float(r["sens_rel_vs_base"]))

    ranking = []
    for a, vals in agg.items():
        ranking.append({
            "assumption": a,
            "n_samples": len(vals),
            "mean_sens_rel": float(np.mean(vals)),
            "max_sens_rel": float(np.max(vals)),
        })
    ranking.sort(key=lambda x: x["mean_sens_rel"], reverse=True)

    with open(out_dir / "q1_assumption_ranking.json", "w", encoding="utf-8") as f:
        json.dump(ranking, f, indent=2)

    manifest = {
        "out_dir": str(out_dir),
        "corridor": CORRIDOR,
        "assumptions": ASSUMPTIONS,
        "csv": str(csv_path),
        "ranking_json": str(out_dir / "q1_assumption_ranking.json"),
    }
    with open(out_dir / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
