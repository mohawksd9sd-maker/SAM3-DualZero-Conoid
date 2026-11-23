"""Tests for the SAM-2 / math-model / May-clone Dual-Zero review (doc 51).

These tests do not lock any new core theorem.  They check statements used
in the review, not Standard-Model numerics.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "experiments" / "sam2_review"
if str(PKG) not in sys.path:
    sys.path.insert(0, str(PKG))

from regulator_checks import (  # noqa: E402
    A5_ICOSAHEDRON_PERM12,
    A5_ORDER,
    PAPER07_IRREP_DIMS,
    PAPER07_PERM12,
    TWO_I_IRREP_DIMS,
    TWO_I_ORDER,
    alpha_formula_is_not_unique,
    division_10_over_3_is_exact_in_Q,
    e8_adjoint_casimir_quadratic,
    epsilon_decays_faster_than_exponential,
    epsilon_is_never_zero,
    epsilon_n,
    epsilon_weighting_fails_weyl,
    even_filter_collapses_sam2_dual_zero,
    icosahedron_vertices_are_not_three,
    paper07_dims_sum_of_squares_wrong,
    paper07_perm12_is_not_icosahedron_a5,
    reg2_symmetric,
    reg2_symmetric_recovers_smooth_value,
    repeating_nine_equals_one,
    sam2_dual_zero_term,
    sam2_reg2_not_a_homomorphism,
    sam2_sequence_converges_to_zero,
    sum_of_squares,
    two_i_dims_sum_of_squares_ok,
)


def test_may_epsilon_never_vanishes_and_decays():
    assert epsilon_n(1) == -1.0
    assert epsilon_n(2) == 0.25
    assert epsilon_is_never_zero()
    assert epsilon_decays_faster_than_exponential()


def test_sam2_sequence_is_a_null_sequence_and_collapses_on_evens():
    assert sam2_dual_zero_term(1) == 0.0
    assert sam2_dual_zero_term(2) == -0.5
    assert sam2_dual_zero_term(4) == -0.25
    assert sam2_sequence_converges_to_zero()
    # Every even term is nonzero, every odd term is zero; a filter
    # containing the evens therefore identifies [0,-0] with 0.
    assert even_filter_collapses_sam2_dual_zero()
    evens_nonzero = all(sam2_dual_zero_term(n) != 0.0 for n in range(2, 80, 2))
    odds_zero = all(sam2_dual_zero_term(n) == 0.0 for n in range(1, 80, 2))
    assert evens_nonzero and odds_zero


def test_ten_over_three_is_exact_in_the_rationals():
    assert division_10_over_3_is_exact_in_Q()
    assert repeating_nine_equals_one()


def test_sam2_piecewise_reg2_is_not_a_homomorphism():
    assert sam2_reg2_not_a_homomorphism()


def test_symmetric_reg2_recovers_smooth_values():
    assert reg2_symmetric_recovers_smooth_value()
    # At a point of continuity the delta → 0 limit is the function itself
    # when there is no jump; a jump would be averaged.
    def step(x: float) -> float:
        return 1.0 if x >= 0 else -1.0

    assert reg2_symmetric(step, 0.0, 1e-3) == 0.0


def test_epsilon_as_heat_trace_weight_fails_weyl():
    out = epsilon_weighting_fails_weyl(t=1e-4)
    assert out["unweighted_tracks_weyl"] is True
    assert out["weighted_fails_weyl"] is True


def test_e8_adjoint_casimir_is_30_not_0_05():
    assert e8_adjoint_casimir_quadratic() == 30
    assert e8_adjoint_casimir_quadratic() != 0.05


def test_two_i_character_table_constraints():
    assert two_i_dims_sum_of_squares_ok()
    assert sum_of_squares(TWO_I_IRREP_DIMS) == TWO_I_ORDER
    # May Paper 07 omitted a 4 and does not sum to |2I|.
    assert paper07_dims_sum_of_squares_wrong()
    assert sum_of_squares(PAPER07_IRREP_DIMS) == 104
    # The claimed 12 = 1⊕2⊕2⊕3⊕4 is not the A5 permutation representation
    # on the 12 icosahedron vertices, which is 1⊕3⊕3⊕5.
    assert paper07_perm12_is_not_icosahedron_a5()
    assert sum(A5_ICOSAHEDRON_PERM12) == 12
    assert sum(PAPER07_PERM12) == 12
    assert icosahedron_vertices_are_not_three()
    # A5 has no 2-dimensional complex irrep (sum of squares of the
    # standard irreps 1,3,3,4,5 is 60).
    assert sum_of_squares((1, 3, 3, 4, 5)) == A5_ORDER


def test_alpha_running_inputs_move_the_output():
    out = alpha_formula_is_not_unique()
    assert out["beta_changes_f"] > 1e-6
    assert out["gut_changes_f"] > 1e-6
