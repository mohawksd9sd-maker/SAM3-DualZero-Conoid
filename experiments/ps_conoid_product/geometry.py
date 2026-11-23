"""4D almost-commutative geometry: truncated conoid × Σ² × F_PS.

Exploratory, not part of the locked SAM-3 core.

The continuous 4-geometry is Y = X_{a,b} × Σ, with X_{a,b} the truncated
right conoid and Σ a compact orientable surface (T² or S²).  The finite
spectral triple is the Pati-Salam one of Chamseddine-Connes-van Suijlekom,
JHEP 11 (2013) 132, arXiv:1304.8050: A_F = H_R ⊕ H_L ⊕ M_4(C), KO-dimension 6.

KO-dimensions add: 2 + 2 + 6 = 10 ≡ 2 (mod 8), which matches the CCM
fermionic setup (doc 45).  The heat kernel is four-dimensional.

Important geometric caveats, stated up front:

- Y is a *Riemannian* product of an incomplete/truncated 2-surface and a
  compact 2-surface.  It is not Lorentzian Minkowski space.  Interpreting
  the spectral action on Y × F_PS as a model of our 3+1 world uses the
  same Euclidean-to-Lorentzian step as CCM, plus the extra identification
  of Y with the 4-manifold in that construction.  Gravity extracted from
  a2 is gravity *on Y*, not automatically Newton's constant in observed
  spacetime.
- Area(X_{a,b}) diverges as π b² when the outer cutoff b → ∞.  The exact
  finite part C0 = 2π ln 2 of that area (unit metric) does not cancel the
  divergence.  Every coefficient that multiplies vol(Y) is therefore
  cutoff-dependent.
- If generations are the zero modes of a flux-twisted Dirac operator on Σ,
  the finite Hilbert space should be taken with multiplicity N_F = 1.
  Using N_F = 3 *and* flux 3 would over-count.  The CCvS Higgs-mass
  numerics assume a finite triple with generation multiplicity in D_F;
  they do not carry over unchanged to the flux-generation setup.

Literature used (fetched, not invented): CCM2007, CC2010, CCvS2013,
CCvS2015, and the locked conoid identities of docs 44-46 (C0, ∫K = -2π).
"""

from __future__ import annotations

import math
from typing import Dict, Optional

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_CODE = _ROOT / "code"
for _p in (str(_CODE),):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from conoid_heat_kernel import (  # noqa: E402
    area_truncation,
    curvature_integral,
    total_curvature_complete,
)
from core_geometry import C0_EXACT  # noqa: E402


PS_ALGEBRA = "H_R ⊕ H_L ⊕ M_4(C)"
PS_GAUGE_GROUP = "SU(2)_R × SU(2)_L × SU(4)"
PS_KO_DIM_F = 6
# CCvS2013: one generation is (2,1,4)+(1,2,4).  Multiplicity is an input
# of the finite Hilbert space unless generations come from ker D_Σ.
PS_FERMION_REP_ONE_GEN = "(2,1,4) + (1,2,4)"


def ko_dimension(*summands: int) -> int:
    return int(sum(summands) % 8)


def product_data() -> Dict[str, object]:
    return {
        "Y": "truncated conoid X_{a,b} × Σ",
        "F": PS_ALGEBRA,
        "ko_Y_F": ko_dimension(2, 2, PS_KO_DIM_F),
        "ko_matches_CCM_fermions": ko_dimension(2, 2, PS_KO_DIM_F) == 2,
        "continuous_dimension": 4,
        "heat_kernel_is_4D": True,
        "Y_is_Minkowski": False,
        "euclidean_to_lorentzian_is_an_extra_step": True,
    }


def area_conoid(a: float, b: float, ell0: float = 1.0) -> float:
    """Area of X_{a,b}, exact decomposition π(b²-a²)+∫ I."""
    return area_truncation(a, b, ell0=ell0)


def area_conoid_asymptotic(b: float, ell0: float = 1.0) -> Dict[str, float]:
    """A(0,b) = π b² + 2π ℓ0² log(b/ℓ0) + 2π ℓ0² ln 2 + o(1)."""
    leading = math.pi * b * b
    log_part = 2.0 * math.pi * ell0 * ell0 * math.log(b / ell0)
    finite = 2.0 * math.pi * ell0 * ell0 * math.log(2.0)
    return {
        "leading_pi_b2": leading,
        "log_part": log_part,
        "finite_part_C0_scaled": finite,
        "C0_unit_metric": C0_EXACT,
        "sum_of_displayed_terms": leading + log_part + finite,
    }


def scalar_curvature_integral_conoid(a: float, b: float, ell0: float = 1.0) -> float:
    """∫_{X} R dA with the 2D convention R = 2K.

    For the complete-surface limit this is 2*(-2π) = -4π.
    """
    return 2.0 * curvature_integral(a, b, ell0=ell0)


def sigma_invariants(kind: str, area: Optional[float] = None, radius: Optional[float] = None) -> Dict[str, float]:
    """Area and ∫ R of the compact factor Σ.

    T² is flat, so ∫ R = 0 and the area is a free modulus.
    The unit-curvature 2-sphere has Area = 4π R² and ∫ R = 8π (R_scalar = 2K,
    ∫ K = 4π).
    """
    if kind == "T2":
        if area is None:
            raise ValueError("T^2 area is a free modulus; pass area=")
        return {"area": float(area), "int_R": 0.0, "int_K": 0.0, "euler": 0.0}
    if kind == "S2":
        if radius is None:
            raise ValueError("S^2 radius is a free modulus; pass radius=")
        r = float(radius)
        return {
            "area": 4.0 * math.pi * r * r,
            "int_R": 8.0 * math.pi,
            "int_K": 4.0 * math.pi,
            "euler": 2.0,
            "radius": r,
        }
    raise ValueError("kind must be T2 or S2")


def product_integrals(
    a: float,
    b: float,
    kind: str,
    ell0: float = 1.0,
    area_sigma: Optional[float] = None,
    radius: Optional[float] = None,
) -> Dict[str, float]:
    """Heat-kernel geometric integrals on Y = X_{a,b} × Σ.

    For a Riemannian product, vol(Y) = Area(X) Area(Σ) and
        ∫_Y R = Area(Σ) ∫_X R_X + Area(X) ∫_Σ R_Σ,
    with R_X = 2K_X.

    These enter a0 (volume) and the Einstein-Hilbert piece of a2.
    They are not, by themselves, a derivation of Newton's constant.
    """
    ax = area_conoid(a, b, ell0)
    int_rx = scalar_curvature_integral_conoid(a, b, ell0)
    sig = sigma_invariants(kind, area=area_sigma, radius=radius)
    a_s = sig["area"]
    int_rs = sig["int_R"]
    vol = ax * a_s
    int_r = a_s * int_rx + ax * int_rs
    return {
        "area_X": ax,
        "area_Sigma": a_s,
        "vol_Y": vol,
        "int_R_X": int_rx,
        "int_R_Sigma": int_rs,
        "int_R_Y": int_r,
        "int_K_X": int_rx / 2.0,
        "complete_int_K_X": total_curvature_complete(),
    }


def flux_yang_mills_integral(
    area_X: float,
    area_sigma: float,
    flux: int,
) -> float:
    """∫_Y |F_Σ|² for a constant curvature U(1) flux on Σ, pulled back to Y.

    On Σ, a connection with Chern number M has ∫_Σ F = 2π M.  For constant
    field strength, ∫_Σ |F|² = (2π M)² / Area(Σ) in the convention
    |F|² dA = F_{12}^2 dA with F_{12} = 2π M / Area.  Pulled back to the
    product (F has no legs along the conoid), ∫_Y |F|² = Area(X) * (2π M)² / Area(Σ).

    This convention is the standard one used in magnetized-torus reductions
    and is enough to read off the sign and the scaling.  An overall factor
    of 2 from 2-form conventions would not change the conclusion that the
    term is nonnegative, vanishes only at M=0, and diverges with Area(X).
    """
    if area_sigma <= 0 or area_X < 0:
        raise ValueError("areas must be positive (Area_X may be 0)")
    return area_X * (2.0 * math.pi * flux) ** 2 / area_sigma


def divergence_report() -> Dict[str, object]:
    """Which integrated terms remain finite as b → ∞, a → 0."""
    # Complete-limit curvature of the conoid is finite; area is not.
    return {
        "vol_Y": "diverges as π b² Area(Σ)",
        "int_R_Y_for_T2": (
            "finite: Area(T²) * ∫_X R_X → -4π Area(T²), because T² is flat"
        ),
        "int_R_Y_for_S2": (
            "diverges: Area(X) * 8π → ∞, plus a finite piece Area(S²)*(-4π)"
        ),
        "flux_YM_for_nonzero_M": "diverges as Area(X) * (2π M)² / Area(Σ)",
        "flux_YM_for_M_0": "vanishes",
        "C0_cancels_the_area_divergence": False,
        "note": (
            "C0 is the finite part of Area(X) after subtracting π b² and the "
            "log term.  It does not make vol(Y) or the flux Yang-Mills integral "
            "finite for M ≠ 0."
        ),
    }


def gravitational_coupling_status() -> Dict[str, object]:
    """What the spectral action says about a Newton constant on Y.

    On a closed 4-manifold the Einstein-Hilbert term in the spectral action
    is local: 1/(16π G) is a coefficient built from the cutoff moments f2, f0
    and from traces on F (CC2010, after (5.46) and §6).  That coefficient
    does *not* involve C0 or ∫K.  Those integrals change the *integrated*
    Einstein-Hilbert and cosmological terms on a truncation, not the local
    value of G.

    Identifying G_Y with Newton's constant in observed 3+1 spacetime is an
    extra assumption (Y is not that spacetime).  Even as a coupling on Y,
    the moments f2, f0 remain free, so G_Y is not uniquely derived.  This
    is the same scheme-dependence already recorded for α in G_N = α ℓ0²
    (docs 43-45).
    """
    return {
        "local_G_depends_on_C0_or_int_K": False,
        "local_G_depends_on_unfixed_moments_f2_f0": True,
        "identification_with_Newton_constant_is_an_assumption": True,
        "unique_derivation": False,
        "verdict": "failed to uniquely derive G_N (or even G_Y) from the product",
        "reason": (
            "The local Einstein-Hilbert coefficient is fixed only once the "
            "cutoff moments are chosen, and it lives on Y, not automatically "
            "in observed spacetime.  C0 and ∫K enter integrated terms and "
            "do not uniquely determine the moments."
        ),
    }


def gauge_boundary_conditions() -> Dict[str, object]:
    """PS gauge coupling relations at the spectral cutoff Λ.

    CCvS2015: the F0 a4 term contains
        (F0 / 2π²) ∫ (g_L² W_L² + g_R² W_R² + g² V²),
    and normalizing each to 1/4 requires g_R = g_L = g at Λ.  A commutative
    Riemannian factor Y multiplies every Yang-Mills term by the same volume
    and does not change the ratios (spectator argument of doc 45, applied
    to F_PS rather than to the CCM algebra).  Matching to the SM at a
    breaking scale m_R is CCvS2015 (25):
        1/g1² = (2/3)/g² + 1/g_R²,  1/g2² = 1/g_L²,  1/g3² = 1/g²,
    with g1 the SM hypercharge coupling (CC2010 convention).
    """
    return {
        "at_Lambda": "g_R = g_L = g",
        "derived_from_spectral_action_normalization": True,
        "changed_by_the_conoid_or_by_Sigma": False,
        "matching_at_m_R": {
            "inv_g1_SM": "2/3 * 1/g^2 + 1/g_R^2",
            "inv_g2_SM": "1/g_L^2",
            "inv_g3_SM": "1/g^2",
            "source": "CCvS2015 eq. (25)",
        },
        "at_unification_reduces_to": "g3^2 = g2^2 = (5/3) g1^2",
        "verdict": "derived, assuming the CCvS spectral action on Y × F_PS",
    }


def generations_bookkeeping() -> Dict[str, object]:
    return {
        "option_A": {
            "description": "N_F = 3 as an input of F_PS; Σ may be flux-free",
            "generation_count": "input, not derived",
            "CCvS_Higgs_numerics_apply_off_the_shelf": True,
            "flux_does_not_explain_generations": True,
        },
        "option_B": {
            "description": "N_F = 1; three chiral zero modes from flux M=3 on Σ",
            "generation_count": "equal to M, and M is not derived (see flux_mechanisms)",
            "CCvS_Higgs_numerics_apply_off_the_shelf": False,
            "reason": (
                "CCvS compute the Higgs/σ potential from traces on a finite "
                "Dirac operator whose generation index already sits in D_F.  "
                "In option B the generation index is a zero-mode label on Σ, "
                "and the Yukawas are overlap integrals.  Those traces are not "
                "the CCvS ones.  We do not invent a replacement a4 computation."
            ),
        },
        "option_N_F_3_and_flux_3": {
            "description": "N_F = 3 and flux 3",
            "generation_count": 9,
            "verdict": "over-counting; not used",
        },
        "preferred_for_this_survey": "option_B, with option_A recorded only as the literature PS model",
    }


def report() -> Dict[str, object]:
    ints_t2 = product_integrals(1e-4, 20.0, "T2", area_sigma=1.0)
    ints_s2 = product_integrals(1e-4, 20.0, "S2", radius=1.0)
    return {
        "exploratory": True,
        "locked_core": False,
        "product": product_data(),
        "asymptotic_area_unit_metric_b20": area_conoid_asymptotic(20.0, 1.0),
        "integrals_T2_example": ints_t2,
        "integrals_S2_example": ints_s2,
        "divergences": divergence_report(),
        "gravity": gravitational_coupling_status(),
        "gauge_BCs": gauge_boundary_conditions(),
        "generations": generations_bookkeeping(),
        "complete_int_K_conoid": total_curvature_complete(),
        "C0": C0_EXACT,
    }
