"""Zeta-regularized determinant of the magnetized-torus Dirac operator.

Exploratory: not part of the locked SAM-3 core.

The Dirac spectrum on a flat torus of area A with integer flux M > 0 is
standard (Landau levels; see e.g. Cremades–Ibáñez–Marchesano, JHEP 05
(2004) 079, and the exact heat kernel already used in doc 48):

    E_n = ± sqrt(4π n |M| / A),   n = 1, 2, …,

each with multiplicity |M|, together with |M| zero modes of one chirality.

The spectrum is independent of the complex structure τ.  Consequently no
functional of this spectrum can fix τ.  The zeta-regularized determinant
with zero modes omitted is nevertheless a well-defined spectral invariant,
in the same family of ideas as the Kronecker determinant on the unfluxed
torus, and can be evaluated in closed form.

Let D² act on the nonzero eigenspaces.  Then

    ζ_{D²}(s) = 2 M (4π M / A)^{-s} ζ(s),

where ζ is the Riemann zeta function (the factor 2 counts both chiralities
of the nonzero levels).  Using ζ(0) = −1/2 and ζ'(0) = −(1/2) log(2π),

    ζ'_{D²}(0) = M log(2 M / A),
    det'(D²)   = (2 M / A)^{-M},
    det'|D|    = (2 M / A)^{-M/2}.

This module records those identities, checks the zeta function against a
truncated Landau-level sum, and asks whether extremizing det'|D| selects
M = 3.
"""

from __future__ import annotations

import math
from typing import Dict, List, Tuple

# Riemann zeta values used in the closed form.  Both are classical.
ZETA_0 = -0.5
ZETA_PRIME_0 = -0.5 * math.log(2.0 * math.pi)


def zeta_D2(s: float, M: int, area: float) -> float:
    """Exact meromorphic expression 2 M (4π M / A)^{-s} ζ(s), for s ≠ 1."""
    if M <= 0 or area <= 0:
        raise ValueError("M and area must be positive")
    # Riemann zeta for real s ≠ 1, via the eta function for moderate s,
    # or the closed values we need.  For tests we mainly use s = 2, 3, 0.
    return 2.0 * M * (4.0 * math.pi * M / area) ** (-s) * _riemann_zeta(s)


def _riemann_zeta(s: float) -> float:
    if abs(s - 1.0) < 1e-12:
        raise ValueError("zeta has a pole at s = 1")
    if abs(s) < 1e-12:
        return ZETA_0
    # For s > 1 the series is elementary.  For the test points s = 2, 3
    # this is enough; for 0 < s < 1 use the eta function.
    if s > 1:
        acc = 0.0
        n = 1
        while True:
            term = n ** (-s)
            acc += term
            if term < 1e-18 * max(1.0, acc):
                break
            n += 1
            if n > 1_000_000:
                break
        return acc
    # eta(s) = ∑ (-1)^{n-1} n^{-s} = (1 − 2^{1-s}) ζ(s)
    acc = 0.0
    n = 1
    while n < 200_000:
        term = n ** (-s)
        acc += term if (n % 2 == 1) else -term
        if n > 20 and abs(term) < 1e-18:
            break
        n += 1
    return acc / (1.0 - 2.0 ** (1.0 - s))


def zeta_D2_from_levels(s: float, M: int, area: float, nmax: int) -> float:
    """Partial sum 2 M ∑_{n=1}^{nmax} (4π n M / A)^{-s}."""
    pref = 4.0 * math.pi * M / area
    acc = 0.0
    for n in range(1, nmax + 1):
        acc += (pref * n) ** (-s)
    return 2.0 * M * acc


def zeta_D2_prime_at_0(M: int, area: float) -> float:
    """Exact value ζ'_{D²}(0) = M log(2 M / A)."""
    if M <= 0 or area <= 0:
        raise ValueError("M and area must be positive")
    return M * math.log(2.0 * M / area)


def log_det_abs_D(M: int, area: float) -> float:
    """log det'|D| = −(M/2) log(2 M / A)."""
    return -0.5 * zeta_D2_prime_at_0(M, area)


def continuous_stationary_M(area: float) -> float:
    """Stationary point of log det'|D| at fixed area, treating M as real.

    ∂/∂M [−(M/2) log(2M/A)] = 0  ⇒  M = A / (2e).
    This is a maximum of log det'|D| (the second derivative is -1/(2M) < 0).
    """
    return area / (2.0 * math.e)


def area_that_places_stationary_at(M: int) -> float:
    """The area for which the continuous stationary point is this integer M."""
    return 2.0 * math.e * M


def scan_integers(area: float, M_max: int = 20) -> List[Tuple[int, float]]:
    return [(M, log_det_abs_D(M, area)) for M in range(1, M_max + 1)]


def best_integer_at_area(area: float, M_max: int = 40) -> Tuple[int, float]:
    """Integer M in 1..M_max that *maximizes* log det'|D| at this area."""
    pairs = scan_integers(area, M_max=M_max)
    M_star, val = max(pairs, key=lambda p: p[1])
    return M_star, val


def report() -> Dict[str, object]:
    # At the area that would "favour" M=3 if one put 3 in by hand.
    A_for_3 = area_that_places_stationary_at(3)
    M_star_3, _ = best_integer_at_area(A_for_3)
    # A generic area that is not tuned to 3.
    A_generic = 1.0
    M_star_g, _ = best_integer_at_area(A_generic)
    scan_generic = scan_integers(A_generic, M_max=8)
    scan_for_3 = scan_integers(A_for_3, M_max=8)
    return {
        "spectrum_depends_on_tau": False,
        "zeta_D2_formula": "2 M (4 pi M / A)^{-s} zeta(s)",
        "zeta_D2_prime_at_0": "M log(2 M / A)",
        "log_det_abs_D": "- (M/2) log(2 M / A)",
        "continuous_stationary_M": "A / (2 e)  (a maximum of log det'|D| at fixed A)",
        "area_that_would_favour_M_3": A_for_3,
        "best_integer_at_that_area": M_star_3,
        "best_integer_at_area_1": M_star_g,
        "log_det_scan_area_1": scan_generic,
        "log_det_scan_area_for_3": scan_for_3,
        "joint_critical_point_of_log_det_alone": False,
        "verdict": (
            "The fluxed Dirac determinant is independent of tau and does not "
            "select M=3.  At fixed area, maximizing det'|D| prefers M nearest A/(2e); placing "
            "that preference at 3 is a choice of area, not a derivation.  "
            "As a function of (M, A) jointly, log det'|D| has no interior "
            "critical point."
        ),
    }
