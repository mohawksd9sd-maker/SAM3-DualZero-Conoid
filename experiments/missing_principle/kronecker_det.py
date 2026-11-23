"""Zeta-regularized det' of the Laplacian on a unit-area flat torus, as a function of τ.

Exploratory: not part of the locked SAM-3 core.

Literature (fetched, not invented)
---------------------------------
- Kronecker's first limit formula expresses the constant term of the Epstein
  zeta (equivalently, the spectral zeta of the flat Laplacian) in terms of
  the Dedekind eta function.  A standard form is
      ζ_Epstein(s, τ) = π/(s-1) + 2π(γ - log 2 - log(√(Im τ) |η(τ)|²)) + O(s-1)
  as s → 1⁺.
- B. Osgood, R. Phillips and P. Sarnak, "Extremals of determinants of
  Laplacians", J. Funct. Anal. 80 (1988) 148–211.  Among unit-area metrics
  on a torus, and in particular among unit-area flat tori, det'Δ is
  maximized at the hexagonal lattice.  Equivalently, the modular function
      F(τ) = √(Im τ) |η(τ)|²
  attains its unique maximum on SL(2,Z)\\H at τ = e^{iπ/3} (equivalently
  e^{2πi/3}, which is in the same orbit).
- P. Chiu, "Height of flat tori", Proc. Amer. Math. Soc. 125 (1997) 723–730.
  For a unit-area flat torus of modulus τ = x+iy the height Z'(0) differs
  from −log(y |η(τ)|⁴) by an additive constant, so the extrema of det'Δ
  and of y |η(τ)|⁴ coincide.

This module evaluates F(τ) numerically from the eta product, checks modular
invariance, and locates the maxima in the standard fundamental domain.
It does not invent a new closed form for det'Δ.  The additive constant in
Z'(0) is not needed to compare τ-points, and is not recomputed here.
"""

from __future__ import annotations

import cmath
import math
from typing import Dict, List, Tuple

import numpy as np

TAU_I = 1j
TAU_RHO = -0.5 + 1j * math.sqrt(3.0) / 2.0  # e^{2πi/3}, hexagonal
TAU_RHO_RIGHT = 0.5 + 1j * math.sqrt(3.0) / 2.0  # e^{iπ/3}, same SL(2,Z) orbit


def dedekind_eta(tau: complex, nterms: int = 80) -> complex:
    """η(τ) = q^{1/24} ∏_{n≥1} (1 − q^n),  q = exp(2πi τ).

    For Im(τ) ≥ √3/2 the factor |q| is smaller than 5×10^{-3}, so a few
    dozen terms already exhaust double precision.
    """
    if tau.imag <= 0:
        raise ValueError("tau must lie in the upper half-plane")
    log_q = 2j * math.pi * tau
    log_eta = log_q / 24.0
    q = cmath.exp(log_q)
    qn = q
    one = 1.0 + 0.0j
    for _ in range(1, nterms + 1):
        log_eta += cmath.log(one - qn)
        qn *= q
        if abs(qn) < 1e-18:
            break
    return cmath.exp(log_eta)


def F(tau: complex, nterms: int = 80) -> float:
    """The modular function √(Im τ) |η(τ)|² of Osgood–Phillips–Sarnak."""
    eta = dedekind_eta(tau, nterms=nterms)
    return math.sqrt(tau.imag) * (abs(eta) ** 2)


def y_eta4(tau: complex, nterms: int = 80) -> float:
    """y |η(τ)|⁴ = F(τ)², monotonically equivalent for locating extrema."""
    val = F(tau, nterms=nterms)
    return val * val


def in_fundamental_domain(tau: complex, tol: float = 1e-12) -> bool:
    """Standard fundamental domain: |Re τ| ≤ 1/2 and |τ| ≥ 1."""
    return abs(tau.real) <= 0.5 + tol and abs(tau) >= 1.0 - tol


def sl2z_apply(tau: complex, a: int, b: int, c: int, d: int) -> complex:
    return (a * tau + b) / (c * tau + d)


def modular_invariance_errors(tau: complex) -> Dict[str, float]:
    """F should be invariant under T: τ→τ+1 and S: τ→−1/τ."""
    f0 = F(tau)
    fT = F(tau + 1)
    fS = F(-1.0 / tau)
    return {
        "F": f0,
        "abs_F_minus_F_T": abs(f0 - fT),
        "abs_F_minus_F_S": abs(f0 - fS),
    }


def scan_fundamental_domain(
    n_x: int = 81,
    n_y: int = 120,
    y_max: float = 3.0,
) -> Dict[str, float]:
    """Grid search for the max of F on the standard fundamental domain.

    The domain is cut off at Im(τ) ≤ y_max.  For large y, η(τ) ∼ e^{πi τ/12}
    and F(τ) ∼ √y exp(−π y / 6) → 0, so the maximum cannot hide at large y.
    """
    xs = np.linspace(-0.5, 0.5, n_x)
    ys = np.linspace(math.sqrt(3.0) / 2.0, y_max, n_y)
    f_max = -1.0
    tau_max = 0j
    f_at_i = F(TAU_I)
    f_at_rho = F(TAU_RHO)
    f_at_rho_right = F(TAU_RHO_RIGHT)
    # Seed the search with the two classical elliptic points so the grid
    # cannot miss them by sampling.
    for tau0 in (TAU_I, TAU_RHO, TAU_RHO_RIGHT):
        val0 = F(tau0)
        if val0 > f_max:
            f_max = val0
            tau_max = tau0
    # Also record the max among rectangular tori (Re τ = 0, Im τ ≥ 1).
    f_rect_max = f_at_i
    y_rect_max = 1.0
    for y in ys:
        for x in xs:
            tau = complex(float(x), float(y))
            if abs(tau) < 1.0 - 1e-12:
                continue
            val = F(tau)
            if val > f_max:
                f_max = val
                tau_max = tau
        # rectangular slice
        if y >= 1.0 - 1e-12:
            val0 = F(1j * float(y))
            if val0 > f_rect_max:
                f_rect_max = val0
                y_rect_max = float(y)
    return {
        "grid_n_x": n_x,
        "grid_n_y": n_y,
        "y_max": y_max,
        "F_max_on_grid": f_max,
        "tau_max_re": tau_max.real,
        "tau_max_im": tau_max.imag,
        "F_at_i": f_at_i,
        "F_at_rho": f_at_rho,
        "F_at_rho_right": f_at_rho_right,
        "F_rect_max": f_rect_max,
        "y_rect_max": y_rect_max,
        "F_max_minus_F_rho": f_max - f_at_rho,
        "F_rho_minus_F_i": f_at_rho - f_at_i,
    }


def report() -> Dict[str, object]:
    scan = scan_fundamental_domain()
    # Distance of the grid maximizer to the right or left hexagonal point.
    d_left = math.hypot(scan["tau_max_re"] - TAU_RHO.real, scan["tau_max_im"] - TAU_RHO.imag)
    d_right = math.hypot(
        scan["tau_max_re"] - TAU_RHO_RIGHT.real,
        scan["tau_max_im"] - TAU_RHO_RIGHT.imag,
    )
    inv = modular_invariance_errors(1.1 + 1.3j)
    return {
        "function": "F(tau) = sqrt(Im tau) |eta(tau)|^2",
        "literature_maximizer": "hexagonal torus, tau = exp(i pi / 3) ~ exp(2 pi i / 3)",
        "scan": scan,
        "grid_maximizer_distance_to_nearest_hexagonal": min(d_left, d_right),
        "modular_invariance_sample": inv,
        "eta_of_i_abs": abs(dedekind_eta(TAU_I)),
        "verdict": (
            "Among unit-area flat tori, extremizing det' of the Laplacian "
            "selects the hexagonal modulus tau = exp(2 pi i / 3) (up to "
            "SL(2,Z)), not a unique area and not the flux.  The square "
            "torus tau = i is only a critical point among rectangular "
            "tori.  This conflicts with a C4-compatibility requirement, "
            "which would instead select tau = i."
        ),
    }
