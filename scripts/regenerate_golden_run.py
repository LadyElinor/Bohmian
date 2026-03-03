from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from grqm.core import run_cycle


def main() -> None:
    out_dir = ROOT / "notebooks" / "outputs" / "golden_run_20260302"
    if out_dir.exists():
        for p in out_dir.glob("*"):
            if p.is_file():
                p.unlink()
            else:
                shutil.rmtree(p)
    out_dir.mkdir(parents=True, exist_ok=True)
    run_cycle(out_dir)
    readme = out_dir / "README.md"
    readme.write_text(
        "# Golden run (v1)\n\n"
        "Regenerate with:\n\n"
        "```\npython scripts/regenerate_golden_run.py\n```\n",
        encoding="utf-8",
    )
    print(f"Regenerated golden run at: {out_dir}")


if __name__ == "__main__":
    main()
