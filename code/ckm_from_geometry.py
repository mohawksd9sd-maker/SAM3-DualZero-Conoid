#!/usr/bin/env python3
"""
SAM3 — Reconstruct CKM observables from locked geometric inputs only.
No experimental retuning.

Inputs (docs/hardening/16, 08, 11):
  theta12, theta23, theta13 (locked angles)
  phi = 2*pi/5 (geometric CP)

Outputs:
  standard V_CKM, delta_CKM, Jarlskog J
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

try:
    from sam3_geometry_constants import ETA_12, ETA_13, ETA_23, PHI_CP, cabibbo_theta12_deg
except ImportError:
    ETA_12, ETA_13, ETA_23 = 0.8607, 0.5439, 0.4789
    PHI_CP = 2.0 * math.pi / 5.0

    def cabibbo_theta12_deg(eta12: float = ETA_12) -> float:
        return math.degrees(eta12 * (math.pi / 12.0))

# Locked angles (degrees) — outputs of prior geometric locks, not fits
THETA12_DEG = 12.85
THETA23_DEG = 2.36
THETA13_DEG = 0.24

# Casimir tip amplitude ratios (doc 09)
C2_OVER_C1 = 1.13
C3_OVER_C2 = 2.46


def theta13_geometric_estimate() -> dict:
    """First-principles estimate of θ13 from defect chain + hierarchy suppression.

    Cabibbo is η12 * (π/12).
    The 1–3 mixing is further suppressed by the generation-1 to generation-3
    tip-amplitude hierarchy and the residual 1–3 defect strength.

    Geometric chain (no free continuous parameter):
      θ13 ~ (η13/η12) * (c1/c3) * θ12

    where c3/c1 = (c3/c2)*(c2/c1).
    """
    theta12 = math.radians(THETA12_DEG)
    c3_over_c1 = C3_OVER_C2 * C2_OVER_C1
    ratio_eta = ETA_13 / ETA_12
    ratio_c = 1.0 / c3_over_c1  # c1/c3
    theta13_est = ratio_eta * ratio_c * theta12
    return {
        "eta13_over_eta12": ratio_eta,
        "c3_over_c1": c3_over_c1,
        "c1_over_c3": ratio_c,
        "theta13_est_deg": math.degrees(theta13_est),
        "theta13_locked_deg": THETA13_DEG,
        "abs_diff_deg": abs(math.degrees(theta13_est) - THETA13_DEG),
        "formula": "theta13 ~ (eta13/eta12)*(c1/c3)*theta12",
        "note": "Estimate from locked η and Casimir ratios; locked θ13 from full bi-unitary remains authoritative",
    }


def vckm_standard(theta12, theta23, theta13, delta) -> np.ndarray:
    """Standard PDG CKM parametrization."""
    c12, s12 = math.cos(theta12), math.sin(theta12)
    c23, s23 = math.cos(theta23), math.sin(theta23)
    c13, s13 = math.cos(theta13), math.sin(theta13)
    e_id = cmath_exp_i(delta)
    e_mid = cmath_exp_i(-delta)

    V = np.array(
        [
            [c12 * c13, s12 * c13, s13 * e_mid],
            [
                -s12 * c23 - c12 * s23 * s13 * e_id,
                c12 * c23 - s12 * s23 * s13 * e_id,
                s23 * c13,
            ],
            [
                s12 * s23 - c12 * c23 * s13 * e_id,
                -c12 * s23 - s12 * c23 * s13 * e_id,
                c23 * c13,
            ],
        ],
        dtype=complex,
    )
    return V


def cmath_exp_i(phi: float) -> complex:
    return complex(math.cos(phi), math.sin(phi))


def jarlskog(V: np.ndarray) -> float:
    """J = Im(Vud Vcs Vus* Vcd*)."""
    return float(np.imag(V[0, 0] * V[1, 1] * np.conj(V[0, 1]) * np.conj(V[1, 0])))


def delta_from_phi(phi: float = PHI_CP) -> float:
    """Map geometric φ=2π/5 into the standard CKM δ convention.

    In the model, φ is the relative C/H phase. After standard rephasing,
    the physical Dirac phase sits near 70° for φ=72° (2π/5) with the
    locked small θ13 (doc 08, 11). Leading relation used here:
      δ ≈ φ - θ13_correction ≈ φ - θ13
    with angles in radians — a geometric convention lock, not a fit.
    """
    theta13 = math.radians(THETA13_DEG)
    return phi - theta13


def main() -> None:
    t13_est = theta13_geometric_estimate()

    th12 = math.radians(THETA12_DEG)
    th23 = math.radians(THETA23_DEG)
    th13 = math.radians(THETA13_DEG)
    delta = delta_from_phi()

    V = vckm_standard(th12, th23, th13, delta)
    J = jarlskog(V)
    absV = np.abs(V)

    # Standard J formula cross-check
    J_std = (
        math.sin(2 * th12)
        * math.sin(2 * th23)
        * math.sin(2 * th13)
        * math.cos(th13)
        * math.sin(delta)
        / 8.0
    )

    out = {
        "inputs": {
            "theta12_deg": THETA12_DEG,
            "theta23_deg": THETA23_DEG,
            "theta13_deg": THETA13_DEG,
            "phi_deg": math.degrees(PHI_CP),
            "delta_CKM_deg": math.degrees(delta),
            "eta_12": ETA_12,
            "eta_13": ETA_13,
            "eta_23": ETA_23,
            "cabibbo_formula_deg": cabibbo_theta12_deg(),
        },
        "theta13_geometric_estimate": t13_est,
        "abs_V_CKM": absV.tolist(),
        "Jarlskog_J_from_V": J,
        "Jarlskog_J_standard_formula": J_std,
        "delta_CKM_deg": math.degrees(delta),
        "note": "All inputs locked geometric; no experimental retuning",
    }

    out_dir = Path(__file__).resolve().parent.parent / "pipeline_output"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "07_ckm_from_geometry.json"
    path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
