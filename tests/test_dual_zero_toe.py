"""Tests for the Dual-Zero re-run of SAM-2 / SAM-3 numerical claims."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
EXPERIMENTS = REPO / "experiments"
for p in (REPO, EXPERIMENTS):
    s = str(p)
    if s not in sys.path:
        sys.path.insert(0, s)

from dual_zero_toe.phase_cancellation import exact_character_integral, report as phase_report
from dual_zero_toe.constants_and_running import (
    c0_exact_mp,
    gn_prefactor_mp,
    report_sam2_alpha,
)
from dual_zero_toe.yukawa_and_selection import report_selection


class PhaseCancellationTests(unittest.TestCase):
    def test_exact_identity(self):
        self.assertEqual(exact_character_integral(0), 2.0 * math.pi)
        for m in (1, 2, 3, 12):
            self.assertEqual(exact_character_integral(m), 0.0j)

    def test_dual_zero_does_not_unzero(self):
        out = phase_report(n_points=512, ms=[0, 1, 2, 3])
        self.assertFalse(out["dual_zero_unzeros_an_exact_zero"])
        self.assertLess(out["offdiag_max_abs_dual_zero"], 0.05)
        row0 = next(r for r in out["rows"] if r["m"] == 0)
        self.assertAlmostEqual(row0["abs_dual_zero"], 2 * math.pi, places=2)


class ConstantsTests(unittest.TestCase):
    def test_c0_and_gn_high_prec_close_to_float(self):
        c0 = float(c0_exact_mp(40))
        self.assertAlmostEqual(c0, 2 * math.pi * math.log(2), places=12)
        gn = float(gn_prefactor_mp(40))
        self.assertAlmostEqual(gn, 64 * math.pi / 45, places=12)

    def test_sam2_kernel_is_not_unique(self):
        out = report_sam2_alpha()
        self.assertTrue(out["claimed_value_matches_CODATA_2018_not_a_derivation"])
        self.assertNotEqual(out["kernel_moves_with_beta"]["0.04"], out["kernel_moves_with_beta"]["0.06"])
        self.assertLess(abs(out["float_minus_mpmath"]), 1e-8)


class SelectionTests(unittest.TestCase):
    def test_hexagonal_still_beats_square_and_flux_not_unique(self):
        out = report_selection()
        self.assertTrue(out["rho_beats_i"])
        self.assertEqual(out["best_integer_M_at_area_1"], 1)
        self.assertEqual(out["best_integer_at_that_area"], 3)
        self.assertGreater(len(out["Z4_invariant_dim_3_fluxes"]), 1)
        self.assertFalse(out["dual_zero_arithmetic_moves_tau_or_untuned_flux"])


if __name__ == "__main__":
    unittest.main()
