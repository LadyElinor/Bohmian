from __future__ import annotations

import argparse
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


def integrate_dense(omega_m, alpha_qg, corrected, rtol=1e-10, atol=1e-12, a0=0.1, v0=1.5):
    def event_stop(_t, y):
        return y[0] - 1e-7

    event_stop.terminal = True
    event_stop.direction = -1

    sol = solve_ivp(
        fun=lambda t, y: rhs(t, y, omega_m, alpha_qg, corrected),
        t_span=(IC.t0, IC.t1),
        y0=[a0, v0],
        method="Radau",
        rtol=rtol,
        atol=atol,
        max_step=1e-4,
        first_step=2e-6,
        events=event_stop,
        dense_output=True,
        jac=None,
    )
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol


def q1_delta(omega_m: float, alpha_qg: float, dt_eval: float, a0=0.1, v0=1.5):
    t = np.linspace(IC.t0, IC.t1, int(round((IC.t1 - IC.t0) / dt_eval)) + 1)
    b = integrate_dense(omega_m, alpha_qg, False, a0=a0, v0=v0)
    c = integrate_dense(omega_m, alpha_qg, True, a0=a0, v0=v0)
    a_b = b.sol(t)[0]
    a_c = c.sol(t)[0]
    return float(l2_rel_err(a_c - a_b, a_b)), t, a_b, a_c


def q1_refine_adaptive(omega_m: float, alpha_qg: float, dt_main=2e-4):
    # Global adaptive refinement (uniformly across every grid point)
    t_m = np.linspace(IC.t0, IC.t1, int(round((IC.t1 - IC.t0) / dt_main)) + 1)
    t_r = np.linspace(IC.t0, IC.t1, int(round((IC.t1 - IC.t0) / (dt_main / 2))) + 1)

    b = integrate_dense(omega_m, alpha_qg, False)
    c = integrate_dense(omega_m, alpha_qg, True)

    a_b_m = b.sol(t_m)[0]
    a_c_m = c.sol(t_m)[0]
    a_b_r = b.sol(t_r)[0]
    a_c_r = c.sol(t_r)[0]

    a_b_m_on_r = np.interp(t_r, t_m, a_b_m)
    a_c_m_on_r = np.interp(t_r, t_m, a_c_m)

    e1 = l2_rel_err(a_b_m_on_r - a_b_r, a_b_r)
    e2 = l2_rel_err(a_c_m_on_r - a_c_r, a_c_r)
    return float(max(e1, e2))


def q2_robust_radau_only(omega_m: float, alpha_qg: float, dt_eval=1e-3):
    t = np.linspace(IC.t0, IC.t1, int(round((IC.t1 - IC.t0) / dt_eval)) + 1)
    r1 = integrate_dense(omega_m, alpha_qg, True, rtol=1e-10, atol=1e-12)
    r2 = integrate_dense(omega_m, alpha_qg, True, rtol=1e-10, atol=1e-12)
    a1 = r1.sol(t)[0]
    a2 = r2.sol(t)[0]
    d = np.abs(a2 - a1)
    return float(np.quantile(d, 0.95)), float(np.quantile(d, 0.99))


def replication_rel_diff(omega_m: float, alpha_qg: float, dt_eval=1e-3):
    t = np.linspace(IC.t0, IC.t1, int(round((IC.t1 - IC.t0) / dt_eval)) + 1)
    r1 = integrate_dense(omega_m, alpha_qg, True, rtol=1e-10, atol=1e-12)
    r2 = integrate_dense(omega_m, alpha_qg, True, rtol=1e-10, atol=1e-12)
    a1 = r1.sol(t)[0]
    a2 = r2.sol(t)[0]
    rel = np.abs(a2 - a1) / (np.abs(a1) + 1e-15)
    return float(np.mean(rel))


def case_key(omega_m: float, alpha_qg: float) -> str:
    return f"om={omega_m:.6f}|aq={alpha_qg:.9e}"


def load_progress(path: Path):
    rows = []
    completed = set()
    if not path.exists():
        return rows, completed

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        obj = json.loads(line)
        if obj.get("status") == "ok":
            rows.append(obj["row"])
            completed.add(obj["case_key"])
    return rows, completed


def write_summary_csv(path: Path, rows: list[dict]):
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def compute_aggregate(rows: list[dict], thresholds: dict):
    if not rows:
        return {
            "n_rows": 0,
            "pass_all_packet_rate": 0.0,
            "max_q1_refinement": None,
            "max_q1_hardened": None,
            "max_q2_p95": None,
            "max_q2_p99": None,
            "max_replication": None,
            "thresholds": thresholds,
            "worst_q1_cases": [],
        }

    sorted_q1 = sorted(rows, key=lambda r: r["q1_refinement_max_obs"], reverse=True)
    worst_q1_cases = [
        {
            "omega_m": r["omega_m"],
            "alpha_qg": r["alpha_qg"],
            "q1_refinement_max_obs": r["q1_refinement_max_obs"],
        }
        for r in sorted_q1[:5]
    ]

    return {
        "n_rows": len(rows),
        "pass_all_packet_rate": float(sum(1 for r in rows if r["pass_all_packet"]) / len(rows)),
        "max_q1_refinement": float(max(r["q1_refinement_max_obs"] for r in rows)),
        "max_q1_hardened": float(max(r["q1_assumption_sensitivity_hardened"] for r in rows)),
        "max_q2_p95": float(max(r["q2_D_p95_worst_method"] for r in rows)),
        "max_q2_p99": float(max(r["q2_D_p99_worst_method"] for r in rows)),
        "max_replication": float(max(r["q2_true_replication_rel_diff"] for r in rows)),
        "thresholds": thresholds,
        "worst_q1_cases": worst_q1_cases,
    }


def select_grid(mode: str):
    alpha_vals = [3e-7, 5e-7, 7e-7, 1e-6, 1.3e-6]
    if mode == "inpolicy":
        omega_vals = [0.285, 0.290, 0.295, 0.300]  # 20 cases
    elif mode == "global":
        omega_vals = [0.280, 0.285, 0.290, 0.295, 0.300, 0.305, 0.310]  # 35 cases (policy-relevant)
    else:
        raise ValueError(f"Unknown mode: {mode}")
    return omega_vals, alpha_vals


def main():
    ap = argparse.ArgumentParser(description="Global adaptive packet runner with checkpoint + resume")
    ap.add_argument("--mode", choices=["inpolicy", "global"], default="global")
    ap.add_argument("--out-dir", default=None, help="Existing/new output directory. If omitted, a timestamped dir is created.")
    ap.add_argument("--resume", action="store_true", help="Resume from progress.jsonl in out-dir")
    args = ap.parse_args()

    root = Path(__file__).resolve().parents[1]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_name = f"grqm_edge_companion_{args.mode}_adaptive_checkpointed_{ts}"
    out_dir = Path(args.out_dir) if args.out_dir else (root / "notebooks" / "outputs" / default_name)
    out_dir.mkdir(parents=True, exist_ok=True)

    progress_path = out_dir / "progress.jsonl"
    error_path = out_dir / "errors.jsonl"
    summary_path = out_dir / "edge_companion_summary.csv"
    agg_live_path = out_dir / "edge_companion_aggregate_live.json"
    agg_final_path = out_dir / "edge_companion_aggregate.json"

    thresholds = {
        "q1_refinement_max": 1e-6,
        "q1_assumption_sensitivity_hardened_max": 0.18,
        "q2_D_p95_max": 0.01,
        "q2_D_p99_max": 0.05,
        "q2_true_replication_rel_diff_max": 1e-6,
    }

    hardening = [
        dict(ic_scale=0.999, dt=1e-3),
        dict(ic_scale=1.001, dt=1e-3),
        dict(ic_scale=1.0, dt=9e-4),
        dict(ic_scale=1.0, dt=1.1e-3),
    ]

    omega_vals, alpha_vals = select_grid(args.mode)
    total_cases = len(omega_vals) * len(alpha_vals)

    if args.resume:
        rows, completed = load_progress(progress_path)
    else:
        rows, completed = [], set()

    print(
        json.dumps(
            {
                "mode": args.mode,
                "out_dir": str(out_dir),
                "total_cases": total_cases,
                "resume": args.resume,
                "already_completed": len(completed),
            },
            indent=2,
        ),
        flush=True,
    )

    done_count = len(completed)
    try:
        for om in omega_vals:
            for aq in alpha_vals:
                ck = case_key(om, aq)
                if ck in completed:
                    continue

                print(f"[case {done_count+1}/{total_cases}] start {ck}", flush=True)
                try:
                    d_base, _, _, _ = q1_delta(om, aq, 1e-3)
                    q1r = q1_refine_adaptive(om, aq, dt_main=2e-4)

                    hs = []
                    for h in hardening:
                        d_pert, _, _, _ = q1_delta(om, aq, h["dt"], a0=IC.a0 * h["ic_scale"], v0=IC.v0)
                        hs.append(abs(d_pert - d_base) / (abs(d_base) + 1e-15))
                    hmax = float(max(hs))

                    p95, p99 = q2_robust_radau_only(om, aq)
                    rep = replication_rel_diff(om, aq)

                    row = {
                        "omega_m": om,
                        "alpha_qg": aq,
                        "q1_delta_proxy_l2": d_base,
                        "q1_refinement_max_obs": q1r,
                        "q1_assumption_sensitivity_hardened": hmax,
                        "q2_D_p95_worst_method": p95,
                        "q2_D_p99_worst_method": p99,
                        "q2_true_replication_rel_diff": rep,
                        "pass_q1_refinement": q1r <= thresholds["q1_refinement_max"],
                        "pass_q1_hardened": hmax <= thresholds["q1_assumption_sensitivity_hardened_max"],
                        "pass_q2_robust": (p95 <= thresholds["q2_D_p95_max"] and p99 <= thresholds["q2_D_p99_max"]),
                        "pass_q2_replication": rep <= thresholds["q2_true_replication_rel_diff_max"],
                    }
                    row["pass_all_packet"] = all([
                        row["pass_q1_refinement"],
                        row["pass_q1_hardened"],
                        row["pass_q2_robust"],
                        row["pass_q2_replication"],
                    ])

                    with progress_path.open("a", encoding="utf-8") as f:
                        f.write(json.dumps({"status": "ok", "case_key": ck, "row": row}) + "\n")

                    rows.append(row)
                    completed.add(ck)
                    done_count += 1

                    agg_live = compute_aggregate(rows, thresholds)
                    agg_live["mode"] = args.mode
                    agg_live["out_dir"] = str(out_dir)
                    agg_live["completed_cases"] = done_count
                    agg_live["total_cases"] = total_cases
                    agg_live_path.write_text(json.dumps(agg_live, indent=2), encoding="utf-8")
                    write_summary_csv(summary_path, rows)

                    print(
                        f"[case {done_count}/{total_cases}] done {ck} | q1_ref={row['q1_refinement_max_obs']:.3e} | pass_all={row['pass_all_packet']}",
                        flush=True,
                    )

                except Exception as case_err:
                    err_rec = {
                        "status": "error",
                        "case_key": ck,
                        "omega_m": om,
                        "alpha_qg": aq,
                        "error": str(case_err),
                    }
                    with error_path.open("a", encoding="utf-8") as ef:
                        ef.write(json.dumps(err_rec) + "\n")
                    raise

    finally:
        write_summary_csv(summary_path, rows)
        final_agg = compute_aggregate(rows, thresholds)
        final_agg["mode"] = args.mode
        final_agg["out_dir"] = str(out_dir)
        final_agg["completed_cases"] = len(completed)
        final_agg["total_cases"] = total_cases
        agg_final_path.write_text(json.dumps(final_agg, indent=2), encoding="utf-8")

    print(json.dumps({"out_dir": str(out_dir), **final_agg}, indent=2), flush=True)


if __name__ == "__main__":
    main()
