"""C0 = 2π ln 2 on the unit metric (proved in the core paper)."""
from __future__ import annotations

import math

from core_geometry import C0_EXACT, C0_finite_part, C0_PAPER_BAND


def test_C0_exact_is_2pi_ln2():
    assert abs(C0_EXACT - 2.0 * math.pi * math.log(2.0)) < 1e-15


def test_quadrature_approaches_exact_value():
    c400 = C0_finite_part(400.0)
    c1000 = C0_finite_part(1000.0)
    assert abs(c1000 - C0_EXACT) < abs(c400 - C0_EXACT)
    assert abs(c1000 - C0_EXACT) < 3e-6
    # remainder is consistent with O(1/U^2)
    assert abs((c1000 - C0_EXACT) * 1000.0 ** 2) < 3.0


def test_old_band_still_does_not_match_exact():
    lo, hi = C0_PAPER_BAND
    assert not (lo <= C0_EXACT <= hi)
