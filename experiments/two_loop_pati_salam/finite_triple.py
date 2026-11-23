"""Finite spectral triple of one generation: which axioms give Pati-Salam / SM (doc 56).

Hilbert space H_F = C^32: particles p = (alpha, I) with alpha in
{1R, 2R, 1L, 2L} and I in {lepton, c1, c2, c3}, then the 16 antiparticles.
Algebra A_PS = H_R + H_L + M_4(C) (real dimension 4 + 4 + 32 = 40):
  pi(q_R, q_L, m) = [ (q_R + q_L) (x) 1_4  on particles ;  1_4 (x) m  on antiparticles ].
Real structure J(xi, eta) = (conj eta, conj xi)  (J = U K, U the block swap).
Grading gamma = +1 on R particles, -1 on L particles, and minus that on antiparticles.
Dirac operator D = [[S, T^*], [T, conj S]] with S the Dirac Yukawa block (R <-> L,
lepton and quark Yukawas allowed to differ) and T the Majorana nu_R entry.

Everything below is a finite, exact-in-principle linear-algebra check; nothing
uses the Dual-Zero regulator, the conoid or omega_0.
"""

from __future__ import annotations

import math
from typing import Dict, Tuple

import numpy as np

N = 32


def idx(alpha: int, I: int, anti: bool = False) -> int:
    return (16 if anti else 0) + 4 * alpha + I


def quat(a: complex, b: complex) -> np.ndarray:
    return np.array([[a, b], [-np.conj(b), np.conj(a)]])


def pi(qR: np.ndarray, qL: np.ndarray, m: np.ndarray) -> np.ndarray:
    A = np.zeros((N, N), complex)
    Q = np.zeros((4, 4), complex)
    Q[:2, :2], Q[2:, 2:] = qR, qL
    A[:16, :16] = np.kron(Q, np.eye(4))
    A[16:, 16:] = np.kron(np.eye(4), m)
    return A


U = np.zeros((N, N))
U[:16, 16:] = np.eye(16)
U[16:, :16] = np.eye(16)


def J_apply(X: np.ndarray) -> np.ndarray:
    """J X J^{-1} for an operator X (J = U K)."""
    return U @ X.conj() @ U.T


def opposite(b: np.ndarray) -> np.ndarray:
    """b^0 = J b^* J^{-1}."""
    return J_apply(b.conj().T)


GAMMA = np.diag(np.concatenate([np.kron([1, 1, -1, -1], np.ones(4)), -np.kron([1, 1, -1, -1], np.ones(4))]))


def dirac(y_nu=0.5, y_e=0.1, y_u=0.9, y_d=0.2, m_M=1.3, rng=None) -> np.ndarray:
    S = np.zeros((16, 16), complex)
    for I in range(4):
        yu, yd = (y_nu, y_e) if I == 0 else (y_u, y_d)
        # R -> L: alpha 0 (1R) <-> 2 (1L), alpha 1 (2R) <-> 3 (2L)
        S[idx(2, I), idx(0, I)] = yu
        S[idx(3, I), idx(1, I)] = yd
    S = S + S.conj().T
    T = np.zeros((16, 16), complex)
    T[idx(0, 0), idx(0, 0)] = m_M
    D = np.zeros((N, N), complex)
    D[:16, :16] = S
    D[16:, 16:] = S.conj()
    D[16:, :16] = T
    D[:16, 16:] = T.conj().T
    return D


def random_ps(rng) -> np.ndarray:
    c = rng.normal(size=4) + 1j * rng.normal(size=4)
    return pi(quat(c[0], c[1]), quat(c[2], c[3]), rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4)))


def random_sm(rng, conj_lepton: bool = False) -> np.ndarray:
    lam = complex(rng.normal(), rng.normal())
    c = rng.normal(size=2) + 1j * rng.normal(size=2)
    m = np.zeros((4, 4), complex)
    m[0, 0] = np.conj(lam) if conj_lepton else lam
    m[1:, 1:] = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    return pi(np.diag([lam, np.conj(lam)]), quat(c[0], c[1]), m)


def comm(a, b):
    return a @ b - b @ a


def first_order_violation(D, sampler_a, sampler_b, rng, trials=20) -> float:
    return max(np.abs(comm(comm(D, sampler_a(rng)), opposite(sampler_b(rng)))).max() for _ in range(trials))


def order_zero_violation(sampler, rng, trials=20) -> float:
    return max(np.abs(comm(sampler(rng), opposite(sampler(rng)))).max() for _ in range(trials))


def ko_signs(D) -> Dict[str, int]:
    """(epsilon, epsilon', epsilon''):  J^2 = eps, JD = eps' DJ, J gamma = eps'' gamma J."""
    J2 = U @ U.conj()  # J^2 = U conj(U)
    eps = int(round(np.real(J2[0, 0])))
    eps1 = 1 if np.allclose(J_apply(D), D) else (-1 if np.allclose(J_apply(D), -D) else 0)
    eps2 = 1 if np.allclose(J_apply(GAMMA), GAMMA) else (-1 if np.allclose(J_apply(GAMMA), -GAMMA) else 0)
    return {"epsilon": eps, "epsilon_prime": eps1, "epsilon_dprime": eps2}


KO_TABLE = {  # n mod 8 -> (eps, eps', eps'') for even n
    0: (1, 1, 1), 2: (-1, 1, -1), 4: (-1, 1, 1), 6: (1, 1, -1),
}


def ko_dimension(D) -> int:
    s = ko_signs(D)
    t = (s["epsilon"], s["epsilon_prime"], s["epsilon_dprime"])
    for n, v in KO_TABLE.items():
        if v == t:
            return n
    return -1


def ps_basis():
    """Real basis of A_PS (40 elements) as operators."""
    out = []
    for k in range(4):
        for which in ("R", "L"):
            c = np.zeros(4, complex)
            c[k // 2] = 1 if k % 2 == 0 else 1j
            q = quat(c[0], c[1])
            z = np.zeros((2, 2))
            out.append(pi(q, z, np.zeros((4, 4))) if which == "R" else pi(z, q, np.zeros((4, 4))))
    for i in range(4):
        for j in range(4):
            for ph in (1, 1j):
                m = np.zeros((4, 4), complex)
                m[i, j] = ph
                out.append(pi(np.zeros((2, 2)), np.zeros((2, 2)), m))
    return out


def sm_basis():
    """Real basis of A_SM = C + H + M_3(C) embedded in A_PS (24 elements)."""
    out = []
    for ph in (1, 1j):
        m = np.zeros((4, 4), complex)
        m[0, 0] = ph
        out.append(pi(np.diag([ph, np.conj(ph)]), np.zeros((2, 2)), m))
    for k in range(4):
        c = np.zeros(2, complex)
        c[k // 2] = 1 if k % 2 == 0 else 1j
        out.append(pi(np.zeros((2, 2)), quat(c[0], c[1]), np.zeros((4, 4))))
    for i in range(1, 4):
        for j in range(1, 4):
            for ph in (1, 1j):
                m = np.zeros((4, 4), complex)
                m[i, j] = ph
                out.append(pi(np.zeros((2, 2)), np.zeros((2, 2)), m))
    return out


def _vec(X):
    return np.concatenate([X.real.ravel(), X.imag.ravel()])


def maximality(D) -> Dict[str, object]:
    """Is A_SM a maximal first-order subspace inside A_PS?

    Direction x (orthogonal complement of A_SM in A_PS, 16 real dims) can be
    added only if [[D, x], b^0] = 0 and [[D, b], x^0] = 0 for all b in A_SM + x.
    We solve the linear condition against A_SM for a general x in the
    complement and report the dimension of the solution space.
    """
    ps, sm = ps_basis(), sm_basis()
    P = np.array([_vec(X) for X in ps]).T
    S = np.array([_vec(X) for X in sm]).T
    # orthogonal complement of span(S) inside span(P), in coefficient space of P
    coef_S = np.linalg.lstsq(P, S, rcond=None)[0]  # 40 x 24
    Uc, s, Vt = np.linalg.svd(coef_S)
    comp = Uc[:, coef_S.shape[1]:]  # 40 x 16
    rows = []
    for b in sm:
        b0 = opposite(b)
        blocks = []
        for kcol in range(comp.shape[1]):
            x = sum(comp[i, kcol] * ps[i] for i in range(len(ps)))
            blocks.append(np.concatenate([_vec(comm(comm(D, x), b0)), _vec(comm(comm(D, b), opposite(x)))]))
        rows.append(np.array(blocks).T)
    M = np.vstack(rows)
    G = M.T @ M  # 16 x 16 Gram matrix (avoids a huge SVD)
    w, v = np.linalg.eigh(G)
    tol = 1e-9 * max(w.max(), 1.0)
    null_vecs = v[:, w < tol]
    null = null_vecs.shape[1]
    # Linear condition against A_SM leaves `null` candidate directions.  The
    # condition must also hold for x against itself (quadratic in x).  Minimise
    # ||[[D, x], x^0]|| over unit x in the candidate space.
    min_self = None
    if null:
        cands = [sum(comp[i, k] * ps[i] for i in range(len(ps))) for k in range(comp.shape[1])]
        basis = [sum(null_vecs[k, j] * cands[k] for k in range(len(cands))) for j in range(null)]
        from scipy.optimize import minimize

        def q(c):
            c = np.asarray(c) / np.linalg.norm(c)
            x = sum(ci * b for ci, b in zip(c, basis))
            return float(np.linalg.norm(comm(comm(D, x), opposite(x))) ** 2)

        rng = np.random.default_rng(0)
        best = min(minimize(q, rng.normal(size=null), method="Nelder-Mead",
                            options={"xatol": 1e-10, "fatol": 1e-14, "maxiter": 4000}).fun for _ in range(12))
        min_self = math.sqrt(best)
    maximal = null == 0 or (min_self is not None and min_self > 1e-6)
    return {"dim_A_PS": len(ps), "dim_A_SM": len(sm), "complement_dim": comp.shape[1],
            "linear_candidate_directions": null, "min_self_violation_on_candidates": min_self,
            "A_SM_is_maximal_first_order": bool(maximal)}


def isospectral_test(seed=7) -> Dict[str, float]:
    """A unitary V not in the commutant: D' = V D V^* has the same spectrum.

    Any Dual-Zero quantity built from the spectrum (Reg_2 of a spectral
    function, eps(n)-weighted mode sums) is identical for D and D', but D'
    breaks the first-order condition / the grading compatibility.  So a
    spectral regulator cannot select the axioms.
    """
    rng = np.random.default_rng(seed)
    D = dirac()
    X = rng.normal(size=(N, N)) + 1j * rng.normal(size=(N, N))
    V, _ = np.linalg.qr(X)
    D2 = V @ D @ V.conj().T
    e1, e2 = np.sort(np.linalg.eigvalsh(D)), np.sort(np.linalg.eigvalsh(D2))

    def reg2_heat(ev, t=0.7, delta=1e-6):
        f = lambda lam: np.exp(-t * lam ** 2)
        return float(np.sum((f(ev + delta) + f(ev - delta)) / 2))

    omega0 = 0.927
    def eps_sum(ev):
        evs = np.sort(np.abs(ev))
        return float(sum(omega0 * (-1) ** n * n ** (-float(n)) * np.exp(-evs[n - 1]) for n in range(1, len(evs) + 1)))

    return {
        "max_eigenvalue_diff": float(np.abs(e1 - e2).max()),
        "reg2_heat_D": reg2_heat(e1), "reg2_heat_D2": reg2_heat(e2),
        "eps_sum_D": eps_sum(e1), "eps_sum_D2": eps_sum(e2),
        "first_order_SM_D": first_order_violation(D, random_sm, random_sm, rng),
        "first_order_SM_D2": first_order_violation(D2, random_sm, random_sm, rng),
        "gamma_anticommutes_D2": float(np.abs(GAMMA @ D2 + D2 @ GAMMA).max()),
        "JD_equals_DJ_D2": float(np.abs(J_apply(D2) - D2).max()),
    }


def report(seed=1) -> Dict[str, object]:
    rng = np.random.default_rng(seed)
    D = dirac()
    D_noMaj_equal = dirac(y_nu=0.9, y_e=0.2, y_u=0.9, y_d=0.2, m_M=0.0)
    D_noMaj = dirac(m_M=0.0)
    return {
        "KO_signs": ko_signs(D), "KO_dim": ko_dimension(D),
        "order_zero_PS": order_zero_violation(random_ps, rng),
        "first_order_PS_generic_D": first_order_violation(D, random_ps, random_ps, rng),
        "first_order_SM_generic_D": first_order_violation(D, random_sm, random_sm, rng),
        "first_order_SM_conj_lepton_entry": first_order_violation(D, lambda r: random_sm(r, True), lambda r: random_sm(r, True), rng),
        "first_order_PS_no_Majorana_lepton_eq_quark": first_order_violation(D_noMaj_equal, random_ps, random_ps, rng),
        "first_order_PS_no_Majorana_lepton_ne_quark": first_order_violation(D_noMaj, random_ps, random_ps, rng),
        "maximality": maximality(D),
        "isospectral": isospectral_test(),
    }
