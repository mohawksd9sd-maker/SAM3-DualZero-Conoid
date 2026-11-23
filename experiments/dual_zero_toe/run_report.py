"""Print the compact Dual-Zero model re-run report.

Usage, from the repository root:

    PYTHONPATH=.:experiments python experiments/dual_zero_toe/run_report.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
EXPERIMENTS = REPO / "experiments"
for p in (REPO, EXPERIMENTS):
    s = str(p)
    if s not in sys.path:
        sys.path.insert(0, s)

from dual_zero_toe.report import report  # noqa: E402

if __name__ == "__main__":
    out = report()
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
