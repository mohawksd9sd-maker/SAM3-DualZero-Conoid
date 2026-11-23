#!/usr/bin/env python3
"""Write reproducibility/further_candidates_report.json (exploratory, not core)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from coincidences import report as coincidence_report  # noqa: E402
from euler_orbifolds import report as euler_report  # noqa: E402
from spectral_action_moduli import report as spectral_report  # noqa: E402
from tadpole_enum import report as tadpole_report  # noqa: E402
from zn_orbifolds import report as zn_report  # noqa: E402


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
        "euler_orbifolds": euler_report(),
        "zn_orbifolds": zn_report(),
        "tadpoles": tadpole_report(),
        "spectral_action_moduli": spectral_report(),
        "coincidences": coincidence_report(),
        "verdict_headline": (
            "No accidental fit: nothing tested here derives three generations, "
            "or a unique flux M=3, or a unique area, without a parameter or a "
            "construction being chosen to that end.  Standard abelian T^6 "
            "orbifolds in the Reffert table never have |chi|/2=3 (the smallest "
            "value is 24; C4-compatible ones give 24, 60 or 90).  Magnetized "
            "T^2/Z_N counts give a 3-dimensional invariant sector only after "
            "choosing a flux in a range.  Tadpole equations do not force 3.  "
            "The product spectral action, including the tip, has no interior "
            "extremum at M=3.  Numerical proximities to the quoted ω0 or to "
            "4/13 are coincidences, with a look-elsewhere count."
        ),
    }


def main() -> None:
    out = ROOT / "reproducibility" / "further_candidates_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    data = _to_builtin(full_survey())
    out.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    print(f"wrote {out}")
    print(data["verdict_headline"])


if __name__ == "__main__":
    main()
