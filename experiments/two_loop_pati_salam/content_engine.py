"""General spectral-boundary engine for docs 68-69 (exploratory).

The Dual-Zero regulator is not touched: only the finite content H_F (and so the
gauge traces I_a, the Yukawa trace a, the running) and the breaking chain change.

Spectral boundary for an arbitrary almost-commutative content (Weyl counting,
J-images handled uniformly, CCM normalisation):
    gauge kinetic term of factor a  ∝  f_0 I_a ,  I_a = sum_{Weyl in H_F} S_a(R)
    =>  I_a g_a^2(Lambda) equal for all a                         (gauge boundary)
    Higgs kinetic term  ∝  f_0 Tr Y^dag Y = f_0 a y_t^2
    =>  y_t^2 a = (2/3) I_a g_a^2 ,  lambda = (2/3) I_a g_a^2 b / a^2.
Three SM generations give I_a = 6 for every factor and (2/3) 6 g^2 = 4 g^2,
the doc 58-60 boundary.  For fermions running in the RGEs, Delta b_a = (2/3) Delta I_a.
Check against the literature: the Beenakker-van den Broek-van Suijlekom MSSM
content (gauginos + one higgsino copy) has I = (6.6, 9, 9) (GUT-normalised U(1))
and gives g_3^2 = g_2^2 = (15/11) g_1,GUT^2 = (11/9) g_Y^2 ... see tests.

Gauge running: exact two-loop coefficients for SM / PS + extra fields from
group_theory (Machacek-Vaughn); extra-field thresholds are step functions at the
stated masses.  Yukawa/quartic running above m_R: the doc 60 one-loop PS system.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field, replace
from fractions import Fraction as Fr
from functools import lru_cache
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

import two_loop_higgs as th
import top_yukawa_search as tys
from group_theory import Field, Group, Model, _Q2Field, pati_salam, ps_groups, sm_groups, standard_model
from rge import PI2_16, Coeffs, match_to_ps

M_PL_RED = 2.435e18
MT_EXP, SMT_EXP, MH_EXP, SMH_EXP = 172.5, 0.7, 125.1, 0.2


# ------------------------------------------------------------------ content description


@dataclass(frozen=True)
class Extra:
    """One extra multiplet in H_F (or an extra scalar).

    group: "PS" (reps in (R, L, 4) order) or "SM" (reps (Y^2*3/5 GUT, L, c)).
    mass: GeV, or the strings "mR" / "Lambda" (trace only, no running).
    kind: "weyl" | "cscalar" | "rscalar".  in_HF: fermions in H_F enter I_a.
    da, da4: Higgs-coupled Yukawa trace (units y_t^2, y_t^4) at Lambda.
    """

    name: str
    group: str
    reps: Tuple
    kind: str = "weyl"
    mult: int = 1
    mass: object = "Lambda"
    in_HF: bool = True
    da: float = 0.0
    da4: float = 0.0

    def field(self) -> Field:
        if self.group == "SM":
            return _Q2Field(self.name, self.reps, self.kind, self.mult)
        return Field(self.name, self.reps, self.kind, self.mult)

    def index(self) -> np.ndarray:
        """Spectral gauge trace I_a (Weyl fermions in H_F only); SM order (1,2,3), PS (R,L,4)."""
        if self.kind != "weyl" or not self.in_HF:
            return np.zeros(3)
        G = sm_groups() if self.group == "SM" else ps_groups()
        f = self.field()
        return np.array([float(f.S(G, a)) * self.mult for a in range(3)])


def _coeffs(base: Model, extras: Sequence[Extra]) -> Coeffs:
    m = Model(base.name + "+x", base.groups, list(base.fields) + [e.field() for e in extras], base.yukawas)
    m.top_one_loop = base.top_one_loop  # type: ignore[attr-defined]
    return Coeffs.from_model(m, 2)


# ------------------------------------------------------------------ SM segment with extras


SM_BASE = standard_model()
C_SM0 = Coeffs.from_model(SM_BASE, 2)


class SMExt:
    """SM two-loop (th.sm_beta, Buttazzo inputs) + exact two-loop gauge shifts of extra SM-phase fields."""

    def __init__(self, extras: Sequence[Extra] = (), Mt: float = 172.5, alpha_s: float = 0.1180,
                 t_max: float = math.log(1e19), s0: Optional[Sequence[float]] = None, mu0: Optional[float] = None):
        self.extras = [e for e in extras if e.group == "SM" and isinstance(e.mass, (int, float))]
        ths = sorted({float(e.mass) for e in self.extras})
        self.segs = []
        p = th.Phys(Mt=Mt, alpha_s=alpha_s)
        if s0 is None:
            m = th.msbar_at_Mt(p)
            s0 = [m["gY"], m["g2"], m["g3"], m["yt"], m["yb"], m["ytau"], m["lambda"]]
            mu0 = Mt
        self.p = p
        edges = [math.log(mu0)] + [math.log(x) for x in ths if x > mu0] + [t_max]
        s = np.array(s0, float)
        for t0, t1 in zip(edges[:-1], edges[1:]):
            act = [e for e in self.extras if float(e.mass) <= math.exp(t0) * 1.0000001]
            dC = None
            if act:
                C = _coeffs(SM_BASE, act)
                dC = (C.b - C_SM0.b, C.B - C_SM0.B)
            sol = solve_ivp(self._rhs, (t0, t1), s, args=(dC,), method="DOP853", rtol=1e-10, atol=1e-13, dense_output=True)
            self.segs.append((t0, t1, sol))
            s = sol.y[:, -1]

    @staticmethod
    def _rhs(t, s, dC):
        d = th.sm_beta(s, 2, False)
        if dC is not None:
            db, dB = dC
            g = np.array([s[0] * math.sqrt(5 / 3), s[1], s[2]])
            dg = g ** 3 * (db + dB @ (g * g) / PI2_16) / PI2_16
            d[0] += dg[0] / math.sqrt(5 / 3)
            d[1] += dg[1]
            d[2] += dg[2]
        return d

    def state(self, mu: float) -> np.ndarray:
        t = math.log(mu)
        for t0, t1, sol in self.segs:
            if t <= t1 + 1e-12:
                return sol.sol(max(t, t0))
        return self.segs[-1][2].sol(t)

    def at(self, mu: float) -> np.ndarray:
        s = self.state(mu)
        return np.array([s[0] * math.sqrt(5 / 3), s[1], s[2], s[3]])

    def run_down(self, s_top: Sequence[float], mu_top: float, mu_low: float) -> np.ndarray:
        """Run a 7-vector down with the same extras (piecewise)."""
        ths = sorted({float(e.mass) for e in self.extras if mu_low < float(e.mass) < mu_top}, reverse=True)
        edges = [math.log(mu_top)] + [math.log(x) for x in ths] + [math.log(mu_low)]
        s = np.array(s_top, float)
        for t0, t1 in zip(edges[:-1], edges[1:]):
            act = [e for e in self.extras if float(e.mass) <= math.exp(t1) * 1.0000001]
            dC = None
            if act:
                C = _coeffs(SM_BASE, act)
                dC = (C.b - C_SM0.b, C.B - C_SM0.B)
            sol = solve_ivp(self._rhs, (t0, t1), s, args=(dC,), method="DOP853", rtol=1e-10, atol=1e-13)
            s = sol.y[:, -1]
        return s


# ------------------------------------------------------------------ PS segment with extras


PS_BASE = pati_salam("composite")


class Piecewise:
    def __init__(self):
        self.segs = []

    def __call__(self, t):
        for t0, t1, sol in self.segs:
            if t <= t1 + 1e-12:
                return sol.sol(max(t, t0))
        return self.segs[-1][2].sol(t)


class PSShim:
    """Duck-type of the doc 60 PS dense solution used by top_yukawa_search._rhs."""

    def __init__(self, pw: Piecewise, t0: float):
        self.pw = pw
        self.t = np.array([t0])

    def sol(self, t):
        return self.pw(t)


def ps_run(s0, tR: float, t_end: float, extras: Sequence[Extra], base: Model = PS_BASE) -> Piecewise:
    """PS two-loop gauge (+ the doc 60 one-loop y) with PS-phase extras switched on at their masses."""
    ps_x = [e for e in extras if e.group == "PS" and e.mass != "Lambda"]
    masses = sorted({math.log(float(e.mass)) for e in ps_x if e.mass != "mR" and math.log(float(e.mass)) > tR})
    edges = [tR] + [m for m in masses if m < t_end] + [t_end]
    pw = Piecewise()
    s = np.array(s0, float)
    for t0, t1 in zip(edges[:-1], edges[1:]):
        act = [e for e in ps_x if e.mass == "mR" or math.log(float(e.mass)) <= t0 + 1e-9]
        C = _coeffs(base, act)
        sol = solve_ivp(_ps_rhs, (t0, t1), s, args=(C,), method="DOP853", rtol=1e-10, atol=1e-13, dense_output=True)
        pw.segs.append((t0, t1, sol))
        s = sol.y[:, -1]
        if not sol.success or not np.all(np.isfinite(s)) or np.any(s[:3] > 6):
            break
    return pw


def _ps_rhs(t, s, C):
    g = s[:3]
    if np.any(~np.isfinite(g)) or np.any(g > 8):
        return np.zeros(4)
    y = s[3]
    g2 = g * g
    two = (C.B @ g2 - C.c * y * y) / PI2_16
    dg = g ** 3 * (C.b + two) / PI2_16
    dy = y * (C.k * y * y - C.G @ g2) / PI2_16
    return np.concatenate([dg, [dy]])


# ------------------------------------------------------------------ unification with the generalised gauge boundary


@dataclass
class Content:
    name: str
    extras: Tuple[Extra, ...] = ()
    n: float = 1.0                # sum y_nu^2 / y_t^2 (PS forces 1)
    sigma: bool = True
    params: int = 0               # continuous parameters fitted/chosen
    derived: bool = True
    note: str = ""

    def I(self) -> np.ndarray:
        """Spectral gauge traces, PS order (R, L, 4)."""
        I = np.array([6.0, 6.0, 6.0])
        for e in self.extras:
            if e.group == "PS":
                I += e.index()
        return I

    def da(self) -> Tuple[float, float]:
        return sum(e.da for e in self.extras), sum(e.da4 for e in self.extras)


def unify_ps(c: Content, Mt: float = 172.5, alpha_s: float = 0.1180):
    """Solve m_R, Lambda with I_R/alpha_R = ... generalised: alpha_a^-1 / I_a equal at Lambda."""
    sm = _sm_cached(tuple(e for e in c.extras if e.group == "SM"), Mt, alpha_s)
    I = c.I()
    t_cap = math.log(1e21)

    def at_mR(lm):
        tR = lm * math.log(10)
        s0 = match_to_ps(sm.at(10 ** lm), "composite", None, True)
        pw = ps_run(s0, tR, t_cap, c.extras)
        def gap_LR(t):
            g = pw(t)[:3]
            return (4 * math.pi / g[0] ** 2) / I[0] - (4 * math.pi / g[1] ** 2) / I[1]
        ts = np.linspace(tR + 1e-6, min(pw.segs[-1][1], t_cap), 200)
        vs = [gap_LR(t) for t in ts]
        for t0, t1, v0, v1 in zip(ts[:-1], ts[1:], vs[:-1], vs[1:]):
            if np.isfinite(v0) and np.isfinite(v1) and v0 * v1 <= 0:
                tL = brentq(gap_LR, t0, t1, xtol=1e-12)
                g = pw(tL)[:3]
                mis = (4 * math.pi / g[2] ** 2) / I[2] - (4 * math.pi / g[1] ** 2) / I[1]
                return tL, mis, pw
        return None

    def f(lm):
        r = at_mR(lm)
        return float("nan") if r is None else r[1]

    def lr0(lm):
        g = match_to_ps(sm.at(10 ** lm), "composite", None, True)[:3]
        return (4 * math.pi / g[0] ** 2) / I[0] - (4 * math.pi / g[1] ** 2) / I[1]
    lg = np.linspace(5.0, 18.5, 136)
    gv = [lr0(x) for x in lg]
    windows = []
    for x0, x1, v0, v1 in zip(lg[:-1], lg[1:], gv[:-1], gv[1:]):
        if v0 * v1 <= 0:
            windows.append(brentq(lr0, x0, x1, xtol=1e-13))
    grid = []
    for ls_ in windows:
        grid += list(np.linspace(max(ls_ - 6.0, 4.0), ls_ - 1e-7, 121)) + list(np.linspace(ls_ + 1e-7, min(ls_ + 6.0, 18.9), 121))
    if not windows:
        grid = list(np.linspace(5.0, 18.5, 136))
    vals = [f(x) for x in grid]
    root = None
    for x0, x1, v0, v1 in zip(grid[:-1], grid[1:], vals[:-1], vals[1:]):
        if np.isfinite(v0) and np.isfinite(v1) and v0 * v1 < 0:
            root = brentq(f, x0, x1, xtol=1e-11)
            break
    if root is None:
        return None
    tL, mis, pw = at_mR(root)
    return {"m_R": 10 ** root, "Lambda": math.exp(tL), "pw": pw, "sm": sm, "I": I}


@lru_cache(maxsize=64)
def _sm_cached(sm_extras: Tuple[Extra, ...], Mt: float, alpha_s: float) -> SMExt:
    return SMExt(sm_extras, Mt, alpha_s)


def predict_ps(c: Content, alpha_s: float = 0.1180, yN_over_g: float = 0.0) -> Dict[str, object]:
    """Spectral boundary at Lambda for content c; doc 60 top-down running; M_t, M_h."""
    u = unify_ps(c, alpha_s=alpha_s)
    if u is None:
        return {"ok": False, "reason": "no unification solution (alpha_a^-1/I_a never meet below 1e21 GeV)"}
    m_R, Lam, pw, sm, I = u["m_R"], u["Lambda"], u["pw"], u["sm"], u["I"]
    tB, tR = math.log(Lam), math.log(m_R)
    gR, gL, g4 = pw(tB)[:3]
    K = (2.0 / 3.0) * I[1] * gL * gL          # = (2/3) I_a g_a^2 for every a at Lambda
    st = sm.state(min(Lam, 1e17))
    yb, ytau = st[4], st[5]
    dx, dx4 = c.da()
    a0 = 3 + c.n + dx
    yt = math.sqrt(max(K - 3 * yb * yb - ytau * ytau, 0.0) / a0)
    b = 3 + c.n * c.n + dx4
    lam = K * b / a0 ** 2
    kap = K * 2 * c.n / a0 if c.sigma else 0.0
    g_eff = math.sqrt(K / 4.0)
    ls = 2 * K   # = 8 g^2 in the doc 60 normalisation
    # Yukawa-coupled extras run only if they are light (mass mR); otherwise trace only
    run_x = sum(e.da for e in c.extras if e.mass == "mR")
    run_x4 = sum(e.da4 for e in c.extras if e.mass == "mR")
    cand = tys.Cand(n=c.n, x=run_x, x4=run_x4, sigma=c.sigma)
    shim = PSShim(pw, tR)
    bc = [yt, math.sqrt(c.n) * yt, lam, kap, ls, yN_over_g * g_eff]
    hi = solve_ivp(tys._rhs, (tB, tR), bc, args=(shim, cand, None), rtol=1e-10, atol=1e-13, method="LSODA")
    if not hi.success or not np.all(np.isfinite(hi.y[:, -1])):
        return {"ok": False, "reason": "Yukawa/quartic run failed"}
    yt_R, yn_R, l, k, ls_R, _ = hi.y[:, -1]
    lam_SM = l - (k * k / ls_R if c.sigma else 0.0)
    s = sm.state(m_R)
    down = sm.run_down([s[0], s[1], s[2], yt_R, s[4], s[5], lam_SM], m_R, sm.p.Mt)
    Mt = th.Mt_from_yt(down[3], alpha_s)
    Mh = th.Mh_from_lambda(down[6], Mt)
    yt_data = _yt_data_at(sm, pw, tR, tB)
    return {"ok": True, "Mt": Mt, "Mh": Mh, "m_R": m_R, "Lambda": Lam, "yt_over_g": yt / gL,
            "yt_B": yt, "gL_B": gL, "g4_B": g4, "gR_B": gR, "I": list(I), "a": a0,
            "yt_over_g_needed": yt_data / gL, "Lambda_below_MPl": Lam < M_PL_RED}


def _yt_data_at(sm, pw, tR, tB):
    """y_t at Lambda from the measured top run up with the same PS one-loop y (as in doc 60)."""
    return float(pw(tB)[3])


# ------------------------------------------------------------------ result row


SIG_MT, SIG_MH = tys.SIG_MT, tys.SIG_MH


def row(c: Content, r: Dict[str, object], **kw) -> Dict[str, object]:
    out = {"name": c.name, "derived": c.derived, "params": c.params, "note": c.note, **kw}
    if not r.get("ok"):
        out.update({"ok": False, "reason": r.get("reason", "")})
        return out
    Mt, Mh = float(r["Mt"]), float(r["Mh"])
    pt, ph = (Mt - MT_EXP) / SIG_MT, (Mh - MH_EXP) / SIG_MH
    out.update({"ok": True, "Mt": Mt, "Mh": Mh, "pull_Mt": pt, "pull_Mh": ph,
                "pass": bool(abs(pt) < 2 and abs(ph) < 2),
                "yt_over_g": r.get("yt_over_g"), "yt_over_g_needed": r.get("yt_over_g_needed"),
                "Lambda": r.get("Lambda"), "m_R": r.get("m_R"),
                "unif_ok": bool(r.get("Lambda_below_MPl", True)) and r.get("m_R", 0) < r.get("Lambda", 1e30)})
    if Mh != Mh or Mh < 0:
        out["note"] = (out["note"] + "; " if out["note"] else "") + "lambda(M_t) < 0: vacuum unstable"
    return out


# ------------------------------------------------------------------ SM-algebra (CCM, A_F = C + H + M_3(C)) variant


def sm_index(extras: Sequence[Extra]) -> np.ndarray:
    I = np.array([6.0, 6.0, 6.0])
    for e in extras:
        if e.group == "SM":
            I += e.index()
    return I


def predict_sm(c: Content, M_N: float = 1e13, alpha_s: float = 0.1180, which: str = "23") -> Dict[str, object]:
    """CCM SM-algebra boundary at alpha_2^-1/I_2 = alpha_3^-1/I_3 ("23") or 1=2 ("12");
    y_t^2 a = (2/3) I_2 g_2^2; nu Dirac Yukawa sqrt(n) y_t above M_N; sigma at M_N."""
    sm_x = tuple(e for e in c.extras if e.group == "SM")
    sm = _sm_cached(sm_x, 172.5, alpha_s)
    I = sm_index(c.extras)
    ia, ib = (1, 2) if which == "23" else (0, 1)

    def gap(lm):
        s = sm.at(10 ** lm)
        return (4 * math.pi / s[ia] ** 2) / I[ia] - (4 * math.pi / s[ib] ** 2) / I[ib]
    lg = np.linspace(4.0, 19.0, 61)
    gv = [gap(x) for x in lg]
    lB = None
    for x0, x1, v0, v1 in zip(lg[:-1], lg[1:], gv[:-1], gv[1:]):
        if v0 * v1 <= 0:
            lB = brentq(gap, x0, x1, xtol=1e-12)
            break
    if lB is None:
        return {"ok": False, "reason": "no gauge boundary below 1e19 GeV"}
    muB = 10 ** lB
    st = sm.state(muB)
    gY, g2, g3, _, yb, ytau, _ = st
    s_ = sm.at(muB)
    K = (2.0 / 3.0) * I[1] * g2 * g2
    dx, dx4 = c.da()
    a0 = 3 + c.n + dx
    yt = math.sqrt(max(K - 3 * yb * yb - ytau * ytau, 0) / a0)
    lam = K * (3 + c.n * c.n + dx4) / a0 ** 2
    kap = K * 2 * c.n / a0 if c.sigma else 0.0
    M_N = min(M_N, muB)
    act = [e for e in sm_x if isinstance(e.mass, (int, float)) and float(e.mass) < muB]
    dC = None
    if act:
        C = _coeffs(SM_BASE, act)
        dC = (C.b - C_SM0.b, C.B - C_SM0.B)

    def rhs(t, s):
        d = tys._sm_high_rhs(t, s, math.log(M_N), c.sigma)
        if dC is not None:
            extra = SMExt._rhs(t, s[:7], dC) - th.sm_beta(s[:7], 2, False)
            d[:3] += extra[:3]
        return d
    s0 = [gY, g2, g3, yt, yb, ytau, lam, math.sqrt(c.n) * yt, kap, 2 * K, 0.0]
    hi = solve_ivp(rhs, (math.log(muB), math.log(M_N)), s0, rtol=1e-10, atol=1e-13, method="DOP853")
    s = hi.y[:, -1]
    lam_SM = s[6] - (s[8] ** 2 / s[9] if c.sigma else 0.0)
    down = sm.run_down(list(s[:6]) + [lam_SM], M_N, sm.p.Mt)
    Mt = th.Mt_from_yt(down[3], alpha_s)
    a = 4 * math.pi / s_[:3] ** 2
    spread = (a / I)
    return {"ok": True, "Mt": Mt, "Mh": th.Mh_from_lambda(down[6], Mt), "Lambda": muB, "yt_over_g": yt / g2,
            "yt_over_g_needed": st[3] / g2, "I": list(I),
            "g1_mismatch": float(spread[0] / spread[1] - 1), "Lambda_below_MPl": muB < M_PL_RED, "m_R": M_N}
