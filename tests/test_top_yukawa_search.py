# erratum 2026-11-26: doc 60 baseline M_t 190.36 -> 190.61 after fixing the Buttazzo v4 reference point (173.10 -> 173.34).
"""Tests for doc 61: structures that lower the spectral top Yukawa."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "experiments" / "two_loop_pati_salam"
if str(PKG) not in sys.path:
    sys.path.insert(0, str(PKG))

import top_yukawa_search as ts  # noqa: E402
from report_61 import kk_identity  # noqa: E402


def test_reduces_to_doc60():
    r = ts.predict(ts.Cand())
    assert abs(r["Mt"] - 190.61) < 0.05 and abs(r["Mh"] - 180.50) < 0.05
    assert abs(r["yt_B"] / r["yt_B_data"] - 1.245) < 0.01


def test_vector_like_fixes_top_not_higgs():
    for m in (1, 3, 4, 12):
        x = ts.solve_for(lambda x: ts._mt(ts.Cand(x=x, x4=x * x / m)), 172.5, 0.0, 8.0, 17)
        assert 2.0 < x < 2.2
        r = ts.predict(ts.Cand(x=x, x4=x * x / m))
        assert 140 < r["Mh"] < 160          # never reaches 125
        assert ts.seesaw_check(r)["m_nu_min_eV"] < 0.05  # neutrino masses still viable
    assert ts.predict(ts.Cand(x=2.1, x4=0.0))["Mh"] > 138  # x4 -> 0 bound


def test_large_ynu_destroys_higgs_with_sigma():
    out = ts.cand1()
    assert 2.9 < out["p=1, yN=0.0g"]["n"] < 3.1
    assert out["p=1, yN=0.0g"]["Mh"] < 50
    assert out["p=1, yN=0.0g"]["seesaw"]["y_N_needed"] > 3.5   # non-perturbative Majorana Yukawa
    assert out["p=1, no sigma"]["Mh"] > 165


def test_flux_towers_preserve_yt_over_g():
    for v in kk_identity().values():
        assert abs(v["yukawa_term"] - v["gauge_term"]) < 1e-12
    base = ts.predict(ts.Cand())["Mt"]
    assert abs(ts.predict(ts.Cand(kk_Mc_over_Lambda=0.3))["Mt"] - base) < 0.05
    assert ts.predict(ts.Cand(kk_Mc_over_Lambda=0.3, kk_yukawa_factor=0.0))["Mt"] > base + 3


def test_lambda_shift_and_chains_do_not_help():
    out = ts.cand3()
    for v in out["scenarios"].values():
        assert v["Mt"] > 189
    assert 7.9 < out["SM_boundary_scale_for_Mt"]["log10_mu"] < 8.4
    assert out["SM_boundary_scale_for_Mt"]["Mh"] > 180


def test_numerology_band():
    out = ts.cand5()
    lo, hi = out["required"]["r_1sigma"]
    assert 0.78 < lo < out["required"]["r"] < hi < 0.82
    assert out["expected_chance_hits"] > 1.0   # hits are expected by chance


def test_sm_group_spectral_model_misses():
    out = ts.cand6()
    assert out["g2=g3, M_N=m_sigma=1e13"]["Mt"] > 185
    assert out["g1=g2, M_N=m_sigma=1e13"]["Mt"] > 183


def test_two_parameter_combo_fits_but_neutrino_tension():
    c = ts.combo(4)["fit"]
    assert 1.7 < c["n"] < 1.9 and 1.1 < c["x"] < 1.4
    assert abs(c["Mt"] - 172.5) < 0.01 and abs(c["Mh"] - 125.1) < 0.01
    assert c["seesaw"]["sum_m_nu_min_eV"] > 0.12
