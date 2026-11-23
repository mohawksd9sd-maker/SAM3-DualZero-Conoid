"""Truncated spectral-action densities on conoid × magnetized T^2, including the tip.

Exploratory: not part of the locked SAM-3 core.

The 4D product Y = X_{a,b} × T^2 of area A, with a flux M on the torus, has
(doc 48, geometry.py):

    vol(Y)        = Area(X) · A,
    ∫_Y R         = A · ∫_X R_X   (T^2 is flat),
    ∫_Y |F|^2     = Area(X) · (2π M)^2 / A,
    Area(X_{a,b}) = π(b² − a²) + finite piece  (→ π b² + C0 + o(1) as
                    a→0, b→∞, on the unit metric, with C0 = 2π ln 2),
    ∫_X R_X       → −4π            (because R_X = 2K and ∫K → −2π).

The tip of the complete conoid is a geodesic boundary of length 8ℓ_0
(doc 46).  The outer cutoff is a second boundary.  The leading boundary
Seeley term is proportional to the volume of the boundary,
    vol(∂Y) = (L_tip + L_outer) · A.
For a geodesic inner boundary the geodesic curvature vanishes, so there
is no additional k_g correction at that order (doc 46).  The four tip
nodes are metric-degeneracy points; no additional index or Seeley
contribution from the nodes is assumed or invented here.

The spectral action is a linear combination of these terms, with Wilson
coefficients f4, f2, f0, f_{1/2} and a cutoff scale Λ that are *not
derived from the conoid*.  This module studies two functionals, with
those coefficients left as explicit inputs:

  (i)  the cutoff-dependent action at finite outer radius b, tip taken
       at a=0, L_tip=8, L_outer the length of the outer u=b circle
       averaged in the obvious way (leading length 2π b, plus a
       correction we do not need for the sign analysis);
  (ii) the finite-part action, dropping every term that diverges as
       π b² when b→∞.

A stationary point in (A, M) is reported only when it occurs for a
reason that does not put 3, or a preferred area, in by hand.  τ does
not enter these coefficients: the fluxed Dirac spectrum on T^2 is
independent of τ (docs 48–49).
"""

from __future__ import annotations

import math
from typing import Dict, Optional, Tuple

C0 = 2.0 * math.pi * math.log(2.0)
INT_R_COMPLETE = -4.0 * math.pi  # ∫_X 2K dA
TIP_LENGTH_UNIT = 8.0


def area_leading(b: float, a: float = 0.0) -> float:
    """π(b² − a²), the divergent/leading piece of Area(X).  C0 is added separately."""
    if b <= a:
        raise ValueError("need b > a")
    return math.pi * (b * b - a * a)


def action_truncated(
    A: float,
    M: int,
    b: float,
    Lambda: float,
    f4: float,
    f2: float,
    f0: float,
    f_bdry: float,
    a: float = 0.0,
    include_leading_area: bool = True,
    L_outer: Optional[float] = None,
) -> float:
    """Schematic spectral action (up to an overall 16π² normalisation).

    S = f4 Λ^4 vol(Y) + f2 Λ^2 ∫R + f0 ∫|F|^2 + f_bdry Λ^3 vol(∂Y).
    If include_leading_area is False, Area(X) is replaced by C0 only
    (the finite-part functional).
    """
    if A <= 0 or Lambda <= 0 or b <= 0:
        raise ValueError("A, Lambda, b must be positive")
    area_X = (area_leading(b, a) + C0) if include_leading_area else C0
    L_out = 2.0 * math.pi * b if L_outer is None else L_outer
    L = (TIP_LENGTH_UNIT if a == 0.0 else 0.0) + (L_out if include_leading_area else TIP_LENGTH_UNIT)
    # For the finite-part functional the outer boundary is a cutoff artefact
    # and is dropped; the tip length remains.
    if not include_leading_area:
        L = TIP_LENGTH_UNIT
    vol = area_X * A
    int_R = INT_R_COMPLETE * A
    int_F2 = area_X * (2.0 * math.pi * M) ** 2 / A
    vol_bdry = L * A
    return (
        f4 * Lambda**4 * vol
        + f2 * Lambda**2 * int_R
        + f0 * int_F2
        + f_bdry * Lambda**3 * vol_bdry
    )


def dS_dM_sign_term(A: float, M: int, area_X: float, f0: float) -> float:
    """∂S/∂M = 2 f0 area_X (2π)^2 M / A.  Vanishes iff M=0 or f0=0."""
    return 2.0 * f0 * area_X * (2.0 * math.pi) ** 2 * M / A


def stationary_A_at_fixed_M(
    M: int,
    Lambda: float,
    f4: float,
    f2: float,
    f0: float,
    f_bdry: float,
    area_X: float,
    L: float,
) -> Optional[float]:
    """Critical point of S in A>0 at fixed M, if it exists and the second
    derivative has the sign of a minimum or maximum.

    ∂S/∂A = f4 Λ^4 area_X + f2 Λ^2 ∫R/A-coefficient + f_bdry Λ^3 L
            − f0 area_X (2π M)^2 / A^2.
    The first three terms are independent of A; call them B.
    ∂S/∂A = B − C / A^2 with C = f0 area_X (2π M)^2.
    A critical point requires B and C of the same sign: A^2 = C/B.
    """
    B = f4 * Lambda**4 * area_X + f2 * Lambda**2 * INT_R_COMPLETE + f_bdry * Lambda**3 * L
    C = f0 * area_X * (2.0 * math.pi * M) ** 2
    if M == 0:
        return None  # S is linear in A; either no critical point or a flat direction
    if B == 0.0:
        return None
    ratio = C / B
    if ratio <= 0.0:
        return None
    return math.sqrt(ratio)


def scan_no_interior_M_extremum(
    A_values=(0.5, 1.0, 2.0, 10.0),
    M_values=range(0, 6),
    b: float = 10.0,
    Lambda: float = 1.0,
    coeffs: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0),
) -> Dict[str, object]:
    f4, f2, f0, f_bdry = coeffs
    # ∂S/∂M vanishes only at M=0, for any A, if f0≠0.
    zeros = []
    for A in A_values:
        for M in M_values:
            area_X = area_leading(b) + C0
            deriv = dS_dM_sign_term(A, M, area_X, f0)
            if abs(deriv) < 1e-15:
                zeros.append((A, M))
    only_M0 = all(M == 0 for _, M in zeros) and len(zeros) == len(A_values)
    return {
        "partial_M_vanishes_only_at_M_0": only_M0,
        "vanishing_points": zeros,
    }


def report() -> Dict[str, object]:
    # Representative coefficients, labelled as an extra assumption, not derived.
    coeffs = {"f4": 1.0, "f2": 1.0, "f0": 1.0, "f_bdry": 1.0, "Lambda": 1.0}
    f4, f2, f0, f_bdry, Lam = 1.0, 1.0, 1.0, 1.0, 1.0
    # Finite-part stationary A at M=1,2,3 (if any), under this coefficient choice.
    fin_A = {}
    for M in (0, 1, 2, 3, 4):
        A_star = stationary_A_at_fixed_M(M, Lam, f4, f2, f0, f_bdry, C0, TIP_LENGTH_UNIT)
        fin_A[str(M)] = A_star
    # Leading (divergent) functional at a large cutoff b.
    b = 100.0
    lead_A = {}
    for M in (0, 1, 2, 3, 4):
        lead_A[str(M)] = stationary_A_at_fixed_M(
            M, Lam, f4, f2, f0, f_bdry, area_leading(b) + C0, TIP_LENGTH_UNIT + 2 * math.pi * b
        )
    # Does any of these preferred A values come out independently of M?  No:
    # A_star is proportional to |M| when it exists.
    # Is there an M that is preferred?  Only M=0 for ∂S/∂M.
    scan = scan_no_interior_M_extremum()
    # Linear-in-A coefficient of the finite-part action at M=0 (the
    # would-be condition for a flat direction in A).
    B_finite_M0 = f4 * Lam**4 * C0 + f2 * Lam**2 * INT_R_COMPLETE + f_bdry * Lam**3 * TIP_LENGTH_UNIT
    return {
        "coefficients_are_inputs": True,
        "coefficients_used_for_illustration": coeffs,
        "tau_enters_these_terms": False,
        "partial_S_partial_M_vanishes_only_at_M_0": scan["partial_M_vanishes_only_at_M_0"],
        "finite_part_stationary_A_at_fixed_M": fin_A,
        "truncated_b_100_stationary_A_at_fixed_M": lead_A,
        "finite_part_linear_A_coefficient_at_M_0": B_finite_M0,
        "flat_direction_in_A_at_M_0": abs(B_finite_M0) < 1e-15,
        "verdict": (
            "The flux derivative of the spectral action (truncated or "
            "finite-part) vanishes only at M=0, for any positive area, as "
            "long as the Yang-Mills coefficient is not tuned to zero.  There "
            "is no interior extremum that selects M=3.  At fixed M≠0 a "
            "stationary area can exist, but it is proportional to |M| and "
            "depends on the underived Wilson coefficients and on Λ; it is "
            "not a unique geometric output.  At M=0 the action is linear in "
            "A, so A is either driven to a boundary or is a flat direction if "
            "the linear coefficient is tuned to zero.  τ does not enter.  "
            "The tip contributes a boundary term proportional to 8ℓ_0 A, "
            "which shifts the linear coefficient in A but does not create a "
            "preferred integer flux.  The four nodes are not assigned an "
            "invented Seeley contribution."
        ),
    }
