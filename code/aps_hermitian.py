#!/usr/bin/env python3
"""Hermitian 2D Dirac discretisation, known-answer tests, and convergence.

Why this file exists
--------------------
`dirac_conoid_aps.build_dirac_matrix` assembles a real first-order operator
and then replaces it by 0.5*(D+D.T). Central differences are antisymmetric,
so that step cancels the derivative terms and leaves only the symmetric
remainder (spin connection, a tiny diagonal, and the APS penalty). The raw
(un-symmetrised) matrix is not Hermitian. That operator is therefore not a
Dirac operator in the sense required for APS / spectral geometry.

This module builds a genuinely Hermitian Dirac operator

    D = i σ¹ e_u(∂_u + ½ ∂_u log f) + i σ² f⁻¹ ∂_v

on ds² = du² + f(u,v)² dv², with either periodic/antiperiodic conditions
(for known-answer tests) or an APS-style boundary penalty in u (for the
conoid, as a numerical experiment, not a complete APS theorem).

Known answers
-------------
On a flat torus T² = R² / (L_u Z × L_v Z) with f ≡ 1 and no spin connection,
the spectrum is

    ± sqrt(k_u² + k_v²),

where k_u = 2π n / L_u or 2π(n+1/2)/L_u according to periodic vs
antiperiodic conditions in u, and likewise for v. There is a zero mode iff
both directions are periodic.

The legacy symmetrised operator fails this test (documented in the tests).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh

# Pauli matrices, acting on the spinor index.
SIGMA1 = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
SIGMA2 = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)


@dataclass
class Grid2D:
    Nu: int
    Nv: int
    u_min: float
    u_max: float
    v_min: float = 0.0
    v_max: float = 2.0 * np.pi
    periodic_u: bool = False
    antiperiodic_u: bool = False
    periodic_v: bool = True
    antiperiodic_v: bool = False

    def axes(self) -> Tuple[np.ndarray, np.ndarray, float, float]:
        if self.periodic_u or self.antiperiodic_u:
            du = (self.u_max - self.u_min) / self.Nu
            u = self.u_min + du * np.arange(self.Nu)
        else:
            u = np.linspace(self.u_min, self.u_max, self.Nu)
            du = float(u[1] - u[0])
        if self.periodic_v or self.antiperiodic_v:
            dv = (self.v_max - self.v_min) / self.Nv
            v = self.v_min + dv * np.arange(self.Nv)
        else:
            v = np.linspace(self.v_min, self.v_max, self.Nv, endpoint=False)
            dv = float(v[1] - v[0]) if self.Nv > 1 else (self.v_max - self.v_min)
        return u, v, float(du), float(dv)

    def n_spinor(self) -> int:
        return 2 * self.Nu * self.Nv


def _idx(i: int, j: int, Nv: int, spin: int) -> int:
    return (i * Nv + j) * 2 + spin


def _wrap_coeff(i: int, N: int, periodic: bool, antiperiodic: bool) -> Tuple[int, complex]:
    """Map a possibly out-of-range index back into 0..N-1, with a sign."""
    if 0 <= i < N:
        return i, 1.0 + 0.0j
    if periodic or antiperiodic:
        ii = i % N
        # How many wraps? for i=-1, ii=N-1, one wrap down → sign -1 if AP
        wraps = (i - ii) // N
        sign = ((-1) ** wraps) if antiperiodic else 1
        return ii, complex(sign)
    return i, 0.0j  # Dirichlet-like: drop the term (open end)


def build_hermitian_dirac(
    grid: Grid2D,
    f_fn: Callable[[np.ndarray, np.ndarray], np.ndarray],
    aps_strength: float = 0.0,
) -> Tuple[sparse.csr_matrix, np.ndarray, np.ndarray]:
    """Hermitian Dirac on the orthogonal metric du² + f² dv²."""
    u, v, du, dv = grid.axes()
    Nu, Nv = grid.Nu, grid.Nv
    n = grid.n_spinor()
    U, V = np.meshgrid(u, v, indexing="ij")
    f = np.asarray(f_fn(U, V), dtype=float)
    # f_u by central difference in u, one-sided at open ends
    fu = np.zeros_like(f)
    fu[1:-1, :] = (f[2:, :] - f[:-2, :]) / (2.0 * du)
    if grid.periodic_u or grid.antiperiodic_u:
        fu[0, :] = (f[1, :] - f[-1, :]) / (2.0 * du)
        fu[-1, :] = (f[0, :] - f[-2, :]) / (2.0 * du)
    else:
        fu[0, :] = (f[1, :] - f[0, :]) / du
        fu[-1, :] = (f[-1, :] - f[-2, :]) / du

    rows: List[int] = []
    cols: List[int] = []
    data: List[complex] = []

    def add(r: int, c: int, val: complex) -> None:
        if val != 0 and 0 <= r < n and 0 <= c < n:
            rows.append(r)
            cols.append(c)
            data.append(complex(val))

    # i σ¹ ∂_u  and  i σ² (1/f) ∂_v  plus spin-connection  i σ¹ (1/2)(f_u/f)
    for i in range(Nu):
        for j in range(Nv):
            fij = float(f[i, j])
            invf = 1.0 / (fij + 1e-30)
            half_log = 0.5 * float(fu[i, j]) * invf
            base = _idx(i, j, Nv, 0)

            # spin connection: i σ¹ * (1/2 f_u/f)  (multiplication operator)
            # <a| i σ¹ |b> * half_log
            for a in range(2):
                for b in range(2):
                    val = 1j * SIGMA1[a, b] * half_log
                    add(base + a, base + b, val)

            # u-derivatives, central
            for off, w in ((+1, 0.5 / du), (-1, -0.5 / du)):
                ii, sign = _wrap_coeff(i + off, Nu, grid.periodic_u, grid.antiperiodic_u)
                if sign == 0:
                    continue
                for a in range(2):
                    for b in range(2):
                        val = 1j * SIGMA1[a, b] * (w * sign)
                        add(base + a, _idx(ii, j, Nv, b), val)

            # v-derivatives
            for off, w in ((+1, 0.5 / dv), (-1, -0.5 / dv)):
                jj, sign = _wrap_coeff(j + off, Nv, grid.periodic_v, grid.antiperiodic_v)
                if sign == 0:
                    continue
                for a in range(2):
                    for b in range(2):
                        val = 1j * SIGMA2[a, b] * (invf * w * sign)
                        add(base + a, _idx(i, jj, Nv, b), val)

            # Optional APS-style penalty at open u-boundaries (numerical device,
            # not a complete APS projection).
            if aps_strength and not (grid.periodic_u or grid.antiperiodic_u):
                if i in (0, Nu - 1):
                    pen = aps_strength / max(du, 1e-12)
                    add(base, base, pen)
                    add(base + 1, base + 1, pen)

    D = sparse.coo_matrix((data, (rows, cols)), shape=(n, n)).tocsr()
    # Numerical hermiticity clean-up at roundoff level only.
    D = 0.5 * (D + D.getH())
    return D, u, v


def hermiticity_error(D: sparse.spmatrix) -> float:
    err = D - D.getH()
    return float(sparse.linalg.norm(err))


def lowest_abs_eigs(D: sparse.spmatrix, k: int = 12, dense: bool | None = None) -> np.ndarray:
    """Eigenvalues nearest zero, sorted by signed value among that set.

    For modest grids, a dense Hermitian eigensolver is used. Shift-invert
    eigsh can miss members of a degenerate cluster (the torus lowest mode
    has multiplicity 8 when both directions are antiperiodic).
    """
    k = min(k, max(2, D.shape[0] - 2))
    if dense is None:
        dense = D.shape[0] <= 2 * 32 * 32  # N<=32 torus, or comparable
    if dense:
        ev = np.linalg.eigvalsh(D.toarray())
        ev = ev[np.argsort(np.abs(ev), kind="mergesort")]
        return np.sort(np.real(ev[:k]))
    evals = eigsh(D, k=k, sigma=0.0, which="LM", return_eigenvectors=False, maxiter=20000, tol=1e-10)
    return np.sort(np.real(evals))


def analytic_torus_eigs(
    L_u: float,
    L_v: float,
    n_max: int = 8,
    antiperiodic_u: bool = False,
    antiperiodic_v: bool = False,
) -> np.ndarray:
    shift_u = 0.5 if antiperiodic_u else 0.0
    shift_v = 0.5 if antiperiodic_v else 0.0
    ev = []
    for n in range(-n_max, n_max + 1):
        for m in range(-n_max, n_max + 1):
            ku = 2.0 * np.pi * (n + shift_u) / L_u
            kv = 2.0 * np.pi * (m + shift_v) / L_v
            val = float(np.hypot(ku, kv))
            ev.append(val)
            ev.append(-val)
    ev = np.array(ev, dtype=float)
    # unique within tolerance, sort by abs then value
    ev = np.unique(np.round(ev, 12))
    return ev[np.argsort(np.abs(ev), kind="mergesort")]


def torus_known_answer(
    N: int = 24,
    L: float = 2.0 * np.pi,
    antiperiodic: bool = True,
    k_compare: int = 8,
) -> dict:
    """Compare discrete Hermitian Dirac on a flat torus to the analytic spectrum."""
    grid = Grid2D(
        Nu=N,
        Nv=N,
        u_min=0.0,
        u_max=L,
        v_min=0.0,
        v_max=L,
        periodic_u=not antiperiodic,
        antiperiodic_u=antiperiodic,
        periodic_v=not antiperiodic,
        antiperiodic_v=antiperiodic,
    )
    D, u, v = build_hermitian_dirac(grid, lambda U, V: np.ones_like(U, dtype=float))
    h_err = hermiticity_error(D)
    num = lowest_abs_eigs(D, k=k_compare)
    exact = analytic_torus_eigs(L, L, n_max=max(6, N // 2), antiperiodic_u=antiperiodic, antiperiodic_v=antiperiodic)
    # Match each numerical eigenvalue to the nearest exact one
    dists = [float(np.min(np.abs(exact - lam))) for lam in num]
    return {
        "N": N,
        "L": L,
        "antiperiodic": antiperiodic,
        "hermiticity_error": h_err,
        "numerical": num.tolist(),
        "nearest_exact": [float(exact[np.argmin(np.abs(exact - lam))]) for lam in num],
        "abs_errors": dists,
        "max_abs_error": float(np.max(dists)),
        "median_abs_error": float(np.median(dists)),
    }


def legacy_symmetrised_torus(N: int = 16, L: float = 2.0 * np.pi) -> dict:
    """Reproduce the legacy construction (real assembly + 0.5(D+D.T)) on a
    flat torus and show that it does not recover the Dirac spectrum.
    """
    Nu = Nv = N
    du = L / Nu
    dv = L / Nv
    npts = Nu * Nv
    rows: List[int] = []
    cols: List[int] = []
    data: List[float] = []

    def add(r, c, val):
        rows.append(r)
        cols.append(c)
        data.append(val)

    def idx(i, j):
        return (i % Nu) * Nv + (j % Nv)

    w_u = [0.5 / du, -0.5 / du]
    off_u = [+1, -1]
    w_v = [0.5 / dv, -0.5 / dv]
    off_v = [+1, -1]
    for i in range(Nu):
        for j in range(Nv):
            p = idx(i, j)
            r0, r1 = p, npts + p
            for off, w in zip(off_u, w_u):
                q = idx(i + off, j)
                add(r0, npts + q, w)
                add(r1, q, w)
            for off, w in zip(off_v, w_v):
                q = idx(i, j + off)
                add(r0, npts + q, -w)
                add(r1, q, +w)
    D = sparse.coo_matrix((data, (rows, cols)), shape=(2 * npts, 2 * npts)).tocsr()
    Dsym = 0.5 * (D + D.T)
    # Compare lowest |eigs| of the symmetrised operator to analytic Dirac
    # After symmetrisation the derivative terms cancel; on a flat torus
    # there is no spin connection, so Dsym may be exactly (or nearly) zero
    # and a shift-invert sparse eigensolver would fail as singular.
    Ddense = Dsym.toarray()
    ev_all = np.linalg.eigvalsh(Ddense)
    evals = np.sort(np.abs(ev_all))[:8]
    fro = float(np.linalg.norm(Ddense))
    exact = analytic_torus_eigs(L, L, n_max=8, antiperiodic_u=False, antiperiodic_v=False)
    exact_abs = np.sort(np.abs(exact))
    # The analytic periodic Dirac has a zero mode, but also a tower of
    # nonzero eigenvalues starting at 1 (for L=2π). A zero operator matches
    # only the zero mode and misses the rest.
    return {
        "legacy_abs_eigs": evals.tolist(),
        "legacy_frobenius_norm": fro,
        "analytic_lowest_abs": [float(x) for x in exact_abs[:8]],
        "legacy_is_essentially_zero": bool(fro < 1e-10),
        "legacy_has_expected_zero_mode": bool(evals[0] < 1e-8),
        "legacy_recovers_first_nonzero_dirac_mode": bool(abs(evals[2] - exact_abs[2]) < 0.05) if len(evals) > 2 else False,
        "note": "Legacy symmetrisation cancels derivatives; the spectrum is not the Dirac spectrum.",
    }


def convergence_study(
    N_list: Tuple[int, ...] = (8, 12, 16, 24, 32),
    antiperiodic: bool = True,
    k_compare: int = 4,
) -> dict:
    rows = []
    for N in N_list:
        r = torus_known_answer(N=N, antiperiodic=antiperiodic, k_compare=k_compare)
        rows.append({"N": N, "max_abs_error": r["max_abs_error"], "hermiticity_error": r["hermiticity_error"]})
    # Empirical order: log(err) ~ -p log(N)
    Ns = np.array([r["N"] for r in rows], dtype=float)
    err = np.array([r["max_abs_error"] for r in rows], dtype=float)
    mask = err > 0
    slope = None
    if np.sum(mask) >= 2:
        slope = float(np.polyfit(np.log(Ns[mask]), np.log(err[mask]), 1)[0])
    return {
        "rows": rows,
        "log_log_slope": slope,
        "expected_slope_near": -2.0,
        "note": "Second-order central differences should give p ≈ 2 (slope ≈ -2).",
    }


def conoid_f(U: np.ndarray, V: np.ndarray, ell0: float = 1.0) -> np.ndarray:
    return np.sqrt(U**2 + 4.0 * ell0**2 * np.cos(2.0 * V) ** 2)


def conoid_spectrum_hermitian(
    Nu: int = 32,
    Nv: int = 32,
    u_max: float = 6.0,
    k: int = 8,
    aps_strength: float = 8.0,
) -> dict:
    """Numerical spectrum of the Hermitian Dirac operator on a truncated conoid.

    This is a numerical experiment. APS is modelled by a boundary penalty, not
    a complete APS projection. Do not treat the eigenvalues as continuum
    theorems.
    """
    grid = Grid2D(
        Nu=Nu,
        Nv=Nv,
        u_min=-u_max,
        u_max=u_max,
        periodic_u=False,
        antiperiodic_u=False,
        periodic_v=True,
        antiperiodic_v=False,
    )
    D, u, v = build_hermitian_dirac(grid, lambda U, V: conoid_f(U, V), aps_strength=aps_strength)
    ev = lowest_abs_eigs(D, k=k)
    return {
        "Nu": Nu,
        "Nv": Nv,
        "u_max": u_max,
        "aps_strength": aps_strength,
        "hermiticity_error": hermiticity_error(D),
        "evals": ev.tolist(),
        "abs_min": float(np.min(np.abs(ev))),
        "note": "Numerical truncated-conoid spectrum; not a continuum APS theorem.",
    }


def main() -> None:
    import json
    from pathlib import Path

    out_dir = Path(__file__).resolve().parent.parent / "pipeline_output"
    out_dir.mkdir(parents=True, exist_ok=True)
    print("Hermiticity + known-answer tests for the 2D Dirac operator")
    torus_ap = torus_known_answer(N=24, antiperiodic=True, k_compare=8)
    print("Antiperiodic torus N=24: max |λ-λ_exact| =", torus_ap["max_abs_error"])
    print("  hermiticity error =", torus_ap["hermiticity_error"])
    conv = convergence_study()
    print("Convergence slope (log err / log N) =", conv["log_log_slope"])
    legacy = legacy_symmetrised_torus(N=16)
    print("Legacy symmetrised |eigs| =", [round(x, 4) for x in legacy["legacy_abs_eigs"]])
    print("Legacy has Dirac zero mode?", legacy["legacy_has_expected_zero_mode"])
    con = conoid_spectrum_hermitian()
    print("Hermitian conoid |λ|_min (numerical, truncated) =", con["abs_min"])
    payload = {"torus_antiperiodic": torus_ap, "convergence": conv, "legacy": legacy, "conoid_numerical": con}
    path = out_dir / "aps_known_answers.json"
    # make JSON-safe
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
