"""ω0 is not derived; G_N prefactor is scheme-dependent."""
from __future__ import annotations

import math

from gn_prefactor_schemes import LOCKED_ALPHA, LOCKED_PRODUCT, alpha_from, table, vol_schemes
from omega0_search import TARGET, candidate_dimensionless, report, required_exponents, dual_zero_sensitivity


def test_no_simple_constant_equals_omega0():
    cands = candidate_dimensionless()
    for name, val in cands.items():
        # coincidences such as sqrt(6/7) are still more than 10^{-3} away
        assert abs(val - TARGET) > 1e-3, name


def test_natural_radii_do_not_give_0927_and_required_p_is_not_4_13():
    ex = required_exponents()
    for name in ("1/|K|_max", "1/sqrt(|K|_max)", "ell0", "2*ell0"):
        assert abs(ex[name]["omega0_if_4_13"] - TARGET) > 0.2
        assert abs(ex[name]["p_required_for_0.927"] - 4.0 / 13.0) > 0.2


def test_dual_zero_weights_scale_linearly_with_omega0():
    rows = {r["omega0"]: r for r in dual_zero_sensitivity()["rows"]}
    ratio = rows[1.00]["sum_abs_eps_nle20"] / rows[0.927]["sum_abs_eps_nle20"]
    assert abs(ratio - 1.00 / 0.927) < 1e-12


def test_convention_lock_product():
    t = table()
    assert abs(t["convention_lock"]["recorded_alpha"] - LOCKED_ALPHA) < 1e-15
    assert abs(t["convention_lock"]["equivalent_product_C_SA_phi2_Vol"] - LOCKED_PRODUCT) < 1e-15
    # α depends on the volume scheme
    alphas = {row["alpha"] for row in t["rows"] if row["C_SA_name"].startswith("1/(24")}
    assert len(alphas) > 1
    # none of the tabulated hypotheses is forced to equal 64π/45
    for row in t["rows"]:
        if row["Vol_name"] == "C0_finite_part":
            assert abs(row["alpha"] / LOCKED_ALPHA - 1.0) > 0.1


def test_search_conclusion_is_negative():
    r = report()
    assert "free input" in r["conclusion"]
