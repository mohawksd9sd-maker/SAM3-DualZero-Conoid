r"""Doc 66 part B: a finite ('bounded pond') universe -- T^3, S^3 and the Poincare dodecahedral space (PDS)
-- and the large-angle CMB, against Planck 2018.

Method (Sachs-Wolfe, ensemble average over Gaussian mode amplitudes):
* flat infinite:  C_l = 4 pi A \int dk/k j_l(k chi*)^2 = 2 pi A/(l(l+1));
* cubic T^3, side L:  \int d^3k/(2pi)^3 -> L^{-3} sum_n, k = 2 pi |n|/L;
* S^3 (curvature radius 1):  C_l = sum_{beta>=3} P(beta) |Phi^beta_l(chi*)|^2,  P = 2 pi^2 A/(beta(beta^2-1)),
  Phi^beta_l ∝ sin^l chi C^{(l+1)}_{beta-l-1}(cos chi) normalised on S^3;
* PDS = S^3/I* (I* binary icosahedral, order 120, acting by Clifford translations -> homogeneous space).
  The level-k (beta = k+1) S^3 modes form (j,j), j = k/2; the I*-invariant subspace is (j) x Inv_j.
  By Clebsch-Gordan orthogonality its m-averaged weight in every l sector is d_j/(2j+1) (d_j = I*-invariants
  in spin j, from the Molien series (1+t^30)/((1-t^12)(1-t^20)) in t = q^{2j}).
The ratio R_l = C_l(model)/C_l(flat) multiplies the Planck 2018 best-fit LCDM spectrum (SW-dominated low l;
ISW and Doppler pieces are treated the same way -- an approximation, stated in the doc).
Likelihood: full-sky inverse-gamma (cosmic variance) with f_sky = 0.94 for l = 2..30 (Commander-like).
"""

from __future__ import annotations

import math
from functools import lru_cache
from pathlib import Path
from typing import Dict, List

import numpy as np
from scipy.integrate import quad
from scipy.special import eval_gegenbauer, gammaln, spherical_jn, eval_legendre

DATA = Path(__file__).resolve().parent / "data"
LMAX = 30
FSKY = 0.94
CHI_STAR_OVER_DH = 14.0 / 4.448      # comoving distance to last scattering / (c/H0), Planck 2018 (h = 0.674)
OMK_PLANCK_BAO = (0.0007, 0.0019)    # Planck 2018 TT,TE,EE+lowE+lensing+BAO
OMK_PLANCK_CMB = (-0.044, 0.017)     # CMB alone (TT,TE,EE+lowE), approximate symmetric error


@lru_cache(maxsize=1)
def planck():
    d = np.loadtxt(DATA / "COM_PowerSpect_CMB-TT-full_R3.01.txt")
    th = np.loadtxt(DATA / "COM_PowerSpect_CMB-base-plikHM-TTTEEE-lowl-lowE-lensing-minimum-theory_R3.01.txt")
    ell = d[:, 0].astype(int)
    D = dict(zip(ell, d[:, 1]))
    err = dict(zip(ell, 0.5 * (d[:, 2] + d[:, 3])))
    T = dict(zip(th[:, 0].astype(int), th[:, 1]))
    return D, err, T


def flat_integral(l: int) -> float:
    return 1.0 / (2 * l * (l + 1))


# ------------------------------------------------------------------ T^3
@lru_cache(maxsize=1)
def _shells(nmax: int = 60):
    r = np.arange(-nmax, nmax + 1)
    X, Y, Z = np.meshgrid(r, r, r, indexing="ij")
    n2 = (X * X + Y * Y + Z * Z).ravel()
    n2 = n2[(n2 > 0) & (n2 <= nmax * nmax)]
    vals, counts = np.unique(n2, return_counts=True)
    return np.sqrt(vals.astype(float)), counts.astype(float), float(nmax)


def ratio_T3(l: int, L: float) -> float:
    """L in units of chi*."""
    nn, cnt, nmax = _shells()
    k = 2 * math.pi * nn / L
    s = (2 * math.pi / L) ** 3 * np.sum(cnt * spherical_jn(l, k) ** 2 / k ** 3)
    kmax = 2 * math.pi * nmax / L
    tail = quad(lambda x: spherical_jn(l, x) ** 2 / x, kmax, kmax + 400, limit=400)[0] + 0.5 / (kmax + 400) ** 2
    return float((s / (4 * math.pi) + tail) / flat_integral(l))


# ------------------------------------------------------------------ S^3 and PDS
def molien_I(kmax: int = 2000) -> np.ndarray:
    """d_j for j = k/2, k = 0..kmax: coefficients of (1+t^30)/((1-t^12)(1-t^20)) in t^k (k even only nonzero)."""
    c = np.zeros(kmax + 1)
    for a in range(0, kmax // 12 + 1):
        for b in range(0, (kmax - 12 * a) // 20 + 1):
            for e in (0, 30):
                k = 12 * a + 20 * b + e
                if k <= kmax:
                    c[k] += 1
    return c


def phi_beta(l: int, beta: np.ndarray, chi: float) -> np.ndarray:
    n = beta - l - 1
    lg = (math.log(math.pi) + (1 - 2 * (l + 1)) * math.log(2) + gammaln(n + 2 * l + 2)
          - gammaln(n + 1) - np.log(n + l + 1) - 2 * gammaln(l + 1))
    val = np.sin(chi) ** l * eval_gegenbauer(n, l + 1, math.cos(chi))
    return val / np.exp(0.5 * lg)


def ratio_S3(l: int, chi: float, pds: bool = False, bmax: int = 1500) -> float:
    beta = np.arange(max(3, l + 1), bmax + 1)
    w = np.ones_like(beta, float)
    if pds:
        d = molien_I(bmax)
        k = beta - 1
        w = 120.0 * d[k] / beta              # d_j/(2j+1) invariant fraction x 120 (power per mode ∝ 1/volume)
    P = 2 * math.pi ** 2 / (beta * (beta ** 2 - 1.0))
    s = np.sum(w * P * phi_beta(l, beta.astype(float), chi) ** 2)
    kmax = bmax * chi
    tail = 4 * math.pi * (quad(lambda x: spherical_jn(l, x) ** 2 / x, kmax, kmax + 400,
                                                               limit=400)[0] + 0.5 / (kmax + 400) ** 2)
    return float((s + tail) / (4 * math.pi * flat_integral(l)))


def chi_star(omk: float) -> float:
    """chi*/R_curv for a closed universe with Omega_k = omk (< 0)."""
    return CHI_STAR_OVER_DH * math.sqrt(abs(omk))


# ------------------------------------------------------------------ likelihood and S_1/2
def model_D(R: Dict[int, float]) -> Dict[int, float]:
    _, _, T = planck()
    return {l: T[l] * R.get(l, 1.0) for l in range(2, LMAX + 1)}


def m2lnL(Dm: Dict[int, float]) -> float:
    D, _, _ = planck()
    s = 0.0
    for l in range(2, LMAX + 1):
        x = D[l] / Dm[l]
        s += (2 * l + 1) * FSKY * (x - math.log(x) - 1)
    return s


def S_half(Dl: Dict[int, float], lmax: int = 100) -> float:
    r"""S_1/2 = \int_{-1}^{1/2} C(theta)^2 dcos(theta), muK^4."""
    D, _, T = planck()
    x = np.linspace(-1, 0.5, 3001)
    C = np.zeros_like(x)
    for l in range(2, lmax + 1):
        d = Dl.get(l, D[l] if Dl is None else T[l])
        Cl = 2 * math.pi * d / (l * (l + 1))
        C += (2 * l + 1) / (4 * math.pi) * Cl * eval_legendre(l, x)
    return float(np.trapezoid(C ** 2, x))


def lcdm() -> Dict[str, float]:
    D, _, T = planck()
    Dm = model_D({})
    return {"m2lnL": m2lnL(Dm), "D2_data": D[2], "D2_LCDM": T[2], "S_half_data": S_half({l: D[l] for l in range(2, 101)}),
            "S_half_LCDM": S_half({l: T[l] for l in range(2, 101)})}


def scan_T3(Ls=None) -> List[Dict]:
    Ls = Ls if Ls is not None else np.round(np.arange(1.0, 6.01, 0.25), 3)
    _, _, T = planck()
    base = m2lnL(model_D({}))
    out = []
    for L in Ls:
        R = {l: ratio_T3(l, float(L)) for l in range(2, LMAX + 1)}
        Dm = model_D(R)
        Dfull = {**{l: T[l] for l in range(2, 101)}, **Dm}
        out.append({"L_over_chi": float(L), "R2": R[2], "R3": R[3], "dchi2": m2lnL(Dm) - base, "S_half": S_half(Dfull),
                    "matched_circles": bool(L < 2.0)})
    return out


def scan_S3(omks=(-0.001, -0.003, -0.005, -0.0099, -0.013, -0.02, -0.03, -0.044), pds: bool = True) -> List[Dict]:
    _, _, T = planck()
    base = m2lnL(model_D({}))
    out = []
    for omk in omks:
        chi = chi_star(omk)
        R = {l: ratio_S3(l, chi, pds) for l in range(2, LMAX + 1)}
        Dm = model_D(R)
        Dfull = {**{l: T[l] for l in range(2, 101)}, **Dm}
        out.append({"Omega_k": omk, "chi_star": chi, "R2": R[2], "R3": R[3], "dchi2": m2lnL(Dm) - base,
                    "S_half": S_half(Dfull), "matched_circles": bool(pds and chi > math.pi / 10),
                    "Omega_k_pull_BAO": (omk - OMK_PLANCK_BAO[0]) / OMK_PLANCK_BAO[1]})
    return out


# ------------------------------------------------------------------ mode-phase interference (T^3)
def t3_phase_realisations(L: float = 2.0, nmax: int = 10, lmax: int = 6, n_real: int = 400, seed: int = 66) -> Dict:
    """Realised C_l for T^3 with (a) random mode phases (Gaussian amplitudes), (b) all phases equal ('one stone':
    coherent), observer at the symmetry point.  Coherent real modes cos(k.x) are even under x -> -x, so every odd l
    vanishes identically.  Returns realisation statistics of C_l / C_l^flat for l = 2..lmax."""
    from scipy.special import sph_harm_y
    rng = np.random.default_rng(seed)
    r = np.arange(-nmax, nmax + 1)
    X, Y, Z = np.meshgrid(r, r, r, indexing="ij")
    n = np.stack([X.ravel(), Y.ravel(), Z.ravel()], 1)
    n = n[(np.abs(n).sum(1) > 0)]
    k = 2 * math.pi * np.linalg.norm(n, axis=1) / L
    th = np.arccos(np.clip(n[:, 2] / np.linalg.norm(n, axis=1), -1, 1))
    ph = np.arctan2(n[:, 1], n[:, 0])
    amp = np.sqrt(2 * math.pi ** 2 / k ** 3 / L ** 3)                      # rms per mode: P(k)/V (A = 1)
    out = {}
    for l in range(2, lmax + 1):
        jl = spherical_jn(l, k)
        Ylm = np.array([sph_harm_y(l, m, th, ph) for m in range(-l, l + 1)])   # (2l+1, Nk)
        base = 4 * math.pi * (1j) ** l * jl * amp
        # complex Gaussian amplitudes with zeta_{-k} = zeta_k^* (real field): use full set, field real part
        Cr = []
        for _ in range(n_real):
            z = (rng.normal(size=len(k)) + 1j * rng.normal(size=len(k))) / math.sqrt(2)
            alm = (Ylm.conj() * (base * z)).sum(1)
            Cr.append(np.mean(np.abs(alm) ** 2) / (4 * math.pi * flat_integral(l)))
        z0 = np.ones(len(k))
        alm0 = (Ylm.conj() * (base * z0)).sum(1)
        # the n-set contains both k and -k, so z = 1 gives the real field sum amp cos(k.x): even, cubic-invariant
        C0 = np.mean(np.abs(alm0) ** 2) / (4 * math.pi * flat_integral(l))
        Cr = np.array(Cr)
        out[l] = {"random_mean": float(Cr.mean()), "random_std": float(Cr.std()), "ensemble_ratio": ratio_T3(l, L),
                  "coherent": float(C0)}
    return out


def report() -> Dict[str, object]:
    t3 = scan_T3()
    pds = scan_S3(pds=True)
    s3 = scan_S3(pds=False)
    best_t3 = min(t3, key=lambda r: r["dchi2"])
    best_pds = min(pds, key=lambda r: r["dchi2"])
    return {"LCDM": lcdm(), "T3": t3, "PDS": pds, "S3": s3, "best_T3": best_t3, "best_PDS": best_pds,
            "phases_T3_L2": t3_phase_realisations(),
            "PDS_first_modes_beta": [int(k + 1) for k in np.nonzero(molien_I(60))[0]]}
