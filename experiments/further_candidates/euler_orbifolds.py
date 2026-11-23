"""Euler characteristics and generation counts for standard T^6 orbifolds, and flux products.

Exploratory: not part of the locked SAM-3 core.

Literature (fetched, not invented)
---------------------------------
- L. Dixon, J. A. Harvey, C. Vafa and E. Witten, "Strings on orbifolds",
  Nucl. Phys. B 261 (1985) 678–705.  The stringy Euler characteristic of an
  orbifold M/G is
      χ = (1/|G|) ∑_{g,h : gh=hg} χ(Fix(g) ∩ Fix(h)).
  For the Z-manifold T^6/Z_3 they obtain χ=72 and, with the spin connection
  embedded in the gauge group, 36 generations (χ/2).
- Hodge numbers of the standard abelian T^6 orbifolds (point group plus
  lattice) are taken from S. Reffert, hep-th/0609040, Tables 2.3–2.4, and
  the same table in Lüst–Reffert–Scheidegger–Stieberger, hep-th/0609014,
  Table 2.1.  For a Calabi–Yau threefold, χ = 2(h^{1,1} − h^{2,1}) and the
  net generation count with standard embedding is |χ|/2.
- The Tian–Yau three-generation manifold (a free Z_3 quotient of a
  complete-intersection Calabi–Yau with χ=−18, giving χ=−6) is a classical
  construction.  It is not a toroidal orbifold, and it is not computed
  from scratch here.  It is cited only as a known construction in a
  different programme.
- Magnetized T^2×T^2×T^2: the Dirac index of a line bundle with integer
  fluxes (M1, M2, M3) is M1 M2 M3 (product of the three two-torus indices).

The Z_3 DHVW sum and the Z_2×Z_2 DHVW sum are computed in this module
and checked against the classical values 72 and 96.  The other χ values
are computed from the published Hodge numbers, not re-derived.
"""

from __future__ import annotations

from typing import Dict, List, Tuple


def dhvw_T6_Z3() -> Dict[str, object]:
    """Stringy Euler characteristic of T^6/Z_3, computed from DHVW.

    The generator rotates each of three hexagonal tori by 2π/3.  Non-identity
    elements have 27 isolated fixed points.  All group elements commute, so
    the sum runs over all 9 pairs (g,h).
    """
    # χ(Fix(1) ∩ Fix(1)) = χ(T^6) = 0
    # χ(Fix(1) ∩ Fix(α^k)) = χ(Fix(α^k)) = 27 for k=1,2, and likewise
    # χ(Fix(α^j) ∩ Fix(α^k)) = 27 for j,k in {1,2}.
    pairs = {}
    elements = (0, 1, 2)

    def chi_fix(g: int, h: int) -> int:
        if g == 0 and h == 0:
            return 0
        return 27

    total = 0
    for g in elements:
        for h in elements:
            val = chi_fix(g, h)
            pairs[f"({g},{h})"] = val
            total += val
    chi = total / 3
    return {
        "group": "Z3",
        "sum_of_pair_contributions": total,
        "chi": chi,
        "generations_chi_over_2": abs(chi) / 2,
        "fixed_points_of_nonidentity": 27,
        "matches_Dixon_et_al_72": chi == 72,
    }


def dhvw_T6_Z2xZ2() -> Dict[str, object]:
    """Stringy Euler characteristic of the standard T^6/(Z_2×Z_2).

    Generators: θ1: (z1,z2,z3)→(z1,−z2,−z3) and cyclic.  Each non-identity
    element fixes 16 copies of a T^2, which has Euler characteristic 0.
    The intersection of two distinct non-identity elements is 4³=64 points.
    """

    def chi_fix(g: int, h: int) -> int:
        # 0 = identity, 1,2,3 = the three non-identity elements.
        if g == 0 or h == 0:
            # Fix(1)=T^6, χ=0; Fix(θi)=16 T^2, χ=0; intersection with 1 is the same.
            return 0
        if g == h:
            return 0
        return 64

    total = 0
    for g in range(4):
        for h in range(4):
            total += chi_fix(g, h)
    chi = total / 4
    return {
        "group": "Z2xZ2",
        "sum_of_pair_contributions": total,
        "chi": chi,
        "generations_chi_over_2": abs(chi) / 2,
        "matches_classical_96": chi == 96,
    }


# Hodge numbers (h11_untw, h21_untw, h11_twist, h21_twist) from
# Reffert hep-th/0609040, Tables 2.3–2.4 / LRSS hep-th/0609014, Table 2.1.
# C4-compatible means the point group contains a Z4 factor, so at least
# one T^2 must admit a Z4 rotation and therefore have τ=i.
REFFERT_HODGE: List[Dict[str, object]] = [
    {"name": "Z3", "lattice": "SU(3)^3", "h": (9, 0, 27, 0), "c4_compatible": False},
    {"name": "Z4", "lattice": "SU(4)^2", "h": (5, 1, 20, 0), "c4_compatible": True},
    {"name": "Z4", "lattice": "SU(2) x SU(4) x SO(5)", "h": (5, 1, 22, 2), "c4_compatible": True},
    {"name": "Z4", "lattice": "SU(2)^2 x SO(5)^2", "h": (5, 1, 26, 6), "c4_compatible": True},
    {"name": "Z6-I", "lattice": "(G2 x SU(3)^2)", "h": (5, 0, 20, 1), "c4_compatible": False},
    {"name": "Z6-I", "lattice": "SU(3) x G2^2", "h": (5, 0, 24, 5), "c4_compatible": False},
    {"name": "Z6-II", "lattice": "SU(2) x SU(6)", "h": (3, 1, 22, 0), "c4_compatible": False},
    {"name": "Z6-II", "lattice": "SU(3) x SO(8)", "h": (3, 1, 26, 4), "c4_compatible": False},
    {"name": "Z6-II", "lattice": "(SU(2)^2 x SU(3) x SU(3))", "h": (3, 1, 28, 6), "c4_compatible": False},
    {"name": "Z6-II", "lattice": "SU(2)^2 x SU(3) x G2", "h": (3, 1, 32, 10), "c4_compatible": False},
    {"name": "Z7", "lattice": "SU(7)", "h": (3, 0, 21, 0), "c4_compatible": False},
    {"name": "Z8-I", "lattice": "(SU(4) x SU(4))", "h": (3, 0, 21, 0), "c4_compatible": True},
    {"name": "Z8-I", "lattice": "SO(5) x SO(9)", "h": (3, 0, 24, 3), "c4_compatible": True},
    {"name": "Z8-II", "lattice": "SU(2) x SO(10)", "h": (3, 1, 24, 2), "c4_compatible": True},
    {"name": "Z8-II", "lattice": "SO(4) x SO(9)", "h": (3, 1, 28, 6), "c4_compatible": True},
    {"name": "Z12-I", "lattice": "E6", "h": (3, 0, 22, 1), "c4_compatible": True},
    {"name": "Z12-I", "lattice": "SU(3) x F4", "h": (3, 0, 26, 5), "c4_compatible": True},
    {"name": "Z12-II", "lattice": "SO(4) x F4", "h": (3, 1, 28, 6), "c4_compatible": True},
    {"name": "Z2xZ2", "lattice": "SU(2)^6", "h": (3, 3, 48, 0), "c4_compatible": False},
    {"name": "Z2xZ4", "lattice": "SU(2)^2 x SO(5)^2", "h": (3, 1, 58, 0), "c4_compatible": True},
    {"name": "Z2xZ6", "lattice": "SU(2)^2 x SU(3) x G2", "h": (3, 1, 48, 2), "c4_compatible": False},
    {"name": "Z2xZ6'", "lattice": "SU(3) x G2^2", "h": (3, 0, 33, 0), "c4_compatible": False},
    {"name": "Z3xZ3", "lattice": "SU(3)^3", "h": (3, 0, 81, 0), "c4_compatible": False},
    {"name": "Z3xZ6", "lattice": "SU(3) x G2^2", "h": (3, 0, 70, 1), "c4_compatible": False},
    {"name": "Z4xZ4", "lattice": "SO(5)^3", "h": (3, 0, 87, 0), "c4_compatible": True},
    {"name": "Z6xZ6", "lattice": "G2^3", "h": (3, 0, 81, 0), "c4_compatible": False},
]


def hodge_row(entry: Dict[str, object]) -> Dict[str, object]:
    u11, u21, t11, t21 = entry["h"]
    h11 = u11 + t11
    h21 = u21 + t21
    chi = 2 * (h11 - h21)
    return {
        "name": entry["name"],
        "lattice": entry["lattice"],
        "h11": h11,
        "h21": h21,
        "chi": chi,
        "generations": abs(chi) // 2,
        "c4_compatible": entry["c4_compatible"],
    }


def standard_orbifold_census() -> Dict[str, object]:
    rows = [hodge_row(e) for e in REFFERT_HODGE]
    gens = sorted({r["generations"] for r in rows})
    three = [r for r in rows if r["generations"] == 3]
    c4 = [r for r in rows if r["c4_compatible"]]
    c4_gens = sorted({r["generations"] for r in c4})
    return {
        "n_orbifolds_in_table": len(rows),
        "generation_values_present": gens,
        "any_with_exactly_3_generations": len(three) > 0,
        "those_with_3": three,
        "c4_compatible_generation_values": c4_gens,
        "c4_compatible_rows": c4,
        "smallest_generation_count": min(gens),
        "rows": rows,
    }


def flux_products_equal_to(target: int, M_max: int = 10) -> List[Tuple[int, int, int]]:
    """Positive integer fluxes with M1 M2 M3 = target, 1 ≤ Mi ≤ M_max, ordered."""
    out = []
    for a in range(1, M_max + 1):
        for b in range(a, M_max + 1):  # a ≤ b to cut permutations in the list of unordered types
            if target % (a * b) == 0:
                c = target // (a * b)
                if b <= c <= M_max:
                    out.append((a, b, c))
    return out


def report() -> Dict[str, object]:
    z3 = dhvw_T6_Z3()
    z22 = dhvw_T6_Z2xZ2()
    census = standard_orbifold_census()
    prods = flux_products_equal_to(3, M_max=10)
    return {
        "dhvw_Z3": z3,
        "dhvw_Z2xZ2": z22,
        "standard_abelian_census": {
            k: census[k]
            for k in (
                "n_orbifolds_in_table",
                "generation_values_present",
                "any_with_exactly_3_generations",
                "c4_compatible_generation_values",
                "smallest_generation_count",
            )
        },
        "c4_compatible_examples": [
            {"name": r["name"], "lattice": r["lattice"], "chi": r["chi"], "generations": r["generations"]}
            for r in census["c4_compatible_rows"]
        ],
        "Tian_Yau": {
            "chi": -6,
            "generations": 3,
            "source": "literature (free Z3 quotient of a CICY with chi=-18)",
            "uses_C4_or_the_conoid": False,
            "is_a_SAM3_derivation": False,
        },
        "magnetized_T2xT2xT2_index_equals_3": {
            "formula": "M1 M2 M3",
            "positive_solutions_up_to_order_M_le_10": prods,
            "forced_by_geometry": False,
            "note": "The only solutions are permutations of (1,1,3); the 3 is an input.",
        },
        "verdict": (
            "No standard abelian T^6 orbifold in the Reffert/LRSS table has "
            "|chi|/2 = 3 (the smallest value in the table is 24).  The "
            "C4-compatible Z4, Z8, Z12 and Z2xZ4, Z4xZ4 entries all give 24, "
            "60 or 90, not 3.  Direct DHVW sums give chi=72 for T^6/Z3 (36 "
            "generations) and chi=96 for T^6/(Z2xZ2) (48 generations).  The "
            "Tian–Yau manifold does have three generations, but it is a "
            "different construction (a free Z3 quotient) and is not forced "
            "by the conoid or its C4.  A magnetized T^2×T^2×T^2 index equals "
            "3 only if one flux is already 3."
        ),
    }
