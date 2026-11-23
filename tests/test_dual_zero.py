"""Definition checks for Dual-Zero. No claim that this identifies zeta zeros."""
from __future__ import annotations

import math

import pytest


def epsilon(n: int, omega0: float = 0.927) -> float:
    """Dual-Zero generator as defined in the corpus: ε(n)=ω0 (-1)^n n^{-n}."""
    return omega0 * ((-1) ** n) * (n ** (-n))


def test_generator_formula_and_decay():
    w = 0.927
    assert epsilon(1, w) == pytest.approx(-w)
    assert epsilon(2, w) == pytest.approx(w * 2 ** (-2))
    # n^{-n} decays faster than exponential: |ε(8)| is already tiny
    assert abs(epsilon(8)) < 1e-7
    vals = [abs(epsilon(n)) for n in range(2, 9)]
    assert all(vals[i] > vals[i + 1] for i in range(len(vals) - 1))


def test_omega0_is_an_input_not_a_derived_output():
    # Changing the input changes the generator; nothing in this definition
    # computes 0.927 from the metric.
    assert epsilon(3, 0.927) != epsilon(3, 1.0)
    assert epsilon(3, 0.5) == pytest.approx(0.5 * (-1) * 3 ** (-3))
