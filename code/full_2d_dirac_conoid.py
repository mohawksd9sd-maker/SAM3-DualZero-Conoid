"""
SAM3 — 2D Dirac prototype on the right conoid

STATUS: PROTOTYPE (not production APS eigensolver).
See docs/hardening/23_Numerical_Production_Readiness.md for the production roadmap.

- Uses geometric defaults from sam3_geometry_constants (omega0 = 0.927).
- Does NOT inject artificial exact zeros; spectrum is whatever the discretisation produces.
- Gap → 0 and residual < 1e-3 claims are locked in docs/hardening/10, not guaranteed by this script alone.
"""

from __future__ import annotations

import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh

try:
    from sam3_geometry_constants import N_BRIDGES, OMEGA0_GEOMETRIC
except ImportError:
    N_BRIDGES = 12
    OMEGA0_GEOMETRIC = 0.927


def conoid_dirac_2d(
    Nu: int = 60,
    Nv: int = 90,
    l0: float = 1.0,
    k_max: int = 12,
    omega0: float = OMEGA0_GEOMETRIC,
):
    """Prototype radial-sector Dirac on the right-conoid metric.

    Parameters
    ----------
    omega0 : float
        Dual-Zero strength. Default is the locked geometric value 0.927.
        Legacy defaults near 0.97 must not be used.
    """
    if abs(omega0 - OMEGA0_GEOMETRIC) > 0.02:
        # Soft guard: allow tiny numeric drift, block old 0.97-era defaults
        raise ValueError(
            f"omega0={omega0} is outside the geometric lock band around {OMEGA0_GEOMETRIC}. "
            "See docs/hardening/18_DualZero_Definition_Lock.md"
        )

    u = np.linspace(-6.0, 6.0, Nu)
    v = np.linspace(0.0, 2.0 * np.pi, Nv, endpoint=False)
    du = u[1] - u[0]

    g_vv = u[:, None] ** 2 + 4.0 * l0**2 * np.cos(2.0 * v[None, :]) ** 2

    # Simple radial spin-connection proxy (prototype)
    spin_conn = u / (2.0 * np.sqrt(u**2 + 4.0 * l0**2 + 1e-15))

    evals = []
    # Angular sectors related to 12-bridge structure
    half = N_BRIDGES // 2
    for m in range(-half, half + 1):
        angular_term = m / (np.mean(np.sqrt(g_vv), axis=1) + 1e-15)
        diag = spin_conn + angular_term
        # Mild Dual-Zero-inspired diagonal regulation (prototype scale)
        diag = diag + omega0 * 1e-6 * np.sin(np.arange(Nu))
        D_rad = diags(
            [diag, np.ones(Nu - 1) / (2.0 * du), -np.ones(Nu - 1) / (2.0 * du)],
            [0, 1, -1],
            shape=(Nu, Nu),
        )
        try:
            e, _ = eigsh(D_rad.tocsr().astype(float), k=min(2, Nu - 2), which="SM", tol=1e-6)
            evals.extend(np.real(e))
        except Exception:
            continue

    if not evals:
        return np.array([])

    evals = np.sort(np.asarray(evals, dtype=float))
    # Do not force artificial zeros — continuum zero modes are a limit statement (doc 10)
    return evals[:k_max]


if __name__ == "__main__":
    ev = conoid_dirac_2d()
    print("Prototype 2D Dirac eigenvalues (l0=1, omega0 geometric):")
    print(ev)
    print(f"|lambda|_min = {np.min(np.abs(ev)) if ev.size else None}")
    print("NOTE: prototype only — see docs/hardening/23_Numerical_Production_Readiness.md")
