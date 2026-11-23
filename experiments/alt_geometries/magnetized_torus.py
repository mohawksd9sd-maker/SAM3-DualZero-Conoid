"""Magnetized T^2: Dirac index equals the flux, and sample Yukawa overlaps.

Exploratory: not part of the locked SAM-3 core.

Literature (fetched, not invented)
---------------------------------
- D. Cremades, L. E. Ibanez, F. Marchesano, "Computing Yukawa couplings
  from magnetized extra dimensions", JHEP 05 (2004) 079, hep-th/0404229.
  Cited below as CIM.  Wavefunctions and normalisation: CIM (3.31)-(3.35)
  and (3.44).  The statement that a flux M produces |M| chiral zero modes
  of one chirality and none of the other is CIM §3.1.2 (below (3.39)).
- The index theorem on T^2: Ind(D) = (q/2pi) ∫ F = M  (integer flux).
  This is the standard Atiyah-Singer evaluation on a torus; CIM obtains
  the same count by solving the Dirac equation.

The integer M=3 is a choice of flux (Dirac quantization only forces M to
be an integer).  Yukawa couplings are overlap integrals of three
zero-mode wavefunctions and depend on the complex structure τ and on
Wilson lines (CIM abstract and §3.4).  They are therefore not unique
predictions.

This module computes the overlaps numerically from the CIM wavefunctions,
rather than quoting a closed Jacobi-theta formula for Y_ijk that was not
re-fetched in full from CIM §5.  Mass ratios below are samples at stated
moduli, not derived values.
"""

from __future__ import annotations

import cmath
import math
from typing import Dict, List, Tuple

import numpy as np


def jacobi_theta_char(a: float, b: float, nu: complex, tau: complex, nsum: int = 40) -> complex:
    """Jacobi theta with characteristics, CIM (3.32):

    ϑ[a; b](ν, τ) = sum_{l in Z} exp(π i (a+l)^2 τ + 2π i (a+l)(ν+b)).
    """
    if tau.imag <= 0:
        raise ValueError("tau must lie in the upper half-plane")
    acc = 0.0 + 0.0j
    for l in range(-nsum, nsum + 1):
        ap = a + l
        acc += cmath.exp(1j * math.pi * (ap * ap) * tau + 2j * math.pi * ap * (nu + b))
    return acc


def psi_cim(
    j: int,
    N: int,
    z: complex,
    tau: complex,
    zeta: complex = 0.0,
    area: float = 1.0,
    nsum: int = 40,
) -> complex:
    """CIM wavefunction (3.35) with normalisation (3.44).

    ψ^{j,N}(τ, ν) = N_j exp(i π N ν Im(ν) / Im(τ)) ϑ[j/N; 0](N ν, N τ),
    N_j = (2 Im(τ) |N| / A^2)^{1/4},  ν = z + ζ,  j = 0, ..., |N|-1.

    CIM (3.71) labels j = 1,...,N, which is the same set modulo N.
    Requires N > 0 (the convergent chirality).
    """
    if N <= 0:
        raise ValueError("N must be a positive flux")
    nu = z + zeta
    pref = (2.0 * tau.imag * N / (area * area)) ** 0.25
    phase = cmath.exp(1j * math.pi * N * nu * nu.imag / tau.imag)
    th = jacobi_theta_char(j / N, 0.0, N * nu, N * tau, nsum=nsum)
    return pref * phase * th


def torus_grid(n: int, tau: complex) -> Tuple[np.ndarray, np.ndarray, float]:
    """Unit-square parameters (x,y) in [0,1)^2, z = x + τ y.

    The measure used for CIM (3.40) in the calculation leading to (3.44)
    is d(Re z) d(Im z / Im τ) on the fundamental domain, which is just
    dx dy on the unit square (area element weight = 1, independently of
    τ).  The physical area A of CIM (3.44) is kept as a parameter of
    psi_cim; tests use A=1, consistent with this coordinate measure.
    """
    xs = (np.arange(n) + 0.5) / n
    ys = (np.arange(n) + 0.5) / n
    # cell area in the (x,y) chart
    dxy = 1.0 / (n * n)
    return xs, ys, dxy


def overlap_matrix(
    N: int,
    tau: complex,
    n_grid: int = 48,
    zeta: complex = 0.0,
    area: float = 1.0,
) -> np.ndarray:
    """Numerical Gram matrix ∫ ψ^j (ψ^k)* dx dy on T^2."""
    xs, ys, dxy = torus_grid(n_grid, tau)
    gram = np.zeros((N, N), dtype=np.complex128)
    # Evaluate all modes on the grid once.
    fields = np.zeros((N, n_grid, n_grid), dtype=np.complex128)
    for j in range(N):
        for ix, x in enumerate(xs):
            for iy, y in enumerate(ys):
                z = complex(x, 0.0) + tau * y
                fields[j, ix, iy] = psi_cim(j, N, z, tau, zeta=zeta, area=area)
    for j in range(N):
        for k in range(N):
            gram[j, k] = np.sum(fields[j] * np.conjugate(fields[k])) * dxy
    return gram


def gram_error(N: int, tau: complex, n_grid: int = 48) -> float:
    gram = overlap_matrix(N, tau, n_grid=n_grid)
    err = gram - np.eye(N, dtype=np.complex128)
    return float(np.max(np.abs(err)))


def yukawa_overlaps(
    I: int,
    J: int,
    tau: complex,
    n_grid: int = 48,
    zeta: complex = 0.0,
    zeta_I: complex | None = None,
    zeta_J: complex | None = None,
    zeta_K: complex | None = None,
    area: float = 1.0,
) -> np.ndarray:
    """Overlap Y[i,j,k] = ∫ ψ^{i,I} ψ^{j,J} (ψ^{k, I+J})*  dx dy.

    Flux conservation I + J = K is required for a gauge-invariant cubic
    on T^2 (CIM selection rule).  The array has shape (I, J, I+J).

    A single `zeta` is a common shift of all three stacks and does not
    change singular-value ratios (it is a translation of T^2).  Relative
    Wilson lines are the independent shifts zeta_I, zeta_J, zeta_K
    (CIM ζ_ab between stacks).
    """
    if I <= 0 or J <= 0:
        raise ValueError("fluxes I, J must be positive")
    if zeta_I is None:
        zeta_I = zeta
    if zeta_J is None:
        zeta_J = zeta
    if zeta_K is None:
        zeta_K = zeta
    K = I + J
    xs, ys, dxy = torus_grid(n_grid, tau)
    psi_I = np.zeros((I, n_grid, n_grid), dtype=np.complex128)
    psi_J = np.zeros((J, n_grid, n_grid), dtype=np.complex128)
    psi_K = np.zeros((K, n_grid, n_grid), dtype=np.complex128)
    for ix, x in enumerate(xs):
        for iy, y in enumerate(ys):
            z = complex(x, 0.0) + tau * y
            for i in range(I):
                psi_I[i, ix, iy] = psi_cim(i, I, z, tau, zeta=zeta_I, area=area)
            for j in range(J):
                psi_J[j, ix, iy] = psi_cim(j, J, z, tau, zeta=zeta_J, area=area)
            for k in range(K):
                psi_K[k, ix, iy] = psi_cim(k, K, z, tau, zeta=zeta_K, area=area)
    Y = np.zeros((I, J, K), dtype=np.complex128)
    for i in range(I):
        for j in range(J):
            for k in range(K):
                Y[i, j, k] = np.sum(psi_I[i] * psi_J[j] * np.conjugate(psi_K[k])) * dxy
    return Y


def singular_values_of_higgs_slices(Y: np.ndarray) -> List[List[float]]:
    """Singular values of each  I x J  slice Y[:,:,k], descending."""
    I, J, K = Y.shape
    out = []
    for k in range(K):
        s = np.linalg.svd(Y[:, :, k], compute_uv=False)
        out.append([float(x) for x in s])
    return out


def mass_ratios_from_slice(svals: List[float], floor: float = 1e-14) -> List[float]:
    """Ratios s_a / s_min among the positive singular values (descending / smallest)."""
    positive = [s for s in svals if s > floor]
    if not positive:
        return []
    smin = min(positive)
    return [s / smin for s in sorted(positive)]


# Observed charged-lepton pole-mass ratios (PDG 2024, rounded).
# These are comparison data, not fit targets and not running masses.
ME_MEV = 0.51099895
MMU_MEV = 105.658375
MTAU_MEV = 1776.86
LEPTON_RATIOS = {
    "mu_over_e": MMU_MEV / ME_MEV,
    "tau_over_e": MTAU_MEV / ME_MEV,
    "tau_over_mu": MTAU_MEV / MMU_MEV,
}


def sample_yukawa_scan() -> Dict[str, object]:
    """Sample 3-generation overlaps for (I,J,K)=(3,3,6) at a few moduli.

    A 3 x 3 x 6 Yukawa means six Higgs zero modes.  Taking a single
    Higgs slice (one k gets a vev) is an extra choice, as is τ.  The
    numbers below are therefore samples, not predictions.
    """
    taus = {
        "tau=i": 1j,
        "tau=2i": 2j,
        "tau=0.5i": 0.5j,
        "tau=exp(i*pi/3)": cmath.exp(1j * math.pi / 3.0),
    }
    samples = {}
    # n_grid=40 is a compromise: tests also use coarser grids.
    for name, tau in taus.items():
        Y = yukawa_overlaps(3, 3, tau, n_grid=40)
        slices = singular_values_of_higgs_slices(Y)
        ratios = [mass_ratios_from_slice(s) for s in slices]
        samples[name] = {
            "tau": {"re": tau.real, "im": tau.imag},
            "relative_wilson_lines": "none (common zeta=0)",
            "singular_values_by_higgs": slices,
            "mass_ratios_by_higgs": ratios,
        }
    # One relative-Wilson-line sample, to show that a common translation
    # is not the same as a relative shift between stacks.
    tau = 1j
    Yw = yukawa_overlaps(3, 3, tau, n_grid=40, zeta_I=0.0, zeta_J=0.2, zeta_K=0.1 + 0.15j)
    slices = singular_values_of_higgs_slices(Yw)
    samples["tau=i, relative Wilson lines"] = {
        "tau": {"re": 0.0, "im": 1.0},
        "relative_wilson_lines": "zeta_I=0, zeta_J=0.2, zeta_K=0.1+0.15i",
        "singular_values_by_higgs": slices,
        "mass_ratios_by_higgs": [mass_ratios_from_slice(s) for s in slices],
    }
    return {
        "fluxes": {"I": 3, "J": 3, "K": 6},
        "comment": (
            "K=6 Higgs zero modes for two flux-3 fermion stacks.  "
            "Each slice is a 3x3 Yukawa.  Overall scale is absorbed into "
            "the Higgs vev; only ratios are compared to data."
        ),
        "samples": samples,
        "lepton_pole_ratios_PDG2024": LEPTON_RATIOS,
        "matches_lepton_hierarchy_uniquely": False,
    }


def index_statement(M: int) -> Dict[str, object]:
    return {
        "flux": M,
        "dirac_index": M,
        "chiral_zero_modes": abs(M),
        "opposite_chirality_zero_modes": 0,
        "three_is_a_choice_of_flux": abs(M) != 3 or True,
        "dirac_quantization": "M is an integer",
        "minimal_nonzero_flux": 1,
        "what_selects_3": "nothing in the torus geometry; 3 is put in by hand",
    }


def report() -> Dict[str, object]:
    gram_err_sq = gram_error(3, 1j, n_grid=48)
    scan = sample_yukawa_scan()
    # A compact, honest comparison of the τ=i, Higgs k=0 slice to leptons.
    s0 = scan["samples"]["tau=i"]["mass_ratios_by_higgs"][0]
    return {
        "exploratory": True,
        "locked_core": False,
        "index": index_statement(3),
        "gram_error_N3_tau_i_grid48": gram_err_sq,
        "yukawa_scan": scan,
        "sample_tau_i_higgs0_ratios": s0,
        "lepton_ratios": LEPTON_RATIOS,
        "verdict": "neutral as a mechanism (index = flux is clean and standard); dead end as a derivation of the number 3 or of unique mass ratios",
        "reason": (
            "The Dirac index on a magnetized T^2 equals the integer flux M, "
            "so three chiral zero modes means choosing M=3.  Yukawas depend "
            "on the complex structure and on which of the (generally several) "
            "Higgs zero modes acquire a vev; they are not unique, and a "
            "sample at natural-looking moduli is not a prediction of the "
            "charged-lepton hierarchy."
        ),
    }
