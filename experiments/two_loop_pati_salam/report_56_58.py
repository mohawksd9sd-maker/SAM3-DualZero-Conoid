"""Numbers quoted in docs 56-58 (run: python report_56_58.py)."""

from __future__ import annotations

import json

import finite_triple
import higgs_masses
import phenomenology as ph
from rge import PDG, solve_unification


def report():
    two = solve_unification(PDG, "composite", 2)
    one = solve_unification(PDG, "composite", 1)
    w15 = solve_unification(PDG, "with15", 2)
    out = {
        "doc56_finite_triple": finite_triple.report(),
        "doc57_proton": {
            "operators": {k: {kk: str(vv) for kk, vv in v.items()} for k, v in ph.operator_table().items()},
            "generic_d6_at_Lambda_two_loop_years": ph.generic_d6_lifetime(two["Lambda_GeV"], two["alpha_U_inv"]),
            "generic_d6_at_Lambda_one_loop_years": ph.generic_d6_lifetime(one["Lambda_GeV"], one["alpha_U_inv"]),
            "generic_d6_at_Lambda_with15_years": ph.generic_d6_lifetime(w15["Lambda_GeV"], w15["alpha_U_inv"]),
            "generic_d6_at_m_R_years": ph.generic_d6_lifetime(two["m_R_GeV"], two["alpha_U_inv"]),
            "kappa_max_at_Lambda": ph.kappa_max(two["Lambda_GeV"], two["alpha_U_inv"]),
            "superK_bound_years": ph.SUPERK_P_EPI0_YEARS,
            "rare_decays": ph.rare_decay_check(two["m_R_GeV"]),
        },
        "doc58_higgs_masses": {
            "PS_n1_with_sigma": higgs_masses.predict(1.0, True, two),
            "PS_n1_no_sigma": higgs_masses.predict(1.0, False, two),
            "mH_observed_top_with_sigma": higgs_masses.mH_with_observed_top(True),
            "mH_observed_top_no_sigma": higgs_masses.mH_with_observed_top(False),
            "n_scan_with_sigma": higgs_masses.n_scan(),
            "seesaw_M_N_eq_m_R": ph.seesaw(two["y_t_at_m_R"], two["m_R_GeV"]),
        },
    }
    return out


if __name__ == "__main__":
    print(json.dumps(report(), indent=1, default=float))
