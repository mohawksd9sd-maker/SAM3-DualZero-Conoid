"""Higgs / σ sector: literature formulas, and what the product does not add.

Exploratory, not part of the locked SAM-3 core.

Source: Chamseddine–Connes, "Resilience of the Spectral Standard Model",
JHEP 09 (2012) 104, arXiv:1208.1030 (CC2012), eqs. (12)–(15) and (30)–(32).
CCvS2015 refers to the same singlet σ as making a 125 GeV Higgs compatible
after running, with m_σ of order 10^{12} GeV, depending on ρ = m_t / m_ν
and on Λ.  Those running numbers are literature results, not recomputed
here as a unique prediction.

The tree-level couplings at the cutoff, in the CC2012 notation (n is a
Yukawa-ratio parameter, not the flux), after kinetic-term normalization, are

    λ_h  = 4 g² (n² + 3) / (n + 3)²
    λ_hσ = 4 g² (2n) / (n + 3)
    λ_σ  = 8 g²

and the mass eigenvalues of the (h, σ) fluctuations about vevs (v̄, w̄) are

    m_±² = λ_h v̄² + λ_σ w̄² ± sqrt( (λ_h v̄² - λ_σ w̄²)² + 4 λ_hσ² v̄² w̄² ).

For v̄² ≪ w̄² the light mass is reduced by
    sqrt(1 - λ_hσ² / (λ_h λ_σ))
relative to the pure-Higgs value.

Honesty about the product:

- Option A (N_F = 3 as an input of F_PS): these formulas apply as in the
  literature, independently of the conoid and of Σ.  They do not become
  a unique m_H = 125 GeV without the running and the free parameter n (or
  ρ).  The product does not fix n.
- Option B (generations from flux, N_F = 1): the CC2012/CCvS traces do
  not apply off the shelf, because the generation index now lives on Σ
  and the Yukawas are overlap integrals.  We do not invent a replacement
  a4 computation.  In particular we do not quote 125 GeV as a prediction
  of option B.
"""

from __future__ import annotations

import math
from typing import Dict


def lambda_h(n: float, g: float) -> float:
    if n <= -3:
        raise ValueError("n = -3 is a pole of the CC2012 normalisation")
    return 4.0 * g * g * (n * n + 3.0) / (n + 3.0) ** 2


def lambda_h_sigma(n: float, g: float) -> float:
    return 4.0 * g * g * (2.0 * n) / (n + 3.0)


def lambda_sigma(g: float) -> float:
    return 8.0 * g * g


def reduction_factor(n: float, g: float = 1.0) -> float:
    """sqrt(1 - λ_hσ² / (λ_h λ_σ)), the CC2012 light-Higgs reduction at tree level.

    Independent of g (it cancels).  Defined when the stability inequality
    λ_hσ² < λ_h λ_σ holds.
    """
    lh = lambda_h(n, g)
    lhs = lambda_h_sigma(n, g)
    ls = lambda_sigma(g)
    disc = 1.0 - (lhs * lhs) / (lh * ls)
    if disc < 0:
        return float("nan")
    return math.sqrt(disc)


def mass_squared_pm(n: float, g: float, vbar: float, wbar: float) -> Dict[str, float]:
    """CC2012 eq. (30)."""
    lh = lambda_h(n, g)
    lhs = lambda_h_sigma(n, g)
    ls = lambda_sigma(g)
    s = lh * vbar * vbar + ls * wbar * wbar
    d = math.sqrt((lh * vbar * vbar - ls * wbar * wbar) ** 2 + 4.0 * lhs * lhs * vbar * vbar * wbar * wbar)
    return {"m_plus_sq": s + d, "m_minus_sq": s - d, "lambda_h": lh, "lambda_hsigma": lhs, "lambda_sigma": ls}


def literature_higgs_status() -> Dict[str, object]:
    return {
        "CC2012_tree_reduction_factor_formula": "sqrt(1 - λ_hσ^2 / (λ_h λ_σ))",
        "CC2012_quotes_a_low_scale_factor_of_order": 0.78,
        "CCvS2015": {
            "m_H_125_compatible": True,
            "not_a_unique_number": True,
            "depends_on": "ρ = m_t / m_ν and Λ (and the running of the scalar couplings)",
            "m_sigma_order_GeV": 1e12,
            "note": (
                "These are literature statements, not recomputed here as a "
                "unique output of the product geometry."
            ),
        },
        "option_B_product": {
            "formulas_apply_off_the_shelf": False,
            "unique_Higgs_mass_from_the_product": False,
        },
        "option_A_literature_PS": {
            "formulas_apply": True,
            "unique_Higgs_mass": False,
            "conoid_or_Sigma_fixes_n": False,
        },
    }


def report() -> Dict[str, object]:
    # Sample tree-level reduction factors, as a check of the formulas.
    samples = {str(n): reduction_factor(n) for n in (0.0, 0.25, 0.5, 1.0, 2.0)}
    # At n=0, λ_hσ = 0, reduction = 1; λ_h = 4 g² * 3 / 9 = (4/3) g².
    return {
        "exploratory": True,
        "locked_core": False,
        "tree_reduction_factors": samples,
        "lambda_h_at_n0_over_g2": lambda_h(0.0, 1.0),
        "lambda_sigma_over_g2": lambda_sigma(1.0),
        "literature": literature_higgs_status(),
        "verdict": (
            "The CC2012 σ-extension can accommodate a 125 GeV Higgs after "
            "running, as a literature result with free parameters.  The "
            "product geometry does not uniquely predict m_H.  In the "
            "flux-generation setup the CC2012 traces do not apply off the shelf."
        ),
    }
