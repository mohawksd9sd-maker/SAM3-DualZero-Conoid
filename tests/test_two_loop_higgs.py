"""Tests for doc 60: two-loop Higgs sector of the spectral Pati-Salam model."""

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

import two_loop_higgs as th  # noqa: E402
from group_theory import standard_model  # noqa: E402


def test_gauge_two_loop_matches_group_theory():
    """g_Y-normalised coefficients used in sm_beta = GUT matrix converted."""
    B = standard_model().two_loop()
    k = Fr(5, 3)
    assert B[0][0] * k * k == Fr(199, 18)  # g1^2 -> 5/3 gY^2, and d gY = (5/3) ...
    assert B[0][1] * k == Fr(9, 2) and B[0][2] * k == Fr(44, 3)
    assert B[1][0] * k == Fr(3, 2) and B[2][0] * k == Fr(11, 6)


def test_matching_inversion():
    m = th.msbar_at_Mt(th.Phys())
    assert th.Mt_from_yt(m["yt"]) == pytest.approx(172.5, abs=1e-9)
    assert th.Mh_from_lambda(m["lambda"], 172.5) == pytest.approx(125.1, abs=1e-9)


def test_sm_benchmark_buttazzo():
    b = th.benchmark(2, True)
    assert -0.017 < b["lambda_MPl"] < -0.012  # Buttazzo et al.: -0.0143 (NNLO)
    assert 9.5 < b["log10_mu_lambda_zero"] < 10.5


@pytest.fixture(scope="module")
def central():
    return th.predict(th.Options())


def test_closure_from_data():
    r = th.predict(th.Options(yt_from_data=True))
    assert abs(r["Mt_pred"] - 172.5) < 0.2


def test_two_loop_top_miss_survives(central):
    assert 188 < central["Mt_pred"] < 193
    assert 177 < central["Mh_pred"] < 184


def test_no_sigma_heavier():
    r = th.predict(th.Options(sigma=False))
    assert r["Mh_pred"] > 185


def test_theory_error_small():
    e = th.error_budget(th.Options())
    assert e["errors"]["dMt_theory"] < 2.0
    assert e["errors"]["dMh_theory"] < 3.0


def test_extension_b_top_still_high():
    r = th.fit_n_to_mh(th.Options())
    assert r["Mh_pred"] == pytest.approx(125.1, abs=1e-3)
    assert r["Mt_pred"] > 177
