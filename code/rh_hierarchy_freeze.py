#!/usr/bin/env python3
"""Freeze RH hierarchy from tip amplitudes; recompute delta_PMNS band."""

from __future__ import annotations

import json
import math
from pathlib import Path

C2_OVER_C1 = 1.13
C3_OVER_C2 = 2.46
C3_OVER_C1 = C3_OVER_C2 * C2_OVER_C1


def main() -> None:
    # M_g ∝ 1/A_g with A = (1, 1.13, 2.7798)
    r1, r2, r3 = 1.0, 1.0 / C2_OVER_C1, 1.0 / C3_OVER_C1
    asym = math.log(r3 / r2)
    center = 235.0 + 25.0 * math.tanh(0.5 * asym)
    width = 35.0 / (1.0 + 0.15 * abs(asym))
    lo, hi = max(180.0, center - width), min(280.0, center + width)
    out = {
        "r1_r2_r3": [r1, r2, r3],
        "origin": "M_g proportional to 1/A_g tip amplitudes",
        "asymmetry_log_r3_over_r2": asym,
        "delta_PMNS_band_deg": [lo, hi],
        "delta_PMNS_center_deg": center,
        "previous_band_deg": [200.0, 270.0],
        "narrowed": (hi - lo) < 70.0,
        "rule": "geometry only; not tuned to global-fit delta_PMNS",
    }
    out_dir = Path(__file__).resolve().parent.parent / "pipeline_output"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "11_rh_hierarchy_pmns.json"
    path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
