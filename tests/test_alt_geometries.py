"""Tests for the exploratory alternative-geometry experiments.

These tests do not lock any new core theorem.  They check the computed
statements in experiments/alt_geometries/ against exact identities and
against the numerical values recorded in the report.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALT = ROOT / "experiments" / "alt_geometries"
for p in (ALT, ROOT / "code"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from conoid_variants import (  # noqa: E402
    aps_index_untwisted,
    curvature_identity_symbolic,
    curvature_matches_minus_fuu_over_f,
    f_metric_n,
    frequency_versus_generations,
    gaussian_curvature_n,
    has_cyclic_isometry,
    isometry_order,
    max_abs_K_at_u,
    node_count,
    tip_circle_length,
    tip_length_numerical,
    tip_nodes,
    total_curvature_complete_limit,
    total_curvature_truncated,
)
from finite_algebras import (  # noqa: E402
    CCM_ALGEBRA,
    PS_ALGEBRA,
    c4_representation_attempt,
    classification_steps,
    two_threes_are_distinct,
)
from magnetized_torus import (  # noqa: E402
    LEPTON_RATIOS,
    gram_error,
    jacobi_theta_char,
    mass_ratios_from_slice,
    singular_values_of_higgs_slices,
    yukawa_overlaps,
)
from product_4d import ko_dimension, what_fixes_the_flux  # noqa: E402
from promising_candidates import (  # noqa: E402
    LIT_COMPOSITE,
    LIT_WITH_15,
    PS_B_COMPOSITE,
    PS_B_WITH_15,
    find_unification,
    relative_log_error,
)
from riemann_roch import (  # noqa: E402
    compact_surface_chi_cannot_be,
    dirac_index,
    euler_characteristic_nonorientable,
    euler_characteristic_orientable,
    holomorphic_chi,
    pairs_with_dirac_index,
    pairs_with_holomorphic_chi,
)


# --- Riemann-Roch / Dirac index ---


def test_holomorphic_chi_and_dirac_index_formulas():
    assert holomorphic_chi(0, 0) == 1
    assert holomorphic_chi(0, 1) == 2
    assert holomorphic_chi(0, 2) == 3  # H^0(O(2)) on the sphere
    assert holomorphic_chi(1, 3) == 3
    assert holomorphic_chi(2, 3) == 2
    # Dirac index equals the degree, for any genus
    for g in range(0, 5):
        assert dirac_index(3, g) == 3
        assert dirac_index(0, g) == 0
        assert dirac_index(-2, g) == -2


def test_euler_characteristic_never_3_for_a_connected_surface():
    for g in range(0, 6):
        for b in range(0, 6):
            assert euler_characteristic_orientable(g, b) != 3
            assert euler_characteristic_orientable(g, b) <= 2
    for k in range(1, 8):
        for b in range(0, 6):
            assert euler_characteristic_nonorientable(k, b) != 3
            assert euler_characteristic_nonorientable(k, b) <= 1
    rec = compact_surface_chi_cannot_be(3)
    assert rec["connected_surface_can_have_chi"] is False
    assert rec["max_chi_connected_compact"] == 2
    assert rec["verdict"] == "dead end"


def test_pairs_that_give_three():
    # Dirac index 3 is always d=3, any genus
    assert pairs_with_dirac_index(3, max_genus=3) == [(0, 3), (1, 3), (2, 3), (3, 3)]
    # holomorphic chi = 3 means d = g + 2
    assert pairs_with_holomorphic_chi(3, max_genus=3) == [(0, 2), (1, 3), (2, 4), (3, 5)]


# --- Magnetized T^2 ---


def test_jacobi_theta_at_origin_for_tau_i():
    # ϑ[0;0](0,i) = sum_l exp(-π l^2) = θ_3(0, exp(-π)), a standard value
    th = jacobi_theta_char(0.0, 0.0, 0.0, 1j, nsum=60)
    # Known: ϑ_3(0, e^{-π}) ≈ 1.0864348112133083
    assert abs(th.imag) < 1e-14
    assert abs(th.real - 1.0864348112133083) < 1e-12


def test_zero_modes_are_orthonormal_on_the_square_and_rectangular_tori():
    for tau in (1j, 2j, 0.5j):
        err = gram_error(3, tau, n_grid=24)
        assert err < 1e-12, (tau, err)
    # Also N=1 and N=2 on the square torus
    assert gram_error(1, 1j, n_grid=24) < 1e-12
    assert gram_error(2, 1j, n_grid=24) < 1e-12


def test_yukawa_flux_conservation_shape_and_tau_i_ratios():
    Y = yukawa_overlaps(3, 3, 1j, n_grid=32)
    assert Y.shape == (3, 3, 6)
    slices = singular_values_of_higgs_slices(Y)
    assert len(slices) == 6
    # At τ=i and vanishing relative Wilson lines, two alternating patterns
    # with a two-fold degeneracy (see doc 47).
    even = mass_ratios_from_slice(slices[0])
    odd = mass_ratios_from_slice(slices[1])
    assert len(even) == 3 and len(odd) == 3
    assert abs(even[1] - 1.0) < 1e-8
    assert abs(even[2] - 8.10539114865) < 1e-4
    assert abs(odd[1] - 32.9715975833) < 1e-3
    assert abs(odd[2] - odd[1]) < 1e-8
    for k in range(6):
        r = mass_ratios_from_slice(slices[k])
        if k % 2 == 0:
            assert abs(r[2] - even[2]) < 1e-6
        else:
            assert abs(r[1] - odd[1]) < 1e-6


def test_relative_wilson_lines_lift_the_degeneracy_but_do_not_match_leptons():
    Y = yukawa_overlaps(3, 3, 1j, n_grid=32, zeta_I=0.0, zeta_J=0.2, zeta_K=0.1 + 0.15j)
    r0 = mass_ratios_from_slice(singular_values_of_higgs_slices(Y)[0])
    assert len(r0) == 3
    # Degeneracy of the two lighter (or two heavier) states is lifted.
    assert abs(r0[1] - 1.0) > 0.5
    assert abs(r0[2] - r0[1]) > 0.5
    # Still nowhere near the charged-lepton hierarchy.
    assert r0[1] < 50
    assert r0[2] < 50
    assert LEPTON_RATIOS["mu_over_e"] > 200
    assert LEPTON_RATIOS["tau_over_e"] > 3000


def test_yukawa_ratios_depend_on_complex_structure():
    Y_i = yukawa_overlaps(3, 3, 1j, n_grid=32)
    Y_2i = yukawa_overlaps(3, 3, 2j, n_grid=32)
    r_i = mass_ratios_from_slice(singular_values_of_higgs_slices(Y_i)[0])
    r_2i = mass_ratios_from_slice(singular_values_of_higgs_slices(Y_2i)[0])
    # The heavy/light ratio changes by a large factor when Im(τ) doubles.
    assert r_2i[2] / r_i[2] > 4.0


# --- Conoid variants ---


def test_n2_recovers_the_locked_metric_and_tip():
    import core_geometry as cg

    u, v, ell0 = 0.7, 0.3, 1.0
    assert abs(f_metric_n(u, v, 2, ell0) - cg.f_metric(u, v, ell0)) < 1e-15
    assert abs(gaussian_curvature_n(u, v, 2, ell0) - cg.gaussian_curvature(u, v, ell0)) < 1e-15
    assert tip_circle_length(2, 1.0) == 8.0
    assert node_count(2) == 4
    assert isometry_order(2) == 4
    locked_nodes = [math.pi / 4 + k * math.pi / 2 for k in range(4)]
    for a, b in zip(tip_nodes(2), locked_nodes):
        assert abs(a - b) < 1e-15


def test_frequency_n_geometry_identities():
    for n in (1, 2, 3, 4):
        assert curvature_identity_symbolic(n)
        assert curvature_matches_minus_fuu_over_f(n)
        assert has_cyclic_isometry(n)
        assert node_count(n) == 2 * n
        assert isometry_order(n) == 2 * n
        assert abs(tip_circle_length(n, 1.0) - 4.0 * n) < 1e-15
        assert abs(tip_length_numerical(n, 1.0) - tip_circle_length(n, 1.0)) < 1e-9
        # max |K| = 1/(4u^2) for u <= n ell0
        assert abs(max_abs_K_at_u(0.5, n, 1.0) - 1.0 / (4.0 * 0.25)) < 1e-12
        rec = total_curvature_complete_limit(n)
        assert abs(rec["outer_integral"] - 2.0 * math.pi) < 1e-10
        assert abs(rec["tip_integral"]) < 1e-5
        assert abs(rec["total_curvature"] + 2.0 * math.pi) < 1e-5


def test_truncated_gauss_bonnet_and_untwisted_index_independent_of_n():
    a, b = 0.3, 5.0
    for n in (1, 2, 3):
        kint = total_curvature_truncated(a, b, n)
        # χ(annulus)=0 and the GB identity is already used to compute the
        # integral, so this is a consistency check of the two ends, not an
        # independent evaluation of K.  The n-independence of the complete
        # limit is the geometric statement; the index is topological.
        assert kint < 0.0
    aps = aps_index_untwisted()
    assert aps["untwisted_APS_index_bounding_spin"] == 0
    assert aps["depends_on_frequency_n"] is False
    scan = frequency_versus_generations()
    assert scan["any_integer_n_produces_3"] is False
    assert scan["verdict"] == "dead end"
    for row in scan["rows"]:
        assert row["equals_3"]["nodes"] is False
        assert row["equals_3"]["isometry_order"] is False


# --- Finite algebras ---


def test_classification_and_c4_dead_end():
    steps = classification_steps()
    assert len(steps) == 6
    assert all(s["derived_from_the_conoid"] is False for s in steps)
    assert two_threes_are_distinct()["identifying_them"].startswith("numerology")
    c4 = c4_representation_attempt()
    assert c4["equals_CCM_algebra"] is False
    assert c4["equals_PS_algebra"] is False
    assert c4["produces_fermion_multiplets"] is False
    assert c4["verdict"] == "dead end"
    assert CCM_ALGEBRA == "C ⊕ H ⊕ M_3(C)"
    assert PS_ALGEBRA == "H_R ⊕ H_L ⊕ M_4(C)"


# --- Products and flux ---


def test_ko_dimension_of_conoid_times_surface_times_F():
    assert ko_dimension(2, 2, 6) == 2  # matches the CCM fermionic setup
    assert ko_dimension(2, 6) == 0  # raw conoid × F does not
    flux = what_fixes_the_flux()
    assert flux["any_attempt_selects_3"] is False
    assert flux["verdict"] == "dead end"


# --- Pati-Salam one-loop reproduction ---


def test_ps_unification_composite_near_literature():
    found = find_unification(PS_B_COMPOSITE)
    assert found is not None
    # Triple meeting is numerically exact once m_R is found.
    assert found["inv_g2_spread_at_Lambda"] < 1e-12
    # CC2010 inputs at M_Z give scales within ~30% of the CCvS2015 quotes
    # (a residual from input couplings, not a method failure).
    assert relative_log_error(found["m_R_GeV"], LIT_COMPOSITE["m_R_GeV"]) < 0.3
    assert relative_log_error(found["Lambda_GeV"], LIT_COMPOSITE["Lambda_GeV"]) < 0.3
    # Order of magnitude: 10^13 and 10^15
    assert 1e13 < found["m_R_GeV"] < 1e14
    assert 1e15 < found["Lambda_GeV"] < 1e16


def test_ps_unification_with_15_near_literature():
    found = find_unification(PS_B_WITH_15)
    assert found is not None
    assert found["inv_g2_spread_at_Lambda"] < 1e-12
    assert relative_log_error(found["m_R_GeV"], LIT_WITH_15["m_R_GeV"]) < 0.3
    assert relative_log_error(found["Lambda_GeV"], LIT_WITH_15["Lambda_GeV"]) < 0.3
    assert 1e13 < found["m_R_GeV"] < 1e14
    assert 1e15 < found["Lambda_GeV"] < 1e16
