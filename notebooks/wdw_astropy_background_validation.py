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
class Case:
    label: str
    omega_m: float


CASES = [
    Case("core_0285", 0.285),
    Case("core_0300", 0.300),
    Case("edge_03075", 0.3075),
]


@dataclass
class CaseResult:
    label: str
    omega_m: float
    omega_l: float
    n_points_model: int
    n_points_astropy: int
    shape_l2_error: float
    shape_max_abs_error: float
    monotonic_model: bool
    monotonic_astropy: bool


def _interp_linear(x_src: np.ndarray, y_src: np.ndarray, x_dst: np.ndarray) -> np.ndarray:
    return np.interp(x_dst, x_src, y_src)


def _normalize_unit_interval(x: np.ndarray) -> np.ndarray:
    x0 = float(x[0])
    x1 = float(x[-1])
    if abs(x1 - x0) < 1e-15:
        return np.zeros_like(x)
    return (x - x0) / (x1 - x0)


def _astropy_a_of_lookback_fraction(omega_m: float, n: int = 1200) -> tuple[np.ndarray, np.ndarray]:
    """
    Build an Astropy ΛCDM reference trajectory as a(τ) over τ in [0,1],
    where τ is normalized lookback time fraction from today (z=0) to z_max.

    This is a shape-only diagnostic (unitless time normalization), not a
    direct unit-calibrated identity test against the toy ODE clock.
    """
    cosmo = FlatLambdaCDM(H0=70.0, Om0=omega_m, Tcmb0=2.725 * u.K)

    z = np.linspace(0.0, 10.0, n)
    a = 1.0 / (1.0 + z)
    t_lb = cosmo.lookback_time(z).to_value(u.Gyr)

    tau = _normalize_unit_interval(t_lb)
    # tau increasing with z; use it directly and map to a
    return tau, a


def _model_a_of_fraction(omega_m: float, n_target: int = 1200) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    p = Params(omega_m=omega_m, omega_l=1.0 - omega_m, alpha_qg=0.0)
    ic = IC(t0=0.0, t1=3.0, a0=0.1, v0=1.5)
    cfg = RunConfig(dt=1e-3, method="rk4", corrected=False)

    t, a, _ = integrate(ic, p, cfg)
    tau = _normalize_unit_interval(t)

    tau_ref = np.linspace(0.0, 1.0, n_target)
    a_ref = _interp_linear(tau, a, tau_ref)
    return tau_ref, a_ref, t, a


def evaluate_case(case: Case) -> CaseResult:
    tau_model, a_model, t_raw, a_raw = _model_a_of_fraction(case.omega_m)
    tau_ref, a_ref_raw = _astropy_a_of_lookback_fraction(case.omega_m)

    # Put both on same normalized amplitude range for shape comparison only.
    a_ref = _normalize_unit_interval(a_ref_raw)
    a_mod = _normalize_unit_interval(a_model)

    a_ref_on_model = _interp_linear(tau_ref, a_ref, tau_model)
    err = a_mod - a_ref_on_model
    l2 = float(np.sqrt(np.mean(err**2)))
    mx = float(np.max(np.abs(err)))

    return CaseResult(
        label=case.label,
        omega_m=case.omega_m,
        omega_l=1.0 - case.omega_m,
        n_points_model=int(len(t_raw)),
        n_points_astropy=int(len(tau_ref)),
        shape_l2_error=l2,
        shape_max_abs_error=mx,
        monotonic_model=bool(np.all(np.diff(a_raw) >= -1e-12)),
        monotonic_astropy=bool(np.all(np.diff(a_ref_raw[::-1]) >= -1e-12)),
    )


def main() -> None:
    results = [evaluate_case(c) for c in CASES]

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = OUT_BASE / f"grqm_astropy_background_validation_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = [asdict(r) for r in results]

    (out_dir / "astropy_background_validation.json").write_text(
        json.dumps(
            {
                "study": "Astropy ΛCDM background shape cross-check",
                "note": (
                    "Shape-only diagnostic using normalized time/amplitude. "
                    "Not a unit-identical claim because toy ODE time scaling differs."
                ),
                "cases": rows,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    csv_lines = [
        "label,omega_m,omega_l,n_points_model,n_points_astropy,shape_l2_error,shape_max_abs_error,monotonic_model,monotonic_astropy"
    ]
    for r in results:
        csv_lines.append(
            f"{r.label},{r.omega_m},{r.omega_l},{r.n_points_model},{r.n_points_astropy},{r.shape_l2_error},{r.shape_max_abs_error},{r.monotonic_model},{r.monotonic_astropy}"
        )
    (out_dir / "astropy_background_validation_summary.csv").write_text(
        "\n".join(csv_lines) + "\n", encoding="utf-8"
    )

    print(
        json.dumps(
            {
                "out_dir": str(out_dir),
                "cases": rows,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
