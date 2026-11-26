"""Doc 72: generalised one-loop (+ selected two-loop) SUSY matching at Q = M_S for the spectral SUSY
boundary of doc 69/70 candidate #10.  Dual-Zero regulator untouched.

Formulas (all transcribed from the sources, not re-derived):
  * BGSS = Bagnaschi-Giudice-Salvioni-Strumia arXiv:1407.4081 (latest arXiv source):
      lambda tree + Delta lambda^{reg} (eq. dmsbar), Delta lambda^{phi} general (eq. threshsusy),
      Delta lambda^{chi1} general (eq. hss, f_i from app. A), Delta lambda^{chi2},
      Delta g_t^{reg, phi, chi} general (eqs. dgtreg, dgtphi, dgtchi), gauge thresholds (dg1-dg3).
  * O(alpha_t alpha_s) two-loop lambda: BGSS eq. (d2lhss) for M3 = mQ = mU (coefficient of X^5 is -1, as in
    BGSS and in FlexibleSUSY meta/SM/HSSUSY_corrections.m; doc 70 code has -1/4: a transcription bug),
    and FlexibleSUSY 'lambda2LPhiHSSAlphaTAlphaSFull' (P. Slavich, general masses) otherwise.
  * O(alpha_t^2) two-loop lambda: FlexibleSUSY 'lambda2LHSSAlphaT2' (degenerate stops, any mu, tan beta).
  * Two-loop O(alpha_s^2) SUSY-QCD top-Yukawa matching: sqcd2l.py (Bednyakov et al. via FlexibleSUSY).
  * tan(beta)-enhanced Delta_b, Delta_tau: standard one-loop forms (Carena et al. hep-ph/9912516 style),
    same as doc 70 but with general masses; sbottom/stau lambda pieces: doc 70 approximation.
Normalisation: BGSS lambda (V = lambda/2 |H|^4); returned 'lam' is ours (V = lambda |H|^4) = BGSS/2.
"""
from __future__ import annotations
import math
from dataclasses import dataclass, asdict
from typing import Dict, Optional
import numpy as np
from scipy.integrate import solve_ivp
import mpmath

from common import *
import two_loop_higgs as th
import susy_spectral as ss
import susy_thresholds as st
from susy_thresholds import F1, F2, F3, F4, F5, F6, F7, F8, F9, I3
from rge import PI2_16

K = 1.0 / PI2_16


@dataclass(frozen=True)
class Spec:
    """All masses in units of M_S (= matching scale Q). mu is signed (relative to M3 > 0)."""
    xt: float = 0.0          # X_t / M_S
    mQ: float = 1.0          # third-generation doublet squark
    mU: float = 1.0          # right stop
    mD: float = 1.0          # right sbottom
    msf: float = 1.0         # all other sfermions (1st/2nd gen squarks, all sleptons)
    M1: float = 1.0
    M2: float = 1.0
    M3: float = 1.0
    mu: float = 1.0
    mA: float = 1.0
    tau_scale: float = 1.0
    msl: float = 0.0         # doc 75 (add-only): slepton mass; 0 -> use msf (all earlier docs)
    fix_x5: bool = True      # BGSS X^5 coefficient (-1) instead of doc-70 (-1/4)
    at2: bool = True         # O(alpha_t^2) lambda
    sqcd2: bool = True       # two-loop SQCD y_t matching
    general_2l: bool = True  # FS general O(at as) when masses are non-degenerate


def _f1(r): return st._lim1(lambda r: 6 * (r * r + 3) * r * r / (7 * (r * r - 1) ** 2) + 6 * (r * r - 5) * r ** 4 * math.log(r * r) / (7 * (r * r - 1) ** 3), r)
def _f2(r): return st._lim1(lambda r: 2 * (r * r + 11) * r * r / (9 * (r * r - 1) ** 2) + 2 * (5 * r * r - 17) * r ** 4 * math.log(r * r) / (9 * (r * r - 1) ** 3), r)
def _f3(r): return st._lim1(lambda r: 2 * (r ** 4 + 9 * r * r + 2) / (3 * (r * r - 1) ** 2) + 2 * (r ** 4 - 7 * r * r - 6) * r * r * math.log(r * r) / (3 * (r * r - 1) ** 3), r)
def _f4(r): return st._lim1(lambda r: 2 * (5 * r ** 4 + 25 * r * r + 6) / (7 * (r * r - 1) ** 2) + 2 * (r ** 4 - 19 * r * r - 18) * r * r * math.log(r * r) / (7 * (r * r - 1) ** 3), r)


def _two_r(fun, r1, r2, eps=2e-3):
    # regularise r = +-1 and r1 = r2 (keep signs: f5..f8 are odd/even in r)
    def nud(r, k):
        return r * (1 + k * eps) if abs(abs(r) - 1) < eps else r
    r1, r2 = nud(r1, 3), nud(r2, -3)
    if abs(r1 - r2) < eps * max(1, abs(r1)):
        r2 = r1 * (1 + 4 * eps) if r1 != 0 else 4 * eps
    return fun(r1, r2)


def _f5(r1, r2): return _two_r(lambda a, b: 0.75 * ((1 + (a + b) ** 2 - a * a * b * b) / ((a * a - 1) * (b * b - 1)) + a ** 3 * (a * a + 1) * math.log(a * a) / ((a * a - 1) ** 2 * (a - b)) - b ** 3 * (b * b + 1) * math.log(b * b) / ((a - b) * (b * b - 1) ** 2)), r1, r2)
def _f6(r1, r2): return _two_r(lambda a, b: 6 / 7 * ((a * a + b * b + a * b - a * a * b * b) / ((a * a - 1) * (b * b - 1)) + a ** 5 * math.log(a * a) / ((a * a - 1) ** 2 * (a - b)) - b ** 5 * math.log(b * b) / ((a - b) * (b * b - 1) ** 2)), r1, r2)
def _f7(r1, r2): return _two_r(lambda a, b: 6 * ((1 + a * b) / ((a * a - 1) * (b * b - 1)) + a ** 3 * math.log(a * a) / ((a * a - 1) ** 2 * (a - b)) - b ** 3 * math.log(b * b) / ((a - b) * (b * b - 1) ** 2)), r1, r2)
def _f8(r1, r2): return _two_r(lambda a, b: 1.5 * ((a + b) / ((a * a - 1) * (b * b - 1)) + a ** 4 * math.log(a * a) / ((a * a - 1) ** 2 * (a - b)) - b ** 4 * math.log(b * b) / ((a - b) * (b * b - 1) ** 2)), r1, r2)


def F5s(x):  # f(r) = F5(r) for signed r (F5 is odd in x)
    return F5(x)


def F7s(x):  # g(r) = F7(r), even in x
    return F7(abs(x))


def li2(z):
    return float(mpmath.polylog(2, z).real)


def lam2l_atas_full(g3, ht, M3, mQ, mU, Xt_abs, Q):
    """FlexibleSUSY lambda2LPhiHSSAlphaTAlphaSFull (P. Slavich; BGSS normalisation). Masses in GeV-like units."""
    CF, Nc = 4 / 3, 3
    as_ = g3 * g3 / (4 * math.pi)
    g = M3 * M3
    x1 = mQ * mQ * (1 - 0.005) / (M3 * (1 + 0.001)) ** 2
    x2 = mU * mU / (M3 * (1 - 0.005)) ** 2
    q2 = Q * Q
    Xt = Xt_abs / M3
    L, Lg = math.log, math.log(g / q2)
    P1, P2 = li2((-1 + x1) / x1), li2((-1 + x2) / x2)
    l1, l2 = L(x1), L(x2)
    t = (-12 * Lg ** 2 + ((-6 + 8 * x1 - 4 * x1 ** 2) * l1 ** 2) / (-1 + x1) ** 2
         + Lg * (8 - 4 / x1 - 4 / x2 - 12 * l1 - 12 * l2)
         + (2 * (-7 + 7 * x2 - 3 * x2 ** 2 + x1 * (6 - 5 * x2 + 2 * x2 ** 2)) * l2) / ((-1 + x1) * (-1 + x2) ** 2)
         + ((-6 + 8 * x2 - 4 * x2 ** 2) * l2 ** 2) / (-1 + x2) ** 2
         + l1 * ((2 * (-7 + x1 * (7 - 5 * x2) + 6 * x2 + x1 ** 2 * (-3 + 2 * x2))) / ((-1 + x1) ** 2 * (-1 + x2))
                 - (2 * ((-2 + x2) * x2 + x1 * (-2 + 8 * x2 - 4 * x2 ** 2) + x1 ** 2 * (1 - 4 * x2 + 2 * x2 ** 2)) * l2) / ((-1 + x1) ** 2 * (-1 + x2) ** 2))
         + Xt ** 2 * (-8 / (x1 * x2) - (4 * (4 * x1 ** 3 - x2 - 2 * x1 ** 2 * (4 + x2) + x1 * (3 + 4 * x2)) * l1 ** 2) / ((-1 + x1) ** 2 * (x1 - x2) ** 2)
                      - (4 * (7 + 3 * x1 * (-2 + x2) - 4 * x2) * l2) / ((-1 + x1) * (x1 - x2) * (-1 + x2))
                      + (4 * (x2 * (-3 + 8 * x2 - 4 * x2 ** 2) + x1 * (1 - 4 * x2 + 2 * x2 ** 2)) * l2 ** 2) / ((x1 - x2) ** 2 * (-1 + x2) ** 2)
                      + Lg * (8 / (x1 * x2) - (24 * l1) / (x1 - x2) + (24 * l2) / (x1 - x2))
                      + l1 * ((4 * (7 - 6 * x2 + x1 * (-4 + 3 * x2))) / ((-1 + x1) * (x1 - x2) * (-1 + x2))
                              + (4 * (((-2 + x1) * x1 * (x1 - x2)) / (-1 + x1) ** 2 + ((-2 + x2) * x2 * (-x1 + x2)) / (-1 + x2) ** 2 + 2 * (x1 + x2)) * l2) / (x1 - x2) ** 2))
         + Xt ** 5 * ((-8 * x1 * (x1 + x2) * l1 ** 2) / ((-1 + x1) * (x1 - x2) ** 4) + (16 * x2 * l2) / ((-1 + x2) * (-x1 + x2) ** 3)
                      - (8 * x2 * (x1 + x2) * l2 ** 2) / ((x1 - x2) ** 4 * (-1 + x2))
                      + l1 * ((16 * x1) / ((-1 + x1) * (x1 - x2) ** 3) + (8 * (x1 + x2) * (-x2 + x1 * (-1 + 2 * x2)) * l2) / ((-1 + x1) * (x1 - x2) ** 4 * (-1 + x2))))
         + Xt * ((8 * (-2 + x1) * l1 ** 2) / ((-1 + x1) * (x1 - x2)) + (16 * l2) / (x1 - x2) - (8 * (-2 + x2) * l2 ** 2) / ((x1 - x2) * (-1 + x2))
                 + Lg * ((16 * l1) / (x1 - x2) - (16 * l2) / (x1 - x2))
                 + l1 * (-16 / (x1 - x2) - (8 * l2) / ((-1 + x1) * (-1 + x2)))
                 + (32 * (-((-1 + x2) * P1) + (-1 + x1) * P2)) / ((-1 + x1) * (x1 - x2) * (-1 + x2)))
         - (2 * (4 * x1 * (-1 + x2) ** 2 * x2 * P1 + (-1 + x1) * ((-1 + x2) * (2 * (-1 + x2) * x2 + x1 * (-2 + 9 * x2 - 6 * x2 ** 2) + x1 ** 2 * (2 - 6 * x2 + 3 * x2 ** 2)) + 4 * (-1 + x1) * x1 * x2 * P2))) / ((-1 + x1) ** 2 * x1 * (-1 + x2) ** 2 * x2)
         + Xt ** 3 * ((8 * (-2 + x1 ** 2 - 3 * x1 * (-1 + x2) + x2) * l1 ** 2) / ((-1 + x1) * (x1 - x2) ** 3) - (16 * (x1 + 3 * x2) * l2) / (x1 - x2) ** 3
                      + (8 * (-2 + x1 + 3 * x2 - 3 * x1 * x2 + x2 ** 2) * l2 ** 2) / ((-1 + x2) * (-x1 + x2) ** 3)
                      + Lg * (32 / (x1 - x2) ** 2 - (16 * (x1 + x2) * l1) / (x1 - x2) ** 3 + (16 * (x1 + x2) * l2) / (x1 - x2) ** 3)
                      + l1 * ((16 * (3 * x1 + x2)) / (x1 - x2) ** 3 + (16 * (x1 + x2 - 2 * x1 * x2) * l2) / ((-1 + x1) * (x1 - x2) ** 2 * (-1 + x2)))
                      - (16 * (4 * (x1 - x2) + (-2 + x1 + x2) * P1 - (-2 + x1 + x2) * P2)) / (x1 - x2) ** 3)
         + Xt ** 4 * ((2 * (5 * x1 ** 4 + 4 * x1 ** 3 * (-2 + x2) - 2 * x2 - x1 ** 2 * x2 * (10 + x2) + 2 * x1 * (1 + 4 * x2 + x2 ** 2)) * l1 ** 2) / ((-1 + x1) ** 2 * (x1 - x2) ** 4)
                      + (2 * (-4 - 7 * x2 + 29 * x2 ** 2 - 16 * x2 ** 3 + x1 ** 2 * (6 - 7 * x2 + 3 * x2 ** 2) + x1 * (-3 + 15 * x2 - 31 * x2 ** 2 + 15 * x2 ** 3)) * l2) / ((-1 + x1) * (x1 - x2) ** 3 * (-1 + x2) ** 2)
                      - (2 * (-2 * x2 + x1 ** 2 * (-2 + x2) * x2 + 8 * x2 ** 3 - 5 * x2 ** 4 - 2 * x1 * (-1 + x2) ** 2 * (-1 + 2 * x2)) * l2 ** 2) / ((x1 - x2) ** 4 * (-1 + x2) ** 2)
                      + Lg * ((-4 * (x1 + x2 + 6 * x1 * x2)) / (x1 * (x1 - x2) ** 2 * x2) + (4 * (2 + 3 * x1 + 3 * x2) * l1) / (x1 - x2) ** 3 - (4 * (2 + 3 * x1 + 3 * x2) * l2) / (x1 - x2) ** 3)
                      + l1 * ((2 * (4 + x1 ** 3 * (16 - 15 * x2) + 3 * x2 - 6 * x2 ** 2 + x1 ** 2 * (-29 + 31 * x2 - 3 * x2 ** 2) + x1 * (7 - 15 * x2 + 7 * x2 ** 2))) / ((-1 + x1) ** 2 * (x1 - x2) ** 3 * (-1 + x2))
                              + (2 * (-4 * x1 ** 2 - 8 * x1 * x2 - 4 * x2 ** 2 - ((-2 + x1) * x1 * (x1 - x2) * (x1 + x2)) / (-1 + x1) ** 2 - ((-2 + x2) * x2 * (-x1 + x2) * (x1 + x2)) / (-1 + x2) ** 2) * l2) / (x1 - x2) ** 4)
                      - (4 * (-x1 ** 2 + x1 ** 3 - 6 * x1 ** 2 * x2 + 5 * x1 ** 3 * x2 + x2 ** 2 + 6 * x1 * x2 ** 2 - 5 * x1 ** 3 * x2 ** 2 - x2 ** 3 - 5 * x1 * x2 ** 3 + 5 * x1 ** 2 * x2 ** 3
                              + (-1 + x1) * x1 * (-1 + x2) * x2 * (-2 + x1 + x2) * P1 - (-1 + x1) * x1 * (-1 + x2) * x2 * (-2 + x1 + x2) * P2)) / ((-1 + x1) * x1 * (x1 - x2) ** 3 * (-1 + x2) * x2)))
    return ht ** 4 * as_ * CF * Nc / (4 * math.pi) ** 3 * t


def lam2l_atas_deg(g3, ht, xt):
    """BGSS eq. (d2lhss), M3 = mQ = mU = M_S = Q (BGSS normalisation)."""
    return g3 * g3 * ht ** 4 / (96 * math.pi ** 4) * (-12 * xt - 6 * xt ** 2 + 14 * xt ** 3 + xt ** 4 / 2 - xt ** 5)


def lam2l_at2(gt, tanb, mst, mu, Xt, Q):
    """FlexibleSUSY lambda2LHSSAlphaT2 (O(alpha_t^2), degenerate stops; BGSS normalisation)."""
    T = tanb
    c2 = 1 + T * T
    s2b = 2 * T / c2
    csc = 1 / s2b
    Lm = math.log(mst ** 2 / Q ** 2)
    r = mu * mu / mst ** 2
    near = abs(-1 + r) < 1e-5
    pwA = -9 / 4 if near else ((-1 + 2 * r + 2 * r * r) * (-math.pi ** 2 / 6 - r * math.log(r) + math.log(r) * math.log(abs(1 - r)) + li2(r))) / abs((1 - r) ** 2)
    pwB = -1 if near else (r * math.log(r)) / (1 - r)
    pwC = 0.5 if near else (1 + (r * math.log(r)) / (1 - r)) / (1 - r)
    Y = Xt / mst + 2 * mu * csc / mst
    x = Xt / mst
    val = (1 / 2 - 8.34993159891064 / c2 + 6 * r
           + x ** 6 * (-1 / 2 + (1 / 2 - Lm / 2) / c2 + Lm / 2) - 4 * Lm + 13 * Lm / c2 - 6 * r * Lm + 3 * Lm ** 2 - 3 * Lm ** 2 / c2
           + x ** 3 * Y * (0.8747904000000002 / c2 - 2 * Lm / c2)
           + Y ** 2 * (0.1252095999999998 / c2 + 3 * Lm / c2)
           + x * Y * (0.5008383999999992 / c2 + 12 * Lm / c2)
           + 4 * pwA - 8 * pwB - 2 * r * pwB + 3 * r * pwC
           + x ** 2 * (-7 + 19.6878144 / c2 - 6 * r + 27 * Lm - 24 * Lm / c2 + 6 * r * Lm + Y ** 2 * (-0.021147733333332752 / c2 - 3 * Lm / c2)
                       + 4 * pwB - 6 * r * pwB - 4 * pwC - 6 * r * pwC)
           + x ** 4 * (11 / 2 - 25 / (4 * c2) + r - 13 * Lm / 2 + 6 * Lm / c2 - r * Lm + Y ** 2 * (-0.020728533333333354 / c2 + Lm / (2 * c2))
                       - pwB / 2 + r * pwB + pwC / 2 + r * pwC / 2))
    return 3 * c2 * val * gt ** 6 / (256 * math.pi ** 4 * T * T)


def thresholds72(sm: Dict[str, float], tanb: float, sp: Spec, M_S: float) -> Dict[str, float]:
    gY, g2, g3, yt = sm["gY"], sm["g2"], sm["g3"], sm["yt"]
    a1, a2, a3 = 5 / 3 * gY * gY, g2 * g2, g3 * g3        # a1 = GUT g1^2
    g1 = math.sqrt(a1)
    t2 = yt * yt
    sb, cb = tanb / math.sqrt(1 + tanb ** 2), 1 / math.sqrt(1 + tanb ** 2)
    cotb = 1 / tanb
    mQ, mU, mD, msf = sp.mQ, sp.mU, sp.mD, sp.msf
    M1, M2, M3, mu, mA = sp.M1, sp.M2, sp.M3, sp.mu, sp.mA
    amu = abs(mu)
    lg = lambda m: math.log(m * m)        # ln(m^2/Q^2), Q = M_S
    Xt = sp.xt
    A = Xt + mu * cotb
    Xb = A - mu * tanb
    Xtt = Xt * Xt / (mQ * mU)
    xqu = mQ / mU
    # ---------------- top Yukawa (BGSS dgtreg, dgtphi, dgtchi)
    d_reg = a1 / 120 + 3 * a2 / 8 - 4 * a3 / 3
    d_qcd = -(4 / 3) * a3 * (lg(M3) + F6(mQ / M3) + F6(mU / M3) - (Xt / M3) * F9(mQ / M3, mU / M3))
    d_g2 = -a2 * (3 / 8 * lg(M2) - 3 / 2 * lg(amu) + 3 / 4 * F6(mQ / M2) - 3 / 4 * F8(mQ / amu, M2 / amu)
                  - 3 / 4 * (M2 / mu) * cotb * F9(mQ / amu, M2 / amu))
    d_g1 = -(3 / 5) * a1 * (17 / 72 * lg(M1) - 1 / 2 * lg(amu) + 1 / 36 * F6(mQ / M1) + 4 / 9 * F6(mU / M1)
                            + 1 / 12 * F8(mQ / amu, M1 / amu) - 1 / 3 * F8(mU / amu, M1 / amu)
                            - Xt / (9 * M1) * F9(mQ / M1, mU / M1)
                            + M1 * cotb / (12 * mu) * F9(mQ / amu, M1 / amu) - M1 * cotb / (3 * mu) * F9(mU / amu, M1 / amu))
    d_yt = -t2 * (3 / (4 * sb * sb) * lg(amu) + 3 / 8 * cotb ** 2 * (2 * lg(mA) - 1) - Xtt / 4 * F5(xqu)
                  + 1 / (sb * sb) * F6(mQ / amu) + 1 / (2 * sb * sb) * F6(mU / amu))
    g1u, g1d = math.sqrt(0.6) * g1 * sb, math.sqrt(0.6) * g1 * cb
    g2u, g2d = g2 * sb, g2 * cb
    r1, r2 = M1 / mu, M2 / mu
    lmu = lg(amu)
    d_chi = (-(1 / 6) * g1u * g1d * F5s(r1) - (1 / 12) * (g1u ** 2 + g1d ** 2) * (F7s(r1) + 3 * lmu)
             - (1 / 2) * g2u * g2d * F5s(r2) - (1 / 4) * (g2u ** 2 + g2d ** 2) * (F7s(r2) + 3 * lmu))
    dyt = K * (d_reg + d_qcd + d_g2 + d_g1 + d_yt + d_chi)
    dyt2 = 0.0
    if sp.sqcd2:
        import sqcd2l
        e = sqcd2l.expansion(g3, M_S, mt_ms=2.0, mQ_r=mQ * 1.0007, mU_r=mU * 0.9993, r3=M3, xt=Xt)
        dyt2 = e[1]
    # ---------------- bottom / tau
    ytM = yt / sb * (1 + dyt)
    d_ne_b = K * (d_reg - (4 / 3) * a3 * (lg(M3) + F6(mQ / M3) + F6(mD / M3) - (A / M3) * F9(mQ / M3, mD / M3)) + d_g2 + d_g1 + d_chi)
    Db_qcd = K * (8 / 3) * a3 * M3 * mu * tanb * I3(mQ ** 2, mD ** 2, M3 ** 2)
    Db_hig = K * ytM ** 2 * mu * A * tanb * I3(mQ ** 2, mU ** 2, mu * mu)
    Db_win = -K * a2 * 1.5 * M2 * mu * tanb * I3(mQ ** 2, M2 ** 2, mu * mu)
    Delta_b = Db_qcd + Db_hig + Db_win
    msl = sp.msl if sp.msl > 0 else msf
    Delta_tau = sp.tau_scale * K * mu * tanb * (0.6 * a1 * M1 * I3(msl ** 2, msl ** 2 * 1.0001, M1 ** 2) - a2 * M2 * I3(msl ** 2, M2 ** 2, mu * mu))
    # ---------------- gauge (BGSS dg1-dg3), 3 generations, msf for gens 1,2 and sleptons
    sq = lambda q, u, d: (lg(q), lg(u), lg(d))
    lQ12, lU12, lD12 = sq(msf, msf, msf)
    lQ3, lU3, lD3 = sq(mQ, mU, mD)
    lL = lE = lg(msl)
    SQ, SU, SD = 2 * lQ12 + lQ3, 2 * lU12 + lU3, 2 * lD12 + lD3
    fg1 = 1 + 0.6 * K * a1 * (-1 / 3 * lg(amu) - 1 / 12 * lg(mA) - 1 / 12 * 3 * (lL + 2 * lE) - 1 / 36 * (SQ + 8 * SU + 2 * SD))
    fg2 = 1 + K * a2 * (1 / 3 - 2 / 3 * lg(M2) - 1 / 3 * lg(amu) - 1 / 12 * lg(mA) - 1 / 12 * (3 * SQ + 3 * lL))
    fg3 = 1 + K * a3 * (1 / 2 - lg(M3) - 1 / 12 * (2 * SQ + SU + SD))
    # ---------------- Higgs quartic (BGSS normalisation)
    c2b = (1 - tanb ** 2) / (1 + tanb ** 2)
    s2b = 2 * tanb / (1 + tanb ** 2)
    c4b, s4b = c2b * c2b - s2b * s2b, 2 * s2b * c2b
    c8b = c4b * c4b - s4b * s4b
    gp = 0.6 * a1 + a2
    lam_tree = gp / 4 * c2b ** 2
    l_reg = -(9 / 100 * a1 * a1 + 3 / 10 * a1 * a2 + (3 / 4 - c2b ** 2 / 6) * a2 * a2)
    sfl = 3 * (a1 * a1 + 25 * a2 * a2) * (2 * lg(msf) + lQ3) + 24 * a1 * a1 * (2 * lg(msf) + lU3) + 6 * a1 * a1 * (2 * lg(msf) + lD3) \
        + (9 * a1 * a1 + 25 * a2 * a2) * 3 * lL + 18 * a1 * a1 * 3 * lE
    l_phi = (3 * t2 * (t2 + 0.5 * (a2 - a1 / 5) * c2b) * lQ3 + 3 * t2 * (t2 + 0.4 * a1 * c2b) * lU3
             + c2b ** 2 / 300 * sfl
             + (261 * a1 * a1 + 630 * a1 * a2 + 1325 * a2 * a2 - 4 * c4b * (9 * a1 * a1 + 90 * a1 * a2 + 175 * a2 * a2)
                - 9 * c8b * (3 * a1 + 5 * a2) ** 2) / 4800 * lg(mA)
             - 3 / 16 * gp ** 2 * s4b ** 2
             + 6 * t2 * t2 * Xtt * (F1(xqu) - Xtt / 12 * F2(xqu))
             + 3 / 4 * t2 * Xtt * c2b * (0.6 * a1 * F3(xqu) + a2 * F4(xqu))
             - 1 / 4 * t2 * Xtt * c2b ** 2 * gp * F5(xqu))
    # BGSS 'mixing' piece in doc 70 was written for degenerate scalars; above is the general eq. (threshsusy)
    l_sb = 0.0
    hb = sm["yb"] / (1 + Delta_b)
    htau = sm["ytau"] / (1 + Delta_tau)
    mbb = math.sqrt(mQ * mD)
    Xbt = Xb / mbb
    Xtau = (A - mu * tanb) / msl
    l_sb = 6 * hb ** 4 * Xbt ** 2 * (1 - Xbt ** 2 / 12) + 2 * htau ** 4 * Xtau ** 2 * (1 - Xtau ** 2 / 12)
    lt = lam_tree
    betl = (2 * lt * (g1d ** 2 + g1u ** 2 + 3 * g2d ** 2 + 3 * g2u ** 2) - g1d ** 4 - g1u ** 4 - 5 * g2d ** 4 - 5 * g2u ** 4
            - 4 * g1d * g1u * g2d * g2u - 2 * (g1d ** 2 + g2u ** 2) * (g1u ** 2 + g2d ** 2))
    l_chi1 = (0.5 * betl * lmu - 7 / 12 * _f1(r1) * (g1d ** 4 + g1u ** 4) - 9 / 4 * _f2(r2) * (g2d ** 4 + g2u ** 4)
              - 3 / 2 * _f3(r1) * g1d ** 2 * g1u ** 2 - 7 / 2 * _f4(r2) * g2d ** 2 * g2u ** 2
              - 8 / 3 * _f5(r1, r2) * g1d * g1u * g2d * g2u
              - 7 / 6 * _f6(r1, r2) * (g1d ** 2 * g2d ** 2 + g1u ** 2 * g2u ** 2)
              - 1 / 6 * _f7(r1, r2) * (g1d ** 2 * g2u ** 2 + g1u ** 2 * g2d ** 2)
              - 4 / 3 * _f8(r1, r2) * (g1d * g2u + g1u * g2d) * (g1d * g2d + g1u * g2u)
              + 2 / 3 * F5s(r1) * g1d * g1u * (lt - 2 * (g1d ** 2 + g1u ** 2)) + 2 * F5s(r2) * g2d * g2u * (lt - 2 * (g2d ** 2 + g2u ** 2))
              + 1 / 3 * F7s(r1) * lt * (g1d ** 2 + g1u ** 2) + F7s(r2) * lt * (g2d ** 2 + g2u ** 2))
    l_chi2 = -1 / 6 * c2b ** 2 * (2 * a2 * a2 * lg(M2) + (9 / 25 * a1 * a1 + a2 * a2) * lmu)
    degenerate_stops = abs(mQ - 1) < 1e-9 and abs(mU - 1) < 1e-9 and abs(M3 - 1) < 1e-9
    if degenerate_stops or not sp.general_2l:
        l_2l = lam2l_atas_deg(g3, yt, Xt) if sp.fix_x5 else a3 * t2 * t2 / (96 * math.pi ** 4) * (-12 * Xt - 6 * Xt * Xt + 14 * Xt ** 3 + Xt ** 4 / 2 - Xt ** 5 / 4)
    else:
        l_2l = lam2l_atas_full(g3, yt, M3 * M_S, mQ * M_S, mU * M_S, Xt * M_S, M_S)
    l_at2 = lam2l_at2(yt, tanb, math.sqrt(mQ * mU) * M_S, amu * M_S, Xt * M_S, M_S) if sp.at2 else 0.0
    lam_bgss = lam_tree + K * (l_reg + l_phi + l_sb + l_chi1 + l_chi2) + l_2l + l_at2
    return {"dyt": dyt, "dyt2": dyt2, "d_qcd": K * d_qcd, "d_ne_b": d_ne_b, "Delta_b": Delta_b, "Delta_tau": Delta_tau,
            "Db_qcd": Db_qcd, "Db_hig": Db_hig, "Db_win": Db_win,
            "fg1": fg1, "fg2": fg2, "fg3": fg3, "lam": lam_bgss / 2, "lam_tree": lam_tree / 2, "lam_2l_atas": l_2l / 2,
            "lam_2l_at2": l_at2 / 2, "lam_1l_phi": K * l_phi / 2}


def run_up72(Mt, tanb, M_S, sp: Spec, alpha_s=0.1180, qcd3=True, t_end=math.log(1e20), sm3=False, mssm3=False):
    p = th.Phys(Mt=Mt, alpha_s=alpha_s)
    m = th.msbar_at_Mt(p)
    s0 = [m["gY"], m["g2"], m["g3"], m["yt"], m["yb"], m["ytau"], m["lambda"]]
    if sm3:
        import rge3
        low = rge3.run_sm3(s0, Mt, M_S, dense=True)
    else:
        low = th.run_sm(s0, Mt, M_S, 2, qcd3, dense=True)
    gY, g2, g3, yt, yb, ytau, _ = low.y[:, -1]
    sm = dict(gY=gY, g2=g2, g3=g3, yt=yt, yb=yb, ytau=ytau)
    thr = thresholds72(sm, tanb, sp, M_S)
    sb, cb = tanb / math.sqrt(1 + tanb ** 2), 1 / math.sqrt(1 + tanb ** 2)
    sM = [gY * math.sqrt(5 / 3) * thr["fg1"], g2 * thr["fg2"], g3 * thr["fg3"], yt / sb * (1 + thr["dyt"] + thr["dyt2"]),
          yb * (1 + thr["d_ne_b"]) / (cb * (1 + thr["Delta_b"])), ytau / (cb * (1 + thr["Delta_tau"])), 0.0]
    blow = lambda t, y, *a: 3.5 - float(np.max(np.abs(y)))
    blow.terminal = True
    if mssm3:
        import rge3
        rhs = rge3.mssm_rhs3
    else:
        rhs = st.mssm_rhs2
    hi = solve_ivp(rhs, (math.log(M_S), t_end), sM, args=(math.log(1e14),), method="DOP853",
                   rtol=1e-9, atol=1e-12, dense_output=True, events=blow)
    return low, hi, sm, thr


def solve72(M_S, sp: Spec = Spec(), n=1.0, dI=4.0, da_u=8.0, which="12", alpha_s=0.1180, qcd3=True, sm3=False, mssm3=False):
    I = tuple(x + dI for x in ss.TRACES["S0 SM fermions only (CCM traces)"])
    cache = {}

    def at(Mt, tanb):
        low, hi, sm, thr = run_up72(Mt, tanb, M_S, sp, alpha_s, qcd3, sm3=sm3, mssm3=mssm3)
        if not hi.success or thr["Delta_b"] <= -0.9:
            return None
        tB = ss.boundary_scale(hi, I, which)
        if tB is None:
            return None
        g1, g2, g3, yt, yb, ytau, _ = hi.sol(tB)
        Kb = (2 / 3) * I[1] * g2 * g2
        return yt - math.sqrt(Kb / (3 + n + da_u)), (3 + da_u) * yb * yb + ytau * ytau - Kb

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
    base = {"M_S": M_S, "spec": asdict(sp)}
    if tb != tb:
        return {"ok": False, **base}
    Mt = float(mt_of(tb))
    low, hi, sm, thr = run_up72(Mt, tb, M_S, sp, alpha_s, qcd3, sm3=sm3, mssm3=mssm3)
    tB = ss.boundary_scale(hi, I, which)
    g = hi.sol(tB)[:3]
    a = 4 * math.pi / np.array(g) ** 2 / np.array(I)
    mis = float(a[2] / a[1] - 1) if which == "12" else float(a[0] / a[1] - 1)
    gY, gw, gs, ytS, ybS, ytauS, _ = low.y[:, -1]
    if sm3:
        import rge3
        down = rge3.run_sm3([gY, gw, gs, ytS, ybS, ytauS, thr["lam"]], M_S, Mt)
    else:
        down = th.run_sm([gY, gw, gs, ytS, ybS, ytauS, thr["lam"]], M_S, Mt, 2, qcd3)
    Mh = th.Mh_from_lambda(down.y[6, -1], Mt)
    pt, ph = pulls(Mt, Mh)
    return {"ok": True, **base, "Mt": Mt, "Mh": float(Mh), "tanb": float(tb), "Lambda": float(math.exp(tB)),
            "unif_mismatch": mis, "pull_Mt": pt, "pull_Mh": ph, **{k: float(v) for k, v in thr.items()}}
