from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np

from ..solvers.pde_splitstep import split_step_sn_1d


@dataclass
class SNParams:
    n_grid: int = 256
    x_max: float = 20.0
    t_max: float = 0.5
    dt: float = 5e-4
    mass: float = 1.0
    hbar: float = 1.0
    kappa: float = 0.02  # effective coupling in toy units
    sigma0: float = 1.0
    x0: float = 0.0
    p0: float = 0.0


def _gaussian_packet(x: np.ndarray, sigma0: float, x0: float, p0: float, hbar: float):
    env = np.exp(-((x - x0) ** 2) / (4.0 * sigma0**2))
    phase = np.exp(1j * p0 * x / hbar)
    psi = env * phase
    norm = np.sqrt(np.trapezoid(np.abs(psi) ** 2, x))
    return psi / (norm + 1e-15)


def _sigma_x(x: np.ndarray, psi: np.ndarray):
    rho = np.abs(psi) ** 2
    z = np.trapezoid(rho, x) + 1e-15
    mu = np.trapezoid(x * rho, x) / z
    var = np.trapezoid(((x - mu) ** 2) * rho, x) / z
    return float(np.sqrt(max(var, 0.0)))


def _q1_signal(sig_sn: np.ndarray, sig_free: np.ndarray):
    return float(np.max(np.abs(sig_sn - sig_free)))


def _q2_refinement(sig_dt: np.ndarray, sig_dt2: np.ndarray):
    d = sig_dt2 - sig_dt
    return float(np.sqrt(np.mean(d**2)) / (np.sqrt(np.mean(sig_dt2**2)) + 1e-15))


def run_sn_1d(params: SNParams, seed: int = 0):
    """Run 1D Schrödinger–Newton and compute first-pass Q1/Q2 diagnostics."""
    np.random.seed(seed)

    x = np.linspace(-params.x_max, params.x_max, params.n_grid)
    n_steps = int(round(params.t_max / params.dt))
    t = np.linspace(0.0, params.t_max, n_steps + 1)

    psi0 = _gaussian_packet(x, params.sigma0, params.x0, params.p0, params.hbar)

    # SN evolution
    psi_sn, phi_sn = split_step_sn_1d(
        psi0=psi0,
        dt=params.dt,
        n_steps=n_steps,
        x=x,
        mass=params.mass,
        hbar=params.hbar,
        kappa=params.kappa,
    )

    # Free evolution (kappa=0)
    psi_free, _ = split_step_sn_1d(
        psi0=psi0,
        dt=params.dt,
        n_steps=n_steps,
        x=x,
        mass=params.mass,
        hbar=params.hbar,
        kappa=0.0,
    )

    sig_sn = np.array([_sigma_x(x, p) for p in psi_sn])
    sig_free = np.array([_sigma_x(x, p) for p in psi_free])
    q1 = _q1_signal(sig_sn, sig_free)

    # refinement check dt vs dt/2
    dt2 = params.dt / 2.0
    n_steps2 = int(round(params.t_max / dt2))
    t2 = np.linspace(0.0, params.t_max, n_steps2 + 1)

    psi_sn2, _ = split_step_sn_1d(
        psi0=psi0,
        dt=dt2,
        n_steps=n_steps2,
        x=x,
        mass=params.mass,
        hbar=params.hbar,
        kappa=params.kappa,
    )
    sig_sn2 = np.array([_sigma_x(x, p) for p in psi_sn2])
    sig_sn_dt_on_dt2 = np.interp(t2, t, sig_sn)
    q2_refine = _q2_refinement(sig_sn_dt_on_dt2, sig_sn2)

    norms = np.array([np.trapezoid(np.abs(p) ** 2, x) for p in psi_sn])
    norm_drift = float(np.max(np.abs(norms - norms[0])))

    return {
        "metadata": {
            "model": "schrodinger-newton-1d-toy",
            "seed": seed,
            "params": asdict(params),
        },
        "grid": {
            "n_grid": params.n_grid,
            "x_min": float(x[0]),
            "x_max": float(x[-1]),
            "n_steps": n_steps,
            "dt": params.dt,
        },
        "q1": {
            "sigma_deviation_max": q1,
            "sigma_sn_final": float(sig_sn[-1]),
            "sigma_free_final": float(sig_free[-1]),
        },
        "q2": {
            "refinement_rel_diff": q2_refine,
            "norm_drift_max": norm_drift,
        },
        "series": {
            "t": t.tolist(),
            "sigma_sn": sig_sn.tolist(),
            "sigma_free": sig_free.tolist(),
            "phi_sn_rms": [float(np.sqrt(np.mean(phi**2))) for phi in phi_sn],
        },
    }
