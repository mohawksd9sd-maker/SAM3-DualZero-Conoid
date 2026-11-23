"""Spectral-action boundary relations at Lambda: top Yukawa, Higgs quartic
with the singlet sigma, Majorana scale and seesaw (doc 58).

Boundary values at Lambda (CC2012 'Resilience', arXiv:1208.1030, eqs. 9-15;
f0 fixed by f0/(2 pi^2) = 1/(4 g^2)):
    n = (y_nu / y_t)^2  at Lambda
    y_t(Lambda)       = 2 g / sqrt(3 + n)          [Tr Y^dagger Y = 4 g^2, top+nu dominance]
    lambda_h(Lambda)  = (n^2 + 3)/(n + 3)^2 * 4 g^2
    lambda_hs(Lambda) = 2 n/(n + 3) * 4 g^2
    lambda_s(Lambda)  = 8 g^2
In Pati-Salam with one bidoublet Yukawa, y_nu = y_t at and above m_R, so
n = 1 is *fixed*, not fitted: y_t = g, lambda_h = g^2, lambda_hs = 2 g^2,
lambda_s = 8 g^2.  None of these depends on f2 or f4; f0 is traded for g.
f2 sets the mass terms (the Higgs and sigma mass parameters ~ f2 Lambda^2):
the electroweak vev and w ~ m_R are therefore NOT predicted.

Potential convention: V = lambda |H|^4 + kappa |H|^2 sigma^2 + (lambda_s/4) sigma^4
(lambda = lambda_h, kappa = lambda_hs, lambda_s = lambda_sigma of CC2012),
m_H^2 = 2 lambda(m_t) v^2.

Running (one loop for y and the quartics; gauge couplings from the two-loop
solution of rge.py):
  Lambda -> m_R  (PS):  16pi^2 dy/dt = y (6 y^2 - 9/4 g_R^2 - 9/4 g_L^2 - 45/4 g_4^2)
     16pi^2 dlambda/dt  = 24 l^2 + 2 k^2 + l (16 y^2 - 9 (g_L^2+g_R^2)) - 8 y^4
                          + 3/8 (2 g_L^4 + (g_L^2 + g_R^2)^2)          [approx.]
     16pi^2 dkappa/dt   = k (12 l + 6 l_s + 8 k + 8 y^2 - 9/2 (g_L^2+g_R^2))
     16pi^2 dlambda_s/dt= 18 l_s^2 + 8 k^2                             [Majorana Yukawa of sigma omitted]
  at m_R: sigma integrated out at tree level, lambda_SM = lambda - kappa^2/lambda_s;
          y_t = y.
  m_R -> m_t (SM):  standard one-loop lambda, y_t (GUT-normalised g_1).
The scalar-only parts (24 l^2 + 2 k^2, ...) are derived in ``scalar_betas``
from the general formula beta_ijkl = sum (lambda_ijmn lambda_mnkl + 2 perms).
"""

from __future__ import annotations

import math
from typing import Dict, Optional

import numpy as np
from scipy.integrate import solve_ivp

from rge import PDG, PI2_16, Coeffs, SMRun, match_to_ps, solve_unification
from group_theory import pati_salam

V_EW = 246.22
MH_OBS = 125.1  # PDG ~125.20(11); 125.1 as requested
MT_POLE = 172.5


def boundary(g: float, n: float = 1.0, with_sigma: bool = True) -> Dict[str, float]:
    out = {
        "y_t": 2 * g / math.sqrt(3 + n),
        "lambda_h": (n * n + 3) / (n + 3) ** 2 * 4 * g * g,
        "lambda_hs": (2 * n / (n + 3)) * 4 * g * g if with_sigma else 0.0,
        "lambda_s": 8 * g * g,
    }
    return out


def scalar_tensor(l: float, k: float, ls: float) -> np.ndarray:
    """lambda_ijkl for 4 real Higgs components + sigma (index 4)."""
    T = np.zeros((5, 5, 5, 5))
    d = np.eye(5)
    for i in range(5):
        for j in range(5):
            for a in range(5):
                for b in range(5):
                    if max(i, j, a, b) < 4:
                        T[i, j, a, b] = 2 * l * (d[i, j] * d[a, b] + d[i, a] * d[j, b] + d[i, b] * d[j, a])
    for i in range(4):
        for j in range(4):
            v = 2 * k * d[i, j]
            for (p, q, r, s) in ((i, j, 4, 4), (i, 4, j, 4), (i, 4, 4, j), (4, i, j, 4), (4, i, 4, j), (4, 4, i, j)):
                T[p, q, r, s] = v
    T[4, 4, 4, 4] = 6 * ls
    return T


def scalar_betas(l: float, k: float, ls: float):
    """(16 pi^2) x pure-scalar one-loop betas of (lambda, kappa, lambda_s)."""
    T = scalar_tensor(l, k, ls)
    M = np.einsum("ijmn,mnkl->ijkl", T, T)
    B = M + np.transpose(M, (0, 2, 1, 3)) + np.transpose(M, (0, 3, 2, 1))
    return B[0, 0, 0, 0] / 6.0, B[0, 0, 4, 4] / 2.0, B[4, 4, 4, 4] / 6.0


def _ps_rhs(t, s, gauge_sol):
    y, l, k, ls = s
    gR, gL, g4 = gauge_sol(t)
    gR2, gL2, g42 = gR * gR, gL * gL, g4 * g4
    dy = y * (6 * y * y - 2.25 * gR2 - 2.25 * gL2 - 11.25 * g42)
    dl = 24 * l * l + 2 * k * k + l * (16 * y * y - 9 * (gL2 + gR2)) - 8 * y ** 4 + 0.375 * (2 * gL2 ** 2 + (gL2 + gR2) ** 2)
    dk = k * (12 * l + 6 * ls + 8 * k + 8 * y * y - 4.5 * (gL2 + gR2))
    dls = 18 * ls * ls + 8 * k * k
    return np.array([dy, dl, dk, dls]) / PI2_16


def _sm_rhs(t, s, gauge_sol):
    y, l = s
    g1, g2, g3 = gauge_sol(t)
    gp2 = 0.6 * g1 * g1
    g22 = g2 * g2
    dy = y * (4.5 * y * y - 0.85 * g1 * g1 - 2.25 * g22 - 8 * g3 * g3)
    dl = 24 * l * l + l * (12 * y * y - 3 * (3 * g22 + gp2)) - 6 * y ** 4 + 0.375 * (2 * g22 ** 2 + (g22 + gp2) ** 2)
    return np.array([dy, dl]) / PI2_16


def predict(n: float = 1.0, with_sigma: bool = True, sol: Optional[Dict] = None) -> Dict[str, object]:
    """Run the spectral boundary values down and compare to m_t, m_H."""
    sol = sol or solve_unification(PDG, "composite", 2)
    m_R, Lam, gU = sol["m_R_GeV"], sol["Lambda_GeV"], sol["g_U"]
    sm = SMRun(PDG, 2)
    # PS gauge couplings from the data-driven two-loop solution (dense)
    C = Coeffs.from_model(pati_salam("composite"), 2)
    from rge import _solve
    s0 = match_to_ps(sm.at(m_R), "composite", None, True)
    gs = _solve(C, math.log(m_R), math.log(Lam), s0, with_yukawa=True, dense=True)
    ps_g = lambda t: gs.sol(t)[:3]
    bc = boundary(gU, n, with_sigma)
    ps = solve_ivp(_ps_rhs, (math.log(Lam), math.log(m_R)),
                   [bc["y_t"], bc["lambda_h"], bc["lambda_hs"], bc["lambda_s"]],
                   args=(ps_g,), rtol=1e-10, atol=1e-12)
    y_mR, l_mR, k_mR, ls_mR = ps.y[:, -1]
    lam_SM_mR = l_mR - (k_mR ** 2 / ls_mR if with_sigma else 0.0)
    sm_g = lambda t: sm.sol.sol(t)[:3]
    smr = solve_ivp(_sm_rhs, (math.log(m_R), math.log(MT_POLE)), [y_mR, lam_SM_mR],
                    args=(sm_g,), rtol=1e-10, atol=1e-12)
    y_mt, lam_mt = smr.y[:, -1]
    # MSbar y_t(m_t) -> pole mass (inverse of the Buttazzo fit, leading slope)
    yt_obs = PDG.yt_at_mt()
    mt_pred = MT_POLE + (y_mt - yt_obs) / 0.00556
    mH = math.sqrt(max(2 * lam_mt, 0.0)) * V_EW
    return {
        "n": n, "with_sigma": with_sigma, "g_U": gU, "m_R": m_R, "Lambda": Lam,
        "boundary_at_Lambda": bc,
        "at_m_R": {"y": y_mR, "lambda_h": l_mR, "lambda_hs": k_mR, "lambda_s": ls_mR,
                   "lambda_SM_after_sigma": lam_SM_mR,
                   "reduction_factor_sqrt": math.sqrt(max(lam_SM_mR / l_mR, 0)) if l_mR > 0 else None},
        "y_t_at_mt_pred": y_mt, "y_t_at_mt_obs": yt_obs,
        "y_t_data_at_Lambda": sol["y_at_Lambda"],
        "m_t_pole_pred_GeV": mt_pred,
        "lambda_at_mt": lam_mt, "m_H_pred_GeV": mH, "m_H_obs_GeV": MH_OBS,
    }


def n_scan(ns=(0.0, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0)):
    sol = solve_unification(PDG, "composite", 2)
    return {n: {k: v for k, v in predict(n, True, sol).items() if k in ("m_t_pole_pred_GeV", "m_H_pred_GeV")} for n in ns}


def mH_with_observed_top(with_sigma: bool = True, n: float = 1.0) -> Dict[str, float]:
    """Higgs mass if only the quartic boundary is imposed and y_t is taken from data."""
    sol = solve_unification(PDG, "composite", 2)
    m_R, Lam, gU = sol["m_R_GeV"], sol["Lambda_GeV"], sol["g_U"]
    sm = SMRun(PDG, 2)
    C = Coeffs.from_model(pati_salam("composite"), 2)
    from rge import _solve
    s0 = match_to_ps(sm.at(m_R), "composite", None, True)
    gs = _solve(C, math.log(m_R), math.log(Lam), s0, with_yukawa=True, dense=True)
    ps_g = lambda t: gs.sol(t)[:3]
    bc = boundary(gU, n, with_sigma)
    ps = solve_ivp(_ps_rhs, (math.log(Lam), math.log(m_R)),
                   [sol["y_at_Lambda"], bc["lambda_h"], bc["lambda_hs"], bc["lambda_s"]],
                   args=(ps_g,), rtol=1e-10, atol=1e-12)
    y_mR, l_mR, k_mR, ls_mR = ps.y[:, -1]
    lam = l_mR - (k_mR ** 2 / ls_mR if with_sigma else 0.0)
    smr = solve_ivp(_sm_rhs, (math.log(m_R), math.log(MT_POLE)), [y_mR, lam],
                    args=(lambda t: sm.sol.sol(t)[:3],), rtol=1e-10, atol=1e-12)
    y_mt, lam_mt = smr.y[:, -1]
    return {"y_t_at_mt_check": y_mt, "m_H_pred_GeV": math.sqrt(max(2 * lam_mt, 0)) * V_EW}
