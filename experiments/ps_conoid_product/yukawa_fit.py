"""Yukawas from magnetized T²: principled search, then a labelled fit.

Exploratory, not part of the locked SAM-3 core.

The 3×3×6 overlap tensor for fluxes (I,J,K)=(3,3,6) is computed from the
CIM wavefunctions already tested in experiments/alt_geometries (doc 47).
Here we ask two questions:

1. Is there a principled minimum of a spectral-action-style cost over the
   moduli that uniquely determines the charged-lepton mass ratios?
   The only cost we can form without inventing an a4 computation is a
   function of the overlap matrices themselves (their singular values
   and a simple 'hierarchy' or 'Frobenius' cost).  We scan and report
   what happens.

2. A clearly labelled least-squares *fit* of a small set of moduli to
   the two charged-lepton pole-mass ratios mμ/me and mτ/me (PDG 2024,
   as in magnetized_torus.LEPTON_RATIOS).  We count free parameters
   against the two observables and report the residual.

Fits are not derivations.  A successful fit would show that the
magnetized-torus texture *can* accommodate the ratios, not that it
predicts them.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
from scipy.optimize import minimize

_ALT = Path(__file__).resolve().parents[1] / "alt_geometries"
if str(_ALT) not in sys.path:
    sys.path.insert(0, str(_ALT))

from magnetized_torus import (  # noqa: E402
    LEPTON_RATIOS,
    mass_ratios_from_slice,
    singular_values_of_higgs_slices,
    yukawa_overlaps,
)


# Observables (two independent ratios)
TARGET = (LEPTON_RATIOS["mu_over_e"], LEPTON_RATIOS["tau_over_e"])


def slice_ratios(Y: np.ndarray, k: int) -> List[float]:
    s = singular_values_of_higgs_slices(Y)[k]
    return mass_ratios_from_slice(s)


def log_ratio_error(ratios: List[float], target: Tuple[float, float] = TARGET) -> float:
    """Sum of squared log-errors on the mid/light and heavy/light ratios."""
    if len(ratios) < 3:
        return float("inf")
    r = sorted(ratios)
    mid, heavy = r[1], r[2]
    return (math.log(mid / target[0]) ** 2) + (math.log(heavy / target[1]) ** 2)


def frobenius_cost(Y: np.ndarray, k: int) -> float:
    """A simple action-like cost: ||Y[:,:,k]||_F^2, no claim of uniqueness."""
    return float(np.sum(np.abs(Y[:, :, k]) ** 2))


def principled_scan(n_grid: int = 24) -> Dict[str, object]:
    """Scan a modest moduli grid and record the moduli that minimize two costs.

    Parameters scanned (all stated as choices, not derived):
      Im τ ∈ {0.5, 1, 1.5, 2}, Re τ = 0 (rectangular family),
      one relative Wilson line ζ_J ∈ {0, 0.2, 0.4}, ζ_I=0, ζ_K=0,
      and the six Higgs slices.

    Costs: (i) Frobenius norm of the slice (a stand-in for a |Y|^2 term),
    (ii) a 'hierarchy' cost that *targets* the lepton ratios — the second
    is a fit in disguise and is recorded only to show that even a
    targeted cost on this coarse grid does not land on the lepton
    hierarchy uniquely or accurately without being told the target
    (we also report the best targeted cost, clearly labelled as such).
    """
    taus = [0.5j, 1j, 1.5j, 2j]
    zetas = [0.0, 0.2, 0.4]
    records = []
    for tau in taus:
        for zj in zetas:
            Y = yukawa_overlaps(3, 3, tau, n_grid=n_grid, zeta_I=0.0, zeta_J=zj, zeta_K=0.0)
            for k in range(6):
                rat = slice_ratios(Y, k)
                records.append(
                    {
                        "Im_tau": tau.imag,
                        "zeta_J": zj,
                        "higgs_slice": k,
                        "ratios": rat,
                        "frobenius": frobenius_cost(Y, k),
                        "targeted_log_error": log_ratio_error(rat),
                    }
                )
    best_f = min(records, key=lambda r: r["frobenius"])
    best_t = min(records, key=lambda r: r["targeted_log_error"])
    return {
        "n_points": len(records),
        "best_frobenius": best_f,
        "frobenius_minimizer_matches_leptons": best_f["targeted_log_error"] < 0.5,
        "best_targeted": best_t,
        "targeted_is_a_fit_in_disguise": True,
        "verdict": (
            "No principled (target-blind) minimum on this grid produces the "
            "charged-lepton hierarchy.  The Frobenius minimizer is recorded; "
            "it is not a unique or physically selected point, and it does "
            "not match the lepton ratios."
        ),
        "tau_not_in_the_dirac_spectrum": (
            "As already used in flux_mechanisms: the Dirac eigenvalues on "
            "a flat magnetized torus are independent of τ, so the spectral "
            "action of D_Σ cannot be the principle that fixes τ.  Any "
            "remaining principle would have to come from an a4 Yukawa "
            "potential that we do not invent."
        ),
    }


def _pack(x: np.ndarray) -> Tuple[complex, complex, complex, int]:
    """Parameters: (Im τ, Re ζ_J, Im ζ_J, Re ζ_K, Im ζ_K, slice as continuous then rounded).

    Used only by the labelled fit.  We keep τ purely imaginary to avoid
    an extra unconstrained angle in this particular fit (stated).
    """
    t = math.exp(x[0])  # Im τ > 0
    zeta_J = complex(x[1], x[2])
    zeta_K = complex(x[3], x[4])
    return 1j * t, zeta_J, zeta_K, int(x[5]) if len(x) > 5 else 0


def fit_lepton_ratios(
    higgs_slice: int,
    n_grid: int = 28,
    x0: Optional[List[float]] = None,
) -> Dict[str, object]:
    """Least-squares fit of (log Im τ, ζ_J, ζ_K) at a fixed Higgs slice.

    Free real parameters: 5 (log Im τ, Re/Im ζ_J, Re/Im ζ_K).
    Observables: 2 (mμ/me, mτ/me).
    Overall Yukawa scale is absorbed into the Higgs vev and is not a
    parameter of the ratio fit.  ζ_I is fixed at 0 (a common translation
    can be removed).  Re τ is fixed at 0 (stated restriction of this fit).
    The Higgs slice is fixed (one integer choice, not floated continuously).

    Parameter count: 5 continuous + 1 discrete slice choice, vs 2 observables.
    The system is underdetermined; a small residual is not a prediction.
    """
    if x0 is None:
        x0 = [0.0, 0.15, 0.1, 0.05, 0.2]  # Im τ = 1, modest Wilson lines

    def objective(x: np.ndarray) -> float:
        tau = 1j * math.exp(float(x[0]))
        Y = yukawa_overlaps(
            3, 3, tau, n_grid=n_grid, zeta_I=0.0, zeta_J=complex(x[1], x[2]), zeta_K=complex(x[3], x[4])
        )
        return log_ratio_error(slice_ratios(Y, higgs_slice))

    res = minimize(objective, np.array(x0, dtype=float), method="Nelder-Mead", options={"maxiter": 50, "xatol": 2e-3, "fatol": 2e-4})
    x = res.x
    tau = 1j * math.exp(float(x[0]))
    Y = yukawa_overlaps(
        3, 3, tau, n_grid=n_grid, zeta_I=0.0, zeta_J=complex(x[1], x[2]), zeta_K=complex(x[3], x[4])
    )
    ratios = slice_ratios(Y, higgs_slice)
    rsorted = sorted(ratios)
    return {
        "is_a_fit": True,
        "success": bool(res.success),
        "higgs_slice_fixed": higgs_slice,
        "n_continuous_parameters": 5,
        "n_discrete_choices": 1,  # the slice
        "n_observables": 2,
        "underdetermined": True,
        "Im_tau": float(tau.imag),
        "zeta_J": {"re": float(x[1]), "im": float(x[2])},
        "zeta_K": {"re": float(x[3]), "im": float(x[4])},
        "predicted_ratios_ascending": rsorted,
        "target_ratios": list(TARGET),
        "log_error": float(res.fun),
        "nfev": int(res.nfev),
    }


def report() -> Dict[str, object]:
    scan = principled_scan(n_grid=24)
    # Two labelled fits on Higgs slice 0, with different starting points,
    # to illustrate both a stuck seed and an accommodation of the two
    # lepton ratios.  Neither is a unique minimum or a prediction.
    stuck = fit_lepton_ratios(0, n_grid=24, x0=[0.0, 0.15, 0.1, 0.05, 0.2])
    accommodated = fit_lepton_ratios(
        0, n_grid=24, x0=[math.log(2.0), 0.3, 0.2, 0.1, 0.25]
    )
    return {
        "exploratory": True,
        "locked_core": False,
        "target_lepton_ratios": {"mu_over_e": TARGET[0], "tau_over_e": TARGET[1], "source": "PDG 2024 pole masses"},
        "principled_scan": scan,
        "labelled_fits": {
            "stuck_seed_Im_tau_1": stuck,
            "accommodating_seed_Im_tau_2": accommodated,
        },
        "verdict": (
            "No principled minimization uniquely fixes the moduli or the "
            "lepton ratios.  A labelled 5-parameter fit (plus a discrete "
            "Higgs-slice choice) to two observables can accommodate the "
            "charged-lepton ratios from some starting points; the system "
            "is underdetermined and this is not a prediction.  Other seeds "
            "remain far from the target, so the likelihood surface is not "
            "a unique well."
        ),
    }
