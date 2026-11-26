# erratum 2026-11-26: doc 60 baseline M_t 190.36 -> 190.61 after fixing the Buttazzo v4 reference point (173.10 -> 173.34).
"""Tests for doc 65: a displaced internal modulus that rings and settles ('stone in a still pond')."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "experiments" / "two_loop_pati_salam"
if str(PKG) not in sys.path:
    sys.path.insert(0, str(PKG))

import ripple_modulus as rm  # noqa: E402


def test_background_planck2018():
    assert 13.6 < rm.t0_s() / rm.YR / 1e9 < 13.95
    assert abs(rm.H_N(0.0) / rm.H0 - 1) < 1e-3
    H1100 = float(rm.H_N(rm.N_of_z(1100.0)))
    assert 2.5e-29 < H1100 < 4.5e-29


def test_spectral_potential_flat():
    V = rm.spectral_potential_einstein(np.linspace(-3, 3, 13), f2=0.7, f4=1.9, Lam=2.0)
    assert np.allclose(V, V[0])


def test_couplings():
    c = rm.couplings()
    assert -0.9 < c["beta_alpha"] < -0.85
    assert -41 < c["beta_p"] < -40
    assert c["boundary_ratios_yt_over_g_lambda_over_g2"] == 0.0


def test_frozen_then_rings_and_settles():
    tr = rm.transfer(1.5e-31, switch=1e9)
    assert abs(tr.phi(-15.0)[0] - 1) < 1e-6          # frozen while H >> m
    env_late = tr.envelope(0.0)[0]
    assert env_late < 0.05                           # rang down
    # WKB scaling after onset: amplitude ∝ a^{-3/2}
    tr2 = rm.transfer(1e-20)
    e1, e2 = tr2.envelope([-5.0, -3.0])
    assert abs(e2 / e1 - math.exp(-3.0)) < 1e-6


def test_wkb_matches_exact_ode():
    m = 1e-30
    ex, wk = rm.transfer(m, switch=1e9), rm.transfer(m, switch=100.0)
    N = -1.0
    assert abs(ex.envelope(N)[0] / wk.envelope(N)[0] - 1) < 0.02


def test_natural_heavy_modulus_survives():
    nb = rm.natural_benchmark()
    assert 1e20 < nb["m_eV"] < 1e21 and nb["allowed"] and nb["dominates_before_decay"]
    assert nb["T_RH_MeV"] > 1e6
    assert rm.evaluate(1e14, 1.0, 1.0)["allowed"]               # ~100 TeV, decays before BBN
    assert not rm.evaluate(1e12, 1.0, 1.0)["allowed"]           # 1 TeV: moduli problem
    assert "moduli problem" in rm.evaluate(1e12, 1.0, 1.0)["failed"]


def test_light_natural_coupling_excluded():
    for m in (1e-30, 1e-22, 1e-12, 1e-3):
        e = rm.evaluate(m, 1e-6, 1.0)
        assert not e["allowed"] and "fifth force / EP" in e["failed"]
    ms = rm.massless_spectral()
    assert ms["eta"] > 0.1 and 1e-7 < ms["kappa_max"] < 3e-7


def test_dm_benchmarks():
    d = rm.dm_benchmark(1e-19)
    assert 1e-7 < d["kappa_max"] < 3e-7
    assert rm.dm_benchmark(1e-20)["kappa_max"] == 0.0           # fuzzy DM excluded
    assert rm.dm_benchmark(0.1)["kappa_max"] == 1.0             # sub-50 um range: kappa = 1 allowed


def test_alpha_variation_scaling_and_oklo():
    tr = rm.transfer(1e-19)
    # with all DM and kappa = 1, quasar alpha passes but clocks fail
    d = rm.dm_benchmark(1e-19)
    e = rm.evaluate(1e-19, d["phi_i_for_all_DM"], 1.0)
    assert e["checks"]["QSO alpha z=1-4"][0] and not e["checks"]["clocks"][0]
    assert tr.envelope(rm.N_of_z(1.0))[0] / tr.envelope(0.0)[0] > 2.5


def test_top_higgs_unchanged():
    th = rm.top_higgs()
    assert abs(th["settled_minimum"]["Mt"] - 190.61) < 0.05
    sc = th["boundary_scale_shift_scan"]
    assert min(v["Mt"] for v in sc.values()) > 188.0
