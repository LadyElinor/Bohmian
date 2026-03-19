from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from grqm.bohmian_probe.guidance import BohmianParams, guarded_quantum_accel, guidance_rhs, quantum_potential
from grqm.bohmian_probe.runner_phase1 import run_phase1


def test_q_finite_away_from_singular_points():
    p = BohmianParams(epsilon_q=1.0, quantum_model="gaussian")
    q = quantum_potential(a=0.5, phi=0.1, p=p)
    assert np.isfinite(q)


def test_guarded_quantum_accel_is_clamped():
    p = BohmianParams(epsilon_q=100.0, quantum_model="plateau", max_quantum_accel_ratio=0.5)
    q = guarded_quantum_accel(a=0.2, phi=0.3, p=p)
    assert np.isfinite(q)
    assert abs(q) <= 10.0


def test_guidance_rhs_finite_on_nominal_state():
    p = BohmianParams(omega_m=0.3, epsilon_q=0.5)
    y = np.array([0.1, 0.01, 1.5, 0.0], dtype=float)
    f = guidance_rhs(0.0, y, p)
    assert np.all(np.isfinite(f))


def test_phase1_runner_outputs_and_schema(tmp_path: Path):
    result = run_phase1(tmp_path)

    required = [
        "decision.json",
        "summary.json",
        "summary.md",
        "symbolic_receipt.json",
        "01_boundary_map.csv",
        "02_solver_stress.csv",
        "03_null_checks.csv",
        "04_variant_sensitivity.csv",
    ]
    for name in required:
        assert (tmp_path / name).exists(), f"Missing artifact: {name}"

    decision = json.loads((tmp_path / "decision.json").read_text(encoding="utf-8"))
    assert decision["recommendation"] in {"PASS_FOUNDATION", "HOLD_FOUNDATION", "REJECT_FOUNDATION"}

    summary = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))
    assert "metrics" in summary
    assert 0.0 <= float(summary["metrics"]["unstable_rate"]) <= 1.0
    assert float(summary["metrics"]["max_null_ref_l2"]) <= 0.05

    assert isinstance(result, dict)
    assert "decision" in result and "summary" in result


def test_phase1_unstable_rate_derisked(tmp_path: Path):
    run_phase1(tmp_path)
    summary = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))
    assert float(summary["metrics"]["unstable_rate"]) <= 0.2
