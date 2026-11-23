"""Predictions of the most promising exploratory candidates, vs data.

Exploratory: not part of the locked SAM-3 core.

This module (i) reproduces the one-loop Pati-Salam gauge running of
Chamseddine-Connes-van Suijlekom, JHEP 11 (2015) 011, arXiv:1507.08161
(CCvS2015), with the beta coefficients and matching relations quoted
there, and (ii) compares sample magnetized-torus mass ratios to
charged-lepton pole-mass ratios.  Neither computation is a SAM-3
prediction: the first does not use the conoid, and the second depends
on moduli that the conoid does not fix.

CCvS2015 quoted numbers (composite-Higgs / "standard" finite Dirac,
their Case I, lepton-quark unification, (b_R, b_L, b) = (7/3, 3, 31/3)):
    m_R ≈ 4.25 × 10^{13} GeV,   Λ ≈ 2.5 × 10^{15} GeV.
If the (1,1,15) scalar is not decoupled, (b_R, b_L, b) = (7/3, 3, 9):
    m_R ≈ 4.1 × 10^{13} GeV,    Λ ≈ 6.3 × 10^{15} GeV.
(Talk slides sometimes quote a different "general Dirac" pair
m_R ≈ 1.5×10^{11} GeV, Λ ≈ 6.3×10^{16} GeV; this module reproduces the
journal-paper coefficients above, not the slides.)

The SM one-loop coefficients below Λ = m_R are the same as in
code/ccm_oneloop_rge.py, taken from CC2010.  Input couplings at M_Z
are the CC2010 values, so that the comparison with doc 45 is apples
to apples; a small shift of Λ and m_R under a different PDG input is
expected and is not a discrepancy in the method.
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Tuple
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[1]
_CODE = _ROOT / "code"
for _p in (str(_HERE), str(_CODE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from magnetized_torus import LEPTON_RATIOS, report as torus_report
from riemann_roch import report as rr_report
from conoid_variants import report as variants_report
from finite_algebras import report as algebras_report
from product_4d import report as product_report

# Reuse the CC2010 inputs already in the core tree, without treating
# this running as a core result.

from ccm_oneloop_rge import (  # noqa: E402
    B_COEFFS as SM_B_COEFFS,
    CC2010_ALPHA_AT_MZ,
    MZ,
    run_alphas,
)


# CCvS2015: 16 π^2 dg/dt = -b g^3, t = ln μ, so
#   1/g^2(μ) = 1/g^2(μ0) + (b / 8π^2) ln(μ/μ0).
# Matching at μ = m_R, CCvS2015 (25):
#   1/g1^2 = (2/3)/g^2 + 1/g_R^2,   1/g2^2 = 1/g_L^2,   1/g3^2 = 1/g^2.
# Here g1,g2,g3 are the SM couplings in the same convention as CC2010
# (g1 is the un-normalized hypercharge coupling g'): at a point where
# g_R = g_L = g one recovers (5/3) g1^2 = g2^2 = g3^2.

PS_B_COMPOSITE = (7.0 / 3.0, 3.0, 31.0 / 3.0)  # (b_R, b_L, b)
PS_B_WITH_15 = (7.0 / 3.0, 3.0, 9.0)
LIT_COMPOSITE = {"m_R_GeV": 4.25e13, "Lambda_GeV": 2.5e15}
LIT_WITH_15 = {"m_R_GeV": 4.1e13, "Lambda_GeV": 6.3e15}


def sm_inv_g2_at(scale: float, alpha_at_mz: Tuple[float, float, float] = CC2010_ALPHA_AT_MZ) -> Tuple[float, float, float]:
    """1/g_i^2(scale) from one-loop SM running of α_i, g^2 = 4π α."""
    inv_alpha = run_alphas(alpha_at_mz, scale, mz=MZ)
    return tuple(ia / (4.0 * math.pi) for ia in inv_alpha)


def ps_couplings_at_mR(m_R: float, alpha_at_mz=CC2010_ALPHA_AT_MZ) -> Optional[Dict[str, float]]:
    """PS couplings 1/g_R^2, 1/g_L^2, 1/g^2 at the breaking scale, or None if 1/g_R^2 <= 0."""
    ig1, ig2, ig3 = sm_inv_g2_at(m_R, alpha_at_mz)
    ig = ig3
    igL = ig2
    igR = ig1 - (2.0 / 3.0) * ig
    if igR <= 0.0 or ig <= 0.0 or igL <= 0.0:
        return None
    return {"inv_gR2": igR, "inv_gL2": igL, "inv_g2": ig, "inv_g1_SM": ig1, "inv_g2_SM": ig2, "inv_g3_SM": ig3}


def run_ps(inv_at_mR: Dict[str, float], b_coeffs: Tuple[float, float, float], scale: float, m_R: float) -> Tuple[float, float, float]:
    bR, bL, b = b_coeffs
    L = math.log(scale / m_R)
    c = 1.0 / (8.0 * math.pi ** 2)
    return (
        inv_at_mR["inv_gR2"] + c * bR * L,
        inv_at_mR["inv_gL2"] + c * bL * L,
        inv_at_mR["inv_g2"] + c * b * L,
    )


def meeting_log_for_pair(inv_i: float, inv_j: float, b_i: float, b_j: float) -> Optional[float]:
    """t = ln(Λ/m_R) at which i and j meet, or None if no UV meeting."""
    db = b_i - b_j
    if db == 0:
        return None
    t = 8.0 * math.pi ** 2 * (inv_j - inv_i) / db
    if t <= 0:
        return None
    return t


def unification_mismatch(m_R: float, b_coeffs: Tuple[float, float, float], alpha_at_mz=CC2010_ALPHA_AT_MZ) -> Optional[float]:
    """Signed mismatch between the two t's that would meet (R,L) and (L,g).

    Zero at a genuine triple meeting.  None if the matching at m_R is invalid
    or a pair does not meet in the UV.
    """
    inv = ps_couplings_at_mR(m_R, alpha_at_mz)
    if inv is None:
        return None
    bR, bL, b = b_coeffs
    t_RL = meeting_log_for_pair(inv["inv_gR2"], inv["inv_gL2"], bR, bL)
    t_Lg = meeting_log_for_pair(inv["inv_gL2"], inv["inv_g2"], bL, b)
    if t_RL is None or t_Lg is None:
        return None
    return t_RL - t_Lg


def find_unification(
    b_coeffs: Tuple[float, float, float],
    alpha_at_mz=CC2010_ALPHA_AT_MZ,
    log10_mR_lo: float = 8.0,
    log10_mR_hi: float = 16.0,
    nscan: int = 200,
) -> Optional[Dict[str, float]]:
    """Scan m_R and bisect a sign change of the (R,L) vs (L,g) meeting mismatch."""
    logs = [log10_mR_lo + (log10_mR_hi - log10_mR_lo) * i / (nscan - 1) for i in range(nscan)]
    vals = []
    for lg in logs:
        mR = 10.0 ** lg
        vals.append((lg, mR, unification_mismatch(mR, b_coeffs, alpha_at_mz)))
    bracket = None
    for (lg1, m1, d1), (lg2, m2, d2) in zip(vals, vals[1:]):
        if d1 is None or d2 is None:
            continue
        if d1 == 0.0:
            bracket = (m1, m1)
            break
        if d1 * d2 < 0.0:
            bracket = (m1, m2)
            break
    if bracket is None:
        return None
    lo, hi = bracket
    for _ in range(80):
        mid = math.sqrt(lo * hi)  # log-bisect
        dmid = unification_mismatch(mid, b_coeffs, alpha_at_mz)
        dlo = unification_mismatch(lo, b_coeffs, alpha_at_mz)
        if dmid is None or dlo is None:
            break
        if dmid == 0.0:
            lo = hi = mid
            break
        if dlo * dmid < 0.0:
            hi = mid
        else:
            lo = mid
    m_R = math.sqrt(lo * hi)
    inv = ps_couplings_at_mR(m_R, alpha_at_mz)
    if inv is None:
        return None
    bR, bL, b = b_coeffs
    t = meeting_log_for_pair(inv["inv_gR2"], inv["inv_gL2"], bR, bL)
    if t is None:
        return None
    Lam = m_R * math.exp(t)
    inv_L = run_ps(inv, b_coeffs, Lam, m_R)
    spread = max(inv_L) - min(inv_L)
    return {
        "m_R_GeV": m_R,
        "Lambda_GeV": Lam,
        "inv_g2_at_Lambda": sum(inv_L) / 3.0,
        "inv_g2_spread_at_Lambda": spread,
        "t_ln_Lambda_over_mR": t,
    }


def relative_log_error(computed: float, literature: float) -> float:
    return abs(math.log(computed / literature))


def ps_unification_report() -> Dict[str, object]:
    out = {}
    for name, b, lit in (
        ("composite_7_3_31_3", PS_B_COMPOSITE, LIT_COMPOSITE),
        ("with_15_7_3_9", PS_B_WITH_15, LIT_WITH_15),
    ):
        found = find_unification(b)
        if found is None:
            out[name] = {"found": False, "literature": lit}
            continue
        out[name] = {
            "found": True,
            "computed": found,
            "literature_CCvS2015": lit,
            "rel_log_error_mR": relative_log_error(found["m_R_GeV"], lit["m_R_GeV"]),
            "rel_log_error_Lambda": relative_log_error(found["Lambda_GeV"], lit["Lambda_GeV"]),
            "comment": (
                "Errors are in natural log, so 0.2 is about 20% in the scale.  "
                "A residual of this size is expected from the difference "
                "between CC2010 couplings at M_Z and whatever CCvS2015 used; "
                "it is not a claim that the literature numbers are wrong."
            ),
        }
    return out


def mass_ratio_comparison() -> Dict[str, object]:
    """Compare sample (3,3,6) torus Yukawa singular-value ratios to leptons.

    This is a check against uniqueness, not a fit.  A candidate would be
    a unique prediction only if the ratios were stable under the remaining
    moduli (τ and the Higgs slice) and close to the measured ones.
    """
    tr = torus_report()
    samples = tr["yukawa_scan"]["samples"]
    lepton = LEPTON_RATIOS
    # For a 3-generation slice the two independent ratios are s2/s1 and s3/s1
    # once sorted ascending.  The lepton analogues are mμ/me and mτ/me.
    rows = []
    any_close = False
    for name, data in samples.items():
        for k, ratios in enumerate(data["mass_ratios_by_higgs"]):
            if len(ratios) < 3:
                continue
            # ratios is already s/smin for each positive singular value, not
            # necessarily sorted in the list returned; sort them.
            rsorted = sorted(ratios)
            pred = {"light_over_light": 1.0, "mid_over_light": rsorted[1], "heavy_over_light": rsorted[2]}
            # "close" would mean within a factor of 3 of both lepton ratios —
            # a loose bar, used only to detect a lucky slice, not to claim a fit.
            close = (
                abs(math.log(pred["mid_over_light"] / lepton["mu_over_e"])) < math.log(3.0)
                and abs(math.log(pred["heavy_over_light"] / lepton["tau_over_e"])) < math.log(3.0)
            )
            any_close = any_close or close
            rows.append(
                {
                    "moduli": name,
                    "higgs_slice": k,
                    "predicted_ratios_ascending": rsorted,
                    "within_factor_3_of_leptons": close,
                }
            )
    n_close = sum(1 for r in rows if r["within_factor_3_of_leptons"])
    return {
        "lepton_pole_ratios_PDG2024": lepton,
        "n_slices_checked": len(rows),
        "n_slices_within_factor_3": n_close,
        "any_slice_is_a_unique_prediction": False,
        "rows": rows,
        "verdict": (
            "The sample (I,J,K)=(3,3,6) Yukawas, at four values of τ and six "
            "Higgs slices each, do not uniquely reproduce the charged-lepton "
            "hierarchy.  Even a lucky slice would not be a prediction: τ and "
            "the slice are free, and the conoid does not fix them."
        ),
    }


def ranked_directions() -> List[Dict[str, object]]:
    return [
        {
            "rank": 1,
            "name": "4D product with a magnetized compact surface, times a CCM or Pati-Salam finite triple",
            "examples": [
                "conoid × T^2_{flux 3} × F",
                "conoid × S^2_{degree 3} × F",
                "ordinary 4D spacetime × T^2_{flux 3} (conoid dropped) × F",
            ],
            "verdict": "promising as a package, with an explicit caveat",
            "why": (
                "This is the only setup in the survey that is simultaneously "
                "4-dimensional (heat kernel and KO-dimension match the CCM "
                "fermionic framework) and has a clean geometric mechanism for "
                "exactly three chiral zero modes — namely an integer flux or "
                "bundle degree equal to 3.  The gauge content and coupling "
                "relations then come from F (CCM or Pati-Salam), not from the "
                "conoid.  The number 3 itself is still a choice of flux, and "
                "Yukawa mass ratios depend on moduli that are not fixed.  "
                "The locked conoid, as a factor, remains incomplete and does "
                "not determine the flux (docs 45-46 and product_4d)."
            ),
            "generation_count": "put in as the flux / degree",
            "coupling_relations": "CCM or Pati-Salam relations of F, not derived from the surface",
            "mass_ratios": "moduli-dependent; not unique; samples do not force the lepton hierarchy",
        },
        {
            "rank": 2,
            "name": "Pati-Salam finite spectral triple as the internal space",
            "verdict": "promising as a literature internal-space alternative; not derived from the conoid",
            "why": (
                "CCvS2013 obtains H_R ⊕ H_L ⊕ M_4(C) by dropping the "
                "first-order condition in the same KO-dimension-6 "
                "classification that yields the SM algebra when the condition "
                "is kept.  CCvS2015 finds one-loop unification of the three "
                "Pati-Salam couplings with an intermediate breaking scale m_R, "
                "and the extra singlet σ can make a 125 GeV Higgs compatible.  "
                "The generation count is still an input.  None of this uses "
                "the locked conoid."
            ),
            "generation_count": "input",
            "coupling_relations": "g_R = g_L = g at Λ; matching to the SM is the standard PS embedding",
            "mass_ratios": "not uniquely predicted; Higgs mass is compatible with 125 GeV for a range of ρ and Λ (CCvS literature), not a single number",
        },
        {
            "rank": 3,
            "name": "CCM finite triple as classified (already in doc 45)",
            "verdict": "neutral",
            "why": (
                "The SM algebra is tightly constrained by the stated axioms, "
                "and the spectral-action coupling relation is clear.  One-loop "
                "running of that relation does not meet at a single scale, and "
                "the CC2010 Higgs example is ~170 GeV, not 125 GeV.  N=3 is "
                "an input.  The raw product conoid × F is 2D, not a 4D model."
            ),
            "generation_count": "input",
            "coupling_relations": "g3^2 = g2^2 = (5/3) g1^2 at Λ; one-loop SM running does not unify",
            "mass_ratios": "Higgs example ~170 GeV (CC2010), not a mass-ratio derivation",
        },
        {
            "rank": 4,
            "name": "Frequency-n conoids, caps, and 'closed' conoid-like surfaces",
            "verdict": "dead end",
            "why": (
                "The untwisted APS index is 0 for every n.  Total curvature "
                "is always -2π.  Node count and isometry order are 2n, never "
                "3.  No unique smooth closed surface is determined by the "
                "embedding; any genuine compact spin surface still needs a "
                "degree-3 twist to get index 3."
            ),
        },
        {
            "rank": 5,
            "name": "C4 representations, four nodes, or twelve-bridge labelling as a finite algebra or fermion content",
            "verdict": "dead end",
            "why": (
                "C4 is abelian; its group algebra is C^4, with unitaries U(1)^4, "
                "not the SM or Pati-Salam algebra.  Counting 4 or 12 against "
                "3×4 is numerology."
            ),
        },
        {
            "rank": 6,
            "name": "Euler characteristic, Hopf bundle, or TS^2 as a source of the integer 3",
            "verdict": "dead end",
            "why": (
                "No connected compact surface has χ=3 (the maximum is 2).  "
                "The Hopf bundle has degree 1 (Dirac index 1).  O(2)=TS^2 has "
                "Dirac index 2; its three holomorphic sections are conformal "
                "Killing fields, not chiral generations."
            ),
        },
    ]


def report() -> Dict[str, object]:
    ps = ps_unification_report()
    masses = mass_ratio_comparison()
    return {
        "exploratory": True,
        "locked_core": False,
        "pati_salam_oneloop": ps,
        "magnetized_torus_mass_ratios": masses,
        "ranked_directions": ranked_directions(),
        "headline": (
            "No alternative surface or internal space examined here derives "
            "the integer 3, or unique mass ratios, from the locked conoid.  "
            "The cleanest generation *mechanism* is a chosen flux or bundle "
            "degree on a compact surface, in a 4D product with a CCM or "
            "Pati-Salam finite triple.  Pati-Salam is the more flexible "
            "internal space in the cited literature, and is not a SAM-3 output."
        ),
    }


def full_survey() -> Dict[str, object]:
    """Bundle every exploratory report into one dictionary for the JSON dump."""
    return {
        "exploratory": True,
        "locked_core_untouched": True,
        "riemann_roch": rr_report(),
        "magnetized_torus": torus_report(),
        "conoid_variants": variants_report(),
        "finite_algebras": algebras_report(),
        "product_4d": product_report(),
        "promising_candidates": report(),
    }
