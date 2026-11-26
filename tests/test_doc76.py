"""Doc 76 (stau LSP, two-loop soft running, loop EWSB / m_A, matching-scale error) for candidate #10.
SAM-3 / Dual-Zero originator: Shawn Dykes.  Dual-Zero regulator untouched.  Needs no SOFTSUSY binary:
checks formulas and the committed result files."""
import json
import math
import os
import sys

D = os.path.join(os.path.dirname(__file__), "..", "experiments", "doc76")
sys.path.insert(0, D)

import gravitino76 as G  # noqa: E402
import lhc76  # noqa: E402
from softsusy_2loop import parse_slha  # noqa: E402


def _j(name):
    return json.load(open(os.path.join(D, name)))


def test_gravitino_width_scaling_and_numbers():
    # tau ~ m_G^2 / m^5 for m_G << m
    t1, t2 = G.lifetime_s(5000.0, 50.0), G.lifetime_s(5000.0, 100.0)
    assert abs(t2 / t1 / 4.0 - 1) < 5e-3
    assert abs(G.lifetime_s(2500.0, 50.0) / t1 / 32.0 - 1) < 5e-3
    assert 0.1 < t1 < 2.0                       # ~0.5 s at (m_stau, m_G) = (5 TeV, 50 GeV)
    assert G.width(100.0, 100.0) == 0.0        # kinematic endpoint


def test_omega_bound_consistency():
    for m in (1500.0, 5000.0):
        for k in G.KAPPA:
            mg = G.mG_max_ntp(m, k)
            assert abs(G.omega_ntp(m, mg, k) - G.OMEGA_DM) < 1e-12
    mg, mgl = 50.0, 27000.0
    tr = G.TR_max(mg, mgl)
    assert abs(0.27 * (tr / 1e10) * (100 / mg) * (mgl / 1000) ** 2 - G.OMEGA_DM) < 1e-12


def test_gravitino_analogy_ratio():
    assert abs(G.mG_analogy(1.0, 7.3e15) - 7.3e15 / (math.sqrt(3) * 2.435e18)) < 1e-15
    assert 1.6e-3 < G.mG_analogy(1.0, 7.3e15) < 1.9e-3


def test_slha_parser():
    txt = "Block MSOFT Q= 2.0e+04\n     1  7.0e+03  # M_1\n    43  2.1e+04\nBlock AU Q= 2.0e+04\n  3  3  -2.0e+04\nDECAY 1000015 1.0\n   1.0  2  15 1000039\n"
    b = parse_slha(txt)
    assert b["MSOFT"]["Q"] == 2.0e4 and b["MSOFT"][(1,)] == 7.0e3 and b["MSOFT"][(43,)] == 2.1e4
    assert b["AU"][(3, 3)] == -2.0e4 and "DECAY" not in b


def test_tree_ewsb_identity():
    from rerun76 import tree_ewsb
    s = dict(tanb_run=60.0, mhu2_MS2=-0.3, mhd2_MS2=-0.2)
    mu2, mA2 = tree_ewsb(s)
    t2 = 3600.0
    assert abs(mu2 - (-0.2 + 0.3 * t2) / (t2 - 1)) < 1e-15
    assert abs(mA2 - (-0.5 + 2 * mu2)) < 1e-15


def test_lhc_classify():
    assert lhc76.classify(2000.0).startswith("inside ATLAS")
    assert lhc76.classify(3000.0).startswith("inside CMS")
    assert lhc76.classify(7000.0) == "beyond Run-2 tautau reach"


def test_two_loop_soft_is_small_and_loop_ewsb_lifts_mA():
    ss = _j("results_softsusy_2loop.json")
    assert len(ss) == 5
    for r in ss:
        s1, s2 = r["ss1"], r["ss2"]
        assert s1["ok"] and s2["ok"]
        assert abs(s2["MS_over_M12"] / s1["MS_over_M12"] - 1) < 0.03
        assert abs(s2["Xt_hat"] - s1["Xt_hat"]) < 0.03
        assert 0.40 < s2["mA_over_MS"] < 0.55          # loop-corrected EWSB (SOFTSUSY)


def test_rerun_mt_mh_shifts():
    rr = _j("results_rerun76.json")
    assert len(rr) == 5
    for tag, d in rr.items():
        t = d["doc75"]
        for v in ("soft2L", "ewsb1L", "Qhalf", "Qtwo"):
            assert d[v]["res"]["ok"], (tag, v)
        s2, e = d["soft2L"]["res"], d["ewsb1L"]["res"]
        assert abs(s2["Mt"] - t["Mt"]) < 0.05 and abs(s2["Mh"] - t["Mh"]) < 0.25
        assert abs(e["Mt"] - t["Mt"]) < 0.1 and -0.8 < e["Mh"] - t["Mh"] < 0.0
        assert 125.5 < e["Mh"] < 127.0 and 171.2 < e["Mt"] < 171.8
        # matching-scale variation Q in [M_S/2, 2 M_S]: |dM_h| < 0.5 GeV, |dM_t| < 0.4 GeV
        for v in ("Qhalf", "Qtwo"):
            assert abs(d[v]["res"]["Mh"] - e["Mh"]) < 0.5 and abs(d[v]["res"]["Mt"] - e["Mt"]) < 0.4
        # same physical spectrum: Q_c / c ~ M_S within 10 %
        assert abs(d["Qhalf"]["res"]["M_S"] * 2 / e["M_S"] - 1) < 0.1
        assert abs(d["Qtwo"]["res"]["M_S"] / 2 / e["M_S"] - 1) < 0.1


def test_mA_beyond_lhc_and_stau_still_lsp():
    for r in _j("results_lhc76.json"):
        assert r["mA_doc76_loopEWSB"] > 7000.0 and r["doc76"] == "beyond Run-2 tautau reach"
    for r in _j("results_gravitino76.json"):
        assert r["stau_is_LSP"]
        assert r["tau_s_analogy"] < 5e3                # CBBN
        assert max(r["omega_ntp_analogy"]) < G.OMEGA_DM
