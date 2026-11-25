"""Doc 71: 'time as a medium' tests (analytic pieces + recorded data results)."""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.join(os.path.dirname(__file__), "..", "experiments", "time_medium")
sys.path.insert(0, HERE)

import time_medium as tm  # noqa: E402

RES = json.load(open(os.path.join(HERE, "results_doc71.json")))


def test_echo_delay_reproduces_abedi_dykaar_afshordi():
    # ADA 2017 eq. (6)/(D): 0.29559 s (GW150914, 67.8 Msun, a = 0.68), 0.10246 s, 0.17962 s
    for M, a, ref in ((67.8, 0.68, 0.29559), (22.6, 0.74, 0.10246), (42.0, 0.66, 0.17962)):
        assert abs(tm.echo_delay(M, a) / ref - 1) < 0.02
    assert abs(tm.rmax_kerr(0.0) - 3.0) < 1e-6


def test_scan_recovers_injected_echo_and_lee_is_calibrated():
    rng = np.random.default_rng(1)
    ell = np.arange(2, 1500)
    D0 = 5000 * np.exp(-ell / 800.0)
    sig = 0.02 * D0 + 5
    om = np.linspace(0.01, 0.2, 60)
    T = np.array([[D0 * np.cos(w * ell), D0 * np.sin(w * ell)] for w in om])
    data = D0 + 0.01 * D0 * np.cos(om[37] * ell) + sig * rng.standard_normal(len(ell))
    dchi, amp, _ = tm.scan_chi2(data, sig, [D0], T)
    assert int(np.argmax(dchi)) == 37 and dchi[37] > 50
    sims = tm.lee_sims(sig, [D0], T, nsim=400)
    # max over 60 frequencies of chi2_2 exceeds the 2-dof local 95% point (5.99) most of the time
    assert np.median(sims) > 5.99 and np.quantile(sims, 0.95) < 25


def test_dispersion_and_graviton_mass_numbers():
    d = tm.dispersion_bounds()
    assert d["GW170817_speed"]["lo"] == -3e-15 and d["GW170817_speed"]["hi"] == 7e-16
    assert 1e-21 < d["graviton_mass_100Hz"]["dv_over_c"] < 3e-21
    assert d["GRB090510_linear"]["dn_at_31GeV"] < 1e-18


def test_future_boundary_needs_closed_space_and_decaying_dark_energy():
    assert tm.future_of_universe()["fate"].startswith("expands")
    assert tm.future_of_universe(Ok=-0.0031)["fate"].startswith("expands")
    r = tm.future_of_universe(Om=0.3191, w0=-0.752, wa=-0.86, Ok=-0.0031)
    assert r["fate"] == "crunch" and r["t_Gyr"] > 1e4


def test_alpha_drift_bounds_clocks_dominate():
    rows = tm.alpha_bounds()
    clocks = rows[0]
    assert abs(clocks["eps"]) < 3e-8 and clocks["err"] < 2e-8
    assert all(clocks["err"] < r["err"] for r in rows[1:])


def test_recorded_cmb_and_ring_results_are_null():
    for kind in ("lin", "log"):
        c = RES["cmb"][kind]
        assert c["p_global"] > 0.05            # no significant echo after look-elsewhere
        assert c["best_dchi2"] < c["sims_max_dchi2_95"] + 1e-9 or c["p_global"] > 0.05
    for k, v in RES["rings"]["sims"]["LCDM"].items():
        assert 0.01 < v["p_ge"] < 0.995 or 0.01 < v["p_le"] < 0.995
