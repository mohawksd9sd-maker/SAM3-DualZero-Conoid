"""Search for the extra structure that could repair the doc-58 mass failures (doc 59).

Generalised Higgs-sector running with independent y_t, y_nu, the singlet sigma
(own quartic, portal, Majorana Yukawa y_N) and a movable sigma threshold.

Above m_R (PS gauge couplings from the doc-55 two-loop solution):
  16pi^2 dy_t/dt  = y_t [ 9/2 y_t^2 + 3/2 y_nu^2 - G.g^2 ]
  16pi^2 dy_nu/dt = y_nu[ 3 y_t^2 + 3 y_nu^2 - G.g^2 ]
      (both reduce to the PS single-coupling 6 y^2 at y_nu = y_t, and to the
       SM 9/2 y_t^2 at y_nu -> 0; G.g^2 = 9/4 g_R^2 + 9/4 g_L^2 + 45/4 g_4^2)
  16pi^2 dlambda/dt = 24 l^2 + 2 k^2 + 4 l (3 y_t^2 + y_nu^2) - 2 (3 y_t^4 + y_nu^4)
                      - 9 l (g_L^2+g_R^2) + 3/8 (2 g_L^4 + (g_L^2+g_R^2)^2)
  16pi^2 dkappa/dt  = k [12 l + 6 l_s + 8 k + 2 (3 y_t^2 + y_nu^2) + 2 y_N^2 - 9/2 (g_L^2+g_R^2)]
  16pi^2 dl_s/dt    = 18 l_s^2 + 8 k^2 + 4 y_N^2 l_s - 4 y_N^4
  16pi^2 dy_N/dt    = 4 y_N^3
  (y_N: one dominant nu_R, L = -(1/2) y_N sigma N N; Machacek-Vaughn with
   two-component fermions: Y_2(S) = y_N^2, H = 6 y_N^4 per Weyl N.)
m_R -> m_sigma (SM gauge, sigma still light, nu_R decoupled at M_N ~ m_R).
At m_sigma: lambda -> lambda - kappa^2/l_s.  m_sigma -> M_t: SM.
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

from group_theory import pati_salam
from higgs_masses import MH_OBS, MT_POLE, V_EW
from rge import PDG, PI2_16, Coeffs, SMRun, _solve, match_to_ps, solve_unification

M_PLANCK_RED = 2.435e18


def boundary(g: float, n: float, yN0: float) -> List[float]:
    yt = 2 * g / math.sqrt(3 + n)
    return [yt, math.sqrt(n) * yt,
            (n * n + 3) / (n + 3) ** 2 * 4 * g * g,
            (2 * n / (n + 3)) * 4 * g * g,
            8 * g * g, yN0]


def yt_two_loop_sm(yt, g1, g2, g3):
    """SM two-loop y_t beta (gauge + top terms; lambda terms omitted), GUT g_1.

    Arason et al. PRD 46 (1992) 3945; Luo-Wang-Xiao hep-ph/0211440.
    Returns (16 pi^2)^2 * beta^(2) / y_t.
    """
    a, b, c, y2 = g1 * g1, g2 * g2, g3 * g3, yt * yt
    return (-12 * y2 * y2 + (393 / 80 * a + 225 / 16 * b + 36 * c) * y2
            + 1187 / 600 * a * a - 9 / 20 * a * b + 19 / 15 * a * c
            - 23 / 4 * b * b + 9 * b * c - 108 * c * c)


TWO_LOOP_TOP = {"on": False}


def _rhs_high(t, s, gfun, sm_gauge: bool):
    yt, yn, l, k, ls, yN = s
    if sm_gauge:
        g1, g2, g3 = gfun(t)
        gp2, g22 = 0.6 * g1 * g1, g2 * g2
        Gt = 0.85 * g1 * g1 + 2.25 * g22 + 8 * g3 * g3
        Gn = 0.45 * g1 * g1 + 2.25 * g22
        wf = 3 * g22 + gp2
        g4t = 0.375 * (2 * g22 ** 2 + (g22 + gp2) ** 2)
        yn_on = 0.0  # nu_R decoupled below m_R
    else:
        gR, gL, g4 = gfun(t)
        Gt = Gn = 2.25 * gR * gR + 2.25 * gL * gL + 11.25 * g4 * g4
        wf = 3 * (gL * gL + gR * gR)
        g4t = 0.375 * (2 * gL ** 4 + (gL * gL + gR * gR) ** 2)
        yn_on = 1.0
    yn = yn * yn_on
    yN = yN * yn_on
    dyt = yt * (4.5 * yt * yt + 1.5 * yn * yn - Gt)
    if sm_gauge and TWO_LOOP_TOP["on"]:
        dyt += yt * yt_two_loop_sm(yt, g1, g2, g3) / PI2_16
    dyn = yn * (3 * yt * yt + 3 * yn * yn - Gn)
    S2 = 3 * yt * yt + yn * yn
    dl = 24 * l * l + 2 * k * k + 4 * l * S2 - 2 * (3 * yt ** 4 + yn ** 4) - 3 * l * wf + g4t
    dk = k * (12 * l + 6 * ls + 8 * k + 2 * S2 + 2 * yN * yN - 1.5 * wf)
    dls = 18 * ls * ls + 8 * k * k + 4 * yN * yN * ls - 4 * yN ** 4
    dyN = 4 * yN ** 3
    return np.array([dyt, dyn, dl, dk, dls, dyN]) / PI2_16


def _rhs_sm(t, s, gfun):
    yt, l = s
    g1, g2, g3 = gfun(t)
    gp2, g22 = 0.6 * g1 * g1, g2 * g2
    dy = yt * (4.5 * yt * yt - 0.85 * g1 * g1 - 2.25 * g22 - 8 * g3 * g3)
    if TWO_LOOP_TOP["on"]:
        dy += yt * yt_two_loop_sm(yt, g1, g2, g3) / PI2_16
    dl = 24 * l * l + l * (12 * yt * yt - 3 * (3 * g22 + gp2)) - 6 * yt ** 4 + 0.375 * (2 * g22 ** 2 + (g22 + gp2) ** 2)
    return np.array([dy, dl]) / PI2_16


class Setup:
    """Gauge background for one unification solution (cached)."""

    def __init__(self, scenario: str = "composite", sol: Optional[Dict] = None):
        self.scenario = scenario
        self.sol = sol or solve_unification(PDG, scenario, 2)
        self.sm = SMRun(PDG, 2)
        C = Coeffs.from_model(pati_salam(scenario), 2)
        m_R, Lam = self.sol["m_R_GeV"], self.sol["Lambda_GeV"]
        s0 = match_to_ps(self.sm.at(m_R), scenario, None, True)
        self.ps = _solve(C, math.log(m_R), math.log(Lam), s0, with_yukawa=True, dense=True)

    def run(self, n: float = 1.0, yN0: float = 0.0, msig_over_mR: float = 1.0,
            sigma: bool = True, bc_override: Optional[List[float]] = None,
            yt_from_data: bool = False) -> Dict[str, float]:
        m_R, Lam, g = self.sol["m_R_GeV"], self.sol["Lambda_GeV"], self.sol["g_U"]
        bc = bc_override or boundary(g, n, yN0)
        if not sigma:
            bc[3] = 0.0
        if yt_from_data:
            bc[0] = self.sol["y_at_Lambda"]
        ps_g = lambda t: self.ps.sol(t)[:3]
        hi = solve_ivp(_rhs_high, (math.log(Lam), math.log(m_R)), bc, args=(ps_g, False), rtol=1e-9, atol=1e-12)
        s = hi.y[:, -1]
        sm_g = lambda t: self.sm.sol.sol(t)[:3]
        m_sig = msig_over_mR * m_R
        if sigma and m_sig < m_R:
            mid = solve_ivp(_rhs_high, (math.log(m_R), math.log(m_sig)), s, args=(sm_g, True), rtol=1e-9, atol=1e-12)
            s = mid.y[:, -1]
            t0 = math.log(m_sig)
        else:
            t0 = math.log(m_R)
        yt, yn, l, k, ls, yN = s
        lam = l - (k * k / ls if sigma else 0.0)
        lo = solve_ivp(_rhs_sm, (t0, math.log(MT_POLE)), [yt, lam], args=(sm_g,), rtol=1e-9, atol=1e-12)
        y_mt, l_mt = lo.y[:, -1]
        yt_obs = PDG.yt_at_mt()
        return {
            "m_t_pred": MT_POLE + (y_mt - yt_obs) / 0.00556,
            "m_H_pred": math.sqrt(max(2 * l_mt, 0.0)) * V_EW,
            "lambda_mt": l_mt, "y_t_mt": y_mt,
            "lambda_s_at_sigma": ls, "kappa_at_sigma": k,
        }


# ---------------------------------------------------------------- (a) sigma


def sigma_variations(st: Optional[Setup] = None) -> Dict[str, Dict]:
    st = st or Setup()
    g = st.sol["g_U"]
    out = {}
    for yfac in (0.0, 0.5, 1.0, 2.0):
        for r in (0.1, 0.3, 1.0):
            res = st.run(1.0, yfac * g, r)
            out[f"yN0={yfac}g, m_sigma/m_R={r}"] = {"m_t": res["m_t_pred"], "m_H": res["m_H_pred"]}
    obs = {}
    for yfac in (0.0, 2.0):
        for r in (0.1, 1.0):
            obs[f"yN0={yfac}g, m_sigma/m_R={r}"] = st.run(1.0, yfac * g, r, yt_from_data=True)["m_H_pred"]
    return {"spectral_top": out, "measured_top_mH": obs}


# ---------------------------------------------------------------- (b) n free


def fit_n(st: Setup, target: str, yN0: float = 0.0) -> Optional[Dict[str, float]]:
    key, val = ("m_H_pred", MH_OBS) if target == "m_H" else ("m_t_pred", MT_POLE)
    f = lambda n: st.run(n, yN0)[key] - val
    grid = np.linspace(0.0, 4.0, 41)
    vals = [f(x) for x in grid]
    for a, b, va, vb in zip(grid[:-1], grid[1:], vals[:-1], vals[1:]):
        if va * vb < 0 and va > -val * 0.99 and vb > -val * 0.99:
            n = brentq(f, a, b, xtol=1e-6)
            r = st.run(n, yN0)
            return {"n": n, "m_t": r["m_t_pred"], "m_H": r["m_H_pred"]}
    return None


def n_free_study() -> Dict[str, object]:
    out = {}
    for sc in ("composite", "with2215"):
        st = Setup(sc)
        out[sc] = {
            "unification": {k: st.sol[k] for k in ("m_R_GeV", "Lambda_GeV", "alpha_U_inv", "g_U")},
            "n1": {k: v for k, v in st.run(1.0).items() if k in ("m_t_pred", "m_H_pred")},
            "fit_n_to_mH": fit_n(st, "m_H"),
            "fit_n_to_mt": fit_n(st, "m_t"),
        }
    return out


# ---------------------------------------------------------------- (c) thresholds


def threshold_propagation(n_samples: int = 40, seed: int = 59) -> Dict[str, object]:
    rng = np.random.default_rng(seed)
    sm = SMRun(PDG, 2)
    mts, mhs, lam = [], [], []
    for _ in range(n_samples):
        u = rng.uniform(-1, 1, 6)
        sol = solve_unification(PDG, "composite", 2, log10_ratios=u, sm=sm)
        if sol is None:
            continue
        st = Setup("composite", sol)
        r = st.run(1.0)
        mts.append(r["m_t_pred"])
        mhs.append(r["m_H_pred"])
        lam.append(math.log10(sol["Lambda_GeV"]))
    a = lambda x: {"min": float(min(x)), "median": float(np.median(x)), "max": float(max(x))}
    return {"samples": len(mts), "m_t": a(mts), "m_H": a(mhs), "log10_Lambda": a(lam)}


# ---------------------------------------------------------------- (d) gravity / higher moments


def required_boundary_shifts(st: Optional[Setup] = None) -> Dict[str, float]:
    """What change of the spectral boundary values would hit 172.5 / 125.1?"""
    st = st or Setup()
    g = st.sol["g_U"]
    base = boundary(g, 1.0, 0.0)
    # top: multiply y_t(Lambda) (and y_nu) by s
    def ft(s):
        bc = list(base); bc[0] *= s; bc[1] *= s
        return st.run(bc_override=bc)["m_t_pred"] - MT_POLE
    s_t = brentq(ft, 0.6, 1.2, xtol=1e-8)
    # Higgs: with that top, multiply lambda_h(Lambda) by r
    def fh(r):
        bc = list(base); bc[0] *= s_t; bc[1] *= s_t; bc[2] *= r
        return st.run(bc_override=bc)["m_H_pred"] - MH_OBS
    try:
        r_h = brentq(fh, 0.0, 1.5, xtol=1e-8)
    except ValueError:
        r_h = float("nan")
    Lam = st.sol["Lambda_GeV"]
    return {
        "y_t_scale_factor_needed": s_t,
        "lambda_h_scale_factor_needed_with_fixed_top": r_h,
        "gravity_correction_size_(Lambda/M_Pl)^2": (Lam / M_PLANCK_RED) ** 2,
        "a6_correction_to_dim4_couplings": 0.0,
    }


def two_loop_top_study() -> Dict[str, object]:
    """Repeat the n fit with SM two-loop y_t running below m_R."""
    st = Setup()
    g = st.sol["g_U"]
    TWO_LOOP_TOP["on"] = True
    try:
        out = {
            "n1": {k: v for k, v in st.run(1.0).items() if k in ("m_t_pred", "m_H_pred")},
            "fit_n_to_mH_yN0": fit_n(st, "m_H", 0.0),
            "fit_n_to_mH_yN2g": fit_n(st, "m_H", 2 * g),
        }
    finally:
        TWO_LOOP_TOP["on"] = False
    return out


def ledger() -> List[Dict[str, object]]:
    """Predictions minus parameters for each candidate repair (filled by report)."""
    return [
        {"fix": "minimal spectral PS (doc 58)", "params": 0, "predictions": 2, "hits": 0},
        {"fix": "(a) sigma with own running, y_N, threshold in motivated ranges", "params": 0, "predictions": 2, "hits": 0},
        {"fix": "(b) extended Higgs content, n = (y_nu/y_t)^2 free", "params": 1, "predictions": 2, "hits": 1},
        {"fix": "(c) PS thresholds at m_R (x/÷10)", "params": 0, "predictions": 2, "hits": 0},
        {"fix": "(d) gravity / a_6 corrections", "params": 0, "predictions": 2, "hits": 0},
        {"fix": "(b)+(d') free y_t(Lambda) and lambda(Lambda) corrections", "params": 2, "predictions": 2, "hits": 2},
    ]


# ---------------------------------------------------------------- gauge-group: Clifford check


def clifford(p: int, q: int):
    """Real Clifford algebra Cl(p,q) (e_i^2=+1 for i<p, -1 otherwise) via complex gammas.

    Returns (real dimension of the span, real dimension of the centre,
    square of the volume element, structure label from the mod-8 table).
    """
    s1 = np.array([[0, 1], [1, 0]], complex)
    s2 = np.array([[0, -1j], [1j, 0]], complex)
    s3 = np.array([[1, 0], [0, -1]], complex)
    I2 = np.eye(2)
    # five anticommuting Hermitian 4x4 gammas
    G = [np.kron(s1, I2), np.kron(s2, I2), np.kron(s3, s1), np.kron(s3, s2), np.kron(s3, s3)]
    n = p + q
    gens = [G[i] if i < p else 1j * G[i] for i in range(n)]
    elems = []
    from itertools import combinations
    for r in range(n + 1):
        for c in combinations(range(n), r):
            M = np.eye(4, dtype=complex)
            for i in c:
                M = M @ gens[i]
            elems.append(M)
    vecs = np.array([np.concatenate([E.real.ravel(), E.imag.ravel()]) for E in elems])
    dim = int(np.linalg.matrix_rank(vecs))
    vol = elems[-1]
    vol2 = vol @ vol
    vol_sq = int(round(np.real(vol2[0, 0]))) if np.allclose(vol2, vol2[0, 0] * np.eye(4)) else None
    # centre within the 2^n abstract algebra: 1 and (for odd n) the volume element
    table = {0: "M(R)", 1: "M(R)+M(R)", 2: "M(R)", 3: "M(C)", 4: "M(H)", 5: "M(H)+M(H)", 6: "M(H)", 7: "M(C)"}
    return {"abstract_dim": 2 ** n, "rep_real_span": dim, "volume_squared": vol_sq,
            "type": table[(p - q) % 8]}


def quaternion_commutant_of_grading() -> int:
    """Real dim of {x in M_2(H) : x gamma = gamma x}, gamma = diag(1,-1) on H^2: H+H = 8."""
    def quat(a, b):
        return np.array([[a, b], [-np.conj(b), np.conj(a)]])
    basis = []
    for i in range(2):
        for j in range(2):
            for (a, b) in ((1, 0), (1j, 0), (0, 1), (0, 1j)):
                M = np.zeros((4, 4), complex)
                M[2 * i:2 * i + 2, 2 * j:2 * j + 2] = quat(a, b)
                basis.append(M)
    gam = np.diag([1, 1, -1, -1])
    rows = np.array([np.concatenate([(B @ gam - gam @ B).real.ravel(), (B @ gam - gam @ B).imag.ravel()]) for B in basis]).T
    return len(basis) - int(np.linalg.matrix_rank(rows))


# ---------------------------------------------------------------- 0nu-beta-beta (generic)


def mbb_ranges() -> Dict[str, Dict[str, float]]:
    """|m_bb| for m_lightest = 0 (NuFIT 6.0 central), scanning Majorana phases."""
    s12, s13 = math.sqrt(0.307), math.sqrt(0.0222)
    c12, c13 = math.sqrt(1 - 0.307), math.sqrt(1 - 0.0222)
    dm21, dm31 = 7.41e-5, 2.51e-3
    out = {}
    for order in ("NO", "IO"):
        if order == "NO":
            m = (0.0, math.sqrt(dm21), math.sqrt(dm31))
        else:
            m3 = 0.0
            m2 = math.sqrt(dm31)  # |dm32| ~ dm31 for IO
            m = (math.sqrt(m2 ** 2 - dm21), m2, m3)
        U2 = (c12 ** 2 * c13 ** 2, s12 ** 2 * c13 ** 2, s13 ** 2)
        vals = []
        for a in np.linspace(0, 2 * math.pi, 73):
            for b in np.linspace(0, 2 * math.pi, 73):
                vals.append(abs(U2[0] * m[0] + U2[1] * m[1] * np.exp(1j * a) + U2[2] * m[2] * np.exp(1j * b)))
        out[order] = {"min_eV": float(min(vals)), "max_eV": float(max(vals))}
    return out
