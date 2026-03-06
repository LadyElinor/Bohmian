from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

import numpy as np

try:
    from astropy.cosmology import FlatLambdaCDM
    import astropy.units as u
except Exception as e:  # pragma: no cover
    raise SystemExit(
        "Astropy is required for this validation. Install with: pip install astropy>=6.0.0\n"
        f"Import error: {e}"
    )

from grqm.core import IC, Params, RunConfig, integrate

ROOT = Path(__file__).resolve().parents[1]
OUT_BASE = ROOT / "notebooks" / "outputs"


@dataclass
class SweepCase:
    label: str
    omega_m: float
    dt: float
    a0: float
    v0: float


SWEEP_CASES = [
    SweepCase("core0285_baseline", 0.285, 1e-3, 0.10, 1.50),
    SweepCase("core0285_dt_half", 0.285, 5e-4, 0.10, 1.50),
    SweepCase("core0285_a0_plus", 0.285, 1e-3, 0.11, 1.50),
    SweepCase("core0285_v0_minus", 0.285, 1e-3, 0.10, 1.45),
    SweepCase("core0300_baseline", 0.300, 1e-3, 0.10, 1.50),
    SweepCase("core0300_dt_half", 0.300, 5e-4, 0.10, 1.50),
    SweepCase("core0300_a0_plus", 0.300, 1e-3, 0.11, 1.50),
    SweepCase("core0300_v0_minus", 0.300, 1e-3, 0.10, 1.45),
    SweepCase("edge03075_baseline", 0.3075, 1e-3, 0.10, 1.50),
    SweepCase("edge03075_dt_half", 0.3075, 5e-4, 0.10, 1.50),
    SweepCase("edge03075_a0_plus", 0.3075, 1e-3, 0.11, 1.50),
    SweepCase("edge03075_v0_minus", 0.3075, 1e-3, 0.10, 1.45),
]


@dataclass
class SweepResult:
    label: str
    omega_m: float
    dt: float
    a0: float
    v0: float
    shape_l2_error: float
    shape_max_abs_error: float
    monotonic_model: bool


def _normalize_unit_interval(x: np.ndarray) -> np.ndarray:
    x0 = float(x[0])
    x1 = float(x[-1])
    if abs(x1 - x0) < 1e-15:
        return np.zeros_like(x)
    return (x - x0) / (x1 - x0)


def _astropy_ref(omega_m: float, n: int = 1200) -> tuple[np.ndarray, np.ndarray]:
    cosmo = FlatLambdaCDM(H0=70.0, Om0=omega_m, Tcmb0=2.725 * u.K)
    z = np.linspace(0.0, 10.0, n)
    a = 1.0 / (1.0 + z)
    t_lb = cosmo.lookback_time(z).to_value(u.Gyr)
    tau = _normalize_unit_interval(t_lb)
    return tau, a


def evaluate(case: SweepCase) -> SweepResult:
    p = Params(omega_m=case.omega_m, omega_l=1.0 - case.omega_m, alpha_qg=0.0)
    ic = IC(t0=0.0, t1=3.0, a0=case.a0, v0=case.v0)
    cfg = RunConfig(dt=case.dt, method="rk4", corrected=False)

    t, a, _ = integrate(ic, p, cfg)
    tau = _normalize_unit_interval(t)
    tau_u = np.linspace(0.0, 1.0, 1200)
    a_model = np.interp(tau_u, tau, a)

    tau_ref, a_ref_raw = _astropy_ref(case.omega_m)
    a_ref = np.interp(tau_u, tau_ref, a_ref_raw)

    # shape-only comparison via normalized amplitude
    a_model_n = _normalize_unit_interval(a_model)
    a_ref_n = _normalize_unit_interval(a_ref)

    err = a_model_n - a_ref_n

    return SweepResult(
        label=case.label,
        omega_m=case.omega_m,
        dt=case.dt,
        a0=case.a0,
        v0=case.v0,
        shape_l2_error=float(np.sqrt(np.mean(err**2))),
        shape_max_abs_error=float(np.max(np.abs(err))),
        monotonic_model=bool(np.all(np.diff(a) >= -1e-12)),
    )


def main() -> None:
    results = [evaluate(c) for c in SWEEP_CASES]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = OUT_BASE / f"grqm_astropy_background_sensitivity_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = [asdict(r) for r in results]
    (out_dir / "astropy_background_sensitivity.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")

    header = "label,omega_m,dt,a0,v0,shape_l2_error,shape_max_abs_error,monotonic_model"
    csv_lines = [header]
    for r in results:
        csv_lines.append(
            f"{r.label},{r.omega_m},{r.dt},{r.a0},{r.v0},{r.shape_l2_error},{r.shape_max_abs_error},{r.monotonic_model}"
        )
    (out_dir / "astropy_background_sensitivity_summary.csv").write_text("\n".join(csv_lines) + "\n", encoding="utf-8")

    # compact aggregates by omega_m
    agg = {}
    for om in sorted({r.omega_m for r in results}):
        block = [r for r in results if r.omega_m == om]
        agg[str(om)] = {
            "n_cases": len(block),
            "l2_min": min(r.shape_l2_error for r in block),
            "l2_max": max(r.shape_l2_error for r in block),
            "max_abs_min": min(r.shape_max_abs_error for r in block),
            "max_abs_max": max(r.shape_max_abs_error for r in block),
            "all_monotonic_model": all(r.monotonic_model for r in block),
        }

    (out_dir / "astropy_background_sensitivity_aggregate.json").write_text(
        json.dumps(agg, indent=2), encoding="utf-8"
    )

    print(json.dumps({"out_dir": str(out_dir), "aggregate": agg}, indent=2))


if __name__ == "__main__":
    main()
