"""Doc 69, route 2: Pati-Salam -> SU(3)xSU(2)_LxSU(2)_RxU(1)_{B-L} (at M_C) -> SM (at m_R).

Dual-Zero untouched.  M_C (SU(4) breaking by the (1,1,15) vev) is an *input*: the
tree-level spectral potential gives every scalar mass term the same -f_2 Lambda^2
structure, so it cannot generate M_C << Lambda (or m_R << Lambda) by itself; see
`radiative_check` for the loop-level test (no spectral quartic turns negative).
Gauge running: exact two-loop coefficients (group_theory) in all three phases;
LR phase content: 3 generations, bidoublet phi, chi_R = color-singlet part of
Delta_R.  B-L normalised so g_BL = g_4 at M_C:  q = sqrt(3/8)(B-L).
Matching (tree, MSbar constants of the heavy vectors at M_C omitted, ~0.1 in alpha^-1):
  m_R: alpha_1^-1 = 3/5 alpha_R^-1 + 2/5 alpha_BL^-1, alpha_2 = alpha_L ;  M_C: g_3 = g_BL = g_4.
Yukawas: doc 60 PS one-loop system above M_C; LR one-loop (same index structure,
SU(4) Casimirs split into SU(3) + B-L) between m_R and M_C; two-loop SM below.
"""

from __future__ import annotations

import math
from fractions import Fraction as Fr
from typing import Dict, List

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

import content_engine as ce
import top_yukawa_search as tys
import two_loop_higgs as th
from group_theory import Field, Group, Model, _Q2Field, pati_salam, yukawa_c, yukawa_one_loop
from rge import PI2_16, Coeffs


def lr_model() -> Model:
    G = (Group("U1BL", "U1"), Group("SU2R", "SU", 2), Group("SU2L", "SU", 2), Group("SU3", "SU", 3))
    S = lambda n, q, r, l, c, kind, m=1: _Q2Field(n, (q, r, l, c), kind, m)
    fl = [S("QL", Fr(1, 24), "1", "F", "F", "weyl", 3), S("QRc", Fr(1, 24), "F", "1", "Fbar", "weyl", 3),
          S("LL", Fr(3, 8), "1", "F", "1", "weyl", 3), S("LRc", Fr(3, 8), "F", "1", "1", "weyl", 3),
          S("phi", Fr(0), "F", "F", "1", "cscalar"), S("chiR", Fr(3, 8), "F", "1", "1", "cscalar")]
    m = Model("LR", G, fl)
    QL1 = S("QL1", Fr(1, 24), "1", "F", "F", "weyl")
    QR1 = S("QR1", Fr(1, 24), "F", "1", "Fbar", "weyl")
    m.yukawas.append(("yt", dict(enumerate(yukawa_c(G, QL1, QR1, 12)))))
    m.top_one_loop = yukawa_one_loop(G, QL1, QR1, 2, 2, 3)  # type: ignore[attr-defined]
    return m


def _lr_coeffs() -> Coeffs:
    m = lr_model()
    b = np.array([float(x) for x in m.one_loop()])
    B = np.array([[float(x) for x in r] for r in m.two_loop()])
    c = np.array([float(m.yukawas[0][1][a]) for a in range(4)])
    k, G = m.top_one_loop
    return Coeffs(b, B, c, float(k), np.array([float(x) for x in G]))


C_LR = _lr_coeffs()
C_PS15 = Coeffs.from_model(pati_salam("with15"), 2)


def _rhs_n(t, s, C):
    g = s[:-1]
    y = s[-1]
    g2 = g * g
    dg = g ** 3 * (C.b + (C.B @ g2 - C.c * y * y) / PI2_16) / PI2_16
    dy = y * (C.k * y * y - C.G @ g2) / PI2_16
    return np.concatenate([dg, [dy]])


def _run(C, t0, t1, s0, dense=True):
    return solve_ivp(_rhs_n, (t0, t1), s0, args=(C,), method="DOP853", rtol=1e-10, atol=1e-13, dense_output=dense)


def unify(log10_MC_over_mR: float, alpha_s: float = 0.1180):
    """Solve m_R (and g_R(m_R)) for M_C = m_R * 10^r; Lambda from g_L = g_R, root g_4 = g_L."""
    sm = ce._sm_cached((), 172.5, alpha_s)
    r = log10_MC_over_mR

    def lr_from(lm):
        mR = 10 ** lm
        tR, tC = math.log(mR), math.log(mR) + r * math.log(10)
        g1, g2, g3, y = sm.at(mR)
        a1, a2 = 4 * math.pi / g1 ** 2, 4 * math.pi / g2 ** 2

        def bl_gap(aR):
            aBL = 2.5 * (a1 - 0.6 * aR)
            if aBL <= 0 or aR <= 0:
                return float("nan")
            s0 = [math.sqrt(4 * math.pi / aBL), math.sqrt(4 * math.pi / aR), g2, g3, y]
            sol = _run(C_LR, tR, tC, s0, dense=False)
            gBL, _, _, g3C, _ = sol.y[:, -1]
            return 4 * math.pi / gBL ** 2 - 4 * math.pi / g3C ** 2
        xs = np.linspace(5.0, a1 / 0.6 - 1.0, 40)
        vs = [bl_gap(x) for x in xs]
        for x0, x1, v0, v1 in zip(xs[:-1], xs[1:], vs[:-1], vs[1:]):
            if np.isfinite(v0) and np.isfinite(v1) and v0 * v1 < 0:
                aR = brentq(bl_gap, x0, x1, xtol=1e-12)
                aBL = 2.5 * (a1 - 0.6 * aR)
                s0 = [math.sqrt(4 * math.pi / aBL), math.sqrt(4 * math.pi / aR), g2, g3, y]
                return _run(C_LR, tR, tC, s0), tR, tC
        return None

    def at(lm):
        res = lr_from(lm)
        if res is None:
            return None
        lr, tR, tC = res
        gBL, gR, gL, g3, y = lr.y[:, -1]
        ps = ce.ps_run([gR, gL, g3, y], tC, math.log(1e21), (), base=pati_salam("with15"))
        def gap(t):
            g = ps(t)[:3]
            return 4 * math.pi / g[0] ** 2 - 4 * math.pi / g[1] ** 2
        ts = np.linspace(tC + 1e-6, ps.segs[-1][1] - 1e-6, 150)
        vs = [gap(t) for t in ts]
        for t0, t1, v0, v1 in zip(ts[:-1], ts[1:], vs[:-1], vs[1:]):
            if v0 * v1 <= 0:
                tL = brentq(gap, t0, t1, xtol=1e-12)
                g = ps(tL)[:3]
                return {"mis": 4 * math.pi / g[2] ** 2 - 4 * math.pi / g[1] ** 2, "tL": tL, "ps": ps, "lr": lr,
                        "tR": tR, "tC": tC, "sm": sm}
        return None

    f = lambda lm: (lambda q: float("nan") if q is None else q["mis"])(at(lm))

    def lr0(lm):
        res = lr_from(lm)
        if res is None:
            return float("nan")
        g = res[0].y[:, -1]
        return 4 * math.pi / g[1] ** 2 - 4 * math.pi / g[2] ** 2
    lg = np.linspace(3.5, 16.0, 26)
    lv = [lr0(x) for x in lg]
    grid = []
    for x0, x1, v0, v1 in zip(lg[:-1], lg[1:], lv[:-1], lv[1:]):
        if np.isfinite(v0) and np.isfinite(v1) and v0 * v1 <= 0:
            ls_ = brentq(lr0, x0, x1, xtol=1e-10)
            grid = list(np.linspace(max(ls_ - 4.0, 3.0), ls_ - 1e-7, 81))
            break
    if not grid:
        return None
    vals = [f(x) for x in grid]
    for x0, x1, v0, v1 in zip(grid[:-1], grid[1:], vals[:-1], vals[1:]):
        if np.isfinite(v0) and np.isfinite(v1) and v0 * v1 < 0:
            lm = brentq(f, x0, x1, xtol=1e-10)
            q = at(lm)
            if q["tL"] > q["tC"]:
                return q
    return None


def _lr_yuk_rhs(t, s, lr):
    yt, yn, l, k, ls, yN = s
    gBL, gR, gL, g3, _ = lr.sol(t)
    Gt = 8 * g3 * g3 + 2.25 * (gL * gL + gR * gR) + 0.25 * gBL * gBL
    Gn = 2.25 * (gL * gL + gR * gR) + 2.25 * gBL * gBL
    wf = 3 * (gL * gL + gR * gR)
    g4t = 0.375 * (2 * gL ** 4 + (gL * gL + gR * gR) ** 2)
    S2 = 3 * yt * yt + yn * yn
    dyt = yt * (1.5 * yt * yt + S2 - Gt)
    dyn = yn * (1.5 * yn * yn + S2 - Gn)
    dl = 24 * l * l + 2 * k * k + 4 * l * S2 - 2 * (3 * yt ** 4 + yn ** 4) - 3 * l * wf + g4t
    dk = k * (12 * l + 6 * ls + 8 * k + 2 * S2 + 2 * yN * yN - 1.5 * wf)
    dls = 18 * ls * ls + 8 * k * k + 4 * yN * yN * ls - 4 * yN ** 4
    return np.array([dyt, dyn, dl, dk, dls, 4 * yN ** 3]) / PI2_16


def predict(log10_MC_over_mR: float, alpha_s: float = 0.1180) -> Dict[str, object]:
    q = unify(log10_MC_over_mR, alpha_s)
    if q is None:
        return {"ok": False, "reason": "no unification solution", "r": log10_MC_over_mR}
    ps, lr, sm, tR, tC, tL = q["ps"], q["lr"], q["sm"], q["tR"], q["tC"], q["tL"]
    gR, gL, g4 = ps(tL)[:3]
    g = math.sqrt((gR ** 2 + gL ** 2 + g4 ** 2) / 3)
    st = sm.state(min(math.exp(tL), 1e17))
    yb, ytau = st[4], st[5]
    yt = math.sqrt(max(4 * g * g - 3 * yb * yb - ytau * ytau, 0.0) / 4.0)
    bc = [yt, yt, 4 * g * g * 4 / 16, 4 * g * g * 2 / 4, 8 * g * g, 0.0]
    shim = ce.PSShim(ps, tC)
    hi = solve_ivp(tys._rhs, (tL, tC), bc, args=(shim, tys.Cand(), None), rtol=1e-10, atol=1e-13, method="LSODA")
    mid = solve_ivp(_lr_yuk_rhs, (tC, tR), hi.y[:, -1], args=(lr,), rtol=1e-10, atol=1e-13, method="LSODA")
    yt_R, yn_R, l, k, ls, _ = mid.y[:, -1]
    lam_SM = l - k * k / ls
    s = sm.state(math.exp(tR))
    down = sm.run_down([s[0], s[1], s[2], yt_R, s[4], s[5], lam_SM], math.exp(tR), sm.p.Mt)
    Mt = th.Mt_from_yt(down[3], alpha_s)
    return {"ok": True, "Mt": Mt, "Mh": th.Mh_from_lambda(down[6], Mt), "m_R": math.exp(tR), "M_C": math.exp(tC),
            "Lambda": math.exp(tL), "g_B": g, "yt_over_g": yt / g, "r": log10_MC_over_mR,
            "Lambda_below_MPl": math.exp(tL) < ce.M_PL_RED}


def radiative_check() -> Dict[str, float]:
    """Do the spectral sigma-sector quartics (lambda, lambda_h_sigma, lambda_sigma) cross zero between
    m_R and Lambda?  If one did, Coleman-Weinberg breaking would fix a scale without input."""
    p, smw, sol, ps = tys.background()
    m_R, Lam = sol["m_R_GeV"], sol["Lambda_GeV"]
    g = math.sqrt(sum(x * x for x in ps.sol(math.log(Lam))[:3]) / 3)
    bc = [g, g, g * g, 2 * g * g, 8 * g * g, 0.0]
    hi = solve_ivp(tys._rhs, (math.log(Lam), math.log(m_R)), bc, args=(ps, tys.Cand(), None), dense_output=True,
                   rtol=1e-10, atol=1e-13)
    ts = np.linspace(math.log(m_R), math.log(Lam), 200)
    v = np.array([hi.sol(t) for t in ts])
    return {"min_lambda": float(v[:, 2].min()), "min_lambda_h_sigma": float(v[:, 3].min()),
            "min_lambda_sigma": float(v[:, 4].min())}
