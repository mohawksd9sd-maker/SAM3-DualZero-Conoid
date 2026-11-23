"""Tests for the exploratory conoid × Σ × Pati–Salam product.

These tests do not lock any new core theorem.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "experiments" / "ps_conoid_product"
for p in (PKG, ROOT / "code", ROOT / "experiments" / "alt_geometries"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from core_geometry import C0_EXACT  # noqa: E402
from flux_mechanisms import (  # noqa: E402
    attempt_anomaly_cancellation,
    heat_kernel_exact,
    heat_kernel_from_spectrum,
    heat_kernel_weyl_leading,
    report as flux_report,
    scan_flux_and_area,
)
from geometry import (  # noqa: E402
    area_conoid_asymptotic,
    flux_yang_mills_integral,
    gauge_boundary_conditions,
    gravitational_coupling_status,
    ko_dimension,
    product_data,
    product_integrals,
    generations_bookkeeping,
    sigma_invariants,
)
from higgs_sigma import (  # noqa: E402
    lambda_h,
    lambda_h_sigma,
    lambda_sigma,
    reduction_factor,
)
from rge_pipeline import (  # noqa: E402
    ALPHA_INV_MZ_PDG2024,
    ALPHA_S_MZ_PDG2026,
    CC2010_ALPHA_AT_MZ,
    LIT_COMPOSITE,
    MZ_CC2010,
    MZ_PDG2026,
    PS_B_COMPOSITE,
    SIN2_THETA_W_MSBAR_PDG2026,
    find_unification_general,
    sm_alphas_at_mz_from_pdg,
)
from yukawa_fit import TARGET, log_ratio_error, principled_scan  # noqa: E402


def test_product_ko_dimension_and_bookkeeping():
    assert ko_dimension(2, 2, 6) == 2
    p = product_data()
    assert p["ko_matches_CCM_fermions"] is True
    assert p["heat_kernel_is_4D"] is True
    assert p["Y_is_Minkowski"] is False
    gens = generations_bookkeeping()
    assert gens["option_N_F_3_and_flux_3"]["generation_count"] == 9
    assert gens["option_B"]["CCvS_Higgs_numerics_apply_off_the_shelf"] is False
    assert gauge_boundary_conditions()["changed_by_the_conoid_or_by_Sigma"] is False
    assert gravitational_coupling_status()["unique_derivation"] is False


def test_product_integrals_add_correctly():
    a, b, area_s = 0.2, 5.0, 3.0
    t2 = product_integrals(a, b, "T2", area_sigma=area_s)
    assert abs(t2["vol_Y"] - t2["area_X"] * area_s) < 1e-10
    # T² is flat: ∫_Y R = Area(T²) * ∫_X R_X
    assert abs(t2["int_R_Y"] - area_s * t2["int_R_X"]) < 1e-10
    assert t2["int_R_Sigma"] == 0.0
    s2 = product_integrals(a, b, "S2", radius=1.0)
    a_s2 = 4.0 * math.pi
    assert abs(s2["area_Sigma"] - a_s2) < 1e-12
    assert abs(s2["int_R_Sigma"] - 8.0 * math.pi) < 1e-12
    assert abs(s2["int_R_Y"] - (a_s2 * s2["int_R_X"] + s2["area_X"] * 8.0 * math.pi)) < 1e-8


def test_complete_T2_einstein_hilbert_is_finite_and_S2_is_not():
    # At a large outer cutoff the T² integrated curvature approaches -4π Area(T²).
    t2 = product_integrals(1e-6, 1e4, "T2", area_sigma=2.0)
    assert abs(t2["int_R_Y"] - (-4.0 * math.pi * 2.0)) < 1e-3
    s2 = product_integrals(1e-6, 1e4, "S2", radius=1.0)
    # Dominated by Area(X)*8π, which grows like 8π² b²
    assert s2["int_R_Y"] > 1e8


def test_area_asymptotic_uses_C0():
    rec = area_conoid_asymptotic(30.0, 1.0)
    assert abs(rec["finite_part_C0_scaled"] - C0_EXACT) < 1e-12
    # Leading term dominates the finite part
    assert rec["leading_pi_b2"] > 10.0 * rec["finite_part_C0_scaled"]


def test_flux_YM_vanishes_only_at_M_0_and_scales_as_M2_over_A():
    assert flux_yang_mills_integral(10.0, 2.0, 0) == 0.0
    y3 = flux_yang_mills_integral(10.0, 2.0, 3)
    y1 = flux_yang_mills_integral(10.0, 2.0, 1)
    assert abs(y3 / y1 - 9.0) < 1e-12
    # doubles if Area(X) doubles; halves if Area(Σ) doubles
    assert abs(flux_yang_mills_integral(20.0, 2.0, 3) / y3 - 2.0) < 1e-12
    assert abs(flux_yang_mills_integral(10.0, 4.0, 3) / y3 - 0.5) < 1e-12


def test_heat_kernel_coth_matches_spectrum_and_weyl_limit():
    t, area, m = 0.002, 1.5, 3
    exact = heat_kernel_exact(t, m, area)
    spec = heat_kernel_from_spectrum(t, m, area, n_max=600)
    weyl = heat_kernel_weyl_leading(t, area)
    assert abs(exact - spec) / exact < 1e-10
    assert abs(exact - weyl) / weyl < 1e-3
    # First correction is positive: exact > Weyl at this order? 
    # coth = 1/x + x/3 + ..., so exact = Weyl + (2π t M²)/(3A) + ...
    assert exact > weyl


def test_spectral_action_prefers_smallest_flux_not_three():
    scan = scan_flux_and_area()
    assert scan["any_fixed_area_prefers_M_3"] is False
    assert scan["all_fixed_area_prefers_minimal_M"] is True
    assert scan["grid_minimum"]["M"] != 3
    assert flux_report()["any_attempt_fixes_flux_3"] is False
    assert flux_report()["any_attempt_fixes_moduli_uniquely"] is False
    assert attempt_anomaly_cancellation()["selects_3"] is False


def test_pdg_alphas_from_stated_inputs():
    a1, a2, a3 = sm_alphas_at_mz_from_pdg()
    aem = 1.0 / ALPHA_INV_MZ_PDG2024
    assert abs(a1 - aem / (1.0 - SIN2_THETA_W_MSBAR_PDG2026)) < 1e-15
    assert abs(a2 - aem / SIN2_THETA_W_MSBAR_PDG2026) < 1e-15
    assert a3 == ALPHA_S_MZ_PDG2026
    # Ballpark: close to the CC2010 inputs used in doc 45
    c1, c2, c3 = CC2010_ALPHA_AT_MZ
    assert abs(a1 - c1) / c1 < 0.02
    assert abs(a2 - c2) / c2 < 0.02
    assert abs(a3 - c3) / c3 < 0.02


def test_oneloop_ps_unification_with_cc2010_and_pdg_inputs():
    f_cc = find_unification_general(PS_B_COMPOSITE, CC2010_ALPHA_AT_MZ, MZ_CC2010, sm_two_loop=False)
    assert f_cc is not None
    assert f_cc["inv_g2_spread_at_Lambda"] < 1e-12
    # Same numbers as doc 47, within a tight tolerance
    assert abs(math.log(f_cc["m_R_GeV"] / 5.429e13)) < 0.01
    f_pdg = find_unification_general(
        PS_B_COMPOSITE, sm_alphas_at_mz_from_pdg(), MZ_PDG2026, sm_two_loop=False
    )
    assert f_pdg is not None
    assert f_pdg["inv_g2_spread_at_Lambda"] < 1e-12
    # PDG inputs land close to the CCvS2015 quoted scales
    assert abs(math.log(f_pdg["m_R_GeV"] / LIT_COMPOSITE["m_R_GeV"])) < 0.05
    assert abs(math.log(f_pdg["Lambda_GeV"] / LIT_COMPOSITE["Lambda_GeV"])) < 0.05
    assert 1e13 < f_pdg["m_R_GeV"] < 1e14
    assert 1e15 < f_pdg["Lambda_GeV"] < 1e16


def test_partial_two_loop_sm_shifts_scales_but_still_meets():
    f = find_unification_general(
        PS_B_COMPOSITE, sm_alphas_at_mz_from_pdg(), MZ_PDG2026, sm_two_loop=True
    )
    assert f is not None
    assert f["inv_g2_spread_at_Lambda"] < 1e-11
    assert 1e13 < f["m_R_GeV"] < 1e14
    assert 1e15 < f["Lambda_GeV"] < 1e16
    # Distinct from the one-loop PDG determination, but of the same order
    f1 = find_unification_general(
        PS_B_COMPOSITE, sm_alphas_at_mz_from_pdg(), MZ_PDG2026, sm_two_loop=False
    )
    assert abs(math.log(f["Lambda_GeV"] / f1["Lambda_GeV"])) > 0.2
    assert abs(math.log(f["Lambda_GeV"] / f1["Lambda_GeV"])) < 1.5


def test_cc2012_scalar_couplings_and_reduction_factor():
    g = 0.5
    assert abs(lambda_h(0.0, g) - (4.0 / 3.0) * g * g) < 1e-15
    assert abs(lambda_sigma(g) - 8.0 * g * g) < 1e-15
    assert abs(lambda_h_sigma(0.0, g)) < 1e-15
    assert abs(reduction_factor(0.0, g) - 1.0) < 1e-15
    # Closed identity: sqrt((3-n²)/(n²+3)) for |n|<sqrt(3)
    for n in (0.25, 0.5, 1.0):
        expected = math.sqrt((3.0 - n * n) / (n * n + 3.0))
        assert abs(reduction_factor(n, g) - expected) < 1e-12
    assert math.isnan(reduction_factor(2.0, g))  # n²=4>3, unstable at tree level


def test_principled_yukawa_scan_does_not_derive_lepton_ratios():
    scan = principled_scan(n_grid=20)
    assert scan["frobenius_minimizer_matches_leptons"] is False
    assert scan["targeted_is_a_fit_in_disguise"] is True
    # The target itself is the PDG lepton ratio pair
    assert TARGET[0] > 200 and TARGET[1] > 3000
    # Sanity of the log-error: perfect match is 0; a 1:1:1 slice is huge
    assert log_ratio_error([1.0, 1.0, 1.0]) > 10.0
    assert log_ratio_error([1.0, TARGET[0], TARGET[1]]) < 1e-15
