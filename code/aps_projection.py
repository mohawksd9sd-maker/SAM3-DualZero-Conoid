#!/usr/bin/env python3
"""APS spectral projection for the 2D Dirac operator.

This module implements the Atiyah–Patodi–Singer boundary condition as a
genuine spectral projection (not a penalty). Known-answer tests are taken
from Falomir, Gamboa Saraví and Santangelo, J. Math. Phys. 39 (1998),
532–544 (arXiv:hep-th/9609194):

* Free Dirac operator on a disk of radius R, flux κ = 0: no zero modes,
  and the nonzero eigenvalues are ± j_{n,l}/R, n = 0,1,2,…, l = 1,2,…,
  each |λ| = j_{n,l}/R occurring with multiplicity 2 for each sign
  (JMP 39, eqs. (56)–(57) with k = −1).
* For k < κ ≤ k+1 the number of zero modes is |k+1|, all of one
  chirality, and the index is k+1 (JMP 39, §III and eq. (79)).

The conoid calculation uses the same projection, applied to the geometric
Dirac operator of code/aps_hermitian.py on a truncation u ∈ [u_min, u_max].
That index and the low-lying spectrum are numerical; they are not a
continuum APS theorem. The tip u=0 is excluded (singular).
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import numpy as np
from scipy.special import jn_zeros


def aps_k(kappa: float) -> int:
    """Unique integer k with k < κ ≤ k+1 (Falomir). κ integer ⇒ k = κ−1."""
    return int(math.ceil(kappa) - 1)


def analytic_disk_index(kappa: float) -> int:
    """Index = k+1 = number of zero modes of one chirality, signed (Falomir)."""
    return aps_k(kappa) + 1


def bessel_disk_spectrum(R: float, n_max: int = 8, l_max: int = 6) -> np.ndarray:
    """Positive |λ| of the free (κ=0) APS Dirac on a disk, with multiplicities.

    For each n ≥ 0 and each zero index l, |λ| = j_{n,l}/R appears twice
    (and independently with both signs). This function returns the sorted
    positive values, each repeated according to the multiplicity of +λ
    (i.e. twice for every (n,l)).
    """
    vals: List[float] = []
    for n in range(0, n_max + 1):
        zeros = jn_zeros(n, l_max)
        for z in zeros:
            vals.extend([float(z) / R, float(z) / R])
    return np.sort(np.array(vals, dtype=float))


def fft_mode_numbers(N: int) -> np.ndarray:
    """Angular frequencies n for a length-N numpy FFT (integers)."""
    return np.fft.fftfreq(N, d=1.0 / N).astype(int)


def _aps_keep_modes(Ntheta: int, kappa: float) -> Tuple[np.ndarray, np.ndarray]:
    """Boolean masks on FFT bins: which upper / lower boundary modes are kept.

    Falomir (11),(13): P_≥ φ = 0 and P_≤ χ = 0, with
    P_≥ = modes n ≥ k+1 and P_≤ = modes n ≤ k+1.
    """
    k = aps_k(kappa)
    n = fft_mode_numbers(Ntheta)
    keep_upper = n < (k + 1)   # not in P_≥
    keep_lower = n > (k + 1)   # not in P_≤
    return keep_upper, keep_lower


@dataclass
class DiskGrid:
    Nr: int
    Ntheta: int
    R: float = 1.0

    def radii(self) -> Tuple[np.ndarray, float]:
        dr = self.R / self.Nr
        r = dr * np.arange(1, self.Nr + 1, dtype=float)  # Δr, 2Δr, …, R
        return r, dr

    def angles(self) -> Tuple[np.ndarray, float]:
        dth = 2.0 * np.pi / self.Ntheta
        th = dth * np.arange(self.Ntheta, dtype=float)
        return th, dth

    def n_full(self) -> int:
        return 2 * self.Nr * self.Ntheta


def _idx(p: int, q: int, Ntheta: int, spin: int) -> int:
    return (p * Ntheta + q) * 2 + spin


def assemble_falomir_disk(grid: DiskGrid, kappa: float = 0.0) -> np.ndarray:
    """Falomir's free-or-flux Dirac on a polar grid, in the √r-weighted L².

    Gauge: φ(r) = −κ r² / (2 R²), A_θ = −φ'(r) = κ r / R² (uniform flux).
    The operator is written on ũ = √r ψ so the discrete inner product is
    flat (∑ Δr Δθ ũ*ũ). The matrix is complex, size 2 Nr Nθ.
    """
    Nr, Nt, R = grid.Nr, grid.Ntheta, grid.R
    r, dr = grid.radii()
    th, dth = grid.angles()
    n_full = grid.n_full()
    D = np.zeros((n_full, n_full), dtype=complex)

    def add(row, col, val):
        D[row, col] += val

    # ∂_θ (central, periodic) and ∂_r (central interior, one-sided at ends)
    # acting on the weighted spinor ũ, including the −1/(2r) connection and A_θ.
    for p in range(Nr):
        rp = float(r[p])
        A_th = kappa * rp / (R * R)  # A_θ
        for q in range(Nt):
            thq = float(th[q])
            e_plus = np.exp(1j * thq)
            e_minus = np.exp(-1j * thq)
            i_u = _idx(p, q, Nt, 0)
            i_l = _idx(p, q, Nt, 1)

            # angular neighbours
            qp = (q + 1) % Nt
            qm = (q - 1) % Nt

            # Radial stencil for ∂_r − 1/(2r)
            if 0 < p < Nr - 1:
                # central ∂_r
                rcoeff_plus = 0.5 / dr
                rcoeff_minus = -0.5 / dr
                r_self = -0.5 / rp
                r_nb = ((p + 1, rcoeff_plus), (p - 1, rcoeff_minus))
            elif p == Nr - 1:
                # one-sided backward: (3u_N - 4u_{N-1} + u_{N-2}) / (2 dr)
                r_self = 1.5 / dr - 0.5 / rp
                r_nb = ((p - 1, -2.0 / dr), (p - 2, 0.5 / dr)) if p >= 2 else ((p - 1, -1.0 / dr),)
            else:
                # p == 0, one-sided forward
                r_self = -1.5 / dr - 0.5 / rp
                r_nb = ((p + 1, 2.0 / dr), (p + 2, -0.5 / dr)) if p + 2 < Nr else ((p + 1, 1.0 / dr),)

            # (Dũ)_φ = i e^{-iθ} (∂_r − 1/(2r) − (i/r)∂_θ − A_θ) ũ_χ
            # (Dũ)_χ = i e^{+iθ} (∂_r − 1/(2r) + (i/r)∂_θ − A_θ) ũ_φ
            # Because B = −i/r ∂_θ − A_θ enters as (∂_r + B) or (−∂_r + B)
            # in Falomir (7). For the upper-from-lower and lower-from-upper
            # we use the equivalent first-order form (74) plus −A_θ in both
            # angular covariant derivatives.
            # Angular: −i/r ∂_θ  on χ in the first row, +i/r ∂_θ on φ in the second.
            # Central ∂_θ ψ_q = (ψ_{q+1} − ψ_{q-1}) / (2 dθ)
            dth_c = 0.5 / dth

            # self terms: r_self and −A_θ
            # first row, from χ:
            add(i_u, i_l, 1j * e_minus * (r_self - A_th))
            # second row, from φ:
            add(i_l, i_u, 1j * e_plus * (r_self - A_th))

            # radial neighbours
            for pn, rc in r_nb:
                add(i_u, _idx(pn, q, Nt, 1), 1j * e_minus * rc)
                add(i_l, _idx(pn, q, Nt, 0), 1j * e_plus * rc)

            # angular neighbours: first row has −(i/r)∂_θ on χ
            # 1j * e_minus * (−i/r) * ∂_θ  = (e_minus / r) * ∂_θ
            # second row: 1j * e_plus * (+i/r) * ∂_θ = − (e_plus / r) * ∂_θ
            add(i_u, _idx(p, qp, Nt, 1), e_minus / rp * dth_c)
            add(i_u, _idx(p, qm, Nt, 1), e_minus / rp * (-dth_c))
            add(i_l, _idx(p, qp, Nt, 0), -e_plus / rp * dth_c)
            add(i_l, _idx(p, qm, Nt, 0), -e_plus / rp * (-dth_c))

    return D


def aps_injection(grid: DiskGrid, kappa: float = 0.0) -> np.ndarray:
    """Isometry Q: C^{n_red} → C^{n_full} whose range is the APS domain.

    Interior (r < R) spinors are unconstrained. At r = R, only the Fourier
    modes allowed by Falomir's (11) are kept.
    """
    Nr, Nt = grid.Nr, grid.Ntheta
    keep_u, keep_l = _aps_keep_modes(Nt, kappa)
    n_u = int(np.sum(keep_u))
    n_l = int(np.sum(keep_l))
    n_int = 2 * (Nr - 1) * Nt
    n_red = n_int + n_u + n_l
    n_full = grid.n_full()
    Q = np.zeros((n_full, n_red), dtype=complex)

    # Interior points p = 0..Nr-2
    for i in range(n_int):
        Q[i, i] = 1.0

    # Boundary p = Nr-1: build unit Fourier modes in the allowed slots.
    # A real-space boundary vector b_q = (1/√Nt) exp(2π i n q / Nt) is unit
    # in the flat discrete ℓ² on the ring (and the √r weight is overall).
    col = n_int
    n_modes = fft_mode_numbers(Nt)
    phase = np.exp(2j * np.pi * np.arange(Nt)[:, None] * n_modes[None, :] / Nt) / np.sqrt(Nt)
    # phase[q, m] corresponds to mode n_modes[m]
    base = 2 * (Nr - 1) * Nt  # starting full index of the boundary ring
    for spin, keep in ((0, keep_u), (1, keep_l)):
        for m in range(Nt):
            if not keep[m]:
                continue
            for q in range(Nt):
                Q[base + q * 2 + spin, col] = phase[q, m]
            col += 1
    assert col == n_red, (col, n_red)
    return Q


def disk_aps_operator(grid: DiskGrid, kappa: float = 0.0) -> Tuple[np.ndarray, np.ndarray]:
    """Return (D_red, Q) for the APS-restricted disk operator."""
    D = assemble_falomir_disk(grid, kappa=kappa)
    Q = aps_injection(grid, kappa=kappa)
    D_red = Q.conj().T @ D @ Q
    return D_red, Q


def hermiticity_rel_error(M: np.ndarray) -> float:
    den = np.linalg.norm(M)
    if den == 0:
        return 0.0
    return float(np.linalg.norm(M - M.conj().T) / den)


def eigs_hermitian_part(M: np.ndarray) -> np.ndarray:
    """Eigenvalues of the Hermitian part (for spectra). Reports if raw M is already close."""
    H = 0.5 * (M + M.conj().T)
    return np.linalg.eigvalsh(H)


def chirality_of_vectors(Q: np.ndarray, vecs_red: np.ndarray, grid: DiskGrid) -> np.ndarray:
    """<γ5> for eigenvectors in the reduced basis, γ5 = diag(1,−1) in Falomir's frame.

    The inner product is the flat one on ũ (√r-weighted).
    """
    full = Q @ vecs_red  # shape (n_full, n_vecs)
    # even components are upper (φ), odd are lower (χ)
    up = np.linalg.norm(full[0::2, :], axis=0) ** 2
    dn = np.linalg.norm(full[1::2, :], axis=0) ** 2
    tot = up + dn
    return (up - dn) / np.maximum(tot, 1e-30)


def numerical_index(evals: np.ndarray, chis: np.ndarray, gap_cut: float) -> Dict[str, float]:
    """Signed chiral count of modes with |λ| < gap_cut."""
    mask = np.abs(evals) < gap_cut
    if not np.any(mask):
        return {"n_small": 0, "index": 0.0, "gap_cut": gap_cut, "min_abs": float(np.min(np.abs(evals)))}
    ch = chis[mask]
    # each near-zero mode contributes sign(<γ5>) if |<γ5>| is decisive
    index = float(np.sum(np.sign(ch)))
    return {
        "n_small": int(np.sum(mask)),
        "index": index,
        "mean_chi": float(np.mean(ch)),
        "gap_cut": gap_cut,
        "min_abs": float(np.min(np.abs(evals))),
        "small_evals": evals[mask].tolist(),
        "small_chi": ch.tolist(),
    }


def disk_known_answer(Nr: int = 24, Ntheta: int = 24, R: float = 1.0, kappa: float = 0.0, n_compare: int = 8) -> dict:
    grid = DiskGrid(Nr=Nr, Ntheta=Ntheta, R=R)
    D_red, Q = disk_aps_operator(grid, kappa=kappa)
    h_err = hermiticity_rel_error(D_red)
    H = 0.5 * (D_red + D_red.conj().T)
    evals, vecs = np.linalg.eigh(H)
    order = np.argsort(np.abs(evals))
    evals_s = evals[order]
    chis = chirality_of_vectors(Q, vecs[:, order], grid)
    out = {
        "Nr": Nr,
        "Ntheta": Ntheta,
        "R": R,
        "kappa": kappa,
        "analytic_index": analytic_disk_index(kappa),
        "n_red": int(D_red.shape[0]),
        "hermiticity_rel_error": h_err,
        "evals_near_zero": evals_s[: max(12, n_compare)].tolist(),
        "chi_near_zero": chis[: max(12, n_compare)].tolist(),
        "min_abs": float(np.min(np.abs(evals))),
    }
    if abs(kappa) < 1e-15:
        exact_pos = bessel_disk_spectrum(R, n_max=6, l_max=5)
        # compare the smallest n_compare *positive* numerical eigenvalues
        pos = np.sort(evals[evals > 0])
        k = min(n_compare, len(pos), len(exact_pos))
        errs = np.abs(pos[:k] - exact_pos[:k])
        out["bessel_positive_numerical"] = pos[:k].tolist()
        out["bessel_positive_exact"] = exact_pos[:k].tolist()
        out["bessel_abs_errors"] = errs.tolist()
        out["bessel_max_abs_error"] = float(np.max(errs)) if k else None
        out["lowest_exact"] = float(exact_pos[0])
    # index: for κ=0 expect no near-zeros; for κ≠0, cut below half the free gap
    free_gap = float(jn_zeros(0, 1)[0]) / R
    cut = 0.35 * free_gap if abs(kappa) > 1e-15 else 0.25 * free_gap
    out["numerical_index"] = numerical_index(evals, chis, gap_cut=cut)
    return out


def disk_convergence(Ns: Tuple[int, ...] = (12, 16, 20, 24), R: float = 1.0) -> dict:
    rows = []
    for N in Ns:
        r = disk_known_answer(Nr=N, Ntheta=N, R=R, kappa=0.0, n_compare=4)
        rows.append({
            "N": N,
            "min_abs": r["min_abs"],
            "lowest_exact": r["lowest_exact"],
            "bessel_max_abs_error": r["bessel_max_abs_error"],
            "hermiticity_rel_error": r["hermiticity_rel_error"],
        })
    Ns_a = np.array([row["N"] for row in rows], dtype=float)
    err = np.array([row["bessel_max_abs_error"] for row in rows], dtype=float)
    slope = None
    if np.all(err > 0) and len(err) >= 2:
        slope = float(np.polyfit(np.log(Ns_a), np.log(err), 1)[0])
    return {"rows": rows, "log_log_slope": slope}


# ---------------------------------------------------------------------------
# Eta invariant of a 1D boundary operator (circle / warped circle)
# ---------------------------------------------------------------------------

def eta_circle_analytic(kappa: float) -> dict:
    """η(B,0) and h(B) for B e_n = (n−κ) e_n on S¹ (Falomir's B, in units R=1).

    For non-integer κ, the spectrum is symmetric about 0 only if {κ}=1/2.
    The standard formula (Hurwitz) is η(0) = 1 − 2{κ} when κ ∉ ℤ,
    and η(0)=0, h=1 when κ ∈ ℤ. This is recorded as a standard Fourier
    eta (see also Falomir et al., JMP 39, eq. (77), for a half-shifted
    operator — we use the unshifted B of their eq. (10) here).
    """
    if abs(kappa - round(kappa)) < 1e-12:
        return {"kappa": kappa, "eta_0": 0.0, "h": 1, "eta_bar": 0.5, "integer_kappa": True}
    frac = kappa - math.floor(kappa)
    eta0 = 1.0 - 2.0 * frac
    return {"kappa": kappa, "eta_0": eta0, "h": 0, "eta_bar": 0.5 * eta0, "integer_kappa": False}


def eta_from_eigs(evals: np.ndarray, s_values: Optional[np.ndarray] = None) -> dict:
    """Truncated η(s) = Σ_{λ≠0} sign(λ)/|λ|^s, and a heat-kernel check of η(0).

    The cutoff eta at s=0 on a finite list is just (#pos − #neg) and is
    not the regularised η(0). We therefore also compute the heat-kernel
    integral (3.2) of Loya's notes, truncated to the given spectrum:
        η ~ (1/√π) ∫_{0}^∞ t^{-1/2} Σ λ e^{-t λ²} dt
    which for a complete spectrum equals η(0). With a truncated spectrum
    this is only an approximation (UV modes missing). Prefer the analytic
    circle formula when it applies.
    """
    ev = np.asarray(evals, dtype=float)
    ev = ev[np.abs(ev) > 1e-12]
    h = int(np.sum(np.abs(evals) <= 1e-12)) if len(evals) else 0
    if ev.size == 0:
        return {"eta_truncated_s0_naive": 0.0, "h": h, "n_modes": 0}
    naive = float(np.sum(np.sign(ev)))
    # Heat-kernel quadrature on a logarithmic t-grid
    # (1/√π) ∫_0^∞ t^{-1/2} Tr(B e^{-t B²}) dt
    t = np.logspace(-8, 6, 800)
    # integrand I(t) = t^{-1/2} * sum λ exp(-t λ²)
    # integrate I(t)/sqrt(π) dt
    def I(tt):
        return tt ** (-0.5) * np.sum(ev * np.exp(-tt * ev * ev))

    Iv = np.array([I(tt) for tt in t])
    # trapezoid in log t: dt = t d(log t)
    logt = np.log(t)
    eta_hk = float(np.trapezoid(Iv * t, logt) / np.sqrt(np.pi))
    return {
        "eta_truncated_s0_naive": naive,
        "eta_heat_kernel_truncated": eta_hk,
        "h": h,
        "n_modes": int(ev.size),
        "min_abs": float(np.min(np.abs(ev))),
    }


# ---------------------------------------------------------------------------
# Conoid: APS projection on the geometric Dirac of aps_hermitian.py
# ---------------------------------------------------------------------------

def conoid_aps_spectrum(
    Nu: int = 24,
    Nv: int = 24,
    u_min: float = 0.4,
    u_max: float = 6.0,
    ell0: float = 1.0,
    k_eigs: int = 16,
) -> dict:
    """Numerical APS Dirac spectrum on a truncated conoid u ∈ [u_min, u_max].

    APS is imposed at both ends by spectral projection of the discrete
    boundary operator (nonnegative modes set to zero). The tip is not
    included. Results are numerical and truncation-dependent.
    """
    # Imported here so the disk tests do not require this module's extras
    from aps_hermitian import Grid2D, build_hermitian_dirac, conoid_f, hermiticity_error

    grid = Grid2D(
        Nu=Nu,
        Nv=Nv,
        u_min=u_min,
        u_max=u_max,
        periodic_u=False,
        antiperiodic_u=False,
        periodic_v=True,
        antiperiodic_v=False,
    )
    # Build without penalty; we will impose a true projection
    D, u, v = build_hermitian_dirac(grid, lambda U, V: conoid_f(U, V, ell0), aps_strength=0.0)
    D = D.toarray()
    n = D.shape[0]
    Nu_, Nv_ = grid.Nu, grid.Nv

    def ring_indices(p: int) -> np.ndarray:
        # 2-component spinors at u-index p, all v, as in aps_hermitian._idx
        return np.array([ (p * Nv_ + q) * 2 + s for q in range(Nv_) for s in range(2) ], dtype=int)

    def boundary_operator(p: int) -> np.ndarray:
        """Discrete A such that D ≈ γ^u (∂_u + A) on this ring, acting on 2 Nv components.

        We extract A from the intra-ring block of D after stripping the
        (normal) derivative coupling to neighbouring rings. This is a
        numerical definition of the boundary operator, not a separate
        continuum parametrix.
        """
        idx = ring_indices(p)
        # Intra-ring block: multiplication (spin connection) + angular derivatives
        A_block = D[np.ix_(idx, idx)].copy()
        # This block already is i σ (A_tangential) without ∂_u (∂_u couples off-ring).
        # For APS we need the self-adjoint operator A in D = σ(∂_n + A).
        # σ = i σ¹ in the geometric frame; A_block = σ A, so A = σ^{-1} A_block.
        sigma = 1j * np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
        # apply σ^{-1} = −i σ¹ on the spinor index of each v
        sig_inv = np.linalg.inv(sigma)
        A = np.zeros_like(A_block)
        for i in range(Nv_):
            for j in range(Nv_):
                A[2*i:2*i+2, 2*j:2*j+2] = sig_inv @ A_block[2*i:2*i+2, 2*j:2*j+2]
        # Hermitian part (discretisation / frame leftovers)
        A = 0.5 * (A + A.conj().T)
        return A, idx

    # For the *outer* boundary, the outward normal is +∂_u; for the *inner*
    # (u=u_min), the outward normal is −∂_u, so APS uses −A (orientation).
    A_in, idx_in = boundary_operator(0)
    A_out, idx_out = boundary_operator(Nu_ - 1)
    # orientation: APS at a boundary uses the operator induced with the
    # *inward* collar coordinate (APS 1975). Inward at the outer end is
    # −∂_u, at the inner end is +∂_u. We follow the usual rule: P_{≥0}(A_out)
    # and P_{≥0}(−A_in) on the outward-oriented operators, equivalently
    # P_{≥0}(A) with A defined from the inward normal.
    # Inward collar: outer uses A_inward = −A_out (if A was extracted from ∂_u).
    # We set A_out_inward = −A_out, A_in_inward = A_in.
    ev_in = np.linalg.eigvalsh(A_in)
    ev_out = np.linalg.eigvalsh(A_out)
    ev_in_inward = np.linalg.eigvalsh(-A_in)  # if A_in was from +∂_u
    # We'll report both orientations and use the inward-normal convention:
    A_in_used = A_in          # inward at inner end is +∂_u
    A_out_used = -A_out       # inward at outer end is −∂_u

    def projector_nonneg(A: np.ndarray) -> np.ndarray:
        evals, vecs = np.linalg.eigh(A)
        P = vecs[:, evals >= -1e-12]  # columns: nonnegative eigenspace
        # orthonormal projector
        if P.size == 0:
            return np.zeros_like(A)
        return P @ P.conj().T

    P_in = projector_nonneg(A_in_used)
    P_out = projector_nonneg(A_out_used)

    # Build the allowed subspace: all interior spinors, plus ker(P) on each end.
    def kernel_injection(P: np.ndarray) -> np.ndarray:
        evals, vecs = np.linalg.eigh(P)
        return vecs[:, evals < 0.5]  # P has ev 0 or 1; keep ev 0

    K_in = kernel_injection(P_in)
    K_out = kernel_injection(P_out)
    n_int = 2 * (Nu_ - 2) * Nv_ if Nu_ > 2 else 0
    n_red = n_int + K_in.shape[1] + K_out.shape[1]
    Q = np.zeros((n, n_red), dtype=complex)
    col = 0
    if Nu_ > 2:
        idx_int = []
        for p in range(1, Nu_ - 1):
            idx_int.extend(ring_indices(p).tolist())
        idx_int = np.array(idx_int, dtype=int)
        for i, fi in enumerate(idx_int):
            Q[fi, col] = 1.0
            col += 1
    for vec in K_in.T:
        Q[idx_in, col] = vec
        col += 1
    for vec in K_out.T:
        Q[idx_out, col] = vec
        col += 1
    assert col == n_red

    D_red = Q.conj().T @ D @ Q
    h_err = hermiticity_rel_error(D_red)
    H = 0.5 * (D_red + D_red.conj().T)
    evals, vecs = np.linalg.eigh(H)
    order = np.argsort(np.abs(evals))
    evals = evals[order]
    # chirality in the geometric frame: σ³ = diag(1,−1) on the spinor index
    full = Q @ vecs[:, : max(k_eigs, 12)]
    up = np.linalg.norm(full[0::2, :], axis=0) ** 2
    dn = np.linalg.norm(full[1::2, :], axis=0) ** 2
    chi = (up - dn) / np.maximum(up + dn, 1e-30)
    gap_cut = 0.05  # absolute; also report 1/u_max scaling separately
    # a more natural cut: a fraction of the median spacing of the first 20 |λ|
    abs_e = np.sort(np.abs(evals))
    typ = float(abs_e[min(20, len(abs_e) - 1)])
    cut = min(0.15, 0.25 * typ) if typ > 0 else 0.05
    nidx = numerical_index(evals, np.pad(chi, (0, max(0, len(evals) - len(chi))), constant_values=0)[: len(evals)], gap_cut=cut)

    eta_in = eta_from_eigs(np.linalg.eigvalsh(A_in_used))
    eta_out = eta_from_eigs(np.linalg.eigvalsh(A_out_used))
    # Analytic comparison: each end is a warped circle, unitarily equivalent
    # (after arc-length) to a standard circle. For the bounding/periodic
    # decision we report the numerical η of A and the naive (Npos−Nneg).
    return {
        "Nu": Nu,
        "Nv": Nv,
        "u_min": u_min,
        "u_max": u_max,
        "ell0": ell0,
        "n_red": n_red,
        "hermiticity_rel_error": h_err,
        "evals_near_zero": evals[:k_eigs].tolist(),
        "abs_near_zero": np.abs(evals[:k_eigs]).tolist(),
        "chi_near_zero": chi[: min(len(chi), k_eigs)].tolist(),
        "min_abs": float(np.min(np.abs(evals))),
        "numerical_index": nidx,
        "eta_inner": eta_in,
        "eta_outer": eta_out,
        "A_inner_eigs": np.linalg.eigvalsh(A_in_used).tolist(),
        "A_outer_eigs": np.linalg.eigvalsh(A_out_used).tolist(),
        "note": "Truncated-conoid numerical APS; not a continuum index theorem. Tip excluded.",
    }


def conoid_u_scan(
    u_max_list: Tuple[float, ...] = (3.0, 4.5, 6.0),
    u_min: float = 0.4,
    N: int = 20,
) -> dict:
    rows = []
    for U in u_max_list:
        r = conoid_aps_spectrum(Nu=N, Nv=N, u_min=u_min, u_max=U, k_eigs=12)
        rows.append({
            "u_max": U,
            "min_abs": r["min_abs"],
            "min_abs_times_U": r["min_abs"] * U,
            "evals_near_zero": r["evals_near_zero"][:8],
            "numerical_index": r["numerical_index"],
            "hermiticity_rel_error": r["hermiticity_rel_error"],
        })
    return {"u_min": u_min, "N": N, "rows": rows}


def main() -> None:
    import json
    from pathlib import Path

    out_dir = Path(__file__).resolve().parent.parent / "reproducibility"
    out_dir.mkdir(parents=True, exist_ok=True)
    print("APS projection: flat-disk known answers")
    disk0 = disk_known_answer(Nr=20, Ntheta=24, R=1.0, kappa=0.0)
    print(f"  κ=0  hermiticity rel err = {disk0['hermiticity_rel_error']:.3e}")
    print(f"  κ=0  min |λ| = {disk0['min_abs']:.4f}  (exact j0,1 = {disk0.get('lowest_exact')})")
    if disk0.get("bessel_max_abs_error") is not None:
        print(f"  κ=0  max |λ−λ_Bessel| on first modes = {disk0['bessel_max_abs_error']:.4f}")
    print(f"  κ=0  analytic index = {disk0['analytic_index']}, numerical = {disk0['numerical_index']}")
    disk_flux = disk_known_answer(Nr=20, Ntheta=24, R=1.0, kappa=0.5)
    print(f"  κ=0.5 analytic index = {disk_flux['analytic_index']}, numerical = {disk_flux['numerical_index']}")
    print(f"  κ=0.5 min |λ| = {disk_flux['min_abs']:.4e}")
    conv = disk_convergence(Ns=(12, 16, 20, 24))
    print(f"  disk convergence slope = {conv['log_log_slope']}")
    print("APS projection: truncated conoid (numerical)")
    con = conoid_aps_spectrum(Nu=18, Nv=20, u_min=0.4, u_max=5.0, k_eigs=12)
    print(f"  conoid hermiticity rel err = {con['hermiticity_rel_error']:.3e}")
    print(f"  conoid min |λ| = {con['min_abs']:.4f}")
    print(f"  conoid numerical index = {con['numerical_index']}")
    scan = conoid_u_scan(u_max_list=(3.0, 4.5, 6.0), N=16)
    print(f"  U-scan min|λ| * U: {[row['min_abs_times_U'] for row in scan['rows']]}")
    payload = {"disk_kappa0": disk0, "disk_kappa05": disk_flux, "disk_convergence": conv, "conoid": con, "conoid_u_scan": scan}
    path = out_dir / "aps_index_results.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
