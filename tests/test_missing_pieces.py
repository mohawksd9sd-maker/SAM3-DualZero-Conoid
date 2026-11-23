"""Tests for doc 59: search for the missing pieces (exploratory)."""

from __future__ import annotations

import math
import sys
from fractions import Fraction as Fr
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "experiments" / "two_loop_pati_salam"
if str(PKG) not in sys.path:
    sys.path.insert(0, str(PKG))

import missing_pieces as mp  # noqa: E402
from group_theory import pati_salam  # noqa: E402


@pytest.fixture(scope="module")
def st():
    return mp.Setup()


def test_reduces_to_doc58(st):
    r = st.run(1.0)
    assert r["m_t_pred"] == pytest.approx(185.76, abs=0.05)
    assert r["m_H_pred"] == pytest.approx(168.12, abs=0.05)


def test_boundary_general_n():
    b = mp.boundary(0.5, 2.0, 0.3)
    assert b[1] == pytest.approx(math.sqrt(2) * b[0])
    assert b[0] == pytest.approx(2 * 0.5 / math.sqrt(5))


def test_sigma_variations_do_not_reach_125(st):
    out = mp.sigma_variations(st)
    mh = [v["m_H"] for v in out["spectral_top"].values()]
    assert 160 < min(mh) and max(mh) < 175
    assert min(out["measured_top_mH"].values()) > 140


def test_n_fit_cannot_hit_both(st):
    a = mp.fit_n(st, "m_H")
    b = mp.fit_n(st, "m_t")
    assert a["m_H"] == pytest.approx(125.1, abs=1e-3) and a["m_t"] > 174
    assert b["m_t"] == pytest.approx(172.5, abs=1e-3) and b["m_H"] < 100


def test_two_loop_top_makes_it_worse():
    r = mp.two_loop_top_study()
    assert r["fit_n_to_mH_yN0"]["m_t"] > 178


def test_with2215_content():
    assert pati_salam("with2215").one_loop() == (Fr(8, 3), Fr(2), Fr(-5))


def test_required_shifts(st):
    r = mp.required_boundary_shifts(st)
    assert 0.8 < r["y_t_scale_factor_needed"] < 0.9
    assert r["gravity_correction_size_(Lambda/M_Pl)^2"] < 1e-6


def test_clifford_structures():
    assert mp.clifford(5, 0)["type"] == "M(H)+M(H)" and mp.clifford(5, 0)["volume_squared"] == 1
    assert mp.clifford(0, 5)["type"] == "M(C)" and mp.clifford(0, 5)["rep_real_span"] == 32
    assert mp.quaternion_commutant_of_grading() == 8


def test_mbb_ranges():
    r = mp.mbb_ranges()
    assert 0.001 < r["NO"]["min_eV"] < r["NO"]["max_eV"] < 0.005
    assert 0.015 < r["IO"]["min_eV"] < r["IO"]["max_eV"] < 0.055
