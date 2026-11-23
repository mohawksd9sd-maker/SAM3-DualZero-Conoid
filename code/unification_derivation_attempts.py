"""Honest attempts to derive unification structure from the locked conoid.

Each attempt is classified as derived / partially derived (with the
assumptions stated) / failed.  Null results stay null.  Nothing in this
file is an experimental fit dressed up as a derivation.
"""

from __future__ import annotations

import math
import os
import sys
from typing import Dict, List

import numpy as np

_CODE = os.path.dirname(os.path.abspath(__file__))
if _CODE not in sys.path:
    sys.path.insert(0, _CODE)

from core_geometry import (  # noqa: E402
    C0_EXACT,
    E0_exact,
    has_c4_isometry,
    c4_is_not_a5,
)
from omega0_search import candidate_dimensionless, required_exponents  # noqa: E402
from gn_prefactor_schemes import table as gn_scheme_table, LOCKED_ALPHA  # noqa: E402
from aps_index_theorem import product_collar_index, falomir_flux_for_index  # noqa: E402
from aps_projection import analytic_disk_index  # noqa: E402


# Standard Model gauge algebra, for comparison only.
SM_GAUGE = "SU(3) × SU(2) × U(1)"


def attempt_gauge_group_from_isometry() -> Dict[str, object]:
    """Does the isometry group of the locked metric give the SM gauge group?

    The locked metric has an exact discrete C₄ isometry (v ↦ v + π/2) and
    no continuous rotational isometry: f depends on v, so ∂_v is not
    Killing.  C₄ is not SU(3)×SU(2)×U(1).  In the Connes–Chamseddine
    spectral action the SM gauge group comes from the finite spectral
    triple’s algebra, not from isometries of a 2D Riemannian metric.

    Result: failed.  The conoid isometry group does not determine the
    SM gauge group.
    """
    sample_ok = has_c4_isometry(n_samples=400, ell0=1.0)
    a5 = c4_is_not_a5()
    return {
        "attempt": "gauge group from locked-metric isometries",
        "verdict": "failed",
        "isometry_group": "C4 (discrete), not a continuous U(1)",
        "C4_check_samples": sample_ok,
        "A5_is_isometry": a5["equal"],
        "A5_counterexample": a5,
        "target": SM_GAUGE,
        "reason": (
            "The locked metric is not rotationally invariant.  Its exact "
            "isometry group is the discrete cyclic group C4.  That group "
            "is not the Standard Model gauge group.  Identifying C4 with "
            "a residual discrete symmetry is possible but is not a "
            "derivation of SU(3)×SU(2)×U(1)."
        ),
    }


def attempt_mass_ratios_from_E0() -> Dict[str, object]:
    """Exact channel-energy ratios versus SM charged-lepton ratios.

    Theorem: E_0(m;U) = (j_{ν,1}/U)² with ν=√(m²+1/4), so the ratio
    E_0(m)/E_0(n) is U-independent and equals (j_{ν_m,1}/j_{ν_n,1})².

    These are well-defined geometric numbers.  Identifying them with
    fermion mass ratios is an extra assumption, which we do not make.
    They do not match m_μ/m_e, m_τ/m_μ, or m_τ/m_e.
    """
    U = 1.0  # ratios are U-independent
    e = {m: E0_exact(m, U) for m in (0, 1, 2, 3)}
    ratios = {
        "E0(1)/E0(0)": e[1] / e[0],
        "E0(2)/E0(0)": e[2] / e[0],
        "E0(3)/E0(0)": e[3] / e[0],
        "E0(2)/E0(1)": e[2] / e[1],
        "E0(3)/E0(2)": e[3] / e[2],
        "E0(3)/E0(1)": e[3] / e[1],
    }
    # PDG-style charged-lepton ratios (order of magnitude only; not used
    # as a fit target).  m_μ/m_e ≈ 206.768, m_τ/m_μ ≈ 16.817, m_τ/m_e ≈ 3477.
    sm = {"mu/e": 206.768, "tau/mu": 16.817, "tau/e": 3477.0}
    closest = min(
        abs(ratios["E0(1)/E0(0)"] - sm["mu/e"]),
        abs(ratios["E0(2)/E0(0)"] - sm["mu/e"]),
        abs(ratios["E0(3)/E0(0)"] - sm["mu/e"]),
        abs(ratios["E0(2)/E0(1)"] - sm["mu/e"]),
        abs(ratios["E0(3)/E0(2)"] - sm["tau/mu"]),
    )
    return {
        "attempt": "SM mass ratios from exact E0(m) ratios",
        "verdict": "failed",
        "geometric_ratios": ratios,
        "E0_0_times_U2": e[0],  # should be pi^2
        "sm_charged_lepton_ratios_for_comparison_only": sm,
        "min_absolute_mismatch_to_those_SM_ratios": closest,
        "reason": (
            "The ratios E0(m)/E0(n) are exact and cutoff-independent, but "
            "they are O(1) numbers (about 1.61, 2.75, 4.19, …).  The "
            "charged-lepton mass ratios are two to three orders of "
            "magnitude larger.  No identification of channel index m with "
            "a generation is made, and no match is claimed."
        ),
    }


def attempt_three_generations_from_APS() -> Dict[str, object]:
    """Can the APS index of the 2D Dirac operator on X_{a,b} equal 3?"""
    apap = product_collar_index("antiperiodic", "antiperiodic")
    flux = falomir_flux_for_index(3)
    return {
        "attempt": "three generations from the APS index on the truncated conoid",
        "verdict": "failed for the untwisted Dirac operator",
        "untwisted_AP_AP_index": apap["index"],
        "untwisted_status": apap["status"],
        "partial_route": (
            "The Falomir disk index equals 3 if an auxiliary U(1) flux "
            "satisfies κ ∈ (2, 3].  That κ is not determined by the "
            "locked metric (the spin connection is already included in "
            "the untwisted Dirac operator)."
        ),
        "falomir_kappa_for_index_3": flux["kappa_interval_desc"],
        "kappa_derived": False,
        "analytic_disk_index_at_kappa_2.5": analytic_disk_index(2.5),
        "analytic_disk_index_at_kappa_3": analytic_disk_index(3.0),
        "analytic_disk_index_at_kappa_2": analytic_disk_index(2.0),
        "reason": (
            "Product-collar APS + vanishing 2D Â-genus give index 0 for "
            "the bounding spin structure, independently of the cut radii "
            "and of ℓ₀.  Index 3 is possible only with an extra flux or "
            "a finite spectral triple that already contains three summands; "
            "neither is derived here."
        ),
    }


def attempt_omega0_and_413() -> Dict[str, object]:
    """Re-run the geometric search for ω₀ and the 4/13 exponent."""
    cands = candidate_dimensionless()
    exps = required_exponents()
    # Also compare ω0 to a few exact geometric numbers not in the
    # previous candidate list (channel ratios, ξ_∞, C0/2π, …).
    extra = {
        "C0/(2 pi) = ln 2": C0_EXACT / (2.0 * math.pi),
        "E0(1)/E0(0)": E0_exact(1, 1.0) / E0_exact(0, 1.0),
        "xi_infinity": 0.5,
        "pi/e": math.pi / math.e,
        "1/sqrt(e)": math.e ** -0.5,
    }
    target = 0.927196198773598
    extra_mismatch = {k: abs(v - target) for k, v in extra.items()}
    best_extra = min(extra_mismatch.values())
    # 4/13 versus anything we can honestly form from (C0, C4, ξ, Bessel)
    four_thirteenths = 4.0 / 13.0
    exp_mismatch = {
        name: abs(row["distance_of_p_to_4_13"])
        for name, row in exps.items()
        if isinstance(row, dict) and "distance_of_p_to_4_13" in row
    }
    return {
        "attempt": "unique geometric derivation of omega0 and the 4/13 exponent",
        "verdict": "failed",
        "n_dimensionless_candidates_checked": len(cands),
        "n_required_exponent_rows": len(exp_mismatch),
        "best_extra_geometric_mismatch_to_omega0": best_extra,
        "extra_comparisons": extra,
        "closest_required_q_to_4/13": min(exp_mismatch.values()) if exp_mismatch else None,
        "reason": (
            "No dimensionless quantity built from (C0, C4, ℓ₀-free ratios, "
            "ξ_∞, channel-energy ratios, or standard constants) equals "
            "ω₀ = e^{-4/π²/√e} or produces the exponent 4/13 uniquely.  "
            "Both remain free inputs of the Dual-Zero generator."
        ),
    }


def attempt_GN_prefactor() -> Dict[str, object]:
    """Is α in G_N = α ℓ₀² uniquely fixed by the spectral action?"""
    table = gn_scheme_table()
    alphas = [row["alpha"] for row in table["rows"]]
    # With the exact C0 the conventional 64π/45 can be rewritten, but
    # the rewrite still contains the scheme factor (φ₂, C_SA).
    # G_N = α ℓ0², conventional α = 64π/45.
    rewritten = (
        "If one writes the Einstein–Hilbert coefficient in terms of the "
        "exact finite part C0 = 2π ln 2 and a cutoff moment φ2, then "
        "α = 1 / (c * φ2 * C0) for a conventional factor c (e.g. 16π or "
        "32π²).  The exact C0 removes one numerical uncertainty but does "
        "not remove the scheme dependence in φ2 or in c."
    )
    return {
        "attempt": "unique spectral-action derivation of the G_N prefactor α",
        "verdict": "failed (scheme-dependent)",
        "n_schemes_tabulated": len(table),
        "alpha_min": min(alphas),
        "alpha_max": max(alphas),
        "conventional_64pi_45": LOCKED_ALPHA,
        "C0_exact": C0_EXACT,
        "rewrite_with_exact_C0": rewritten,
        "reason": (
            "Different admissible cutoff moments and volume identifications "
            "produce different α, already visible in the scheme table.  "
            "The conventional value 64π/45 is a choice of scheme, not a "
            "uniqueness theorem."
        ),
    }


def attempt_couplings_from_spectral_action() -> Dict[str, object]:
    """Running / unification of gauge couplings from the spectral action.

    The Chamseddine–Connes spectral action on a product almost-commutative
    geometry can produce gauge couplings, but only after a finite algebra
    and a cutoff function are chosen.  We do not have a derived finite
    algebra from the conoid, nor a unique cutoff.  No coupling unification
    scale or coupling ratios are derived here.
    """
    return {
        "attempt": "gauge-coupling unification from the spectral action on conoid × F",
        "verdict": "failed",
        "reason": (
            "The bosonic spectral action yields Yang–Mills terms whose "
            "coefficients depend on (i) the cutoff moments of the action "
            "and (ii) the traces / KO-dimension data of a finite spectral "
            "triple F.  F is not derived from the locked conoid, and the "
            "cutoff moments are the same scheme data that leave α in G_N "
            "unfixed.  Without those inputs there is no honest unification "
            "prediction (no unique g1:g2:g3 or unique MU)."
        ),
    }


def report() -> Dict[str, object]:
    attempts: List[Dict[str, object]] = [
        attempt_gauge_group_from_isometry(),
        attempt_three_generations_from_APS(),
        attempt_mass_ratios_from_E0(),
        attempt_omega0_and_413(),
        attempt_GN_prefactor(),
        attempt_couplings_from_spectral_action(),
    ]
    verdicts = {a["attempt"]: a["verdict"] for a in attempts}
    return {"attempts": attempts, "verdicts": verdicts}


if __name__ == "__main__":
    import json

    r = report()
    print(json.dumps({"verdicts": r["verdicts"]}, indent=2))
    for a in r["attempts"]:
        print("---")
        print(a["attempt"], ":", a["verdict"])
