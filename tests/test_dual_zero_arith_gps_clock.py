"""GPS-style long sum: tiny clock increments added to a large time base."""

from __future__ import annotations

import unittest
from fractions import Fraction

from dual_zero_arith.demos import gps_clock_sum_decimal, gps_clock_sum_float64


class GPSFloat64Tests(unittest.TestCase):
    def test_naive_loses_nanosecond_ticks_dual_zero_does_not(self):
        # 100,000 ticks of 1 ns at a 1e9 s base.  Naive float64 does not move.
        # Dual-Zero restored matches the exact Fraction sum.
        n = 100_000
        out = gps_clock_sum_float64(n_steps=n, base=1_000_000_000.0, increment=1e-9)
        self.assertEqual(out.naive_total, Fraction.from_float(1_000_000_000.0))
        self.assertEqual(out.dual_restored, out.exact_total)
        self.assertEqual(out.restored_minus_exact, Fraction(0))
        self.assertGreater(out.lost_by_naive, Fraction(0))
        self.assertEqual(out.lost_by_naive, out.increment * n)
        # The whole added interval is lost by naive addition.
        self.assertEqual(out.exact_total - out.naive_total, out.increment * n)


class GPSDecimalTests(unittest.TestCase):
    def test_six_place_decimal_drops_nanosecond_ticks(self):
        n = 10_000
        out = gps_clock_sum_decimal(
            n_steps=n,
            base=Fraction(1_000_000_000),
            increment=Fraction(1, 1_000_000_000),
            places=6,
        )
        # Visible unit is 1e-6; 1e-9 truncates to 0.
        self.assertEqual(out.naive_total, Fraction(1_000_000_000))
        self.assertEqual(out.dual_restored, out.exact_total)
        self.assertEqual(out.restored_minus_exact, Fraction(0))
        self.assertEqual(out.lost_by_naive, Fraction(1, 1_000_000_000) * n)
        self.assertEqual(out.exact_total, Fraction(1_000_000_000) + Fraction(n, 1_000_000_000))
