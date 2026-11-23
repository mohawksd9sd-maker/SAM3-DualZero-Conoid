"""Dual-Zero and the product spectral action (magnetized surface × PS / CCM).

The Seeley–DeWitt integrands of the product Y = X × Σ, with integer
flux M on Σ, were already analysed in docs 48–50.  They are smooth
functions of (A, M) and independent of τ on a magnetized flat torus.
Reg₂ acting on a smooth function of a spectral parameter returns that
function in the δ → 0 limit, so the Dual-Zero axiom does not change:

  - ∂S/∂M = 0 only at M=0 (for f0 ≠ 0);
  - any stationary area at fixed M is proportional to |M| and depends
    on underived Wilson coefficients and on Λ;
  - τ does not enter these coefficients.

At a pole of a spectral zeta, Reg₂ extracts the finite part and drops
the residue.  The residue is precisely the Weyl / volume Seeley term.
Using Reg₂ in place of residue extraction would discard that term, which
is a different and worse truncation, not a new selection principle
(compare the forbidden ε(n)-weighted heat trace in doc 51).  The
finite-part functional was already studied in doc 50 and does not
select M=3.

This module re-uses the existing product action and records those facts
under the Dual-Zero axiom, including a Pati–Salam / CCM reading: the
internal finite triple does not alter the (A, M) Seeley structure used
here (docs 45, 48).
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict

_FC = Path(__file__).resolve().parents[1] / "further_candidates"
if str(_FC) not in sys.path:
    sys.path.insert(0, str(_FC))

from spectral_action_moduli import (  # noqa: E402
    C0,
    INT_R_COMPLETE,
    dS_dM_sign_term,
    report as sa_report,
    scan_no_interior_M_extremum,
    stationary_A_at_fixed_M,
    area_leading,
    TIP_LENGTH_UNIT,
)

from axiom import reg2_finite


def seeley_densities_are_smooth_in_moduli() -> bool:
    """S(A) at fixed M, coefficients, and Λ is smooth for A>0, so Reg₂(S)=S."""
    def S_of_A(A: float) -> float:
        area_X = C0
        M = 3
        f4, f2, f0, f_bdry, Lam = 1.0, 1.0, 1.0, 1.0, 1.0
        L = TIP_LENGTH_UNIT
        vol = area_X * A
        int_R = INT_R_COMPLETE * A
        int_F2 = area_X * (2.0 * 3.141592653589793 * M) ** 2 / A
        vol_bdry = L * A
        return f4 * Lam**4 * vol + f2 * Lam**2 * int_R + f0 * int_F2 + f_bdry * Lam**3 * vol_bdry

    A0 = 2.0
    return abs(reg2_finite(S_of_A, A0, 1e-5) - S_of_A(A0)) < 1e-6


def report() -> Dict[str, object]:
    base = sa_report()
    scan = scan_no_interior_M_extremum()
    return {
        "internal_space": "Pati-Salam or CCM finite triple (spectator for these integrands)",
        "tau_enters_seeley_coefficients_on_magnetized_T2": False,
        "reg2_of_smooth_action_in_A_recovers_action": seeley_densities_are_smooth_in_moduli(),
        "partial_S_partial_M_vanishes_only_at_M_0": scan["partial_M_vanishes_only_at_M_0"],
        "finite_part_stationary_A_at_fixed_M": base["finite_part_stationary_A_at_fixed_M"],
        "reg2_at_a_pole_drops_the_residue_not_a_selection_principle": True,
        "verdict": (
            "In the almost-commutative product with a Pati–Salam or CCM "
            "finite triple, Dual-Zero as Reg₂ on functions of a spectral "
            "parameter does not change the Seeley analysis of docs 48–50: "
            "there is no interior extremum that selects M=3, a stationary "
            "area at fixed M is not a unique geometric output, and τ does "
            "not enter.  Replacing residue extraction by Reg₂ would drop "
            "the Weyl term and is not used."
        ),
    }
