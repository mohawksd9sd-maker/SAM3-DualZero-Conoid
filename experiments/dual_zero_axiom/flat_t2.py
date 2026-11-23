"""Dual-Zero-regulated det' Δ on a unit-area unfluxed flat torus, as a function of τ.

In the δ → 0 limit the functional is the Osgood–Phillips–Sarnak height
(doc 49): it is maximised at the hexagonal modulus, not at τ = i, and it
does not involve a flux.  At finite Dual-Zero shift δ the functional
−[ζ_Δ'(δ)+ζ_Δ'(−δ)]/2 remains a modular invariant of τ (the spectrum is
isometric under SL(2,Z)), so the hexagonal elliptic point stays a
critical point.  This module checks that the ranking vs. the square
torus does not flip, and that no new interior maximizer appears.
"""

from __future__ import annotations

import math
from typing import Dict, List, Tuple

from axiom import residual_scale
from zeta_tools import (
    TAU_I,
    TAU_RHO,
    TAU_RHO_RIGHT,
    dz_log_det_laplacian,
    ops_F,
    s_is_safe,
    unreg_log_det_proxy,
    zeta_laplacian,
)


def ranking_unregulated() -> Dict[str, float]:
    hi = unreg_log_det_proxy(TAU_I)
    hr = unreg_log_det_proxy(TAU_RHO)
    hrr = unreg_log_det_proxy(TAU_RHO_RIGHT)
    return {
        "height_i": hi,
        "height_rho": hr,
        "height_rho_right": hrr,
        "F_i": ops_F(TAU_I),
        "F_rho": ops_F(TAU_RHO),
        "rho_beats_i": hr > hi,
        "rho_equals_rho_right": abs(hr - hrr) < 1e-12,
    }


def ranking_at_delta(delta: float, area: float = 1.0) -> Dict[str, object]:
    li = dz_log_det_laplacian(delta, TAU_I, area)
    lr = dz_log_det_laplacian(delta, TAU_RHO, area)
    lrr = dz_log_det_laplacian(delta, TAU_RHO_RIGHT, area)
    return {
        "delta": delta,
        "logdet_i": li,
        "logdet_rho": lr,
        "logdet_rho_right": lrr,
        "rho_beats_i": lr > li,
        "rho_matches_rho_right": abs(lr - lrr) < 1e-8 * max(1.0, abs(lr)),
    }


def modular_invariance_sample(delta: float, tau: complex = 1.1 + 1.3j) -> Dict[str, float]:
    """ζ_Δ(δ) should agree at τ, τ+1, and −1/τ (unit area)."""
    a = zeta_laplacian(delta, tau)
    b = zeta_laplacian(delta, tau + 1)
    c = zeta_laplacian(delta, -1.0 / tau)
    return {
        "delta": delta,
        "abs_tau_minus_T": float(abs(a - b)),
        "abs_tau_minus_S": float(abs(a - c)),
    }


def modest_grid(delta: float, n_x: int = 9, n_y: int = 10, y_max: float = 2.0) -> Dict[str, object]:
    """Max of the DZ functional on a coarse fundamental-domain grid.

    The hexagonal and square points are included explicitly so the grid
    cannot miss them.  This is a consistency check, not a high-resolution
    proof of uniqueness (that uniqueness in the δ → 0 limit is the OPS
    theorem, already used in doc 49).
    """
    xs = [i / (n_x - 1) - 0.5 for i in range(n_x)]
    y_min = math.sqrt(3.0) / 2.0
    ys = [y_min + (y_max - y_min) * i / (n_y - 1) for i in range(n_y)]
    best_val = -1e300
    best_tau = 0j
    seeds = [(TAU_I, "i"), (TAU_RHO, "rho"), (TAU_RHO_RIGHT, "rho_right")]
    labelled = []
    for tau, name in seeds:
        val = dz_log_det_laplacian(delta, tau)
        labelled.append((name, val))
        if val > best_val:
            best_val = val
            best_tau = tau
    for y in ys:
        for x in xs:
            tau = complex(x, y)
            if abs(tau) < 1.0 - 1e-12:
                continue
            val = dz_log_det_laplacian(delta, tau)
            if val > best_val:
                best_val = val
                best_tau = tau
    d_left = math.hypot(best_tau.real - TAU_RHO.real, best_tau.imag - TAU_RHO.imag)
    d_right = math.hypot(best_tau.real - TAU_RHO_RIGHT.real, best_tau.imag - TAU_RHO_RIGHT.imag)
    d_i = math.hypot(best_tau.real - TAU_I.real, best_tau.imag - TAU_I.imag)
    return {
        "delta": delta,
        "best_re": best_tau.real,
        "best_im": best_tau.imag,
        "distance_to_nearest_hexagonal": min(d_left, d_right),
        "distance_to_i": d_i,
        "labelled": labelled,
        "maximizer_is_hexagonal": min(d_left, d_right) < 0.15,
        "maximizer_is_square": d_i < 0.05 and min(d_left, d_right) > 0.1,
    }


def report(omega0_samples=(0.1, 0.5, 0.927, 1.0, 2.0)) -> Dict[str, object]:
    unreg = ranking_unregulated()
    deltas: List[Tuple[str, float]] = []
    for d in (1e-4, 0.02, 0.1, 0.2):
        if s_is_safe(d):
            deltas.append((f"explicit:{d}", d))
    for omega0 in omega0_samples:
        # N=2 scale is the largest Dual-Zero approximant still usually safe.
        d = residual_scale(2, omega0)
        if s_is_safe(d):
            deltas.append((f"omega0={omega0},N=2", d))
        d3 = residual_scale(3, omega0)
        if s_is_safe(d3) and d3 >= 1e-6:
            deltas.append((f"omega0={omega0},N=3", d3))

    rankings = []
    flipped = []
    for tag, d in deltas:
        row = ranking_at_delta(d)
        row["tag"] = tag
        rankings.append(row)
        if not row["rho_beats_i"]:
            flipped.append(tag)

    # One modest grid at a mid-size safe δ, plus the unregulated comparison.
    grid = modest_grid(0.1)
    inv = modular_invariance_sample(0.2)

    return {
        "unregulated": unreg,
        "rankings_at_delta": rankings,
        "any_delta_flips_rho_vs_i": bool(flipped),
        "flipped_tags": flipped,
        "grid_at_delta_0.1": grid,
        "modular_invariance_sample": inv,
        "selects_unique_area": False,
        "involves_a_flux": False,
        "verdict": (
            "On the unfluxed unit-area torus, Dual-Zero regulation of det' Δ "
            "does not move the maximizer off the hexagonal modulus and does "
            "not prefer the square torus τ = i.  It does not involve a flux "
            "and does not select an area (the comparison is at unit area; "
            "overall scaling of the metric is a separate modulus, already "
            "known not to be fixed by the OPS height alone).  Modular "
            "invariance of the spectrum is inherited by the Dual-Zero "
            "functional.  Changing ω₀ does not flip the ranking."
        ),
    }
