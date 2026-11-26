"""Doc 75: zero-dial Higgs routes for candidate #10 (originator of SAM-3 / Dual-Zero: Shawn Dykes).
Dual-Zero regulator untouched.  Reuses the doc 72/73 pipeline (experiments/open_routes_72) unchanged.

Route 1  Pati-Salam SU(2)_R x U(1)_{B-L} -> U(1)_Y non-decoupling D-term (tree-level, derived here by
         integrating out the heavy D-flat direction; same result as Batra-Delgado-Kaplan-Tait hep-ph/0309149).
Route 2  X_t from a spectral-action soft boundary at Lambda (structure: Beenakker-van den Broek-van Suijlekom
         arXiv:1409.5983 eqs. massterm2/trilinterm), run down with one-loop MSSM soft RGEs (Martin-Vaughn
         hep-ph/9311340; Martin hep-ph/9709356 primer, third-family Yukawas).
Route 3  vector-like pair with k = y_t: Martin arXiv:0910.2732 eq. (deltamhsimple) / (approxm2h).
"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "open_routes_72"))
import numpy as np
from scipy.integrate import solve_ivp
from common import *          # noqa: F401,F403  (pulls, set_matching, two_loop_higgs as _th)
import thr72 as T
HERE = os.path.dirname(os.path.abspath(__file__))   # re-set: 'from common import *' exports common.HERE
import two_loop_higgs as th

PI2_16 = 16 * math.pi ** 2
MZ = 91.1876


# ------------------------------------------------------------------ shared: M_h with an extra delta-lambda at M_S
def state(r):
    """Rebuild the doc-73 solution r (one entry of results_route1d.json): SM couplings at M_S, thresholds, MSSM run."""
    kw = r.get("kw", {})
    set_matching(kw.get("mode", "doc60"))
    sp = T.Spec(**r["spec"])
    low, hi, sm, thr = T.run_up72(r["Mt"], r["tanb"], r["M_S"], sp, kw.get("alpha_s", 0.1180), True, sm3=True, mssm3=True)
    return low, hi, sm, thr, sp


def mh_with(r, dlam=0.0, st=None):
    """M_h after adding dlam (our normalisation V = lam |H|^4) to the M_S matching; M_t and M_S unchanged
    (lambda does not enter the M_t / unification solve).  Returns (Mh, lam_MS_total)."""
    import rge3
    low, hi, sm, thr, sp = st or state(r)
    gY, gw, gs, yt, yb, ytau, _ = low.y[:, -1]
    lam = thr["lam"] + dlam
    down = rge3.run_sm3([gY, gw, gs, yt, yb, ytau, lam], r["M_S"], r["Mt"])
    return float(th.Mh_from_lambda(down.y[6, -1], r["Mt"])), lam


# ------------------------------------------------------------------ route 1: non-decoupling D-term
def dterm_factor(gA2, gB2, x):
    """U(1)_A x U(1)_B -> U(1), Higgs charged under A only, breaking fields with soft mass m and vev u.
    Integrating out the D-flat direction at tree level: g_eff^2 = g^2 (1 + (gA^2/gB^2) x/(1+x)),
    x = m^2 / (2 u^2 (gA^2 + gB^2)) ~ m^2 / M_V^2  (derivation in doc 75 sec. 2; = BDKT hep-ph/0309149)."""
    return 1.0 + (gA2 / gB2) * x / (1.0 + x)


def g_eff2_direct(gA2, gB2, mu_):
    """Same quantity from the explicit minimisation V(S) = mu_ S^2/2 + gA^2 (h+S)^2/2 + gB^2 S^2/2, mu_ = m^2/(2u^2)."""
    return gA2 * (gB2 + mu_) / (gA2 + gB2 + mu_)


PS_RATIO = 2.0 / 3.0   # gA^2/gB^2 = g_R^2 / ((3/2) g_4^2) at v_R with g_R = g_4 (spectral PS boundary, doc 69)


def route1_dlam(r, x, st=None, frozen=False):
    """delta lambda (ours) from Delta-1 applied to g'^2 c2b^2 / 8.  'tracking': g'(M_S) [the hard term follows the
    D-term]; 'frozen': g'(Lambda) value held fixed from v_R = Lambda down to M_S (one-loop running of the hard term
    not computed -> the two give a band)."""
    low, hi, sm, thr, sp = st or state(r)
    tb = r["tanb"]
    c2b = (1 - tb * tb) / (1 + tb * tb)
    if frozen:
        g1L = hi.sol(math.log(r["Lambda"]))[0]
        gp2 = 0.6 * g1L ** 2
    else:
        gp2 = sm["gY"] ** 2
    return gp2 * (dterm_factor(PS_RATIO, 1.0, x) - 1.0) * c2b ** 2 / 8.0


# ------------------------------------------------------------------ route 3: vector-like pair (Martin 0910.2732)
def f_martin(x):
    return math.log(x) - (5 - 1 / x) * (1 - 1 / x) / 6


def f_martin_series(eps):
    """f(1+eps) for tiny eps (avoids cancellation): exact series eps/3 - eps^4/12 + O(eps^5) (checked with sympy)."""
    return eps / 3 - eps ** 4 / 12


def martin_dmh2(k, tanb, MF, Msc2, Xk=0.0, Nc=3, v=246.22, eps=None):
    """Delta m_h^2 (GeV^2), k^4 sin^4 beta term of Martin eq. (deltamhsimple); x = Msc2/MF^2."""
    sb = tanb / math.sqrt(1 + tanb * tanb)
    x = Msc2 / MF ** 2
    if eps is None:
        eps = x - 1
    else:                       # pass eps = m_soft^2 / M_F^2 directly when it is below double precision
        x = 1 + eps
    f = f_martin_series(eps) if abs(eps) < 1e-4 else f_martin(x)
    mix = Xk ** 2 / (x * MF ** 2) * (1 - 1 / (3 * x)) - Xk ** 4 / (12 * x * x * MF ** 4)
    return Nc / (4 * math.pi ** 2) * k ** 4 * v * v * sb ** 4 * (f + mix)


def dlam_from_dmh2(dmh2, v=246.22):
    """tree-level conversion m_h^2 = 2 lam v^2 (our normalisation) -> delta lam at the matching scale."""
    return dmh2 / (2 * v * v)


# ------------------------------------------------------------------ route 2: one-loop MSSM soft RGEs
B1 = np.array([33 / 5, 1.0, -3.0])
IDX = dict(M1=0, M2=1, M3=2, At=3, Ab=4, Ata=5, Q3=6, U3=7, D3=8, L3=9, E3=10, Hu=11, Hd=12, Q1=13, U1=14, D1=15, L1=16, E1=17)


def soft_rhs(t, s, cpl):
    g1, g2, g3, yt, yb, yl = cpl(t)[:6]
    a1, a2, a3 = g1 * g1, g2 * g2, g3 * g3
    t2, b2, l2 = yt * yt, yb * yb, yl * yl
    M1, M2, M3, At, Ab, Al = s[:6]
    mQ3, mU3, mD3, mL3, mE3, mHu, mHd, mQ1, mU1, mD1, mL1, mE1 = s[6:]
    S = mHu - mHd + (mQ3 + 2 * mQ1) - (mL3 + 2 * mL1) - 2 * (mU3 + 2 * mU1) + (mD3 + 2 * mD1) + (mE3 + 2 * mE1)
    Xt = 2 * t2 * (mHu + mQ3 + mU3 + At * At)
    Xb = 2 * b2 * (mHd + mQ3 + mD3 + Ab * Ab)
    Xl = 2 * l2 * (mHd + mL3 + mE3 + Al * Al)
    G = lambda c3, c2, c1: c3 * a3 * M3 ** 2 + c2 * a2 * M2 ** 2 + c1 * a1 * M1 ** 2
    d = np.empty(18)
    d[0:3] = 2 * B1 * np.array([a1, a2, a3]) * np.array([M1, M2, M3])
    d[3] = 12 * t2 * At + 2 * b2 * Ab + 32 / 3 * a3 * M3 + 6 * a2 * M2 + 26 / 15 * a1 * M1
    d[4] = 12 * b2 * Ab + 2 * t2 * At + 2 * l2 * Al + 32 / 3 * a3 * M3 + 6 * a2 * M2 + 14 / 15 * a1 * M1
    d[5] = 8 * l2 * Al + 6 * b2 * Ab + 6 * a2 * M2 + 18 / 5 * a1 * M1
    sQ = -G(32 / 3, 6, 2 / 15)
    sU = -G(32 / 3, 0, 32 / 15)
    sD = -G(32 / 3, 0, 8 / 15)
    sL = -G(0, 6, 6 / 5)
    sE = -G(0, 0, 24 / 5)
    sH = -G(0, 6, 6 / 5)
    d[6] = Xt + Xb + sQ + a1 * S / 5
    d[7] = 2 * Xt + sU - 4 / 5 * a1 * S
    d[8] = 2 * Xb + sD + 2 / 5 * a1 * S
    d[9] = Xl + sL - 3 / 5 * a1 * S
    d[10] = 2 * Xl + sE + 6 / 5 * a1 * S
    d[11] = 3 * Xt + sH + 3 / 5 * a1 * S
    d[12] = 3 * Xb + Xl + sH - 3 / 5 * a1 * S
    d[13] = sQ + a1 * S / 5
    d[14] = sU - 4 / 5 * a1 * S
    d[15] = sD + 2 / 5 * a1 * S
    d[16] = sL - 3 / 5 * a1 * S
    d[17] = sE + 6 / 5 * a1 * S
    return d / PI2_16


# BvdBvS NC-MSSM normalisations (arXiv:1409.5984 Identification, M = 3 generations): r_2 = r_3 = 3/(6+4M), r_1 = 9/(3+10M)
R1, R2, R3 = 9 / 33, 3 / 18, 3 / 18
RN = dict(Q3=R2 * 2 + R3 * 3, U3=R1 + R3 * 3, D3=R1 + R3 * 3, L3=R2 * 2 + R1, E3=2 * R1, Hu=R1 + R2 * 2, Hd=R1 + R2 * 2)
for _k in ("Q", "U", "D", "L", "E"):
    RN[_k + "1"] = RN[_k + "3"]


def soft_run(hi, Lambda, M_S, m0=0.0, A0=0.0, M12=1.0, weights=False):
    """Boundary at Lambda (units of M12): gaugino masses M12, all A = A0, m^2 = m0^2 (+ 2 r N M12^2 if weights).
    Couplings from the doc-73 MSSM solution hi (3-loop MSSM RGEs, g1 GUT-normalised).  Returns low-scale dict."""
    s0 = np.zeros(18)
    s0[0:3] = M12
    s0[3:6] = A0
    for k, i in IDX.items():
        if i >= 6:
            s0[i] = m0 * m0 + (2 * RN[k] * M12 * M12 if weights else 0.0)
    sol = solve_ivp(soft_rhs, (math.log(Lambda), math.log(M_S)), s0, args=(hi.sol,), method="DOP853", rtol=1e-9, atol=1e-12)
    s = sol.y[:, -1]
    out = {k: float(s[i]) for k, i in IDX.items()}
    out["cpl_MS"] = [float(v) for v in hi.sol(math.log(M_S))[:6]]
    return out


def spec_from_soft(o, tanb, sgn=1.0):
    """Low-scale soft parameters -> doc-72 Spec in units of M_S = sqrt(mQ3 mU3); mu, m_A from tree EWSB."""
    if min(o["Q3"], o["U3"], o["D3"], o["L3"], o["E3"]) <= 0:
        return None, {"reason": "tachyonic sfermion"}
    MS = math.sqrt(math.sqrt(o["Q3"] * o["U3"]))
    t2 = tanb * tanb
    mu2 = (o["Hd"] - o["Hu"] * t2) / (t2 - 1)          # M_Z^2/2 neglected (M_S >> M_Z; units of M12)
    if mu2 <= 0:
        return None, {"reason": "no EWSB (mu^2 <= 0)", "mu2": mu2}
    mu = sgn * math.sqrt(mu2)
    mA2 = o["Hu"] + o["Hd"] + 2 * mu2
    if mA2 <= 0:
        return None, {"reason": "m_A^2 <= 0", "mA2": mA2}
    Xt = o["At"] - mu / tanb
    # Spec sign convention: M3 > 0 reference; gaugino masses all positive here
    msq12 = (o["Q1"] * o["U1"] * o["D1"]) ** (1 / 6)
    msl = (o["L3"] * o["E3"] * o["L1"] * o["E1"]) ** (1 / 8)
    sp = T.Spec(xt=Xt / MS, mQ=math.sqrt(o["Q3"]) / MS, mU=math.sqrt(o["U3"]) / MS, mD=math.sqrt(o["D3"]) / MS,
                msf=msq12 / MS, msl=msl / MS, M1=o["M1"] / MS, M2=o["M2"] / MS, M3=o["M3"] / MS, mu=mu / MS,
                mA=math.sqrt(mA2) / MS)
    return sp, {"MS_over_M12": MS, "mu_over_MS": mu / MS, "mA_over_MS": math.sqrt(mA2) / MS, "Xt_hat": Xt / MS,
                "At_over_MS": o["At"] / MS, "stau_L": math.sqrt(o["L3"]) / MS, "stau_R": math.sqrt(o["E3"]) / MS}
