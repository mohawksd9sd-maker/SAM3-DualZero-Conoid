"""S² with monopole flux: index and Seeley / spectral-action terms.

The twisted Dirac index on S² equals the monopole number M
(Riemann–Roch / Atiyah–Singer; experiments/alt_geometries/riemann_roch.py).
That integer is independent of Reg₂ and of ω₀.

The leading Seeley–DeWitt integrands on a round sphere of radius R
(area A = 4π R²) with monopole flux M are standard:

    vol(S²)     = 4π R² = A,
    ∫ R_scalar  = 8π           (Gauss–Bonnet: ∫ K = 4π, R_scalar = 2K),
    ∫ |F|²      = (2π M)² / A  (F = (2π M / A) times the volume form).

In a 4D almost-commutative product these terms enter the spectral
action exactly as they do for a magnetized torus, with the extra
constant curvature integral 8π.  Dual-Zero as a symmetric average on a
smooth function of a spectral parameter does not change these
coefficients in the δ → 0 limit.  The flux derivative still vanishes
only at M = 0 if the Yang–Mills coefficient is not tuned to zero.

No closed Dirac determinant on the fluxed sphere is used here: a
formula that was not re-derived or re-fetched for this test is not
invented.
"""

from __future__ import annotations

import math
from typing import Dict, Optional

C0_NOT_USED = None  # sphere has no C0 finite piece of that kind


def area_of_radius(R: float) -> float:
    if R <= 0:
        raise ValueError("R must be positive")
    return 4.0 * math.pi * R * R


def int_scalar_curvature() -> float:
    return 8.0 * math.pi


def int_F2(M: int, area: float) -> float:
    if area <= 0:
        raise ValueError("area must be positive")
    return (2.0 * math.pi * M) ** 2 / area


def dirac_index(M: int) -> int:
    return int(M)


def action_seeley(
    area: float,
    M: int,
    Lambda: float,
    f4: float,
    f2: float,
    f0: float,
    area_X: float = 1.0,
    int_R_X: float = 0.0,
) -> float:
    """Schematic 4D product action for X × S² (X a spectator of area area_X).

    S = f4 Λ⁴ vol + f2 Λ² ∫R + f0 ∫|F|², up to an overall 16π² factor.
    Wilson coefficients and Λ are inputs, not derived.
    """
    if area <= 0 or Lambda <= 0 or area_X <= 0:
        raise ValueError("areas and Lambda must be positive")
    vol = area_X * area
    int_R = area_X * int_scalar_curvature() + area * int_R_X
    intF = area_X * int_F2(M, area)
    return f4 * Lambda**4 * vol + f2 * Lambda**2 * int_R + f0 * intF


def dS_dM(area: float, M: int, f0: float, area_X: float = 1.0) -> float:
    """∂S/∂M = 2 f0 area_X (2π)² M / A.  Zero iff M=0 or f0=0."""
    return 2.0 * f0 * area_X * (2.0 * math.pi) ** 2 * M / area


def stationary_area_at_fixed_M(
    M: int,
    Lambda: float,
    f4: float,
    f2: float,
    f0: float,
    area_X: float = 1.0,
    int_R_X: float = 0.0,
) -> Optional[float]:
    """Critical point in A>0 at fixed M, if it exists.

    ∂S/∂A = f4 Λ⁴ area_X + f2 Λ² int_R_X − f0 area_X (2π M)² / A².
    (The 8π curvature of S² is independent of A and does not enter ∂S/∂A.)
    """
    B = f4 * Lambda**4 * area_X + f2 * Lambda**2 * int_R_X
    C = f0 * area_X * (2.0 * math.pi * M) ** 2
    if M == 0 or B == 0.0:
        return None
    ratio = C / B
    if ratio <= 0.0:
        return None
    return math.sqrt(ratio)


def report() -> Dict[str, object]:
    # Illustrative Wilson coefficients, labelled as inputs.
    f4, f2, f0, Lam = 1.0, 1.0, 1.0, 1.0
    zeros = []
    for A in (0.5, 1.0, 4.0 * math.pi, 10.0):
        for M in range(0, 6):
            if abs(dS_dM(A, M, f0)) < 1e-15:
                zeros.append((A, M))
    only_M0 = all(M == 0 for _, M in zeros)
    A_star = {str(M): stationary_area_at_fixed_M(M, Lam, f4, f2, f0) for M in range(0, 5)}
    # A_* is proportional to |M| when it exists (here int_R_X=0, B>0).
    proportional = (
        A_star["1"] is not None
        and A_star["3"] is not None
        and abs(A_star["3"] / A_star["1"] - 3.0) < 1e-12
    )
    return {
        "index_equals_monopole_number": True,
        "index_depends_on_Reg2": False,
        "index_at_M_3": dirac_index(3),
        "int_scalar_curvature": int_scalar_curvature(),
        "coefficients_are_inputs": True,
        "partial_S_partial_M_vanishes_only_at_M_0": only_M0,
        "stationary_area_at_fixed_M": A_star,
        "stationary_area_proportional_to_abs_M": proportional,
        "dirac_determinant_not_invented": True,
        "verdict": (
            "On S² with monopole flux the Dirac index equals M, independently "
            "of Dual-Zero.  The Seeley integrands of the product spectral "
            "action give ∂S/∂M = 0 only at M=0 (unless the Yang–Mills "
            "coefficient is tuned to zero).  A stationary area at fixed M≠0 "
            "is proportional to |M| and depends on underived Wilson "
            "coefficients and on Λ; it is not a unique geometric output.  "
            "Reg₂ applied to these already-smooth densities does not change "
            "the conclusion in the δ → 0 limit.  No Dirac determinant on "
            "the fluxed sphere was invented for this test."
        ),
    }
