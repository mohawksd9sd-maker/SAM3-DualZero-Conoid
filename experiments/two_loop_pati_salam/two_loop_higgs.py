"""Two-loop Higgs-sector calculation for the spectral Pati-Salam model (doc 60).

Below m_R: full two-loop SM RGEs for (g_Y, g_2, g_3, y_t, y_b, y_tau, lambda),
V = lambda |H|^4 (m_h^2 = 2 lambda v^2 at tree level), g_Y = g' (not GUT
normalised), with optional three-loop pure-QCD terms for g_3 and y_t.

Sources: Machacek-Vaughn NPB 222 (1983) 83, 236 (1984) 221, 249 (1985) 70;
Luo-Wang-Xiao PRD 67 (2003) 065019; Ford-Jack-Jones NPB 387 (1992) 373;
Buttazzo et al. JHEP 12 (2013) 089 (arXiv:1307.3536), appendix and eqs.
(57)-(60) for the NNLO MS-bar couplings at mu = M_t, which are used for the
matching (pole masses <-> MS-bar couplings).  Three-loop QCD: quark-mass
anomalous dimension gamma_2 (Tarasov 1982; Larin-Vermaseren 1993) and
beta_2 of QCD (Tarasov-Vladimirov-Zharkov 1980).

Above m_R: Pati-Salam two-loop gauge running (rge.py) with the Yukawa /
quartic system of missing_pieces.py (one loop) plus an estimated two-loop
PS Yukawa term used only for the error budget.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, replace
from typing import Dict, Optional

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

import missing_pieces as mp
from group_theory import pati_salam
from rge import PDG, PI2_16, Coeffs, Inputs, _solve, match_to_ps, solve_unification

ZETA3 = 1.2020569031595942
MPL_RED = 2.435e18

# ------------------------------------------------------------------ matching at M_t (Buttazzo et al. 2013)


@dataclass(frozen=True)
class Phys:
    Mt: float = 172.5
    Mh: float = 125.1
    alpha_s: float = 0.1180
    MW: float = 80.384  # Buttazzo reference point (keeps the fit at its centre)
    mb_mb: float = 4.18
    mtau: float = 1.77686


MT_REF = 173.34  # erratum 2026-11-26: Buttazzo et al. 1307.3536v4 fits are expanded around M_t = 173.34 (v2 used 173.10)


def msbar_at_Mt(p: Phys = Phys()) -> Dict[str, float]:
    """NNLO MS-bar couplings at mu = M_t (Buttazzo et al. v4 eqs. 57-60 fits)."""
    dt = p.Mt - MT_REF
    da = (p.alpha_s - 0.1184) / 0.0007
    dw = (p.MW - 80.384) / 0.014
    v = 246.22
    return {
        "lambda": 0.12604 + 0.00206 * (p.Mh - 125.15) - 0.00004 * dt,
        "yt": 0.93690 + 0.00556 * dt - 0.00042 * da,
        "g2": 0.64779 + 0.00004 * dt + 0.00011 * dw,
        "gY": 0.35830 + 0.00011 * dt - 0.00020 * dw,
        "g3": 1.1666 + 0.00314 * da - 0.00046 * dt,
        # small Yukawas: one-loop-level estimates at M_t (y_b from m_b(m_b) run
        # to M_t, y_tau tree level); they enter only at the 10^-4 level
        "yb": math.sqrt(2) * 2.75 / v,
        "ytau": math.sqrt(2) * p.mtau / v,
    }


MATCH_ERR = {"yt": 0.00050, "lambda": 0.00030}  # Buttazzo theory errors


def Mt_from_yt(yt: float, alpha_s: float = 0.1180) -> float:
    da = (alpha_s - 0.1184) / 0.0007
    return MT_REF + (yt - 0.93690 + 0.00042 * da) / 0.00556


def Mh_from_lambda(lam: float, Mt: float) -> float:
    """Higgs pole mass from lambda(M_t) (NNLO threshold, inverse of the fit)."""
    return 125.15 + (lam - 0.12604 + 0.00004 * (Mt - MT_REF)) / 0.00206


# ------------------------------------------------------------------ SM betas


def sm_beta(s, loops: int = 2, qcd3: bool = False) -> np.ndarray:
    gY, g2, g3, yt, yb, ytau, lam = s
    a, b, c = gY * gY, g2 * g2, g3 * g3
    t2, b2, l2 = yt * yt, yb * yb, ytau * ytau
    k1 = 1.0 / PI2_16
    k2 = k1 * k1
    # one loop
    dgY = gY * a * (41 / 6) * k1
    dg2 = g2 * b * (-19 / 6) * k1
    dg3 = g3 * c * (-7.0) * k1
    dyt = yt * (4.5 * t2 + 1.5 * b2 + l2 - 17 / 12 * a - 2.25 * b - 8 * c) * k1
    dyb = yb * (4.5 * b2 + 1.5 * t2 + l2 - 5 / 12 * a - 2.25 * b - 8 * c) * k1
    dyl = ytau * (2.5 * l2 + 3 * t2 + 3 * b2 - 15 / 4 * a - 2.25 * b) * k1
    Y2 = 3 * t2 + 3 * b2 + l2
    dl = (24 * lam * lam + 4 * lam * Y2 - 2 * (3 * t2 * t2 + 3 * b2 * b2 + l2 * l2)
          - 3 * lam * (3 * b + a) + 0.375 * (2 * b * b + (b + a) ** 2)) * k1
    if loops >= 2:
        dgY += gY * a * (199 / 18 * a + 4.5 * b + 44 / 3 * c - 17 / 6 * t2 - 5 / 6 * b2 - 2.5 * l2) * k2
        dg2 += g2 * b * (1.5 * a + 35 / 6 * b + 12 * c - 1.5 * t2 - 1.5 * b2 - 0.5 * l2) * k2
        dg3 += g3 * c * (11 / 6 * a + 4.5 * b - 26 * c - 2 * t2 - 2 * b2) * k2
        dyt += yt * (-12 * t2 * t2 + (131 / 16 * a + 225 / 16 * b + 36 * c - 12 * lam) * t2 + 6 * lam * lam
                     + 1187 / 216 * a * a - 0.75 * a * b + 19 / 9 * a * c - 23 / 4 * b * b + 9 * b * c - 108 * c * c) * k2
        dl += (-312 * lam ** 3 - 144 * lam * lam * t2 + 36 * lam * lam * (3 * b + a) - 3 * lam * t2 * t2
               + 80 * lam * c * t2 + 22.5 * lam * b * t2 + 85 / 6 * lam * a * t2
               - 73 / 8 * lam * b * b + 39 / 4 * lam * b * a + 629 / 24 * lam * a * a
               + 30 * t2 ** 3 - 32 * c * t2 * t2 - 8 / 3 * a * t2 * t2
               - 2.25 * b * b * t2 + 10.5 * b * a * t2 - 19 / 4 * a * a * t2
               + 305 / 16 * b ** 3 - 289 / 48 * b * b * a - 559 / 48 * b * a * a - 379 / 48 * a ** 3) * k2
    if qcd3:
        # pure-QCD three-loop pieces, n_f = 6
        nf = 6
        aS = c / (4 * math.pi ** 2)  # alpha_s / pi
        gam2 = (1249 + (-2216 / 27 - 160 / 3 * ZETA3) * nf - 140 / 81 * nf * nf) / 64
        dyt += -2 * yt * gam2 * aS ** 3
        b2q = 2857 / 2 - 5033 / 18 * nf + 325 / 54 * nf * nf  # beta(a_s=alpha_s/4pi) coefficient
        # d g3/dt = - g3 * b2q * (alpha_s/4pi)^3
        dg3 += -g3 * b2q * (c / (16 * math.pi ** 2)) ** 3
    return np.array([dgY, dg2, dg3, dyt, dyb, dyl, dl])


def run_sm(s0, mu0: float, mu1: float, loops=2, qcd3=False, dense=False):
    return solve_ivp(lambda t, s: sm_beta(s, loops, qcd3), (math.log(mu0), math.log(mu1)), s0,
                     method="DOP853", rtol=1e-10, atol=1e-13, dense_output=dense)


# ------------------------------------------------------------------ benchmark (Buttazzo et al.)


def benchmark(loops=2, qcd3=True) -> Dict[str, float]:
    """Run the Buttazzo M_t couplings (Mt=173.34, Mh=125.15, as=0.1184) up."""
    m = msbar_at_Mt(Phys(Mt=MT_REF, Mh=125.15, alpha_s=0.1184))
    s0 = [m["gY"], m["g2"], m["g3"], m["yt"], m["yb"], m["ytau"], m["lambda"]]
    sol = run_sm(s0, MT_REF, MPL_RED, loops, qcd3, dense=True)
    f = lambda lm: sol.sol(lm * math.log(10))[6]
    lm0 = brentq(f, 4.0, 18.0) if f(4.0) * f(18.0) < 0 else float("nan")
    end = sol.y[:, -1]
    lam_min = min(sol.sol(x)[6] for x in np.linspace(math.log(1e15), math.log(MPL_RED), 60))
    return {"lambda_MPl": end[6], "yt_MPl": end[3], "g3_MPl": end[2], "g2_MPl": end[1],
            "gY_MPl": end[0], "log10_mu_lambda_zero": lm0, "lambda_min_1e15_MPl": lam_min}


# ------------------------------------------------------------------ SM bottom-up wrapper for the gauge solve


class SMWrapper:
    """Bottom-up SM run from the NNLO M_t couplings; .at(mu) gives (g1_GUT, g2, g3, yt)."""

    def __init__(self, p: Phys = Phys(), qcd3: bool = False):
        self.p = p
        m = msbar_at_Mt(p)
        self.s0 = [m["gY"], m["g2"], m["g3"], m["yt"], m["yb"], m["ytau"], m["lambda"]]
        self.full = run_sm(self.s0, p.Mt, 1e18, 2, qcd3, dense=True)

        class _S:
            pass

        self.sol = _S()
        self.sol.sol = lambda t: self._gut(self.full.sol(t))

    @staticmethod
    def _gut(s):
        return np.array([s[0] * math.sqrt(5 / 3), s[1], s[2], s[3]])

    def at(self, mu):
        return self._gut(self.full.sol(math.log(mu)))

    def state(self, mu):
        return self.full.sol(math.log(mu))


# ------------------------------------------------------------------ the prediction


PS_TWO_LOOP_PROXY = {"on": False}


def _ps_rhs(t, s, gfun):
    """PS segment: (y_t, y_nu, lambda, kappa, lambda_s, y_N) one loop (+ proxy)."""
    d = mp._rhs_high(t, s, gfun, False)
    if PS_TWO_LOOP_PROXY["on"]:
        # gauge-only two-loop Yukawa term, QCD-like structure scaled to SU(4):
        # -2 y gamma_1 (alpha_4/pi)^2 with C_F(4)=15/8 in place of 4/3
        gR, gL, g4 = gfun(t)
        a4 = g4 * g4 / (4 * math.pi ** 2)
        scale = (15 / 8) / (4 / 3)
        d[0] += -2 * s[0] * 3.375 * scale ** 2 * a4 * a4
        d[1] += -2 * s[1] * 3.375 * scale ** 2 * a4 * a4
    return d


@dataclass
class Options:
    scenario: str = "composite"
    sigma: bool = True
    n: float = 1.0
    yN_over_g: float = 0.0
    msig_over_mR: float = 1.0
    qcd3: bool = False
    loops_sm: int = 2
    mu_B_over_Lambda: float = 1.0
    ps_proxy: bool = False
    yt_from_data: bool = False
    phys: Phys = Phys()
    log10_ratios: Optional[tuple] = None


def predict(o: Options = Options()) -> Dict[str, float]:
    p = o.phys
    smw = SMWrapper(p, o.qcd3)
    inp = replace(PDG, alpha_s=p.alpha_s, mt_pole=p.Mt)
    sol = solve_unification(inp, o.scenario, 2, log10_ratios=o.log10_ratios, sm=smw)
    m_R, Lam = sol["m_R_GeV"], sol["Lambda_GeV"]
    # PS gauge background
    C = Coeffs.from_model(pati_salam(o.scenario), 2)
    s0 = match_to_ps(smw.at(m_R), o.scenario, None if o.log10_ratios is None else list(o.log10_ratios), True)
    t_top = math.log(max(Lam, Lam * o.mu_B_over_Lambda)) + 0.01
    ps = _solve(C, math.log(m_R), t_top, s0, with_yukawa=True, dense=True)
    gfun = lambda t: ps.sol(t)[:3]
    mu_B = Lam * o.mu_B_over_Lambda
    gR, gL, g4 = gfun(math.log(mu_B))
    g = math.sqrt((gR ** 2 + gL ** 2 + g4 ** 2) / 3)
    # small Yukawas at the boundary from the data (inputs, not predictions)
    st_mB = smw.state(min(mu_B, 1e17))
    yb, ytau = st_mB[4], st_mB[5]
    # Tr Y^dagger Y = 4 g^2 including b, tau:  y_t^2 (3 + n) = 4 g^2 - 3 y_b^2 - y_tau^2
    yt_B = math.sqrt(max(4 * g * g - 3 * yb * yb - ytau * ytau, 0) / (3 + o.n))
    bc = mp.boundary(g, o.n, o.yN_over_g * g)
    bc[0], bc[1] = yt_B, math.sqrt(o.n) * yt_B
    if o.yt_from_data:
        bc[0] = smw.state(min(mu_B, 1e17))[3]  # ~ y_t from bottom-up data (approximate above m_R)
        bc[0] = sol["y_at_Lambda"]
        bc[1] = math.sqrt(o.n) * bc[0]
    if not o.sigma:
        bc[3] = 0.0
    PS_TWO_LOOP_PROXY["on"] = o.ps_proxy
    try:
        hi = solve_ivp(_ps_rhs, (math.log(mu_B), math.log(m_R)), bc, args=(gfun,), rtol=1e-10, atol=1e-13)
    finally:
        PS_TWO_LOOP_PROXY["on"] = False
    yt, yn, l, k, ls, yN = hi.y[:, -1]
    # sigma segment (SM gauge, one loop for the sigma couplings) if m_sigma < m_R
    m_sig = o.msig_over_mR * m_R
    st_R = smw.state(m_R)
    gY, g2, g3 = st_R[0], st_R[1], st_R[2]
    if o.sigma and m_sig < m_R:
        sm_g = lambda t: smw._gut(smw.full.sol(t))[:3]
        mid = solve_ivp(mp._rhs_high, (math.log(m_R), math.log(m_sig)), [yt, yn, l, k, ls, yN],
                        args=(sm_g, True), rtol=1e-10, atol=1e-13)
        yt, yn, l, k, ls, yN = mid.y[:, -1]
        st_s = smw.state(m_sig)
        gY, g2, g3 = st_s[0], st_s[1], st_s[2]
        mu_low = m_sig
    else:
        mu_low = m_R
    lam_SM = l - (k * k / ls if o.sigma else 0.0)
    st_low = smw.state(mu_low)
    s_start = [gY, g2, g3, yt, st_low[4], st_low[5], lam_SM]
    down = run_sm(s_start, mu_low, p.Mt, o.loops_sm, o.qcd3)
    gYt, g2t, g3t, yt_t, _, _, lam_t = down.y[:, -1]
    Mt_pred = Mt_from_yt(yt_t, p.alpha_s)
    Mh_pred = Mh_from_lambda(lam_t, Mt_pred)
    Mh_pred_obsMt = Mh_from_lambda(lam_t, p.Mt)
    return {"m_R": m_R, "Lambda": Lam, "g_U": sol["g_U"], "g_at_muB": g,
            "yt_at_Lambda_boundary": yt_B, "yt_at_Lambda_data": sol["y_at_Lambda"],
            "yt_Mt_pred": yt_t, "lambda_Mt_pred": lam_t, "g3_Mt_check": g3t,
            "Mt_pred": Mt_pred, "Mh_pred": Mh_pred, "Mh_pred_at_obs_Mt": Mh_pred_obsMt}


# ------------------------------------------------------------------ error budget


def error_budget(base: Options = Options()) -> Dict[str, object]:
    c = predict(base)
    shifts = {}

    def d(name, o):
        r = predict(o)
        shifts[name] = {"dMt": r["Mt_pred"] - c["Mt_pred"], "dMh": r["Mh_pred"] - c["Mh_pred"]}

    d("missing higher orders (add 3-loop QCD)", replace(base, qcd3=True))
    d("boundary scale x2", replace(base, mu_B_over_Lambda=2.0))
    d("boundary scale /2", replace(base, mu_B_over_Lambda=0.5))
    d("PS two-loop Yukawa proxy", replace(base, ps_proxy=True))
    if base.sigma:
        d("sigma threshold m_R/10", replace(base, msig_over_mR=0.1))
    d("alpha_s +0.0009", replace(base, phys=replace(base.phys, alpha_s=base.phys.alpha_s + 0.0009)))
    # matching errors (Buttazzo): y_t +-0.0005 -> M_t, lambda +-0.0003 -> M_h
    shifts["M_t matching (y_t +-0.0005)"] = {"dMt": 0.0005 / 0.00556, "dMh": 0.0}
    shifts["M_h matching (lambda +-0.0003)"] = {"dMt": 0.0, "dMh": 0.0003 / 0.00206}
    sym = {}
    for k in ("dMt", "dMh"):
        # scale variations: take the larger of up/down
        vals = {n: abs(v[k]) for n, v in shifts.items()}
        scale = max(vals.get("boundary scale x2", 0), vals.get("boundary scale /2", 0))
        others = [v for n, v in vals.items() if not n.startswith("boundary scale") and not n.startswith("alpha_s")]
        sym[k + "_theory"] = math.sqrt(scale ** 2 + sum(x * x for x in others))
        sym[k + "_parametric"] = vals["alpha_s +0.0009"]
    return {"central": c, "shifts": shifts, "errors": sym}


def threshold_spread(n: int = 12, seed: int = 60, base: Options = Options()) -> Dict[str, float]:
    rng = np.random.default_rng(seed)
    mt, mh = [], []
    for _ in range(n):
        u = tuple(rng.uniform(-1, 1, 6))
        r = predict(replace(base, log10_ratios=u))
        mt.append(r["Mt_pred"])
        mh.append(r["Mh_pred"])
    return {"Mt_std": float(np.std(mt)), "Mh_std": float(np.std(mh)),
            "Mt_range": [float(min(mt)), float(max(mt))], "Mh_range": [float(min(mh)), float(max(mh))]}


def fit_n_to_mh(base: Options) -> Dict[str, float]:
    f = lambda n: predict(replace(base, n=n))["Mh_pred"] - 125.1
    grid = np.linspace(1.0, 3.5, 11)
    vals = [f(x) for x in grid]
    for a, b, va, vb in zip(grid[:-1], grid[1:], vals[:-1], vals[1:]):
        if va * vb < 0:
            n = brentq(f, a, b, xtol=1e-5)
            r = predict(replace(base, n=n))
            return {"n": n, "Mt_pred": r["Mt_pred"], "Mh_pred": r["Mh_pred"]}
    return {"n": float("nan")}
