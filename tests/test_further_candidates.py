"""Tests for the exploratory further-candidate survey (doc 50).

These tests do not lock any new core theorem.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "experiments" / "further_candidates"
if str(PKG) not in sys.path:
    sys.path.insert(0, str(PKG))

from coincidences import TARGETS, classify, source_constants  # noqa: E402
from euler_orbifolds import (  # noqa: E402
    dhvw_T6_Z2xZ2,
    dhvw_T6_Z3,
    flux_products_equal_to,
    standard_orbifold_census,
)
from spectral_action_moduli import (  # noqa: E402
    C0,
    INT_R_COMPLETE,
    dS_dM_sign_term,
    stationary_A_at_fixed_M,
)
from tadpole_enum import intersection, search_one_stack, tadpoles, tadpoles_ok  # noqa: E402
from zn_orbifolds import (  # noqa: E402
    z2_counts,
    z2_literature,
    z3_invariant,
    z3_literature_even,
    z6_literature,
)


# --- Euler / Hodge -------------------------------------------------------------

def test_dhvw_Z3_is_72():
    out = dhvw_T6_Z3()
    assert out["chi"] == 72
    assert out["generations_chi_over_2"] == 36


def test_dhvw_Z2xZ2_is_96():
    out = dhvw_T6_Z2xZ2()
    assert out["chi"] == 96
    assert out["generations_chi_over_2"] == 48


def test_standard_orbifold_table_has_no_three_generations():
    census = standard_orbifold_census()
    assert census["any_with_exactly_3_generations"] is False
    assert census["smallest_generation_count"] == 24
    # Every Z4 in the table is C4-compatible and has 24 generations.
    for row in census["c4_compatible_rows"]:
        if row["name"] == "Z4":
            assert row["generations"] == 24
            assert row["chi"] == 48
    # Spot-check Z3 Hodge: (36, 0), χ=72.
    z3 = next(r for r in census["rows"] if r["name"] == "Z3")
    assert z3["h11"] == 36 and z3["h21"] == 0 and z3["chi"] == 72


def test_flux_product_3_only_if_a_three_is_present():
    sols = flux_products_equal_to(3, M_max=10)
    assert sols == [(1, 1, 3)]
    # And 3 is never forced by taking only 1s.
    assert flux_products_equal_to(1, M_max=10) == [(1, 1, 1)]


# --- Z_N counts ----------------------------------------------------------------

def test_z2_counts_match_kobayashi_nagamoto_table_1():
    for M in range(1, 25):
        assert z2_counts(M) == z2_literature(M)
        assert sum(z2_counts(M).values()) == M


def test_z2_invariant_3_first_at_M_4_not_at_minimal_flux():
    assert z2_counts(1)["+1"] == 1
    assert z2_counts(3)["+1"] == 2
    assert [M for M in range(1, 13) if z2_counts(M)["+1"] == 3] == [4, 5]


def test_z3_even_invariant_and_table_5():
    # M=6: n=1, r=0 → inv 3, ω 2, ωbar 1
    assert z3_literature_even(6) == {"+1": 3, "omega": 2, "omega_bar": 1}
    assert z3_invariant(6) == 3
    assert z3_invariant(8) == 3
    assert z3_invariant(10) == 3
    # Exception to floor(M/3)+1: at M=4=6*0+4, floor(4/3)+1=2, but I^(3)=1.
    assert z3_invariant(4) == 1
    assert 4 // 3 + 1 == 2
    # Smallest positive even flux is M=2, invariant 1, not 3.
    assert z3_literature_even(2)["+1"] == 1


def test_z6_formula_sums_to_M_for_even_M():
    for M in range(2, 31, 2):
        counts = z6_literature(M)
        assert all(v >= 0 for v in counts.values()), (M, counts)
        assert sum(counts.values()) == M
    # Invariant 3 first at M=12 (floor(12/6)+1=3), a range 12..17.
    assert z6_literature(2)["+1"] == 1
    assert [M for M in range(2, 25, 2) if z6_literature(M)["+1"] == 3] == [12, 14, 16]


# --- Tadpoles ------------------------------------------------------------------

def test_tadpole_arithmetic_and_intersection_on_a_hand_example():
    # A filler D9 of multiplicity 16: (16; 1,1,1; 0,0,0) gives tadpole (16,0,0,0), not a solution.
    filler = (16, 1, 1, 1, 0, 0, 0)
    assert tadpoles([filler]) == (16, 0, 0, 0)
    assert tadpoles_ok([filler]) is False
    # Intersection of two 'trivial' flux-free stacks vanishes.
    a = (1, 1, 1, 1, 0, 0, 0)
    b = (1, 1, 1, 1, 0, 0, 0)
    assert intersection(a, b) == 0
    # A single unit of flux on one torus: I = 0 still, because two of the three factors vanish.
    c = (1, 1, 1, 1, 1, 0, 0)
    assert intersection(a, c) == 0


def test_no_one_stack_solution_at_small_wrapping():
    out = search_one_stack(wrap_max=3, N_candidates=(1, 2, 4, 8, 16))
    assert out["n_solutions"] == 0


# --- Spectral action -----------------------------------------------------------

def test_C0_and_complete_curvature_match_locked_values():
    assert abs(C0 - 2 * math.pi * math.log(2.0)) < 1e-15
    assert abs(INT_R_COMPLETE + 4 * math.pi) < 1e-15


def test_flux_derivative_vanishes_only_at_M_0():
    for A in (0.5, 1.0, 7.0):
        assert abs(dS_dM_sign_term(A, 0, area_X=3.0, f0=1.0)) < 1e-15
        assert dS_dM_sign_term(A, 3, area_X=3.0, f0=1.0) != 0.0


def test_stationary_area_is_proportional_to_abs_M_when_it_exists():
    # With all coefficients +1, Λ=1, area_X=C0, L=8, a stationary A may or
    # may not exist (depends on the sign of B).  If it exists for M=1 and
    # M=3, the ratio must be 3.
    A1 = stationary_A_at_fixed_M(1, 1.0, 1.0, 1.0, 1.0, 1.0, C0, 8.0)
    A3 = stationary_A_at_fixed_M(3, 1.0, 1.0, 1.0, 1.0, 1.0, C0, 8.0)
    if A1 is not None and A3 is not None:
        assert abs(A3 / A1 - 3.0) < 1e-12
    # M=0 is never a critical point in A (linear action).
    assert stationary_A_at_fixed_M(0, 1.0, 1.0, 1.0, 1.0, 1.0, C0, 8.0) is None


# --- Coincidences --------------------------------------------------------------

def test_coincidence_sources_are_the_declared_constants():
    s = source_constants()
    assert abs(s["C0"] - 2 * math.pi * math.log(2.0)) < 1e-15
    assert s["tip_over_ell0"] == 8.0
    assert s["n_nodes"] == 4.0
    # 13 is not a source.
    assert "13" not in s and "four_thirteenths" not in s
    # F(ρ) > F(i), as computed independently in doc 49.
    assert s["F_rho"] > s["F_i"]


def test_classify_thresholds():
    assert classify(0.927, 0.927, "omega0_quoted") == "abs_hit_on_3_digit_target"
    assert classify(3.0, 3.0, "three") == "rel_hit_0.5pct"
    assert classify(1.0, 3.0, "three") == "no"
    assert "four_thirteenths" in TARGETS
