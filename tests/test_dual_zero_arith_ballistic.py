"""Ballistic and rocket Euler trajectories: rounding drift vs Dual-Zero."""

from __future__ import annotations

import unittest
from fractions import Fraction

from dual_zero_arith.demos import ballistic_float64, rocket_decimal, rocket_float64


class BallisticFloat64Tests(unittest.TestCase):
    def test_dual_zero_matches_exact_euler_not_necessarily_analytic(self):
        # Keep this test modest so the suite stays fast.  A larger run is in
        # run_demos.py.  Earth-scale x0 makes float64 ULPs coarser.
        out = ballistic_float64(
            x0=Fraction(6_400_000),
            v0=Fraction(100),
            g=Fraction("9.80665"),
            dt=Fraction(1, 100),
            n_steps=5_000,  # T = 50 s
        )
        self.assertEqual(out.dual_minus_euler_x, Fraction(0))
        self.assertEqual(out.dual_x, out.exact_euler_x)
        self.assertEqual(out.dual_v, out.exact_euler_v)
        # Discretization error is a property of Euler, not of Dual-Zero.
        self.assertGreater(out.discretization_error_x, Fraction(0))
        # Rounding drift of naive float64 may be tiny at this scale; we
        # record it, and only require Dual-Zero to match exact Euler.
        self.assertGreaterEqual(out.rounding_drift_x, Fraction(0))


class RocketDecimalTests(unittest.TestCase):
    def test_six_place_decimal_has_visible_drift_dual_zero_restores(self):
        out = rocket_decimal(
            x0=Fraction(0),
            v0=Fraction(0),
            thrust_over_mass=Fraction(20),
            g=Fraction("9.80665"),
            dt=Fraction(1, 100),
            n_steps=2_000,  # T = 20 s
            places=6,
        )
        self.assertEqual(out.dual_minus_euler_x, Fraction(0))
        self.assertEqual(out.dual_x, out.exact_euler_x)
        self.assertGreater(out.rounding_drift_x, Fraction(0))
        self.assertGreater(out.discretization_error_x, Fraction(0))
        # Dual-Zero does not cancel discretization error.
        self.assertEqual(out.dual_x, out.exact_euler_x)
        self.assertNotEqual(out.dual_x, out.analytic_x)


class RocketFloat64Tests(unittest.TestCase):
    def test_rocket_float64_restores_euler(self):
        out = rocket_float64(
            x0=Fraction(6_400_000),
            v0=Fraction(0),
            thrust_over_mass=Fraction(20),
            g=Fraction("9.80665"),
            dt=Fraction(1, 100),
            n_steps=5_000,
        )
        self.assertEqual(out.dual_minus_euler_x, Fraction(0))
        self.assertEqual(out.dual_x, out.exact_euler_x)
