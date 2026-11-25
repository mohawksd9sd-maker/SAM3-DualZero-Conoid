"""Doc 71: "time as a medium" -- falsifiable versions tested against published data (exploratory).

Dual-Zero untouched.  Six concrete versions of Shawn's picture (time as a pond-like medium whose
"banks" reflect the creation ripples back):

 T1  reflecting past/initial-time boundary -> oscillations in the primordial spectrum
     (mirror at conformal time tau_b: linear oscillations cos(2 k tau_b + phi), omega_lin = 2 k* tau_b;
      reflecting boundary at a fixed physical energy ("new-physics hypersurface"): log oscillations).
     Fitted to the Planck 2018 unbinned TT spectrum (COM_PowerSpect_CMB-TT-full_R3.01), diagonal
     Gaussian likelihood, CAMB transfer functions, look-elsewhere from Gaussian simulations.
 T2  CCC-style concentric low-variance rings: ring statistic on the WMAP 9-yr ILC map (KQ85 mask)
     vs Gaussian simulations.
 T3  GW echoes from a reflecting membrane near horizons: Abedi-Dykaar-Afshordi delay formula,
     compared with published searches.
 T4  time as a dispersive medium: GW170817 / GRB 170817A speed, Fermi/LHAASO GRB dispersion,
     GWTC-3 graviton-mass bound -> bounds on a refractive index of time.
 T5  reflection off a future time boundary (crunch / rip): background-cosmology check.
 T6  refractive index varying with cosmic epoch -> alpha variation (clocks, Oklo, quasars, CMB).
"""

from __future__ import annotations

import math
import os
from typing import Dict, List

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PLANCK = os.path.join(HERE, "..", "two_loop_pati_salam", "data")
KSTAR = 0.05  # Mpc^-1, Planck 2018 X pivot for the feature models

# ------------------------------------------------------------------ physical constants
G_SUN_S = 4.925491e-6        # G M_sun / c^3 in s
G_SUN_M = 1476.625           # G M_sun / c^2 in m
L_P = 1.616255e-35           # m
E_PL_GEV = 1.220890e19       # GeV
H_EV_S = 4.135667696e-15     # eV s
YR_S = 3.15576e7


# ================================================================== T1: CMB oscillations

def planck_tt(lmax: int = 2500):
    d = np.loadtxt(os.path.join(PLANCK, "COM_PowerSpect_CMB-TT-full_R3.01.txt"))
    d = d[d[:, 0] <= lmax]
    ell = d[:, 0].astype(int)
    sig = 0.5 * (d[:, 2] + d[:, 3])
    return ell, d[:, 1], sig


def camb_setup(kb: float = 2.0):
    import camb
    p = camb.set_params(H0=67.32, ombh2=0.022383, omch2=0.12011, mnu=0.06, omk=0, tau=0.0543,
                        As=2.101e-9, ns=0.96605, lmax=2600, lens_potential_accuracy=1)
    p.set_accuracy(AccuracyBoost=1.0, lSampleBoost=50)
    p.Accuracy.IntkAccuracyBoost = kb
    p.Accuracy.SourcekAccuracyBoost = kb
    return p, camb.get_transfer_functions(p)


def camb_dl(res, fac=None, ns=0.96605, As=2.101e-9):
    from camb import initialpower
    k = np.logspace(-5.5, 0.7, 40000)
    P = As * (k / KSTAR) ** (ns - 1) * (fac(k) if fac is not None else 1.0)
    ip = initialpower.SplinedInitialPower()
    ip.set_scalar_table(k, P)
    ip.effective_ns_for_nonlinear = ns
    res.power_spectra_from_transfer(ip)
    return res.get_cmb_power_spectra(CMB_unit="muK")["total"][:, 0]


def feature(kind: str, omega: float, phase: float):
    if kind == "lin":
        return lambda k: np.cos(omega * k / KSTAR + phase)
    return lambda k: np.cos(omega * np.log(k / KSTAR) + phase)


EPS = 0.03


def templates(kind: str, omegas, res=None, D0=None, ell=None):
    """Linear response of D_ell to P -> P (1 + EPS cos(...)) and (1 + EPS sin(...)), per unit amplitude."""
    out = []
    for w in omegas:
        fc, fs = feature(kind, w, 0.0), feature(kind, w, -math.pi / 2)
        Dc = camb_dl(res, lambda k: 1 + EPS * fc(k))
        Ds = camb_dl(res, lambda k: 1 + EPS * fs(k))
        out.append(np.stack([(Dc[ell] - D0[ell]) / EPS, (Ds[ell] - D0[ell]) / EPS]))
    return np.array(out)


def _basis(cols, sig):
    X = np.stack(cols, axis=1) / sig[:, None]
    q, _ = np.linalg.qr(X)
    return q


def scan_chi2(D, sig, base_cols, tmpl):
    """Delta chi^2(omega) = chi^2(no feature) - chi^2(best A_c, A_s); nuisance = base_cols (amplitude, tilt)."""
    r = D / sig
    q0 = _basis(base_cols, sig)
    chi0 = r @ r - np.sum((q0.T @ r) ** 2)
    dchi, amp = [], []
    for T in tmpl:
        q = _basis(list(base_cols) + [T[0], T[1]], sig)
        chi = r @ r - np.sum((q.T @ r) ** 2)
        dchi.append(chi0 - chi)
        X = np.stack(list(base_cols) + [T[0], T[1]], axis=1) / sig[:, None]
        c, *_ = np.linalg.lstsq(X, r, rcond=None)
        amp.append((float(c[-2]), float(c[-1])))
    return np.array(dchi), amp, float(chi0)


def lee_sims(sig, base_cols, tmpl, nsim=1000, seed=71):
    """Max Delta chi^2 over the frequency grid for Gaussian noise realisations of the null model."""
    rng = np.random.default_rng(seed)
    R = rng.standard_normal((len(sig), nsim))      # whitened residuals of the null model
    q0 = _basis(base_cols, sig)
    base = np.sum((q0.T @ R) ** 2, axis=0)
    best = np.full(nsim, -np.inf)
    for T in tmpl:
        q = _basis(list(base_cols) + [T[0], T[1]], sig)
        best = np.maximum(best, np.sum((q.T @ R) ** 2, axis=0) - base)
    return best


# ================================================================== T2: ring statistic

def ring_geometry(nside: int, mask, ncent_nside: int = 16, radii=None, width: float = 1.0, min_cov: float = 0.7):
    import healpy as hp
    radii = np.arange(2.5, 20.0, 1.0) if radii is None else radii
    cpix = np.arange(hp.nside2npix(ncent_nside))
    cvec = np.array(hp.pix2vec(ncent_nside, cpix)).T
    good = mask[hp.vec2pix(nside, *cvec.T)] > 0
    geo = []
    for v in cvec[good]:
        idx = hp.query_disc(nside, v, math.radians(radii[-1] + width / 2))
        idx = idx[mask[idx] > 0]
        ang = np.degrees(np.arccos(np.clip(np.array(hp.pix2vec(nside, idx)).T @ v, -1, 1)))
        lab = np.full(len(idx), -1)
        for i, r in enumerate(radii):
            lab[(ang >= r - width / 2) & (ang < r + width / 2)] = i
        sel = lab >= 0
        full = np.array([len(hp.query_disc(nside, v, math.radians(r + width / 2))) -
                         len(hp.query_disc(nside, v, math.radians(r - width / 2))) for r in radii])
        geo.append((idx[sel], lab[sel], full))
    return radii, geo


def ring_sigmas(m, radii, geo, min_cov: float = 0.7):
    nr = len(radii)
    S = np.full((len(geo), nr), np.nan)
    for c, (idx, lab, full) in enumerate(geo):
        x = m[idx]
        n = np.bincount(lab, minlength=nr)
        s1 = np.bincount(lab, x, minlength=nr)
        s2 = np.bincount(lab, x * x, minlength=nr)
        ok = n >= min_cov * full
        with np.errstate(invalid="ignore", divide="ignore"):
            v = s2 / n - (s1 / n) ** 2
        S[c, ok] = np.sqrt(np.maximum(v[ok], 0))
    return S


def ring_stats(S, drop_uK: float = 15.0) -> Dict[str, float]:
    """GP-style: a ring is 'low' if its sigma is >= drop below the all-centre mean at that radius;
    families = centres with >= 3 low rings."""
    mu = np.nanmean(S, axis=0)
    low = S < (mu - drop_uK)
    nlow = np.sum(low, axis=1)
    z = (S - mu) / np.nanstd(S, axis=0)
    return {"n_low": float(np.sum(low)), "n_family3": float(np.sum(nlow >= 3)), "z_min": float(np.nanmin(z)),
            "n_family5": float(np.sum(nlow >= 5))}


# ================================================================== T3: GW echoes

def rmax_kerr(a: float, mu: float = 0.8) -> float:
    """Peak of the angular-momentum barrier, Abedi-Dykaar-Afshordi eq. (3), root near the photon sphere."""
    from scipy.optimize import brentq
    m2 = mu * mu

    def f(r):
        return ((1 - m2) * ((2 - m2) * r * r + 2 * (2 + m2) * r + (2 - m2)) * a ** 4
                + 4 * r * r * ((1 - m2) * r * r - 2 * r - 3 * (1 - m2)) * a * a + 2 * r ** 4 * (r - 3) ** 2)
    rp = 1 + math.sqrt(1 - a * a)
    xs = np.linspace(rp + 1e-3, 3.0, 400)
    v = [f(x) for x in xs]
    for x0, x1, v0, v1 in zip(xs[:-1], xs[1:], v[:-1], v[1:]):
        if v0 * v1 <= 0:
            return brentq(f, x0, x1)
    return 3.0


def echo_delay(M_det_msun: float, a: float, membrane_proper: float = L_P) -> float:
    """Delta t_echo (s), ADA eqs. (2)-(5): Planck-proper-length membrane outside a Kerr horizon."""
    M = M_det_msun * G_SUN_M                       # metres
    rp, rm = M * (1 + math.sqrt(1 - a * a)), M * (1 - math.sqrt(1 - a * a))
    rmax = rmax_kerr(a) * M
    dr = math.sqrt(1 - a * a) * membrane_proper ** 2 / (4 * M * (1 + math.sqrt(1 - a * a)))
    aa = (a * M) ** 2
    t = (2 * rmax - 2 * rp - 2 * dr + 2 * (rp * rp + aa) / (rp - rm) * math.log((rmax - rp) / dr)
         - 2 * (rm * rm + aa) / (rp - rm) * math.log((rmax - rm) / (rp - rm + dr)))
    return t / 299792458.0


# ================================================================== T4: dispersion

def dispersion_bounds() -> Dict[str, Dict[str, float]]:
    out = {}
    # GW170817 + GRB 170817A (LVC, Fermi-GBM, INTEGRAL, ApJL 848 L13 (2017)): -3e-15 < dv/c < +7e-16
    out["GW170817_speed"] = {"lo": -3e-15, "hi": 7e-16, "f_Hz": 100.0}
    # Fermi-LAT GRB 090510 (Vasileiou et al. PRD 87 122001 (2013)): E_QG,1 > 7.6 E_Pl (95%, subluminal)
    E = 31.0  # GeV, highest-energy photon
    out["GRB090510_linear"] = {"E_QG1_over_EPl": 7.6, "dn_at_31GeV": E / (7.6 * E_PL_GEV)}
    # LHAASO GRB 221009A (arXiv:2402.06009): E_QG,1 > 10 E_Pl; E_QG,2 > 6e-8 E_Pl
    out["GRB221009A_linear"] = {"E_QG1_over_EPl": 10.0, "dn_at_10TeV": 1e4 / (10 * E_PL_GEV)}
    # GWTC-3 (arXiv:2112.06861): m_g <= 2.42e-23 eV (90%)
    mg = 2.42e-23
    for f in (20.0, 100.0, 1000.0):
        out[f"graviton_mass_{int(f)}Hz"] = {"m_g_eV": mg, "dv_over_c": 0.5 * (mg / (H_EV_S * f)) ** 2}
    return out


# ================================================================== T5: future boundary

def future_of_universe(Om=0.315, Ok=0.0, w0=-1.0, wa=0.0, H0=67.4, amax=1e6):
    """Integrate the CPL background forward; report recollapse (crunch) or rip time in Gyr from now."""
    from scipy.integrate import solve_ivp
    Or = 9.1e-5
    Ode = 1 - Om - Ok - Or
    H0g = H0 / 977.792  # 1/Gyr

    def E2(a):
        f = a ** (-3 * (1 + w0 + wa)) * math.exp(-3 * wa * (1 - a))
        return Or / a ** 4 + Om / a ** 3 + Ok / a ** 2 + Ode * f

    # a'' = -(H0^2/2) sum (1+3w_i) Omega_i(a) a  -- use second-order form to pass turnaround
    def rhs(t, y):
        a, ad = y
        w = w0 + wa * (1 - a)
        f = a ** (-3 * (1 + w0 + wa)) * math.exp(-3 * wa * (1 - a))
        acc = -0.5 * H0g ** 2 * (2 * Or / a ** 3 + Om / a ** 2 + (1 + 3 * w) * Ode * f * a)
        return [ad, acc]

    crunch = lambda t, y: y[0] - 1e-3
    crunch.terminal = True
    big = lambda t, y: y[0] - amax
    big.terminal = True
    s = solve_ivp(rhs, (0, 1e6), [1.0, H0g * math.sqrt(E2(1.0))], events=[crunch, big], rtol=1e-8, atol=1e-12,
                  max_step=50.0)
    if s.t_events[0].size:
        return {"fate": "crunch", "t_Gyr": float(s.t_events[0][0]), "a_max": float(np.max(s.y[0]))}
    if s.t_events[1].size:
        return {"fate": "expands forever (a > 1e6)", "t_Gyr": float(s.t_events[1][0])}
    return {"fate": "undetermined within 1e6 Gyr", "t_Gyr": float(s.t[-1])}


# ================================================================== T6: alpha variation

def alpha_bounds() -> List[Dict[str, float]]:
    """Bounds on eps in Delta alpha/alpha = eps ln(1+z) (a slowly varying 'refractive index of time' coupled to EM).
    Published inputs: Lange et al. PRL 126 011102 (2021); Damour-Dyson NPB 480 37 (1996);
    Murphy et al. A&A 658 A123 (2022); Planck int. XXIV A&A 580 A22 (2015)."""
    H0_per_yr = 67.4 / 977.792 / 1e9
    rows = []
    # clocks: dalpha/dt / alpha = 1.0(1.1)e-18 /yr ; d ln(1+z)/dt = -H0 at z = 0
    rows.append({"probe": "Yb+ optical clocks (today)", "eps": -1.0e-18 / H0_per_yr, "err": 1.1e-18 / H0_per_yr,
                 "z": 0.0})
    # Oklo, 1.8-2 Gyr ago (z ~ 0.16), 95% range -0.9e-7..1.2e-7 -> central 0.15e-7, 1 sigma ~ 0.53e-7
    L = math.log(1.16)
    rows.append({"probe": "Oklo reactor (~2 Gyr ago)", "eps": 0.15e-7 / L, "err": 0.53e-7 / L, "z": 0.16})
    # quasar absorbers, z 0.6-2.4: -0.5 +- 0.5 stat +- 0.4 sys ppm  (use ln(1+z) at z ~ 1.3)
    L = math.log(2.3)
    rows.append({"probe": "quasar absorbers (ESPRESSO + 28)", "eps": -0.5e-6 / L, "err": math.hypot(0.5, 0.4) * 1e-6 / L,
                 "z": 1.3})
    L = math.log(1090.0)
    rows.append({"probe": "CMB recombination (Planck)", "eps": 3.6e-3 / L, "err": 3.7e-3 / L, "z": 1089.0})
    return rows


class FastCls:
    """Linear map P(k) -> lensed D_ell^TT from CAMB's own C_ell transfer functions (q-grid dq = 6.6e-5 Mpc^-1
    up to q ~ 0.3), checked against full CAMB runs to 0.14% (omega = 10) and 0.02% (omega = 126) of the
    template amplitude.  Lensing: camb.correlations.lensed_cls with the fiducial C_L^phiphi (linear in C_ell)."""

    def __init__(self, kb: float = 2.0):
        p, res = camb_setup(kb)
        self.D0 = camb_dl(res)
        tr = res.get_cmb_transfer_data(tp="scalar")
        self.L, self.q = tr.L, tr.q
        u = res.get_unlensed_scalar_cls(CMB_unit="muK", raw_cl=True)
        self.P0 = 2.101e-9 * (self.q / KSTAR) ** (0.96605 - 1)
        K = tr.delta_p_l_k[0] ** 2 * np.gradient(np.log(self.q))
        K *= np.median(u[self.L, 0] / (K @ self.P0))
        self.K = K
        self.clpp = res.get_lens_potential_cls(lmax=2800, raw_cl=False)[:, 0]

    def lensed(self, cl_raw):
        from camb import correlations
        arr = np.zeros((2801, 4))
        L = self.L
        arr[L, 0] = cl_raw * L * (L + 1) / (2 * np.pi)
        return correlations.lensed_cls(arr, self.clpp)[:, 0]

    def response(self, fac):
        """lensed D_ell response to P0 -> P0 (1 + fac(k)) (linear)."""
        return self.lensed(self.K @ (self.P0 * fac(self.q)))
