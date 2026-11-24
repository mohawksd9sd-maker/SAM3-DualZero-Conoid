"""Numbers quoted in doc 62 (run: python report_62.py, ~10 s)."""

from __future__ import annotations

import json
from pathlib import Path

import lattice_geometries as lg


def main() -> Path:
    out = lg.report()
    path = Path(__file__).with_name("results_doc62.json")
    path.write_text(json.dumps(out, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o)))
    return path


if __name__ == "__main__":
    print(main())
