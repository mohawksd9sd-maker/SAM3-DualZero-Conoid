"""Product geometries: conoid × S^2 or × T^2 (with flux) to reach 4D.

Exploratory: not part of the locked SAM-3 core.  The KO-dimension
arithmetic reuses the same addition rule as code/almost_commutative_product.py
(doc 45).  The new question is whether the second factor, or the conoid
itself, fixes the flux that would give three generations.
"""

from __future__ import annotations

import math
from typing import Dict, List


def ko_dimension(*summands: int) -> int:
    return int(sum(summands) % 8)


CCM_KO_F = 6
CCM_TARGET_KO = 2  # 4D spacetime × F has 4+6=10 ≡ 2, the CCM fermionic setup


def option_table() -> List[Dict[str, object]]:
    rows = [
        {
            "name": "conoid × F",
            "continuous_dimension": 2,
            "ko": ko_dimension(2, CCM_KO_F),
            "ko_matches_CCM": ko_dimension(2, CCM_KO_F) == CCM_TARGET_KO,
            "heat_kernel_is_4D": False,
            "generation_mechanism": "none (untwisted conoid APS index is 0; N on F is an input)",
            "verdict": "dead end as a 4D unification model (doc 45)",
        },
        {
            "name": "4D manifold × F   (standard CCM)",
            "continuous_dimension": 4,
            "ko": ko_dimension(4, CCM_KO_F),
            "ko_matches_CCM": True,
            "heat_kernel_is_4D": True,
            "generation_mechanism": "N=3 is an input of F",
            "verdict": "the standard CCM setup; 3 is not derived (doc 45)",
        },
        {
            "name": "conoid × T^2 × F",
            "continuous_dimension": 4,
            "ko": ko_dimension(2, 2, CCM_KO_F),
            "ko_matches_CCM": ko_dimension(2, 2, CCM_KO_F) == CCM_TARGET_KO,
            "heat_kernel_is_4D": True,
            "generation_mechanism": (
                "If the T^2 factor carries an integer flux M, the Dirac index "
                "on T^2 is M.  Three generations means choosing M=3.  The "
                "conoid is then a spectator 2-factor (incomplete, with a "
                "geodesic tip boundary; doc 46) and does not determine M."
            ),
            "verdict": "promising as a 4D product that can host a flux; dead end as a derivation of the flux",
        },
        {
            "name": "conoid × S^2 × F",
            "continuous_dimension": 4,
            "ko": ko_dimension(2, 2, CCM_KO_F),
            "ko_matches_CCM": True,
            "heat_kernel_is_4D": True,
            "generation_mechanism": (
                "Twisted Dirac index on S^2 equals the degree of the line "
                "bundle.  The Hopf bundle O(1) has degree 1; TS^2 = O(2) has "
                "degree 2.  Degree 3 is again a choice.  The round metric on "
                "S^2 is unique up to scale, which is tidier than a torus "
                "modulus, but uniqueness of the metric does not uniquely "
                "select the bundle."
            ),
            "verdict": "neutral/promising as a 4D product; dead end as a derivation of degree 3",
        },
        {
            "name": "R^{1,3} × T^2_flux × F   (conoid dropped)",
            "continuous_dimension": "4 (spacetime) + 2 (internal surface)",
            "ko": "depends on how the T^2 is treated (Riemannian factor vs internal)",
            "ko_matches_CCM": "not the standard 4D × F setup; this is a 6D continuous geometry times F",
            "heat_kernel_is_4D": "no, unless T^2 is treated as a finite/internal factor and reduced",
            "generation_mechanism": "index = flux on T^2, with 3 chosen",
            "verdict": "standard magnetized-compactification mechanism; 3 is a choice; not a SAM-3 construction",
        },
    ]
    return rows


def what_fixes_the_flux() -> Dict[str, object]:
    """Candidates that might have selected M=3, with an honest status for each."""
    attempts = [
        {
            "attempt": "Dirac quantization",
            "gives": "M ∈ Z",
            "selects_3": False,
            "note": "The smallest positive integer is 1, not 3.",
        },
        {
            "attempt": "Conoid total curvature ∫ K dA = -2π, so |∫K| / 2π = 1",
            "gives": 1,
            "selects_3": False,
            "note": "If this were used as a flux, it would give index 1, not 3.  Treating it as a flux at all is already an extra identification, not forced by the product construction.",
        },
        {
            "attempt": "Four tip nodes, or C4, or 2n nodes of a frequency-n variant",
            "gives": "4, or 2n",
            "selects_3": False,
            "note": "Never 3 for integer n.  Using 4-1=3 or 12/4=3 is numerology.",
        },
        {
            "attempt": "Hopf bundle on the S^2 factor",
            "gives": 1,
            "selects_3": False,
            "note": "The distinguished positive line bundle on the sphere has degree 1.",
        },
        {
            "attempt": "Tangent bundle of the S^2 factor",
            "gives": 2,
            "selects_3": False,
            "note": "Dirac index 2.  The 3 holomorphic sections of O(2) are conformal Killing fields, not chiral generations (see riemann_roch.naturalness_of_three).",
        },
        {
            "attempt": "Anomaly cancellation or supersymmetry stability on a stack of magnetized branes",
            "gives": "linear constraints on a collection of fluxes, in models that are not uniquely fixed by the conoid",
            "selects_3": False,
            "note": "Such conditions can make M=3 consistent in some models, but they do not uniquely select it, and they are not derived from the locked embedding.",
        },
        {
            "attempt": "Minimality among fluxes that give at least three chiral zero modes",
            "gives": "M=3 is then the smallest integer >= 3",
            "selects_3": False,
            "note": "Circular: the target 'at least three' is the thing to be derived.",
        },
    ]
    return {
        "attempts": attempts,
        "any_attempt_selects_3": False,
        "verdict": "dead end",
        "reason": (
            "Every 4D product that can host three chiral zero modes does so "
            "by putting in an integer flux or degree equal to 3.  No "
            "geometric invariant of the locked conoid, and no distinguished "
            "bundle on S^2 or T^2, produces that integer."
        ),
    }


def report() -> Dict[str, object]:
    return {
        "exploratory": True,
        "locked_core": False,
        "options": option_table(),
        "flux": what_fixes_the_flux(),
        "ko_conoid_T2_F": ko_dimension(2, 2, 6),
        "ko_matches_CCM_fermions": ko_dimension(2, 2, 6) == 2,
        "verdict": (
            "promising as a way to reach a 4D heat kernel and the CCM "
            "KO-dimension (conoid × T^2 × F or conoid × S^2 × F); "
            "dead end as a derivation of the flux / generation count"
        ),
    }
