"""Regression tests for the 2026-11-26 erratum (docs 60, 70, 72, 73).

1. Buttazzo et al. 1307.3536v4 fits are expanded around M_t = 173.34 GeV (v2 used 173.10).
2. BGSS 1407.4081 two-loop O(alpha_t alpha_s) quartic threshold has -X_t^5/M_S^5 (not -1/4).
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "experiments", "two_loop_pati_salam"))

import two_loop_higgs as th  # noqa: E402
import susy_thresholds as st  # noqa: E402


def test_buttazzo_v4_reference_point():
    assert th.MT_REF == 173.34
    m = th.msbar_at_Mt(th.Phys(Mt=173.34, Mh=125.15, alpha_s=0.1184))
    assert abs(m["yt"] - 0.93690) < 1e-12 and abs(m["lambda"] - 0.12604) < 1e-12 and abs(m["g3"] - 1.1666) < 1e-12
    assert abs(th.Mt_from_yt(0.93690, 0.1184) - 173.34) < 1e-9
    assert abs(th.Mh_from_lambda(0.12604, 173.34) - 125.15) < 1e-9


def test_two_loop_quartic_threshold_x5_coefficient():
    sm = dict(gY=0.36, g2=0.64, g3=1.0, yt=0.85, yb=0.5, ytau=0.4)
    tb = 50.0
    on = st.thresholds(sm, tb, st.Spectrum(xt=2.449))
    off = st.thresholds(sm, tb, st.Spectrum(xt=2.449, two_loop_lam=False))
    assert off["lam_2l"] == 0.0
    l2 = on["lam_2l"]
    # recompute from the BGSS polynomial using the threshold's own couplings: the ratio of the
    # polynomial at X and the polynomial at X with the -X^5/4 bug must not match
    X = 2.449
    good = -12 * X - 6 * X * X + 14 * X ** 3 + X ** 4 / 2 - X ** 5
    bad = -12 * X - 6 * X * X + 14 * X ** 3 + X ** 4 / 2 - X ** 5 / 4
    on0 = st.thresholds(sm, tb, st.Spectrum(xt=1.0))["lam_2l"]
    p1 = -12 - 6 + 14 + 0.5 - 1.0
    assert abs(l2 / on0 - good / p1) < 0.05 * abs(good / p1)
    assert abs(l2 / on0 - bad / p1) > 0.2 * abs(bad / p1)
