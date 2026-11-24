"""Numbers quoted in doc 63 (run: python report_63.py, ~15 s)."""

from __future__ import annotations

import json
from pathlib import Path

import vl_principles as vp


def main() -> Path:
    out = vp.report()
    path = Path(__file__).with_name("results_doc63.json")
    path.write_text(json.dumps(out, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o)))
    return path


if __name__ == "__main__":
    print(main())
