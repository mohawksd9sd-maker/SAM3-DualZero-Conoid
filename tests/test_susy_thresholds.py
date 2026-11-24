"""Doc 70: SUSY threshold corrections for the spectral SUSY boundary."""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "experiments", "two_loop_pati_salam"))

import susy_thresholds as st  # noqa: E402


def test_loop_functions_normalised_and_delta_b_consistent():
    for f in (st.F1, st.F2, st.F3, st.F4, st.F5, st.F7):
        assert abs(f(1.0) - 1) < 1e-3
    assert abs(st.F6(1.0)) < 1e-3 and abs(st.F8(1, 1) - 1) < 1e-3 and abs(st.F9(1, 1) - 1) < 1e-3
    assert abs(st.I3(1, 1, 1) - 0.5) < 1e-3
    # the gluino piece of the y_b threshold (F9 form) equals the standard 2 M3^2 I(m,m,M3) Delta_b form
    for x in (0.3, 0.5, 2.0, 3.0):
        assert abs(st.F9(x, x) / (2 * st.I3(x * x, x * x, 1.0)) - 1) < 0.01


def test_eft_higgs_matches_susyhd_ballpark():
    # Vega-Villadoro 2015 fig. 3 (tan b = 20, M_t = 173.34): ~116 GeV at X_t = 0, M_S = 2 TeV; 125 at ~10-20 TeV
    assert 114 < st.mh_only(2e3, 173.34, 20.0, st.Spectrum()) < 118
    assert 122.5 < st.mh_only(1e4, 173.34, 20.0, st.Spectrum()) < 126
    assert st.mh_only(2e3, 173.34, 20.0, st.Spectrum(xt=2.0)) > 123


def test_candidate_10_with_thresholds():
    r = st.solve_thr(3e4, st.Spectrum(sgn_mu=1.0))
    assert r["ok"] and abs(r["yt_over_g"] - math.sqrt(5 / 9)) < 1e-6
    assert 0.25 < r["Delta_b"] < 0.45 and 60 < r["tanb"] < 75
    assert 169.8 < r["Mt"] < 171.2 and 124 < r["Mh"] < 126.5   # 2 GeV low with M_h ~ 125
    rm = st.solve_thr(3e4, st.Spectrum(sgn_mu=-1.0))
    assert rm["ok"] and rm["Mt"] < r["Mt"] - 1.0
