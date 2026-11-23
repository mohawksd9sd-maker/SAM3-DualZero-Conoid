"""Known-answer and hermiticity tests for the 2D Dirac discretisation."""
from __future__ import annotations

import numpy as np
import pytest

from aps_hermitian import (
    Grid2D,
    analytic_torus_eigs,
    build_hermitian_dirac,
    conoid_spectrum_hermitian,
    convergence_study,
    hermiticity_error,
    legacy_symmetrised_torus,
    lowest_abs_eigs,
    torus_known_answer,
)


def test_antiperiodic_torus_known_answer():
    # N=16 is cheap and already has max error ~ 4.5e-3 (second order)
    report = torus_known_answer(N=16, k_compare=8)
    assert report["hermiticity_error"] < 1e-12
    assert report["max_abs_error"] < 0.01


def test_convergence_order_near_two():
    study = convergence_study(N_list=(8, 12, 16, 24))
    # central differences => p ≈ 2
    assert abs(study["log_log_slope"] + 2.0) < 0.08
    for row in study["rows"]:
        assert row["hermiticity_error"] < 1e-12


def test_legacy_symmetrisation_is_not_the_dirac_operator():
    legacy = legacy_symmetrised_torus(N=12)
    # The lowest eight |eigenvalues| of the symmetrised matrix do not match
    # the analytic periodic Dirac tower (0, 1, 1, √2, ...).
    assert legacy["legacy_recovers_first_nonzero_dirac_mode"] is False
    num = np.array(legacy["legacy_abs_eigs"])
    exact = np.array(legacy["analytic_lowest_abs"])
    assert np.linalg.norm(num - exact) > 0.5


def test_truncated_conoid_operator_is_hermitian():
    report = conoid_spectrum_hermitian(Nu=16, Nv=16, u_max=5.0, aps_strength=6.0, k=6)
    assert report["hermiticity_error"] < 1e-12
    ev = np.array(report["evals"])
    assert ev.shape[0] == 6
    assert np.all(np.isfinite(ev))


def test_analytic_torus_lowest_mode():
    # Antiperiodic, L=2π: k = n+1/2, lowest |λ| = √(0.5^2+0.5^2) = √0.5
    ev = analytic_torus_eigs(2 * np.pi, 2 * np.pi, n_max=4, antiperiodic_u=True, antiperiodic_v=True)
    assert abs(abs(ev).min() - np.sqrt(0.5)) < 1e-12
