"""Finite spectral triples: CCM classification and the Pati-Salam variant.

Exploratory: not part of the locked SAM-3 core.  This module records the
verified literature classification and asks whether any locked SAM-3
geometric feature (C4 isometry, four tip nodes, twelve-bridge labelling)
determines a finite algebra or representation.  It does not invent a new
classification.

Literature (fetched, not invented)
---------------------------------
- A. H. Chamseddine, A. Connes, "Why the Standard Model", J. Geom. Phys.
  58 (2008) 38-47, arXiv:0706.3688.  Cited as CC2008.  Classification of
  irreducible finite geometries of KO-dimension 6; the first-order
  condition selects C ⊕ H ⊕ M3(C); the generation count N is an input.
- A. H. Chamseddine, A. Connes, W. D. van Suijlekom, "Beyond the Spectral
  Standard Model: Emergence of Pati-Salam Unification", JHEP 11 (2013)
  132, arXiv:1304.8050.  Cited as CCvS2013.  Dropping the first-order
  condition leaves the algebra H_R ⊕ H_L ⊕ M4(C), with inner-automorphism
  group SU(2)_R x SU(2)_L x SU(4).  The Standard Model algebra is the
  maximal subalgebra compatible with the first-order condition,
  C ⊕ H ⊕ M3(C) ⊂ H_R ⊕ H_L ⊕ M4(C).
- A. H. Chamseddine, A. Connes, W. D. van Suijlekom, "Grand unification
  in the spectral Pati-Salam model", JHEP 11 (2015) 011,
  arXiv:1507.08161.  Cited as CCvS2015.  One-loop unification of the
  Pati-Salam couplings for several Dirac-operator scenarios, with an
  intermediate breaking scale m_R.

The "3" in M3(C) is the colour algebra, coming from k=4 after the
first-order reduction (M4(C) -> C ⊕ M3(C)).  It is not the generation
count.  Identifying those two threes is a confusion, not a derivation.
"""

from __future__ import annotations

from typing import Dict, List


# --- documented classification steps (CC2008 / CCvS2013) ---

CCM_ALGEBRA = "C ⊕ H ⊕ M_3(C)"
PS_ALGEBRA = "H_R ⊕ H_L ⊕ M_4(C)"
PS_GAUGE_GROUP = "SU(2)_R × SU(2)_L × SU(4)"
CCM_GAUGE_GROUP = "U(1) × SU(2) × SU(3)   (unitaries of A_F, modulo the kernel of the adjoint action)"
PS_FERMION_REP_ONE_GEN = "(2,1,4) + (1,2,4)"
CCM_KO_DIM_F = 6


def classification_steps() -> List[Dict[str, object]]:
    """The CC2008 / CCvS2013 chain, recorded as a checklist, not re-proved."""
    return [
        {
            "step": 1,
            "assumption": "KO-dimension 6 (mod 8), to avoid fermion doubling (Majorana-Weyl)",
            "output": "sign table (ε, ε', ε'') = (1, 1, -1)",
            "derived_from_the_conoid": False,
        },
        {
            "step": 2,
            "assumption": "order-zero condition and irreducibility; centre of the complexified algebra is C ⊕ C",
            "output": "A_C = M_k(C) ⊕ M_k(C), with dim H = k^2 (per generation, before multiplicity)",
            "derived_from_the_conoid": False,
        },
        {
            "step": 3,
            "assumption": "symplectic (quaternionic) linearity on one summand: k = 2a even",
            "output": "M_a(H) ⊕ M_{2a}(C)",
            "derived_from_the_conoid": False,
        },
        {
            "step": 4,
            "assumption": "a grading (chirality) breaks M_a(H); the case a=2 (k=4) is the one that reproduces the known fermion quantum numbers",
            "output": "H_R ⊕ H_L ⊕ M_4(C)   (Pati-Salam algebra)",
            "note": (
                "a=2 is selected because it gives the right quantum numbers, "
                "not because a geometric principle forces a=2 uniquely without "
                "that target.  CC2008 presents it as the case that works."
            ),
            "derived_from_the_conoid": False,
        },
        {
            "step": 5,
            "assumption": "first-order condition on D (CC2008); dropped in CCvS2013",
            "output": (
                "maximal subalgebra C ⊕ H ⊕ M_3(C) ⊂ H_R ⊕ H_L ⊕ M_4(C)  (CCM / SM algebra)"
            ),
            "without_first_order": "one remains at the Pati-Salam algebra",
            "derived_from_the_conoid": False,
        },
        {
            "step": 6,
            "assumption": "multiplicity N of the finite Hilbert space (generations)",
            "output": "N is an input (CC2008 / CCM2007: 'We will restrict ourselves to N=3')",
            "derived_from_the_conoid": False,
        },
    ]


def two_threes_are_distinct() -> Dict[str, object]:
    return {
        "colour_3": {
            "origin": "M_3(C) after first-order reduction of M_4(C)",
            "status": "an output of the classification plus the first-order condition, for the k=4 case",
        },
        "generation_3": {
            "origin": "multiplicity N of H_F",
            "status": "an input in every cited paper",
        },
        "identifying_them": "numerology / confusion, not a derivation",
    }


def c4_representation_attempt() -> Dict[str, object]:
    """Can the locked C4 isometry determine a finite algebra or fermion multiplets?

    C4 is cyclic of order 4.  Over C it has four one-dimensional irreps,
    ρ_k(r) = exp(i k π / 2), k=0,1,2,3.  The complex group algebra is
    C[C4] ≅ C ⊕ C ⊕ C ⊕ C, whose unitary group is U(1)^4, not the
    Standard Model or Pati-Salam group.

    Number-matching (4 nodes, 4 irreps, 12 = 3x4 bridges, 12 = 2x2x3, ...)
    is recorded and flagged as numerology: none of these equalities is a
    representation-theoretic derivation of A_F or of a fermion multiplet.
    """
    irreps = [
        {"k": k, "character_of_generator": str((1j) ** k)} for k in range(4)
    ]
    coincidences = [
        {
            "match": "4 tip nodes = 4 irreps of C4",
            "flag": "numerology: both sides are the order of the same cyclic group",
        },
        {
            "match": "12-bridge labelling 2π/12 = 3 generations × 4 nodes (or 4 irreps)",
            "flag": "numerology: the 12-bridge spacing is a convention (STATUS), not a theorem, and 12=3×4 is an arithmetic identity",
        },
        {
            "match": "C4 cannot be SU(3), SU(2), or SU(2)×SU(2)×SU(4)",
            "flag": "not a coincidence; it is an obstruction.  An abelian isometry group does not produce a nonabelian gauge algebra by taking its irreps.",
        },
    ]
    return {
        "isometry_of_locked_conoid": "C4",
        "irreps_over_C": irreps,
        "group_algebra": "C ⊕ C ⊕ C ⊕ C",
        "unitary_group_of_group_algebra": "U(1)^4",
        "equals_CCM_algebra": False,
        "equals_PS_algebra": False,
        "produces_fermion_multiplets": False,
        "coincidences": coincidences,
        "verdict": "dead end",
        "reason": (
            "The locked isometry group is abelian of order 4.  Its "
            "representation ring and group algebra do not yield "
            "C ⊕ H ⊕ M_3(C) or H_R ⊕ H_L ⊕ M_4(C), nor the corresponding "
            "fermion representations.  Counting 4 nodes or 12 bridges against "
            "3×4 is not a derivation."
        ),
    }


def pati_salam_summary() -> Dict[str, object]:
    return {
        "algebra": PS_ALGEBRA,
        "gauge_group": PS_GAUGE_GROUP,
        "one_generation_fermions": PS_FERMION_REP_ONE_GEN,
        "generation_count": "input (N copies of the finite Hilbert space)",
        "relation_to_CCM": (
            "CCM is the maximal first-order subalgebra of the Pati-Salam algebra"
        ),
        "derived_from_the_conoid": False,
        "literature_status": (
            "CCvS2013 introduces the algebra by dropping the first-order "
            "condition; CCvS2015 analyses one-loop gauge unification and "
            "notes that a real singlet σ can make a 125 GeV Higgs compatible "
            "and can stabilise the vacuum, with a relation involving "
            "ρ = m_top / m_ν and the unification scale.  That is a "
            "literature result, not a unique mass prediction, and it does "
            "not use the conoid."
        ),
        "verdict": (
            "promising as an internal-space alternative to CCM (literature); "
            "dead end as something derived from SAM-3 geometry"
        ),
    }


def ccm_classification_verdict() -> Dict[str, object]:
    return {
        "algebra": CCM_ALGEBRA,
        "generation_count": "input",
        "derived_from_the_conoid": False,
        "verdict": (
            "neutral: the classification is a real constraint on the finite "
            "algebra once one accepts the stated axioms, but those axioms "
            "and the choice N=3 are not supplied by the conoid.  Already "
            "analysed as a product in doc 45."
        ),
    }


def report() -> Dict[str, object]:
    return {
        "exploratory": True,
        "locked_core": False,
        "classification_steps": classification_steps(),
        "two_threes": two_threes_are_distinct(),
        "c4_attempt": c4_representation_attempt(),
        "pati_salam": pati_salam_summary(),
        "ccm": ccm_classification_verdict(),
    }
