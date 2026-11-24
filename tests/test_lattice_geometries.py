"""Tests for doc 62: hexagonal ("Flower of Life") and D_4 ("4D Flower of Life") internal spaces."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "experiments" / "two_loop_pati_salam"
if str(PKG) not in sys.path:
    sys.path.insert(0, str(PKG))

import lattice_geometries as lg  # noqa: E402


def test_hex_zn_counts_match_literature_even_M():
    for N in (3, 6):
        for M in range(2, 13, 2):
            assert lg.literature_match(M, N) is True
            s = lg.sector_counts(M, N)
            assert sum(s.values()) == M


def test_odd_M_needs_scherk_schwarz_phase():
    for M in (1, 3, 5):
        assert lg.sector_counts(M, 3) is None


def test_three_generations_not_forced():
    assert lg.three_generation_fluxes(3)["invariant_sector_dim_3"] == [6, 8, 10]
    assert lg.three_generation_fluxes(6, 18)["invariant_sector_dim_3"] == [12, 14, 16]


def test_hex_texture_is_order_one():
    tex = lg.hex_textures(n_grid=30)
    for v in tex.values():
        assert v["sigma2_over_sigma1_min"] > 0.1        # charm/top would be O(1): excluded by data
        assert v["fraction_with_sigma2_below_0.01"] == 0.0
    ratios = tex["T2_hex_(3,3,6)"]["basis_higgs_ratios"]
    assert any(abs(r[1] - r[2]) < 1e-8 for r in ratios)  # symmetric point -> degeneracies


def test_d4_hurwitz_facts():
    d = lg.d4_report()
    assert d["hurwitz_units"] == 24 and d["omega_order3"] and d["omega_is_integer_matrix"]
    assert d["fixed_points_T4_Z3"] == 9 and d["chi_resolution"] == 24
    assert lg.d4_shells(4) == {1: 24, 2: 24, 3: 96, 4: 24}
    assert not lg.d4_vs_hex_product()["A2xA2_sublattice_of_D4"]


def test_t4_indices():
    t = lg.t4z3_generations()
    assert abs(t["K3_check_no_flux"] - 2.0) < 1e-12
    assert len(t["three_generation_solutions"]) > 1
    c = lg.t4_index_census()
    assert 0.05 < c["fraction_index_3"] < 0.2


def test_kk_modes_below_lambda_spoil_unification():
    assert lg.kk_unification_shift(1.0)["kk_states_below_Lambda"] == 0
    s = lg.kk_unification_shift(0.9)
    assert s["kk_states_below_Lambda"] == 24 and s["delta_alpha_inv_4_minus_L"] > 2


def test_pipeline_rows():
    rows = lg.pipeline_rows()
    for v in rows.values():
        assert v["Mt"] > 190
