"""
SAM3 pure-geometry constants (single source of truth).

All defaults match docs/hardening/16 and 18.
omega0 is geometric ≈ 0.927 — never the older free default ≈ 0.97.
"""

from __future__ import annotations

import math
from typing import Dict

N_BRIDGES: int = 12
DELTA_THETA: float = 2.0 * math.pi / N_BRIDGES  # π/6

# Geometric Dual-Zero strength: (R_curv / D_bridge)^(4/13)
# Locked value from conoid curvature / bridge spacing (doc 18).
OMEGA0_GEOMETRIC: float = 0.927

# Representation-theoretic Casimirs on generation module (doc 09)
C_G: Dict[int, float] = {1: 6.0 / 5.0, 2: 1.0, 3: 4.0 / 5.0}

# Continuum defect overlaps (locked numerical continuum integrals)
ETA_12: float = 0.8607
ETA_13: float = 0.5439
ETA_23: float = 0.4789

# Intertwiner norm (doc 14)
KAPPA_U_OVER_KAPPA_D: float = 0.5

# CP phase from E3 + I^2 = -1 + tip orientation (doc 08)
PHI_CP: float = 2.0 * math.pi / 5.0

# G_N prefactor structure (docs 13, 20)
def G_N_over_ell0_sq() -> float:
    return 64.0 * math.pi / 45.0


def omega0_from_geometry(R_curv: float, D_bridge: float) -> float:
    """Canonical geometric formula. Use OMEGA0_GEOMETRIC for the locked number."""
    if D_bridge <= 0:
        raise ValueError("D_bridge must be positive")
    return (R_curv / D_bridge) ** (4.0 / 13.0)


def cabibbo_theta12_rad(eta12: float = ETA_12) -> float:
    """θ12 ≈ η12 × (π/12) = η12 × Δθ/2 relative to bridge spacing convention in locks."""
    return eta12 * (math.pi / 12.0)


def cabibbo_theta12_deg(eta12: float = ETA_12) -> float:
    return math.degrees(cabibbo_theta12_rad(eta12))


def frozen_geometry_dict() -> dict:
    return {
        "n_bridges": N_BRIDGES,
        "delta_theta": DELTA_THETA,
        "omega0_geometric": OMEGA0_GEOMETRIC,
        "C_1": C_G[1],
        "C_2": C_G[2],
        "C_3": C_G[3],
        "eta_12": ETA_12,
        "eta_13": ETA_13,
        "eta_23": ETA_23,
        "kappa_u_over_kappa_d": KAPPA_U_OVER_KAPPA_D,
        "phi_CP": PHI_CP,
        "phi_CP_deg": math.degrees(PHI_CP),
        "G_N_over_ell0_sq": G_N_over_ell0_sq(),
        "theta12_from_eta_deg": cabibbo_theta12_deg(),
        "note": "omega0 must remain 0.927 geometric; do not use legacy 0.97 defaults",
    }
