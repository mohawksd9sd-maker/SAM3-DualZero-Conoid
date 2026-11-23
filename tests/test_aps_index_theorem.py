"""Analytic APS index of the untwisted Dirac operator on the truncated conoid."""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))

from aps_index_theorem import (
    eta_bar_circle_dirac,
    falomir_flux_for_index,
    product_collar_index,
    report,
    xi_by_quadrature,
    xi_mean_holonomy,
)
from aps_projection import analytic_disk_index


def test_xi_closed_form_matches_quadrature():
    for u in (0.2, 0.5, 1.0, 2.0, 6.0, 20.0):
        a = xi_mean_holonomy(u)
        b = xi_by_quadrature(u, n=8000)
        assert abs(a - b) < 1e-6
        assert 0.0 < a <= 0.5 + 1e-12


def test_xi_limits():
    assert xi_mean_holonomy(1e-4) < 0.05
    assert abs(xi_mean_holonomy(1e4) - 0.5) < 1e-6


def test_xi_monotone_up_to_half():
    us = [0.1, 0.3, 1.0, 3.0, 10.0, 40.0]
    xs = [xi_mean_holonomy(u) for u in us]
    assert all(xs[i] < xs[i + 1] for i in range(len(xs) - 1))
    assert xs[-1] < 0.5 + 1e-14


def test_product_collar_AP_AP_index_is_zero():
    r = product_collar_index("antiperiodic", "antiperiodic")
    assert r["bulk_A_hat"] == 0.0
    assert r["inner"]["h"] == 0.0
    assert r["outer"]["h"] == 0.0
    assert abs(r["inner"]["eta_bar"]) < 1e-14
    assert abs(r["outer"]["eta_bar"]) < 1e-14
    assert r["index"] == 0
    assert r["three_not_attained"] is True


def test_periodic_end_contributes_half():
    r = eta_bar_circle_dirac(0.0, "periodic")
    assert r["h"] == 1.0
    assert r["eta"] == 0.0
    assert r["eta_bar"] == 0.5


def test_periodic_periodic_index_in_unit_range_not_three():
    r = product_collar_index("periodic", "periodic")
    assert r["three_not_attained"] is True
    if r["index"] is not None:
        assert r["index"] in (-1, 0, 1)
        assert r["index"] != 3


def test_falomir_index_3_needs_underived_flux():
    flux = falomir_flux_for_index(3)
    assert flux["derived_from_conoid_metric"] is False
    lo, hi = flux["kappa_interval"]
    assert lo == 2.0 and hi == 3.0
    assert analytic_disk_index(2.5) == 3
    assert analytic_disk_index(3.0) == 3
    assert analytic_disk_index(2.0) == 2  # κ = 2 is the top of the index-2 slot


def test_report_flags_three_generations_refuted_for_untwisted():
    r = report()
    assert r["untwisted_index_AP_AP"] == 0
    assert r["three_generations_from_untwisted_index"] == "refuted"
    assert r["xi_u_1e4"] > 0.49
    assert max(row["abs_diff"] for row in r["xi_rows"]) < 1e-5
