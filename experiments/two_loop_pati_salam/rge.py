"""Two-loop SM -> Pati-Salam running and the no-tuning unification solve.

t = ln(mu / GeV).  State: (g_1, g_2, g_3, y_t) below m_R (g_1 in GUT
normalisation), (g_R, g_L, g_4, y) above m_R.

  16 pi^2 dg_a/dt = g_a^3 [ b_a + (sum_b B_ab g_b^2 - c_a y^2) / (16 pi^2) ]
  16 pi^2 dy/dt   = y [ k y^2 - sum_a G_a g_a^2 ]           (one loop)

Coefficients come from group_theory (exact Fractions -> floats once).

Unknowns: m_R and Lambda.  Conditions at Lambda: g_L = g_R (the spectral-
action normalisation of the F_0 a_4 Yang-Mills terms, CCvS2015) and
g_4 = g_L.  Two equations, two unknowns, no free parameter left: there is no
tuning knob.  Whether a solution exists is the test.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction as Fr
from typing import Dict, Optional, Sequence, Tuple

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

from group_theory import (
    pati_salam,
    sm_components_of_heavy_fields,
    sm_groups,
    standard_model,
    threshold_b,
)

PI2_16 = 16.0 * math.pi ** 2
T_CAP = 1.0e20  # search for the L=R point up to 10^20 GeV (above M_Planck)

# ---------------------------------------------------------------- inputs


@dataclass(frozen=True)
class Inputs:
    MZ: float = 91.1876
    alpha_s: float = 0.1180
    alpha_em_inv: float = 127.95
    sin2w: float = 0.23122
    mt_pole: float = 172.5

    def gauge_at_MZ(self) -> Tuple[float, float, float]:
        a = 1.0 / self.alpha_em_inv
        a1 = (5.0 / 3.0) * a / (1.0 - self.sin2w)
        a2 = a / self.sin2w
        return tuple(math.sqrt(4 * math.pi * x) for x in (a1, a2, self.alpha_s))  # type: ignore

    def yt_at_mt(self) -> float:
        """MSbar y_t(mu = M_t) from the pole mass.

        Buttazzo et al., JHEP 12 (2013) 089, arXiv:1307.3536, eq. (60) fit
        (NNLO QCD + NLO EW matching):
          y_t(M_t) = 0.93690 + 0.00556 (M_t/GeV - 173.10)
                     - 0.00042 (alpha_s(M_Z) - 0.1184)/0.0007
        """
        return 0.93690 + 0.00556 * (self.mt_pole - 173.10) - 0.00042 * (self.alpha_s - 0.1184) / 0.0007


PDG = Inputs()
PDG_ALPHA_INV_127930 = Inputs(alpha_em_inv=127.930)


# ---------------------------------------------------------------- coefficients


@dataclass
class Coeffs:
    b: np.ndarray
    B: np.ndarray
    c: np.ndarray
    k: float
    G: np.ndarray

    @staticmethod
    def from_model(m, loops: int) -> "Coeffs":
        b = np.array([float(x) for x in m.one_loop()])
        if loops >= 2:
            B = np.array([[float(x) for x in r] for r in m.two_loop()])
            c = np.array([float(m.yukawas[0][1][a]) for a in range(3)])
        else:
            B = np.zeros((3, 3))
            c = np.zeros(3)
        k, G = m.top_one_loop
        return Coeffs(b, B, c, float(k), np.array([float(x) for x in G]))


def rhs(t, s, C: Coeffs, with_yukawa: bool):
    g = s[:3]
    y = s[3]
    g2 = g * g
    two = (C.B @ g2 - (C.c * y * y if with_yukawa else 0.0)) / PI2_16
    dg = g ** 3 * (C.b + two) / PI2_16
    dy = y * (C.k * y * y - C.G @ g2) / PI2_16 if with_yukawa else 0.0
    return np.concatenate([dg, [dy]])


def _solve(C, t0, t1, s0, with_yukawa=True, dense=False, events=None):
    return solve_ivp(
        rhs, (t0, t1), s0, args=(C, with_yukawa), method="DOP853",
        rtol=1e-11, atol=1e-13, dense_output=dense, events=events,
    )


# ---------------------------------------------------------------- SM segment


class SMRun:
    """Dense SM solution from M_Z up to 10^18 GeV (reused for every m_R)."""

    def __init__(self, inp: Inputs = PDG, loops: int = 2, t_max: float = math.log(1e18)):
        self.inp = inp
        self.loops = loops
        self.C = Coeffs.from_model(standard_model(), loops)
        g0 = np.array(inp.gauge_at_MZ())
        tZ, tt = math.log(inp.MZ), math.log(inp.mt_pole)
        yt = inp.yt_at_mt()
        # M_Z -> M_t: gauge only (y_t held at y_t(M_t); the two-loop Yukawa
        # effect over ln(M_t/M_Z)=0.64 is ~1e-5 relative, stated)
        seg = _solve(self.C, tZ, tt, np.concatenate([g0, [yt]]), with_yukawa=False)
        gt = seg.y[:3, -1]
        self.sol = _solve(self.C, tt, t_max, np.concatenate([gt, [yt]]), with_yukawa=(loops >= 1), dense=True)
        self.t_max = t_max

    def at(self, mu: float) -> np.ndarray:
        return self.sol.sol(math.log(mu))


# ---------------------------------------------------------------- matching


def heavy_spectrum(scenario: str):
    comps = sm_components_of_heavy_fields(scenario)
    bs = [np.array([float(x) for x in threshold_b(f, k)]) for _, f, k in comps]
    G = sm_groups()
    TV = np.zeros(3)
    for _, f, k in comps:
        if k == "vector":
            TV += np.array([2 * float(f.S(G, a)) for a in range(3)])
        elif k == "vector_real":
            TV += np.array([float(f.S(G, a)) for a in range(3)])
    return [n for n, _, _ in comps], bs, TV


def match_to_ps(sm_state: np.ndarray, scenario: str, log10_ratios: Optional[Sequence[float]] = None,
                msbar_constant: bool = True) -> np.ndarray:
    """SM (g1,g2,g3,y) at m_R -> PS (gR,gL,g4,y) at m_R.

    alpha_1^-1 = 3/5 alpha_R^-1 + 2/5 alpha_4^-1 + d_1, alpha_2^-1 = alpha_L^-1 + d_2,
    alpha_3^-1 = alpha_4^-1 + d_3, with one-loop MSbar threshold terms
      d_i = - sum_c b_{c,i}/(2 pi) ln(M_c/m_R) - T_i(V)/(12 pi).
    """
    names, bs, TV = heavy_spectrum(scenario)
    a_inv = 4 * math.pi / sm_state[:3] ** 2
    d = np.zeros(3)
    if log10_ratios is not None:
        for bc, r in zip(bs, log10_ratios):
            d -= bc / (2 * math.pi) * (r * math.log(10.0))
    if msbar_constant:
        d -= TV / (12 * math.pi)
    a2L = a_inv[1] - d[1]
    a4 = a_inv[2] - d[2]
    aR = (5.0 / 3.0) * (a_inv[0] - d[0] - 0.4 * a4)
    g = np.sqrt(4 * math.pi / np.array([aR, a2L, a4]))
    return np.concatenate([g, [sm_state[3]]])


# ---------------------------------------------------------------- PS segment + solve


def ps_meeting(sm: SMRun, m_R: float, scenario: str, loops: int, log10_ratios=None,
               msbar_constant: bool = True):
    """Run PS from m_R to the point where g_L = g_R; return (Lambda, mismatch, state)."""
    C = Coeffs.from_model(pati_salam(scenario), loops)
    s0 = match_to_ps(sm.at(m_R), scenario, log10_ratios, msbar_constant)
    tR = math.log(m_R)

    def ev(t, s, *a):
        return 1.0 / s[0] ** 2 - 1.0 / s[1] ** 2

    ev.terminal = True
    sol = _solve(C, tR, max(tR + 1.0, math.log(T_CAP)), s0, with_yukawa=True, events=ev)
    if not sol.t_events[0].size:
        return None
    tL = sol.t_events[0][0]
    s = sol.y_events[0][0]
    a = 4 * math.pi / s[:3] ** 2  # alpha^-1 of (R, L, 4)
    return math.exp(tL), a[2] - a[1], s


def solve_unification(inp: Inputs = PDG, scenario: str = "composite", loops: int = 2,
                      log10_ratios=None, msbar_constant: Optional[bool] = None,
                      sm: Optional[SMRun] = None) -> Optional[Dict[str, float]]:
    """Find m_R with alpha_4^-1 = alpha_L^-1 at the scale where alpha_L = alpha_R."""
    if msbar_constant is None:
        msbar_constant = loops >= 2
    sm = sm or SMRun(inp, loops)

    def f(lm):
        r = ps_meeting(sm, 10 ** lm, scenario, loops, log10_ratios, msbar_constant)
        return float("nan") if r is None else r[1]

    # The L=R meeting above m_R exists only for m_R below the scale m_R* at
    # which the matched alpha_R^-1 and alpha_L^-1 already coincide (there
    # Lambda = m_R).  Bracket the root inside that window.
    def lr_gap(lm):
        s0 = match_to_ps(sm.at(10 ** lm), scenario, log10_ratios, msbar_constant)
        return 1.0 / s0[0] ** 2 - 1.0 / s0[1] ** 2

    lgrid = np.linspace(6.0, 17.5, 116)
    gaps = [lr_gap(x) for x in lgrid]
    lm_star = None
    for x0, x1, v0, v1 in zip(lgrid[:-1], lgrid[1:], gaps[:-1], gaps[1:]):
        if v0 > 0 >= v1:
            lm_star = brentq(lr_gap, x0, x1, xtol=1e-13)
            break
    if lm_star is None:
        return None
    grid = np.linspace(lm_star - 4.0, lm_star - 1e-7, 81)
    vals = [f(x) for x in grid]
    root = None
    for x0, x1, v0, v1 in zip(grid[:-1], grid[1:], vals[:-1], vals[1:]):
        if np.isfinite(v0) and np.isfinite(v1) and v0 * v1 < 0:
            root = brentq(f, x0, x1, xtol=1e-12)
            break
    if root is None:
        return None
    m_R = 10 ** root
    Lam, mis, s = ps_meeting(sm, m_R, scenario, loops, log10_ratios, msbar_constant)
    a = 4 * math.pi / s[:3] ** 2
    yR = sm.at(m_R)[3]
    return {
        "m_R_GeV": m_R,
        "Lambda_GeV": Lam,
        "alpha_U_inv": float(a[1]),
        "g_U": float(math.sqrt(4 * math.pi / a[1])),
        "residual_alpha_inv_spread": float(max(a) - min(a)),
        "y_t_at_m_R": float(yR),
        "y_at_Lambda": float(s[3]),
        "loops": loops,
        "scenario": scenario,
        "m_R_star_GeV": 10 ** lm_star,
    }


def mismatch_at_fixed_mR(inp: Inputs, m_R: float, scenario="composite", loops=2):
    """alpha_4^-1 - alpha_{L=R}^-1 at the L=R point for a *given* m_R."""
    sm = SMRun(inp, loops)
    return ps_meeting(sm, m_R, scenario, loops, None, loops >= 2)
