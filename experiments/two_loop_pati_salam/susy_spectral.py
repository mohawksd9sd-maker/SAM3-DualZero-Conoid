"""Doc 69, route 3: supersymmetric spectral boundary + MSSM running (exploratory).

Dual-Zero untouched.  Two finite contents:
  S0  'SM fermions only in H_F' (CCM traces I = 6,6,6) with MSSM running above M_S;
  S1  Beenakker-van den Broek-van Suijlekom (arXiv:1409.5984) content: gauginos and
      one higgsino copy in H_F -> I = (6.6, 9, 9), i.e. g3^2 = g2^2 = (11/9) gY^2
      [their eq. (25)]; S2 the two-higgsino-copy variant (their Remark 2) I = (7.2, 10, 9).
Each Higgs doublet gets its own kinetic normalisation:
  H_u: y_t^2 (3 + n) = (2/3) I_2 g_2^2 ,   H_d: 3 y_b^2 + y_tau^2 = (2/3) I_2 g_2^2,
so tan(beta) is *fixed* by m_b (given the SUSY threshold Delta_b), not chosen.
Running: SM two-loop below M_S; MSSM two-loop gauge (exact, group_theory), two-loop
y_t, one-loop y_b, y_tau (Martin-Vaughn / Barger-Berger-Ohmann) above.  Tree-level
matching y_t^SM = y_t sin(beta), y_b^SM = y_b cos(beta)(1+Delta_b), y_tau^SM = y_tau cos(beta).
M_h: lambda(M_S) = (g2^2 + gY^2)/8 cos^2 2beta + 3 y_t^4/(16 pi^2) X^2 (1 - X^2/12), SM two-loop down.
"""

from __future__ import annotations

import math
from fractions import Fraction as Fr
from typing import Dict, List, Optional

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, fsolve

import two_loop_higgs as th
from group_theory import Model, _Q2Field, sm_groups
from rge import PI2_16, Coeffs

M_PL_RED = 2.435e18


def mssm_model(n_higgsino_copies: int = 1) -> Model:
    G = sm_groups()
    S = lambda n, q, r2, r3, kind, m=1: _Q2Field(n, (q, r2, r3), kind, m)
    f = []
    for kind in ("weyl", "cscalar"):
        f += [S("Q" + kind, Fr(1, 60), "F", "F", kind, 3), S("u" + kind, Fr(4, 15), "1", "Fbar", kind, 3),
              S("d" + kind, Fr(1, 15), "1", "Fbar", kind, 3), S("L" + kind, Fr(3, 20), "F", "1", kind, 3),
              S("e" + kind, Fr(3, 5), "1", "1", kind, 3), S("Hu" + kind, Fr(3, 20), "F", "1", kind, n_higgsino_copies),
              S("Hd" + kind, Fr(3, 20), "F", "1", kind, n_higgsino_copies)]
    f += [S("wino", Fr(0), "adj", "1", "weyl"), S("gluino", Fr(0), "1", "adj", "weyl")]
    m = Model("MSSM", G, f)
    m.yukawas.append(("yt", {0: Fr(26, 5), 1: Fr(6), 2: Fr(4)}))
    m.top_one_loop = (Fr(6), (Fr(13, 15), Fr(3), Fr(16, 3)))  # type: ignore[attr-defined]
    return m


C_MSSM = Coeffs.from_model(mssm_model(), 2)
# The generic Machacek-Vaughn two-loop matrix misses the gaugino-sfermion-fermion "Yukawa" (sqrt2 g)
# contributions, so only the one-loop b is taken from the group data (it is exact: 33/5, 1, -3);
# the MSSM two-loop gauge matrix is the standard one (Martin-Vaughn PRD 50 (1994) 2282).
C_MSSM.B = np.array([[199 / 25, 27 / 5, 88 / 5], [9 / 5, 25.0, 24.0], [11 / 5, 9.0, 14.0]])
C_MSSM.c = np.array([26 / 5, 6.0, 4.0])
CB = np.array([14 / 5, 6, 4])
CTAU = np.array([18 / 5, 2, 0])

# spectral traces I = (I_1 GUT, I_2, I_3) of the finite Hilbert space
TRACES = {"S0 SM fermions only (CCM traces)": (6.0, 6.0, 6.0),
          "S1 BvdBvS: + gauginos + 1 higgsino copy": (6.6, 9.0, 9.0),
          "S2 BvdBvS Remark 2: + 2 higgsino copies": (7.2, 10.0, 9.0)}


def mssm_rhs(t, s, nu_on: float):
    g1, g2, g3, yt, yb, ytau, yn = s
    g = np.array([g1, g2, g3])
    gg = g * g
    t2, b2, l2 = yt * yt, yb * yb, ytau * ytau
    n2 = yn * yn if t > nu_on else 0.0
    two = (C_MSSM.B @ gg - C_MSSM.c * t2 - CB * b2 - CTAU * l2) / PI2_16
    dg = g ** 3 * (C_MSSM.b + two) / PI2_16
    a, b, c = gg
    dyt = yt * (6 * t2 + b2 + n2 - 16 / 3 * c - 3 * b - 13 / 15 * a)
    dyt2 = yt * (-22 * t2 * t2 - 5 * b2 * b2 - 5 * t2 * b2 - b2 * l2 + (6 / 5 * a + 6 * b + 16 * c) * t2 + 0.4 * a * b2
                 + 2743 / 450 * a * a + 7.5 * b * b - 16 / 9 * c * c + a * b + 136 / 45 * a * c + 8 * b * c)
    dyb = yb * (t2 + 6 * b2 + l2 - 16 / 3 * c - 3 * b - 7 / 15 * a)
    dyl = ytau * (3 * b2 + 4 * l2 + n2 - 3 * b - 9 / 5 * a)
    dyn = yn * (3 * t2 + 4 * n2 + l2 - 3 * b - 0.6 * a) if t > nu_on else 0.0
    return np.concatenate([dg, np.array([dyt + dyt2 / PI2_16, dyb, dyl, dyn]) / PI2_16])


def run_up(Mt: float, tanb: float, M_S: float, Delta_b: float = 0.0, n: float = 0.0, M_N: float = 1e14,
           alpha_s: float = 0.1180, t_end: float = math.log(1e20)):
    p = th.Phys(Mt=Mt, alpha_s=alpha_s)
    m = th.msbar_at_Mt(p)
    s0 = [m["gY"], m["g2"], m["g3"], m["yt"], m["yb"], m["ytau"], m["lambda"]]
    low = th.run_sm(s0, Mt, max(M_S, Mt), 2, False, dense=True)
    gY, g2, g3, yt, yb, ytau, _ = low.y[:, -1]
    sb, cb = tanb / math.sqrt(1 + tanb * tanb), 1 / math.sqrt(1 + tanb * tanb)
    sM = [gY * math.sqrt(5 / 3), g2, g3, yt / sb, yb / (cb * (1 + Delta_b)), ytau / cb, 0.0]
    blow = lambda t, y, *a: 3.5 - float(np.max(np.abs(y)))
    blow.terminal = True
    hi = solve_ivp(mssm_rhs, (math.log(max(M_S, Mt)), t_end), sM, args=(math.log(M_N),), method="DOP853",
                   rtol=1e-9, atol=1e-12, dense_output=True, events=blow)
    return low, hi


def susy_lambda(gY, g2, yt, tanb, X_hat=0.0):
    """lambda(M_S) in the convention V = lambda |H|^4, m_h^2 = 2 lambda v^2 (v = 246 GeV):
    tree (g^2 + g'^2)/8 cos^2 2beta + one-loop degenerate-stop threshold 3 y_t^4/(16 pi^2) X^2 (1 - X^2/12)."""
    c2b = (1 - tanb ** 2) / (1 + tanb ** 2)
    return (g2 * g2 + gY * gY) / 8 * c2b ** 2 + 3 * yt ** 4 / (16 * math.pi ** 2) * X_hat ** 2 * (1 - X_hat ** 2 / 12)


def boundary_scale(hi, I, which: str) -> Optional[float]:
    i, j = (0, 1) if which == "12" else (1, 2)
    def gap(t):
        g = hi.sol(t)[:3]
        return (4 * math.pi / g[i] ** 2) / I[i] - (4 * math.pi / g[j] ** 2) / I[j]
    ts = np.linspace(hi.t[0] + 1e-6, hi.t[-1] - 1e-6, 80)
    vs = [gap(t) for t in ts]
    for t0, t1, v0, v1 in zip(ts[:-1], ts[1:], vs[:-1], vs[1:]):
        if np.isfinite(v0) and np.isfinite(v1) and v0 * v1 <= 0:
            return brentq(gap, t0, t1, xtol=1e-12)
    return None


def solve(M_S: float, trace: str = "S0 SM fermions only (CCM traces)", which: str = "12", n: float = 0.0,
          Delta_b: float = 0.0, X_hat: float = 0.0, alpha_s: float = 0.1180,
          dI: float = 0.0, da_u: float = 0.0, da_d: Optional[float] = None) -> Dict[str, object]:
    """Solve (M_t, tan beta) from the two spectral Higgs normalisations; then M_h.
    dI: universal extra gauge trace (heavy Higgs-blind or H_u-coupled VL states at Lambda);
    da_u: extra H_u-coupled Yukawa trace (units y_t^2) -- the combination route (SUSY + extra content)."""
    I = tuple(x + dI for x in TRACES[trace])

    def at(Mt, tanb):
        low, hi = run_up(Mt, tanb, M_S, Delta_b, n, alpha_s=alpha_s)
        if not hi.success:
            return None
        tB = boundary_scale(hi, I, which)
        if tB is None:
            return None
        g1, g2, g3, yt, yb, ytau, _ = hi.sol(tB)
        K = (2 / 3) * I[1] * g2 * g2
        dd = da_u if da_d is None else da_d   # H_d-coupled share (units y_b^2) of the same extra block
        return yt - math.sqrt(K / (3 + n + da_u)), (3 + dd) * yb * yb + ytau * ytau - K

    def mt_of(tanb):
        f = lambda Mt: (lambda r: float("nan") if r is None else r[0])(at(Mt, tanb))
        x = _bracket_root(f, 150.0, 240.0, 19)
        return x

    def hd(tanb):
        Mt = mt_of(tanb)
        if Mt != Mt:
            return float("nan")
        r = at(Mt, tanb)
        return float("nan") if r is None else r[1]

    tb = _bracket_root(hd, 2.0, 90.0, 23, log=True)
    if tb != tb:
        return {"ok": False, "reason": "no (M_t, tan beta) solution with a perturbative boundary", "M_S": M_S, "trace": trace}
    best = (mt_of(tb), math.log(tb))
    Mt, tanb = float(best[0]), float(math.exp(best[1]))
    low, hi = run_up(Mt, tanb, M_S, Delta_b, n, alpha_s=alpha_s)
    tB = boundary_scale(hi, I, which)
    g1, g2, g3 = hi.sol(tB)[:3]
    a = 4 * math.pi / np.array([g1, g2, g3]) ** 2 / np.array(I)
    mis3 = float(a[2] / a[1] - 1) if which == "12" else float(a[0] / a[1] - 1)
    # Higgs mass: matching at M_S
    gY, gw, gs, ytS, ybS, ytauS, _ = low.y[:, -1]
    c2b = (1 - tanb ** 2) / (1 + tanb ** 2)
    lam = susy_lambda(gY, gw, ytS, tanb, X_hat)
    down = th.run_sm([gY, gw, gs, ytS, ybS, ytauS, lam], max(M_S, Mt), Mt, 2, False)
    Mh = th.Mh_from_lambda(down.y[6, -1], Mt)
    lam_max = susy_lambda(gY, gw, ytS, tanb, math.sqrt(6.0))
    down2 = th.run_sm([gY, gw, gs, ytS, ybS, ytauS, lam_max], max(M_S, Mt), Mt, 2, False)
    Mh_max = th.Mh_from_lambda(down2.y[6, -1], Mt)
    yt_B = float(hi.sol(tB)[3])
    return {"ok": True, "Mt": Mt, "tanb": tanb, "Mh": Mh, "Lambda": math.exp(tB), "yt_over_g": yt_B / float(g2),
            "g_B": float(g2), "unif_mismatch": mis3, "Lambda_below_MPl": math.exp(tB) < M_PL_RED, "M_S": M_S,
            "trace": trace, "X_hat": X_hat, "Delta_b": Delta_b, "Mh_maxmix": Mh_max, "n": n, "which": which}


def _bracket_root(f, lo, hi, n, log=False):
    xs = np.geomspace(lo, hi, n) if log else np.linspace(lo, hi, n)
    vs = [f(x) for x in xs]
    for x0, x1, v0, v1 in zip(xs[:-1], xs[1:], vs[:-1], vs[1:]):
        if np.isfinite(v0) and np.isfinite(v1) and v0 * v1 < 0:
            return brentq(f, x0, x1, xtol=1e-7 * x0)
    return float("nan")


def needed_yt_over_g(M_S: float, tanb: float, trace="S0 SM fermions only (CCM traces)", which="12") -> float:
    """Top-first inversion: y_t/g_2 at the spectral boundary needed for the measured M_t = 172.5."""
    low, hi = run_up(172.5, tanb, M_S)
    tB = boundary_scale(hi, TRACES[trace], which)
    if tB is None:
        return float("nan")
    s = hi.sol(tB)
    return float(s[3] / s[1])


def combo_fit(M_S: float, dI: float = 4.0, n: float = 1.0) -> Dict[str, object]:
    """SUSY + one VL 16-pair worth of trace (dI = 4) with an H_u-coupled share da_u fitted to M_t = 172.5."""
    f = lambda x: (lambda r: r["Mt"] - 172.5 if r.get("ok") else float("nan"))(solve(M_S, n=n, dI=dI, da_u=x))
    x = _bracket_root(f, 0.0, 16.0, 9)
    if x != x:
        return {"ok": False, "M_S": M_S, "dI": dI}
    r = solve(M_S, n=n, dI=dI, da_u=x)
    r.update({"da_u": x, "dI": dI, "params": 2})
    return r
