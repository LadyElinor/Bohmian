import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

import numpy as np

from grqm_proxy_toymodel_v1 import IC, Params, RunConfig, integrate, interp_to_grid, l2_rel_err

CORRIDOR = [
    {"run_id": 19, "alpha_qg": 1.0e-6, "omega_m": 0.30},
    {"run_id": 16, "alpha_qg": 4.6415888336127725e-7, "omega_m": 0.30},
    {"run_id": 13, "alpha_qg": 2.1544346900318822e-7, "omega_m": 0.30},
]


def q1_delta(params: Params, ic: IC, dt_main=1e-3, correction_power=5):
    t_b, a_b, _ = integrate(ic, params, RunConfig(dt=dt_main, method="rk4", corrected=False))
    t_c, a_c, _ = integrate(ic, params, RunConfig(dt=dt_main, method="rk4", corrected=True, correction_power=correction_power))
    return float(l2_rel_err(a_c - a_b, a_b))


def main():
    root = Path(__file__).resolve().parents[1]
    out_root = root / "notebooks" / "outputs"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = out_root / f"grqm_q1_assumption_hardening_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    for item in CORRIDOR:
        p = Params(omega_m=item["omega_m"], omega_l=1.0-item["omega_m"], alpha_qg=item["alpha_qg"])
        base_ic = IC()
        base = q1_delta(p, base_ic, dt_main=1e-3, correction_power=5)

        # hardened perturbation set
        tests = [
            ("ic_a0_scale", 0.999, dict(a0=base_ic.a0*0.999, v0=base_ic.v0, t0=base_ic.t0, t1=base_ic.t1), 1e-3, 5),
            ("ic_a0_scale", 1.001, dict(a0=base_ic.a0*1.001, v0=base_ic.v0, t0=base_ic.t0, t1=base_ic.t1), 1e-3, 5),
            ("dt_main", 9e-4, dict(a0=base_ic.a0, v0=base_ic.v0, t0=base_ic.t0, t1=base_ic.t1), 9e-4, 5),
            ("dt_main", 1.1e-3, dict(a0=base_ic.a0, v0=base_ic.v0, t0=base_ic.t0, t1=base_ic.t1), 1.1e-3, 5),
            ("correction_power_n", 5, dict(a0=base_ic.a0, v0=base_ic.v0, t0=base_ic.t0, t1=base_ic.t1), 1e-3, 5),
        ]

        sens_vals = []
        for name, setting, ic_kwargs, dt_main, n in tests:
            ic = IC(**ic_kwargs)
            d = q1_delta(p, ic, dt_main=dt_main, correction_power=n)
            s = abs(d-base)/(abs(base)+1e-15)
            sens_vals.append(s)
            rows.append({
                "run_id": item["run_id"],
                "alpha_qg": item["alpha_qg"],
                "assumption": name,
                "setting": setting,
                "delta_proxy_l2": d,
                "sens_rel_vs_base": s,
            })

        rows.append({
            "run_id": item["run_id"],
            "alpha_qg": item["alpha_qg"],
            "assumption": "summary",
            "setting": "max_hardened_sens",
            "delta_proxy_l2": base,
            "sens_rel_vs_base": float(max(sens_vals)),
        })

    csv_path = out_dir / "q1_hardening.csv"
    keys = list(rows[0].keys())
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write(",".join(keys)+"\n")
        for r in rows:
            f.write(",".join(str(r[k]) for k in keys)+"\n")

    print(json.dumps({"out_dir": str(out_dir), "csv": str(csv_path)}, indent=2))

if __name__ == "__main__":
    main()
