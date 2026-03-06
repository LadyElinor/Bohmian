from __future__ import annotations

import csv
import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

import numpy as np

from grqm.core import Params
from grqm.symbolic import validate_correction_term_symbolic


ROOT = Path(__file__).resolve().parent
OUT_ROOT = ROOT / "outputs"


def correction_to_classical_ratio(a: float, p: Params, correction_power: int = 5) -> dict[str, float]:
    classical = -(p.omega_m) / (2.0 * a * a) + p.omega_l * a
    correction = p.alpha_qg / (a**correction_power)
    return {
        "classical": classical,
        "correction": correction,
        "ratio_signed": correction / classical,
        "ratio_abs": abs(correction) / (abs(classical) + 1e-30),
    }


def main() -> None:
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = OUT_ROOT / f"grqm_symbolic_ratio_receipt_{run_id}"
    out_dir.mkdir(parents=True, exist_ok=True)

    omega_points = {
        "core_0p300": 0.300,
        "edge_0p305": 0.305,
        "edge_0p3075": 0.3075,
    }
    a_points = np.array([1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 0.5, 1.0], dtype=float)

    symbolic = validate_correction_term_symbolic(correction_power=5)

    rows: list[dict[str, float | str]] = []
    summary: dict[str, dict[str, float]] = {}

    for label, omega_m in omega_points.items():
        p = Params(omega_m=omega_m, omega_l=0.7, alpha_qg=1.0e-7)
        ratio_values = []
        for a in a_points:
            r = correction_to_classical_ratio(a, p, correction_power=5)
            ratio_values.append(r["ratio_abs"])
            rows.append(
                {
                    "omega_label": label,
                    "omega_m": omega_m,
                    "a": float(a),
                    "classical": float(r["classical"]),
                    "correction": float(r["correction"]),
                    "ratio_signed": float(r["ratio_signed"]),
                    "ratio_abs": float(r["ratio_abs"]),
                }
            )

        summary[label] = {
            "omega_m": omega_m,
            "ratio_abs_at_1e-6": float(ratio_values[0]),
            "ratio_abs_at_1e-3": float(ratio_values[3]),
            "ratio_abs_at_1e-1": float(ratio_values[5]),
            "ratio_abs_at_1": float(ratio_values[7]),
            "ratio_abs_min": float(np.min(ratio_values)),
            "ratio_abs_max": float(np.max(ratio_values)),
        }

    with (out_dir / "symbolic_correction_ratio_rows.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    with (out_dir / "symbolic_correction_ratio_summary.json").open("w", encoding="utf-8") as f:
        json.dump({"symbolic_validation": asdict(symbolic), "summary": summary}, f, indent=2)

    print(out_dir)


if __name__ == "__main__":
    main()
