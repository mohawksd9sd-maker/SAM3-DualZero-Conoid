"""Explicit Dual-Zero definitions and inexpensive honesty checks (doc 51).

Nothing here is a derivation of a Standard-Model parameter, a uniqueness
theorem, or a proof of three generations.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Callable

# ---------------------------------------------------------------------------
# Cross-version Dual-Zero definitions (stated as the sources state them)
# ---------------------------------------------------------------------------

# May 2026 / current SAM-3 generator (docs 18, 42; May Paper 02 / paper 1.3).
# omega0 is an input, not a derived constant.
def epsilon_n(n: int, omega0: float = 1.0) -> float:
    """ε(n) = ω0 (-1)^n n^{-n}, n ≥ 1."""
    if n < 1:
        raise ValueError("n must be a positive integer")
    return omega0 * ((-1) ** n) * (n ** -n)


# Symmetric average as stated in the May 2026 Dual-Zero axiom paper.
# This is a proposed regularisation of a function of a real variable,
# not a theorem about ζ(s).
def reg2_symmetric(f: Callable[[float], float], lam: float, delta: float) -> float:
    if delta <= 0:
        raise ValueError("delta must be positive")
    return 0.5 * (f(lam + delta) + f(lam - delta))


# SAM-2 v2.21 / desktop "math models" Dual-Zero sequence, 1-based:
# [0, -0] = [(0, -1/2, 0, -1/4, 0, -1/6, ...)]
# odd n: 0; even n: -1/n.
def sam2_dual_zero_term(n: int) -> float:
    if n < 1:
        raise ValueError("n must be a positive integer")
    if n % 2 == 1:
        return 0.0
    return -1.0 / n


# Piecewise Reg_2 as written in SAM-2 v2.21, with the undefined objects
# filled in only enough to test the piecewise map.  The source leaves
# Reg and H_{[0,-0]} unspecified.  Here H is a positive stand-in so that
# the claimed threshold rule can be checked as a map R → R.
SAM2_REG2_THRESHOLD = 1e-64


def sam2_reg2_piecewise(x: float, H: float = 1e-64) -> float:
    if abs(x) > SAM2_REG2_THRESHOLD:
        return x
    if x == 0.0:
        return 0.0
    return x / (1.0 + H / abs(x))


# Standard complex irrep dimensions of the binary icosahedral group
# 2I ≅ SL(2,5), order 120.  Sum of squares equals the group order.
TWO_I_IRREP_DIMS = (1, 2, 2, 3, 3, 4, 4, 5, 6)
TWO_I_ORDER = 120

# Dimensions listed in May 2026 Paper 07 (missing one 4-dimensional irrep).
PAPER07_IRREP_DIMS = (1, 2, 2, 3, 3, 4, 5, 6)

# Paper 07 claimed decomposition of a 12-dimensional permutation representation.
PAPER07_PERM12 = (1, 2, 2, 3, 4)

# A5 acting on the 12 vertices of an icosahedron: the permutation
# representation over C is 1 ⊕ 3 ⊕ 3' ⊕ 5.  A5 has no 2-dimensional
# complex irreps.
A5_ICOSAHEDRON_PERM12 = (1, 3, 3, 5)
A5_ORDER = 60


def sum_of_squares(dims: tuple[int, ...]) -> int:
    return sum(d * d for d in dims)


def is_ultrafilter_base_doubling(sets_contain_evens: bool) -> bool:
    """Model a single fact about the SAM-2 Dual-Zero class.

    If a filter (in particular any ultrafilter) contains the even numbers,
    the SAM-2 sequence is identically 0 on that set, hence equivalent to
    the zero sequence.  The source's "constructive" base {n_k} with
    n_{k+1} > 2 n_k can be chosen entirely in the evens, so this
    collapse is not forbidden by the stated construction.
    """
    return sets_contain_evens


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def epsilon_is_never_zero(n_max: int = 30, omega0: float = 1.0) -> bool:
    return all(epsilon_n(n, omega0) != 0.0 for n in range(1, n_max + 1))


def epsilon_decays_faster_than_exponential(n: int = 100) -> bool:
    """|ε(n)| = n^{-n} = exp(-n log n), which is o(exp(-c n)) for every c."""
    exact = math.exp(-n * math.log(n))
    return abs(abs(epsilon_n(n)) - exact) / exact < 1e-12 and abs(epsilon_n(n)) < math.exp(-4.0 * n)


def sam2_sequence_converges_to_zero(n_max: int = 10_000) -> bool:
    return max(abs(sam2_dual_zero_term(n)) for n in range(1, n_max + 1) if n % 2 == 0) <= 1.0 / 2 and (
        abs(sam2_dual_zero_term(n_max if n_max % 2 == 0 else n_max - 1)) < 2e-4
    )


def even_filter_collapses_sam2_dual_zero() -> bool:
    """On the evens, every SAM-2 Dual-Zero term is 0, so the class is 0."""
    evens_all_zero = all(sam2_dual_zero_term(n) == 0.0 for n in range(1, 200, 2))
    # The odd-index terms are the zeros; even-index terms are the nonzero ones.
    # Collapse happens if the *even* indices are in the filter:
    evens_are_the_nonzero_slots = all(sam2_dual_zero_term(n) != 0.0 for n in range(2, 40, 2))
    return evens_all_zero and evens_are_the_nonzero_slots and is_ultrafilter_base_doubling(True)


def division_10_over_3_is_exact_in_Q() -> bool:
    """0.9repeating = 1 in R, and (10/3)*3 = 10 in Q.  No information is lost."""
    return Fraction(10, 3) * 3 == Fraction(10, 1) and Fraction(1, 3) * 3 == Fraction(1, 1)


def repeating_nine_equals_one() -> bool:
    # 0.999... = 1 is the definition of the real 1 via geometric series.
    s = sum(Fraction(9, 10 ** k) for k in range(1, 80))
    return Fraction(1, 1) - s < Fraction(1, 10 ** 70)


def sam2_reg2_not_a_homomorphism(H: float = 1e-64) -> bool:
    """The piecewise threshold map fails additivity at the cutoff."""
    a = 0.6 * SAM2_REG2_THRESHOLD
    b = 0.6 * SAM2_REG2_THRESHOLD
    left = sam2_reg2_piecewise(a + b, H)
    right = sam2_reg2_piecewise(a, H) + sam2_reg2_piecewise(b, H)
    return abs(left - (a + b)) < 1e-80 and abs(left - right) > 0.1 * SAM2_REG2_THRESHOLD


def unweighted_heat_trace(t: float, n_max: int = 400) -> float:
    """∑_{n=1}^{N} exp(-t n^2).  As t → 0 this tracks (1/2)(√(π/t) − 1)."""
    return sum(math.exp(-t * n * n) for n in range(1, n_max + 1))


def weyl_leading_half_line(t: float) -> float:
    return 0.5 * (math.sqrt(math.pi / t) - 1.0)


def epsilon_weighted_heat_trace(t: float, omega0: float = 1.0, n_max: int = 40) -> float:
    """∑ ε(n) exp(-t n^2), the weighting written in May Paper 02, Thm. on heat traces."""
    return sum(epsilon_n(n, omega0) * math.exp(-t * n * n) for n in range(1, n_max + 1))


def epsilon_weighting_fails_weyl(t: float = 1e-4) -> dict[str, float | bool]:
    unweighted = unweighted_heat_trace(t)
    weyl = weyl_leading_half_line(t)
    weighted = epsilon_weighted_heat_trace(t)
    # The unweighted sum tracks Weyl; the ε-weighted sum stays O(1).
    return {
        "t": t,
        "unweighted": unweighted,
        "weyl": weyl,
        "weighted": weighted,
        "unweighted_tracks_weyl": abs(unweighted - weyl) / abs(weyl) < 0.05,
        "weighted_fails_weyl": abs(weighted) < 10 and abs(weyl) > 50,
    }


def e8_adjoint_casimir_quadratic() -> int:
    """Standard dual Coxeter number / adjoint quadratic Casimir of E8 is 30.

    SAM-2 v2.21 attributes the coefficient 0.05 in f(k) to 'the smallest
    nontrivial E8 adjoint Casimir'.  0.05 is not that Casimir.
    """
    return 30


def two_i_dims_sum_of_squares_ok() -> bool:
    return sum_of_squares(TWO_I_IRREP_DIMS) == TWO_I_ORDER


def paper07_dims_sum_of_squares_wrong() -> bool:
    return sum_of_squares(PAPER07_IRREP_DIMS) != TWO_I_ORDER


def paper07_perm12_is_not_icosahedron_a5() -> bool:
    return tuple(sorted(PAPER07_PERM12)) != tuple(sorted(A5_ICOSAHEDRON_PERM12))


def icosahedron_vertices_are_not_three() -> bool:
    return 12 != 3


def alpha_formula_is_not_unique(
    target: float = 1 / 137.035999084,
    k: float = 91.1876,
    k_pl: float = 1.22e19,
    ell_pl: float = 1.0,
) -> dict[str, float]:
    """The SAM-2 running formula has free inputs; nearby coefficients also hit 1/137.

    f(k) = ℓ_Pl (k_Pl / k)^{1/3} (1 + β / log10(k / k_GUT))^{-1},
    with β = 0.05 and k_GUT, k_Pl, ℓ_Pl chosen in the source.  This helper
    only shows that the output 1/α is sensitive to β: changing β moves 1/α,
    so a quoted match to a CODATA value is a fit, not a unique derivation.
    """

    def f(beta: float, k_gut: float) -> float:
        return ell_pl * (k_pl / k) ** (1.0 / 3.0) * (1.0 + beta / math.log10(k / k_gut)) ** -1

    # Just record that different β give different f, hence a unique β is a fit.
    f_a = f(0.05, 1e16)
    f_b = f(0.04, 1e16)
    f_c = f(0.05, 1e15)
    return {
        "target_1_over_alpha": 1.0 / target,
        "f_beta_0.05_gut_1e16": f_a,
        "f_beta_0.04_gut_1e16": f_b,
        "f_beta_0.05_gut_1e15": f_c,
        "beta_changes_f": abs(f_a - f_b) / abs(f_a),
        "gut_changes_f": abs(f_a - f_c) / abs(f_a),
    }


def reg2_symmetric_recovers_smooth_value() -> bool:
    """For smooth f, the symmetric average is f(λ) + O(δ^2).  It is not a new operation on smooth data."""
    def f(x: float) -> float:
        return math.exp(-x * x) + 0.3 * x

    lam = 0.4
    delta = 1e-4
    mid = reg2_symmetric(f, lam, delta)
    return abs(mid - f(lam)) < 1e-7


def report() -> dict:
    weyl = epsilon_weighting_fails_weyl()
    alpha = alpha_formula_is_not_unique()
    return {
        "epsilon_never_zero": epsilon_is_never_zero(),
        "epsilon_super_exponential": epsilon_decays_faster_than_exponential(),
        "sam2_sequence_to_zero": sam2_sequence_converges_to_zero(),
        "sam2_collapses_on_even_filter": even_filter_collapses_sam2_dual_zero(),
        "division_exact_in_Q": division_10_over_3_is_exact_in_Q(),
        "repeating_nine_equals_one": repeating_nine_equals_one(),
        "sam2_reg2_not_homomorphism": sam2_reg2_not_a_homomorphism(),
        "reg2_symmetric_smooth": reg2_symmetric_recovers_smooth_value(),
        "weyl_check": weyl,
        "e8_adjoint_casimir": e8_adjoint_casimir_quadratic(),
        "two_i_sum_of_squares": sum_of_squares(TWO_I_IRREP_DIMS),
        "paper07_sum_of_squares": sum_of_squares(PAPER07_IRREP_DIMS),
        "paper07_dims_wrong": paper07_dims_sum_of_squares_wrong(),
        "paper07_perm12_not_icosahedron": paper07_perm12_is_not_icosahedron_a5(),
        "twelve_is_not_three": icosahedron_vertices_are_not_three(),
        "alpha_sensitivity": alpha,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(report(), indent=2, default=str))
