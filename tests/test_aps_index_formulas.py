"""Analytic APS-disk formulae (Falomir et al., JMP 39 (1998)).

These tests check the *formulas*, and a modest numerical Bessel check of
the mode-by-mode scheme for the n=1 family (which is more stable in that
scheme than J_0). A complete, Hermitian 2D disk discretisation that
reproduces the full Bessel tower and the nonzero-flux index is not
claimed.
"""
from __future__ import annotations

import numpy as np
from scipy.special import jn_zeros

from aps_disk_modes import analytic_disk_index, aps_k, mode_evals, nearly_real, unique_bessel_positives
from aps_projection import eta_circle_analytic


def test_falomir_index_formula():
    assert aps_k(0.0) == -1 and analytic_disk_index(0.0) == 0
    assert analytic_disk_index(0.5) == 1
    assert analytic_disk_index(1.0) == 1  # k=0, since 0 < 1 <= 1
    assert analytic_disk_index(1.5) == 2
    assert analytic_disk_index(2.5) == 3


def test_eta_circle_noninteger_and_integer():
    a = eta_circle_analytic(0.5)
    assert a["h"] == 0 and abs(a["eta_0"] - 0.0) < 1e-15  # 1-2*{1/2}=0
    b = eta_circle_analytic(0.0)
    assert b["integer_kappa"] and b["h"] == 1 and abs(b["eta_bar"] - 0.5) < 1e-15
    c = eta_circle_analytic(1.25)
    assert abs(c["eta_0"] - (1.0 - 2.0 * 0.25)) < 1e-15


def test_mode_n1_nearly_real_evals_approach_J1_zeros():
    """The n=1 radial APS scheme reproduces the first J_1 zero to ~0.02 at N=80."""
    ev = nearly_real(mode_evals(1, R=1.0, N=80, kappa=0.0), imag_abs=0.05)
    pos = np.sort(ev[ev > 0.5])
    j1 = float(jn_zeros(1, 1)[0])
    assert np.min(np.abs(pos - j1)) < 0.03


def test_kappa0_has_no_near_zero_in_n1_sector():
    ev = nearly_real(mode_evals(1, R=1.0, N=80, kappa=0.0), imag_abs=0.05)
    assert np.min(np.abs(ev)) > 0.5
