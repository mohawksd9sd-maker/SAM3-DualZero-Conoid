"""Doc 67: is the spectral 'dial' y_t(Lambda) = g_U * (trace factor) avoidable, and do any DERIVED mechanisms
move M_t, M_h?  Every number reuses the doc 60 pipeline (top_yukawa_search.predict: two-loop SM + NNLO matching,
PS two-loop gauge / one-loop Yukawa-quartic running, spectral boundary at Lambda) with the doc 63 accounting.
The Dual-Zero regulator is never modified.
"""

from __future__ import annotations

import math
from dataclasses import replace
from typing import Dict, List

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

import top_yukawa_search as ts
import two_loop_higgs as th

MT_EXP, SMT_EXP = 172.5, 0.7
MH_EXP, SMH_EXP = 125.1, 0.2
SMT_TH, SMH_TH = ts.SIG_MT, ts.SIG_MH     # doc 60 pipeline errors (theory (+) measurement)


def _row(name, r, derived, params, note=""):
    Mt, Mh = float(r["Mt"]), float(r["Mh"])
    if Mh < 0:
        note = (note + "; " if note else "") + "lambda(M_t) < 0: vacuum unstable"
    pt = (Mt - MT_EXP) / math.hypot(SMT_TH, SMT_EXP)
    ph = (Mh - MH_EXP) / math.hypot(SMH_TH, SMH_EXP)
    return {"name": name, "Mt": Mt, "dMt": SMT_TH, "Mh": Mh, "dMh": SMH_TH, "pull_Mt": pt, "pull_Mh": ph,
            "pass": bool(abs(pt) < 2 and abs(ph) < 2), "derived": derived, "params": params, "note": note}


def baseline() -> Dict:
    return ts.predict(ts.Cand())


def required_yt_ratio() -> float:
    return ts.required_ratio()["r"] if isinstance(ts.required_ratio(), dict) and "r" in ts.required_ratio() else 0.8026


# ------------------------------------------------------------------ 1. sigma (CC 2012; twisted / grand symmetry)
def c1_sigma() -> List[Dict]:
    out = [_row("no sigma (CCM 2007 SM-like)", ts.predict(ts.Cand(sigma=False)), True, 0),
           _row("sigma at m_R (CC 2012), lambda_sigma, lambda_h_sigma spectral", ts.predict(ts.Cand()), True, 0)]
    for f in (0.1, 0.01):
        out.append(_row(f"sigma mass {f} m_R", ts.predict(ts.Cand(msig_over_mR=f)), False, 1, "m_sigma not fixed by the action"))
    for y in (1.0, 2.0):
        out.append(_row(f"Majorana Yukawa y_N = {y} g at Lambda", ts.predict(ts.Cand(yN_over_g=y)), False, 1))
    # what sigma would give if the top were right (r_yuk chosen, i.e. the dial turned by hand)
    r = ts.predict(ts.Cand(r_yuk=0.8026))
    out.append(_row("sigma + top fixed by hand (r = 0.8026)", r, False, 1, "shows sigma alone cannot reach 125 either"))
    return out


def sigma_sector_at_mR() -> Dict[str, float]:
    """Spectral boundary for (lambda, lambda_h_sigma, lambda_sigma) at Lambda, run to m_R (same equations as
    top_yukawa_search.predict); m_sigma ~ sqrt(2 lambda_sigma) v_R with v_R from the doc 60 seesaw."""
    from scipy.integrate import solve_ivp
    import math as _m
    c = ts.Cand()
    p, smw, sol, ps = ts.background()
    m_R, Lam = sol["m_R_GeV"], sol["Lambda_GeV"]
    tB = _m.log(Lam)
    gR, gL, g4 = ts._gauge(tB, ps, c, None)
    g = _m.sqrt((gR ** 2 + gL ** 2 + g4 ** 2) / 3)
    st = smw.state(Lam)
    yb, ytau = st[4], st[5]
    a0 = 3 + c.n + c.x
    G4 = 4 * g * g
    yt = _m.sqrt(max(G4 - 3 * yb * yb - ytau * ytau, 0.0) / a0)
    lam = G4 * (3 + c.n ** 2) / a0 ** 2
    kap = G4 * 2 * c.n / a0
    bc = [yt, _m.sqrt(c.n) * yt, lam, kap, 8 * g * g, 0.0]
    hi = solve_ivp(ts._rhs, (tB, _m.log(m_R)), bc, args=(ps, c, None), rtol=1e-10, atol=1e-13, method="LSODA")
    yt_R, yn_R, l, k, ls, yN = hi.y[:, -1]
    vR = 7.828e13
    return {"Lambda_boundary": {"lambda": lam, "lambda_h_sigma": kap, "lambda_sigma": 8 * g * g},
            "at_m_R": {"lambda": l, "lambda_h_sigma": k, "lambda_sigma": ls, "threshold_k2_over_ls": k * k / ls},
            "m_sigma_GeV": _m.sqrt(2 * ls) * vR, "m_R_GeV": m_R}


# ------------------------------------------------------------------ 2. PS without first order: (15,2,2) Higgs mixing
def mixed_bidoublet(theta: float, scenario: str = "with2215") -> Dict:
    """Light Higgs = cos(theta) H_(1,2,2) + sin(theta) H_(15,2,2).  Spectral kinetic terms are orthogonal
    (Tr Y1^dag Y15 = 3 - 3 = 0), each normalised to Tr Y^dag Y = 4 g^2:
        Y1  = g (1,1,1 | 1),   Y15 = (g/sqrt3) (1,1,1 | -3)    (quark colours | lepton)
    => y_t = g (cos + sin/sqrt3), y_nu = g (cos - sqrt3 sin), lambda = Tr Y^4/(4 g^2)  (x4 = 0, b = 3 + n^2)."""
    u = math.cos(theta) + math.sin(theta) / math.sqrt(3)
    v = math.cos(theta) - math.sqrt(3) * math.sin(theta)
    n = (v / u) ** 2
    x = 4 / u ** 2 - 3 - n
    c = ts.Cand(scenario=scenario, n=n, x=x, x4=0.0, extra_running=False)
    r = ts.predict(c)
    r.update({"theta": theta, "u": u, "v": v, "n": n})
    return r


def c2_no_first_order() -> Dict:
    rows = [_row("PS scalars (1,1,15) light, first order kept", ts.predict(ts.Cand(scenario="with15")), True, 0),
            _row("PS scalars (2,2,15) light, no mixing", ts.predict(ts.Cand(scenario="with2215")), True, 0)]
    f = lambda th_: mixed_bidoublet(th_)["Mt"] - MT_EXP
    thetas = np.linspace(-1.6, 1.6, 65)
    vals = [f(t) for t in thetas]
    sols = []
    for a, b, va, vb in zip(thetas[:-1], thetas[1:], vals[:-1], vals[1:]):
        if va * vb < 0:
            sols.append(brentq(f, a, b, xtol=1e-6))
    fits = []
    for s in sols:
        r = mixed_bidoublet(s)
        rows.append(_row(f"(1,2,2)-(15,2,2) mixing, theta = {s:.3f} fitted to M_t", r, False, 1,
                         f"y_nu/y_t = {r['v']/r['u']:.3f}"))
        fits.append({"theta": s, "Mt": r["Mt"], "Mh": r["Mh"], "ynu_over_yt": r["v"] / r["u"]})
    scan = [{"theta": float(t), "Mt": float(mixed_bidoublet(t)["Mt"]), "Mh": float(mixed_bidoublet(t)["Mh"])}
            for t in np.linspace(-0.9, 0.9, 19)]
    return {"rows": rows, "fits": fits, "scan": scan,
            "theta_range_Mt": [min(s["Mt"] for s in scan), max(s["Mt"] for s in scan)]}


# ------------------------------------------------------------------ 3. higher heat-kernel terms
def entropy_h(x):
    """Fermionic-entropy spectral function (Chamseddine-Connes-van Suijlekom 2019): h(x) = x/(1+e^x) + log(1+e^{-x})."""
    return x / (1 + math.exp(x)) + math.log1p(math.exp(-x))


def moments() -> Dict[str, Dict[str, float]]:
    """f0 = f(0), f_{-2} = -d f(u)/du at u = 0 for f as a function of u = D^2/Lambda^2."""
    hpp = (entropy_h(1e-3) - 2 * entropy_h(0.0) + entropy_h(-1e-3)) / 1e-6
    return {"flat cutoff (CC choice)": {"f0": 1.0, "f_m2": 0.0},
            "heat kernel e^{-u}": {"f0": 1.0, "f_m2": 1.0},
            "fermionic entropy h(sqrt u)": {"f0": math.log(2), "f_m2": -hpp / 2},
            "Dual-Zero weighting of a_n (eps(6)/eps(4) = -4^4/6^6 relative)": {"f0": 1.0, "f_m2": -(4 ** 4) / 6 ** 6}}


C6_ESTIMATE = -0.033    # rough Gilkey a_6/a_4 Higgs-vs-gauge kinetic difference (see doc 67, +-100%)


def c3_heat_kernel() -> Dict:
    r_req = 0.8026
    need = r_req ** 2 - 1.0
    out = {"needed_delta_yt2_over_g2": need, "moments": moments(), "c6_estimate": C6_ESTIMATE,
           "vev_over_Lambda_sq": (ts.V_EW / ts.predict(ts.Cand())["Lambda"]) ** 2, "rows": []}
    for name, m in out["moments"].items():
        eps = m["f_m2"] / m["f0"]
        delta = C6_ESTIMATE * eps            # at p = Lambda
        r = ts.predict(ts.Cand(r_yuk=math.sqrt(max(1 + delta, 1e-6)), r_quartic_power=2))
        out["rows"].append(_row(f"a6 correction, f = {name}", r, True, 0, f"delta(y_t^2/g^2) = {delta:+.4f}"))
        out["rows"][-1]["c6_needed"] = need / eps if eps else float("inf")
    return out


# ------------------------------------------------------------------ 4. traces over generations / product geometry
def c4_traces() -> List[Dict]:
    rows = [_row("PS forced y_nu = y_t (n = 1, baseline)", ts.predict(ts.Cand()), True, 0),
            _row("no Dirac neutrino Yukawa (n = 0; not PS)", ts.predict(ts.Cand(n=0.0)), False, 0, "violates PS Y_nu = Y_u"),
            _row("PS Y_nu = Y_u full 3x3 (n = 1 + share 7e-6)", ts.predict(ts.Cand(n=1.0 + 7e-6, x=4 * 7e-6)), True, 0)]
    for d in (2, 4, 16):
        c = ts.Cand(trace_scale=float(d), x=(d - 1) * 4.0, x4=(d - 1) * 4.0, sigma_trace_scale=1.0, extra_running=False)
        rows.append(_row(f"product geometry F x F_{d} (all traces x {d})", ts.predict(c), True, 0, "ratios invariant"))
    rows.append(_row("two independent 'dials' (separate f0 per layer)", ts.predict(ts.Cand(r_yuk=0.8026)), False, 1,
                     "not a spectral action: one f per action"))
    return rows


# ------------------------------------------------------------------ 5. gravity / asymptotic safety
def lambda_MPl_zero_Mh(Mt: float = MT_EXP) -> float:
    """M_h such that lambda(M_Pl,red) = 0 in the two-loop SM with measured M_t (Shaposhnikov-Wetterich-type)."""
    def lamPl(Mh):
        m = th.msbar_at_Mt(th.Phys(Mt=Mt, Mh=Mh))
        s0 = [m["gY"], m["g2"], m["g3"], m["yt"], m["yb"], m["ytau"], m["lambda"]]
        return th.run_sm(s0, Mt, th.MPL_RED, 2, True).y[6, -1]
    return brentq(lamPl, 110, 150)


def c5_gravity() -> Dict:
    Lam = ts.predict(ts.Cand())["Lambda"]
    Gt = Lam ** 2 / (8 * math.pi * th.MPL_RED ** 2)
    return {"Gtilde_at_Lambda": Gt, "max_shift_ln_yt": Gt * 10,
            "rows": [_row("gravity corrections at Lambda (G mu^2 ~ 1e-8)", ts.predict(ts.Cand()), True, 0),
                     {"name": "lambda(M_Pl) = 0 boundary (SW 2010), M_t input", "Mt": MT_EXP, "dMt": SMT_EXP,
                      "Mh": lambda_MPl_zero_Mh(), "dMh": 1.5, "derived": False, "params": 1,
                      "note": "replaces the spectral boundary; top is input", "pass": None}]}


# ------------------------------------------------------------------ 6. thresholds
def c6_thresholds() -> Dict:
    base = ts.predict(ts.Cand())
    up = ts.predict(ts.Cand(r_yuk=1.01))
    dMt_per_pct = up["Mt"] - base["Mt"]
    # leading-log mismatch if heavy states (W_R, X, Delta, sigma, N) spread by x3 around m_R:
    # difference of the y_t anomalous dimension PS vs SM at m_R
    _, smw, sol, ps = ts.background()
    mR = sol["m_R_GeV"]
    gY, g2, g3 = smw.state(mR)[:3]
    gR, gL, g4 = ps.sol(math.log(mR))[:3]
    G_sm = 17 / 12 * gY ** 2 + 2.25 * g2 ** 2 + 8 * g3 ** 2
    G_ps = 2.25 * gR ** 2 + 2.25 * gL ** 2 + 11.25 * g4 ** 2
    dln = abs(G_ps - G_sm) * math.log(3) / (16 * math.pi ** 2)
    finite = (g4 ** 2) / (16 * math.pi ** 2) * 4 / 3 * 2       # O(C_F g^2/16pi^2) finite parts, generous
    rows = []
    for f in (1 / 3, 3.0):
        rows.append(_row(f"Lambda thresholds: boundary at {f:.2f} Lambda", ts.predict(ts.Cand(mu_B_over_Lambda=f)), True, 0))
    tot = math.hypot(dln, finite) * 100
    return {"dMt_per_1pct_yt": dMt_per_pct, "dln_yt_mR_log": dln, "dln_yt_finite": finite,
            "dMt_mR_thresholds": tot * dMt_per_pct, "needed_pct": (1 - 0.8026) * 100, "rows": rows,
            "kk_landau_towers_doc61": "M_t 190.36 for M_c/Lambda = 0.3-1 (doc 61 cand 4)"}


# ------------------------------------------------------------------ 7. cutoff vs unification scale
def c7_cutoff() -> List[Dict]:
    rows = []
    for f in (0.01, 0.1, 5.0):
        rows.append(_row(f"spectral cutoff = {f} x gauge-meeting scale", ts.predict(ts.Cand(mu_B_over_Lambda=f)), False, 1,
                         "breaks g_L = g_R = g_4 at the cutoff"))
    return rows


# ------------------------------------------------------------------ outliers
def outliers() -> List[Dict]:
    base = ts.predict(ts.Cand())
    return [
        _row("twisted spectral triple / grand symmetry (sigma from twist)", base, True, 0, "same field content as cand. 1"),
        _row("quanta of geometry (two Cliffords -> M2(H)+M4(C), PS)", base, True, 0, "PS traces unchanged"),
        _row("zeta-regularised trace normalisation", base, True, 0, "a_4 = zeta-residue: same f0 ratio"),
        _row("Dual-Zero (-1)^n n^-n weighting of heat-kernel a_n", base, True, 0,
             "gauge and Higgs kinetic both in a_4 -> ratio unchanged; a_6 suppressed by 4^4/6^6"),
    ]


def report() -> Dict:
    c2 = c2_no_first_order()
    c3 = c3_heat_kernel()
    c5 = c5_gravity()
    c6 = c6_thresholds()
    out = {"baseline": _row("doc 60 baseline", baseline(), True, 0), "c1_sigma": c1_sigma(),
           "sigma_sector": sigma_sector_at_mR(), "c2_no_first_order": c2,
           "c3_heat_kernel": c3, "c4_traces": c4_traces(), "c5_gravity": c5, "c6_thresholds": c6,
           "c7_cutoff": c7_cutoff(), "outliers": outliers()}
    return out
