"""Tests for the exploratory missing-principle survey.

These tests do not lock any new core theorem.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "experiments" / "missing_principle"
if str(PKG) not in sys.path:
    sys.path.insert(0, str(PKG))

from c4_equivariant import (  # noqa: E402
    character_indices,
    has_fixed_point,
    nodes_cycled_by_generator,
)
from kronecker_det import (  # noqa: E402
    F,
    TAU_I,
    TAU_RHO,
    TAU_RHO_RIGHT,
    dedekind_eta,
    in_fundamental_domain,
    modular_invariance_errors,
    scan_fundamental_domain,
)
from magnetized_det import (  # noqa: E402
    area_that_places_stationary_at,
    best_integer_at_area,
    continuous_stationary_M,
    log_det_abs_D,
    zeta_D2,
    zeta_D2_from_levels,
    zeta_D2_prime_at_0,
)
from z4_orbifold import (  # noqa: E402
    _fourth_power_error,
    _unitarity_error,
    literature_counts_alpha0,
    s_matrix,
    sector_counts,
)


# --- Kronecker / det' on flat tori -------------------------------------------------

def test_eta_positive_imaginary_and_known_size_at_i():
    # |η(i)| is a classical constant, approximately 0.7682254223262603
    eta_i = abs(dedekind_eta(TAU_I))
    assert abs(eta_i - 0.7682254223262603) < 1e-12


def test_F_is_modular_invariant():
    err = modular_invariance_errors(0.2 + 1.4j)
    assert err["abs_F_minus_F_T"] < 1e-12
    assert err["abs_F_minus_F_S"] < 1e-12


def test_hexagonal_points_are_in_the_fundamental_domain_or_its_edge():
    assert in_fundamental_domain(TAU_RHO)
    assert in_fundamental_domain(TAU_RHO_RIGHT)
    assert in_fundamental_domain(TAU_I)


def test_F_larger_at_hexagonal_than_at_square():
    assert F(TAU_RHO) > F(TAU_I)
    assert abs(F(TAU_RHO) - F(TAU_RHO_RIGHT)) < 1e-12


def test_grid_maximum_is_at_the_hexagonal_point():
    scan = scan_fundamental_domain()
    # The grid includes the two hexagonal vertices (x=±1/2, y=√3/2).
    d_left = math.hypot(scan["tau_max_re"] - TAU_RHO.real, scan["tau_max_im"] - TAU_RHO.imag)
    d_right = math.hypot(
        scan["tau_max_re"] - TAU_RHO_RIGHT.real,
        scan["tau_max_im"] - TAU_RHO_RIGHT.imag,
    )
    assert min(d_left, d_right) < 0.05
    assert scan["F_max_minus_F_rho"] < 1e-10
    # Among rectangular tori the grid maximum should sit at the square.
    assert abs(scan["y_rect_max"] - 1.0) < 0.05
    assert abs(scan["F_rect_max"] - F(TAU_I)) < 1e-8


# --- Magnetized Dirac determinant --------------------------------------------------

def test_zeta_D2_matches_truncated_landau_sum():
    M, A, s = 3, 2.0, 2.0
    exact = zeta_D2(s, M, A)
    partial = zeta_D2_from_levels(s, M, A, nmax=20000)
    assert abs(exact - partial) / abs(exact) < 1e-4


def test_closed_form_zeta_prime_at_zero():
    M, A = 3, 5.0
    # Independent evaluation of ζ'_{D²}(0) from the formula
    # 2M [ -log(4π M/A) ζ(0) + ζ'(0) ] and the closed value M log(2M/A).
    zeta0 = -0.5
    zeta_prime0 = -0.5 * math.log(2.0 * math.pi)
    from_factors = 2 * M * (-math.log(4 * math.pi * M / A) * zeta0 + zeta_prime0)
    assert abs(from_factors - zeta_D2_prime_at_0(M, A)) < 1e-12
    assert abs(from_factors - M * math.log(2 * M / A)) < 1e-12


def test_stationary_point_is_area_over_2e():
    A = 12.0
    assert abs(continuous_stationary_M(A) - A / (2 * math.e)) < 1e-15
    # The second-derivative test: log det is smaller at the nearest integers
    # than far away, and the area that places the stationary point at 3
    # has best integer 3.
    A3 = area_that_places_stationary_at(3)
    assert abs(A3 - 6 * math.e) < 1e-12
    M_star, _ = best_integer_at_area(A3)
    assert M_star == 3
    # At unit area the preferred integer is 1, not 3.
    M1, _ = best_integer_at_area(1.0)
    assert M1 == 1
    # Jointly in (M, A), moving A at fixed M always changes log det:
    # there is no interior critical point of log det'|D| alone.
    assert log_det_abs_D(3, 10.0) != log_det_abs_D(3, 11.0)


# --- Z4 orbifold counts ------------------------------------------------------------

def test_s_matrix_is_unitary_and_has_order_four():
    for M in (1, 2, 3, 4, 5, 7, 8, 9, 12, 16):
        C = s_matrix(M)
        assert _unitarity_error(C) < 1e-12
        assert _fourth_power_error(C) < 1e-12


def test_sector_counts_match_kobayashi_nagamoto_table_iii():
    for M in range(1, 25):
        assert sector_counts(M) == literature_counts_alpha0(M)
        # And they add up to M.
        assert sum(sector_counts(M).values()) == M


def test_invariant_sector_has_dimension_3_exactly_for_M_8_through_11():
    have_three = [M for M in range(1, 25) if sector_counts(M)["+1"] == 3]
    assert have_three == [8, 9, 10, 11]
    # The invariant count is floor(M/4)+1, so M=0 is not in the list,
    # and M=3 gives one invariant mode, not three.
    assert sector_counts(3)["+1"] == 1
    assert sector_counts(4)["+1"] == 2


# --- C4-equivariant index on the conoid -------------------------------------------

def test_c4_action_is_free_away_from_the_identity():
    assert has_fixed_point(0) is True
    assert has_fixed_point(1) is False
    assert has_fixed_point(2) is False
    assert has_fixed_point(3) is False
    assert has_fixed_point(5) is False


def test_nodes_form_a_4_cycle():
    images = nodes_cycled_by_generator()
    assert sorted(images) == [0, 1, 2, 3]
    assert len(set(images)) == 4


def test_every_character_index_vanishes():
    chars = character_indices()
    assert chars == {"+1": 0, "+i": 0, "-1": 0, "-i": 0}
