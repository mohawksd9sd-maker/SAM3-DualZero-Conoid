"""Singular tip u→0 of the locked right conoid: geometry, Dirac, index, heat kernel.

This is the analysis that the product-collar APS theorem (doc 44) does not
cover: that theorem applies to the smooth compact annulus X_{a,b} with 0<a.

Conclusions (labelled below) are theorems, numerical observations, or
honest negatives.  Cheeger cone-point formulae, incomplete-edge index
theorems, and conical-defect heat-kernel terms are cited only to record
that the tip is *not* of those types; their numerical coefficients are
not applied.

Abstract vs embedded
--------------------
The Dirac operator and the index are defined on the abstract Riemannian
surface (the coordinate cylinder with the induced metric), not on the
image in R³.  The embedding
    r(u,v) = (u cos v, u sin v, ℓ0 sin(2v))
is an embedding for u>0.  At u=0 the image is the segment
{0}×{0}×[−ℓ0,ℓ0] on the z-axis: a self-intersection of the image along
the open segment, with the four coordinate nodes mapping to the two
endpoints (each with two preimages).  That is a statement about the
map r, not about the abstract metric singularity.

Abstract metric, completed
--------------------------
On M = (0, U)×S¹ the metric ds² = du² + f² dv² is smooth and positive
definite (f>0 for u>0).  It is incomplete: the curves of constant v
are unit-speed geodesics, so dist((u,v), {u=0}) = u is finite.

The metric tensor itself, in coordinates (u,v), is C^∞ on the closed
cylinder [0,U]×S¹: g_vv = u² + 4ℓ0² cos²(2v) is a trigonometric
polynomial.  It is positive definite except at the four boundary points
    v_k = π/4 + k π/2,  u = 0,
where g_vv = 0.  The metric completion adds the circle u=0, of length
    L(0) = ∫_0^{2π} 2ℓ0 |cos(2v)| dv = 8 ℓ0.
Away from the four nodes, f(0,v) = 2ℓ0 |cos(2v)| > 0 and the metric
is a smooth product-type collar (f_u = u/f = 0 at u=0), so the regular
part of the tip is a genuine Riemannian boundary.  The geodesic
curvature of u=0 vanishes wherever f>0 (k_g = f_u/f = 0): the regular
tip is a geodesic.

The four nodes are therefore isolated degeneracy points of a C^∞ metric
on a compact surface with boundary, lying on a geodesic boundary
circle.  They are not interior cone points (the Cheeger model
dr² + r² g_N does not describe a neighbourhood of a node: the metric
is anisotropic, and a neighbourhood in the completion is a half-disk,
not a full cone).  They are not an incomplete edge in the sense of
Mazzeo / Albin–Gell-Redman (no positive-dimensional singular stratum
with a conical normal plane).

Curvature
---------
K = −4ℓ0² cos²(2v)/f^4 ≤ 0 everywhere it is defined.  K is unbounded
near the four nodes: for each fixed u ∈ (0, 2ℓ0],
    max_v |K(u,·)| = 1/(4u²),
attained where 4ℓ0² cos²(2v) = u².  The older claim ||K||_max = 1/(4ℓ0²)
is the value of |K| at the mid-arcs u=0, |cos(2v)|=1; it is not a
global bound.  Nonetheless K is integrable: on the complete surface
∫ K dA = −2π, hence ∫ |K| dA = 2π, and the mass of |K| in a
coordinate half-disk of radius R about a node is O(R).  Combined with
the Gauss–Bonnet identity and I(a)→0 as a→0, there is no residual
δ-mass of curvature at the tip circle or at the four nodes.

Dirac operator
--------------
Chernoff (J. Funct. Anal. 12 (1973); Pacific J. Math. 72 (1977)) and
Wolf (Indiana Univ. Math. J. 22 (1973)): the Dirac operator on a
*complete* Riemannian spin manifold is essentially self-adjoint on
compactly supported smooth spinors.  The converse obstruction is
immediate here: M is incomplete, with a boundary at finite distance,
so essential self-adjointness fails for the usual reason it fails on
any compact surface with boundary.

In any open set of the closed cylinder that avoids the four nodes, the
metric is a smooth product collar at u=0, and the Dirac operator has
the standard APS collar form σ(∂_u + A).  Each angular mode of A is a
regular (limit-circle) endpoint of a 1D Dirac system: a boundary
condition is required.  The space of self-adjoint extensions is the
usual infinite-dimensional Grassmannian of elliptic boundary
conditions on the tip circle (and at the outer end).  The four nodes
are a capacity-zero / measure-zero subset of that circle; they do not
turn the problem into a Cheeger cone-point deficiency problem, and we
do not invent a finite deficiency index for each node.

Index
-----
For every a>0 the product-collar APS index of X_{a,U} is 0 (doc 44),
for the bounding spin structure, independently of a.  The inner
boundary operator in the product-collar picture has no kernel for
that spin structure, for every a>0 (no spectral flow as a↓0).  This
is strong evidence that the limiting problem on the completed surface
also has index 0 if one uses APS (or the Friedrichs / minimal
extension, the other standard choice) at the tip.  We do *not* claim
a new theorem that “APS on a circle with four metric degeneracies”
is already in the literature.  We do claim that nothing in the tip
geometry produces a derived index of 3: an extension with index 3
would be an additional choice of boundary condition, not forced by
the metric.

Heat kernel
-----------
The area of a tip neighbourhood {u≤a} is finite and is ~ 8 ℓ0 a as
a→0 (no area divergence).  Standard boundary Seeley terms involve
the geodesic curvature of the boundary; k_g=0 on the regular tip, so
those terms vanish there.  The conical-defect corrections of the
form (β/6)((2π/β)²−1) at a cone of angle β (e.g. Fursaev, De Nardo–
Fursaev–Miele, hep-th/9405143 and hep-th/9605153) are for metric
cones and are not applicable.  We do not invent a 0-dimensional
coefficient at the four nodes.
"""

from __future__ import annotations

import math
from typing import Dict, List, Tuple

import numpy as np

import os
import sys

_CODE = os.path.dirname(os.path.abspath(__file__))
if _CODE not in sys.path:
    sys.path.insert(0, _CODE)

from conoid_heat_kernel import (  # noqa: E402
    boundary_integral_u_over_f,
    curvature_integral,
    total_curvature_complete,
)
from core_geometry import (  # noqa: E402
    f_metric,
    gaussian_curvature,
    tip_nodes,
    angular_integrand_I,
)
from aps_index_theorem import product_collar_index, eta_bar_circle_dirac  # noqa: E402


def tip_circle_length(ell0: float = 1.0) -> float:
    """Length of the completed tip locus u=0: 8 ℓ0."""
    return 8.0 * ell0


def geodesic_curvature_on_regular_tip(v: float, ell0: float = 1.0) -> float:
    """k_g = f_u/f = u/f at u=0, which is 0 wherever f(0,v)>0."""
    f0 = f_metric(0.0, v, ell0)
    if f0 <= 0.0:
        return float("nan")
    return 0.0  # exact: f_u(0,v) = 0/f0 = 0


def max_abs_K_at_u(u: float, ell0: float = 1.0) -> float:
    """Exact: for 0 < u ≤ 2ℓ0, max_v |K| = 1/(4u²); for u ≥ 2ℓ0, 4ℓ0²/(u²+4ℓ0²)²."""
    if u <= 0:
        raise ValueError("u must be positive")
    if u <= 2.0 * ell0:
        return 1.0 / (4.0 * u * u)
    t = 4.0 * ell0 * ell0
    return t / (u * u + t) ** 2


def numerical_max_abs_K(u: float, ell0: float = 1.0, n: int = 20000) -> float:
    vs = np.linspace(0.0, 2.0 * math.pi, n, endpoint=False)
    return float(max(abs(gaussian_curvature(u, float(v), ell0)) for v in vs))


def K_is_nonpositive_sample(n_u: int = 40, n_v: int = 200, ell0: float = 1.0) -> bool:
    us = np.geomspace(1e-4, 20.0, n_u)
    vs = np.linspace(0.0, 2.0 * math.pi, n_v, endpoint=False)
    for u in us:
        for v in vs:
            if gaussian_curvature(float(u), float(v), ell0) > 1e-12:
                return False
    return True


def old_K_max_claim_fails(ell0: float = 1.0) -> Dict[str, float]:
    """The value 1/(4ℓ0²) is exceeded as soon as u < ℓ0, near the nodes."""
    claimed = 1.0 / (4.0 * ell0 * ell0)
    u = 0.5 * ell0
    actual = max_abs_K_at_u(u, ell0)
    return {"claimed": claimed, "actual_at_u=ell0/2": actual, "ratio": actual / claimed}


def local_abs_K_mass_bound(R: float, ell0: float = 1.0) -> float:
    """Analytic L¹ bound in the local model of one node.

    In coordinates s = v − π/4, f² ≈ u² + 16 ℓ0² s² = u² + α² s², α=4ℓ0,
    ∫_{u²+α²s² ≤ R², u≥0} |K| dA ≈ (π/2) (R/α) = π R / (8 ℓ0).
    """
    alpha = 4.0 * ell0
    return (math.pi / 2.0) * (R / alpha)


def numerical_abs_K_mass_box(
    u_max: float, s_max: float, ell0: float = 1.0, nu: int = 240, ns: int = 240
) -> float:
    us = np.linspace(1e-14, u_max, nu)
    ss = np.linspace(-s_max, s_max, ns)
    acc = np.empty((nu, ns))
    v0 = math.pi / 4
    for i, u in enumerate(us):
        for j, s in enumerate(ss):
            f = f_metric(float(u), float(v0 + s), ell0)
            K = gaussian_curvature(float(u), float(v0 + s), ell0)
            acc[i, j] = abs(K) * f
    return float(np.trapezoid(np.trapezoid(acc, ss, axis=1), us))


def tip_neighbourhood_area(a: float, ell0: float = 1.0, n_u: int = 2000) -> float:
    """A(0,a) = π a² + ∫_0^a I(u;ℓ0) du, with I(0)=8ℓ0."""
    if a < 0:
        raise ValueError("a>=0")
    if a == 0:
        return 0.0

    def I(u: float) -> float:
        if ell0 == 1.0:
            return angular_integrand_I(u, ell0=1.0)
        if u <= 0.0:
            return 8.0 * ell0
        return ell0 * angular_integrand_I(u / ell0, ell0=1.0)

    us = np.linspace(0.0, a, n_u)
    Is = np.array([I(float(u)) for u in us])
    return math.pi * a * a + float(np.trapezoid(Is, us))


def inner_aps_kernel_along_cuts(a_values=None) -> Dict[str, object]:
    """Product-collar AP boundary operator has h=0 at every positive cut."""
    if a_values is None:
        a_values = (1e-4, 0.01, 0.1, 0.5, 1.0, 5.0)
    rows = []
    for a in a_values:
        r = eta_bar_circle_dirac(0.0, "antiperiodic")
        rows.append({"a": a, "h": r["h"], "eta_bar": r["eta_bar"]})
    return {
        "rows": rows,
        "all_h_zero": all(row["h"] == 0.0 for row in rows),
        "index_of_each_truncation": product_collar_index("antiperiodic", "antiperiodic")["index"],
    }


def metric_circle_ratio_around_node(
    epsilons: Tuple[float, ...] = (0.06, 0.04, 0.03, 0.02),
    u_max: float = 0.22,
    s_max: float = 0.22,
    nu: int = 320,
    ns: int = 321,
    ell0: float = 1.0,
    margin: float = 0.04,
) -> List[Dict[str, float]]:
    """Numerical length of the metric circle of radius ε about one node.

    A Dijkstra approximation on a grid in (u, s), s = v − π/4.  The ratios
    L/ε are reported as a numerical observation, not as a theorem that the
    limit is π.  They are used only to distinguish a cusp (L/ε→0) or a
    full cone (L/ε→2π) from a half-disk-scale link (L/ε of order π).
    """
    import heapq

    us = np.linspace(0.0, u_max, nu)
    ss = np.linspace(-s_max, s_max, ns)
    j0 = int(np.argmin(np.abs(ss)))
    inf = 1e100
    dist = np.full((nu, ns), inf)
    dist[0, j0] = 0.0
    heap = [(0.0, 0, j0)]

    def edge_len(i1, j1, i2, j2) -> float:
        u1, s1 = us[i1], ss[j1]
        u2, s2 = us[i2], ss[j2]
        um, sm = 0.5 * (u1 + u2), 0.5 * (s1 + s2)
        f = f_metric(float(max(um, 0.0)), float(math.pi / 4 + sm), ell0)
        du, ds = u2 - u1, s2 - s1
        return math.sqrt(du * du + f * f * ds * ds)

    nbrs = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))
    while heap:
        d, i, j = heapq.heappop(heap)
        if d > dist[i, j] + 1e-15:
            continue
        for di, dj in nbrs:
            ii, jj = i + di, j + dj
            if 0 <= ii < nu and 0 <= jj < ns:
                nd = d + edge_len(i, j, ii, jj)
                if nd < dist[ii, jj] - 1e-15:
                    dist[ii, jj] = nd
                    heapq.heappush(heap, (nd, ii, jj))

    rows = []
    for eps in epsilons:
        length = 0.0
        nseg = 0
        for i in range(nu - 1):
            if us[i + 1] > us[-1] - margin:
                continue
            for j in range(ns - 1):
                if min(abs(ss[j]), abs(ss[j + 1])) > ss[-1] - margin:
                    continue
                corners = ((i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1))
                vals = [dist[a, b] for a, b in corners]
                if any(v > 1e99 for v in vals):
                    continue
                pts = []
                for e1, e2 in ((0, 1), (1, 2), (2, 3), (3, 0)):
                    i1, j1 = corners[e1]
                    i2, j2 = corners[e2]
                    d1, d2 = dist[i1, j1], dist[i2, j2]
                    if (d1 - eps) * (d2 - eps) <= 0 and d1 != d2:
                        t = min(1.0, max(0.0, (eps - d1) / (d2 - d1)))
                        pts.append(
                            (
                                us[i1] + t * (us[i2] - us[i1]),
                                ss[j1] + t * (ss[j2] - ss[j1]),
                            )
                        )
                if len(pts) >= 2:
                    (u1, s1), (u2, s2) = pts[0], pts[1]
                    um, sm = 0.5 * (u1 + u2), 0.5 * (s1 + s2)
                    f = f_metric(float(max(um, 0.0)), float(math.pi / 4 + sm), ell0)
                    length += math.sqrt((u2 - u1) ** 2 + f * f * (s2 - s1) ** 2)
                    nseg += 1
        rows.append(
            {
                "eps": eps,
                "L": length,
                "L_over_eps": length / eps,
                "nseg": float(nseg),
                "pi": math.pi,
                "two_pi": 2.0 * math.pi,
            }
        )
    return rows


def report() -> Dict[str, object]:
    ratios = metric_circle_ratio_around_node()
    return {
        "tip_length_unit": tip_circle_length(1.0),
        "complete_curvature": total_curvature_complete(),
        "int_abs_K_complete": 2.0 * math.pi,
        "K_nonpositive": K_is_nonpositive_sample(),
        "old_K_max_claim": old_K_max_claim_fails(),
        "max_abs_K_at_u=0.5": {
            "exact": max_abs_K_at_u(0.5),
            "numerical": numerical_max_abs_K(0.5),
        },
        "inner_I_to_zero": {
            "I(1e-6)": boundary_integral_u_over_f(1e-6),
            "I(1e-8)": boundary_integral_u_over_f(1e-8),
        },
        "local_L1_mass_R=0.05": {
            "analytic_half_disk": local_abs_K_mass_bound(0.05),
            "numerical_box_0.05": numerical_abs_K_mass_box(0.05, 0.05),
        },
        "area_u_le_0.01": tip_neighbourhood_area(0.01),
        "area_over_a_at_0.01": tip_neighbourhood_area(0.01) / 0.01,
        "aps_along_cuts": inner_aps_kernel_along_cuts(),
        "metric_circle_ratios": ratios,
        "verdicts": {
            "singularity_type": (
                "geodesic boundary circle of length 8ℓ0 with four C^∞ "
                "metric-degeneracy points; not a cone, not an incomplete edge"
            ),
            "K_max_claim": "the global bound |K|≤1/(4ℓ0²) is false; |K| is unbounded and L¹",
            "Dirac_ESA": "failed (manifold with boundary at finite distance); APS/Friedrichs needed",
            "index_3_from_the_tip": (
                "failed as a derivation: every positive-cut APS index is 0, "
                "there is no spectral flow, and no Cheeger cone correction applies; "
                "an extension with index 3 would be put in by hand"
            ),
            "conical_heat_kernel_term": (
                "not applicable; regular-tip k_g=0; no invented node coefficients"
            ),
        },
    }


if __name__ == "__main__":
    import json

    r = report()
    # compact
    out = {k: v for k, v in r.items() if k != "metric_circle_ratios"}
    out["L_over_eps"] = [row["L_over_eps"] for row in r["metric_circle_ratios"]]
    print(json.dumps(out, indent=2, default=str))
