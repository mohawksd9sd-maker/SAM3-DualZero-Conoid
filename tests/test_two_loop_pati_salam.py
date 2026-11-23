"""Tests for docs 55-58: two-loop SM -> Pati-Salam running and its spin-offs.

Exploratory; none of this locks a new core theorem.
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction as Fr
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "experiments" / "two_loop_pati_salam"
for p in (PKG, ROOT):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import finite_triple as ft  # noqa: E402
import higgs_masses as hm  # noqa: E402
import phenomenology as ph  # noqa: E402
from group_theory import (  # noqa: E402
    Field,
    Group,
    Model,
    dual_zero_record,
    pati_salam,
    sm_components_of_heavy_fields,
    standard_model,
    threshold_b,
)
from rge import PDG, PDG_ALPHA_INV_127930, solve_unification  # noqa: E402


# ---------------------------------------------------------------- group theory


def test_sm_one_loop_literature():
    assert standard_model().one_loop() == (Fr(41, 10), Fr(-19, 6), Fr(-7))


def test_sm_two_loop_literature():
    B = standard_model().two_loop()
    assert B == (
        (Fr(199, 50), Fr(27, 10), Fr(44, 5)),
        (Fr(9, 10), Fr(35, 6), Fr(12)),
        (Fr(11, 10), Fr(9, 2), Fr(-26)),
    )


def test_sm_top_yukawa_coefficients():
    m = standard_model()
    assert tuple(m.yukawas[0][1][a] for a in range(3)) == (Fr(17, 10), Fr(3, 2), Fr(2))
    k, G = m.top_one_loop
    assert k == Fr(9, 2) and G == (Fr(17, 20), Fr(9, 4), Fr(8))


@pytest.mark.parametrize("nf", [0, 3, 6])
def test_qcd_two_loop_nf(nf):
    # beta_1 = -102 + 38/3 n_f for SU(3) with n_f Dirac flavours (2 n_f Weyl triplets)
    G = (Group("SU3", "SU", 3),)
    fields = [Field("q", ("F",), "weyl", 2 * nf)] if nf else []
    m = Model("QCD", G, fields)
    assert m.two_loop()[0][0] == Fr(-102) + Fr(38, 3) * nf
    assert m.one_loop()[0] == Fr(-11) + Fr(2, 3) * nf


@pytest.mark.parametrize("sc,b", [("composite", (Fr(-7, 3), Fr(-3), Fr(-31, 3))), ("with15", (Fr(-7, 3), Fr(-3), Fr(-9)))])
def test_ps_one_loop_matches_repo(sc, b):
    assert pati_salam(sc).one_loop() == b


def test_ps_two_loop_values_and_yukawa():
    p = pati_salam("composite")
    B = p.two_loop()
    assert B[2][2] == Fr(-206, 3) and B[0][0] == Fr(50, 3) and B[1][1] == Fr(8)
    assert tuple(p.yukawas[0][1][a] for a in range(3)) == (Fr(4), Fr(4), Fr(4))
    assert p.top_one_loop[0] == Fr(6)


@pytest.mark.parametrize("sc", ["composite", "with15"])
def test_heavy_decomposition_sum_rule(sc):
    """SM b + all heavy SM components = PS b projected with the matching relation."""
    tot = list(standard_model().one_loop())
    for _, f, k in sm_components_of_heavy_fields(sc):
        tot = [a + b for a, b in zip(tot, threshold_b(f, k))]
    p = pati_salam(sc).one_loop()
    assert tot == [Fr(3, 5) * p[0] + Fr(2, 5) * p[2], p[1], p[2]]


def test_dual_zero_record_exact():
    vis, res = dual_zero_record(Fr(199, 50))
    assert Fr(vis) + res == Fr(199, 50)


# ---------------------------------------------------------------- running


@pytest.fixture(scope="module")
def sols():
    return {
        "one": solve_unification(PDG, "composite", 1),
        "two": solve_unification(PDG, "composite", 2),
        "one_repo": solve_unification(PDG_ALPHA_INV_127930, "composite", 1),
    }


def test_one_loop_reproduces_repo(sols):
    r = sols["one_repo"]
    assert abs(r["m_R_GeV"] / 4.205e13 - 1) < 3e-3
    assert abs(r["Lambda_GeV"] / 2.399e15 - 1) < 3e-3


def test_two_loop_solution_exists_and_meets(sols):
    r = sols["two"]
    assert r is not None
    assert r["residual_alpha_inv_spread"] < 1e-8
    assert 3.5e13 < r["m_R_GeV"] < 4.3e13
    assert 1.0e15 < r["Lambda_GeV"] < 1.4e15
    assert r["m_R_GeV"] < r["Lambda_GeV"] < 1.22e19
    assert 44.0 < r["alpha_U_inv"] < 45.0


def test_two_loop_lowers_lambda_by_about_two(sols):
    ratio = sols["one"]["Lambda_GeV"] / sols["two"]["Lambda_GeV"]
    assert 1.7 < ratio < 2.4


def test_thresholds_shift_but_do_not_destroy():
    u = np.zeros(6)
    u[0] = 1.0  # leptoquark x10
    r = solve_unification(PDG, "composite", 2, log10_ratios=u)
    assert r is not None and r["residual_alpha_inv_spread"] < 1e-8
    assert 12.5 < math.log10(r["m_R_GeV"]) < 14.5


# ---------------------------------------------------------------- doc 57


def test_operator_baryon_number():
    t = ph.operator_table()
    for name, v in t.items():
        if v["epsilon"]:
            assert v["Delta_B"] != 0
        else:
            assert v["Delta_B"] == 0 and v["Delta_F"] == 0


def test_lifetime_scaling_and_bound(sols):
    r = sols["two"]
    t1 = ph.generic_d6_lifetime(r["Lambda_GeV"], r["alpha_U_inv"])
    t2 = ph.generic_d6_lifetime(2 * r["Lambda_GeV"], r["alpha_U_inv"])
    assert abs(t2 / t1 - 16) < 1e-9
    assert t1 < ph.SUPERK_P_EPI0_YEARS  # a generic d=6 operator at Lambda would be excluded
    assert ph.rare_decay_check(r["m_R_GeV"])["passes"]


# ---------------------------------------------------------------- doc 58


def test_scalar_betas_match_formula():
    l, k, s = 0.3, 0.2, 0.5
    bl, bk, bs = hm.scalar_betas(l, k, s)
    assert bl == pytest.approx(24 * l * l + 2 * k * k)
    assert bk == pytest.approx(k * (12 * l + 6 * s + 8 * k))
    assert bs == pytest.approx(18 * s * s + 8 * k * k)


def test_boundary_n1():
    g = 0.53
    b = hm.boundary(g, 1.0)
    assert b["y_t"] == pytest.approx(g)
    assert b["lambda_h"] == pytest.approx(g * g)
    assert b["lambda_hs"] == pytest.approx(2 * g * g)
    assert b["lambda_s"] == pytest.approx(8 * g * g)


def test_spectral_predictions_regression(sols):
    p = hm.predict(1.0, True, sols["two"])
    assert 180 < p["m_t_pole_pred_GeV"] < 192  # misses 172.5
    assert 160 < p["m_H_pred_GeV"] < 176  # misses 125.1
    q = hm.mH_with_observed_top(True)
    assert abs(q["y_t_at_mt_check"] - PDG.yt_at_mt()) < 1e-6
    assert 140 < q["m_H_pred_GeV"] < 160


def test_seesaw_order(sols):
    r = sols["two"]
    s = ph.seesaw(r["y_t_at_m_R"], r["m_R_GeV"])
    assert 0.05 < s["m_nu3_eV"] < 0.5


# ---------------------------------------------------------------- doc 56


def test_finite_triple_axioms():
    D = ft.dirac()
    assert ft.ko_dimension(D) == 6
    rng = np.random.default_rng(3)
    assert ft.order_zero_violation(ft.random_ps, rng) < 1e-12
    assert ft.first_order_violation(D, ft.random_ps, ft.random_ps, rng) > 1.0
    assert ft.first_order_violation(D, ft.random_sm, ft.random_sm, rng) < 1e-12
    D0 = ft.dirac(y_nu=0.9, y_e=0.2, y_u=0.9, y_d=0.2, m_M=0.0)
    assert ft.first_order_violation(D0, ft.random_ps, ft.random_ps, rng) < 1e-12


def test_sm_is_maximal_first_order():
    m = ft.maximality(ft.dirac())
    assert m["A_SM_is_maximal_first_order"]
    assert m["dim_A_SM"] == 24 and m["dim_A_PS"] == 40


def test_regulator_blind_to_axioms():
    r = ft.isospectral_test()
    assert r["max_eigenvalue_diff"] < 1e-12
    assert r["reg2_heat_D"] == pytest.approx(r["reg2_heat_D2"], rel=1e-12)
    assert r["eps_sum_D"] == pytest.approx(r["eps_sum_D2"], rel=1e-12)
    assert r["first_order_SM_D"] < 1e-12 and r["first_order_SM_D2"] > 1e-3
