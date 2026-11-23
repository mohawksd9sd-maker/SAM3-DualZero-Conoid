"""Geometric heat-kernel ingredients of the locked right conoid.

Exact identities (no cutoff function required):

1. Area of the truncated conoid X_{a,b} = [a,b] × S¹, 0 < a < b < ∞,
   with volume form f du dv:

       A(a,b) = π(b² − a²) + ∫_a^b I(u) du,

   where I(u) = ∫_0^{2π} (f − u) dv.  On the unit metric, as b→∞ with a
   fixed (or a→0, since I is bounded near 0),

       A(a,b) = π b² + 2π log b + C0 + o(1),    C0 = 2π ln 2.

   For general ℓ0 one has I(u;ℓ0) = ℓ0 I(u/ℓ0; 1), hence
       A(0,b) = π b² + 2π ℓ0² log(b/ℓ0) + 2π ℓ0² ln 2 + o(1).

2. Gaussian curvature integral, by an exact u-antiderivative
   (K f = −A / f³ with A = 4ℓ0² cos²(2v)):

       ∫_{X_{a,b}} K dA = ∫_0^{2π} ( a/f(a,v) − b/f(b,v) ) dv.

3. Gauss–Bonnet for the annulus (χ = 0) is the identity
       ∫ K dA + ∫_{u=b} (f_u/f) ds − ∫_{u=a} (f_u/f) ds = 0,
   because (f_u/f) ds = (u/f) dv on a u = const. curve.

4. Complete-surface limit: as a→0 and b→∞,
       ∫ K dA → −2π.
   (The outer integrand b/f → 1, the inner integrand a/f → 0 in L¹.)

These are integrals of the metric and of K.  They enter the Seeley–DeWitt
a0 (area, times the fibre rank) and a2 (a universal multiple of ∫R plus
boundary terms) of any Laplace-type operator.  We do not invent a unique
numerical prefactor for a2 of the APS Dirac operator beyond the geometric
integrals above; the universal interior combination for the Dirac Laplacian
on a closed surface is recorded as a literature pointer (Gilkey; the
Lichnerowicz shift R/4), not as a new derivation of a 4D coupling.
"""

from __future__ import annotations

import math
from typing import Dict

import numpy as np
from scipy.special import ellipk

import os
import sys

_CODE = os.path.dirname(os.path.abspath(__file__))
if _CODE not in sys.path:
    sys.path.insert(0, _CODE)

from core_geometry import C0_EXACT, angular_integrand_I, f_metric  # noqa: E402


def circumference_density(u: float, v: float, ell0: float = 1.0) -> float:
    """The factor f, i.e. √g in (u,v) coordinates."""
    return f_metric(u, v, ell0)


def u_over_f(u: float, v: float, ell0: float = 1.0) -> float:
    return u / f_metric(u, v, ell0)


def boundary_integral_u_over_f(u: float, ell0: float = 1.0, n: int = 8000) -> float:
    """∫_0^{2π} (u/f(u,v)) dv  =  ∫ (f_u/f) ds on the curve u = const.

    Closed form: 4 u K(k) / √(u²+4ℓ0²),  k² = 4ℓ0²/(u²+4ℓ0²),
    with K the complete elliptic integral of the first kind.
    The argument ``n`` is accepted for API stability and ignored.
    """
    del n
    if u < 0:
        raise ValueError("u must be nonnegative")
    if u == 0.0:
        return 0.0
    denom = math.sqrt(u * u + 4.0 * ell0 * ell0)
    kprime = u / denom  # √(1−k²)
    m = 1.0 - kprime * kprime
    # K(k) ~ log(4/k') as k'→0; scipy.ellipk overflows once 1−m underflows.
    if kprime < 1e-8:
        K = math.log(4.0 / kprime)
        return 4.0 * kprime * K
    return 4.0 * kprime * float(ellipk(m))


def curvature_integral(a: float, b: float, ell0: float = 1.0, n: int = 8000) -> float:
    """Exact antiderivative reduced to a 1D angular integral: bin − bout."""
    if not (0.0 < a < b):
        raise ValueError("need 0 < a < b")
    return boundary_integral_u_over_f(a, ell0, n) - boundary_integral_u_over_f(b, ell0, n)


def gauss_bonnet_residual(a: float, b: float, ell0: float = 1.0, n: int = 8000) -> float:
    """∫K + I(b) − I(a), which vanishes identically (up to quadrature)."""
    Ik = curvature_integral(a, b, ell0, n)
    bout = boundary_integral_u_over_f(b, ell0, n)
    binr = boundary_integral_u_over_f(a, ell0, n)
    return Ik + bout - binr


def total_curvature_complete() -> float:
    """∫ K dA over the complete open conoid (0,∞)×S¹, unit or any ℓ0."""
    return -2.0 * math.pi


def area_truncation(a: float, b: float, ell0: float = 1.0, n_u: int = 4000) -> float:
    """A(a,b) = π(b²−a²) + ∫_a^b I(u;ℓ0) du, trapezoid in u."""
    if not (0.0 <= a < b):
        raise ValueError("need 0 ≤ a < b")
    us = np.linspace(a, b, n_u)
    # I(u;ℓ0) = ℓ0 I(u/ℓ0; 1) for u>0; at u=0, I=8 ℓ0.
    def I(u: float) -> float:
        if ell0 == 1.0:
            return angular_integrand_I(u, ell0=1.0)
        if u <= 0.0:
            return 8.0 * ell0
        return ell0 * angular_integrand_I(u / ell0, ell0=1.0)

    Is = np.array([I(float(u)) for u in us])
    return math.pi * (b * b - a * a) + float(np.trapezoid(Is, us))


def area_asymptotic_unit(b: float) -> float:
    """π b² + 2π log b + C0,  unit metric, tip included, large-b finite part."""
    return math.pi * b * b + 2.0 * math.pi * math.log(b) + C0_EXACT


def area_asymptotic(b: float, ell0: float) -> float:
    """π b² + 2π ℓ0² log(b/ℓ0) + 2π ℓ0² ln 2."""
    return (
        math.pi * b * b
        + 2.0 * math.pi * ell0 * ell0 * math.log(b / ell0)
        + 2.0 * math.pi * ell0 * ell0 * math.log(2.0)
    )


def inner_boundary_tends_to_zero(u_values=None, ell0: float = 1.0) -> Dict[str, object]:
    if u_values is None:
        u_values = (1.0, 0.3, 0.1, 0.03, 0.01, 0.003)
    rows = [{"u": u, "integral": boundary_integral_u_over_f(u, ell0)} for u in u_values]
    return {"rows": rows, "limit_0": 0.0, "monotonic_down": all(
        rows[i]["integral"] > rows[i + 1]["integral"] for i in range(len(rows) - 1)
    )}


def report() -> Dict[str, object]:
    pairs = [(0.2, 6.0), (0.05, 20.0), (0.01, 80.0)]
    gb = []
    for a, b in pairs:
        gb.append({
            "a": a, "b": b,
            "int_K": curvature_integral(a, b),
            "GB_residual": gauss_bonnet_residual(a, b),
            "area": area_truncation(a, b),
        })
    # complete-curvature approach
    approach = [{"b": b, "int_K": curvature_integral(1e-4, b)} for b in (5.0, 20.0, 80.0, 400.0)]
    # area vs asymptotic on the unit metric, a very small
    areas = []
    for b in (10.0, 20.0, 40.0):
        A = area_truncation(1e-8, b, ell0=1.0)
        asym = area_asymptotic_unit(b)
        areas.append({"b": b, "A": A, "asymptotic": asym, "diff": A - asym})
    return {
        "C0": C0_EXACT,
        "complete_curvature": total_curvature_complete(),
        "gauss_bonnet": gb,
        "intK_approaching_minus_2pi": approach,
        "area_vs_asymptotic": areas,
        "inner_end": inner_boundary_tends_to_zero(),
    }


if __name__ == "__main__":
    import json
    r = report()
    out = {
        "complete_curvature": r["complete_curvature"],
        "max_GB_residual": max(abs(row["GB_residual"]) for row in r["gauss_bonnet"]),
        "intK_at_large_b": r["intK_approaching_minus_2pi"][-1],
        "area_diff_at_20": [row for row in r["area_vs_asymptotic"] if row["b"] == 20.0][0]["diff"],
        "inner_monotonic": r["inner_end"]["monotonic_down"],
    }
    print(json.dumps(out, indent=2))
