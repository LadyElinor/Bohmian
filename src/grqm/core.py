from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np


@dataclass
class Params:
    omega_m: float = 0.3
    omega_l: float = 0.7
    alpha_qg: float = 1.0e-7


@dataclass
class IC:
    t0: float = 0.0
    t1: float = 3.0
    a0: float = 0.1
    v0: float = 1.5


@dataclass
class RunConfig:
    dt: float
    method: str = "rk4"  # rk4 or euler
    corrected: bool = False
    correction_power: int = 5


def accel(a: float, p: Params, corrected: bool, correction_power: int = 5) -> float:
    base = -(p.omega_m) / (2.0 * a * a) + p.omega_l * a
    if corrected:
        return base + p.alpha_qg / (a**correction_power)
    return base


def rhs(y, p: Params, corrected: bool, correction_power: int = 5):
    a, v = y
    return np.array([v, accel(a, p, corrected, correction_power)], dtype=float)


def step_euler(y, dt, p, corrected, correction_power):
    return y + dt * rhs(y, p, corrected, correction_power)


def step_rk4(y, dt, p, corrected, correction_power):
    k1 = rhs(y, p, corrected, correction_power)
    k2 = rhs(y + 0.5 * dt * k1, p, corrected, correction_power)
    k3 = rhs(y + 0.5 * dt * k2, p, corrected, correction_power)
    k4 = rhs(y + dt * k3, p, corrected, correction_power)
    return y + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)


def integrate(ic: IC, p: Params, cfg: RunConfig):
    n = int(round((ic.t1 - ic.t0) / cfg.dt))
    t = np.linspace(ic.t0, ic.t1, n + 1)
    y = np.zeros((n + 1, 2), dtype=float)
    y[0, 0] = ic.a0
    y[0, 1] = ic.v0

    for i in range(n):
        if y[i, 0] <= 0:
            y[i + 1 :] = y[i]
            break
        if cfg.method == "euler":
            y[i + 1] = step_euler(y[i], cfg.dt, p, cfg.corrected, cfg.correction_power)
        elif cfg.method == "rk4":
            y[i + 1] = step_rk4(y[i], cfg.dt, p, cfg.corrected, cfg.correction_power)
        else:
            raise ValueError(f"Unknown method: {cfg.method}")

    return t, y[:, 0], y[:, 1]


def interp_to_grid(t_src, x_src, t_dst):
    return np.interp(t_dst, t_src, x_src)


def l2_rel_err(err, ref, eps=1e-15):
    num = float(np.sqrt(np.mean((err) ** 2)))
    den = float(np.sqrt(np.mean(ref**2)) + eps)
    return num / den


def run_cycle(out_dir: Path):
    np.random.seed(42)
    p = Params()
    ic = IC()

    dt_main = 1e-3
    dt_ref = 5e-4
    dt_exact = 2.5e-4
    dt_coarse = 2e-3

    t_b, a_b, _ = integrate(ic, p, RunConfig(dt=dt_main, method="rk4", corrected=False))
    t_c, a_c, _ = integrate(ic, p, RunConfig(dt=dt_main, method="rk4", corrected=True))

    delta_proxy_l2 = l2_rel_err(a_c - a_b, a_b)
    delta_proxy_max_abs = float(np.max(np.abs(a_c - a_b)))
    delta_proxy_sign_final = float(np.sign((a_c - a_b)[-1]))

    t_b_ref, a_b_ref, _ = integrate(ic, p, RunConfig(dt=dt_ref, method="rk4", corrected=False))
    t_c_ref, a_c_ref, _ = integrate(ic, p, RunConfig(dt=dt_ref, method="rk4", corrected=True))

    a_b_main_on_ref = interp_to_grid(t_b, a_b, t_b_ref)
    a_c_main_on_ref = interp_to_grid(t_c, a_c, t_c_ref)

    baseline_refinement_error = l2_rel_err(a_b_main_on_ref - a_b_ref, a_b_ref)
    corrected_refinement_error = l2_rel_err(a_c_main_on_ref - a_c_ref, a_c_ref)

    _, a_c_n4, _ = integrate(ic, p, RunConfig(dt=dt_main, method="rk4", corrected=True, correction_power=4))
    delta_proxy_n4_l2 = l2_rel_err(a_c_n4 - a_b, a_b)
    assumption_sensitivity_rel = abs(delta_proxy_n4_l2 - delta_proxy_l2) / (abs(delta_proxy_l2) + 1e-15)

    t_exact, a_exact, _ = integrate(ic, p, RunConfig(dt=dt_exact, method="rk4", corrected=True))
    t_approx, a_approx, _ = integrate(ic, p, RunConfig(dt=dt_main, method="euler", corrected=True))

    a_approx_on_exact = interp_to_grid(t_approx, a_approx, t_exact)
    D_t = np.abs(a_approx_on_exact - a_exact)
    D_star = float(np.mean(D_t))
    D_max = float(np.max(D_t))

    t_alt, a_alt, _ = integrate(ic, p, RunConfig(dt=dt_coarse, method="rk4", corrected=True))
    a_alt_on_exact = interp_to_grid(t_alt, a_alt, t_exact)
    D_t_alt = np.abs(a_alt_on_exact - a_exact)
    D_star_alt = float(np.mean(D_t_alt))
    D_max_alt = float(np.max(D_t_alt))

    stat_u = 0.0
    sys_u_q1 = float(max(baseline_refinement_error, corrected_refinement_error))
    epi_u_q1 = float(assumption_sensitivity_rel * abs(delta_proxy_l2))
    total_u_q1 = float(math.sqrt(stat_u**2 + sys_u_q1**2 + epi_u_q1**2))

    sys_u_q2 = float(abs(D_star_alt - D_star))
    epi_u_q2 = 0.0
    total_u_q2 = float(math.sqrt(stat_u**2 + sys_u_q2**2 + epi_u_q2**2))

    results = {
        "metadata": {
            "seed": 42,
            "units": "dimensionless",
            "model": "FRW-inspired minisuperspace toy ODE",
            "ic": asdict(ic),
            "params": asdict(p),
        },
        "thresholds": {
            "q1_effect_persist_min": 1e-4,
            "q1_refinement_max": 5e-3,
            "q1_assumption_sensitivity_max": 0.5,
            "q2_Dstar_min": 1e-4,
            "q2_replication_rel_diff_max": 0.5,
        },
        "q1": {
            "delta_proxy_l2": delta_proxy_l2,
            "delta_proxy_max_abs": delta_proxy_max_abs,
            "delta_proxy_sign_final": delta_proxy_sign_final,
            "baseline_refinement_error": baseline_refinement_error,
            "corrected_refinement_error": corrected_refinement_error,
            "delta_proxy_n4_l2": delta_proxy_n4_l2,
            "assumption_sensitivity_rel": assumption_sensitivity_rel,
            "uncertainty": {
                "stat": stat_u,
                "sys": sys_u_q1,
                "epi": epi_u_q1,
                "total": total_u_q1,
            },
        },
        "q2": {
            "D_star": D_star,
            "D_max": D_max,
            "D_star_alt": D_star_alt,
            "D_max_alt": D_max_alt,
            "replication_rel_diff": abs(D_star_alt - D_star) / (abs(D_star) + 1e-15),
            "uncertainty": {
                "stat": stat_u,
                "sys": sys_u_q2,
                "epi": epi_u_q2,
                "total": total_u_q2,
            },
        },
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "grqm_proxy_results_v1.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    summary_lines = [
        "metric,value",
        f"q1.delta_proxy_l2,{delta_proxy_l2}",
        f"q1.delta_proxy_max_abs,{delta_proxy_max_abs}",
        f"q1.baseline_refinement_error,{baseline_refinement_error}",
        f"q1.corrected_refinement_error,{corrected_refinement_error}",
        f"q1.assumption_sensitivity_rel,{assumption_sensitivity_rel}",
        f"q1.unc_total,{total_u_q1}",
        f"q2.D_star,{D_star}",
        f"q2.D_max,{D_max}",
        f"q2.D_star_alt,{D_star_alt}",
        f"q2.replication_rel_diff,{abs(D_star_alt - D_star) / (abs(D_star) + 1e-15)}",
        f"q2.unc_total,{total_u_q2}",
    ]
    with open(out_dir / "grqm_proxy_results_v1_summary.csv", "w", encoding="utf-8") as f:
        f.write("\n".join(summary_lines) + "\n")

    return results
