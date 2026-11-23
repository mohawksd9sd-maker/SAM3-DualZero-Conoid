"""Riemann-Roch and twisted-Dirac index on compact Riemann surfaces.

Exploratory: not part of the locked SAM-3 core.

Standard facts used (not re-derived here):

- Riemann-Roch: for a holomorphic line bundle L of degree d on a compact
  Riemann surface of genus g,
      chi(L) := dim H^0(L) - dim H^1(L) = d + 1 - g.
  This is the holomorphic Euler characteristic, not automatically the
  spin-Dirac index.  Textbook statement: e.g. Farkas-Kra, or Hartshorne,
  Algebraic Geometry, Ch. IV.

- Spin Dirac: a spin structure is a theta characteristic S, i.e. a line
  bundle with S tensor S = K (canonical bundle), so deg(S) = g - 1.
  The index of the Dirac operator twisted by a holomorphic line bundle E
  of degree d is
      chi(S tensor E) = deg(S tensor E) + 1 - g = (g - 1 + d) + 1 - g = d.
  So the chiral index equals the degree (the flux), independently of genus.

The number 3 is a choice of degree, not an output of the topology of a
given surface.  No compact surface (orientable or not, with or without
boundary) has Euler characteristic 3; the maximum is 2 (the sphere).
"""

from __future__ import annotations

import math
from typing import Dict, List, Tuple


def holomorphic_chi(genus: int, degree: int) -> int:
    """chi(L) = deg(L) + 1 - g."""
    if genus < 0:
        raise ValueError("genus must be >= 0")
    return int(degree + 1 - genus)


def dirac_index(degree: int, genus: int = 0) -> int:
    """Index of the spin Dirac operator twisted by a line bundle of degree d.

    Equals d, independently of genus (see module docstring).
    The unused genus argument is kept so call sites can be explicit.
    """
    _ = genus
    return int(degree)


def euler_characteristic_orientable(genus: int, n_boundary: int = 0) -> int:
    """chi = 2 - 2g - b for a compact orientable surface with b boundary circles."""
    if genus < 0 or n_boundary < 0:
        raise ValueError("genus and boundary count must be >= 0")
    return 2 - 2 * genus - n_boundary


def euler_characteristic_nonorientable(crosscaps: int, n_boundary: int = 0) -> int:
    """chi = 2 - k - b for a compact non-orientable surface with k >= 1 crosscaps."""
    if crosscaps < 1 or n_boundary < 0:
        raise ValueError("need k >= 1 crosscaps and b >= 0")
    return 2 - crosscaps - n_boundary


def compact_surface_chi_cannot_be(target: int) -> Dict[str, object]:
    """No compact 2-manifold (possibly with boundary, possibly non-orientable)
    has Euler characteristic larger than 2.  In particular chi = 3 is
    impossible, including for disconnected compact surfaces only if one
    allows a disjoint union whose chi adds to 3 (e.g. sphere ⊔ disk),
    which is not a connected spacetime factor and is not used here.
    """
    # Connected case: chi <= 2, with equality only for the sphere.
    # Orientable: 2 - 2g - b <= 2, equals 3 only if -2g - b = 1, impossible
    # for integers g,b >= 0.
    # Non-orientable: 2 - k - b <= 1 (k >= 1), never 3.
    return {
        "target": target,
        "max_chi_connected_compact": 2,
        "achieved_by": "the 2-sphere (g=0, no boundary)",
        "connected_surface_can_have_chi": target <= 2,
        "orientable_obstruction": (
            "2 - 2g - b = 3 iff -2g - b = 1, impossible for integers g,b >= 0"
        ),
        "nonorientable_obstruction": (
            "2 - k - b <= 1 for k >= 1, never 3"
        ),
        "disconnected_numerology": (
            "A disjoint union can have chi=3 (sphere ⊔ disk), but that is "
            "not a connected base and is not a derivation of three generations."
        ),
        "verdict": "dead end" if target == 3 else (
            "possible" if target <= 2 else "impossible for a connected compact surface"
        ),
    }


def pairs_with_dirac_index(target: int, max_genus: int = 6) -> List[Tuple[int, int]]:
    """All (g, d) with 0 <= g <= max_genus and Dirac index d = target."""
    return [(g, target) for g in range(max_genus + 1)]


def pairs_with_holomorphic_chi(target: int, max_genus: int = 6) -> List[Tuple[int, int]]:
    """All (g, d) with chi(L) = d + 1 - g = target, for 0 <= g <= max_genus.

    In particular the sphere (g=0) with d=2 has chi=3: these are the three
    holomorphic sections of O(2) = TS^2, i.e. the conformal Killing fields
    of the sphere (the Lie algebra of PSL(2,C)).  That is a distinguished
    3, but those sections are vector fields, not chiral fermion zero modes
    of a Dirac operator (the Dirac index would be d=2, not 3).  Identifying
    them with generations is numerology.
    """
    return [(g, target - 1 + g) for g in range(max_genus + 1)]


def naturalness_of_three() -> Dict[str, object]:
    """Does any compact surface produce the integer 3 without a choice of flux?"""
    chi3 = compact_surface_chi_cannot_be(3)
    dirac_pairs = pairs_with_dirac_index(3)
    holo_pairs = pairs_with_holomorphic_chi(3)
    hopf = {
        "bundle": "O(1) on CP^1 (Hopf line bundle)",
        "degree": 1,
        "dirac_index": 1,
        "note": "The unique degree-1 positive line bundle on the sphere gives index 1, not 3.",
    }
    tangent = {
        "bundle": "O(2) = TS^2",
        "degree": 2,
        "dirac_index": 2,
        "holomorphic_chi": 3,
        "holomorphic_sections": "conformal Killing fields, not fermion generations",
        "flag": "numerology if sold as three generations",
    }
    return {
        "dirac_index_equals": "the degree d of the twisting bundle (flux)",
        "genus_drops_out_of_dirac_index": True,
        "pairs_dirac_index_3": dirac_pairs,
        "pairs_holomorphic_chi_3": holo_pairs,
        "euler_characteristic_3": chi3,
        "hopf_bundle": hopf,
        "sphere_O2": tangent,
        "three_is_a_choice_of_degree": True,
        "verdict": "neutral as a mechanism (index = flux is clean); dead end as a derivation of the number 3",
        "reason": (
            "The twisted-Dirac index on any compact Riemann surface equals the "
            "degree d of the twisting line bundle and is independent of genus.  "
            "Getting 3 means choosing d=3.  Nothing in the topology of a "
            "connected compact surface (Euler characteristic cannot be 3; the "
            "Hopf bundle has degree 1; TS^2 has degree 2) produces 3 as a "
            "Dirac index without that choice."
        ),
    }


def report() -> Dict[str, object]:
    n = naturalness_of_three()
    return {
        "exploratory": True,
        "locked_core": False,
        "holomorphic_chi_formula": "d + 1 - g",
        "dirac_index_formula": "d  (independent of genus)",
        "sample_chi": {
            "sphere_O0": holomorphic_chi(0, 0),
            "sphere_O1": holomorphic_chi(0, 1),
            "sphere_O2": holomorphic_chi(0, 2),
            "torus_degree_3": holomorphic_chi(1, 3),
            "genus2_degree_3": holomorphic_chi(2, 3),
        },
        "sample_dirac_index": {
            "sphere_untwisted_or_degree_0": dirac_index(0, 0),
            "sphere_degree_3": dirac_index(3, 0),
            "torus_degree_3": dirac_index(3, 1),
            "genus2_degree_3": dirac_index(3, 2),
        },
        "naturalness": n,
        "verdict": n["verdict"],
    }
