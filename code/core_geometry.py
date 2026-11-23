#!/usr/bin/env python3
"""Core conoid geometry: induced metric, curvature, C4, C0, channel monotonicity.

Every function here is used by the reproducibility script and by pytest.
No experimental input. ell0=1 is the unit-metric convention of the core paper.
"""
from __future__ import annotations

import math
from typing import Callable, Tuple

import numpy as np
from scipy.integrate import quad
from scipy.linalg import eigh_tridiagonal

# Locked embedding: r(u,v) = (u cos v, u sin v, ell0 sin(2v))
# Core paper / doc 35.


def induced_metric_symbolic() -> dict:
    """Exact induced metric of the locked embedding, via sympy.

    r(u,v) = (u cos v, u sin v, ell0 sin(2v))
    => g_uu = 1, g_uv = 0, g_vv = u^2 + 4 ell0^2 cos^2(2v).
    """
    import sympy as sp

    u, v, ell = sp.symbols("u v ell", real=True, positive=True)
    r = sp.Matrix([u * sp.cos(v), u * sp.sin(v), ell * sp.sin(2 * v)])
    ru, rv = sp.diff(r, u), sp.diff(r, v)
    guu = sp.simplify(ru.dot(ru))
    guv = sp.simplify(ru.dot(rv))
    gvv = sp.simplify(rv.dot(rv))
    expected = u**2 + 4 * ell**2 * sp.cos(2 * v) ** 2
    return {
        "g_uu": guu,
        "g_uv": guv,
        "g_vv": gvv,
        "g_uu_is_1": guu == 1,
        "g_uv_is_0": guv == 0,
        "g_vv_matches": sp.simplify(gvv - expected) == 0,
        "tip_coefficient": 4,
    }


def induced_metric_coeff() -> dict:
    """Coefficient of ell0^2 cos^2(2v) in g_vv, which must be 4."""
    s = induced_metric_symbolic()
    return {
        "g_uu": 1.0,
        "g_uv": 0.0,
        "g_vv_formula": "u^2 + 4*ell0^2*cos^2(2v)",
        "tip_coefficient": 4,
        "symbolic_ok": bool(s["g_uu_is_1"] and s["g_uv_is_0"] and s["g_vv_matches"]),
    }


def curvature_identity_symbolic() -> bool:
    """Exact identity K = -f_uu/f = -4 ell0^2 cos^2(2v) / f^4."""
    import sympy as sp

    u, v, ell = sp.symbols("u v ell", real=True, positive=True)
    f = sp.sqrt(u**2 + 4 * ell**2 * sp.cos(2 * v) ** 2)
    K = sp.simplify(-sp.diff(f, u, 2) / f)
    closed = -4 * ell**2 * sp.cos(2 * v) ** 2 / f**4
    return sp.simplify(K - closed) == 0


def f_metric(u: float, v: float, ell0: float = 1.0) -> float:
    return math.sqrt(u * u + 4.0 * ell0 * ell0 * math.cos(2.0 * v) ** 2)


def has_c4_isometry(n_samples: int = 200, ell0: float = 1.0) -> bool:
    """f(u, v+pi/2) = f(u,v) identically on a sample, and algebraically."""
    rng = np.random.default_rng(0)
    us = rng.uniform(0.0, 5.0, n_samples)
    vs = rng.uniform(0.0, 2.0 * math.pi, n_samples)
    a = np.array([f_metric(float(u), float(v), ell0) for u, v in zip(us, vs)])
    b = np.array([f_metric(float(u), float(v + 0.5 * math.pi), ell0) for u, v in zip(us, vs)])
    return bool(np.allclose(a, b, rtol=0, atol=1e-14))


def c4_is_not_a5() -> dict:
    """A5 as a continuous isometry group of f is false: f is not invariant under
    a generic rotation of v by 2pi/5 (the C5 generator of A5's icosahedral action
    on a suitable coordinate). We only need one counterexample.
    """
    u, ell0 = 0.3, 1.0
    v0 = 0.2
    f0 = f_metric(u, v0, ell0)
    f5 = f_metric(u, v0 + 2.0 * math.pi / 5.0, ell0)
    return {
        "f(v)": f0,
        "f(v+2pi/5)": f5,
        "equal": abs(f0 - f5) < 1e-12,
        "conclusion": "C5 (hence A5) is not an isometry of the locked metric",
    }


def tip_nodes(ell0: float = 1.0) -> list:
    """f=0 iff u=0 and cos(2v)=0, i.e. v = pi/4 + k*pi/2, four points on S^1."""
    return [math.pi / 4 + k * math.pi / 2 for k in range(4)]


def gaussian_curvature(u: float, v: float, ell0: float = 1.0) -> float:
    """K = -f_uu / f  for ds^2 = du^2 + f^2 dv^2, away from f=0.

    For f^2 = u^2 + 4 ell0^2 cos^2(2v) this is
    K = -4 ell0^2 cos^2(2v) / f^4
    (doc 20).
    """
    c = math.cos(2.0 * v)
    f2 = u * u + 4.0 * ell0 * ell0 * c * c
    if f2 <= 0:
        return float("nan")
    return -(4.0 * ell0 * ell0 * c * c) / (f2 * f2)


def curvature_formula_matches(n_samples: int = 80) -> bool:
    """Check K = -f_uu/f against the closed form (symbolic identity + FD)."""
    if not curvature_identity_symbolic():
        return False
    rng = np.random.default_rng(1)
    for _ in range(n_samples):
        u = float(rng.uniform(0.3, 4.0))
        v = float(rng.uniform(0.0, 2.0 * math.pi))
        if abs(math.cos(2 * v)) < 0.05:
            continue
        # h=1e-6 is below double-precision for the second derivative
        h = 1e-5
        fuu = (f_metric(u + h, v) - 2 * f_metric(u, v) + f_metric(u - h, v)) / h**2
        K_fd = -fuu / f_metric(u, v)
        K_ex = gaussian_curvature(u, v)
        if abs(K_fd - K_ex) > 1e-5 * (1 + abs(K_ex)):
            return False
    return True


def angular_integrand_I(u: float, ell0: float = 1.0, n_v: int = 8000) -> float:
    """I(u) = ∫_0^{2π} (f(u,v) - u) dv, with f at this ell0.

    The integrand is 2π-periodic. A composite trapezoid rule on a uniform
    grid is spectrally accurate away from u=0 and still robust at u=0,
    where f(0,v)=2 ell0 |cos(2v)| has four kinks.
    """
    if u <= 0.0:
        return 8.0 * ell0
    a2 = 4.0 * ell0 * ell0
    v = np.linspace(0.0, 2.0 * math.pi, n_v, endpoint=False)
    return float(np.sum(np.sqrt(u * u + a2 * np.cos(2.0 * v) ** 2) - u) * (2.0 * math.pi / n_v))


def C0_finite_part(U: float = 400.0, ell0: float = 1.0) -> float:
    """C0(U) = ∫_0^U I(u) du - 2π log U, which converges as U→∞.

    The core paper subtracts 2π log(U+1); the two prescriptions have the same
    limit because log(U+1)-log U → 0. We use log U.
    """
    if ell0 != 1.0:
        # f(u,v;ell0) = ell0 * f(u/ell0, v; 1), so the unit-metric C0 is the
        # natural one. Callers should pass ell0=1.
        raise ValueError("C0_finite_part is defined on the unit metric ell0=1")

    part1, _ = quad(angular_integrand_I, 0.0, 1.0, epsabs=1e-10, limit=200)
    part2, _ = quad(
        lambda u: angular_integrand_I(u) - 2.0 * math.pi / u,
        1.0,
        U,
        epsabs=1e-10,
        limit=500,
    )
    # ∫_0^U I - 2π log U = part1 + (∫_1^U (I-2π/u) + 2π log U) - 2π log U
    return float(part1 + part2)


# Converged value from U=2000..5000 (November 2026 audit). The core paper's
# earlier band 4.43--4.45 does not reproduce.
C0_CONVERGED = 4.3551723
C0_PAPER_BAND = (4.43, 4.45)


def ground_energy_radial(m: float, U: float = 20.0, N: int = 800, eps: float = 1e-6) -> float:
    """Lowest eigenvalue of H_m = -d²/du² + m²/(u+eps)² on (0,U), Dirichlet.

    This is a numerical check of variational monotonicity, not a replacement
    for the analytic argument. The m=0 limit-circle issue is avoided by the
    cutoff eps and Dirichlet at both ends; treat m=0 as indicative only.
    """
    du = U / (N + 1)
    us = (np.arange(1, N + 1, dtype=float)) * du
    diag = 2.0 / du**2 + (m * m) / (us + eps) ** 2
    off = np.full(N - 1, -1.0 / du**2)
    evals = eigh_tridiagonal(diag, off, select="i", select_range=(0, 0), check_finite=False)
    return float(evals[0][0])


def omega0_from_radius(R: float, D_bridge: float = 2.0 * math.pi / 12.0) -> float:
    return (R / D_bridge) ** (4.0 / 13.0)


def natural_curvature_radii(ell0: float = 1.0) -> dict:
    """Standard readings of R_curvature at the curvature maximum (u=0, |cos(2v)|=1).

    |K|_max = 1/(4 ell0^2). None of these, with D=2π/12, yields ω0=0.927
    under (R/D)^{4/13}.
    """
    Kmax = 1.0 / (4.0 * ell0 * ell0)
    D = 2.0 * math.pi / 12.0
    cands = {
        "1/|K|_max": 1.0 / Kmax,
        "1/sqrt(|K|_max)": 1.0 / math.sqrt(Kmax),
        "ell0": ell0,
        "2*ell0": 2.0 * ell0,
    }
    out = {}
    for name, R in cands.items():
        out[name] = {
            "R": R,
            "R_over_D": R / D,
            "omega0_if_4_13": omega0_from_radius(R, D),
        }
    # Inverse: what R would be required
    target = 0.927
    RD = target ** (13.0 / 4.0)
    out["required_for_0.927"] = {"R_over_D": RD, "R": RD * D, "omega0": target}
    return out
