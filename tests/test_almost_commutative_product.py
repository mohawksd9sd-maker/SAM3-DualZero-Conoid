"""Almost-commutative product, heat-kernel integrals, CCM one-loop running."""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))

from almost_commutative_product import (
    CCM_KO_DIM_F,
    F0_from_g3,
    generation_count_status,
    ko_dimension,
    option_table,
    report as acm_report,
    spectator_argument,
)
from ccm_oneloop_rge import (
    B_COEFFS,
    CC2010_ALPHA_AT_MZ,
    CC2010_G_AT_MZ,
    LAMBDA_CCM_EXAMPLE,
    MZ,
    alpha_from_g,
    report as rge_report,
    run_alphas,
)
from conoid_heat_kernel import (
    area_asymptotic_unit,
    area_truncation,
    boundary_integral_u_over_f,
    curvature_integral,
    gauss_bonnet_residual,
    total_curvature_complete,
)
from core_geometry import C0_EXACT
from u1_twist_and_tip import report as tip_report, tip_geometry


def test_ko_dimension_arithmetic():
    assert ko_dimension(2, 6) == 0
    assert ko_dimension(4, 6) == 2
    assert ko_dimension(4, 2, 6) == 4
    assert ko_dimension(2, 2, 6) == 2
    assert CCM_KO_DIM_F == 6


def test_only_conoid_times_sigma_and_plain_CCM_have_ko_2_and_dim_4():
    rows = option_table()
    ok = [r for r in rows if r["ko_matches_CCM_fermions"] and r["heat_kernel_is_4D"]]
    names = {r["name"] for r in ok}
    assert any("conoid × Σ^2" in n or "conoid × Σ" in n for n in names)
    assert any("plain CCM" in n for n in names)
    # the raw 2D product is not 4D
    raw = next(r for r in rows if r["name"].startswith("conoid × F"))
    assert raw["heat_kernel_is_4D"] is False
    assert raw["ko_matches_CCM_fermions"] is False
    assert "failed" in raw["verdict"]


def test_paper09_ko_claim_flagged():
    r = acm_report()
    assert r["paper09_ko_claim_is_wrong"] is True
    assert r["literature_ko_of_F"] == 6
    assert r["paper09_claimed_ko_of_F"] == 4


def test_generations_are_an_input():
    g = generation_count_status()
    assert g["CCM_N_is_input"] is True
    assert g["conoid_APS_index_untwisted"] == 0
    assert "failed" in g["verdict"]


def test_spectator_preserves_ratios():
    s = spectator_argument()
    assert s["ccm_ratio_preserved"] is True
    assert s["higgs_quartic_at_Lambda_preserved"] is True


def test_F0_normalization_CC2010():
    # g3^2 F0 / (2 π^2) = 1/4
    g3 = 0.5
    F0 = F0_from_g3(g3)
    assert abs(g3 * g3 * F0 / (2.0 * math.pi ** 2) - 0.25) < 1e-14


def test_gauss_bonnet_identity():
    for a, b in ((0.2, 6.0), (0.05, 20.0), (0.01, 80.0), (1e-4, 400.0)):
        assert abs(gauss_bonnet_residual(a, b, n=4000)) < 1e-12


def test_complete_curvature_is_minus_2pi():
    assert total_curvature_complete() == -2.0 * math.pi
    # approach from inside
    val = curvature_integral(1e-12, 1e8)
    assert abs(val + 2.0 * math.pi) < 1e-8


def test_outer_integral_approaches_2pi():
    assert abs(boundary_integral_u_over_f(1e6) - 2.0 * math.pi) < 1e-10
    assert boundary_integral_u_over_f(1e-8) < 1e-6


def test_area_matches_C0_asymptotic():
    b = 20.0
    A = area_truncation(1e-10, b, ell0=1.0, n_u=8000)
    asym = area_asymptotic_unit(b)
    assert abs(A - asym) / asym < 1e-4
    # the finite part at large b, after subtracting πb²+2π log b, is C0
    # already baked into the asymptotic; check C0 itself
    assert abs(C0_EXACT - 2 * math.pi * math.log(2.0)) < 1e-15


def test_one_loop_reproduces_CC2010_coefficients():
    # α3^{-1}(Λ) = α3^{-1}(MZ) + (42/(12π)) log(Λ/MZ)  =  + 7/(2π) log
    a = CC2010_ALPHA_AT_MZ
    inv = run_alphas(a, LAMBDA_CCM_EXAMPLE)
    L = math.log(LAMBDA_CCM_EXAMPLE / MZ)
    expected3 = 1.0 / a[2] + 7.0 / (2.0 * math.pi) * L
    assert abs(inv[2] - expected3) < 1e-12
    expected1 = 1.0 / a[0] - (41.0 / 6.0) / (2.0 * math.pi) * L
    assert abs(inv[0] - expected1) < 1e-12


def test_CC2010_g_and_alpha_are_consistent_to_quoted_rounding():
    for g, a in zip(CC2010_G_AT_MZ, CC2010_ALPHA_AT_MZ):
        # CC2010 quotes α1=0.0101 for g1=0.3575 (α1=0.01017); 4-decimal rounding.
        assert abs(alpha_from_g(g) - a) < 1e-4


def test_couplings_do_not_unify_exactly_at_one_loop():
    r = rge_report()
    assert r["unification_exact_at_one_loop"] is False
    # the three pairwise scales are not the same (classic SM fact)
    s = r["meeting_scales"]
    vals = list(s.values())
    assert max(vals) / min(vals) > 2.0
    assert r["higgs_example"]["agrees_with_observed_125"] is False
    assert r["conoid_changes_this_running"] is False
    # spread at 1e17 is a few percent or more
    assert r["at_1e17_GeV"]["relative_spread"] > 0.02


def test_gauss_bonnet_flux_is_not_in_2_3():
    r = tip_report()
    assert r["flux"]["int_K_over_2pi"] == -1.0
    assert r["flux"]["in_interval_2_3"] is False
    assert r["flux"]["verdict"] == "failed"
    assert r["truncated_index"]["index"] == 0
    assert r["truncated_index"]["produces_index_3"] is False


def test_tip_endpoints_are_double_covered():
    t = tip_geometry()
    assert t["each_endpoint_has_two_preimages"] is True
    assert t["endpoints_z"] == [-1.0, 1.0]
    assert all(abs(f) < 1e-15 for f in t["f_at_nodes"])


def test_elliptic_boundary_matches_quadrature():
    import numpy as np
    from core_geometry import f_metric
    u, ell0 = 1.0, 1.0
    n = 20000
    vs = np.linspace(0.0, 2.0 * math.pi, n, endpoint=False)
    quad = float(np.sum([u / f_metric(u, float(v), ell0) for v in vs]) * (2 * math.pi / n))
    exact = boundary_integral_u_over_f(u, ell0)
    assert abs(exact - quad) < 1e-8
