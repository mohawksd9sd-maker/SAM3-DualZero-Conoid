"""One-loop (and partial two-loop) RG pipeline for the PS product.

Exploratory, not part of the locked SAM-3 core.

Direction of the argument, stated honestly:
  The CCvS2015 procedure uses the measured SM couplings at M_Z as *inputs*,
  runs them up to a variable breaking scale m_R, and adjusts m_R until
  g_R, g_L and g meet.  That determines (m_R, Λ) from the data plus the
  PS boundary condition.  It is not a prediction of the couplings at M_Z.
  Because the geometry does not fix m_R or Λ (flux_mechanisms, geometry),
  there is no top-down prediction of (g1, g2, g3)(M_Z) from the product.

This module:

- Builds SM couplings at M_Z from stated PDG sources, and also from the
  CC2010 inputs already used in the locked-core comparison (doc 45).
- Reproduces the one-loop CCvS2015 pipeline (SM below m_R, PS above).
- Adds a *partial* two-loop run below m_R: SM gauge two-loop matrix B_ij
  of Machacek–Vaughn / Martin, in GUT normalisation, with two-loop Yukawa
  contributions omitted (stated approximation).  The PS segment remains
  one-loop: CCvS2015 did not publish two-loop PS β-functions, and we do
  not invent them.

Sources for the inputs
----------------------
- M_Z = 91.1879(20) GeV,  α_s(M_Z) = 0.1180(9),
  sin²θ_W(M_Z)|_{MSbar} = 0.23122(6):
  PDG 2026 Physical Constants, https://pdg.lbl.gov/2026/reviews/rpp2026-rev-phys-constants.pdf
  (revised May 2026).
- α̂^{-1}(M_Z²) = 127.930(8):
  PDG 2024 recommendation, as quoted in 2026 workshop discussion of the
  2026 Review (the 2026 constants table lists only α(0)^{-1} =
  137.035999177(21) and does not recommend a new α(M_Z)).  We use the
  2024 value and label it as such.
- One-loop SM b = (41/6, -19/6, -7) in the CC2010 hypercharge convention
  (g1 = g').  One-loop PS (b_R, b_L, b) from CCvS2015.
- Two-loop SM gauge matrix, GUT normalisation ĝ1² = (5/3) g'²,
  b̂ = (41/10, -19/6, -7),
      B = [[199/50, 27/10, 44/5],
           [9/10,  35/6,  12 ],
           [11/10,  9/2,  -26]],
  Machacek–Vaughn NPB 222 (1983) 83; as quoted in Martin, arXiv:hep-ph/9709356
  and in Roy, arXiv:1907.10238, eq. (II.3).
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Tuple

import numpy as np
from scipy.integrate import solve_ivp


# --- PDG / literature inputs ---

MZ_PDG2026 = 91.1879  # GeV
ALPHA_S_MZ_PDG2026 = 0.1180
SIN2_THETA_W_MSBAR_PDG2026 = 0.23122
ALPHA_INV_MZ_PDG2024 = 127.930  # PDG 2024 recommendation; see module docstring
ALPHA_INV_0_PDG2026 = 137.035999177  # Thomson limit, not used in the running

# CC2010, for an apples-to-apples comparison with docs 45 and 47
# (these are *not* the latest PDG values).
from pathlib import Path
import sys

_CODE = Path(__file__).resolve().parents[2] / "code"
_ALT = Path(__file__).resolve().parents[1] / "alt_geometries"
for _p in (str(_CODE), str(_ALT)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from ccm_oneloop_rge import (  # noqa: E402
    B_COEFFS as SM_B_ONELOOP_UNNORM,
    CC2010_ALPHA_AT_MZ,
    MZ as MZ_CC2010,
)
from promising_candidates import (  # noqa: E402
    LIT_COMPOSITE,
    LIT_WITH_15,
    PS_B_COMPOSITE,
    PS_B_WITH_15,
    find_unification,
    ps_couplings_at_mR,
    relative_log_error,
    run_ps,
    sm_inv_g2_at,
)


# Two-loop SM, GUT normalisation
SM_B_GUT = (41.0 / 10.0, -19.0 / 6.0, -7.0)
SM_B_MATRIX_GUT = (
    (199.0 / 50.0, 27.0 / 10.0, 44.0 / 5.0),
    (9.0 / 10.0, 35.0 / 6.0, 12.0),
    (11.0 / 10.0, 9.0 / 2.0, -26.0),
)


def alpha_em_mz(alpha_inv: float = ALPHA_INV_MZ_PDG2024) -> float:
    return 1.0 / alpha_inv


def sm_alphas_at_mz_from_pdg(
    alpha_inv_mz: float = ALPHA_INV_MZ_PDG2024,
    sin2: float = SIN2_THETA_W_MSBAR_PDG2026,
    alpha_s: float = ALPHA_S_MZ_PDG2026,
) -> Tuple[float, float, float]:
    """(α1, α2, α3) at M_Z, with α1 = g'²/(4π) (CC2010 / CCvS convention)."""
    aem = alpha_em_mz(alpha_inv_mz)
    c2 = 1.0 - sin2
    a1 = aem / c2
    a2 = aem / sin2
    return (a1, a2, alpha_s)


def gut_alphas_from_unnorm(alpha_unnorm: Tuple[float, float, float]) -> Tuple[float, float, float]:
    """α̂1 = (5/3) α',  α̂2 = α2,  α̂3 = α3."""
    a1, a2, a3 = alpha_unnorm
    return ((5.0 / 3.0) * a1, a2, a3)


def unnorm_alphas_from_gut(alpha_gut: Tuple[float, float, float]) -> Tuple[float, float, float]:
    a1h, a2, a3 = alpha_gut
    return ((3.0 / 5.0) * a1h, a2, a3)


def two_loop_gauge_beta_gut(g: np.ndarray) -> np.ndarray:
    """dg_i / d ln μ  at two loops, gauge only, GUT normalisation."""
    sixteen = 16.0 * math.pi ** 2
    b = SM_B_GUT
    B = SM_B_MATRIX_GUT
    out = np.zeros(3)
    for i in range(3):
        one = b[i] * g[i] ** 3 / sixteen
        two = 0.0
        for j in range(3):
            two += B[i][j] * g[j] ** 2
        two = (g[i] ** 3 / sixteen) * (two / sixteen)
        out[i] = one + two
    return out


def run_sm_two_loop_gauge_only(
    alpha_unnorm_at_mz: Tuple[float, float, float],
    scale: float,
    mz: float,
) -> Tuple[float, float, float]:
    """α_i^{-1}(scale) in the un-normalized convention, via two-loop gauge ODE.

    Integrates the GUT-normalized couplings and converts back.  Yukawa
    contributions at two loops are omitted.
    """
    a_gut_mz = gut_alphas_from_unnorm(alpha_unnorm_at_mz)
    g0 = np.array([math.sqrt(4.0 * math.pi * a) for a in a_gut_mz], dtype=float)
    t0 = math.log(mz)
    t1 = math.log(scale)

    def rhs(t, y):
        return two_loop_gauge_beta_gut(y)

    sol = solve_ivp(rhs, (t0, t1), g0, rtol=1e-9, atol=1e-11, dense_output=False)
    if not sol.success:
        raise RuntimeError(sol.message)
    g1 = sol.y[:, -1]
    a_gut = tuple(float(gi * gi / (4.0 * math.pi)) for gi in g1)
    a_un = unnorm_alphas_from_gut(a_gut)
    return tuple(1.0 / a for a in a_un)


def sm_inv_g2_at_two_loop(
    scale: float,
    alpha_at_mz: Tuple[float, float, float],
    mz: float,
) -> Tuple[float, float, float]:
    inv_alpha = run_sm_two_loop_gauge_only(alpha_at_mz, scale, mz)
    return tuple(ia / (4.0 * math.pi) for ia in inv_alpha)


def unification_mismatch_hybrid(
    m_R: float,
    b_ps: Tuple[float, float, float],
    alpha_at_mz: Tuple[float, float, float],
    mz: float,
    sm_two_loop: bool,
) -> Optional[float]:
    """Signed mismatch of the (R,L) vs (L,g) meeting logs, or None."""
    if sm_two_loop:
        ig = sm_inv_g2_at_two_loop(m_R, alpha_at_mz, mz)
    else:
        # promising_candidates.sm_inv_g2_at uses CC2010 MZ unless we pass scale
        # and inject alphas; it uses MZ default.  Recompute with the stated mz.
        from ccm_oneloop_rge import run_alphas, B_COEFFS

        inv_alpha = run_alphas(alpha_at_mz, m_R, mz=mz)
        ig = tuple(ia / (4.0 * math.pi) for ia in inv_alpha)
    ig1, ig2, ig3 = ig
    g2 = ig3
    gL = ig2
    gR = ig1 - (2.0 / 3.0) * g2
    if gR <= 0.0 or g2 <= 0.0 or gL <= 0.0:
        return None
    bR, bL, b = b_ps

    def t_meet(inv_i, inv_j, bi, bj):
        db = bi - bj
        if db == 0:
            return None
        t = 8.0 * math.pi ** 2 * (inv_j - inv_i) / db
        return t if t > 0 else None

    t_rl = t_meet(gR, gL, bR, bL)
    t_lg = t_meet(gL, g2, bL, b)
    if t_rl is None or t_lg is None:
        return None
    return t_rl - t_lg


def find_unification_general(
    b_ps: Tuple[float, float, float],
    alpha_at_mz: Tuple[float, float, float],
    mz: float,
    sm_two_loop: bool = False,
    log10_mR_lo: float = 8.0,
    log10_mR_hi: float = 16.0,
    nscan: int = 200,
) -> Optional[Dict[str, float]]:
    logs = [log10_mR_lo + (log10_mR_hi - log10_mR_lo) * i / (nscan - 1) for i in range(nscan)]
    vals = []
    for lg in logs:
        mR = 10.0 ** lg
        vals.append((mR, unification_mismatch_hybrid(mR, b_ps, alpha_at_mz, mz, sm_two_loop)))
    bracket = None
    for (m1, d1), (m2, d2) in zip(vals, vals[1:]):
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
        mid = math.sqrt(lo * hi)
        dmid = unification_mismatch_hybrid(mid, b_ps, alpha_at_mz, mz, sm_two_loop)
        dlo = unification_mismatch_hybrid(lo, b_ps, alpha_at_mz, mz, sm_two_loop)
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
    # rebuild couplings at m_R
    if sm_two_loop:
        ig = sm_inv_g2_at_two_loop(m_R, alpha_at_mz, mz)
    else:
        from ccm_oneloop_rge import run_alphas

        inv_alpha = run_alphas(alpha_at_mz, m_R, mz=mz)
        ig = tuple(ia / (4.0 * math.pi) for ia in inv_alpha)
    ig1, ig2, ig3 = ig
    inv = {
        "inv_gR2": ig1 - (2.0 / 3.0) * ig3,
        "inv_gL2": ig2,
        "inv_g2": ig3,
    }
    bR, bL, b = b_ps
    t = 8.0 * math.pi ** 2 * (inv["inv_gL2"] - inv["inv_gR2"]) / (bR - bL)
    # careful: t_RL = 8π² (inv_L - inv_R) / (b_R - b_L)? 
    # GR2 + (bR/8π²) t = GL2 + (bL/8π²) t  ⇒  GR2 - GL2 = (bL - bR) t / 8π²
    # t = 8π² (GR2 - GL2) / (bL - bR) = 8π² (GL2 - GR2) / (bR - bL)
    # Yes.
    if t <= 0:
        return None
    Lam = m_R * math.exp(t)
    inv_L = run_ps(inv, b_ps, Lam, m_R)
    spread = max(inv_L) - min(inv_L)
    return {
        "m_R_GeV": m_R,
        "Lambda_GeV": Lam,
        "inv_g2_at_Lambda": sum(inv_L) / 3.0,
        "inv_g2_spread_at_Lambda": spread,
        "t_ln_Lambda_over_mR": t,
        "g_at_Lambda": 1.0 / math.sqrt(sum(inv_L) / 3.0) if sum(inv_L) > 0 else float("nan"),
    }


def pdg_input_table() -> Dict[str, object]:
    a = sm_alphas_at_mz_from_pdg()
    return {
        "MZ_GeV": MZ_PDG2026,
        "alpha_s": ALPHA_S_MZ_PDG2026,
        "sin2_thetaW_MSbar": SIN2_THETA_W_MSBAR_PDG2026,
        "alpha_inv_MZ": ALPHA_INV_MZ_PDG2024,
        "alpha_inv_MZ_source": "PDG 2024 recommendation 127.930(8); PDG 2026 did not recommend a new value",
        "other_source": "PDG 2026 Physical Constants for M_Z, α_s, sin²θ_W",
        "alpha1_alpha2_alpha3": a,
        "g1_g2_g3": tuple(math.sqrt(4.0 * math.pi * x) for x in a),
    }


def report() -> Dict[str, object]:
    pdg = pdg_input_table()
    a_pdg = pdg["alpha1_alpha2_alpha3"]
    out: Dict[str, object] = {"inputs": pdg, "runs": {}}
    for label, b, lit in (
        ("composite_oneloop_CC2010inputs", PS_B_COMPOSITE, LIT_COMPOSITE),
        ("composite_oneloop_PDG", PS_B_COMPOSITE, LIT_COMPOSITE),
        ("composite_sm2loop_PDG", PS_B_COMPOSITE, LIT_COMPOSITE),
        ("with15_oneloop_PDG", PS_B_WITH_15, LIT_WITH_15),
    ):
        if "CC2010" in label:
            found = find_unification_general(b, CC2010_ALPHA_AT_MZ, MZ_CC2010, sm_two_loop=False)
        elif "sm2loop" in label:
            found = find_unification_general(b, a_pdg, MZ_PDG2026, sm_two_loop=True)
        else:
            found = find_unification_general(b, a_pdg, MZ_PDG2026, sm_two_loop=False)
        rec: Dict[str, object] = {"found": found is not None, "literature_CCvS2015": lit}
        if found is not None:
            rec["computed"] = found
            rec["rel_log_error_mR"] = relative_log_error(found["m_R_GeV"], lit["m_R_GeV"])
            rec["rel_log_error_Lambda"] = relative_log_error(found["Lambda_GeV"], lit["Lambda_GeV"])
        rec["honesty"] = (
            "m_R and Λ are determined by fitting the PS meeting condition "
            "to the stated M_Z inputs.  They are not predictions of the "
            "product geometry, which does not fix either scale."
        )
        out["runs"][label] = rec
    out["prediction_of_MZ_couplings"] = {
        "possible": False,
        "reason": (
            "A top-down run from Λ through m_R to M_Z needs g(Λ) and m_R.  "
            "Neither is fixed by the geometry.  Running down from the "
            "fitted (m_R, Λ) only returns the inputs by construction."
        ),
    }
    return out
