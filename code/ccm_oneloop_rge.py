"""One-loop RG running of the CCM boundary conditions, vs measured couplings.

All beta functions and the unification relation are taken from
Chamseddine–Connes, Fortschr. Phys. 58 (2010) 553–600, arXiv:1004.0464,
eqs. (5.51) and (6.1)–(6.8).  The one-loop coefficients are the standard
SM values in the hypercharge convention used there:

    β_{g_i} = (4π)^{-2} b_i g_i^3,    b = (41/6, −19/6, −7),

which integrate to CC2010 (6.4)–(6.6).  g1 is the SM hypercharge coupling.

This module reproduces the literature statement that the three couplings
do not meet at one scale (CC2010, below (6.8)), and records a Higgs-mass
check against the CC2010 example (λ0=0.356 at 10^17 GeV, m_H ~ 170 GeV).

The conoid, treated as a spectator Riemannian factor, does not change the
boundary ratios or the one-loop SM beta functions (see
almost_commutative_product.spectator_argument).  The running below is
therefore the standard CCM/SM running, not a new conoid prediction.
"""

from __future__ import annotations

import math
from typing import Dict, Tuple


# CC2010 (6.3)
B_COEFFS = (41.0 / 6.0, -19.0 / 6.0, -7.0)
MZ = 91.188  # GeV, the value used in CC2010 (6.2)

# CC2010 (6.7)–(6.8), their experimental inputs
CC2010_G_AT_MZ = (0.3575, 0.6514, 1.221)
CC2010_ALPHA_AT_MZ = (0.0101, 0.0337, 0.1186)

# Observed Higgs mass (PDG 2024 average, rounded; used only as a comparison,
# not as a fit target).  CC2010 predicts ~170 GeV in the cutoff-function
# approximation, which is not the measured value.
MH_OBSERVED_GEV = 125.20
MH_CCM_EXAMPLE_GEV = 170.0
LAMBDA_CCM_EXAMPLE = 1.0e17  # GeV
LAMBDA0_CCM_EXAMPLE = 0.356
LAMBDA_MZ_CCM_EXAMPLE = 0.241


def alpha_from_g(g: float) -> float:
    return g * g / (4.0 * math.pi)


def alpha_inverse_run(alpha_inv_mu: float, b: float, mu: float, scale: float) -> float:
    """α^{-1}(scale) = α^{-1}(μ) − (b / 2π) ln(scale/μ)."""
    return alpha_inv_mu - (b / (2.0 * math.pi)) * math.log(scale / mu)


def run_alphas(alpha_at_mz: Tuple[float, float, float], scale: float, mz: float = MZ):
    inv = []
    for a, b in zip(alpha_at_mz, B_COEFFS):
        inv.append(alpha_inverse_run(1.0 / a, b, mz, scale))
    return tuple(inv)


def meeting_scale(alpha_inv_i, alpha_inv_j, b_i, b_j, mz: float = MZ) -> float:
    """Scale at which α_i = α_j, assuming one-loop running from mz.

    0 = (αi^{-1}−αj^{-1}) − ((b_i−b_j)/2π) ln(Λ/mz)
    """
    d_inv = alpha_inv_i - alpha_inv_j
    d_b = b_i - b_j
    if d_b == 0:
        raise ValueError("equal b")
    # d_inv - (d_b / 2π) ln(Λ/mz) = 0
    return mz * math.exp(2.0 * math.pi * d_inv / d_b)


def ccm_unification_ratio_invariants(alpha_inv: Tuple[float, float, float]) -> Dict[str, float]:
    """How far (5/3)α1, α2, α3 are from a common value, as relative spreads.

    CCM wants α3 = α2 = (5/3) α1, i.e. α1^{-1} = (5/3) α2^{-1} = (5/3) α3^{-1}.
    Equivalently compare α2^{-1}, α3^{-1}, and (3/5) α1^{-1}.
    """
    i1, i2, i3 = alpha_inv
    # targets: i2, i3, and (3/5) i1 should be equal
    t1 = (3.0 / 5.0) * i1
    vals = (t1, i2, i3)
    mean = sum(vals) / 3.0
    spread = max(abs(v - mean) / abs(mean) for v in vals)
    return {
        "alpha1_inv": i1,
        "alpha2_inv": i2,
        "alpha3_inv": i3,
        "three_fifths_alpha1_inv": t1,
        "relative_spread": spread,
    }


def report_cc2010_inputs() -> Dict[str, object]:
    a = CC2010_ALPHA_AT_MZ
    # prefer α from the stated g's when checking internal consistency
    a_from_g = tuple(alpha_from_g(g) for g in CC2010_G_AT_MZ)
    inv_mz = tuple(1.0 / x for x in a)
    # pairwise meeting scales
    i1, i2, i3 = inv_mz
    b1, b2, b3 = B_COEFFS
    # For (5/3)α1 vs α2: compare (3/5) i1 with i2
    # Run of (3/5) α1^{-1}: α1^{-1}(Λ) = i1 − (b1/2π) L, so (3/5)α1^{-1}(Λ)
    # equals α2^{-1}(Λ) when
    # (3/5)(i1 − (b1/2π)L) = i2 − (b2/2π)L
    def meet_scaled():
        # (3/5) i1 − i2 = L/2π * ((3/5) b1 − b2)
        L = 2.0 * math.pi * ((3.0 / 5.0) * i1 - i2) / ((3.0 / 5.0) * b1 - b2)
        return MZ * math.exp(L)

    lam23 = meeting_scale(i2, i3, b2, b3)
    lam12_gut = meet_scaled()  # (5/3)α1 = α2
    # α3 = (5/3)α1
    L = 2.0 * math.pi * ((3.0 / 5.0) * i1 - i3) / ((3.0 / 5.0) * b1 - b3)
    lam13_gut = MZ * math.exp(L)

    scales = {
        "Lambda_alpha2_eq_alpha3_GeV": lam23,
        "Lambda_five_thirds_alpha1_eq_alpha2_GeV": lam12_gut,
        "Lambda_five_thirds_alpha1_eq_alpha3_GeV": lam13_gut,
    }
    at = {}
    for name, lam in scales.items():
        inv = run_alphas(a, lam)
        at[name] = {"scale_GeV": lam, **ccm_unification_ratio_invariants(inv)}

    # also evaluate at the CC2010 example 1e17 GeV
    inv_17 = run_alphas(a, LAMBDA_CCM_EXAMPLE)
    at_17 = ccm_unification_ratio_invariants(inv_17)

    return {
        "inputs": "CC2010 (6.7)–(6.8)",
        "alpha_at_MZ_quoted": a,
        "alpha_at_MZ_from_g": a_from_g,
        "meeting_scales": scales,
        "at_meeting_scales": at,
        "at_1e17_GeV": at_17,
        "unification_exact_at_one_loop": False,
        "higgs_example": {
            "Lambda_GeV": LAMBDA_CCM_EXAMPLE,
            "lambda_at_Lambda": LAMBDA0_CCM_EXAMPLE,
            "lambda_at_MZ_CC2010": LAMBDA_MZ_CCM_EXAMPLE,
            "m_H_CC2010_GeV": MH_CCM_EXAMPLE_GEV,
            "m_H_observed_GeV": MH_OBSERVED_GEV,
            "agrees_with_observed_125": False,
            "citation": "CC2010, below (6.12): λ0=0.356 at 10^17 GeV gives λ(MZ)~0.241 and m_H of order 170 GeV",
        },
        "conoid_changes_this_running": False,
    }


def report() -> Dict[str, object]:
    return report_cc2010_inputs()


if __name__ == "__main__":
    import json
    r = report()
    scales = {k: v for k, v in r["meeting_scales"].items()}
    print(json.dumps({
        "meeting_scales_GeV": scales,
        "relative_spreads": {k: v["relative_spread"] for k, v in r["at_meeting_scales"].items()},
        "spread_at_1e17": r["at_1e17_GeV"]["relative_spread"],
        "unification_exact": r["unification_exact_at_one_loop"],
        "higgs_CCM_vs_observed": (
            r["higgs_example"]["m_H_CC2010_GeV"],
            r["higgs_example"]["m_H_observed_GeV"],
        ),
    }, indent=2))
