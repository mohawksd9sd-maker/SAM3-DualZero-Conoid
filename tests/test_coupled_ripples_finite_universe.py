"""Tests for doc 66: coupled ripples (part A) and finite-universe low-l CMB (part B)."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "experiments" / "two_loop_pati_salam"
if str(PKG) not in sys.path:
    sys.path.insert(0, str(PKG))

import coupled_ripples as cr  # noqa: E402
import finite_universe as fu  # noqa: E402


# ------------------------------------------------------------------ A
def test_linear_mixing_eigenmasses_and_tachyon():
    lm = cr.light_mode(1.3, 0.5)
    w, _ = cr.eigen(1.3, 0.5)
    assert abs(lm["m_light"] ** 2 - w[0]) < 1e-12
    assert cr.light_mode(1.0, 1.2)["tachyonic"]


def test_strong_mixing_delays_settling():
    weak = cr.simulate(mu=1.3, eps=0.1, tau_end=200, n_out=8000)
    strong = cr.simulate(mu=1.3, eps=0.99, tau_end=300, n_out=12000)
    assert cr.settle_slowest(strong, 1.3, 0.99) > 3 * cr.settle_slowest(weak, 1.3, 0.1)


def test_cubic_resonant_transfer_and_freeze():
    lin = cr.simulate(mu=2.0, phi0=(1.0, 0.01), tau_end=200, n_out=8000)
    nl = cr.simulate(mu=2.0, g3=1.0, phi0=(1.0, 0.01), tau_end=200, n_out=8000)
    assert 1 - cr.beat_share(nl)[1] > 0.3 > 1 - cr.beat_share(lin)[1]
    assert cr.settle_time(nl["t"], nl["Et"]) < 20


def test_quartic_no_transfer():
    nl = cr.simulate(mu=1.0, lam=10.0, phi0=(1.0, 0.01), tau_end=200, n_out=8000)
    assert 1 - cr.beat_share(nl)[1] < 1e-3


def test_degenerate_beats_in_alpha():
    r = cr.simulate(mu=1.05, tau_end=300, n_out=20000)
    env = np.abs(r["p1"] + r["p2"]) * r["t"] ** 0.75
    late = env[len(env) // 2:]
    assert (late.max() - np.percentile(late, 2)) / late.max() > 0.9


def test_mathieu_narrow_vs_broad():
    weak = cr.mathieu(1.0, k_grid=[0.5, 1.0], tau_end=30)
    strong = cr.mathieu(1000.0, k_grid=[1.9, 2.2], tau_end=30)
    assert weak["ln_n_max"] < 0 < strong["ln_n_max"] < 30


def test_friction_threshold_and_hierarchy():
    f = cr.var_friction(cs=(1.0, 1e6))
    assert 50 < f[0]["m_min_TeV"] < 150 and f[1]["m_min_TeV"] < 2
    h = cr.hierarchy_threshold()
    assert 5e-8 < h["mu_min"] < 5e-7


# ------------------------------------------------------------------ B
def test_flat_limits():
    for l in (2, 5):
        assert abs(fu.ratio_T3(l, 50.0) - 1) < 2e-3
        assert abs(fu.ratio_S3(l, 0.01) - 1) < 2e-3
        assert abs(fu.ratio_S3(l, 0.01, pds=True) - 1) < 2e-3


def test_pds_spectrum():
    d = fu.molien_I(60)
    assert [int(k + 1) for k in np.nonzero(d)[0]][:6] == [1, 13, 21, 25, 31, 33]


def test_planck_data_and_lcdm():
    L = fu.lcdm()
    assert abs(L["D2_data"] - 225.9) < 0.5 and 1000 < L["D2_LCDM"] < 1030
    assert L["S_half_data"] < 0.3 * L["S_half_LCDM"]


def test_finite_space_suppresses_quadrupole():
    assert fu.ratio_T3(2, 1.5) < 0.5 < fu.ratio_T3(2, 2.0)
    assert fu.ratio_S3(2, fu.chi_star(-0.013), pds=True) < 0.5
    assert abs(fu.ratio_S3(2, fu.chi_star(-0.013), pds=False) - 1) < 1e-3   # plain S^3: no topology effect


def test_phase_coherence_kills_quadrupole_and_odd():
    ph = fu.t3_phase_realisations(L=2.0, nmax=6, lmax=5, n_real=50)
    assert ph[2]["coherent"] < 1e-20 and ph[3]["coherent"] < 1e-20 and ph[5]["coherent"] < 1e-20
    assert ph[4]["coherent"] > 1e-4
    assert abs(ph[3]["random_mean"] / ph[3]["ensemble_ratio"] - 1) < 0.35
