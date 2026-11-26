"""Doc 74 (ideas: Shawn Dykes) -- quick checks of the sound-from-the-banks toy pieces."""
import math
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "experiments", "time_medium_sound"))
hp = pytest.importorskip("healpy")
import sound_banks as sb  # noqa: E402


def test_sphere_focus_gain():
    for kR in (1.0, 2.0, 6.0):
        _, _, g = sb.sphere_inphase_solution(kR)
        assert g == pytest.approx(abs(kR / math.sin(kR)), rel=1e-9)


def test_offcentre_only_axisymmetric_power_sums_to_one():
    f = sb.offcentre_sphere_multipoles(2.0, 20.0)
    assert sum(f) == pytest.approx(1.0) and f[0] == 0.0


def test_planarity_of_pure_modes():
    lmax = 4
    for mm, expect in ((4, 1.0), (0, 0.5)):          # Y_44 planar; Y_40: <(n.L)^2> max = l(l+1)/2 / l^2
        alm = np.zeros(hp.Alm.getsize(lmax), dtype=complex)
        alm[hp.Alm.getidx(lmax, 4, mm)] = 1.0
        st, f0 = sb.ell_stats(alm, lmax, 64)
        if mm == 4:
            assert st[4]["planarity"] == pytest.approx(1.0, abs=1e-9)
        else:
            assert st[4]["planarity"] == pytest.approx(10 / 16, abs=1e-9)
            assert st[4]["f0_max"] > 0.99          # grid-limited (no HEALPix pixel exactly at the pole)


def test_chirp_stationary_phase_tilts():
    t = np.linspace(1e-3, 50, 200000)
    for om, ns in ((1 + 3 * t, 2.0), (t ** 2, 1.5), (np.exp(0.3 * t), 1.0)):
        w, P = sb.chirp_spectrum_stationary_phase(t, om, np.ones_like(t))
        k = w / np.exp(np.mean(np.log(w))) * 0.05
        assert sb.ns_running_fit(k, P)["n_s"] == pytest.approx(ns, abs=1e-6)


def test_parity_ratio():
    ell = np.arange(2, 31)
    D = np.where(ell % 2 == 0, 2.0, 1.0)
    assert sb.parity_ratio(D, ell, 30) == pytest.approx(2.0)
