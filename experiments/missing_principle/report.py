#!/usr/bin/env python3
"""Write reproducibility/missing_principle_report.json (exploratory, not core)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from c4_equivariant import report as c4_report  # noqa: E402
from kronecker_det import report as kronecker_report  # noqa: E402
from magnetized_det import report as magnetized_report  # noqa: E402
from z4_orbifold import report as z4_report  # noqa: E402


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


def full_survey() -> dict:
    return {
        "exploratory": True,
        "locked_core_untouched": True,
        "kronecker_det_flat_torus": kronecker_report(),
        "magnetized_dirac_det": magnetized_report(),
        "z4_orbifold_zero_modes": z4_report(),
        "c4_equivariant_conoid_index": c4_report(),
        "verdict_headline": (
            "No mechanism tested here derives the flux M=3 uniquely, or "
            "fixes the surface area.  Two genuine (and mutually conflicting) "
            "mechanisms can fix the complex structure of a flat torus: "
            "maximizing det'Δ selects the hexagonal modulus; requiring a C4 "
            "isometry compatible with the conoid selects the square modulus.  "
            "The Z4 orbifold produces a 3-dimensional invariant sector only "
            "after a choice of flux in a range, and the C4-equivariant index "
            "of the conoid vanishes in every sector."
        ),
    }


def main() -> None:
    out = ROOT / "reproducibility" / "missing_principle_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    data = _to_builtin(full_survey())
    out.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    print(f"wrote {out}")
    print(data["verdict_headline"])


if __name__ == "__main__":
    main()
