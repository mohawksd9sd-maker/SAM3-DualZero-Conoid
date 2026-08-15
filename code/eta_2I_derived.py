#!/usr/bin/env python3
"""Derived 2I radial eta_ij with k_g = A_g^{phi^2}. Locked continuum eta not overwritten."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

PHI = (1.0 + math.sqrt(5.0)) / 2.0
MU = PHI**2
A = np.array([1.0, 1.13, 2.7798])
LOCKED = np.array([0.8607, 0.5439, 0.4789])


def eta_from_k(k: np.ndarray) -> np.ndarray:
    e = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            e[i, j] = 2.0 * math.sqrt(k[i] * k[j]) / (k[i] + k[j])
    return e


def main() -> None:
    k = A**MU
    eta = eta_from_k(k)
    derived = np.array([eta[0, 1], eta[0, 2], eta[1, 2]])
    res = np.abs(derived - LOCKED)
    out = {
        "A_tip": A.tolist(),
        "mu_phi_squared": MU,
        "k_g": k.tolist(),
        "eta_matrix": eta.tolist(),
        "eta_12_13_23_derived": derived.tolist(),
        "eta_12_13_23_locked_continuum": LOCKED.tolist(),
        "residuals": res.tolist(),
        "rms_residual": float(math.sqrt(np.mean(res**2))),
        "policy": "locked continuum defect eta remain CKM inputs; derived is 2I prediction",
        "formula": "eta_ij = 2*sqrt(k_i*k_j)/(k_i+k_j), k=A^{phi^2}",
    }
    out_dir = Path(__file__).resolve().parent.parent / "pipeline_output"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "10_eta_2I_derived.json"
    path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
