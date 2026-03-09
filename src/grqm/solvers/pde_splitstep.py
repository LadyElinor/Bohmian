from __future__ import annotations

import numpy as np


def poisson_solve_periodic_1d(rho: np.ndarray, dx: float, kappa: float) -> np.ndarray:
    """Solve phi_xx = kappa * rho on a periodic 1D domain.

    Uses FFT with zero-mean gauge fix (phi_k[0] = 0).
    """
    n = rho.size
    k = 2.0 * np.pi * np.fft.fftfreq(n, d=dx)
    rho_k = np.fft.fft(rho)

    phi_k = np.zeros_like(rho_k, dtype=complex)
    mask = k != 0.0
    phi_k[mask] = -kappa * rho_k[mask] / (k[mask] ** 2)
    phi_k[~mask] = 0.0 + 0.0j

    phi = np.fft.ifft(phi_k)
    return np.real(phi)


def split_step_sn_1d(
    psi0: np.ndarray,
    dt: float,
    n_steps: int,
    x: np.ndarray,
    mass: float,
    hbar: float,
    kappa: float,
):
    """Second-order Strang split-step for 1D Schrödinger–Newton.

    i hbar dpsi/dt = [-(hbar^2 / 2m) dxx + m*phi] psi
    dxx phi = kappa * |psi|^2
    """
    psi = psi0.astype(complex).copy()
    n = psi.size
    dx = float(x[1] - x[0])
    k = 2.0 * np.pi * np.fft.fftfreq(n, d=dx)

    kinetic_phase_half = np.exp(-1j * (hbar * (k**2) / (2.0 * mass)) * (dt / 2.0))

    psi_hist = np.zeros((n_steps + 1, n), dtype=complex)
    phi_hist = np.zeros((n_steps + 1, n), dtype=float)
    psi_hist[0] = psi

    rho = np.abs(psi) ** 2
    phi = poisson_solve_periodic_1d(rho, dx=dx, kappa=kappa)
    phi_hist[0] = phi

    for i in range(1, n_steps + 1):
        # kinetic half-step
        psi_k = np.fft.fft(psi)
        psi = np.fft.ifft(kinetic_phase_half * psi_k)

        # potential full-step (recompute from current density)
        rho = np.abs(psi) ** 2
        phi = poisson_solve_periodic_1d(rho, dx=dx, kappa=kappa)
        potential_phase = np.exp(-1j * (mass * phi / hbar) * dt)
        psi = potential_phase * psi

        # kinetic half-step
        psi_k = np.fft.fft(psi)
        psi = np.fft.ifft(kinetic_phase_half * psi_k)

        psi_hist[i] = psi
        phi_hist[i] = phi

    return psi_hist, phi_hist
