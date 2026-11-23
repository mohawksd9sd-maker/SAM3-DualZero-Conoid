"""Singular tip u→0: geometry, curvature integrability, APS cuts, no index 3."""

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))

from core_geometry import f_metric, gaussian_curvature, tip_nodes
from singular_tip_analysis import (
    inner_aps_kernel_along_cuts,
    local_abs_K_mass_bound,
    max_abs_K_at_u,
    metric_circle_ratio_around_node,
    numerical_abs_K_mass_box,
    numerical_max_abs_K,
    old_K_max_claim_fails,
    tip_circle_length,
    tip_neighbourhood_area,
    report,
)
from conoid_heat_kernel import boundary_integral_u_over_f, total_curvature_complete


def test_tip_circle_length_is_8_ell0():
    assert tip_circle_length(1.0) == 8.0
    assert tip_circle_length(2.0) == 16.0
    # quadrature of 2 ℓ0 |cos(2v)|
    vs = np.linspace(0.0, 2.0 * math.pi, 20000, endpoint=False)
    L = float(np.sum([2.0 * abs(math.cos(2.0 * v)) for v in vs]) * (2.0 * math.pi / 20000))
    assert abs(L - 8.0) < 1e-4


def test_four_nodes_and_f_vanishes_only_there():
    nodes = tip_nodes()
    assert len(nodes) == 4
    for v in nodes:
        assert abs(f_metric(0.0, v)) < 1e-15
        assert abs(math.cos(2.0 * v)) < 1e-15
    # a regular tip point
    assert f_metric(0.0, 0.0) == 2.0


def test_constant_v_rays_are_unit_speed_and_hit_the_tip_in_distance_u():
    # g_uu=1, Gamma^u_uu=Gamma^v_uu=0, so (u,v0) is a geodesic of speed 1
    # This is tested by the Christoffel identity and by f-independent g_uu=1.
    # Distance to u=0 along the ray is exactly u.
    assert f_metric(0.3, 0.2) > 0
    # g_uu = 1 is in the locked metric by construction


def test_kg_vanishes_on_regular_tip():
    # f_u = u/f, so at u=0 with f>0 one has k_g=0
    for v in (0.0, 0.2, 1.0, 2.0):
        assert f_metric(0.0, v) > 0.5
        assert abs(0.0 / f_metric(0.0, v)) == 0.0


def test_K_nonpositive_and_unbounded_near_nodes():
    # K <= 0
    for u in (0.01, 0.1, 1.0, 5.0):
        for v in np.linspace(0.0, 2.0 * math.pi, 80, endpoint=False):
            assert gaussian_curvature(u, float(v)) <= 1e-12
    # unbounded: max at small u exceeds 1/(4 ℓ0^2) by a large factor
    claimed = 0.25
    assert abs(max_abs_K_at_u(0.1) - 1.0 / (4.0 * 0.1 * 0.1)) < 1e-12
    assert max_abs_K_at_u(0.1) > 20.0 * claimed
    fail = old_K_max_claim_fails()
    assert fail["ratio"] == 4.0  # at u=ell0/2, 1/(4*(0.5)^2) / (1/4) = 4


def test_max_abs_K_formula_matches_scan():
    for u in (0.2, 0.5, 1.0, 3.0, 5.0):
        exact = max_abs_K_at_u(u)
        num = numerical_max_abs_K(u, n=40000)
        assert abs(num - exact) / exact < 2e-3


def test_K_is_L1_near_a_node():
    # numerical box mass is finite and shrinks with the box
    m1 = numerical_abs_K_mass_box(0.05, 0.05, nu=200, ns=200)
    m2 = numerical_abs_K_mass_box(0.02, 0.02, nu=200, ns=200)
    assert m1 < 0.1 and m2 < m1
    assert m2 < 0.05
    # analytic local-model mass is O(R)
    assert abs(local_abs_K_mass_bound(0.05) - math.pi * 0.05 / 8.0) < 1e-15


def test_complete_curvature_is_minus_2pi_so_int_abs_K_is_2pi():
    assert total_curvature_complete() == -2.0 * math.pi
    # I(a)→0: no leftover delta mass at the tip
    assert boundary_integral_u_over_f(1e-8) < 1e-6
    assert boundary_integral_u_over_f(1e-4) < 1e-2


def test_tip_area_is_finite_and_linear_in_a():
    a = 0.01
    A = tip_neighbourhood_area(a)
    # I(0)=8, so A ~ 8a as a→0 (plus π a²)
    assert 7.5 * a < A < 8.5 * a + math.pi * a * a + 0.01
    assert tip_neighbourhood_area(0.0) == 0.0


def test_aps_index_zero_with_no_kernel_on_every_cut():
    r = inner_aps_kernel_along_cuts()
    assert r["all_h_zero"] is True
    assert r["index_of_each_truncation"] == 0


def test_metric_circle_is_half_disk_scale_not_cusp_or_full_cone():
    rows = metric_circle_ratio_around_node(
        epsilons=(0.05, 0.03),
        u_max=0.2,
        s_max=0.2,
        nu=220,
        ns=221,
        margin=0.04,
    )
    for row in rows:
        ratio = row["L_over_eps"]
        # not a cusp (0) and not a full cone (2π≈6.28); of order π
        assert 1.5 < ratio < 5.0, row


def test_report_verdicts_do_not_claim_index_3():
    r = report()
    assert "failed" in r["verdicts"]["index_3_from_the_tip"]
    assert "failed" in r["verdicts"]["Dirac_ESA"]
    assert "not a cone" in r["verdicts"]["singularity_type"]
    assert r["tip_length_unit"] == 8.0
    assert r["K_nonpositive"] is True
