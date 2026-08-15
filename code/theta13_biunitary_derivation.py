#!/usr/bin/env python3
"""Full singular-vector derivation of CKM angles — derivation only."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from numpy.linalg import svd

ETA12 = 0.8607
C2_OVER_C1 = 1.13
C3_OVER_C2 = 2.46
C3_OVER_C1 = C3_OVER_C2 * C2_OVER_C1
KAPPA = 0.5
PHI = 2.0 * math.pi / 5.0
TH23 = math.radians(2.36)


def givens(i: int, j: int, theta: float, n: int = 3) -> np.ndarray:
    R = np.eye(n, dtype=float)
    c, s = math.cos(theta), math.sin(theta)
    R[i, i] = R[j, j] = c
    R[i, j] = s
    R[j, i] = -s
    return R


def pdg_angles(V: np.ndarray) -> dict:
    absV = np.abs(V)
    s13 = min(float(absV[0, 2]), 1.0)
    c13 = math.sqrt(max(1.0 - s13**2, 0.0))
    s12 = min(float(absV[0, 1]) / (c13 + 1e-15), 1.0)
    s23 = min(float(absV[1, 2]) / (c13 + 1e-15), 1.0)
    return {
        "theta12_deg": math.degrees(math.asin(s12)),
        "theta23_deg": math.degrees(math.asin(s23)),
        "theta13_deg": math.degrees(math.asin(s13)),
        "Vus": float(absV[0, 1]),
        "Vub": float(absV[0, 2]),
        "Vcb": float(absV[1, 2]),
    }


def main() -> None:
    th12 = ETA12 * (math.pi / 12.0)
    A = np.array([1.0, C2_OVER_C1, C3_OVER_C1])
    yd = A / A[2]
    yu = yd.copy()
    yu[0] *= KAPPA
    yu = yu / yu[2]

    OLd = givens(0, 1, th12) @ givens(1, 2, TH23)
    Yd = OLd @ np.diag(yd)
    Yu = np.diag(yu)

    Ud, sd, _ = svd(Yd)
    Uu, su, _ = svd(Yu)
    od, ou = np.argsort(sd), np.argsort(su)
    V = Uu[:, ou].T.conj() @ Ud[:, od]
    ang = pdg_angles(V)

    th13_phys = th12 * TH23 * (yd[0] / yd[2])
    delta = PHI - th13_phys
    J = (
        0.125
        * math.sin(2 * th12)
        * math.sin(2 * TH23)
        * math.sin(2 * th13_phys)
        * math.cos(th13_phys)
        * math.sin(delta)
    )

    out = {
        "svd_angles_deg": ang,
        "theta13_phys_deg": math.degrees(th13_phys),
        "theta13_archive_deg": 0.24,
        "delta_CKM_deg": math.degrees(delta),
        "Jarlskog_J": J,
        "yd": yd.tolist(),
        "yu": yu.tolist(),
        "formula": "theta13_phys = theta12 * theta23 * (y1/y3)",
        "rule": "derivation only; archive theta13=0.24 not overwritten",
    }
    out_dir = Path(__file__).resolve().parent.parent / "pipeline_output"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "09_theta13_biunitary.json"
    path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
