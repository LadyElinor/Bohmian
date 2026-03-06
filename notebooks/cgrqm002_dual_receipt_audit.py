from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT_BASE = ROOT / "notebooks" / "outputs"

RUN_DIRS = [
    OUT_BASE / "grqm_cgrqm002_rk_family_minipack_20260305_171537",
    OUT_BASE / "grqm_cgrqm002_rk_family_minipack_20260305_184849",
]

# Acceptance bounds (must match predeclared mini-pack note)
MAX_Q2_D_P95 = 0.50
MAX_Q2_D_P99 = 0.80
MAX_ABS_SPREAD_P95 = 1e-8
MAX_REPL_REL_DIFF = 1e-6


@dataclass
class RunMetrics:
    run_dir: str
    n_points: int
    all_points_pass: bool
    global_max_q2_D_p95: float
    global_max_q2_D_p99: float
    global_max_rk_family_abs_spread_p95: float
    global_max_replication_rel_diff: float


def load_metrics(run_dir: Path) -> RunMetrics:
    summary = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
    return RunMetrics(
        run_dir=str(run_dir),
        n_points=int(summary["n_points"]),
        all_points_pass=bool(summary["all_points_pass"]),
        global_max_q2_D_p95=float(summary["global_max_q2_D_p95"]),
        global_max_q2_D_p99=float(summary["global_max_q2_D_p99"]),
        global_max_rk_family_abs_spread_p95=float(summary["global_max_rk_family_abs_spread_p95"]),
        global_max_replication_rel_diff=float(summary["global_max_replication_rel_diff"]),
    )


def acceptance_pass(m: RunMetrics) -> bool:
    return (
        m.all_points_pass
        and m.global_max_q2_D_p95 <= MAX_Q2_D_P95
        and m.global_max_q2_D_p99 <= MAX_Q2_D_P99
        and m.global_max_rk_family_abs_spread_p95 <= MAX_ABS_SPREAD_P95
        and m.global_max_replication_rel_diff <= MAX_REPL_REL_DIFF
    )


def point_table(run_dir: Path) -> pd.DataFrame:
    df = pd.read_csv(run_dir / "rk_family_point_summary.csv")
    key_cols = ["omega_m", "alpha_qg"]
    metric_cols = [
        "max_q2_D_p95",
        "max_q2_D_p99",
        "rk_family_abs_spread_p95",
        "q2_true_replication_rel_diff",
        "pass_acceptance",
    ]
    return df[key_cols + metric_cols].sort_values(key_cols).reset_index(drop=True)


def main() -> None:
    metrics = [load_metrics(d) for d in RUN_DIRS]
    run_pass = [acceptance_pass(m) for m in metrics]

    p0 = point_table(RUN_DIRS[0])
    p1 = point_table(RUN_DIRS[1])

    numeric_cols = [
        "max_q2_D_p95",
        "max_q2_D_p99",
        "rk_family_abs_spread_p95",
        "q2_true_replication_rel_diff",
    ]
    key_cols = ["omega_m", "alpha_qg"]

    joined = p0.merge(p1, on=key_cols, suffixes=("_run1", "_run2"))
    max_abs_metric_diff = {
        col: float((joined[f"{col}_run1"] - joined[f"{col}_run2"]).abs().max())
        for col in numeric_cols
    }
    point_pass_identical = bool((joined["pass_acceptance_run1"] == joined["pass_acceptance_run2"]).all())

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = OUT_BASE / f"grqm_cgrqm002_dual_receipt_audit_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    report = {
        "audit": "C-GRQM-002 dual mini-pack receipt consistency",
        "run_dirs": [str(d) for d in RUN_DIRS],
        "acceptance_bounds": {
            "max_q2_D_p95": MAX_Q2_D_P95,
            "max_q2_D_p99": MAX_Q2_D_P99,
            "max_rk_family_abs_spread_p95": MAX_ABS_SPREAD_P95,
            "max_replication_rel_diff": MAX_REPL_REL_DIFF,
        },
        "runs": [asdict(m) for m in metrics],
        "run_acceptance_pass": run_pass,
        "both_runs_acceptance_pass": all(run_pass),
        "point_pass_identical": point_pass_identical,
        "max_abs_metric_diff_across_runs": max_abs_metric_diff,
        "decision": "PASS" if all(run_pass) and point_pass_identical else "FAIL",
    }

    (out_dir / "dual_receipt_audit_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    joined.to_csv(out_dir / "dual_receipt_point_compare.csv", index=False)

    print(json.dumps({"out_dir": str(out_dir), "decision": report["decision"]}, indent=2))


if __name__ == "__main__":
    main()
