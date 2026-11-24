"""Search for structure that lowers the spectral top Yukawa (doc 61).

Exploratory.  The Dual-Zero regulator (generator eps(n) = omega_0 (-1)^n n^-n,
symmetric Reg_2) is not touched by anything here: every candidate changes
the finite geometry F, the spectrum between m_R and Lambda, or the gauge
group, never the regulator.

All candidates reuse the doc-60 pipeline: two-loop SM below m_R (NNLO
Buttazzo matching at M_t), PS two-loop gauge running with one-loop
Yukawa/quartic running above m_R, spectral boundary at Lambda.

Generalised spectral boundary (CC2012 traces, in units of y_t at Lambda):
    a = Tr Y^dag Y / y_t^2 = 3 + n + x + (3 y_b^2 + y_tau^2)/y_t^2
    b = Tr (Y^dag Y)^2 / y_t^4 = 3 + n^2/p + x4
    y_t^2 = 4 g^2 / a,  lambda = 4 g^2 b / a^2,
    lambda_h_sigma = 4 g^2 * 2 n / a,  lambda_sigma = 8 g^2
with n = sum_i y_nu_i^2 / y_t^2 spread equally over p generations, and
(x, x4) the extra trace of vector-like / extra-copy fermions that couple to
the Higgs (Dirac masses >= m_R, so they decouple with nu_R).  For p = 1,
x = x4 = 0 this is exactly the doc 58-60 boundary.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field, replace
from functools import lru_cache
from typing import Dict, List, Optional

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

import two_loop_higgs as th
from group_theory import pati_salam
from rge import PDG, PI2_16, Coeffs, _solve, match_to_ps, solve_unification

V_EW = 246.22
EV = 1e-9  # GeV


# ------------------------------------------------------------------ cached gauge background


@lru_cache(maxsize=16)
def background(scenario: str = "composite", alpha_s: float = 0.1180, Mt: float = 172.5):
    p = th.Phys(Mt=Mt, alpha_s=alpha_s)
    smw = th.SMWrapper(p)
    sol = solve_unification(replace(PDG, alpha_s=alpha_s, mt_pole=Mt), scenario, 2, sm=smw)
    m_R, Lam = sol["m_R_GeV"], sol["Lambda_GeV"]
    C = Coeffs.from_model(pati_salam(scenario), 2)
    s0 = match_to_ps(smw.at(m_R), scenario, None, True)
    ps = _solve(C, math.log(m_R), math.log(Lam) + 0.8, s0, with_yukawa=True, dense=True)
    return p, smw, sol, ps


# ------------------------------------------------------------------ candidate description


@dataclass
class Cand:
    scenario: str = "composite"
    sigma: bool = True
    n: float = 1.0            # sum_i y_nu_i^2 / y_t^2 at Lambda
    p: int = 1                # generations sharing n equally
    x: float = 0.0            # extra Higgs-coupled trace (units of y_t^2)
    x4: float = 0.0           # extra quartic trace (units of y_t^4)
    yN_over_g: float = 0.0
    msig_over_mR: float = 1.0
    r_yuk: float = 1.0        # multiplicative factor on y_t(Lambda) (candidate 5)
    r_quartic_power: int = 0  # lambda scaled by r^k, kappa by r^(k/2) (Higgs normalisation: k = 4)
    # candidate 4: Landau-level (flux) towers of the matter between M_c and Lambda
    kk_Mc_over_Lambda: Optional[float] = None
    kk_flux: int = 3
    kk_yukawa_factor: float = 2.0   # Weyl Yukawa couplings per Dirac level (L_k H R_k, both chiralities)
    mu_B_over_Lambda: float = 1.0


def _kk_levels(t: float, tc: Optional[float]) -> float:
    """Number of Landau levels below e^t: E_k = M_c sqrt(k) -> k_max = (mu/M_c)^2 (continuous)."""
    if tc is None or t <= tc:
        return 0.0
    return math.exp(2 * (t - tc))


def _gauge(t: float, ps, c: Cand, tc: Optional[float]):
    gR, gL, g4 = ps.sol(t)[:3]
    if tc is not None and t > tc:
        # each level = kk_flux Dirac 16's: universal Delta b = (8/3) * kk_flux per level
        db = 8.0 / 3.0 * c.kk_flux
        dB = db * 0.5 * (math.exp(2 * (t - tc)) - 1.0)  # int_tc^t levels dt'
        out = []
        for g in (gR, gL, g4):
            ainv = 4 * math.pi / g ** 2 - dB / (2 * math.pi)
            out.append(math.sqrt(4 * math.pi / ainv) if ainv > 0 else float("nan"))
        return tuple(out)
    return gR, gL, g4


def _rhs(t, s, ps, c: Cand, tc):
    yt, yn, l, k, ls, yN = s
    gR, gL, g4 = _gauge(t, ps, c, tc)
    G = 2.25 * gR * gR + 2.25 * gL * gL + 11.25 * g4 * g4
    wf = 3 * (gL * gL + gR * gR)
    g4t = 0.375 * (2 * gL ** 4 + (gL * gL + gR * gR) ** 2)
    nk = _kk_levels(t, tc)
    extra2 = c.x * yt * yt + c.kk_yukawa_factor * nk * (3 * yt * yt + c.p * yn * yn)
    extra4 = c.x4 * yt ** 4 + c.kk_yukawa_factor * nk * (3 * yt ** 4 + c.p * yn ** 4)
    S2 = 3 * yt * yt + c.p * yn * yn + extra2
    dyt = yt * (4.5 * yt * yt + 1.5 * c.p * yn * yn + extra2 - G)
    dyn = yn * (3 * yt * yt + (2 + c.p) * yn * yn + extra2 - G)
    dl = 24 * l * l + 2 * k * k + 4 * l * S2 - 2 * (3 * yt ** 4 + c.p * yn ** 4 + extra4) - 3 * l * wf + g4t
    dk = k * (12 * l + 6 * ls + 8 * k + 2 * S2 + 2 * yN * yN - 1.5 * wf)
    dls = 18 * ls * ls + 8 * k * k + 4 * yN * yN * ls - 4 * yN ** 4
    dyN = 4 * yN ** 3
    return np.array([dyt, dyn, dl, dk, dls, dyN]) / PI2_16


def predict(c: Cand = Cand(), alpha_s: float = 0.1180) -> Dict[str, float]:
    p, smw, sol, ps = background(c.scenario, alpha_s)
    m_R, Lam = sol["m_R_GeV"], sol["Lambda_GeV"]
    tB = math.log(Lam * c.mu_B_over_Lambda)
    tc = None if c.kk_Mc_over_Lambda is None else math.log(Lam * c.kk_Mc_over_Lambda)
    gR, gL, g4 = _gauge(tB, ps, c, tc)
    g = math.sqrt((gR ** 2 + gL ** 2 + g4 ** 2) / 3)
    st = smw.state(min(Lam * c.mu_B_over_Lambda, 1e17))
    yb, ytau = st[4], st[5]
    a0 = 3 + c.n + c.x
    yt2 = max(4 * g * g - 3 * yb * yb - ytau * ytau, 0.0) / a0
    yt = math.sqrt(yt2) * c.r_yuk
    b = 3 + c.n * c.n / c.p + c.x4
    rq = c.r_yuk ** c.r_quartic_power
    lam = 4 * g * g * b / a0 ** 2 * rq
    kap = (4 * g * g * 2 * c.n / a0 * math.sqrt(rq)) if c.sigma else 0.0
    bc = [yt, math.sqrt(c.n / c.p) * yt, lam, kap, 8 * g * g, c.yN_over_g * g]
    if not np.all(np.isfinite(bc)):
        return {"ok": False, "reason": "gauge Landau pole below Lambda"}
    hi = solve_ivp(_rhs, (tB, math.log(m_R)), bc, args=(ps, c, tc), rtol=1e-10, atol=1e-13, method="LSODA")
    if not hi.success or not np.all(np.isfinite(hi.y[:, -1])):
        return {"ok": False}
    yt_R, yn_R, l, k, ls, yN = hi.y[:, -1]
    st_R = smw.state(m_R)
    mu_low = m_R
    s = [yt_R, yn_R, l, k, ls, yN]
    if c.sigma and c.msig_over_mR < 1.0:
        import missing_pieces as mp
        sm_g = lambda t: smw._gut(smw.full.sol(t))[:3]
        mu_low = c.msig_over_mR * m_R
        mid = solve_ivp(mp._rhs_high, (math.log(m_R), math.log(mu_low)), s, args=(sm_g, True), rtol=1e-10, atol=1e-13)
        s = list(mid.y[:, -1])
    yt_l, _, l, k, ls, _ = s
    lam_SM = l - (k * k / ls if c.sigma else 0.0)
    st_low = smw.state(mu_low)
    down = th.run_sm([st_low[0], st_low[1], st_low[2], yt_l, st_low[4], st_low[5], lam_SM], mu_low, p.Mt, 2, False)
    yt_t, lam_t = down.y[3, -1], down.y[6, -1]
    Mt = th.Mt_from_yt(yt_t, alpha_s)
    return {"ok": True, "Mt": Mt, "Mh": th.Mh_from_lambda(lam_t, Mt), "g_B": g, "yt_B": yt,
            "yt_B_data": sol["y_at_Lambda"], "lambda_B": lam, "yn_mR": yn_R, "yt_mR": yt_R,
            "m_R": m_R, "Lambda": Lam, "g_max": max(gR, gL, g4)}


# ------------------------------------------------------------------ helpers


def solve_for(fun, target: float, lo: float, hi: float, n: int = 25, log: bool = False):
    xs = np.geomspace(lo, hi, n) if log else np.linspace(lo, hi, n)
    vals = []
    for x in xs:
        r = fun(x)
        vals.append(r - target if np.isfinite(r) else float("nan"))
    for x0, x1, v0, v1 in zip(xs[:-1], xs[1:], vals[:-1], vals[1:]):
        if np.isfinite(v0) and np.isfinite(v1) and v0 * v1 < 0:
            return brentq(lambda x: fun(x) - target, x0, x1, xtol=1e-7 * max(1.0, abs(x0)))
    return float("nan")


def _mt(c):
    r = predict(c)
    return r["Mt"] if r.get("ok") else float("nan")


SIG_MT = math.hypot(1.18, 0.3)   # doc 60 total error (+) measurement
SIG_MH = math.hypot(1.76, 0.11)


def pulls(r):
    return {"Mt_pull": (r["Mt"] - 172.5) / SIG_MT, "Mh_pull": (r["Mh"] - 125.1) / SIG_MH}


# ------------------------------------------------------------------ (1) large Dirac neutrino Yukawas


def seesaw(yn_mR: float, m_R: float, g_R: float, m_nu_max_eV: float = 0.05) -> Dict[str, float]:
    """Type-I: m_nu = m_D^2 / M_N, m_D = y_nu v / sqrt2.  M_N = y_N v_R, v_R ~ m_R / g_R."""
    mD = yn_mR * V_EW / math.sqrt(2)
    MN_needed = mD * mD / (m_nu_max_eV * EV)
    vR = m_R / g_R
    return {"m_D_GeV": mD, "M_N_needed_GeV": MN_needed, "v_R_GeV": vR,
            "y_N_needed": MN_needed / vR, "m_nu_eV_if_MN_eq_mR": mD * mD / m_R / EV}


def yN_max_perturbative(m_R: float, Lam: float) -> float:
    """Largest y_N(m_R) with y_N(Lambda) <= sqrt(4 pi) under 16 pi^2 dy_N/dt = 4 y_N^3."""
    L = math.log(Lam / m_R)
    return 1.0 / math.sqrt(1.0 / (4 * math.pi) + 8 * L / PI2_16)


def seesaw_check(r: Dict[str, float], p_gen: int = 1) -> Dict[str, float]:
    _, _, sol, ps = background("composite")
    gR = ps.sol(math.log(sol["m_R_GeV"]))[0]
    vR = r["m_R"] / gR
    yNmax = yN_max_perturbative(r["m_R"], r["Lambda"])
    mD = r["yn_mR"] * V_EW / math.sqrt(2)
    m_min = mD * mD / (yNmax * vR) / EV
    # sum of masses: degenerate p_gen copies, or heaviest + oscillation minimum (normal ordering)
    sum_min = p_gen * m_min if p_gen > 1 else m_min + 2 * math.sqrt(max(m_min ** 2 - 0.0025, 0.0)) if m_min > 0.05 else m_min + 0.0087
    return {"m_D_GeV": mD, "v_R_GeV": vR, "yN_max_mR": yNmax, "M_N_max_GeV": yNmax * vR,
            "m_nu_min_eV": m_min, "sum_m_nu_min_eV": sum_min, "cosmology_bound_eV": 0.12}


def cand1() -> Dict[str, object]:
    out = {}
    _, _, sol, ps = background("composite")
    gR_mR = ps.sol(math.log(sol["m_R_GeV"]))[0]
    for p in (1, 3):
        for yNg in (0.0, 2.0):
            key = f"p={p}, yN={yNg}g"
            n = solve_for(lambda n: _mt(Cand(n=n, p=p, yN_over_g=yNg)), 172.5, 1.0, 6.0)
            r = predict(Cand(n=n, p=p, yN_over_g=yNg))
            out[key] = {"n": n, "y_nu_over_y_t_each": math.sqrt(n / p), **{k: r[k] for k in ("Mt", "Mh", "yt_B", "yn_mR")},
                        **pulls(r), "seesaw": seesaw(r["yn_mR"], r["m_R"], gR_mR, 0.05 if p == 1 else 0.04)}
    for p in (1, 3):
        n = solve_for(lambda n: _mt(Cand(n=n, p=p, sigma=False)), 172.5, 1.0, 6.0)
        r = predict(Cand(n=n, p=p, sigma=False))
        out[f"p={p}, no sigma"] = {"n": n, "Mt": r["Mt"], "Mh": r["Mh"], **pulls(r)}
    return out


# ------------------------------------------------------------------ (2) extra copies / vector-like fermions


def cand2() -> Dict[str, object]:
    out = {}
    # discrete copies of the third-generation Yukawa block with the same y (zero continuous parameters)
    for label, x, x4 in (("+1 VL quark doublet+singlet (x=3)", 3.0, 3.0),
                         ("+1 VL lepton doublet+singlet (x=1)", 1.0, 1.0),
                         ("+1 full PS 16 copy (x=4)", 4.0, 4.0),
                         ("+2 VL lepton (x=2)", 2.0, 2.0)):
        r = predict(Cand(x=x, x4=x4))
        out[label] = {"x": x, "Mt": r["Mt"], "Mh": r["Mh"], "yt_B": r["yt_B"], **pulls(r)}
    # continuous: extra states with Yukawa c*y_t, multiplicity N (x = N c^2, x4 = N c^4)
    xs = solve_for(lambda x: _mt(Cand(x=x, x4=x)), 172.5, 0.0, 6.0)
    r = predict(Cand(x=xs, x4=xs))
    out["fit x (c=1) to M_t"] = {"x": xs, "Mt": r["Mt"], "Mh": r["Mh"]}
    # two-parameter fit: x and x4 to both M_t and M_h (c != 1)
    def mh_at(x4):
        x = solve_for(lambda x: _mt(Cand(x=x, x4=x4)), 172.5, 0.0, 8.0, 17)
        return predict(Cand(x=x, x4=x4))["Mh"] if np.isfinite(x) else float("nan")
    grid = {}
    for x4 in (0.0, 0.5, 1.0, 2.0, 3.0):
        x = solve_for(lambda x: _mt(Cand(x=x, x4=x4)), 172.5, 0.0, 8.0, 17)
        grid[str(x4)] = {"x": x, "Mh": predict(Cand(x=x, x4=x4))["Mh"] if np.isfinite(x) else float("nan")}
    out["M_t fixed, vary x4"] = grid
    return out


# ------------------------------------------------------------------ (3) Lambda / breaking chain


def data_ratio_curve() -> List[Dict[str, float]]:
    """y_t(mu)/[2 g(mu)/sqrt(3+n)] from bottom-up SM data, n = 1, g = g_2 and g = rms GUT."""
    _, smw, _, _ = background("composite")
    rows = []
    for lm in np.arange(8.0, 18.01, 1.0):
        gY, g2, g3, yt = smw.state(10 ** lm)[:4]
        g1 = gY * math.sqrt(5 / 3)
        grms = math.sqrt((g1 * g1 + g2 * g2 + g3 * g3) / 3)
        rows.append({"log10_mu": float(lm), "yt": yt, "g2": g2, "g3": g3, "ratio_vs_g2": yt / g2,
                     "ratio_vs_grms": yt / grms})
    return rows


def cand3() -> Dict[str, object]:
    out = {"scenarios": {}, "mu_B_scan": {}}
    for sc in ("composite", "with15", "with2215"):
        try:
            r = predict(Cand(scenario=sc))
        except Exception as e:  # pragma: no cover
            out["scenarios"][sc] = {"error": str(e)}
            continue
        if r.get("ok"):
            out["scenarios"][sc] = {"Lambda": r["Lambda"], "m_R": r["m_R"], "g_B": r["g_B"], "Mt": r["Mt"], "Mh": r["Mh"]}
    for f in (0.01, 0.1, 1.0, 3.0, 5.0):
        r = predict(Cand(mu_B_over_Lambda=f))
        if r.get("ok"):
            out["mu_B_scan"][str(f)] = {"Mt": r["Mt"], "Mh": r["Mh"], "g_B": r["g_B"]}
    out["data_ratio_curve"] = data_ratio_curve()
    # SM-group boundary forced at a lower scale (no unification there: g1, g2, g3 unequal)
    lstar = brentq(lambda lm: _sm_mt_at(lm) - 172.5, 6.0, 12.0)
    out["SM_boundary_scale_for_Mt"] = {"log10_mu": lstar, **sm_group(1.0, 1e30, False, log10_muB=lstar)}
    return out


def _sm_mt_at(lm: float) -> float:
    return sm_group(1.0, 1e30, False, log10_muB=lm)["Mt"]


# ------------------------------------------------------------------ (4) flux / Landau-level towers


def cand4() -> Dict[str, object]:
    out = {"scan": {}}
    for f in (1.0, 0.8, 0.6, 0.5, 0.4, 0.3):
        r = predict(Cand(kk_Mc_over_Lambda=f))
        if r.get("ok"):
            out["scan"][str(f)] = {"Mt": r["Mt"], "Mh": r["Mh"], "g_B": r["g_B"], "levels_at_Lambda": (1 / f) ** 2}
        else:
            out["scan"][str(f)] = {"ok": False}
    fc = solve_for(lambda f: _mt(Cand(kk_Mc_over_Lambda=f)), 172.5, 0.15, 0.999, 30)
    if np.isfinite(fc):
        r = predict(Cand(kk_Mc_over_Lambda=fc))
        out["fit_Mc_to_Mt"] = {"Mc_over_Lambda": fc, "Mc_GeV": fc * r["Lambda"], "Mt": r["Mt"], "Mh": r["Mh"],
                               "g_B": r["g_B"], "levels_at_Lambda": 1 / fc ** 2, **pulls(r)}
    else:
        out["fit_Mc_to_Mt"] = None
    return out


# ------------------------------------------------------------------ (5) canonical factor (numerology check)


def required_ratio() -> Dict[str, float]:
    f = lambda r: _mt(Cand(r_yuk=r))
    r0 = solve_for(f, 172.5, 0.7, 1.0)
    lo = solve_for(f, 172.5 - SIG_MT, 0.7, 1.0)
    hi = solve_for(f, 172.5 + SIG_MT, 0.7, 1.0)
    return {"r": r0, "r_1sigma": sorted([lo, hi])}


def canonical_constants() -> Dict[str, float]:
    w = 0.927
    return {
        "omega0": w, "omega0^2": w * w, "omega0^3": w ** 3, "sqrt(omega0)": math.sqrt(w),
        "omega0^(13/4)": w ** (13 / 4), "(1+omega0)/2 - 1/8": (1 + w) / 2 - 0.125,
        "4/5": 0.8, "sqrt(2/3)": math.sqrt(2 / 3), "sqrt(5/8)": math.sqrt(5 / 8), "pi/4": math.pi / 4,
        "2/sqrt(6)": 2 / math.sqrt(6), "sqrt(3/5)*... (g1 norm)": math.sqrt(3 / 5), "e^(-1/4)": math.exp(-0.25),
        "sqrt(4/6) (a=6)": math.sqrt(4 / 6), "sqrt(4/7) (a=7)": math.sqrt(4 / 7), "1/sqrt(phi)": 1 / math.sqrt((1 + 5 ** 0.5) / 2),
    }


def cand5() -> Dict[str, object]:
    req = required_ratio()
    lo, hi = req["r_1sigma"]
    consts = {k: v for k, v in canonical_constants().items() if v is not None}
    hits = {k: v for k, v in consts.items() if lo <= v <= hi}
    # Dual-Zero generator values: eps(n) = omega0 (-1)^n n^-n; Reg2 of (1, eps)-type sequences
    w = 0.927
    eps = {n: w * (-1) ** n * n ** (-n) for n in range(1, 6)}
    dz = {"1+eps(2)": 1 + eps[2], "1+eps(3)": 1 + eps[3], "Reg2(1+eps)_1": 1 + (eps[2] + eps[3]) / 2,
          "1+eps(1)": 1 + eps[1], "sum_n eps(n)+1": 1 + sum(eps.values())}
    for k, v in dz.items():
        if lo <= v <= hi:
            hits["DZ:" + k] = v
    # what the factor does to M_h if it is a Higgs-normalisation factor (lambda ~ r^4)
    r = req["r"]
    yuk_only = predict(Cand(r_yuk=r))
    norm = predict(Cand(r_yuk=r, r_quartic_power=4))
    width = hi - lo
    expected_chance_hits = len(consts) * width / (max(consts.values()) - min(consts.values()))
    return {"required": req, "constants": consts, "expected_chance_hits": expected_chance_hits, "dual_zero_values": dz, "within_1sigma": hits,
            "Mh_if_yukawa_only": yuk_only["Mh"], "Mh_if_Higgs_normalisation": norm["Mh"]}


# ------------------------------------------------------------------ (6) SM-group spectral model (CCM / Boyle-Farnsworth B-L + complex sigma)


def _sm_high_rhs(t, s, nu_on_above: float, sig_on: bool):
    # s = 7 SM couplings + (yn, k, ls, yN)
    base = th.sm_beta(s[:7], 2, False)
    gY, g2, g3, yt, yb, ytau, lam = s[:7]
    yn, k, ls, yN = s[7:]
    on = 1.0 if t > nu_on_above else 0.0
    yn2 = on * yn * yn
    base[3] += yt * yn2 / PI2_16
    base[6] += (4 * lam * yn2 - 2 * yn2 * yn2 + 2 * k * k) / PI2_16
    Y2 = 3 * yt * yt + 3 * yb * yb + ytau * ytau + yn2
    dyn = on * yn * (1.5 * yn2 + Y2 - 0.75 * gY * gY - 2.25 * g2 * g2)
    wf = 3 * g2 * g2 + gY * gY
    dk = k * (12 * lam + 6 * ls + 8 * k + 2 * Y2 + 2 * yN * yN - 1.5 * wf)
    dls = 18 * ls * ls + 8 * k * k + 4 * yN * yN * ls - 4 * yN ** 4
    dyN = 4 * yN ** 3
    return np.concatenate([base, np.array([dyn, dk, dls, dyN]) / PI2_16])


def sm_group(n: float = 1.0, M_N: float = 1e13, sigma: bool = True, which: str = "g2=g3",
             log10_muB: Optional[float] = None) -> Dict[str, float]:
    """SM-gauge-group spectral boundary (g = g_2) at the scale `which`, or at a forced scale."""
    p, smw, _, _ = background("composite")
    def gap(lm):
        gY, g2, g3 = smw.state(10 ** lm)[:3]
        return g2 - g3 if which == "g2=g3" else gY * math.sqrt(5 / 3) - g2
    lB = log10_muB if log10_muB is not None else brentq(gap, 10.0, 18.0)
    M_N = min(M_N, 10 ** lB)
    muB = 10 ** lB
    st = smw.state(muB)
    gY, g2, g3, _, yb, ytau, _ = st
    g = g2
    a = 3 + n
    yt = math.sqrt(max(4 * g * g - 3 * yb * yb - ytau * ytau, 0) / a)
    lam = 4 * g * g * (3 + n * n) / a ** 2
    kap = 4 * g * g * 2 * n / a if sigma else 0.0
    s0 = [gY, g2, g3, yt, yb, ytau, lam, math.sqrt(n) * yt, kap, 8 * g * g, 0.0]
    hi = solve_ivp(_sm_high_rhs, (math.log(muB), math.log(M_N)), s0, args=(math.log(M_N), sigma),
                   rtol=1e-10, atol=1e-13, method="DOP853")
    s = hi.y[:, -1]
    lam_SM = s[6] - (s[8] ** 2 / s[9] if sigma else 0.0)
    down = th.run_sm(list(s[:6]) + [lam_SM], M_N, p.Mt, 2, False)
    Mt = th.Mt_from_yt(down.y[3, -1])
    return {"log10_Lambda": lB, "g_B": g, "yt_B": yt, "yt_B_data": smw.state(muB)[3],
            "Mt": Mt, "Mh": th.Mh_from_lambda(down.y[6, -1], Mt)}


def cand6() -> Dict[str, object]:
    out = {}
    for which in ("g2=g3", "g1=g2"):
        for MN in (1e11, 1e13):
            out[f"{which}, M_N=m_sigma=1e{int(math.log10(MN))}"] = sm_group(1.0, MN, True, which)
        out[f"{which}, no sigma"] = sm_group(1.0, 1e13, False, which)
    out["g2=g3, n fitted to M_t"] = None
    try:
        nfit = solve_for(lambda n: sm_group(n, 1e13, True)["Mt"], 172.5, 0.5, 6.0, 12)
        if np.isfinite(nfit):
            out["g2=g3, n fitted to M_t"] = {"n": nfit, **sm_group(nfit, 1e13, True)}
    except Exception:
        pass
    return out


# ------------------------------------------------------------------ (7) twisted / grand symmetry: same traces


def cand7() -> Dict[str, object]:
    out = {}
    for label, c in (("grand symmetry: sigma from twist, PS composite", Cand()),
                     ("extra PS scalars (2,2,15) light", Cand(scenario="with2215")),
                     ("extra PS scalars (1,1,15) light", Cand(scenario="with15"))):
        r = predict(c)
        if r.get("ok"):
            out[label] = {"Mt": r["Mt"], "Mh": r["Mh"], "yt_B": r["yt_B"]}
    return out


# ------------------------------------------------------------------ combination: VL trace + large y_nu (two parameters)


def combo(m_mult: int = 4) -> Dict[str, object]:
    """For each n, fix the VL trace x by M_t = 172.5 (x4 = x^2/m); then solve n for M_h = 125.1."""
    def at_n(n):
        x = solve_for(lambda x: _mt(Cand(n=n, x=x, x4=x * x / m_mult)), 172.5, 0.0, 8.0, 17)
        if not np.isfinite(x):
            return float("nan"), float("nan")
        return x, predict(Cand(n=n, x=x, x4=x * x / m_mult))["Mh"]
    rows = {}
    for n in (1.0, 1.5, 2.0, 2.5):
        x, mh = at_n(n)
        rows[str(n)] = {"x": x, "Mh": mh}
    nfit = solve_for(lambda n: at_n(n)[1], 125.1, 1.0, 3.0, 9)
    best = None
    if np.isfinite(nfit):
        x, mh = at_n(nfit)
        r = predict(Cand(n=nfit, x=x, x4=x * x / m_mult))
        _, _, sol, ps = background("composite")
        gR = ps.sol(math.log(sol["m_R_GeV"]))[0]
        best = {"n": nfit, "x": x, "Mt": r["Mt"], "Mh": r["Mh"], "seesaw": seesaw_check(r)}
        # feed back the largest perturbative y_N (needed for the lightest possible m_nu)
        yNg = best["seesaw"]["yN_max_mR"] / 2.0 / r["g_B"]  # rough y_N(Lambda)/g, y_N grows ~2x to Lambda
        rr = predict(Cand(n=nfit, x=x, x4=x * x / m_mult, yN_over_g=min(yNg, math.sqrt(4 * math.pi) / r["g_B"] * 0.99)))
        best["with_large_yN"] = {"Mt": rr.get("Mt"), "Mh": rr.get("Mh")}
    return {"m_mult": m_mult, "scan": rows, "fit": best}
