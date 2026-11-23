"""Collect Dual-Zero axiom well-posedness and selection-scan results (doc 52)."""

from __future__ import annotations

from typing import Dict

from axiom import well_posedness_report
from flat_t2 import report as flat_report
from magnetized_t2 import report as magnetized_report
from orbifold_z4 import report as z4_report
from product_action import report as product_report
from sphere_monopole import report as sphere_report


def report() -> Dict[str, object]:
    wp = well_posedness_report()
    mag = magnetized_report()
    flat = flat_report()
    z4 = z4_report()
    sph = sphere_report()
    prod = product_report()
    selected = {
        "M_3_without_tuning": False,
        "unique_area_without_tuning": False,
        "unique_tau_forced_to_i_by_DualZero": False,
        "hexagonal_tau_is_still_preferred_on_unfluxed_T2": (
            flat["unregulated"]["rho_beats_i"] and not flat["any_delta_flips_rho_vs_i"]
        ),
        "any_new_selection_from_DualZero": False,
    }
    return {
        "exploratory": True,
        "locked_core": False,
        "well_posedness": wp,
        "magnetized_T2": mag,
        "unfluxed_T2": flat,
        "T2_over_Z4": z4,
        "sphere_monopole": sph,
        "product_PS_CCM": prod,
        "selection": selected,
        "verdict": (
            "The standalone Dual-Zero axiom is well-posed as a symmetric "
            "average on functions of a spectral parameter, with ω₀ an input, "
            "and is not used as an ε(n) heat-trace weight.  Applied without "
            "fitting to the magnetized torus, the unfluxed torus, T²/Z₄, "
            "the monopole sphere, and the Pati–Salam / CCM product, it does "
            "not select M=3 or a unique area, and it does not override the "
            "known hexagonal preference for det' Δ or the C₄ requirement "
            "τ=i.  Honest null; no new selection principle."
        ),
    }


if __name__ == "__main__":
    import json

    out = report()
    # Drop bulky per-delta records from the printed summary.
    print(json.dumps(
        {
            "well_posedness": out["well_posedness"],
            "selection": out["selection"],
            "magnetized_verdict": out["magnetized_T2"]["verdict"],
            "flat_verdict": out["unfluxed_T2"]["verdict"],
            "z4_verdict": out["T2_over_Z4"]["verdict"],
            "sphere_verdict": out["sphere_monopole"]["verdict"],
            "product_verdict": out["product_PS_CCM"]["verdict"],
            "overall": out["verdict"],
            "any_delta_flips_rho_vs_i": out["unfluxed_T2"]["any_delta_flips_rho_vs_i"],
            "M3_only_when_area_tuned": out["magnetized_T2"]["omega_sensitivity"][
                "M3_occurs_only_when_area_is_tuned"
            ],
            "z4_fluxes_with_dim_3": out["T2_over_Z4"]["fluxes_with_invariant_sector_dimension_3"],
        },
        indent=2,
        default=str,
    ))
