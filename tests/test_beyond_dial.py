"""Docs 68-69: matter-content search, multi-stage breaking, SUSY spectral boundary (exploratory)."""

import math
import os
import sys
from fractions import Fraction as Fr

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "experiments", "two_loop_pati_salam"))

import content_engine as ce  # noqa: E402
import matter_search as ms  # noqa: E402
import multistage as mst  # noqa: E402
import susy_spectral as ss  # noqa: E402
import two_loop_higgs as th  # noqa: E402


def test_engine_reproduces_doc60_baseline():
    r = ce.predict_ps(ce.Content("base"))
    assert r["ok"]
    assert abs(r["Mt"] - 190.36) < 0.02 and abs(r["Mh"] - 180.50) < 0.02
    assert abs(r["m_R"] / 4.2166e13 - 1) < 1e-3 and abs(r["Lambda"] / 1.2409e15 - 1) < 1e-3


def test_trace_index_reproduces_bvdbvs_coupling_relations():
    # gauginos (1x1, 2x2, 3x3 blocks) + one higgsino copy: I = (6.6, 9, 9) (GUT-normalised U(1))
    ex = (ce.Extra("wino", "SM", (Fr(0), "adj", "1")), ce.Extra("gluino", "SM", (Fr(0), "1", "adj")),
          ce.Extra("Hu", "SM", (Fr(3, 20), "F", "1")), ce.Extra("Hd", "SM", (Fr(3, 20), "F", "1")))
    I = ce.sm_index(ex)
    assert I == pytest.approx([6.6, 9.0, 9.0])
    # g_a^2 I_a = const  ->  g_2^2 / g_Y^2 = (I_1 / I_2) / (3/5) = 11/9   [arXiv:1409.5984 eq. (25)]
    assert (I[0] / I[1]) / 0.6 == pytest.approx(11 / 9)
    # two higgsino copies (their Remark 2): g_3^2 = 10/9 g_2^2 = 4/3 g_Y^2
    ex2 = ex + (ce.Extra("Hu2", "SM", (Fr(3, 20), "F", "1")), ce.Extra("Hd2", "SM", (Fr(3, 20), "F", "1")))
    I2 = ce.sm_index(ex2)
    assert I2[1] / I2[2] == pytest.approx(10 / 9)
    assert (I2[0] / I2[2]) / 0.6 == pytest.approx(4 / 3)


def test_trace_only_content_cannot_lower_the_ratio():
    # Higgs-blind extra fermions: y_t/g_L = sqrt(I_L / 6) >= 1 (n = 1), whatever the other traces
    for I in ([6, 6, 6], [7, 6, 6], [8, 7, 7], [10, 10, 10]):
        r = ms.predict_trace_only(I)
        if r.get("ok"):
            assert r["yt_over_g"] == pytest.approx(math.sqrt(I[1] / 6.0), rel=2e-3)
            assert r["Mt"] > 189.0


def test_r_sector_direction_lowers_lambda_but_not_enough():
    r = ce.predict_ps(ce.Content("R", ms.ps_extras("(3,1,1)+(1) [H_R x H_R^o]", 2, "Lambda")))
    assert r["ok"] and r["Lambda"] < 1e13 and r["yt_over_g"] == pytest.approx(1.0, abs=2e-3)
    assert 180.0 < r["Mt"] < 190.0


def test_vector_doublets_lower_the_cutoff_as_in_stephan_2007():
    vd = lambda k: ce.Extra("VD", "SM", (Fr(3, 20), "F", "1"), "weyl", 2 * k, 1e4)
    lam = [ce.predict_sm(ce.Content("vd", (vd(k),)))["Lambda"] for k in (1, 2, 3)]
    assert lam[0] > lam[1] > lam[2] and 1e10 < lam[0] < 1e13


def test_mssm_coefficients_and_higgs_eft():
    assert list(ss.C_MSSM.b) == pytest.approx([6.6, 1.0, -3.0])
    low, _ = ss.run_up(172.5, 50.0, 1e4)
    gY, g2, g3, yt, yb, ytau, _ = low.y[:, -1]
    lam = ss.susy_lambda(gY, g2, yt, 50.0, 0.0)
    d = th.run_sm([gY, g2, g3, yt, yb, ytau, lam], 1e4, 172.5, 2, False)
    assert 120.0 < th.Mh_from_lambda(d.y[6, -1], 172.5) < 128.0   # ~124 GeV at M_S = 10 TeV, X_t = 0


def test_susy_spectral_boundary_overshoots_the_top():
    r = ss.solve(1e3)
    assert r["ok"] and r["Mt"] > 180.0 and r["tanb"] > 40
    assert abs(r["unif_mismatch"]) < 0.01      # MSSM gauge unification works


def test_multistage_limit_and_flatness():
    a = mst.predict(0.001)
    assert a["ok"] and abs(a["Mt"] - 191.2) < 0.3
    b = mst.predict(2.0)
    assert b["ok"] and abs(b["Mt"] - a["Mt"]) < 1.5


def test_combo_susy_plus_vl_pair_needs_a_fitted_share():
    # universal y = y_t on both chains (da = 8): ratio 0.745, top lands ~4 GeV low, flat in M_S
    r = ss.solve(3e3, n=1.0, dI=4.0, da_u=8.0)
    assert r["ok"] and abs(r["yt_over_g"] - math.sqrt(5 / 9)) < 1e-6
    assert 167.5 < r["Mt"] < 169.5 and abs(r["unif_mismatch"]) < 0.01
    # no VL Yukawa share: the trace alone raises the top above the SUSY baseline
    r0 = ss.solve(3e3, n=1.0, dI=4.0, da_u=0.0)
    assert r0["ok"] and r0["Mt"] > 185.0
    # the share that hits 172.5 is between, i.e. a continuous fit
    rf = ss.solve(1e4, n=1.0, dI=4.0, da_u=6.1946)
    assert rf["ok"] and abs(rf["Mt"] - 172.5) < 0.3 and 118 < rf["Mh"] < 132
