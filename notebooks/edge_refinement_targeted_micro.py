from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


class IC:
    t0 = 0.0
    t1 = 3.0
    a0 = 0.1
    v0 = 1.5


def l2_rel_err(err, ref, eps=1e-15):
    num = float(np.sqrt(np.mean((err) ** 2)))
    den = float(np.sqrt(np.mean(ref**2)) + eps)
    return num / den


def rhs(_t, y, omega_m: float, alpha_qg: float, corrected: bool, correction_power: int = 5):
    a, v = y
    if a <= 0:
        return [0.0, 0.0]
    base = -(omega_m) / (2.0 * a * a) + (1.0 - omega_m) * a
    corr = alpha_qg / (a**correction_power) if corrected else 0.0
    return [v, base + corr]


def integrate_dense(omega_m, alpha_qg, use_approx, method='Radau', t_span=None, rtol=1e-11, atol=1e-13, a0=0.1, v0=1.5):
    if t_span is None:
        t_span = (IC.t0, IC.t1)

    max_step = 2e-4
    first_step = 5e-6
    event_floor = 1e-7

    def event_stop(_t, y):
        return y[0] - event_floor

    event_stop.terminal = True
    event_stop.direction = -1

    sol = solve_ivp(
        fun=lambda t, y: rhs(t, y, omega_m, alpha_qg, use_approx),
        t_span=t_span,
        y0=[a0, v0],
        method=method,
        rtol=rtol,
        atol=atol,
        max_step=max_step,
        first_step=first_step,
        events=event_stop,
        dense_output=True,
    )
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol


def smooth(x: np.ndarray, window: int = 7) -> np.ndarray:
    if window <= 1:
        return x
    if window % 2 == 0:
        window += 1
    k = np.ones(window) / window
    return np.convolve(x, k, mode='same')


def q1_delta_dense(omega_m: float, alpha_qg: float, dt_eval: float, smooth_window: int = 1):
    t = np.linspace(IC.t0, IC.t1, int(round((IC.t1 - IC.t0) / dt_eval)) + 1)
    b = integrate_dense(omega_m, alpha_qg, False)
    c = integrate_dense(omega_m, alpha_qg, True)
    a_b = b.sol(t)[0]
    a_c = c.sol(t)[0]
    delta = a_c - a_b
    if smooth_window > 1:
        delta = smooth(delta, smooth_window)
    return float(l2_rel_err(delta, a_b)), t, a_b, a_c


def q1_refine_dense(omega_m: float, alpha_qg: float, dt_main=1e-3, smooth_window: int = 1):
    dt_ref = dt_main / 2
    _, t_m, a_b_m, a_c_m = q1_delta_dense(omega_m, alpha_qg, dt_main, smooth_window=smooth_window)
    _, t_r, a_b_r, a_c_r = q1_delta_dense(omega_m, alpha_qg, dt_ref, smooth_window=smooth_window)
    a_b_m_on_r = np.interp(t_r, t_m, a_b_m)
    a_c_m_on_r = np.interp(t_r, t_m, a_c_m)
    e1 = l2_rel_err(a_b_m_on_r - a_b_r, a_b_r)
    e2 = l2_rel_err(a_c_m_on_r - a_c_r, a_c_r)
    return float(max(e1, e2))


def main():
    root = Path(__file__).resolve().parents[1]
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    out_dir = root / 'notebooks' / 'outputs' / f'grqm_edge_refinement_targeted_{ts}'
    out_dir.mkdir(parents=True, exist_ok=True)

    targets = [
        (0.3075, 7e-7),
        (0.3075, 1e-6),
        (0.31, 7e-7),
        (0.31, 1e-6),
    ]

    thresholds = {
        'q1_refinement_max': 1e-6,
    }

    rows = []
    for om, aq in targets:
        r_plain = q1_refine_dense(om, aq, dt_main=1e-3, smooth_window=1)
        r_sm7 = q1_refine_dense(om, aq, dt_main=1e-3, smooth_window=7)
        r_sm11 = q1_refine_dense(om, aq, dt_main=1e-3, smooth_window=11)
        rows.append({
            'omega_m': om,
            'alpha_qg': aq,
            'q1_refine_dense_plain': r_plain,
            'q1_refine_dense_sm7': r_sm7,
            'q1_refine_dense_sm11': r_sm11,
            'pass_plain': r_plain <= thresholds['q1_refinement_max'],
            'pass_sm7': r_sm7 <= thresholds['q1_refinement_max'],
            'pass_sm11': r_sm11 <= thresholds['q1_refinement_max'],
        })

    with (out_dir / 'edge_refinement_targeted_summary.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    agg = {
        'n_rows': len(rows),
        'max_plain': float(max(r['q1_refine_dense_plain'] for r in rows)),
        'max_sm7': float(max(r['q1_refine_dense_sm7'] for r in rows)),
        'max_sm11': float(max(r['q1_refine_dense_sm11'] for r in rows)),
        'threshold': thresholds['q1_refinement_max'],
        'pass_rate_plain': float(sum(1 for r in rows if r['pass_plain']) / len(rows)),
        'pass_rate_sm7': float(sum(1 for r in rows if r['pass_sm7']) / len(rows)),
        'pass_rate_sm11': float(sum(1 for r in rows if r['pass_sm11']) / len(rows)),
    }
    (out_dir / 'edge_refinement_targeted_aggregate.json').write_text(json.dumps(agg, indent=2), encoding='utf-8')
    print(json.dumps({'out_dir': str(out_dir), **agg}, indent=2))


if __name__ == '__main__':
    main()
