"""Exact channel energies E_0(m; U) = (j_{ν,1}/U)², ν = √(m²+1/4)."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))

from core_geometry import (
    E0_exact,
    E0_simple_lower_bound,
    E0_variational_upper_bound,
    besselJ_first_zero,
    bessel_order_for_channel,
    ground_energy_radial,
)


def test_half_integer_first_zero_is_pi():
    assert abs(besselJ_first_zero(0.5) - math.pi) < 1e-14


def test_bessel_order_m0_is_half():
    assert abs(bessel_order_for_channel(0.0) - 0.5) < 1e-15


def test_E0_of_zero_is_pi_squared_over_U2():
    for U in (1.0, 10.0, 20.0, 40.0):
        assert abs(E0_exact(0.0, U) - (math.pi / U) ** 2) < 1e-14


def test_exact_matches_dirichlet_numerics():
    U = 20.0
    for m in (0, 1, 2, 3, 4):
        exact = E0_exact(m, U)
        num = ground_energy_radial(m, U=U, N=800, eps=1e-8)
        assert abs(num - exact) / exact < 1e-5


def test_ratios_are_U_independent():
    r20 = E0_exact(2.0, 20.0) / E0_exact(1.0, 20.0)
    r40 = E0_exact(2.0, 40.0) / E0_exact(1.0, 40.0)
    assert abs(r20 - r40) < 1e-14


def test_variational_bounds():
    U = 20.0
    # m = 0: both bounds collapse to the exact value
    e0 = E0_exact(0.0, U)
    assert abs(E0_simple_lower_bound(0.0, U) - e0) < 1e-14
    assert abs(E0_variational_upper_bound(0.0, U) - e0) < 1e-12
    for m in (1, 2, 3, 5, 8):
        e = E0_exact(m, U)
        lo = E0_simple_lower_bound(m, U)
        hi = E0_variational_upper_bound(m, U)
        assert lo < e + 1e-15
        assert e <= hi + 1e-12
        # the Bessel lower bound (m²+1/4)/U² is strict: j_{ν,1} > ν
        assert e > (m * m + 0.25) / (U * U)


def test_monotonicity_in_m():
    U = 20.0
    vals = [E0_exact(m, U) for m in range(0, 7)]
    assert all(vals[i] < vals[i + 1] for i in range(len(vals) - 1))
