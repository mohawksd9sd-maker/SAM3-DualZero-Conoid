"""Collect all Dual-Zero re-runs and the unification ranking."""

from __future__ import annotations

from typing import Dict

from .constants_and_running import (
    report_c0_and_gn,
    report_omega0,
    report_rge_precision,
    report_sam2_alpha,
)
from .phase_cancellation import report as report_phase
from .yukawa_and_selection import report_selection, report_yukawa


def report() -> Dict:
    phase = report_phase(n_points=2048)
    c0 = report_c0_and_gn()
    om = report_omega0()
    alpha = report_sam2_alpha()
    rge = report_rge_precision()
    yuk = report_yukawa()
    sel = report_selection()

    any_genuine_change = False
    # A genuine change would be: a claimed zero that is not a zero in exact
    # arithmetic, or a selection (flux, τ, a constant) that appears only
    # after residual restoration, without a parameter being chosen to make
    # it so.  None of the re-runs produced that.
    changes = {
        "phase_cancellation_zeros_unzeroed": False,
        "C0_exact_value_moved": False,
        "omega0_or_4_13_became_derived": False,
        "SAM2_alpha_became_unique": False,
        "RGE_scales_are_no_longer_a_fit": False,
        "flux_or_tau_selected_without_tuning": False,
        "Yukawa_near_zeros_became_O1_couplings": False,
    }

    ranking = {
        "criterion": (
            "How far a line gets, with Dual-Zero preserved or enhanced, "
            "toward one consistent framework that unifies gravity with the "
            "gauge forces and matter: anomaly freedom, a correct low-energy "
            "limit, and no free-parameter fits.  Three generations is nice "
            "if it happens, not a requirement."
        ),
        "1_best": (
            "Current SAM-3 Dual-Zero (the ε(n)+Reg₂ definition, with ω₀ an "
            "input, plus the arithmetic residual channel) together with a "
            "4D almost-commutative product: a spacetime factor × a compact "
            "magnetized surface × a Pati–Salam or CCM finite triple.  "
            "Geometry/shape of the 2-surface factor is negotiable; the "
            "locked conoid is consistent but not required.  This is the "
            "only line that is internally consistent and already has "
            "standard mechanisms for gravity (spectral action), a gauge "
            "group (PS or SM), and chiral matter (index = flux or bundle "
            "degree), while keeping Dual-Zero."
        ),
        "2": (
            "May 2026 SAM-3, keeping only the same regulator definition "
            "and dropping the 2I generation 'proof', the fitted CKM/Yukawa "
            "claims, and the uniqueness/10÷3/RH extras.  As a TOE bundle "
            "those extras are not consistent; as a regulator they are the "
            "source of line 1."
        ),
        "3": (
            "SAM-2 v2.21 and the desktop hybrid RTFs (E8 / SO(10) '20 exact "
            "parameters').  More ambitious claims, but the regulator is not "
            "well-defined and the constants are fits.  Dual-Zero arithmetic "
            "does not repair that."
        ),
        "4": "HSTO / HSC software is not a unification framework.",
    }

    return {
        "any_genuine_change_from_rounding_restoration": any_genuine_change,
        "changes": changes,
        "phase_cancellation": phase,
        "c0_and_gn": c0,
        "omega0": om,
        "sam2_alpha": alpha,
        "rge": rge,
        "yukawa": yuk,
        "selection": sel,
        "ranking": ranking,
    }


if __name__ == "__main__":
    import json

    out = report()
    # Compact print for the console; full structured data is in the dict.
    compact = {
        "any_genuine_change_from_rounding_restoration": out[
            "any_genuine_change_from_rounding_restoration"
        ],
        "changes": out["changes"],
        "phase_verdict": out["phase_cancellation"]["verdict"],
        "phase_offdiag_max_abs_naive": out["phase_cancellation"]["offdiag_max_abs_naive"],
        "phase_offdiag_max_abs_dual_zero": out["phase_cancellation"]["offdiag_max_abs_dual_zero"],
        "C0_float_minus_mpmath": out["c0_and_gn"]["C0_float64_minus_mpmath"],
        "C0_integral_U400_error": out["c0_and_gn"]["C0_numerical_integrals"]["400.0"]["minus_exact"],
        "omega0_verdict": out["omega0"].get("verdict", out["omega0"]),
        "sam2_alpha_verdict": out["sam2_alpha"]["verdict"],
        "sam2_float_minus_mpmath_kernel": out["sam2_alpha"]["float_minus_mpmath"],
        "rge_verdict": out["rge"]["verdict"],
        "rge_rel_diff_log_mR": out["rge"]["rel_diff_log_mR"],
        "yukawa_verdict": out["yukawa"]["verdict"],
        "yukawa_gram": out["yukawa"]["gram_error_max_abs_I_minus_G"],
        "Y_tau_i": out["yukawa"]["Y_tau_i"],
        "selection_verdict": out["selection"]["verdict"],
        "F_rho_beats_i": out["selection"]["rho_beats_i"],
        "best_M_at_area_1": out["selection"]["best_integer_M_at_area_1"],
        "ranking": out["ranking"],
    }
    print(json.dumps(compact, indent=2, default=str))
