from __future__ import annotations

import csv
import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

import numpy as np

from grqm.core import IC, Params, RunConfig, accel, integrate, l2_rel_err
from grqm.symbolic import validate_correction_term_symbolic


ROOT = Path(__file__).resolve().parent
OUT_ROOT = ROOT / "outputs"


def summarize_case(omega_m: float, omega_label: str, correction_power: int = 5) -> dict[str, float | str | bool]:
    p = Params(omega_m=omega_m, omega_l=0.7, alpha_qg=1.0e-7)
    ic = IC()
    cfg = RunConfig(dt=1e-3, method="rk4", corrected=True, correction_power=correction_power)

    t_b, a_b, _ = integrate(ic, p, RunConfig(dt=cfg.dt, method=cfg.method, corrected=False, correction_power=correction_power))
    t_c, a_c, _ = integrate(ic, p, cfg)

    delta = a_c - a_b
    delta_proxy_l2 = l2_rel_err(delta, a_b)
    delta_proxy_max_abs = float(np.max(np.abs(delta)))

    a_probe = np.array([1e-6, 1e-4, 1e-2, 1e-1, 1.0], dtype=float)
    ratio_probe = []
    for a in a_probe:
        base = -(p.omega_m) / (2.0 * a * a) + p.omega_l * a
        corr = p.alpha_qg / (a**correction_power)
        ratio_probe.append(float(abs(corr) / (abs(base) + 1e-30)))

    # Trajectory-level correction/classical ratio on the corrected path.
    base_traj = np.array([-(p.omega_m) / (2.0 * a * a) + p.omega_l * a for a in a_c], dtype=float)
    corr_traj = np.array([p.alpha_qg / (a**correction_power) for a in a_c], dtype=float)
    ratio_traj_abs = np.abs(corr_traj) / (np.abs(base_traj) + 1e-30)

    return {
        "omega_label": omega_label,
        "omega_m": omega_m,
        "correction_power": correction_power,
        "delta_proxy_l2": float(delta_proxy_l2),
        "delta_proxy_max_abs": delta_proxy_max_abs,
        "ratio_abs_a_1e-6": ratio_probe[0],
        "ratio_abs_a_1e-4": ratio_probe[1],
        "ratio_abs_a_1e-2": ratio_probe[2],
        "ratio_abs_a_1e-1": ratio_probe[3],
        "ratio_abs_a_1": ratio_probe[4],
        "traj_ratio_abs_t0": float(ratio_traj_abs[0]),
        "traj_ratio_abs_tmid": float(ratio_traj_abs[len(ratio_traj_abs) // 2]),
        "traj_ratio_abs_tend": float(ratio_traj_abs[-1]),
        "traj_ratio_abs_max": float(np.max(ratio_traj_abs)),
        "traj_ratio_abs_min": float(np.min(ratio_traj_abs)),
        "a_min_corrected_path": float(np.min(a_c)),
        "a_final_corrected_path": float(a_c[-1]),
        "path_nonnegative": bool(np.all(a_c > 0.0)),
    }


def main() -> None:
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = OUT_ROOT / f"grqm_core_edge_diag_pack_{run_id}"
    out_dir.mkdir(parents=True, exist_ok=True)

    symbolic_results = {
        f"n_{n}": asdict(validate_correction_term_symbolic(correction_power=n)) for n in (4, 5, 6)
    }

    rows = [
        summarize_case(omega_m=0.300, omega_label="core_0p300", correction_power=5),
        summarize_case(omega_m=0.305, omega_label="edge_0p305", correction_power=5),
        summarize_case(omega_m=0.3075, omega_label="edge_0p3075", correction_power=5),
    ]

    with (out_dir / "core_edge_diag_rows.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "symbolic_family_validation": symbolic_results,
        "diagnostic_rows": rows,
        "notes": {
            "purpose": "core-vs-edge diagnostic evidence pack with symbolic + numeric receipts",
            "governance": "diagnostic-only; no status/policy change",
            "edge_block_posture": "unchanged (Omega_m >= 0.305 remains blocked)",
        },
    }

    with (out_dir / "core_edge_diag_summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(out_dir)


if __name__ == "__main__":
    main()
