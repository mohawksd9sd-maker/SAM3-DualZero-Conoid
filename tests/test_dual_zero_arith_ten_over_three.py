"""The 10/3 × 3 truncation fallacy, and its Dual-Zero restoration.

In Q and in R, 10/3 × 3 = 10 exactly: there is no information loss in
exact arithmetic (0.999… = 1).  The fallacy appears when 10/3 is
truncated to a finite visible representative 3.33333, then multiplied
by 3, giving 9.99999.  The Dual-Zero residual keeps the discarded tail
1/300000 and restores 10.
"""

from __future__ import annotations

import unittest
from fractions import Fraction

from dual_zero_arith.pairing import (
    DualZero,
    naive_decimal_mul,
    restore,
    split_decimal,
    split_float64,
)


class TenOverThreeDecimalTests(unittest.TestCase):
    places = 5  # 3.33333 has five digits after the point

    def test_visible_is_the_familiar_truncation(self):
        vis, res = split_decimal(Fraction(10, 3), self.places)
        self.assertEqual(vis, Fraction(333333, 100000))
        self.assertEqual(res, Fraction(1, 300000))
        dz = DualZero.from_exact_decimal(Fraction(10, 3), self.places)
        self.assertEqual(dz.visible_decimal_string(), "3.33333")

    def test_naive_product_is_nine_point_nine_nine_nine_nine_nine(self):
        vis, _ = split_decimal(Fraction(10, 3), self.places)
        product_exact_on_visibles = vis * 3
        self.assertEqual(product_exact_on_visibles, Fraction(999999, 100000))
        self.assertEqual(format(float(product_exact_on_visibles), ".5f"), "9.99999")
        truncated_product = naive_decimal_mul(vis, Fraction(3), self.places)
        self.assertEqual(truncated_product, Fraction(999999, 100000))
        self.assertNotEqual(truncated_product, Fraction(10))

    def test_dual_zero_restores_exactly_ten(self):
        dz = DualZero.from_exact_decimal(Fraction(10, 3), self.places)
        restored = restore(dz.visible, dz.residual)
        self.assertEqual(restored, Fraction(10, 3))
        self.assertEqual(restored * 3, Fraction(10))
        self.assertEqual((dz * 3).exact(), Fraction(10))
        self.assertEqual(dz * 3, Fraction(10))

    def test_residual_is_exactly_what_truncation_removed(self):
        dz = DualZero.from_exact_decimal(Fraction(10, 3), self.places)
        self.assertEqual(dz.visible + dz.residual, Fraction(10, 3))
        self.assertEqual(dz.residual, Fraction(10, 3) - dz.visible)


class TenOverThreeFloat64Tests(unittest.TestCase):
    def test_intermediate_residual_is_nonzero(self):
        vis, res = split_float64(Fraction(10, 3))
        self.assertNotEqual(res, Fraction(0))
        self.assertEqual(Fraction.from_float(vis) + res, Fraction(10, 3))

    def test_ieee_product_already_equals_ten(self):
        # Honest: this particular identity already holds in float64.
        # Dual-Zero is still required to *prove* exact restoration in Q,
        # and the intermediate split still has a nonzero residual.
        self.assertEqual((10.0 / 3.0) * 3.0, 10.0)

    def test_dual_zero_restores_exactly_ten(self):
        dz = DualZero.from_exact_float64(Fraction(10, 3))
        self.assertEqual(restore(dz.visible, dz.residual), Fraction(10, 3))
        self.assertEqual((dz * 3).exact(), Fraction(10))
        self.assertEqual(dz * 3, Fraction(10))

    def test_naive_identity_that_ieee_does_lose(self):
        # Companion: 0.1 + 0.2 is not 0.3 in float64, but Dual-Zero restores 3/10.
        self.assertNotEqual(0.1 + 0.2, 0.3)
        a = DualZero.from_exact_float64(Fraction(1, 10))
        b = DualZero.from_exact_float64(Fraction(2, 10))
        self.assertEqual((a + b).exact(), Fraction(3, 10))


class InvariantTests(unittest.TestCase):
    def test_decimal_chain_stays_exact(self):
        x = DualZero.from_exact_decimal(Fraction(10, 3), 5)
        y = (x * 3) / 3
        self.assertEqual(y.exact(), Fraction(10, 3))
        self.assertEqual(((x * 3) / 3 * 3).exact(), Fraction(10))

    def test_float64_chain_stays_exact(self):
        x = DualZero.from_exact_float64(Fraction(10, 3))
        self.assertEqual(((x * 3) / 3).exact(), Fraction(10, 3))
        self.assertEqual(((x / 7) * 7).exact(), Fraction(10, 3))

    def test_invariant_after_mixed_ops(self):
        x = DualZero.from_exact_decimal(Fraction(2, 7), 6)
        y = DualZero.from_exact_decimal(Fraction(5, 3), 6)
        z = (x + y) * x - y / 2
        self.assertTrue(z.invariant_holds())
        self.assertEqual(z.exact(), (Fraction(2, 7) + Fraction(5, 3)) * Fraction(2, 7) - Fraction(5, 3) / 2)
