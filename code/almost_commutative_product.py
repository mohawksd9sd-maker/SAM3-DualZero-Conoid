"""Almost-commutative products of the locked conoid with the CCM finite triple.

Literature used (fetched and quoted, not invented)
-------------------------------------------------
- A. H. Chamseddine, A. Connes, M. Marcolli, "Gravity and the standard model
  with neutrino mixing", Adv. Theor. Math. Phys. 11 (2007) 991–1089,
  arXiv:hep-th/0610241.  Cited below as CCM2007.
- A. H. Chamseddine, A. Connes, "Noncommutative geometry as a framework for
  unification of all fundamental interactions including gravity. Part I",
  Fortschr. Phys. 58 (2010) 553–600, arXiv:1004.0464.  Cited below as CC2010.

The finite spectral triple F is the standard one of those papers:
algebra A_F = ℂ ⊕ ℍ ⊕ M_3(ℂ), KO-dimension 6, metric dimension 0.
CCM2007 p. 12 / §2: the multiplicity N = 3 "is an input" and "is not
predicted by our model in its present form".

This module does not treat Paper 09 of this repository as a source: that
draft assigns KO-dimension 4 to F (it is 6) and claims that the product of
the 2D conoid with F yields 4D Einstein–Hilbert gravity.  Both claims are
inconsistent with the literature above and with the dimension of the heat
kernel.  See the option table and doc 45.
"""

from __future__ import annotations

from typing import Dict, List


# --- CCM data, copied from the papers above ---

CCM_ALGEBRA = "C ⊕ H ⊕ M_3(C)"
CCM_KO_DIM_F = 6  # CCM2007, abstract and §1: "KO-dimension 6 modulo 8"
CCM_METRIC_DIM_F = 0
CCM_N_GENERATIONS = 3  # input, CCM2007: "We will restrict ourselves to N=3"

# Unification relation, CCM2007 §1 and CC2010 (5.51), (6.1):
#   g3^2 = g2^2 = (5/3) g1^2
# at the spectral cutoff Λ.  Here g1 is the SM hypercharge coupling g'
# (so that sin^2 θ_W = 3/8 at Λ).  Normalization of the kinetic terms:
#   g3^2 F0 / (2 π^2) = 1/4,   CC2010 (6.1).
# Moments: f_k = ∫_0^∞ f(v) v^{k-1} dv (k>0), f_0 = f(0)  (CCM2007 (1.3)).
# CC2010 writes the same moments as F0, F2, F4.

CCM_UNIFICATION = "g3^2 = g2^2 = (5/3) g1^2"
CCM_SIN2_THETA_W_AT_LAMBDA = 3.0 / 8.0
# CC2010 (6.1)
def F0_from_g3(g3: float) -> float:
    """F0 required by CC2010 (6.1): g3^2 F0 / (2π^2) = 1/4."""
    import math
    return (0.5 * math.pi ** 2) / (g3 * g3)


# Standard KO-dimension of the canonical spectral triple on a closed
# Riemannian spin manifold of dimension n is n mod 8.  KO-dimensions
# of a product add (mod 8).


def ko_dimension(*summands: int) -> int:
    return int(sum(summands) % 8)


def option_table() -> List[Dict[str, object]]:
    """Product geometries one might form, with KO-dimension and heat-kernel dim.

    The CCM fermionic action is set up for total KO-dimension ≡ 2 (mod 8),
    which is what 4D spacetime × F (4+6=10≡2) provides (CCM2007).
    """
    rows = [
        {
            "name": "conoid × F  (no extra spacetime)",
            "continuous_dimension": 2,
            "ko": ko_dimension(2, 6),
            "ko_matches_CCM_fermions": ko_dimension(2, 6) == 2,
            "heat_kernel_is_4D": False,
            "verdict": "failed as a 4D unification model",
            "reason": (
                "The heat kernel is two-dimensional: the spectral action has "
                "terms of type Λ^2 Area + (curvature / boundary), not a 4D "
                "Einstein–Hilbert + Yang–Mills action.  KO-dimension 2+6=8≡0, "
                "not the CCM value 2.  This is the raw product conoid × F."
            ),
        },
        {
            "name": "M^4 × conoid × F  (conoid as extra internal factor)",
            "continuous_dimension": 6,
            "ko": ko_dimension(4, 2, 6),
            "ko_matches_CCM_fermions": ko_dimension(4, 2, 6) == 2,
            "heat_kernel_is_4D": False,
            "note_on_dimension": (
                "The continuous geometry is 6-dimensional, so the leading "
                "Seeley expansion is 6D (Λ^6, Λ^4, Λ^2, …).  If one instead "
                "treats the conoid as a ‘compact internal’ factor and expands "
                "only in the 4D directions, the 4D coefficients are multiplied "
                "by integrals over the conoid (area, ∫K, …)."
            ),
            "verdict": "partially derived, with a dimensional hypothesis",
            "reason": (
                "KO-dimension 4+2+6=12≡4, not 2, so the CCM fermionic "
                "package does not carry over unchanged.  If one ignores that "
                "and treats the conoid as a spectator Riemannian factor in "
                "front of F, every 4D gauge kinetic term is multiplied by the "
                "same internal area: the CCM ratios g3^2=g2^2=(5/3)g1^2 are "
                "unchanged.  The overall scale (the relation of F0 to g^2, "
                "and of F2 to G_N) is rescaled by that area and remains "
                "scheme-dependent.  The conoid does not fix ω0, α, or the "
                "generation count, and does not modify the CCM Higgs-quartic "
                "relation at Λ, which comes from traces on F."
            ),
        },
        {
            "name": "(conoid × Σ^2) × F  (extra 2-manifold to reach 4D)",
            "continuous_dimension": 4,
            "ko": ko_dimension(2, 2, 6),
            "ko_matches_CCM_fermions": ko_dimension(2, 2, 6) == 2,
            "heat_kernel_is_4D": True,
            "verdict": "partially derived, assuming a choice of Σ^2",
            "reason": (
                "This is the only product in the list whose continuous "
                "dimension is 4 and whose KO-dimension is 2, matching CCM.  "
                "The 4-geometry Y=conoid×Σ^2 is not unique: every statement "
                "about volumes and curvature of Y depends on a choice of Σ^2 "
                "that is not determined by the locked conoid.  For any such "
                "choice, F is still the CCM finite triple, so the gauge-coupling "
                "ratios and the Higgs-gauge relation at Λ are the standard CCM "
                "ones (spectator argument).  The conoid contributes its area "
                "and its total curvature −2π to the gravitational coefficients, "
                "but does not uniquely fix F0, F2, F4 or α."
            ),
        },
        {
            "name": "M^4 × F  (plain CCM; conoid unused)",
            "continuous_dimension": 4,
            "ko": ko_dimension(4, 6),
            "ko_matches_CCM_fermions": True,
            "heat_kernel_is_4D": True,
            "verdict": "derived in the literature, independent of the conoid",
            "reason": (
                "This is CCM2007/CC2010.  It does not use the conoid, so it "
                "cannot be a derivation of anything from the locked metric."
            ),
        },
    ]
    return rows


def spectator_argument() -> Dict[str, object]:
    """Why a commutative Riemannian factor does not change CCM coupling ratios.

    If the extra geometry C (the conoid, or conoid × Σ^2, …) is a commutative
    spin manifold that tensors with F, inner fluctuations of the finite
    algebra act as gauge fields on H_F and are constant along C.  Each
    4D Yang–Mills term in a4 is multiplied by the same integral ∫_C vol.
    The relative coefficients of Tr B^2, Tr W^2 and Tr V^2 are therefore
    exactly those of CCM, and the relation g3^2=g2^2=(5/3)g1^2 is unchanged.
    Changing the overall area rescales the map from F0 to g^2 but not the
    ratios.  The Higgs quartic at Λ is likewise a ratio of traces on F
    (CC2010 §6) and is not modified by a spectator volume.
    """
    return {
        "ccm_ratio_preserved": True,
        "higgs_quartic_at_Lambda_preserved": True,
        "F0_g_relation_rescaled_by_area": True,
        "generation_count_unchanged": True,
        "reason": (
            "Spectator volumes cancel in coupling ratios and in the "
            "Higgs-to-gauge relation at Λ.  They do not cancel in G_N "
            "or in the cosmological term, which remain scheme-dependent."
        ),
    }


def generation_count_status() -> Dict[str, object]:
    return {
        "CCM_N": CCM_N_GENERATIONS,
        "CCM_N_is_input": True,
        "citation": (
            "CCM2007: “The multiplicity N=3 here is an input, and it "
            "corresponds to the number of particle generations in the "
            "standard model. The number of generations is not predicted "
            "by our model in its present form and has to be taken as an "
            "input datum.”"
        ),
        "conoid_APS_index_untwisted": 0,
        "conoid_does_not_replace_the_input": True,
        "verdict": "failed (generation count is an input of F, not a conoid derivation)",
    }


def cutoff_moment_constraints() -> Dict[str, object]:
    """What the conoid does (and does not) say about F0, F2, F4.

    In plain 4D CCM, the three moments are used as initial conditions for
    (g^2, G_N, cosmological constant), not predicted (CC2010, below (6.1)).
    A spectator area A multiplies the map F0 ↦ 1/g^2 and F2 ↦ 1/G_N.
    The exact finite part C0=2π ln 2 can be used as one choice of A, but
    that is a scheme, not a uniqueness theorem (doc 43–44).  No additional
    equation determines the three moments uniquely.
    """
    return {
        "plain_CCM": "F0, F2, F4 set (g^2, G_N, Lambda_cosmo); not predicted",
        "with_spectator_area_A": (
            "F0 A and F2 A enter the same two relations; still two equations "
            "for three moments plus a scheme-dependent A"
        ),
        "unique_constraint": False,
        "verdict": "failed to uniquely fix F0, F2, F4, or α",
    }


def report() -> Dict[str, object]:
    return {
        "algebra": CCM_ALGEBRA,
        "KO_dim_F": CCM_KO_DIM_F,
        "options": option_table(),
        "spectator": spectator_argument(),
        "generations": generation_count_status(),
        "moments": cutoff_moment_constraints(),
        "paper09_ko_claim_is_wrong": True,
        "paper09_claimed_ko_of_F": 4,
        "literature_ko_of_F": 6,
    }


if __name__ == "__main__":
    import json
    r = report()
    print(json.dumps({
        "algebra": r["algebra"],
        "KO_dim_F": r["KO_dim_F"],
        "options": [
            {"name": o["name"], "dim": o["continuous_dimension"],
             "ko": o["ko"], "ko_ok": o["ko_matches_CCM_fermions"],
             "verdict": o["verdict"]}
            for o in r["options"]
        ],
        "generations": r["generations"]["verdict"],
        "moments": r["moments"]["verdict"],
        "paper09_ko_claim_is_wrong": True,
    }, indent=2))
