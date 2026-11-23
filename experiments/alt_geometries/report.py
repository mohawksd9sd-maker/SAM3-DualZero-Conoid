#!/usr/bin/env python3
"""Write reproducibility/alt_geometries_report.json (exploratory, not core)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
for p in (HERE, ROOT / "code"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from promising_candidates import full_survey  # noqa: E402


def _to_builtin(obj):
    if isinstance(obj, dict):
        return {str(k): _to_builtin(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_builtin(v) for v in obj]
    if isinstance(obj, bool):
        return obj
    if isinstance(obj, int) and not isinstance(obj, bool):
        return int(obj)
    if isinstance(obj, float):
        return float(obj)
    if obj is None or isinstance(obj, str):
        return obj
    if hasattr(obj, "item"):
        return _to_builtin(obj.item())
    return str(obj)


def main() -> Path:
    outdir = ROOT / "reproducibility"
    outdir.mkdir(exist_ok=True)
    path = outdir / "alt_geometries_report.json"
    data = _to_builtin(full_survey())
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    print(f"wrote {path}")
    return path


if __name__ == "__main__":
    main()
