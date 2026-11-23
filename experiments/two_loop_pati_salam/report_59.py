"""Numbers quoted in doc 59 (run: python report_59.py)."""

from __future__ import annotations

import json

import missing_pieces as mp


def report():
    st = mp.Setup()
    return {
        "a_sigma": mp.sigma_variations(st),
        "b_n_free": mp.n_free_study(),
        "b_two_loop_top": mp.two_loop_top_study(),
        "c_thresholds": mp.threshold_propagation(40),
        "d_required_shifts": mp.required_boundary_shifts(st),
        "ledger": mp.ledger(),
        "clifford": {"Cl(5,0)": mp.clifford(5, 0), "Cl(0,5)": mp.clifford(0, 5),
                     "Cl(4,0)": mp.clifford(4, 0),
                     "dim_commutant_grading_in_M2H": mp.quaternion_commutant_of_grading()},
        "mbb": mp.mbb_ranges(),
    }


if __name__ == "__main__":
    print(json.dumps(report(), indent=1, default=float))
