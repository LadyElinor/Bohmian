"""Compatibility wrapper for legacy notebook/script imports.

Core implementation now lives in `src/grqm/core.py`.
This file preserves old import paths used by existing cycle scripts.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from grqm.core import (  # noqa: E402
    IC,
    Params,
    RunConfig,
    integrate,
    interp_to_grid,
    l2_rel_err,
    run_cycle,
)


if __name__ == "__main__":
    out = ROOT / "outputs"
    results = run_cycle(out)
    import json

    print(json.dumps(results, indent=2))
