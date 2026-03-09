from __future__ import annotations

import argparse
import json
from pathlib import Path

from grqm.models.schrodinger_newton import SNParams, run_sn_1d


def main():
    ap = argparse.ArgumentParser(description="Run 1D Schrödinger-Newton toy diagnostic")
    ap.add_argument("--out-dir", default="outputs", help="Output directory")
    ap.add_argument("--kappa", type=float, default=0.02)
    ap.add_argument("--dt", type=float, default=5e-4)
    ap.add_argument("--t-max", type=float, default=0.5)
    ap.add_argument("--n-grid", type=int, default=256)
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    params = SNParams(kappa=args.kappa, dt=args.dt, t_max=args.t_max, n_grid=args.n_grid)
    res = run_sn_1d(params)

    out = out_dir / "grqm_schrodinger_newton_results_v1.json"
    out.write_text(json.dumps(res, indent=2), encoding="utf-8")

    print(json.dumps({
        "out": str(out),
        "q1_sigma_deviation_max": res["q1"]["sigma_deviation_max"],
        "q2_refinement_rel_diff": res["q2"]["refinement_rel_diff"],
        "q2_norm_drift_max": res["q2"]["norm_drift_max"],
    }, indent=2))


if __name__ == "__main__":
    main()
