from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import run_cycle


def main() -> None:
    parser = argparse.ArgumentParser(description="Run GRQM toy model v1 and emit JSON/CSV outputs.")
    parser.add_argument(
        "--out-dir",
        default="outputs",
        help="Output directory for grqm_proxy_results_v1.json/csv (default: outputs)",
    )
    parser.add_argument("--print-json", action="store_true", help="Print full JSON results to stdout")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    results = run_cycle(out_dir)
    if args.print_json:
        print(json.dumps(results, indent=2))
    else:
        print(f"Wrote outputs to: {out_dir}")


if __name__ == "__main__":
    main()
