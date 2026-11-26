"""Doc 70: one-loop SUSY threshold corrections at M_S for the spectral SUSY boundary (exploratory).

Dual-Zero untouched.  Same spectral boundary as susy_spectral.solve (each Higgs doublet normalised
by its own Yukawa trace, tan(beta) fixed by m_b), now with

  * top Yukawa threshold, Bagnaschi-Giudice-Salvioni-Strumia arXiv:1407.4081 eqs. (22)-(25):
      yhat_t(MSSM, DR) = y_t(SM, MSbar)/sin(beta) * (1 + Dg_reg + Dg_phi + Dg_chi)
    including the gluino-stop SUSY-QCD piece  -(4/3) g3^2 [ln(M3^2/m^2) + 2 F6 - (X_t/M3) F9]
    and the stop/higgsino, wino, bino pieces (evaluated for m_Q = m_U = m_A = M1 = M2 = |mu| = M_S,
    gluino M3 = r3 M_S free, X_t free);
  * bottom Yukawa: same non-enhanced pieces plus the tan(beta)-enhanced Delta_b (gluino-sbottom,
    higgsino-stop, wino), resummed  yhat_b = y_b(1 + d_ne)/(cos(beta)(1 + Delta_b));
  * tau Yukawa: tan(beta)-enhanced Delta_tau (bino, wino; approximate, degenerate);
  * gauge couplings: DR-bar conversion and the gluino log;
  * Higgs quartic: eq. (8) with Delta lambda^{1l,reg} (9), Delta lambda^{1l,phi} (10) in the
    degenerate-scalar limit with full D-term/heavy-Higgs pieces, Delta lambda^{1l,chi} (11) and (13),
    the two-loop O(g3^2 y_t^4) term (36), plus the sbottom/stau tan(beta)-enhanced trilinears
    (same structure as the stop term with X_b = A - mu tan(beta), X_tau likewise);
  * MSSM two-loop RGEs above M_S for g_i, y_t, y_b, y_tau (Martin-Vaughn PRD 50 (1994) 2282;
    Barger-Berger-Ohmann PRD 47 (1993) 1093); SM two-loop + three-loop QCD below.
Their lambda normalisation is V = lambda/2 |H|^4; ours is V = lambda |H|^4, so lambda_ours = lambda_BGSS/2.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, asdict
from typing import Dict, Optional

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

import two_loop_higgs as th
import susy_spectral as ss
from rge import PI2_16

K = 1.0 / PI2_16


# ------------------------------------------------------------------ loop functions (1407.4081 app. A)

def _lim1(fun, x, eps=2e-3):
    if abs(abs(x) - 1) < eps:
        s = 1.0 if x > 0 else -1.0
        return 0.5 * (fun(s * (1 + 2 * eps)) + fun(s * (1 - 2 * eps)))
    return fun(x)


def F1(x): return _lim1(lambda x: x * math.log(x * x) / (x * x - 1), x)
def F2(x): return _lim1(lambda x: 6 * x * x * (2 - 2 * x * x + (1 + x * x) * math.log(x * x)) / (x * x - 1) ** 3, x)
def F3(x): return _lim1(lambda x: 2 * x * (5 * (1 - x * x) + (1 + 4 * x * x) * math.log(x * x)) / (3 * (x * x - 1) ** 2), x)
def F4(x): return _lim1(lambda x: 2 * x * (x * x - 1 - math.log(x * x)) / (x * x - 1) ** 2, x)
def F5(x): return _lim1(lambda x: 3 * x * (1 - x ** 4 + 2 * x * x * math.log(x * x)) / (1 - x * x) ** 3, x)
def F6(x): return _lim1(lambda x: (x * x - 3) / (4 * (1 - x * x)) + x * x * (x * x - 2) / (2 * (1 - x * x) ** 2) * math.log(x * x), x)
def F7(x): return _lim1(lambda x: -3 * (x ** 4 - 6 * x * x + 1) / (2 * (x * x - 1) ** 2)
                        + 3 * x ** 4 * (x * x - 3) / (x * x - 1) ** 3 * math.log(x * x), x)


def _two(fun, x1, x2, eps=2e-3):
    x1, x2 = abs(x1), abs(x2)
    if abs(x1 - 1) < eps:
        x1 = 1 + 3 * eps
    if abs(x2 - 1) < eps:
        x2 = 1 - 3 * eps
    if abs(x1 - x2) < eps:
        x2 = x1 * (1 + 4 * eps)
    return fun(x1, x2)


def F8(x1, x2):
    return _two(lambda a, b: -2 + 2 / (a * a - b * b) * (a ** 4 / (a * a - 1) * math.log(a * a)
                                                        - b ** 4 / (b * b - 1) * math.log(b * b)), x1, x2)


def F9(x1, x2):
    return _two(lambda a, b: 2 / (a * a - b * b) * (a * a / (a * a - 1) * math.log(a * a)
                                                   - b * b / (b * b - 1) * math.log(b * b)), x1, x2)


def I3(a, b, c):
    """Standard Delta_b loop function of squared masses; I(m^2,m^2,m^2) = 1/(2 m^2)."""
    def f(a, b, c):
        return -(a * b * math.log(a / b) + b * c * math.log(b / c) + c * a * math.log(c / a)) / ((a - b) * (b - c) * (c - a))
    e = 1e-3
    a, b, c = a, b * (1 + e), c * (1 - 1.3 * e) if abs(a - c) < e * a else c
    if abs(a - b) < 1e-4 * a:
        b = a * (1 + 2e-3)
    if abs(c - a) < 1e-4 * a or abs(c - b) < 1e-4 * b:
        c = c * (1 - 3e-3)
    return f(a, b, c)


# ------------------------------------------------------------------ spectrum

@dataclass(frozen=True)
class Spectrum:
    """Soft spectrum at M_S: all sfermions, m_A, M1, M2 and |mu| = M_S; gluino M3 = r3 M_S;
    sign of mu (relative to M3 > 0); X_t = A_t - mu cot(beta) = xt M_S; common A for b, tau."""
    xt: float = 0.0
    r3: float = 1.0
    sgn_mu: float = 1.0
    mu_ratio: float = 1.0      # |mu|/M_S (doc 70 scans use 1)
    tau_scale: float = 1.0     # multiplier on the approximate Delta_tau (uncertainty knob)
    two_loop_lam: bool = True
    sbottom_stau_lam: bool = True
    yuk_thr: bool = True       # y_t / non-enhanced y_b thresholds and gauge DR conversion
    db_thr: bool = True        # tan(beta)-enhanced Delta_b, Delta_tau
    lam_thr: bool = True       # loop pieces of the Higgs quartic matching (tree always kept)


def thresholds(sm: Dict[str, float], tanb: float, sp: Spectrum, yt_mssm_guess: Optional[float] = None) -> Dict[str, float]:
    """All one-loop matching quantities at Q = M_S from SM MS-bar couplings `sm` (gY, g2, g3, yt, yb, ytau)."""
    assert sp.mu_ratio == 1.0, "only |mu| = M_S is implemented for the higgsino-gaugino pieces"
    gY, g2, g3, yt = sm["gY"], sm["g2"], sm["g3"], sm["yt"]
    g1sq = 5 / 3 * gY * gY                 # GUT-normalised g1^2
    a1, a2, a3, t2 = g1sq, g2 * g2, g3 * g3, yt * yt
    sb, cb = tanb / math.sqrt(1 + tanb ** 2), 1 / math.sqrt(1 + tanb ** 2)
    cotb = 1 / tanb
    mu = sp.sgn_mu * sp.mu_ratio            # mu / M_S
    r3 = sp.r3
    x3 = 1 / r3                             # m_squark / M3
    Xt = sp.xt                              # X_t / M_S
    A = Xt + mu * cotb                      # A / M_S (common trilinear)
    Xb = A - mu * tanb
    Xtau = A - mu * tanb
    lmu = math.log(sp.mu_ratio ** 2)
    xq_mu = 1 / sp.mu_ratio                 # m_Q/|mu| ; M_i/|mu| equal to the same number here
    # --- top Yukawa, eqs. (23)-(25), all soft masses = M_S except M3 and mu
    d_reg = (a1 / 120 + 3 * a2 / 8 - 4 * a3 / 3)
    d_qcd = -(4 / 3) * a3 * (math.log(r3 * r3) + 2 * F6(x3) - (Xt / r3) * F9(x3, x3))
    sgn = sp.sgn_mu
    d_g2 = -a2 * (3 / 8 * 0.0 - 3 / 2 * 0.0 * lmu + 3 / 4 * F6(xq_mu) - 3 / 4 * F8(xq_mu, xq_mu)
                  - 3 / 4 * sgn * cotb * F9(xq_mu, xq_mu))
    d_g1 = -(3 / 5) * a1 * (1 / 36 * F6(xq_mu) + 4 / 9 * F6(xq_mu) + 1 / 12 * F8(xq_mu, xq_mu) - 1 / 3 * F8(xq_mu, xq_mu)
                            - Xt / 9 * F9(1.0, 1.0) + sgn * cotb / 12 * F9(xq_mu, xq_mu) - sgn * cotb / 3 * F9(xq_mu, xq_mu))
    d_yt = -t2 * (3 / (4 * sb * sb) * lmu + 3 / 8 * cotb ** 2 * (2 * 0.0 - 1) - Xt * Xt / 4 * F5(1.0)
                  + 1 / (sb * sb) * F6(xq_mu) + 1 / (2 * sb * sb) * F6(xq_mu))
    g1u, g1d = math.sqrt(0.6 * a1) * sb, math.sqrt(0.6 * a1) * cb
    g2u, g2d = g2 * sb, g2 * cb
    rr = sgn / sp.mu_ratio                  # M_i / mu (signed)
    d_chi = (-(1 / 6) * g1u * g1d * F5(rr) - (1 / 12) * (g1u ** 2 + g1d ** 2) * (F7(rr) + 3 * lmu)
             - (1 / 2) * g2u * g2d * F5(rr) - (1 / 4) * (g2u ** 2 + g2d ** 2) * (F7(rr) + 3 * lmu))
    dyt = K * (d_reg + d_qcd + d_g2 + d_g1 + d_yt + d_chi)
    # --- bottom Yukawa: non-enhanced pieces (QCD exact with A instead of X_t; EW as for the top), enhanced Delta_b
    ytM = yt / sb * (1 + dyt) if yt_mssm_guess is None else yt_mssm_guess
    d_ne_b = K * (d_reg - (4 / 3) * a3 * (math.log(r3 * r3) + 2 * F6(x3) - (A / r3) * F9(x3, x3)) + d_g2 + d_g1 + d_chi)
    Db_qcd = K * (4 / 3) * a3 * (mu * tanb / r3) * F9(x3, x3)
    Db_hig = K * ytM ** 2 * mu * A * tanb * I3(1.0, 1.0, mu * mu)
    Db_win = -K * a2 * mu * 1.0 * tanb * 1.5 * I3(1.0, 1.0, mu * mu)
    Delta_b = Db_qcd + Db_hig + Db_win
    Delta_tau = sp.tau_scale * K * mu * tanb * (0.6 * a1 * I3(1.0, 1.0, 1.0) - a2 * I3(1.0, 1.0, mu * mu))
    # --- gauge (DR-bar conversion, gluino log)
    fg3 = 1 + K * a3 * (0.5 - 2 * math.log(r3))
    fg2 = 1 + K * a2 / 3
    # --- Higgs quartic (BGSS normalisation), degenerate scalars, m_A = M_S
    c2b = (1 - tanb ** 2) / (1 + tanb ** 2)
    s2b = 2 * tanb / (1 + tanb ** 2)
    c4b, s4b = c2b * c2b - s2b * s2b, 2 * s2b * c2b
    c8b = c4b * c4b - s4b * s4b
    gp = 0.6 * a1 + a2
    lam_tree = gp / 4 * c2b ** 2
    l_reg = -(9 / 100 * a1 * a1 + 3 / 10 * a1 * a2 + (3 / 4 - c2b ** 2 / 6) * a2 * a2)
    X2 = Xt * Xt
    l_phi = (6 * t2 * t2 * X2 * (F1(1.0) - X2 / 12 * F2(1.0))
             + 3 / 4 * t2 * X2 * c2b * (0.6 * a1 * F3(1.0) + a2 * F4(1.0))
             - 1 / 4 * t2 * X2 * c2b ** 2 * gp * F5(1.0)
             + (261 * a1 * a1 + 630 * a1 * a2 + 1325 * a2 * a2 - 4 * c4b * (9 * a1 * a1 + 90 * a1 * a2 + 175 * a2 * a2)
                - 9 * c8b * (3 * a1 + 5 * a2) ** 2) / 4800
             - 3 / 16 * gp ** 2 * s4b ** 2)
    # sbottom / stau trilinears: coupling of the SM-like Higgs = yhat cos(beta) = y^SM/(1+Delta)
    l_sb = 0.0
    if sp.sbottom_stau_lam:
        hb = sm["yb"] / (1 + Delta_b)
        htau = sm["ytau"] / (1 + Delta_tau)
        l_sb = 6 * hb ** 4 * Xb ** 2 * (1 - Xb ** 2 / 12) + 2 * htau ** 4 * Xtau ** 2 * (1 - Xtau ** 2 / 12)
    l_chi1 = 0.0
    # eq. (11) with all r = M_i/mu = rr; f_i(1) = 1 at |mu| = M_i (only implemented there)
    if abs(abs(rr) - 1) < 1e-9:
        lt = lam_tree
        betl = (2 * lt * (g1d ** 2 + g1u ** 2 + 3 * g2d ** 2 + 3 * g2u ** 2) - g1d ** 4 - g1u ** 4 - 5 * g2d ** 4 - 5 * g2u ** 4
                - 4 * g1d * g1u * g2d * g2u - 2 * (g1d ** 2 + g2u ** 2) * (g1u ** 2 + g2d ** 2))
        s = sgn  # odd pieces flip with sign(mu): f(r)=F5 odd; f5..f8 limits taken at |r| = 1 times parity
        l_chi1 = (0.5 * betl * lmu - 7 / 12 * (g1d ** 4 + g1u ** 4) - 9 / 4 * (g2d ** 4 + g2u ** 4)
                  - 3 / 2 * g1d ** 2 * g1u ** 2 - 7 / 2 * g2d ** 2 * g2u ** 2 - 8 / 3 * s * g1d * g1u * g2d * g2u
                  - 7 / 6 * (g1d ** 2 * g2d ** 2 + g1u ** 2 * g2u ** 2) - 1 / 6 * (g1d ** 2 * g2u ** 2 + g1u ** 2 * g2d ** 2)
                  - 4 / 3 * s * (g1d * g2u + g1u * g2d) * (g1d * g2d + g1u * g2u)
                  + 2 / 3 * s * g1d * g1u * (lt - 2 * (g1d ** 2 + g1u ** 2)) + 2 * s * g2d * g2u * (lt - 2 * (g2d ** 2 + g2u ** 2))
                  + 1 / 3 * lt * (g1d ** 2 + g1u ** 2) + lt * (g2d ** 2 + g2u ** 2))
    l_chi2 = -1 / 6 * c2b ** 2 * (2 * a2 * a2 * 0.0 + (9 / 25 * a1 * a1 + a2 * a2) * lmu)
    l_2l = 0.0
    if sp.two_loop_lam:
        # eq. (36): valid for M3 = m_Q = m_U = M_S; used for all r3 (uncertainty quoted)
        l_2l = a3 * t2 * t2 / (96 * math.pi ** 4) * (-12 * Xt - 6 * X2 + 14 * Xt ** 3 + X2 * X2 / 2 - Xt ** 5)  # erratum 2026-11-26: was -Xt**5/4; BGSS 1407.4081 eq. (36) has -X_t^5/M_S^5
    lam_bgss = lam_tree + (K * (l_reg + l_phi + l_sb + l_chi1 + l_chi2) + l_2l if sp.lam_thr else 0.0)
    if not sp.yuk_thr:
        dyt, d_ne_b, fg3, fg2 = 0.0, 0.0, 1.0, 1.0
    if not sp.db_thr:
        Delta_b = Db_qcd = Db_hig = Db_win = Delta_tau = 0.0
    return {"dyt": dyt, "d_qcd": K * d_qcd, "d_ew": K * (d_reg + 4 / 3 * a3 + d_g2 + d_g1 + d_chi), "d_yuk": K * d_yt,
            "d_ne_b": d_ne_b, "Delta_b": Delta_b, "Db_qcd": Db_qcd, "Db_hig": Db_hig, "Db_win": Db_win,
            "Delta_tau": Delta_tau, "fg3": fg3, "fg2": fg2, "lam": lam_bgss / 2, "lam_tree": lam_tree / 2,
            "lam_1l_stop": K * l_phi / 2, "lam_sb_stau": K * l_sb / 2, "lam_2l": l_2l / 2,
            "lam_reg_chi": K * (l_reg + l_chi1 + l_chi2) / 2}


# ------------------------------------------------------------------ MSSM two-loop RGEs (third family)

def mssm_rhs2(t, s, nu_on: float):
    g1, g2, g3, yt, yb, ytau, yn = s
    g = np.array([g1, g2, g3])
    gg = g * g
    t2, b2, l2 = yt * yt, yb * yb, ytau * ytau
    n2 = yn * yn if t > nu_on else 0.0
    two = (ss.C_MSSM.B @ gg - ss.C_MSSM.c * t2 - ss.CB * b2 - ss.CTAU * l2) / PI2_16
    dg = g ** 3 * (ss.C_MSSM.b + two) / PI2_16
    a, b, c = gg
    dyt = yt * (6 * t2 + b2 + n2 - 16 / 3 * c - 3 * b - 13 / 15 * a)
    dyt2 = yt * (-22 * t2 * t2 - 5 * b2 * b2 - 5 * t2 * b2 - b2 * l2 + (6 / 5 * a + 6 * b + 16 * c) * t2 + 0.4 * a * b2
                 + 2743 / 450 * a * a + 7.5 * b * b - 16 / 9 * c * c + a * b + 136 / 45 * a * c + 8 * b * c)
    dyb = yb * (t2 + 6 * b2 + l2 - 16 / 3 * c - 3 * b - 7 / 15 * a)
    dyb2 = yb * (-22 * b2 * b2 - 5 * t2 * t2 - 5 * b2 * t2 - 3 * b2 * l2 - 3 * l2 * l2 + 0.8 * a * t2
                 + (0.4 * a + 6 * b + 16 * c) * b2 + 1.2 * a * l2
                 + 287 / 90 * a * a + 7.5 * b * b - 16 / 9 * c * c + a * b + 8 / 9 * a * c + 8 * b * c)
    dyl = ytau * (3 * b2 + 4 * l2 + n2 - 3 * b - 9 / 5 * a)
    dyl2 = ytau * (-10 * l2 * l2 - 9 * b2 * b2 - 9 * b2 * l2 - 3 * b2 * t2 + (1.2 * a + 6 * b) * l2
                   + (-0.4 * a + 16 * c) * b2 + 13.5 * a * a + 7.5 * b * b + 1.8 * a * b)
    dyn = yn * (3 * t2 + 4 * n2 + l2 - 3 * b - 0.6 * a) if t > nu_on else 0.0
    return np.concatenate([dg, np.array([dyt + dyt2 / PI2_16, dyb + dyb2 / PI2_16, dyl + dyl2 / PI2_16, dyn]) / PI2_16])


def run_up_thr(Mt: float, tanb: float, M_S: float, sp: Spectrum, n: float = 0.0, M_N: float = 1e14,
               alpha_s: float = 0.1180, qcd3: bool = True, t_end: float = math.log(1e20)):
    p = th.Phys(Mt=Mt, alpha_s=alpha_s)
    m = th.msbar_at_Mt(p)
    s0 = [m["gY"], m["g2"], m["g3"], m["yt"], m["yb"], m["ytau"], m["lambda"]]
    low = th.run_sm(s0, Mt, M_S, 2, qcd3, dense=True)
    gY, g2, g3, yt, yb, ytau, _ = low.y[:, -1]
    sm = dict(gY=gY, g2=g2, g3=g3, yt=yt, yb=yb, ytau=ytau)
    thr = thresholds(sm, tanb, sp)
    sb, cb = tanb / math.sqrt(1 + tanb ** 2), 1 / math.sqrt(1 + tanb ** 2)
    sM = [gY * math.sqrt(5 / 3), g2 * thr["fg2"], g3 * thr["fg3"], yt / sb * (1 + thr["dyt"]),
          yb * (1 + thr["d_ne_b"]) / (cb * (1 + thr["Delta_b"])), ytau / (cb * (1 + thr["Delta_tau"])), 0.0]
    blow = lambda t, y, *a: 3.5 - float(np.max(np.abs(y)))
    blow.terminal = True
    hi = solve_ivp(mssm_rhs2, (math.log(M_S), t_end), sM, args=(math.log(M_N),), method="DOP853",
                   rtol=1e-9, atol=1e-12, dense_output=True, events=blow)
    return low, hi, sm, thr


def solve_thr(M_S: float, sp: Spectrum = Spectrum(), n: float = 1.0, dI: float = 4.0, da_u: float = 8.0,
              da_d: Optional[float] = None, trace: str = "S0 SM fermions only (CCM traces)", which: str = "12",
              alpha_s: float = 0.1180, qcd3: bool = True) -> Dict[str, object]:
    """Spectral SUSY boundary with full one-loop matching at M_S.  Default content = doc 69 candidate #10
    (S0 traces + one Higgs-coupled VL PS pair, universal y = y_t on both chains: dI = 4, da = 8, n = 1)."""
    I = tuple(x + dI for x in ss.TRACES[trace])
    dd = da_u if da_d is None else da_d
    cache = {}

    def at(Mt, tanb):
        low, hi, sm, thr = run_up_thr(Mt, tanb, M_S, sp, n, alpha_s=alpha_s, qcd3=qcd3)
        if not hi.success or thr["Delta_b"] <= -0.9:
            return None
        tB = ss.boundary_scale(hi, I, which)
        if tB is None:
            return None
        g1, g2, g3, yt, yb, ytau, _ = hi.sol(tB)
        Kb = (2 / 3) * I[1] * g2 * g2
        return yt - math.sqrt(Kb / (3 + n + da_u)), (3 + dd) * yb * yb + ytau * ytau - Kb

    def mt_of(tanb):
        if tanb in cache:
            return cache[tanb]
        f = lambda Mt: (lambda r: float("nan") if r is None else r[0])(at(Mt, tanb))
        x = ss._bracket_root(f, 150.0, 220.0, 15)
        cache[tanb] = x
        return x

    def hd(tanb):
        Mt = mt_of(tanb)
        if Mt != Mt:
            return float("nan")
        r = at(Mt, tanb)
        return float("nan") if r is None else r[1]

    tb = ss._bracket_root(hd, 5.0, 120.0, 21, log=True)
    base = {"M_S": M_S, "spectrum": asdict(sp), "n": n, "dI": dI, "da_u": da_u}
    if tb != tb:
        return {"ok": False, **base}
    Mt = float(mt_of(tb))
    low, hi, sm, thr = run_up_thr(Mt, tb, M_S, sp, n, alpha_s=alpha_s, qcd3=qcd3)
    tB = ss.boundary_scale(hi, I, which)
    g1, g2, g3 = hi.sol(tB)[:3]
    a = 4 * math.pi / np.array([g1, g2, g3]) ** 2 / np.array(I)
    mis = float(a[2] / a[1] - 1)
    gY, gw, gs, ytS, ybS, ytauS, _ = low.y[:, -1]
    down = th.run_sm([gY, gw, gs, ytS, ybS, ytauS, thr["lam"]], M_S, Mt, 2, qcd3)
    Mh = th.Mh_from_lambda(down.y[6, -1], Mt)
    return {"ok": True, **base, "Mt": Mt, "tanb": float(tb), "Mh": float(Mh), "Lambda": float(math.exp(tB)),
            "yt_over_g": float(hi.sol(tB)[3] / g2), "unif_mismatch": mis, "lam_MS": thr["lam"],
            **{k: float(v) for k, v in thr.items() if k not in ("lam",)}}


def mh_only(M_S: float, Mt: float, tanb: float, sp: Spectrum, alpha_s: float = 0.1180, qcd3: bool = True) -> float:
    """Plain MSSM EFT Higgs mass for given (M_t, tan beta, M_S, spectrum): validation against SusyHD-type results."""
    p = th.Phys(Mt=Mt, alpha_s=alpha_s)
    m = th.msbar_at_Mt(p)
    s0 = [m["gY"], m["g2"], m["g3"], m["yt"], m["yb"], m["ytau"], m["lambda"]]
    low = th.run_sm(s0, Mt, M_S, 2, qcd3)
    gY, g2, g3, yt, yb, ytau, _ = low.y[:, -1]
    thr = thresholds(dict(gY=gY, g2=g2, g3=g3, yt=yt, yb=yb, ytau=ytau), tanb, sp)
    down = th.run_sm([gY, g2, g3, yt, yb, ytau, thr["lam"]], M_S, Mt, 2, qcd3)
    return float(th.Mh_from_lambda(down.y[6, -1], Mt))
