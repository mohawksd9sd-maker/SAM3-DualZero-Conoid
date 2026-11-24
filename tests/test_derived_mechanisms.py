"""Tests for doc 67: the spectral 'dial' and derived mechanisms for M_t, M_h."""

from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "experiments" / "two_loop_pati_salam"
if str(PKG) not in sys.path:
    sys.path.insert(0, str(PKG))

import derived_mechanisms as dm  # noqa: E402


def test_sigma_moves_higgs_not_top():
    rows = {r["name"][:12]: r for r in dm.c1_sigma()}
    no, yes = rows["no sigma (CC"], rows["sigma at m_R"]
    assert abs(no["Mt"] - yes["Mt"]) < 0.1
    assert 8 < no["Mh"] - yes["Mh"] < 12
    hand = [r for r in dm.c1_sigma() if "by hand" in r["name"]][0]
    assert abs(hand["Mt"] - 172.5) < 0.05 and hand["Mh"] > 145


def test_sigma_sector():
    s = dm.sigma_sector_at_mR()
    assert abs(s["Lambda_boundary"]["lambda_h_sigma"] - 2 * s["Lambda_boundary"]["lambda"]) < 1e-12   # n = 1: kappa = 2 lambda
    assert 0.1 < s["at_m_R"]["threshold_k2_over_ls"] < 0.2
    assert 1 < s["m_sigma_GeV"] / s["m_R_GeV"] < 5


def test_mixed_bidoublet_orthogonality_and_limits():
    r0 = dm.mixed_bidoublet(0.0, scenario="composite")
    assert abs(r0["Mt"] - 190.36) < 0.05            # theta = 0 is the baseline boundary
    c2 = dm.c2_no_first_order()
    assert len(c2["fits"]) == 2
    for f in c2["fits"]:
        assert abs(f["Mt"] - 172.5) < 0.01 and f["Mh"] < 0 and abs(abs(f["ynu_over_yt"]) - 1.87) < 0.01


def test_heat_kernel_moments_and_needed():
    m = dm.moments()
    assert m["flat cutoff (CC choice)"]["f_m2"] == 0.0
    assert abs(m["fermionic entropy h(sqrt u)"]["f_m2"] - 0.125) < 1e-4
    assert abs(m["fermionic entropy h(sqrt u)"]["f0"] - math.log(2)) < 1e-12
    c3 = dm.c3_heat_kernel()
    assert abs(c3["needed_delta_yt2_over_g2"] + 0.356) < 0.002
    assert all(r["Mt"] > 188 for r in c3["rows"])
    assert c3["vev_over_Lambda_sq"] < 1e-24


def test_product_geometry_invariant():
    for r in dm.c4_traces():
        if r["name"].startswith("product geometry"):
            assert abs(r["Mt"] - 190.36) < 0.05 and abs(r["Mh"] - 180.5) < 0.1


def test_gravity_and_SW():
    g = dm.c5_gravity()
    assert g["Gtilde_at_Lambda"] < 1e-7
    assert 127 < g["rows"][1]["Mh"] < 131


def test_thresholds_too_small():
    t = dm.c6_thresholds()
    assert t["dMt_mR_thresholds"] < 3 and t["needed_pct"] > 15
    assert all(abs(r["Mt"] - 190.36) < 1.5 for r in t["rows"])


def test_nothing_derived_passes():
    out = dm.report()
    import report_67 as rp
    rows = rp.all_rows(out)
    assert not any(r["pass"] for r in rows if r["derived"])
