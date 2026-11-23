#!/usr/bin/env python3
"""Search for a unique geometric derivation of ω0 ≈ 0.927 and of the exponent 4/13.

Honesty: this script does not invent a derivation. It records every natural
dimensionless reading of the locked metric that was tried, the exponent that
would be required to hit 0.927 from (R/D)^p, and a Dual-Zero sensitivity
scan. If no unique match is found, ω0 remains a free input.
"""
from __future__ import annotations

import math
from typing import Dict

from core_geometry import (
    C0_CONVERGED,
    gaussian_curvature,
    natural_curvature_radii,
    omega0_from_radius,
)
from dual_zero_constructive import epsilon, reg2, weights


TARGET = 0.927
D_BRIDGE = 2.0 * math.pi / 12.0
C0_EXACT = 2.0 * math.pi * math.log(2.0)


def candidate_dimensionless() -> Dict[str, float]:
    """Simple closed-form numbers, plus geometric quantities from the metric.

    None of these is claimed to be a derivation of 0.927.
    """
    return {
        "C0/(2*pi)": C0_EXACT / (2.0 * math.pi),  # = ln 2
        "ln2": math.log(2.0),
        "sqrt(6/7)": math.sqrt(6.0 / 7.0),
        "13/14": 13.0 / 14.0,
        "sqrt(13/15)": math.sqrt(13.0 / 15.0),
        "14/15": 14.0 / 15.0,
        "e/3": math.e / 3.0,
        "cos(pi/7)": math.cos(math.pi / 7.0),
        "4/pi*ln2": 4.0 / math.pi * math.log(2.0),
        "2/e": 2.0 / math.e,
    }


def required_exponents(ell0: float = 1.0) -> dict:
    """If ω0 = (R/D)^{p} = 0.927, what p would each natural R require?

    p = ln(0.927) / ln(R/D). This is not a derivation of p=4/13.
    """
    data = natural_curvature_radii(ell0=ell0)
    out = {}
    for name in ("1/|K|_max", "1/sqrt(|K|_max)", "ell0", "2*ell0"):
        RD = data[name]["R_over_D"]
        p = math.log(TARGET) / math.log(RD)
        out[name] = {
            "R": data[name]["R"],
            "R_over_D": RD,
            "omega0_if_4_13": data[name]["omega0_if_4_13"],
            "p_required_for_0.927": p,
            "distance_of_p_to_4_13": p - 4.0 / 13.0,
        }
    out["required_R_for_4_13"] = data["required_for_0.927"]
    return out


def dual_zero_sensitivity(omega_values=None) -> dict:
    """How Dual-Zero weights and Reg2 scale with ω0.

    Because ε(n)=ω0 (−1)^n n^{-n} is linear in ω0, sums of |ε| and the
    Reg2 pairing of the absolute weights scale exactly linearly. This is
    recorded, not hidden. No nonlinear downstream geometric observable
    depending on ω0 was found in the core (CKM/η scripts do not take ω0
    as a derived input).
    """
    if omega_values is None:
        omega_values = (0.80, 0.90, 0.927, 0.95, 1.00, 1.22, 1.51)
    rows = []
    for w in omega_values:
        s = sum(weights(20, omega0=w))
        r = reg2(weights(20, omega0=w))
        rows.append({
            "omega0": w,
            "sum_abs_eps_nle20": s,
            "reg2_first": r[0] if r else None,
            "sum_over_0.927": s / sum(weights(20, omega0=TARGET)),
        })
    return {"rows": rows, "linearity": "sum|ε| and Reg2(|ε|) scale exactly as ω0"}


def report() -> dict:
    cands = candidate_dimensionless()
    nearest = min(cands.items(), key=lambda kv: abs(kv[1] - TARGET))
    return {
        "target": TARGET,
        "candidates": cands,
        "nearest_simple_constant": {"name": nearest[0], "value": nearest[1], "delta": nearest[1] - TARGET},
        "exponents": required_exponents(),
        "sensitivity": dual_zero_sensitivity(),
        "conclusion": (
            "No unique geometric definition of R_curv, and no derivation of "
            "the exponent 4/13, was found. The closest simple constants "
            "(sqrt(6/7)≈0.9258, 13/14≈0.9286) are numerical coincidences, "
            "not derivations. ω0 remains a free input."
        ),
    }


def main() -> None:
    import json
    from pathlib import Path
    r = report()
    print("ω0 search")
    print(" nearest simple constant:", r["nearest_simple_constant"])
    print(" exponents p required for 0.927:")
    for k, v in r["exponents"].items():
        if k == "required_R_for_4_13":
            print(f"  {k}: {v}")
        else:
            print(f"  {k}: p={v['p_required_for_0.927']:.4f}  (4/13={4/13:.4f})  ω0(4/13)={v['omega0_if_4_13']:.4f}")
    print(" sensitivity: |ε| sums scale linearly with ω0")
    print(" conclusion:", r["conclusion"])
    out = Path(__file__).resolve().parent.parent / "reproducibility" / "omega0_search.json"
    out.write_text(json.dumps(r, indent=2), encoding="utf-8")
    print("Wrote", out)


if __name__ == "__main__":
    main()
