"""Tests for doc 64: cube flavour groups, cube internal spaces, and the brief notes."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "experiments" / "two_loop_pati_salam"
if str(PKG) not in sys.path:
    sys.path.insert(0, str(PKG))

import flavor_cube as fc  # noqa: E402

ORDERS = {"A4": 12, "S4": 24, "O_h": 48, "Delta27": 27, "T'": 24, "T7": 21}


@pytest.fixture(scope="module")
def flav():
    return fc.flavour_report()


def test_group_orders_and_homomorphism():
    for name, fn in fc.GROUPS.items():
        G = fn()
        assert len(G) == ORDERS[name]
        # every rep matrix is unitary
        for el in G:
            for k, M in el.items():
                M = np.asarray(M)
                assert np.allclose(M @ M.conj().T, np.eye(M.shape[0]), atol=1e-9), (name, k)


def test_triplet_singlet_higgs_forces_degenerate_texture(flav):
    for g, a in (("A4", "L=3, R=3, H=1"), ("S4", "L=3, R=3, H=1"), ("O_h", "L=3-, R=3-, H=1+"),
                 ("Delta27", "L=3, R=3, H=1_00"), ("T7", "L=3, R=3, H=1")):
        r = flav[g]["assignments"][a]
        assert r["n_invariants"] == 1
        assert r["random_H"]["forced_degenerate"] and abs(r["random_H"]["share_median"] - 2.0) < 1e-9


def test_forbidden_and_free_assignments(flav):
    assert flav["A4"]["assignments"]["L=3, R=1+1'+1'', H=1"]["n_invariants"] == 0
    assert flav["S4"]["assignments"]["L=3, R=3', H=1"]["n_invariants"] == 0
    assert flav["O_h"]["assignments"]["L=3-, R=3+, H=1+"]["n_invariants"] == 0
    assert flav["A4"]["assignments"]["L=1+1'+1'', R=1+1'+1'', H=1"]["n_invariants"] == 3
    r = flav["A4"]["assignments"]["L=3, R=3, H=3"]
    assert r["n_invariants"] == 2 and not r["random_H"]["forced_degenerate"]


def test_higgs_triplet_rank2_degenerate(flav):
    for g, a in (("S4", "L=3, R=3, H=3"), ("O_h", "L=3-, R=3-, H=3+")):
        r = flav[g]["assignments"][a]["random_H"]
        assert r["forced_rank_le_2"] and r["forced_equal_pair"] and abs(r["share_median"] - 1.0) < 1e-9


def test_a4_tribimaximal_and_theta13_exclusion():
    m = fc.a4_mixing(n=20)
    p = m["prediction_sin2"]
    assert abs(p["s12"] - 1 / 3) < 1e-9 and p["s13"] < 1e-12 and abs(p["s23"] - 0.5) < 1e-9
    assert max(m["spread_over_random_couplings"].values()) < 1e-9   # parameter-independent prediction
    assert m["pulls_sigma"]["s13"] < -30


def test_pipeline_rows():
    p = fc.pipeline()
    base = p["data-consistent texture (share 7e-6)"]
    assert abs(base["Mt"] - 190.36) < 0.05 and abs(base["Mh"] - 180.50) < 0.05
    y1 = p["Y ~ 1 (degenerate, any cube group, 1 parameter)"]
    assert 135 < y1["Mt"] < 147 and y1["mc_over_mt"] == 1.0
    assert 155 < p["rank-2 degenerate (S4/O_h/T' with Higgs triplet)"]["Mt"] < 165


def test_seven_d_chirality():
    z = fc.seven_d_zero_modes()
    for k in ("T3 constant modes (no orbifold)", "T3/Z2 rotation (twist +1)", "T2 x S1/Z2 reflection, no flux (eta +1)"):
        assert z[k][0] == z[k][1]          # vector-like
    assert z["magnetized T2 x S1/Z2 (per flux unit, eta +1)"] == [2, 0] or tuple(z["magnetized T2 x S1/Z2 (per flux unit, eta +1)"]) == (2, 0)
    assert z["2O invariants on internal spinor"] == 0
    assert fc.binary_octahedral_invariants() == 0


def test_cubic_shells_and_kk_shift():
    assert fc.cubic_shells(3) == {1: 6, 2: 12, 3: 8}
    assert fc.kk7_unification_shift(1.0)["delta_alpha_inv"] == 0.0
    assert fc.kk7_unification_shift(0.9)["states"] == 6
    assert fc.kk7_unification_shift(0.7)["delta_alpha_inv"] > 2.0


def test_square_lattice_texture_excluded():
    st = fc.square_texture()
    assert min(r[0] for r in st["rows"]) > 0.02          # light share >> 7e-6
    assert st["Mt_range_by_higgs_direction"][1] < 190.0


def test_notes():
    a = fc.ark_numbers()
    assert a["hits"] == {} and a["numbers_tried"] == 13
    s = sorted(fc.fano_cubic()["singular_values"])
    assert s[0] < 1e-12 and np.allclose(s[1:], 1.0)
