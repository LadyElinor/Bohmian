from __future__ import annotations

import csv
import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

import numpy as np

from .guidance import BohmianParams, integrate_fixed
from .symbolic_core import receipt_to_dict, symbolic_receipt


def l2_rel(x: np.ndarray, y: np.ndarray, eps: float = 1e-15) -> float:
    return float(np.sqrt(np.mean((x - y) ** 2)) / (np.sqrt(np.mean(y**2)) + eps))


def write_csv(path: Path, rows: list[dict]):
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def _run_case(omega_m: float, epsilon_q: float, model: str, dt: float = 1e-3) -> dict:
    p = BohmianParams(omega_m=omega_m, epsilon_q=epsilon_q, quantum_model=model)
    t0, t1 = 0.0, 2.0
    y0 = np.array([0.1, 0.01, 1.5, 0.0], dtype=float)
    t, y = integrate_fixed(t0, t1, dt, y0, p, method="rk4")
    finite = bool(np.all(np.isfinite(y)))
    max_abs = float(np.max(np.abs(y)))
    stable = bool(finite and max_abs < p.max_abs_state)
    return {
        "t": t,
        "y": y,
        "stable": stable,
        "min_a": float(np.min(y[:, 0])),
        "max_abs_state": max_abs,
    }


def run_phase1(out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)

    receipt = symbolic_receipt()
    (out_dir / "symbolic_receipt.json").write_text(json.dumps(receipt_to_dict(receipt), indent=2), encoding="utf-8")

    omega_grid = [0.295, 0.300, 0.305, 0.310, 0.315]
    eps_grid = [0.0, 0.10, 0.25, 0.50, 0.75, 1.00]

    boundary_rows: list[dict] = []
    stress_rows: list[dict] = []
    null_rows: list[dict] = []
    variant_rows: list[dict] = []

    unstable = 0
    total = 0
    max_null_l2 = 0.0
    max_inv_l2 = 0.0

    y0 = np.array([0.1, 0.01, 1.5, 0.0], dtype=float)
    t0, t1 = 0.0, 2.0

    for om in omega_grid:
        ref_params = BohmianParams(omega_m=om, epsilon_q=0.0, quantum_model="off")
        t_ref, y_ref = integrate_fixed(t0, t1, 5e-4, y0, ref_params, method="rk4")
        a_ref = y_ref[:, 0]

        # Null consistency (same model with coarser dt)
        t_null, y_null = integrate_fixed(t0, t1, 1e-3, y0, ref_params, method="rk4")
        a_null = np.interp(t_ref, t_null, y_null[:, 0])
        null_l2 = l2_rel(a_null, a_ref)
        max_null_l2 = max(max_null_l2, null_l2)

        # Solver stress at epsilon_q=0
        for m in ("euler", "heun", "rk4"):
            _t, y_num = integrate_fixed(t0, t1, 1e-3, y0, ref_params, method=m)
            a_num = np.interp(t_ref, np.linspace(t0, t1, len(y_num)), y_num[:, 0])
            inv_l2 = l2_rel(a_num, a_ref)
            max_inv_l2 = max(max_inv_l2, inv_l2)
            stress_rows.append(
                {
                    "omega_m": om,
                    "method": m,
                    "epsilon_q": 0.0,
                    "l2_vs_rk4_fine": inv_l2,
                    "stable": bool(np.all(np.isfinite(y_num))),
                }
            )

        null_rows.append(
            {
                "omega_m": om,
                "epsilon_q": 0.0,
                "null_ref_l2": null_l2,
                "threshold": 1.0e-2,
                "passes": bool(null_l2 <= 1.0e-2),
            }
        )

        for eps in eps_grid:
            case = _run_case(om, eps, model="gaussian", dt=1e-3)
            total += 1
            if not case["stable"]:
                unstable += 1
            boundary_rows.append(
                {
                    "omega_m": om,
                    "epsilon_q": eps,
                    "model": "gaussian",
                    "stable": case["stable"],
                    "min_a": case["min_a"],
                    "max_abs_state": case["max_abs_state"],
                }
            )

            if eps in (0.25, 0.75):
                for model in ("gaussian", "plateau"):
                    ref = _run_case(om, eps, model=model, dt=5e-4)
                    coarser = _run_case(om, eps, model=model, dt=1e-3)
                    a_ref_model = ref["y"][:, 0]
                    a_coarser = np.interp(ref["t"], coarser["t"], coarser["y"][:, 0])
                    variant_rows.append(
                        {
                            "omega_m": om,
                            "epsilon_q": eps,
                            "quantum_model": model,
                            "dt_l2_vs_ref": l2_rel(a_coarser, a_ref_model),
                            "stable_ref": ref["stable"],
                            "stable_coarser": coarser["stable"],
                        }
                    )

    unstable_rate = float(unstable / total) if total else 1.0

    write_csv(out_dir / "01_boundary_map.csv", boundary_rows)
    write_csv(out_dir / "02_solver_stress.csv", stress_rows)
    write_csv(out_dir / "03_null_checks.csv", null_rows)
    write_csv(out_dir / "04_variant_sensitivity.csv", variant_rows)

    pass_foundation = (
        receipt.hamiltonian_finite_on_nominal_point
        and receipt.decomposition_reconstruction_ok
        and receipt.wdw_residual_nominal_finite
        and max_null_l2 <= 1e-2
        and max_inv_l2 <= 2.2e-1
        and unstable_rate <= 0.1
    )

    if pass_foundation:
        rec = "PASS_FOUNDATION"
        rationale = "Symbolic and numerical sanity gates pass with low instability under guarded dynamics."
    elif unstable_rate <= 0.2 and max_null_l2 <= 1.2e-2:
        rec = "HOLD_FOUNDATION"
        rationale = "Core gates mostly pass; keep in HOLD while expanding canonical/observational bridge tests."
    else:
        rec = "REJECT_FOUNDATION"
        rationale = "Foundation lane remains too unstable or fails basic numerical consistency gates."

    decision = {
        "recommendation": rec,
        "rationale": rationale,
        "gates": {
            "symbolic_receipt_ok": bool(
                receipt.hamiltonian_finite_on_nominal_point
                and receipt.decomposition_reconstruction_ok
                and receipt.wdw_residual_nominal_finite
            ),
            "max_null_ref_l2": max_null_l2,
            "max_solver_invariance_l2": max_inv_l2,
            "unstable_rate": unstable_rate,
        },
        "caveats": [
            "Minisuperspace adaptation remains a truncation, not a full canonical quantization proof.",
            "No observational-fit or cosmological-parameter inference claim is made here.",
            "Quantum potential models are controlled proxies for stress-testing only.",
        ],
    }
    (out_dir / "decision.json").write_text(json.dumps(decision, indent=2), encoding="utf-8")

    summary = {
        "timestamp": datetime.now().isoformat(),
        "grid": {"omega_m": omega_grid, "epsilon_q": eps_grid},
        "metrics": {
            "max_null_ref_l2": max_null_l2,
            "max_solver_invariance_l2": max_inv_l2,
            "unstable_rate": unstable_rate,
            "stable_points": int(total - unstable),
            "total_points": int(total),
        },
        "symbolic_receipt": receipt_to_dict(receipt),
        "governance_note": "Phase-1 adaptation evidence package; conservative interpretation only.",
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    md = [
        "# Bohmian/de Broglie Adaptation Sprint Summary",
        "",
        f"- Timestamp: {summary['timestamp']}",
        f"- Recommendation: **{rec}**",
        f"- Rationale: {rationale}",
        "",
        "## Key Metrics",
        f"- Max null-reference L2: {max_null_l2:.3e}",
        f"- Max solver-invariance L2: {max_inv_l2:.3e}",
        f"- Unstable rate: {unstable_rate:.3f}",
        f"- Stable grid points: {total - unstable}/{total}",
        "",
        "## Caveats",
        "- Minisuperspace truncation and proxy quantum models are methodological scaffolds.",
        "- Results are internal stability diagnostics, not empirical validation.",
        "- Further canonical and data-facing lanes are required before promotion beyond foundation.",
    ]
    (out_dir / "summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # Backward-compatible legacy names expected by earlier smoke tests.
    (out_dir / "phase1_decision.json").write_text(json.dumps(decision, indent=2), encoding="utf-8")
    (out_dir / "phase1_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (out_dir / "phase1_summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    write_csv(out_dir / "guidance_sanity_checks.csv", boundary_rows)

    return {"decision": decision, "summary": summary, "out_dir": str(out_dir)}


def main():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path("outputs") / f"bohmian_adaptation_{ts}"
    result = run_phase1(out_dir)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
