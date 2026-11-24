"""Numbers quoted in doc 64 (run: python report_64.py, ~5 s)."""

from __future__ import annotations

import json
from pathlib import Path

import flavor_cube as fc


def main() -> Path:
    out = fc.report()
    path = Path(__file__).with_name("results_doc64.json")
    path.write_text(json.dumps(out, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o)))
    return path


if __name__ == "__main__":
    print(main())
