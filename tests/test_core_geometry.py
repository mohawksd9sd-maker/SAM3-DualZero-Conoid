"""Exact and numerical checks for the locked conoid geometry."""
from __future__ import annotations

import math

import pytest

from core_geometry import (
    C0_CONVERGED,
    C0_PAPER_BAND,
    C0_finite_part,
    c4_is_not_a5,
    curvature_formula_matches,
    curvature_identity_symbolic,
    f_metric,
    gaussian_curvature,
    ground_energy_radial,
    has_c4_isometry,
    induced_metric_symbolic,
    natural_curvature_radii,
    omega0_from_radius,
    tip_nodes,
)


def test_induced_metric_coefficient_is_4():
    s = induced_metric_symbolic()
    assert s["g_uu_is_1"]
    assert s["g_uv_is_0"]
    assert s["g_vv_matches"]
    assert s["tip_coefficient"] == 4


def test_c4_isometry_and_not_a5():
    assert has_c4_isometry()
    counter = c4_is_not_a5()
    assert counter["equal"] is False


def test_four_tip_nodes():
    nodes = tip_nodes()
    assert len(nodes) == 4
    for v in nodes:
        assert abs(f_metric(0.0, v)) < 1e-15
    # no other zeros of cos(2v) on a fine grid at u=0, up to period
    for k in range(8):
        v = k * math.pi / 8
        if min(abs((v - n) % (2 * math.pi)) for n in nodes) > 1e-12 and min(
            abs((v - n + 2 * math.pi) % (2 * math.pi)) for n in nodes
        ) > 1e-12:
            # if cos(2v) != 0 then f(0,v) != 0
            if abs(math.cos(2 * v)) > 1e-12:
                assert f_metric(0.0, v) > 0


def test_curvature_formula():
    assert curvature_identity_symbolic()
    assert curvature_formula_matches()
    # |K|_max at u=0, |cos(2v)|=1 is 1/4 (ell0=1)
    v = 0.0
    assert abs(gaussian_curvature(0.0, v) + 0.25) < 1e-15


def test_C0_reproduces_converged_value_not_old_band():
    c200 = C0_finite_part(200.0)
    c400 = C0_finite_part(400.0)
    # already close at U=200; closer at 400
    assert abs(c400 - C0_CONVERGED) < 2e-5
    assert abs(c200 - C0_CONVERGED) < 2e-4
    assert abs(c400 - c200) < 2e-4
    # the earlier paper band 4.43--4.45 does not reproduce
    lo, hi = C0_PAPER_BAND
    assert not (lo <= c400 <= hi)
    assert not (lo <= C0_CONVERGED <= hi)


def test_channel_energies_increase_in_m():
    energies = [ground_energy_radial(m, U=20.0, N=400) for m in (0, 1, 2, 3)]
    assert energies[0] < energies[1] < energies[2] < energies[3]


def test_omega0_not_reproduced_from_natural_radii():
    data = natural_curvature_radii()
    for name in ("1/|K|_max", "1/sqrt(|K|_max)", "ell0", "2*ell0"):
        w = data[name]["omega0_if_4_13"]
        assert abs(w - 0.927) > 0.2
    # the R that would give 0.927 is not one of those geometric readings
    R_needed = data["required_for_0.927"]["R"]
    natural_Rs = {data[n]["R"] for n in ("1/|K|_max", "1/sqrt(|K|_max)", "ell0", "2*ell0")}
    assert all(abs(R_needed - R) > 0.05 for R in natural_Rs)
    # consistency of the inverse
    D = 2.0 * math.pi / 12.0
    assert abs(omega0_from_radius(R_needed, D) - 0.927) < 1e-12
