#!/usr/bin/env python3
"""Write reproducibility/ps_conoid_product_report.json (exploratory, not core)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
for p in (HERE, ROOT / "code", ROOT / "experiments" / "alt_geometries"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from geometry import report as geometry_report  # noqa: E402
from flux_mechanisms import report as flux_report  # noqa: E402
from rge_pipeline import report as rge_report  # noqa: E402
from yukawa_fit import report as yukawa_report  # noqa: E402
from higgs_sigma import report as higgs_report  # noqa: E402


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
        "geometry": geometry_report(),
        "flux_mechanisms": flux_report(),
        "rge": rge_report(),
        "yukawas": yukawa_report(),
        "higgs_sigma": higgs_report(),
        "verdict_headline": (
            "The product Y × F_PS with Y = (truncated conoid) × Σ is a "
            "consistent 4D, KO-dimension-2 almost-commutative geometry.  "
            "The Pati-Salam gauge relations at Λ are derived (spectator).  "
            "Nothing in the combined geometry fixes flux = 3 or the moduli "
            "of Σ.  The one-loop (and partial two-loop) RG pipeline "
            "determines (m_R, Λ) from measured couplings; it does not "
            "predict those couplings.  Yukawa moduli are not uniquely "
            "fixed; a labelled fit is underdetermined.  The Higgs mass is "
            "not a unique prediction of the product."
        ),
    }


def main() -> Path:
    outdir = ROOT / "reproducibility"
    outdir.mkdir(exist_ok=True)
    path = outdir / "ps_conoid_product_report.json"
    path.write_text(json.dumps(_to_builtin(full_survey()), indent=2, sort_keys=True) + "\n")
    print(f"wrote {path}")
    return path


if __name__ == "__main__":
    main()
