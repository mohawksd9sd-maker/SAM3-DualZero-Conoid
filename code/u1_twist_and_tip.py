"""Natural U(1) twists (index 3?) and the singular tip of the locked embedding.

U(1) twist
----------
The Falomir disk index is k+1 for k < κ ≤ k+1, so index 3 needs κ ∈ (2, 3].
A natural candidate 2-form on the conoid is the Gauss–Bonnet density K dA.
The complete-surface integral is ∫ K dA = −2π (conoid_heat_kernel), so the
dimensionless flux ∫ K dA / 2π equals −1, not a number in (2, 3].
The spin connection of the locked metric is already part of the untwisted
Dirac operator and is the geometric object whose curvature is K; using it
again as an auxiliary flux would be double-counting (doc 44).
The isometry group is C4; its irreducible characters are 4th roots of unity
and do not single out a holonomy in (2, 3].
Verdict: failed to derive a natural κ ∈ (2, 3].

Singular tip
------------
Locked embedding: r(u,v) = (u cos v, u sin v, ℓ0 sin(2v)).
For u>0 this is an embedding (u = √(x²+y²) is unique).  At u=0 the image
is the segment {0}×{0}×[−ℓ0, ℓ0] on the z-axis, covered more than once.
The four coordinate nodes v=π/4 + kπ/2, where f=0, map to the two
endpoints z=±ℓ0 (each with two preimages).  Along the open segment two
ruling lines cross (a self-intersection of the image in R³).  The abstract
metric on u>0 is smooth; degeneracy is only at u=0.

APS index of the *truncated* surface X_{a,b} is 0 for every a>0 (doc 44).
Cutting closer to the tip therefore cannot produce index 3.  The singular
space obtained by adding u=0 is not a smooth compact manifold with
boundary; the APS theorem as used in doc 44 does not apply to it, and we
do not invent an index for that space.
Verdict: partially analysed (geometry of the tip, and the a→0 limit of
the truncated index is 0); the singular-space index is not computed and
is not an index-3 theorem.
"""

from __future__ import annotations

import math
from typing import Dict, List, Tuple

import os
import sys

_CODE = os.path.dirname(os.path.abspath(__file__))
if _CODE not in sys.path:
    sys.path.insert(0, _CODE)

from aps_index_theorem import falomir_flux_for_index, product_collar_index  # noqa: E402
from aps_projection import analytic_disk_index  # noqa: E402
from conoid_heat_kernel import total_curvature_complete  # noqa: E402
from core_geometry import f_metric, tip_nodes  # noqa: E402


def embedding(u: float, v: float, ell0: float = 1.0) -> Tuple[float, float, float]:
    return (u * math.cos(v), u * math.sin(v), ell0 * math.sin(2.0 * v))


def flux_from_gauss_bonnet() -> Dict[str, object]:
    kappa = total_curvature_complete() / (2.0 * math.pi)  # −1
    return {
        "int_K": total_curvature_complete(),
        "kappa_if_K_is_the_field_strength": kappa,
        "in_interval_2_3": False,
        "falomir_index_if_this_kappa": analytic_disk_index(kappa) if kappa > -1e-12 else analytic_disk_index(kappa),
        "verdict": "failed",
        "reason": (
            "The only natural closed 2-form built from the metric curvature "
            "has flux −1, which is not in (2, 3].  The spin connection is "
            "already in the untwisted Dirac operator."
        ),
    }


def tip_geometry(ell0: float = 1.0) -> Dict[str, object]:
    nodes = tip_nodes(ell0)
    images = [embedding(0.0, v, ell0) for v in nodes]
    # endpoints z = ± ell0, each hit twice
    zs = [p[2] for p in images]
    return {
        "nodes_v": nodes,
        "images_at_u0": images,
        "endpoints_z": sorted(set(round(z, 12) for z in zs)),
        "each_endpoint_has_two_preimages": zs.count(ell0) == 2 and zs.count(-ell0) == 2,
        "f_at_nodes": [f_metric(0.0, v, ell0) for v in nodes],
        "segment_half_length": ell0,
    }


def truncated_index_independent_of_cut() -> Dict[str, object]:
    # The theorem is independent of a,b; this is a reminder, not a scan.
    apap = product_collar_index("antiperiodic", "antiperiodic")
    return {
        "index": apap["index"],
        "independent_of_a_b": True,
        "a_to_0_still_zero": True,
        "produces_index_3": False,
    }


def report() -> Dict[str, object]:
    flux = flux_from_gauss_bonnet()
    # Don't claim analytic_disk_index for negative κ unless the formula extends;
    # record the interval check only.
    target = falomir_flux_for_index(3)
    return {
        "flux": {
            "int_K_over_2pi": flux["kappa_if_K_is_the_field_strength"],
            "in_interval_2_3": False,
            "target_interval_for_index_3": target["kappa_interval_desc"],
            "verdict": flux["verdict"],
            "reason": flux["reason"],
        },
        "tip": tip_geometry(),
        "truncated_index": truncated_index_independent_of_cut(),
        "verdicts": {
            "natural_U1_flux_for_index_3": "failed",
            "singular_tip": (
                "partially derived: embedding and self-intersection described; "
                "APS index stays 0 for every a>0; singular-space index not computed"
            ),
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(report(), indent=2, default=str))
