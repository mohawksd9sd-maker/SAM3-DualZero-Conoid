"""Doc 75 (zero-dial Higgs routes for candidate #10; SAM-3 / Dual-Zero originator: Shawn Dykes).
Dual-Zero regulator untouched."""
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "experiments", "higgs_routes_75"))

import h75  # noqa: E402

D73 = os.path.join(os.path.dirname(__file__), "..", "experiments", "open_routes_72", "results_route1d.json")


def test_dterm_factor_matches_direct_minimisation():
    rng = np.random.default_rng(1)
    for _ in range(50):
        gA2, gB2, mu_ = rng.uniform(0.1, 2), rng.uniform(0.1, 2), rng.uniform(0, 50)
        g2 = gA2 * gB2 / (gA2 + gB2)
        x = mu_ / (gA2 + gB2)
        assert abs(g2 * h75.dterm_factor(gA2, gB2, x) - h75.g_eff2_direct(gA2, gB2, mu_)) < 1e-12


def test_dterm_limits():
    gA2, gB2 = 0.5, 0.75
    g2 = gA2 * gB2 / (gA2 + gB2)
    assert h75.dterm_factor(gA2, gB2, 0.0) == 1.0                     # SUSY limit: decouples
    assert abs(g2 * h75.dterm_factor(gA2, gB2, 1e15) - gA2) < 1e-12   # non-decoupling limit: full g_A
    # PS: g'^2 = (3/5) g_U^2 -> g_R^2 = g_U^2 in the x -> inf limit
    assert abs(0.6 * h75.dterm_factor(h75.PS_RATIO, 1.0, 1e15) - 1.0) < 1e-12


def test_martin_function():
    assert abs(h75.f_martin(1.0)) < 1e-15
    for e in (1e-3, 1e-2):
        assert abs(h75.f_martin(1 + e) - h75.f_martin_series(e)) < 1e-9
    # Martin 0910.2732 normalisation: N_c/(4 pi^2) k^4 v^2 sin^4b f(x); x = 2, k^4 v^2 sin^4b = (190 GeV)^2
    k = (190.0 ** 2 / 246.22 ** 2) ** 0.25
    d = h75.martin_dmh2(k, 1e8, 1000.0, 2e6)
    assert abs(d - 3 / (4 * math.pi ** 2) * 190.0 ** 2 * h75.f_martin(2.0)) < 1e-6
    # VL at the cutoff (model setting): eps = (M_S/Lambda)^2 -> no effect
    assert abs(h75.martin_dmh2(0.52, 69.0, 1.3e16, 1.3e16 ** 2, eps=(2.7e3 / 1.3e16) ** 2)) < 1e-20


def test_pipeline_reproduces_doc73_and_route1_derived_is_zero():
    r = [o for o in json.load(open(D73)) if o["kw"] == {"xt": 0.0, "sgn": 1.0, "mode": "doc60"}][0]
    st = h75.state(r)
    mh, _ = h75.mh_with(r, 0.0, st)
    assert abs(mh - r["Mh"]) < 1e-6
    x_der = (r["M_S"] / r["Lambda"]) ** 2
    assert x_der < 1e-24
    mh1, _ = h75.mh_with(r, h75.route1_dlam(r, x_der, st), st)
    assert abs(mh1 - r["Mh"]) < 1e-9
    # a positive delta lambda raises M_h monotonically
    assert h75.mh_with(r, 0.005, st)[0] > mh + 1.5


def test_soft_rge_gaugino_ratio_and_At_sign():
    r = [o for o in json.load(open(D73)) if o["kw"] == {"xt": 0.0, "sgn": 1.0, "mode": "doc60"}][0]
    low, hi, sm, thr, sp = h75.state(r)
    o = h75.soft_run(hi, r["Lambda"], r["M_S"], m0=1.0, A0=0.0)
    gL = hi.sol(math.log(r["Lambda"]))[:3]
    gS = hi.sol(math.log(r["M_S"]))[:3]
    # one-loop: M_a / g_a^2 is RG invariant; the coupling run is 3-loop, so allow 3%
    for i, k in enumerate(("M1", "M2", "M3")):
        assert abs(o[k] / (gS[i] ** 2 / gL[i] ** 2) - 1) < 0.03
    assert o["At"] < -1.0                       # gaugino-driven A_t is negative (SLHA sign, M3 > 0)
    spec, info = h75.spec_from_soft(o, r["tanb"])
    assert spec is not None and -1.1 < info["Xt_hat"] < -0.6


def test_thr72_msl_default_is_backward_compatible():
    import thr72 as T
    sm = dict(gY=0.36, g2=0.64, g3=1.0, yt=0.85, yb=0.6, ytau=0.7)
    a = T.thresholds72(sm, 60.0, T.Spec(xt=-1.0, msf=1.3), 2.7e3)
    b = T.thresholds72(sm, 60.0, T.Spec(xt=-1.0, msf=1.3, msl=1.3), 2.7e3)
    for k in a:
        assert abs(a[k] - b[k]) < 1e-14
