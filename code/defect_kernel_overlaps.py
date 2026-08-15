#!/usr/bin/env python3
"""Diagnostic: shared tip defect + radial profiles (not a lock overwrite)."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from numpy.linalg import norm

PHI = (1.0 + math.sqrt(5.0)) / 2.0
A = np.array([1.0, 1.13, 2.7798])
K = A ** (PHI**2)
LOCKED = [0.8607, 0.5439, 0.4789]


def main() -> None:
    Nu, Nv = 120, 96
    u = np.linspace(0.0, 10.0, Nu)
    v = np.linspace(0.0, 2.0 * math.pi, Nv, endpoint=False)
    rad = np.zeros((3, Nu))
    for i in range(3):
        rad[i] = np.exp(-K[i] * u)
        rad[i] /= math.sqrt(np.sum(rad[i] ** 2) * (u[1] - u[0]) + 1e-30)
    # Shared angular defect from curvature
    c2 = np.cos(2.0 * v) ** 2 + 0.05
    eta = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            Wi = rad[i][:, None] * c2[None, :]
            Wj = rad[j][:, None] * c2[None, :]
            Wi = Wi / (norm(Wi) + 1e-30)
            Wj = Wj / (norm(Wj) + 1e-30)
            eta[i, j] = float(np.sum(Wi * Wj))
    for i in range(3):
        s = math.sqrt(abs(eta[i, i]) + 1e-30)
        eta[i, :] /= s
        eta[:, i] /= s
        eta[i, i] = 1.0
    derived = [float(eta[0, 1]), float(eta[0, 2]), float(eta[1, 2])]
    out = {
        "eta_shared_tip_radial": derived,
        "locked_continuum": LOCKED,
        "note": "diagnostic only; matches pure radial 2I law when angular is shared",
        "k_g": K.tolist(),
    }
    out_dir = Path(__file__).resolve().parent.parent / "pipeline_output"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "12_defect_kernel_diagnostic.json"
    path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
