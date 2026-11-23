"""Frequency-n right conoids, caps, and 'closed' variants.

Exploratory: these are not the locked SAM-3 embedding except for n=2,
which recovers f = sqrt(u^2 + 4 ell0^2 cos^2(2v)).  The locked core is
left unchanged.  The n=2 formulae below are consistency checks against
that core, not replacements for it.

Embedding family (right conoids of frequency n >= 1):

    r_n(u,v) = (u cos v,  u sin v,  ell0 sin(n v))

The induced metric is du^2 + f_n^2 dv^2 with

    f_n = sqrt(u^2 + n^2 ell0^2 cos^2(n v)).

For n=2 this is exactly the locked metric.  Isometry: v |-> v + pi/n
generates C_{2n}.  Nodes at u=0: the 2n zeros of cos(n v).  Tip-circle
length: 4 n ell0.  Gaussian curvature from the embedding:

    K = - n^2 ell0^2 cos^2(n v) / f_n^4 = - (f_n)_{uu} / f_n.

The complete-surface total curvature is still -2 pi, independent of n.
The truncated surface is always the annulus [a,b] x S^1; the untwisted
APS index with bounding spin structures at both ends is 0, independent
of n and of the metric (same product-collar argument as doc 44).
"""

from __future__ import annotations

import math
from typing import Dict, List

import numpy as np


def f_metric_n(u: float, v: float, n: int, ell0: float = 1.0) -> float:
    if n < 1:
        raise ValueError("frequency n must be a positive integer")
    return math.sqrt(u * u + (n * ell0) ** 2 * math.cos(n * v) ** 2)


def gaussian_curvature_n(u: float, v: float, n: int, ell0: float = 1.0) -> float:
    """K = - n^2 ell0^2 cos^2(n v) / f^4, away from f=0."""
    c = math.cos(n * v)
    f2 = u * u + (n * ell0) ** 2 * c * c
    if f2 <= 0:
        return float("nan")
    return -((n * ell0) ** 2 * c * c) / (f2 * f2)


def curvature_matches_minus_fuu_over_f(
    n: int, ell0: float = 1.0, n_samples: int = 40
) -> bool:
    """Finite-difference check that K = -f_uu / f for this warped-product metric."""
    rng = np.random.default_rng(2 + n)
    h = 1e-5
    for _ in range(n_samples):
        u = float(rng.uniform(0.4, 4.0))
        v = float(rng.uniform(0.0, 2.0 * math.pi))
        if abs(math.cos(n * v)) < 0.08:
            continue
        fuu = (
            f_metric_n(u + h, v, n, ell0)
            - 2.0 * f_metric_n(u, v, n, ell0)
            + f_metric_n(u - h, v, n, ell0)
        ) / h**2
        k_fd = -fuu / f_metric_n(u, v, n, ell0)
        k_ex = gaussian_curvature_n(u, v, n, ell0)
        if abs(k_fd - k_ex) > 1e-5 * (1.0 + abs(k_ex)):
            return False
    return True


def curvature_identity_symbolic(n: int) -> bool:
    """Exact identity K = -f_uu/f = -n^2 ell^2 cos^2(n v)/f^4."""
    import sympy as sp

    u, v, ell = sp.symbols("u v ell", real=True, positive=True)
    nn = sp.Integer(n)
    f = sp.sqrt(u**2 + (nn * ell) ** 2 * sp.cos(nn * v) ** 2)
    k = sp.simplify(-sp.diff(f, u, 2) / f)
    closed = -(nn * ell) ** 2 * sp.cos(nn * v) ** 2 / f**4
    return sp.simplify(k - closed) == 0


def isometry_order(n: int) -> int:
    """f_n is invariant under v |-> v + pi/n, a cyclic action of order 2n."""
    return 2 * n


def has_cyclic_isometry(n: int, n_samples: int = 80, ell0: float = 1.0) -> bool:
    step = math.pi / n
    rng = np.random.default_rng(10 + n)
    us = rng.uniform(0.0, 5.0, n_samples)
    vs = rng.uniform(0.0, 2.0 * math.pi, n_samples)
    a = np.array([f_metric_n(float(u), float(v), n, ell0) for u, v in zip(us, vs)])
    b = np.array(
        [f_metric_n(float(u), float(v + step), n, ell0) for u, v in zip(us, vs)]
    )
    # The generator should have order 2n, not a smaller positive order in general.
    # For a generic sample, f(v + 2pi/(2n)) = f(v) and f(v + 2pi/k) != f(v)
    # for proper divisors only as a metric identity of order 2n.
    return bool(np.allclose(a, b, rtol=0, atol=1e-14))


def tip_nodes(n: int) -> List[float]:
    """u=0 and cos(n v)=0: v = pi/(2n) + k pi/n, k = 0, ..., 2n-1."""
    return [math.pi / (2 * n) + k * math.pi / n for k in range(2 * n)]


def node_count(n: int) -> int:
    return 2 * n


def tip_circle_length(n: int, ell0: float = 1.0) -> float:
    """∫_0^{2π} f_n(0,v) dv = n ell0 ∫ |cos(n v)| dv = 4 n ell0.

    (θ = n v, ∫_0^{2π n} |cos θ| dθ / n = 4.)
    """
    return 4.0 * n * ell0


def tip_length_numerical(n: int, ell0: float = 1.0) -> float:
    """Adaptive integral of f_n(0,v); the integrand has 2n kinks (nodes)."""
    from scipy.integrate import quad

    def integrand(v: float) -> float:
        return f_metric_n(0.0, v, n, ell0)

    cuts = [0.0]
    for v0 in tip_nodes(n):
        if 0.0 < v0 < 2.0 * math.pi:
            cuts.append(v0)
    cuts.append(2.0 * math.pi)
    total = 0.0
    for a, b in zip(cuts, cuts[1:]):
        val, _err = quad(integrand, a, b, epsabs=1e-12, limit=200)
        total += val
    return float(total)


def max_abs_K_at_u(u: float, n: int, ell0: float = 1.0) -> float:
    """max_v |K(u,.)| = 1/(4 u^2) when 0 < u <= n ell0, else the endpoint value
    at |cos|=1, namely n^2 ell0^2 / (u^2 + n^2 ell0^2)^2.
    """
    if u <= 0:
        return float("inf")
    cap = n * ell0
    if u <= cap:
        return 1.0 / (4.0 * u * u)
    w = cap * cap
    return w / (u * u + w) ** 2


def boundary_integral_u_over_f(u: float, n: int, ell0: float = 1.0) -> float:
    """∫_0^{2π} u/f_n(u,v) dv, i.e. ∫ k_g ds on a u=const circle (outward +∂u).

    Near the 2n nodes the integrand has peaks of width ~ u/(n^2 ell0).
    A uniform grid undersamples them; the integral is split at the nodes
    and each open interval is handled by adaptive quadrature.  As u -> 0
    the contribution of each node vanishes as u |ln u|, and the integrand
    tends to 0 uniformly on compact sets away from the nodes, so the
    whole integral tends to 0.
    """
    if u <= 0:
        return 0.0
    from scipy.integrate import quad

    def integrand(v: float) -> float:
        return u / f_metric_n(u, v, n, ell0)

    total = 0.0
    # integrate from 0 to 2π, splitting at nodes (mod 2π)
    cuts = [0.0]
    for v0 in tip_nodes(n):
        if 0.0 < v0 < 2.0 * math.pi:
            cuts.append(v0)
    cuts.append(2.0 * math.pi)
    for a, b in zip(cuts, cuts[1:]):
        val, _err = quad(integrand, a, b, epsabs=1e-12, limit=200)
        total += val
    return float(total)


def total_curvature_truncated(a: float, b: float, n: int, ell0: float = 1.0) -> float:
    """Gauss-Bonnet on the annulus: ∫ K dA = ∫_a^b ∫ -f_uu dv du = ∫ (a/f(a) - b/f(b)) dv."""
    return boundary_integral_u_over_f(a, n, ell0) - boundary_integral_u_over_f(b, n, ell0)


def total_curvature_complete_limit(n: int, ell0: float = 1.0) -> Dict[str, float]:
    """a -> 0 and b -> infinity: tip contribution -> 0, outer -> 2 pi, ∫K -> -2 pi."""
    a, b = 1e-8, 1e8
    tip = boundary_integral_u_over_f(a, n, ell0)
    outer = boundary_integral_u_over_f(b, n, ell0)
    return {
        "tip_integral": tip,
        "outer_integral": outer,
        "total_curvature": tip - outer,
        "expected_total": -2.0 * math.pi,
    }


def aps_index_untwisted() -> Dict[str, object]:
    """The truncated frequency-n conoid is still [a,b] x S^1.

    The product-collar APS index of the untwisted Dirac operator, with a
    bounding spin structure at both ends, is 0, by the same argument as
    docs 44 and 46.  The metric (hence n) does not enter the index.
    """
    return {
        "topology": "[a,b] x S^1",
        "untwisted_APS_index_bounding_spin": 0,
        "depends_on_frequency_n": False,
        "depends_on_ell0": False,
        "three_from_frequency": False,
        "reason": (
            "Index is a topological invariant of the spin Dirac operator "
            "with the stated APS conditions on an annulus; it is 0 for every n."
        ),
    }


def closed_and_capped_variants(n: int, ell0: float = 1.0) -> Dict[str, object]:
    """Honest status of 'closed' or 'capped' conoid-like surfaces.

    The metric completion at u=0 is a geodesic circle of length 4 n ell0
    with 2n metric-degeneracy points (same analysis as doc 46, with 4
    replaced by 2n).  It is not a cone point, so there is no Cheeger
    compactification by adding a point that stays isometric to the
    original metric.
    """
    length = tip_circle_length(n, ell0)
    return {
        "tip_is_a_cone_point": False,
        "tip_is_geodesic_circle_with_nodes": True,
        "tip_length": length,
        "node_count": node_count(n),
        "collapse_tip_to_a_point": {
            "isometric": False,
            "reason": (
                f"The tip circle has positive length {length} (for ell0={ell0}); "
                "collapsing it is a different metric, not the completion."
            ),
        },
        "cap_tip_with_a_smooth_disk": {
            "regular_circle_would_match_a_hemisphere": (
                "A geodesic circle of length L matches the equator of a "
                f"round sphere of radius L/(2 pi) = {length / (2.0 * math.pi)}; "
                "k_g = 0 matches as well, away from the nodes."
            ),
            "obstruction": (
                "The metric on the tip circle degenerates at 2n nodes, so a "
                "C^infty cap that stays regular at those points is not given "
                "by the embedding and would have to resolve the nodes.  That "
                "resolution is an extra choice, not unique."
            ),
            "if_resolved_to_a_smooth_sphere": (
                "Untwisted Dirac index on a sphere is 0; a twist of degree d "
                "gives index d.  The 2n nodes do not select d=3 "
                f"(for n=2 one has 4 nodes; for n=3 one has 6)."
            ),
        },
        "identify_the_two_boundary_circles": {
            "topology": "torus",
            "untwisted_dirac_index": 0,
            "twisted_index": "the degree / flux, again a choice",
        },
        "three_comes_out_naturally": False,
        "verdict": "dead end",
        "reason": (
            "No unique smooth closed surface is determined by the embedding.  "
            "Every genuine compactification that yields a closed spin surface "
            "has untwisted Dirac index 0, and index 3 still requires a degree-3 "
            "twist.  The node count is 2n, never 3."
        ),
    }


def frequency_versus_generations(max_n: int = 6) -> Dict[str, object]:
    rows = []
    for n in range(1, max_n + 1):
        rows.append(
            {
                "n": n,
                "isometry": f"C_{2 * n}",
                "nodes": node_count(n),
                "tip_length_over_ell0": tip_circle_length(n, 1.0),
                "total_curvature_complete": -2.0 * math.pi,
                "untwisted_APS_index": 0,
                "equals_3": {
                    "nodes": node_count(n) == 3,
                    "isometry_order": (2 * n) == 3,
                    "tip_length_over_ell0": abs(tip_circle_length(n, 1.0) - 3.0) < 1e-15,
                    "total_curvature_over_2pi": False,  # always -1
                },
            }
        )
    return {
        "rows": rows,
        "any_integer_n_produces_3": False,
        "flag_numerology": (
            "Setting n=3 because one wants three generations only changes the "
            "isometry to C_6 and the node count to 6; the index stays 0.  "
            "That is a name, not a derivation."
        ),
        "verdict": "dead end",
        "reason": (
            "For every integer n the untwisted index is 0, the total curvature "
            "is -2 pi, and the discrete geometric counts are 2n (nodes) and "
            "2n (isometry order).  None of these is 3."
        ),
    }


def report() -> Dict[str, object]:
    n_locked = 2
    return {
        "exploratory": True,
        "locked_core": False,
        "n2_recovers_locked_metric": True,
        "n2_tip_length": tip_circle_length(n_locked, 1.0),
        "n2_nodes": node_count(n_locked),
        "n2_isometry_order": isometry_order(n_locked),
        "curvature_identities": {n: curvature_identity_symbolic(n) for n in (1, 2, 3, 4)},
        "complete_total_curvature": {
            n: total_curvature_complete_limit(n) for n in (1, 2, 3)
        },
        "aps": aps_index_untwisted(),
        "frequency_scan": frequency_versus_generations(),
        "closed_capped": closed_and_capped_variants(2),
        "verdict": "dead end",
        "reason": frequency_versus_generations()["reason"],
    }
