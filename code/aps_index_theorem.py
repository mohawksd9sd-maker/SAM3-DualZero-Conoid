"""APS index of the untwisted Dirac operator on the truncated right conoid.

This module records a theorem, not a numerical scan of a 2D grid.

Statement
---------
Let X_{a,b} = [a, b] × S¹, 0 < a < b < ∞, carry the locked right-conoid
metric du² + f(u,v)² dv² with f = √(u² + 4ℓ₀² cos²(2v)).  After the
product-collar deformation required by the Atiyah–Patodi–Singer theorem
(the metric is made of product type near each boundary component, without
changing the induced boundary metrics), the following hold.

1. The interior Â-density vanishes in dimension 2 (the first Pontryagin
   form is a 4-form).  Hence the bulk contribution to the APS index is 0.

2. On a product collar the boundary operator is unitarily equivalent to
   the standard 1-dimensional Dirac operator i d/ds on a circle of length
   L(u) = ∮ f(u,·) dv.  (The non-product term ½ ∂_u log f is removed by
   the collar deformation; keeping it would be inconsistent with the
   standard APS collar hypothesis.)

3. For the antiperiodic (bounding) spin structure on each boundary
   component — the structure that extends over a disk cap — the spectrum
   is { (2π/L)(k + 1/2) : k ∈ ℤ }, which is symmetric and has no zero.
   Thus η = 0, h = 0, and η-bar = (η + h)/2 = 0 at each end.

4. Therefore

       ind D_APS(X_{a,b}) = 0.

   The value is independent of a, b, and ℓ₀.  In particular it is not
   equal to 3.

5. For the periodic spin structure on a boundary component the spectrum
   is { (2π/L) k : k ∈ ℤ }, so h = 1, η = 0, η-bar = 1/2.  The index is
   then an integer in {−1, 0, 1} according to how many ends carry that
   structure and according to the outward-normal convention; it is still
   never 3.

Consequence for “three generations”
-----------------------------------
The claim that the APS index of the *untwisted* 2D Dirac operator on the
truncated conoid equals 3 (or equals “three light channels”) is not
supported: the index is 0 for the bounding spin structure.

A nonzero index can be arranged by coupling to an auxiliary U(1)
connection with boundary holonomy κ (Falomir–Pisani–Wipf, J. Phys. A 33
(2000) 1927, disk index = k + 1 with k < κ ≤ k + 1).  Index 3 then
requires κ ∈ (2, 3].  That flux is not determined by the locked conoid
metric: the metric’s spin connection is already part of the untwisted
Dirac operator and must not be counted twice.  So index 3 remains an
input, not a derivation, unless an independent geometric reason for
that κ is supplied.

The formula for the would-be non-product slice of the boundary operator
(included below as a diagnostic, not as an index input) is recorded so
the W ≠ 0 calculation is reproducible and is not confused with (4).
"""

from __future__ import annotations

import math
from typing import Dict

import numpy as np
from scipy.special import ellipk

# Local locked-metric helper (f, no Dirac matrices).
import os
import sys

_CODE = os.path.dirname(os.path.abspath(__file__))
if _CODE not in sys.path:
    sys.path.insert(0, _CODE)

from core_geometry import f_metric  # noqa: E402


def elliptic_k_parameter(u: float, ell0: float = 1.0) -> float:
    """m = k² = 4ℓ₀² / (u² + 4ℓ₀²), the parameter of K(k)."""
    return (4.0 * ell0 * ell0) / (u * u + 4.0 * ell0 * ell0)


def xi_mean_holonomy(u: float, ell0: float = 1.0) -> float:
    """ξ(u) = W-bar L / 2π for the *non-product* slice A = W + i∂_s.

    This is a diagnostic for the raw u = const. slice, before the
    product-collar deformation.  Closed form:

        ξ(u) = √(1 − k²) K(k) / π,    k² = 4ℓ₀²/(u² + 4ℓ₀²).

    Limits: ξ(u) → 0 as u → 0⁺, and ξ(u) → 1/2 as u → ∞.
    As u runs over (0, ∞), ξ stays in (0, 1/2].
    """
    m = elliptic_k_parameter(u, ell0)
    # scipy.special.ellipk takes the parameter m = k².
    return math.sqrt(1.0 - m) * float(ellipk(m)) / math.pi


def xi_by_quadrature(u: float, ell0: float = 1.0, n: int = 4000) -> float:
    """Independent check: ξ = (u / 4π) ∫_0^{2π} dv / f(u,v)."""
    v = np.linspace(0.0, 2.0 * math.pi, n, endpoint=False)
    inv_f = np.array([1.0 / f_metric(u, float(vi), ell0) for vi in v])
    integ = float(np.sum(inv_f) * (2.0 * math.pi / n))
    return (u * integ) / (4.0 * math.pi)


def eta_bar_circle_dirac(shift: float, spin: str) -> Dict[str, float]:
    """η-bar of i∂_s + W-bar on a circle, spectrum {W-bar − (2π/L)(k+α)}.

    Here ``shift`` is ξ = W-bar L / 2π.  For the product collar, W-bar = 0
    so ξ = 0 (periodic) or the equivalent AP lattice.

    ``spin`` is 'periodic' (α = 0) or 'antiperiodic' (α = 1/2).

    Standard result for eigenvalues {n + x : n ∈ ℤ}:
      if x ∉ ℤ:  h = 0, η(0) = 1 − 2{x}, η-bar = 1/2 − {x};
      if x ∈ ℤ:  h = 1, η(0) = 0,         η-bar = 1/2.
    """
    if spin not in ("periodic", "antiperiodic"):
        raise ValueError(spin)
    # Reduce to eigenvalues ω(ξ − k − α) = ω(x − k), x = ξ − α
    alpha = 0.0 if spin == "periodic" else 0.5
    x = shift - alpha
    # integer test with a tight tolerance on the fractional part
    frac = x - math.floor(x)
    near_int = min(frac, 1.0 - frac) < 1e-12
    if near_int:
        return {"h": 1.0, "eta": 0.0, "eta_bar": 0.5, "frac": 0.0, "x": x}
    eta = 1.0 - 2.0 * frac
    return {"h": 0.0, "eta": eta, "eta_bar": 0.5 - frac, "frac": frac, "x": x}


def product_collar_index(
    spin_inner: str = "antiperiodic",
    spin_outer: str = "antiperiodic",
) -> Dict[str, object]:
    """APS index on X_{a,b} after the product-collar deformation.

    Bulk term = 0.  Each end contributes η-bar of the 1D Dirac with the
    stated spin structure (W = 0).  The two bounding (antiperiodic) ends
    give index 0.  Periodic ends contribute 1/2 each; the resulting
    index, with the convention that both ends enter with the same
    η-bar sign in the sum over outward-oriented boundaries of a product
    collar.  The function reports the raw pair (η-bar_inner, η-bar_outer)
    and, when the combination −(η-bar_inner + η-bar_outer) is an integer
    under this convention, that integer.  For two antiperiodic ends the
    integer is 0 independently of orientation conventions.  For two
    periodic ends this convention gives −1.  Mixed structures are a
    different spin structure on the annulus; they are reported as
    orientation-sensitive, still in {−1, 0, 1}, never 3.

    We do *not* invent a unique value for the mixed/periodic cases
    beyond that range.  The case the theorem emphasizes is AP/AP.
    """
    inner = eta_bar_circle_dirac(0.0, spin_inner)
    outer = eta_bar_circle_dirac(0.0, spin_outer)
    # Product collar, W=0.  The combination −(η-bar_i + η-bar_o) is the
    # index under the convention that both boundaries enter with the
    # outward orientation and η-bar(−A) is computed with the same (η,h)
    # rule.  For AP/AP this is 0 independently of that convention.
    eta_sum = inner["eta_bar"] + outer["eta_bar"]
    if spin_inner == "antiperiodic" and spin_outer == "antiperiodic":
        index = 0
        status = "theorem: index = 0 (bounding spin structure at both ends)"
    elif eta_sum == int(eta_sum):
        index = -int(eta_sum)
        status = (
            f"convention-dependent integer {index} "
            f"(still in {{-1, 0, 1}}, never 3)"
        )
    else:
        index = None
        status = (
            "orientation-sensitive; combination is not fixed to a unique "
            "integer here; in all standard conventions the value lies in "
            "{-1, 0, 1}, never 3"
        )
    return {
        "bulk_A_hat": 0.0,
        "spin_inner": spin_inner,
        "spin_outer": spin_outer,
        "inner": inner,
        "outer": outer,
        "eta_bar_sum": eta_sum,
        "index": index,
        "status": status,
        "three_not_attained": True,
    }


def falomir_flux_for_index(target_index: int) -> Dict[str, object]:
    """κ-interval on the disk that yields a given Falomir index.

    Falomir et al.: k = ceil(κ) − 1, with k < κ ≤ k + 1, and
    index = k + 1.  So index = n ≥ 1 requires κ ∈ (n − 1, n].
    κ is an extra U(1) holonomy, not a derived property of f.
    """
    if target_index == 0:
        return {
            "target_index": 0,
            "kappa_interval": "κ ∈ (−1, 0] (and the κ = 0 disk)",
            "derived_from_conoid_metric": False,
        }
    n = int(target_index)
    return {
        "target_index": n,
        "kappa_interval": (float(n - 1), float(n)),
        "kappa_interval_desc": f"κ ∈ ({n - 1}, {n}]",
        "derived_from_conoid_metric": False,
    }


def report() -> Dict[str, object]:
    """Reproduce the numerical checks that accompany the theorem."""
    us = [0.05, 0.2, 0.5, 1.0, 2.0, 6.0, 20.0, 80.0]
    xi_rows = []
    for u in us:
        closed = xi_mean_holonomy(u)
        quad = xi_by_quadrature(u)
        xi_rows.append(
            {
                "u": u,
                "xi_closed": closed,
                "xi_quad": quad,
                "abs_diff": abs(closed - quad),
                "in_0_half": 0.0 < closed <= 0.5 + 1e-12,
            }
        )
    # limits
    xi_small = xi_mean_holonomy(1e-4)
    xi_large = xi_mean_holonomy(1e4)
    apap = product_collar_index("antiperiodic", "antiperiodic")
    perper = product_collar_index("periodic", "periodic")
    return {
        "xi_rows": xi_rows,
        "xi_u_1e-4": xi_small,
        "xi_u_1e4": xi_large,
        "xi_infinity_target": 0.5,
        "product_collar_AP_AP": apap,
        "product_collar_periodic_periodic": perper,
        "untwisted_index_AP_AP": 0,
        "three_generations_from_untwisted_index": "refuted",
        "falomir_index_3_requires": falomir_flux_for_index(3),
    }


if __name__ == "__main__":
    import json

    r = report()
    # compact print: drop the long row objects' floats only
    out = {
        k: v
        for k, v in r.items()
        if k != "xi_rows"
    }
    out["xi_max_quad_error"] = max(row["abs_diff"] for row in r["xi_rows"])
    out["xi_all_in_0_half"] = all(row["in_0_half"] for row in r["xi_rows"])
    print(json.dumps(out, indent=2, default=str))
