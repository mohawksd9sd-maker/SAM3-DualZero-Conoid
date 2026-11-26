"""Doc 74: "sound from the banks" -- Shawn Dykes's time-as-medium sound ideas, tested (exploratory).

Originator of the ideas: Shawn Dykes (26 Nov 2026).  Dual-Zero untouched.

 S1  sound drives the ripples INWARD from the banks (boundary) on all sides, not a central stone.
     Toy model: driven Helmholtz equation in a bounded domain (sphere, cube) with in-phase boundary drive.
     Derived signatures: focusing at the centre, symmetric-only mode selection, axisymmetric sky for an
     off-focus observer, even-parity dominance for an observer at the focus.  Tested on Planck PR3 SMICA
     (+ WMAP 9 ILC) low multipoles: axisymmetry / planarity / common axis, parity ratio, focus-spot search.
 S2  one original frequency: line (pure tone) and harmonic-comb primordial spectra through CAMB transfer
     functions vs Planck 2018 TT; localized-bump limits.
 S3  changing frequency (chirp, "let there be light"): stationary-phase map from a drive sweep to the
     primordial spectrum -> n_s, running; a parametric spoken-phrase model -> Planck TT chi^2.
 S4  Penrose / CCC low-variance rings re-run on Planck SMICA (doc 71 used WMAP only) + a simple
     Hawking-point (annulus-variance) count.
"""
from __future__ import annotations

import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "time_medium"))
import time_medium as tm  # noqa: E402

DATA = os.path.join(HERE, "data")
THEORY = os.path.join(tm.PLANCK, "COM_PowerSpect_CMB-base-plikHM-TTTEEE-lowl-lowE-lensing-minimum-theory_R3.01.txt")
OBS_TT = os.path.join(tm.PLANCK, "COM_PowerSpect_CMB-TT-full_R3.01.txt")


# ============================================================ S1a: toy driven cavity

def sphere_inphase_solution(kR: float, gamma: float = 0.0, n: int = 400):
    """In-phase drive Phi(R)=1 on a sphere: Phi(r) = j0(k r)/j0(k R) (k -> k(1+i gamma) for damping).
    Returns r/R grid, |Phi|, centre gain |Phi(0)/Phi(R)| = |kR/sin kR|."""
    k = kR * (1 + 1j * gamma)
    x = np.linspace(0, 1, n)
    j0 = lambda z: np.where(np.abs(z) < 1e-12, 1.0 + 0j, np.sin(z) / np.where(np.abs(z) < 1e-12, 1, z))
    phi = j0(k * x) / j0(k)
    return x, np.abs(phi), float(np.abs(phi[0]))


def cube_inphase_fd(kL: float, N: int = 41, gamma: float = 0.02):
    """Finite-difference solve of (lap + k^2) Phi = 0 in the cube [-1,1]^3 (half-width L=1) with Phi = 1 on all
    six faces (sound driven in phase from every bank).  Returns grid and complex Phi (N^3 incl. boundary)."""
    import scipy.sparse as sp
    import scipy.sparse.linalg as spl
    h = 2.0 / (N - 1)
    n = N - 2
    k2 = (kL * (1 + 1j * gamma)) ** 2
    e = np.ones(n)
    D = sp.diags([e[:-1], -2 * e, e[:-1]], [-1, 0, 1]) / h ** 2
    I = sp.identity(n)
    A = (sp.kron(sp.kron(D, I), I) + sp.kron(sp.kron(I, D), I) + sp.kron(sp.kron(I, I), D)).tocsr().astype(complex)
    A = A + k2 * sp.identity(n ** 3)
    # boundary value 1 enters as -sum of neighbouring boundary values / h^2
    b = np.zeros((n, n, n))
    b[0, :, :] += 1; b[-1, :, :] += 1; b[:, 0, :] += 1; b[:, -1, :] += 1; b[:, :, 0] += 1; b[:, :, -1] += 1
    b = -b.ravel() / h ** 2
    sol = spl.spsolve(A.tocsc(), b.astype(complex))
    Phi = np.ones((N, N, N), dtype=complex)
    Phi[1:-1, 1:-1, 1:-1] = sol.reshape(n, n, n)
    g = np.linspace(-1, 1, N)
    return g, Phi


def sky_multipoles_from_field(g, Phi, centre, radius, nside=32, lmax=12):
    """Sample a 3-D field on a sphere (the observer's 'last-scattering sphere') and return normalized C_ell."""
    import healpy as hp
    from scipy.ndimage import map_coordinates
    v = np.array(hp.pix2vec(nside, np.arange(hp.nside2npix(nside))))
    pts = np.asarray(centre)[:, None] + radius * v
    idx = (pts - g[0]) / (g[1] - g[0])
    re = map_coordinates(Phi.real, idx, order=3)
    im = map_coordinates(Phi.imag, idx, order=3)
    out = {}
    for name, m in (("re", re), ("im", im)):
        cl = hp.anafast(m, lmax=lmax)
        tot = np.sum(cl[1:] * (2 * np.arange(1, lmax + 1) + 1))
        out[name] = (cl * (2 * np.arange(lmax + 1) + 1) / max(tot, 1e-300)).tolist()   # fraction of anisotropic power
    return out


def offcentre_sphere_multipoles(kd: float, kr: float, lmax: int = 12):
    """Uniform in-phase drive in a sphere, observer at distance d from the focus, LSS radius r:
    Phi = j0(k|x0 + r n|) = sum_l (2l+1) j_l(kd) j_l(kr) P_l(cos) -> only m = 0 about the focus axis.
    Returns fraction of anisotropic power per ell."""
    from scipy.special import spherical_jn
    L = np.arange(lmax + 1)
    a2 = ((2 * L + 1) * spherical_jn(L, kd) * spherical_jn(L, kr)) ** 2 / (2 * L + 1)   # (2l+1) C_l ~ (2l+1)^2 ... /(2l+1)
    w = a2.copy()
    w[0] = 0
    return (w / w.sum()).tolist()


# ============================================================ S1b: low-ell statistics on maps

def lowell_alm(m, lmax=10, nside_lo=64, mask=None):
    import healpy as hp
    if hp.get_nside(m) != nside_lo:
        m = hp.ud_grade(m, nside_lo)
    if mask is not None:
        m = np.where(mask > 0, m, 0.0)
    m = hp.remove_dipole(m) if mask is None else m
    return hp.map2alm(m, lmax=lmax, iter=3, use_pixel_weights=False)


def _Lmats(l):
    """Angular-momentum matrices in the complex Y_lm basis, m = -l..l."""
    m = np.arange(-l, l + 1)
    Lz = np.diag(m).astype(complex)
    cp = np.sqrt(l * (l + 1) - m[:-1] * (m[:-1] + 1))
    Lp = np.diag(cp, -1).astype(complex)          # L+ |m> = c |m+1>
    Lm = Lp.conj().T
    Lx = 0.5 * (Lp + Lm)
    Ly = -0.5j * (Lp - Lm)
    return Lx, Ly, Lz


def full_m_vector(alm, l, lmax):
    import healpy as hp
    a = np.zeros(2 * l + 1, dtype=complex)
    for mm in range(0, l + 1):
        v = alm[hp.Alm.getidx(lmax, l, mm)]
        a[l + mm] = v
        if mm > 0:
            a[l - mm] = (-1) ** mm * np.conj(v)
    return a


def ell_stats(alm, lmax, axis_grid):
    """Per ell: planarity P = max_n <(n.L)^2>/(l^2 |a|^2) (=1: all power in |m|=l), with its axis;
    axisymmetry f0(n) = fraction of power in m = 0 about n, maximised over n, with its axis."""
    import healpy as hp
    out = {}
    f0maps = {}
    for l in range(2, lmax + 1):
        a = full_m_vector(alm, l, lmax)
        nrm = np.vdot(a, a).real
        Ls = _Lmats(l)
        Aij = np.array([[np.vdot(a, (Ls[i] @ Ls[j] + Ls[j] @ Ls[i]) @ a).real / 2 for j in range(3)] for i in range(3)])
        w, V = np.linalg.eigh(Aij)
        P = w[-1] / (l * l * nrm)
        # m = 0 power about n: |a'_l0|^2 = 4 pi/(2l+1) |sum_m a_lm Y_lm(n)|^2
        sub = np.zeros(hp.Alm.getsize(l), dtype=complex)
        for mm in range(0, l + 1):
            sub[hp.Alm.getidx(l, l, mm)] = alm[hp.Alm.getidx(lmax, l, mm)]
        T = hp.alm2map(sub, axis_grid, lmax=l)
        f0 = 4 * np.pi * T ** 2 / ((2 * l + 1) * nrm)
        f0maps[l] = f0
        out[l] = {"planarity": float(P), "axis_planar": V[:, -1].tolist(), "f0_max": float(f0.max()),
                  "axis_f0": [float(x) for x in hp.pix2vec(axis_grid, int(np.argmax(f0)))]}
    return out, f0maps


def common_axis_stats(f0maps, lrange):
    """Focus prediction: all multipoles axisymmetric about ONE axis -> S = max_n mean_l f0_l(n)."""
    S = np.mean([f0maps[l] for l in lrange], axis=0)
    return float(S.max()), int(np.argmax(S))


def axis_angle(u, v):
    return float(np.degrees(np.arccos(min(1.0, abs(np.dot(u, v)) / (np.linalg.norm(u) * np.linalg.norm(v))))))


def parity_ratio(D, ell, lmax):
    s = (ell >= 2) & (ell <= lmax)
    e = s & (ell % 2 == 0)
    o = s & (ell % 2 == 1)
    return float(np.mean(D[e]) / np.mean(D[o]))


# ============================================================ S1c: focus / concentric j0 spot search

def focus_filter_matrix(nside, mask, ncent_nside=16, kappas=(15, 25, 40, 60, 90), theta_max_deg=25.0, min_cov=0.7):
    """Sparse operator: map -> least-squares amplitude of a concentric sinc(kappa*theta) profile (mean removed)
    in a disc of radius theta_max about each centre.  sinc(kappa theta) is the projection of a focus j0(k s)
    onto the last-scattering sphere when the focus lies on it (kappa = k r_LS)."""
    import healpy as hp
    import scipy.sparse as sp
    cvec = np.array(hp.pix2vec(ncent_nside, np.arange(hp.nside2npix(ncent_nside)))).T
    rows, cols, vals, meta = [], [], [], []
    r = 0
    full_n = len(hp.query_disc(nside, cvec[0], math.radians(theta_max_deg)))
    for ci, v in enumerate(cvec):
        if mask[hp.vec2pix(nside, *v)] <= 0:
            continue
        idx = hp.query_disc(nside, v, math.radians(theta_max_deg))
        idx = idx[mask[idx] > 0]
        if len(idx) < min_cov * full_n:
            continue
        th = np.arccos(np.clip(np.array(hp.pix2vec(nside, idx)).T @ v, -1, 1))
        for kap in kappas:
            t = np.sinc(kap * th / np.pi)
            t = t - t.mean()
            w = t / np.dot(t, t)
            rows += [r] * len(idx); cols += idx.tolist(); vals += w.tolist()
            meta.append((ci, kap))
            r += 1
    M = sp.csr_matrix((vals, (rows, cols)), shape=(r, hp.nside2npix(nside)))
    return M, meta


# ============================================================ S2: tones through CAMB transfer

def theory_cl(lmax):
    th = np.loadtxt(THEORY)
    cl = np.zeros(lmax + 1)
    L = th[:, 0].astype(int)
    s = L <= lmax
    cl[L[s]] = th[s, 1] * 2 * np.pi / (L[s] * (L[s] + 1))
    return cl


def gauss_lnk(k, k0, w):
    return np.exp(-0.5 * (np.log(k / k0) / w) ** 2)


def fit_shape(fc, shape_P, D, sig, ell, extra_cols=()):
    """Best-fit amplitude for D_ell = A * T(shape) (+ optional extra templates); returns chi2, A."""
    T = fc.lensed(fc.K @ shape_P)[ell]
    cols = [T] + list(extra_cols)
    X = np.stack(cols, 1) / sig[:, None]
    c, *_ = np.linalg.lstsq(X, D / sig, rcond=None)
    r = D / sig - X @ c
    return float(r @ r), c


# ============================================================ S3: chirps

def chirp_spectrum_stationary_phase(t, omega, amp):
    """Stationary-phase spectrum of s(t) = A(t) cos(phi), omega = dphi/dt:
    |S(omega)|^2 ~ pi A^2 / (2 |d omega/dt|); per ln(omega): omega |S|^2.  Returns (omega, power per ln omega)
    on the monotonic sweep."""
    wd = np.gradient(omega, t)
    return omega, omega * np.pi * amp ** 2 / (2 * np.abs(wd))


def ns_running_fit(k, P, kmin=0.005, kmax=0.2, kp=0.05):
    s = (k >= kmin) & (k <= kmax)
    x = np.log(k[s] / kp)
    c = np.polyfit(x, np.log(P[s]), 2)
    return {"n_s": float(1 + c[1]), "alpha_s": float(2 * c[0])}


def speech_phrase(fs=16000, seed=0):
    """Parametric model of a male voice saying 'let there be light' (ASSUMED, not a recording):
    syllables (onset s, duration s, F0 start/end Hz): let .00 .17 125->120; there .21 .22 122->112;
    be .47 .16 115->110; light .67 .38 150->85 (pitch accent then fall); 40-60 ms gaps; 1.05 s total.
    Voiced source = harmonics of F0 with -12 dB/oct tilt, shaped by fixed vowel formants per syllable."""
    rng = np.random.default_rng(seed)
    syl = [(0.00, 0.17, 125, 120, (530, 1840, 2480)),   # /E/
           (0.21, 0.22, 122, 112, (530, 1840, 2480)),   # /E@/
           (0.47, 0.16, 115, 110, (270, 2290, 3010)),   # /i/
           (0.67, 0.38, 150, 85, (730, 1090, 2440))]    # /aI/ start
    T = 1.10
    t = np.arange(int(T * fs)) / fs
    s = np.zeros_like(t)
    f0_track = np.full_like(t, np.nan)
    env_track = np.zeros_like(t)
    for (t0, d, fa, fb, F) in syl:
        sel = (t >= t0) & (t < t0 + d)
        tt = (t[sel] - t0) / d
        f0 = fa + (fb - fa) * tt + (25 * np.sin(np.pi * tt) if fb < fa - 30 else 0)
        ph = 2 * np.pi * np.cumsum(f0) / fs
        env = np.sin(np.pi * np.clip(tt, 0, 1)) ** 0.6
        sig = np.zeros(sel.sum())
        for h in range(1, 40):
            fh = h * f0
            g = sum(1.0 / (1 + ((fh - Fi) / (0.08 * Fi + 60)) ** 2) for Fi in F) * h ** -2.0
            sig += g * np.cos(h * ph + rng.uniform(0, 2 * np.pi)) * (fh < fs / 2)
        s[sel] += env * sig
        f0_track[sel] = f0
        env_track[sel] = env
    return t, s, f0_track, env_track
