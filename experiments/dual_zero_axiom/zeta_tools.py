"""Special-function helpers for Dual-Zero-regulated spectral zetas.

Exploratory: not part of the locked core.  Riemann zeta and the
real-analytic Eisenstein series are standard; no new closed forms are
claimed.
"""

from __future__ import annotations

import math
from typing import Tuple

import mpmath as mp

# Working precision: enough for scans, cheap enough for tests.
mp.mp.dps = 25

TAU_I = 1j
TAU_RHO = -0.5 + 1j * math.sqrt(3.0) / 2.0
TAU_RHO_RIGHT = 0.5 + 1j * math.sqrt(3.0) / 2.0

# Singularities to avoid when evaluating spectral zetas.
# s = 1 is a genuine pole of both the Riemann zeta and the Laplacian /
# Eisenstein zetas.  s = 1/2 is an apparent singularity of the Eisenstein
# Fourier expansion.  s = 0 is a regular point of ζ, ζ_{D²}, and (after
# continuation) of ζ_Δ; the expansion is usable for small nonzero s.
FORBIDDEN_S = (0.5, 1.0)
MIN_DISTANCE_TO_FORBIDDEN = 0.04


def s_is_safe(s: float, min_distance: float = MIN_DISTANCE_TO_FORBIDDEN) -> bool:
    if s == 0.0:
        return False  # use the closed unregulated value at zero instead
    return all(abs(s - p) >= min_distance for p in FORBIDDEN_S)


def riemann_zeta(s, deriv: int = 0):
    return mp.zeta(s, derivative=deriv)


def _divisor_sigma(v, n: int):
    acc = mp.mpf(0)
    d = 1
    while d * d <= n:
        if n % d == 0:
            acc += mp.power(d, v)
            if d * d != n:
                acc += mp.power(n // d, v)
        d += 1
    return acc


def eisenstein_E(tau: complex, s, nterms: int = 40):
    """Real-analytic Eisenstein series E(τ,s) = ∑' (Im τ / |mτ+n|²)^s.

    Fourier expansion (standard; e.g. Iwaniec, *Topics in Classical
    Automorphic Forms*):

        E(τ,s) = 2 ζ(2s) y^s
               + 2√π Γ(s−1/2)/Γ(s) ζ(2s−1) y^{1−s}
               + (8 π^s / Γ(s)) y^{1/2} ∑_{N≥1} N^{s−1/2} σ_{1−2s}(N)
                     cos(2π N x) K_{s−1/2}(2π N y).

    Valid for s away from the apparent singularities {0, 1/2, 1}.
    """
    if tau.imag <= 0:
        raise ValueError("tau must lie in the upper half-plane")
    s = mp.mpf(s)
    if not s_is_safe(float(s)):
        raise ValueError(f"s={s} is too close to a pole of the expansion")
    x, y = mp.mpf(tau.real), mp.mpf(tau.imag)
    term1 = 2 * mp.zeta(2 * s) * mp.power(y, s)
    term2 = (
        2
        * mp.sqrt(mp.pi)
        * mp.gamma(s - mp.mpf("0.5"))
        / mp.gamma(s)
        * mp.zeta(2 * s - 1)
        * mp.power(y, 1 - s)
    )
    pref = 8 * mp.power(mp.pi, s) / mp.gamma(s) * mp.sqrt(y)
    acc = term1 + term2
    half = mp.mpf("0.5")
    for n in range(1, nterms + 1):
        acc += pref * (
            mp.power(n, s - half)
            * _divisor_sigma(1 - 2 * s, n)
            * mp.cos(2 * mp.pi * n * x)
            * mp.besselk(s - half, 2 * mp.pi * n * y)
        )
    return acc


def zeta_laplacian(s, tau: complex, area: float = 1.0, nterms: int = 40):
    """Spectral zeta of the flat Laplacian on a torus of area A and modulus τ.

    Eigenvalues λ_{m,n} = (4π² / A) |m + n τ|² / Im(τ) for (m,n) ≠ (0,0),
    so ζ_Δ(s) = (A / (4π²))^s E(τ, s).
    """
    if area <= 0:
        raise ValueError("area must be positive")
    return mp.power(mp.mpf(area) / (4 * mp.pi**2), s) * eisenstein_E(tau, s, nterms=nterms)


def zeta_laplacian_prime(s, tau: complex, area: float = 1.0, h=None, nterms: int = 40):
    """Numerical derivative of ζ_Δ at a safe s, using a symmetric difference."""
    s = mp.mpf(s)
    if h is None:
        h = mp.mpf("1e-8")
    # Stay away from forbidden points.
    if (not s_is_safe(float(s + h))) or (not s_is_safe(float(s - h))):
        h = mp.mpf("1e-6")
        if (not s_is_safe(float(s + h))) or (not s_is_safe(float(s - h))):
            raise ValueError(f"cannot differentiate zeta_Delta at s={s}")
    plus = zeta_laplacian(s + h, tau, area, nterms=nterms)
    minus = zeta_laplacian(s - h, tau, area, nterms=nterms)
    return (plus - minus) / (2 * h)


def zeta_D2_magnetized(s, M: int, area: float):
    """ζ_{D²}(s) = 2 M (4π M / A)^{-s} ζ(s), M > 0, s ≠ 1 (doc 49)."""
    if M <= 0 or area <= 0:
        raise ValueError("M and area must be positive")
    s = mp.mpf(s)
    alpha = 4 * mp.pi * M / area
    return 2 * M * mp.power(alpha, -s) * mp.zeta(s)


def zeta_D2_magnetized_prime(s, M: int, area: float):
    """Exact derivative of the closed form."""
    if M <= 0 or area <= 0:
        raise ValueError("M and area must be positive")
    s = mp.mpf(s)
    if abs(float(s) - 1.0) < MIN_DISTANCE_TO_FORBIDDEN:
        raise ValueError("s is too close to the pole at 1")
    alpha = 4 * mp.pi * M / area
    return 2 * M * mp.power(alpha, -s) * (
        -mp.log(alpha) * mp.zeta(s) + mp.zeta(s, derivative=1)
    )


def dz_log_det_from_zeta_prime(zp_plus, zp_minus) -> float:
    """log det_DZ(δ) = −½ · [ζ'(δ) + ζ'(−δ)] / 2.

    The overall factor −½ is the conversion from ζ_{D²} (or ζ_Δ) to
    log det' of the first-order / square-root operator as in doc 49
    for |D|, and to log det' Δ when applied to ζ_Δ (then the −½ should
    *not* be used if one wants log det' Δ = −ζ_Δ'(0); see
    `dz_log_det_laplacian`).
    """
    return float(-0.5 * 0.5 * (zp_plus + zp_minus))


def dz_log_det_abs_D(delta: float, M: int, area: float) -> float:
    """Dual-Zero-regulated log det'|D| on a magnetized torus, at shift δ."""
    if delta <= 0:
        raise ValueError("delta must be positive")
    if not s_is_safe(delta) or not s_is_safe(-delta):
        raise ValueError(f"delta={delta} is too close to a zeta pole")
    zp_p = zeta_D2_magnetized_prime(delta, M, area)
    zp_m = zeta_D2_magnetized_prime(-delta, M, area)
    return dz_log_det_from_zeta_prime(zp_p, zp_m)


def unreg_log_det_abs_D(M: int, area: float) -> float:
    """Exact unregulated value −(M/2) log(2M/A) (doc 49)."""
    if M <= 0 or area <= 0:
        raise ValueError("M and area must be positive")
    return -0.5 * M * math.log(2.0 * M / area)


def dz_log_det_laplacian(delta: float, tau: complex, area: float = 1.0) -> float:
    """Dual-Zero-regulated log det' Δ = − [ζ_Δ'(δ) + ζ_Δ'(−δ)] / 2."""
    if delta <= 0:
        raise ValueError("delta must be positive")
    if not s_is_safe(delta) or not s_is_safe(-delta):
        raise ValueError(f"delta={delta} is too close to a pole")
    zp_p = zeta_laplacian_prime(delta, tau, area)
    zp_m = zeta_laplacian_prime(-delta, tau, area)
    return float(-0.5 * (zp_p + zp_m))


def dedekind_eta(tau: complex, nterms: int = 80) -> complex:
    if tau.imag <= 0:
        raise ValueError("tau must lie in the upper half-plane")
    log_q = 2j * math.pi * tau
    log_eta = log_q / 24.0
    q = cmath_exp(log_q)
    qn = q
    one = 1.0 + 0.0j
    for _ in range(1, nterms + 1):
        log_eta += clog(one - qn)
        qn *= q
        if abs(qn) < 1e-18:
            break
    return cexp(log_eta)


def cmath_exp(z: complex) -> complex:
    import cmath

    return cmath.exp(z)


def clog(z: complex) -> complex:
    import cmath

    return cmath.log(z)


def cexp(z: complex) -> complex:
    import cmath

    return cmath.exp(z)


def ops_F(tau: complex) -> float:
    """√(Im τ) |η(τ)|²."""
    eta = dedekind_eta(tau)
    return math.sqrt(tau.imag) * (abs(eta) ** 2)


def unreg_height(tau: complex) -> float:
    """Kronecker height −log F(τ).  Smaller height means larger det' Δ."""
    return -math.log(ops_F(tau))


def unreg_log_det_proxy(tau: complex) -> float:
    """log det' Δ up to an additive constant: +log F(τ), unit area.

    det' Δ is maximised where F is maximised (OPS / Chiu, doc 49).
    """
    return math.log(ops_F(tau))


def unit_area_points() -> Tuple[complex, complex, complex]:
    return TAU_I, TAU_RHO, TAU_RHO_RIGHT
