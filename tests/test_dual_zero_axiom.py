"""Tests for the standalone Dual-Zero axiom and selection scans (doc 52).

These tests do not lock any new core theorem.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "experiments" / "dual_zero_axiom"
if str(PKG) not in sys.path:
    sys.path.insert(0, str(PKG))

from axiom import (  # noqa: E402
    well_posedness_report,
    residual_scale,
    epsilon,
    reg2_finite,
)
from flat_t2 import (  # noqa: E402
    modular_invariance_sample,
    ranking_at_delta,
    ranking_unregulated,
)
from magnetized_t2 import (  # noqa: E402
    area_for_unreg_stationary,
    best_integer,
    index_of_flux,
    joint_interior_critical_point,
    log_det,
    unreg_stationary_M,
)
from orbifold_z4 import fluxes_with_invariant_dimension, report as z4_report  # noqa: E402
from product_action import report as product_report, seeley_densities_are_smooth_in_moduli  # noqa: E402
from sphere_monopole import (  # noqa: E402
    dS_dM,
    dirac_index,
    int_scalar_curvature,
    report as sphere_report,
    stationary_area_at_fixed_M,
)
from zeta_tools import (  # noqa: E402
    TAU_I,
    s_is_safe,
    unreg_log_det_abs_D,
    zeta_D2_magnetized_prime,
    zeta_laplacian,
)


def test_well_posedness_all_true():
    wp = well_posedness_report()
    assert wp["omega0_is_an_input"] is True
    assert wp["epsilon_is_not_a_heat_trace_weight"] is True
    for key, val in wp.items():
        if key in {"omega0_is_an_input", "epsilon_is_not_a_heat_trace_weight"}:
            continue
        assert val is True, key


def test_epsilon_and_scale():
    assert epsilon(1, 1.0) == -1.0
    assert residual_scale(2, 1.0) == 0.25
    assert residual_scale(2, 0.927) == 0.927 * 0.25


def test_magnetized_unregulated_and_index():
    assert index_of_flux(3) == 3
    assert best_integer(1.0)[0] == 1
    A3 = area_for_unreg_stationary(3)
    assert abs(unreg_stationary_M(A3) - 3.0) < 1e-12
    assert best_integer(A3)[0] == 3
    assert abs(log_det(3, A3, delta=None) - unreg_log_det_abs_D(3, A3)) < 1e-12


def test_magnetized_closed_form_derivative_at_zero_limit():
    # ζ'_{D²}(s) → M log(2M/A) as s → 0 (doc 49).
    M, A = 3, 1.0
    target = M * math.log(2.0 * M / A)
    val = float(zeta_D2_magnetized_prime(1e-8, M, A))
    assert abs(val - target) / abs(target) < 1e-6


def test_magnetized_finite_delta_does_not_select_3_at_generic_area():
    # At area 1 the unregulated maximizer is M=1; a mid-size safe δ must
    # not jump to a unique preference for 3.
    for delta in (1e-4, 0.05, 0.2):
        assert s_is_safe(delta)
        assert best_integer(1.0, delta=delta)[0] != 3
    joint = joint_interior_critical_point(delta=0.25)
    assert joint["selects_M_3_for_all_areas"] is False
    assert joint["selects_a_single_M_for_all_areas"] is False


def test_magnetized_dz_recovers_unreg_at_tiny_delta():
    A, M = 2.0, 2
    unreg = log_det(M, A, delta=None)
    tiny = log_det(M, A, delta=1e-6)
    assert abs(tiny - unreg) < 1e-6


def test_unfluxed_torus_hexagonal_still_wins():
    unreg = ranking_unregulated()
    assert unreg["rho_beats_i"] is True
    assert unreg["rho_equals_rho_right"] is True
    for delta in (0.02, 0.1, 0.2):
        row = ranking_at_delta(delta)
        assert row["rho_beats_i"] is True
        assert row["rho_matches_rho_right"] is True
    inv = modular_invariance_sample(0.2)
    assert inv["abs_tau_minus_T"] < 1e-12
    assert inv["abs_tau_minus_S"] < 1e-12


def test_eisenstein_matches_lattice_sum_at_s2():
    # ∑' (m²+n²)^{-2} = 4 ζ(2) G  (G = Catalan's constant) on the square torus.
    import mpmath as mp

    G = float(mp.catalan)
    exact = 4.0 * (math.pi**2 / 6.0) * G
    E = float(zeta_laplacian(2.0, TAU_I, area=4.0 * math.pi**2))
    # With area = 4π², ζ_Δ(s) = E(τ,s), so ζ_Δ(2) = ∑' (m²+n²)^{-2}.
    assert abs(E - exact) / exact < 1e-10


def test_z4_dimension_3_is_not_unique():
    fluxes = fluxes_with_invariant_dimension(3)
    assert 8 in fluxes and 11 in fluxes
    assert len(fluxes) > 1
    z4 = z4_report()
    assert z4["index_or_sector_counts_depend_on_Reg2"] is False
    assert z4["unique_flux_with_dimension_3"] is False
    assert z4["tau_already_fixed_to_i_by_C4"] is True


def test_sphere_index_and_seeley_signs():
    assert dirac_index(3) == 3
    assert abs(int_scalar_curvature() - 8.0 * math.pi) < 1e-15
    for A in (1.0, 4.0 * math.pi):
        assert abs(dS_dM(A, 0, 1.0)) < 1e-15
        assert abs(dS_dM(A, 3, 1.0)) > 1.0
    a1 = stationary_area_at_fixed_M(1, 1.0, 1.0, 1.0, 1.0)
    a3 = stationary_area_at_fixed_M(3, 1.0, 1.0, 1.0, 1.0)
    assert a1 is not None and a3 is not None
    assert abs(a3 / a1 - 3.0) < 1e-12
    sph = sphere_report()
    assert sph["index_depends_on_Reg2"] is False
    assert sph["dirac_determinant_not_invented"] is True


def test_product_action_unchanged_and_no_interior_M():
    assert seeley_densities_are_smooth_in_moduli() is True
    prod = product_report()
    assert prod["partial_S_partial_M_vanishes_only_at_M_0"] is True
    assert prod["tau_enters_seeley_coefficients_on_magnetized_T2"] is False


def test_reg2_does_not_use_the_value_at_a_jump():
    def step(x: float) -> float:
        return 1.0 if x > 0 else (-1.0 if x < 0 else 999.0)

    assert abs(reg2_finite(step, 0.0, 1e-3)) < 1e-15
