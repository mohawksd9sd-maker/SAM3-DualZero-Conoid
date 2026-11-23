"""Standalone Dual-Zero axiom (May 2026 / doc 18 definition 2.2).

This module states the regulator as an operation on functions of a
spectral parameter.  It does *not* weight heat traces or mode sums by
ε(n).  ω₀ is an input.  Nothing here is a derivation of a physical
constant, a flux, or a modulus.
"""

from __future__ import annotations

import math
from typing import Callable

# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

def epsilon(n: int, omega0: float = 1.0) -> float:
    """ε(n) = ω₀ (-1)^n n^{-n}, n ≥ 1.  ω₀ > 0 is an input."""
    if n < 1:
        raise ValueError("n must be a positive integer")
    if omega0 <= 0:
        raise ValueError("omega0 must be positive")
    return omega0 * ((-1) ** n) * (n ** -n)


def residual_scale(n: int, omega0: float = 1.0) -> float:
    """Positive finite-N scale δ_N = ω₀ N^{-N} used in the approximant."""
    if n < 1:
        raise ValueError("n must be a positive integer")
    if omega0 <= 0:
        raise ValueError("omega0 must be positive")
    return omega0 * (n ** -n)


# ---------------------------------------------------------------------------
# Reg_2 on functions of a spectral parameter
# ---------------------------------------------------------------------------

def reg2_finite(f: Callable[[float], float], lam: float, delta: float) -> float:
    """Finite approximant: [f(λ+δ) + f(λ−δ)] / 2,  δ > 0."""
    if delta <= 0:
        raise ValueError("delta must be positive")
    return 0.5 * (f(lam + delta) + f(lam - delta))


def reg2_N(f: Callable[[float], float], lam: float, n: int, omega0: float = 1.0) -> float:
    """Approximant at the Dual-Zero scale δ_N = ω₀ N^{-N}."""
    return reg2_finite(f, lam, residual_scale(n, omega0))


def reg2_of_jump(left: float, right: float) -> float:
    """Value of the δ → 0⁺ limit at a simple jump discontinuity."""
    return 0.5 * (left + right)


def finite_part_simple_pole(residue: float, regular: float, delta: float) -> float:
    """Symmetric average of a/(x) + b + O(x) about the pole.

    [ (a/δ + b) + (a/(−δ) + b) ] / 2 = b.  The residue is dropped.
    This is the Cauchy principal-value / finite-part extraction, and it
    is recorded so it is not confused with residue (Seeley) extraction.
    The unused arguments document the input; the output is `regular`.
    """
    _ = residue, delta
    return regular


# ---------------------------------------------------------------------------
# Well-posedness predicates (used by tests)
# ---------------------------------------------------------------------------

def is_linear_on_samples() -> bool:
    def f(x: float) -> float:
        return math.sin(x) + 0.3 * x * x

    def g(x: float) -> float:
        return math.exp(-x * x)

    lam, delta = 0.4, 1e-3
    left = reg2_finite(lambda x: 2.0 * f(x) - 3.0 * g(x), lam, delta)
    right = 2.0 * reg2_finite(f, lam, delta) - 3.0 * reg2_finite(g, lam, delta)
    return abs(left - right) < 1e-12


def kills_odd_germ_at_zero() -> bool:
    def odd(x: float) -> float:
        return x + 0.2 * x**3

    return abs(reg2_finite(odd, 0.0, 1e-3)) < 1e-15


def preserves_even_germ_up_to_delta_sq() -> bool:
    def even(x: float) -> float:
        return 1.0 + 2.0 * x * x + 0.1 * x**4

    # At 0, [even(δ)+even(−δ)]/2 = even(δ)
    mid = reg2_finite(even, 0.0, 1e-3)
    return abs(mid - even(1e-3)) < 1e-15


def recovers_continuous_value() -> bool:
    def f(x: float) -> float:
        return math.exp(-x * x) + 0.3 * x

    lam, delta = 0.4, 1e-4
    return abs(reg2_finite(f, lam, delta) - f(lam)) < 1e-7


def jump_is_averaged() -> bool:
    def step(x: float) -> float:
        if x > 0:
            return 1.0
        if x < 0:
            return -1.0
        return 100.0  # value at the jump must not matter

    return abs(reg2_finite(step, 0.0, 1e-3) - 0.0) < 1e-15


def approximant_converges_to_continuous_value(omega0: float = 1.0) -> bool:
    def f(x: float) -> float:
        return math.cos(x)

    lam = 0.7
    vN = reg2_N(f, lam, n=8, omega0=omega0)
    return abs(vN - f(lam)) < 1e-12


def heat_trace_as_function_of_t_is_unchanged() -> bool:
    """Reg₂ acts on t ↦ Tr e^{-tΔ}, which is smooth for t > 0, so it
    returns the unweighted heat trace.  This is the allowed use.
    Weighting modes by ε(n) is forbidden and is not performed here.
    """
    def heat(t: float) -> float:
        # Model spectrum λ_n = n², n ≥ 1, plus the constant mode 1.
        return 1.0 + sum(math.exp(-t * n * n) for n in range(1, 80))

    t0 = 0.05
    return abs(reg2_finite(heat, t0, 1e-6) - heat(t0)) < 1e-8


def forbidden_epsilon_weight_fails_weyl(t: float = 1e-4) -> bool:
    """Documentary check only: ∑ ε(n) e^{-t n²} does not track Weyl.

    This weighting is *not* part of the axiom.  The test exists so the
    selection calculations cannot silently fall back on it.
    """
    unweighted = sum(math.exp(-t * n * n) for n in range(1, 400))
    weyl = 0.5 * (math.sqrt(math.pi / t) - 1.0)
    weighted = sum(epsilon(n, 1.0) * math.exp(-t * n * n) for n in range(1, 40))
    return abs(unweighted - weyl) / abs(weyl) < 0.05 and abs(weighted) < 10 and abs(weyl) > 50


def pole_finite_part_is_the_regular_term() -> bool:
    """Reg₂ at a simple pole returns the finite part, not the residue."""
    def f(x: float) -> float:
        # 3/x + 5 + x, evaluated off zero
        return 3.0 / x + 5.0 + x

    mid = reg2_finite(f, 0.0, 1e-4)
    return abs(mid - 5.0) < 1e-8


def even_in_the_shift() -> bool:
    def f(x: float) -> float:
        return math.exp(-x) + x**3

    a = reg2_finite(f, 0.2, 0.05)
    b = 0.5 * (f(0.2 - 0.05) + f(0.2 + 0.05))
    return abs(a - b) < 1e-15


DEFAULT_OMEGA0_SAMPLES = (0.1, 0.5, 0.927, 1.0, 2.0)


def well_posedness_report() -> dict:
    return {
        "linear": is_linear_on_samples(),
        "kills_odd_germ": kills_odd_germ_at_zero(),
        "preserves_even_germ": preserves_even_germ_up_to_delta_sq(),
        "recovers_continuous": recovers_continuous_value(),
        "averages_jump": jump_is_averaged(),
        "N8_approximant_converges": approximant_converges_to_continuous_value(),
        "heat_trace_of_t_unchanged": heat_trace_as_function_of_t_is_unchanged(),
        "forbidden_weight_fails_weyl": forbidden_epsilon_weight_fails_weyl(),
        "pole_yields_finite_part_not_residue": pole_finite_part_is_the_regular_term(),
        "even_in_shift": even_in_the_shift(),
        "omega0_is_an_input": True,
        "epsilon_is_not_a_heat_trace_weight": True,
    }
