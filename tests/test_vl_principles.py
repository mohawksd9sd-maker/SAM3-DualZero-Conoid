# erratum 2026-11-26: doc 60 baseline M_t 190.36 -> 190.61 after fixing the Buttazzo v4 reference point (173.10 -> 173.34).
"""Tests for doc 63: principles that could force vector-like Higgs-coupled fermions."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "experiments" / "two_loop_pati_salam"
if str(PKG) not in sys.path:
    sys.path.insert(0, str(PKG))

import vl_principles as vp  # noqa: E402


def test_finite_ps_triple_axioms():
    F = vp.FinitePS(False)
    D = F.dirac(1.0)
    assert F.dim == 32 and vp.order_zero(F) < 1e-12
    assert vp.first_order_violation(F, D) < 1e-12
    assert vp.first_order_violation(F, F.dirac(1.0, majorana=2.0)) > 1.0   # Majorana term breaks first order (CCvS)
    assert vp.orientability_residual(F) < 1e-10                             # PS one generation is orientable
    k = vp.ko_signs(F, D)
    assert k["JD-DJ"] < 1e-12 and k["Jgamma+gammaJ"] < 1e-12


def test_vector_like_pair_breaks_orientability_not_first_order():
    F = vp.FinitePS(True)
    D = F.dirac(1.0, 0.7, 0.5)
    assert vp.first_order_violation(F, D) < 1e-12
    assert vp.ko_signs(F, D)["Dgamma+gammaD (off-diagonal D)"] < 1e-12
    assert vp.orientability_residual(F) > 0.5


def test_poincare_duality_impossible_for_ps():
    for vl in (False, True):
        I = vp.intersection_form(vp.FinitePS(vl))
        assert np.allclose(I, -I.T) and abs(np.linalg.det(I)) < 1e-9  # odd-rank antisymmetric


def test_anomalies_fix_ML_eq_MR_only():
    assert vp.anomalies(3, 3)["SU4^3"] == 0 and vp.anomalies(3, 2)["SU4^3"] != 0
    assert vp.anomalies(3, 3, 5)["SU4^3"] == 0      # vector-like pairs are invisible


def test_poincare_sphere():
    assert len(vp.icosians()) == 120
    assert vp.invariant_dims(62) == vp.molien(62)
    d = vp.poincare_sphere_dirac()
    assert d["zero_modes"] == 0 and d["lowest_levels"][0] == {"|lambda|": 1.5, "sign": "-", "mult": 2}
    assert d["lowest_levels"][1]["|lambda|"] == 12.5


def test_full_copies_leave_top_invariant():
    r = vp.full_copies_invariance(2)
    assert abs(r["at_Lambda"]["Mt"] - 190.61) < 0.05 and abs(r["at_Lambda"]["Mh"] - 180.5) < 0.1


def test_gauge_trace_correction():
    req = vp.requirement_formula()
    assert 2.1 < req["da_at_dN0"] < 2.3 and 2.0 < req["slope_da_per_dN"] < 2.1
    c = vp.doc61_row_corrected()
    assert c["with_gauge_trace"]["Mt"] > 190      # doc 61 row fails once its gauge trace is counted
    r = vp.vl_pairs_case(1, 2, "Lambda")
    assert abs(r["Mt"] - 172.5) < 0.01 and 145 < r["Mh"] < 156 and 5.8 < r["share_da"] < 6.6
    r1 = vp.vl_pairs_case(1, 1, "Lambda")
    assert 155 < r1["Mh"] < 165


def test_omega0_cube():
    o = vp.omega0_cube()
    w = o["omega0^3 (0.927)"]
    assert 171.5 < w["Mt"] < 172.2 and 149 < w["Mh_yukawa_only"] < 152 and 137 < w["Mh_higgs_normalisation"] < 141
    assert o["look_elsewhere"]["p_at_least_one"] > 0.7
