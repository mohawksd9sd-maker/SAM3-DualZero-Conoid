"""Lattice internal spaces as structure candidates for the top Yukawa (doc 62).

Exploratory.  The Dual-Zero regulator is not used or modified here.

"Flower of Life" (2D): the pattern itself is planar decoration; the testable
object it is drawn on is the hexagonal lattice A_2, i.e. the torus with
tau = exp(i pi/3), and its Z_3 / Z_6 orbifolds.
"4D Flower of Life": the D_4 lattice (24-cell, kissing number 24), realised
as the Hurwitz quaternions, the torus T^4 = R^4 / D_4 and its Z_3 orbifold
(fixed-point-free order-3 unit, 9 fixed points -> resolves to K3).

What is computed
* Z_N (N = 3, 6) action on the CIM flux-M zero modes at tau = exp(i pi/3):
  the rotation matrix is obtained numerically by least squares from
  psi^j(rho z) = sum_k C_jk psi^k(z); its closure residual and eigenvalue
  multiplicities give the sector counts.  These are compared with the
  Kobayashi-Nagamoto tables (arXiv:1709.09784).  Even M closes at
  vanishing Scherk-Schwarz phase; odd M does not (it needs non-zero SS
  phases, not computed here).
* Yukawa textures from triple overlaps (CIM) on the hexagonal T^2, flux
  (3,3,6), and on T^2/Z_3 with the M = 6 invariant three-generation sector
  (flux (6,6,12)).  The texture fixes the Yukawa share of the light
  generations in Tr Y^dag Y, which is the only way such a geometry can
  enter the spectral boundary y_t^2 a = 4 g^2.
* D_4: Hurwitz units (24), the order-3 unit omega = (-1+i+j+k)/2,
  det(1 - L_omega) = 9 fixed points, Euler number of the resolution (24),
  Dirac index on T^4 (Pfaffian of the integer flux), on the T^4/Z_3
  orbifold (Lefschetz fixed-point formula, checked against Ahat(K3) = 2),
  and on K3 with a line bundle (2 + c_1^2 / 2).
"""

from __future__ import annotations

import cmath
import itertools
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np

_ROOT = Path(__file__).resolve().parents[1]
for sub in ("alt_geometries", "further_candidates"):
    p = str(_ROOT / sub)
    if p not in sys.path:
        sys.path.insert(0, p)

from magnetized_torus import psi_cim  # noqa: E402
import zn_orbifolds as zo  # noqa: E402

TAU_HEX = cmath.exp(1j * math.pi / 3)

# ------------------------------------------------------------------ Z_N on the hexagonal torus


def zero_mode_matrix(M: int, pts: List[complex], tau: complex = TAU_HEX) -> np.ndarray:
    return np.array([[psi_cim(j, M, z, tau) for j in range(M)] for z in pts])


def rotation_matrix(M: int, N: int, seed: int = 0) -> Tuple[np.ndarray, float]:
    """C with psi(rho z) = psi(z) C (row vectors), rho = exp(2 pi i / N); returns (C, residual)."""
    rng = np.random.default_rng(seed)
    rho = cmath.exp(2j * math.pi / N)
    pts = [complex(*rng.uniform(-0.6, 0.6, 2)) for _ in range(4 * M + 8)]
    A = zero_mode_matrix(M, pts)
    B = zero_mode_matrix(M, [rho * z for z in pts])
    C = np.linalg.lstsq(A, B, rcond=None)[0]
    return C, float(np.linalg.norm(A @ C - B) / np.linalg.norm(B))


def sector_counts(M: int, N: int) -> Optional[Dict[int, int]]:
    """Multiplicity of each eigenvalue exp(2 pi i k / N), k = 0..N-1; None if the action does not close."""
    C, res = rotation_matrix(M, N)
    if res > 1e-8:
        return None
    ev = np.linalg.eigvals(C)
    ks = np.round(np.angle(ev) / (2 * math.pi) * N).astype(int) % N
    c = Counter(int(k) for k in ks)
    return {k: c.get(k, 0) for k in range(N)}


def literature_match(M: int, N: int) -> Optional[bool]:
    s = sector_counts(M, N)
    if s is None or M % 2:
        return None
    if N == 3:
        lit = zo.z3_literature_even(M)
        return (s[0], s[1], s[2]) == (lit["+1"], lit["omega"], lit["omega_bar"])
    lit = list(zo.z6_literature(M).values())
    return [s[k] for k in range(6)] == lit


def three_generation_fluxes(N: int, M_max: int = 24) -> Dict[str, List[int]]:
    inv, anyk = [], []
    for M in range(2, M_max + 1, 2):
        s = sector_counts(M, N)
        if s is None:
            continue
        if s[0] == 3:
            inv.append(M)
        if 3 in s.values():
            anyk.append(M)
    return {"invariant_sector_dim_3": inv, "some_sector_dim_3": anyk}


# ------------------------------------------------------------------ Yukawa textures


def _grid(n: int, tau: complex = TAU_HEX):
    xs = (np.arange(n) + 0.5) / n
    return [complex(x, 0.0) + tau * y for x in xs for y in xs], 1.0 / (n * n)


def triple_overlap(I: int, J: int, n_grid: int = 36, tau: complex = TAU_HEX) -> np.ndarray:
    K = I + J
    pts, w = _grid(n_grid, tau)
    PI, PJ, PK = (zero_mode_matrix(m, pts, tau) for m in (I, J, K))
    return np.einsum("pi,pj,pk->ijk", PI, PJ, PK.conj()) * w


def sector_basis(M: int, N: int, k: int) -> np.ndarray:
    """Orthonormal basis (columns, in the psi^j basis) of the Z_N sector k."""
    C, res = rotation_matrix(M, N)
    if res > 1e-8:
        raise ValueError("rotation does not close")
    ev, V = np.linalg.eig(C)
    ks = np.round(np.angle(ev) / (2 * math.pi) * N).astype(int) % N
    Q, _ = np.linalg.qr(V[:, ks == k])
    return Q


def texture_stats(Y: np.ndarray, n_random: int = 200, seed: int = 62) -> Dict[str, object]:
    """Singular values of the 3x3 Yukawa for each Higgs basis direction and for random Higgs directions."""
    I, J, K = Y.shape
    def sv(v):
        s = np.linalg.svd(np.tensordot(Y, v, axes=([2], [0])), compute_uv=False)
        return s / s[0]
    basis = [sv(np.eye(K)[k]).tolist() for k in range(K)]
    rng = np.random.default_rng(seed)
    r2, share = [], []
    for _ in range(n_random):
        v = rng.normal(size=K) + 1j * rng.normal(size=K)
        s = sv(v / np.linalg.norm(v))
        r2.append(s[1])
        share.append(float(np.sum(s[1:] ** 2)))
    return {"basis_higgs_ratios": basis, "sigma2_over_sigma1_median": float(np.median(r2)),
            "sigma2_over_sigma1_min": float(np.min(r2)),
            "light_share_median": float(np.median(share)), "light_share_min": float(np.min(share)),
            "fraction_with_sigma2_below_0.01": float(np.mean(np.array(r2) < 0.01))}


def hex_textures(n_grid: int = 36) -> Dict[str, object]:
    Y = triple_overlap(3, 3, n_grid)
    out = {"T2_hex_(3,3,6)": texture_stats(Y)}
    # T^2/Z_3: three generations in the invariant sector of M = 6; Higgs in the invariant sector of M = 12
    Y6 = triple_overlap(6, 6, n_grid)
    B6, B12 = sector_basis(6, 3, 0), sector_basis(12, 3, 0)
    Yp = np.einsum("ijk,ia,jb,kc->abc", Y6, B6, B6, B12.conj())
    out["T2/Z3_hex_M6_invariant_(3x3x%d)" % B12.shape[1]] = texture_stats(Yp)
    return out


# ------------------------------------------------------------------ D_4 / Hurwitz quaternions


def qmul(a, b):
    a0, a1, a2, a3 = a
    b0, b1, b2, b3 = b
    return (a0 * b0 - a1 * b1 - a2 * b2 - a3 * b3,
            a0 * b1 + a1 * b0 + a2 * b3 - a3 * b2,
            a0 * b2 - a1 * b3 + a2 * b0 + a3 * b1,
            a0 * b3 + a1 * b2 - a2 * b1 + a3 * b0)


HURWITZ_BASIS = np.array([[0.5, 0.5, 0.5, 0.5], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=float)  # rows


def hurwitz_units() -> List[Tuple[float, ...]]:
    units = set()
    for c in itertools.product(range(-2, 3), repeat=4):
        v = np.array(c) @ HURWITZ_BASIS
        if abs(v @ v - 1) < 1e-12:
            units.add(tuple(np.round(v, 6)))
    return sorted(units)


def left_mult_matrix(u) -> np.ndarray:
    """Integer matrix of x -> u x in the Hurwitz basis."""
    Binv = np.linalg.inv(HURWITZ_BASIS)
    rows = [np.array(qmul(u, tuple(b))) @ Binv for b in HURWITZ_BASIS]
    return np.array(rows)


def d4_report() -> Dict[str, object]:
    units = hurwitz_units()
    G = HURWITZ_BASIS @ HURWITZ_BASIS.T
    omega = (-0.5, 0.5, 0.5, 0.5)
    L = left_mult_matrix(omega)
    Lint = np.round(L).astype(int)
    fixed = int(round(abs(np.linalg.det(np.eye(4) - L))))
    ev = np.linalg.eigvals(L)
    chi_orb = (0 + 2 * fixed) / 3      # orbifold Euler number (Lefschetz: chi(T^4)=0, each fixed pt +1 per twist)
    chi_K3 = chi_orb + fixed * 2       # each A_2 singularity resolved by two (-2)-curves
    # root count (norm 2 after scaling by sqrt 2): units are the 24 vertices of the 24-cell
    return {"hurwitz_units": len(units), "gram_det_scaled": float(np.linalg.det(2 * G)),
            "omega_is_integer_matrix": bool(np.allclose(L, Lint)), "omega_order3": bool(np.allclose(np.linalg.matrix_power(Lint, 3), np.eye(4))),
            "omega_eigen_angles_deg": sorted(float(round(math.degrees(np.angle(e)))) for e in ev),
            "fixed_points_T4_Z3": fixed, "chi_orbifold": chi_orb, "chi_resolution": chi_K3,
            "kissing_equals_chi_K3": len(units) == chi_K3}


def pfaffian(n: np.ndarray) -> int:
    return int(n[0, 1] * n[2, 3] - n[0, 2] * n[1, 3] + n[0, 3] * n[1, 2])


def t4_index_census(rng_max: int = 2) -> Dict[str, object]:
    vals = range(-rng_max, rng_max + 1)
    cnt = Counter()
    for a, b, c, d, e, f in itertools.product(vals, repeat=6):
        n = np.zeros((4, 4), dtype=int)
        n[0, 1], n[0, 2], n[0, 3], n[1, 2], n[1, 3], n[2, 3] = a, b, c, d, e, f
        n = n - n.T
        cnt[abs(pfaffian(n))] += 1
    tot = sum(cnt.values())
    return {"fluxes": tot, "fraction_index_3": cnt[3] / tot, "distribution": {k: v for k, v in sorted(cnt.items()) if k <= 8}}


def t4z3_generations(pf_max: int = 15) -> Dict[str, object]:
    """Invariant index on T^4/Z_3 (twist angles 2pi/3, -2pi/3; 9 fixed points).

    Lefschetz: n_inv = (1/3) [ Pf + sum_{g=theta,theta^2} sum_p chi_p(g) / det(1 - g)|_spinor ],
    with each fixed point contributing +chi_p/3 per twist for this SU(2)-type action.
    a = number of fixed points with trivial flux phase (chi_p = 1); the others have chi_p = omega^{+-1}.
    Check: Pf = 0, a = 9 gives 2 = Ahat(K3).
    """
    sols = []
    for pf in range(0, pf_max + 1):
        for a in range(0, 10):
            s = a * 2 / 3 + (9 - a) * 2 * (-0.5) / 3
            n = (pf + s) / 3
            if abs(n - round(n)) < 1e-9 and round(n) == 3:
                sols.append({"Pf": pf, "a_trivial_fixed_points": a})
    k3 = (0 + 9 * 2 / 3) / 3
    return {"K3_check_no_flux": k3, "three_generation_solutions": sols,
            "K3_line_bundle_index": "2 + c1^2/2 (c1^2 even): 3 at c1^2 = 2; any integer possible"}


# ------------------------------------------------------------------ pipeline consequences


def light_generation_trace_from_data() -> Dict[str, float]:
    """(m_c^2 + m_u^2)/m_t^2 at ~10^15 GeV (Xing-Zhang-Zhou running masses, rounded)."""
    mt, mc, mu = 0.48, 0.0012, 2.4e-6  # y-equivalent ratios at 1e15 GeV (y_c/y_t ~ 2.6e-3)
    r = (mc / mt) ** 2 + (mu / mt) ** 2
    return {"light_share_quarks_data": r, "x_from_data": (3 + 1) * r}


def pipeline_rows() -> Dict[str, object]:
    import top_yukawa_search as ts
    rows = {}
    base = ts.predict(ts.Cand())
    rows["hex T2 / T2/Z3 / D4 T4 / T4/Z3 (chiral index only, x = 0)"] = {"x": 0.0, "Mt": base["Mt"], "Mh": base["Mh"]}
    d = light_generation_trace_from_data()
    r = ts.predict(ts.Cand(x=d["x_from_data"], x4=0.0))
    rows["light generations at their measured share"] = {"x": d["x_from_data"], "Mt": r["Mt"], "Mh": r["Mh"]}
    return rows


def texture_pipeline(stats: Dict[str, object], n: float = 1.0) -> Dict[str, float]:
    """If the geometric texture were used as is: light share -> extra trace x (quarks and PS leptons)."""
    import top_yukawa_search as ts
    s = stats["light_share_median"]
    x = (3 + n) * s
    x4 = (3 + n * n) * s * s / 2  # two light states sharing equally (rough)
    r = ts.predict(ts.Cand(x=x, x4=x4))
    return {"light_share": s, "x": x, "Mt": r["Mt"], "Mh": r["Mh"], "mc_over_mt_implied": stats["sigma2_over_sigma1_median"]}


def report() -> Dict[str, object]:
    z = {}
    for N in (3, 6):
        z[f"Z{N}"] = {str(M): sector_counts(M, N) for M in range(1, 13)}
    matches = {f"Z{N}": [literature_match(M, N) for M in range(2, 13, 2)] for N in (3, 6)}
    tex = hex_textures()
    return {
        "hex_sector_counts": z,
        "kobayashi_nagamoto_match_even_M": matches,
        "odd_M_closes_at_zero_SS_phase": any(sector_counts(M, 3) is not None for M in (1, 3, 5, 7)),
        "three_generation_fluxes": {f"Z{N}": three_generation_fluxes(N) for N in (3, 6)},
        "textures": tex,
        "texture_pipeline": {k: texture_pipeline(v) for k, v in tex.items()},
        "d4": d4_report(),
        "t4_index_census": t4_index_census(),
        "t4z3": t4z3_generations(),
        "texture_range": {k: texture_range(v) for k, v in tex.items()},
        "d4_shells": d4_shells(6),
        "d4_vs_hex_product": d4_vs_hex_product(),
        "kk_unification_shift": {str(f): kk_unification_shift(f) for f in (1.0, 0.9, 0.7, 0.5)},
        "pipeline": pipeline_rows(),
        "light_trace_data": light_generation_trace_from_data(),
    }


# ------------------------------------------------------------------ texture range over Higgs directions


def texture_range(stats: Dict[str, object], n: float = 1.0) -> Dict[str, object]:
    """M_t over the Higgs basis directions (the Higgs direction is a free choice)."""
    import top_yukawa_search as ts
    out = []
    for s in stats["basis_higgs_ratios"]:
        s = np.array(s)
        share = float(np.sum(s[1:] ** 2))
        x, x4 = (3 + n) * share, (3 + n * n) * float(np.sum(s[1:] ** 4))
        r = ts.predict(ts.Cand(x=x, x4=x4))
        out.append({"ratios": s.tolist(), "share": share, "Mt": r["Mt"], "Mh": r["Mh"]})
    return {"by_higgs_direction": out, "Mt_min": min(o["Mt"] for o in out), "Mt_max": max(o["Mt"] for o in out)}


# ------------------------------------------------------------------ 8D: KK towers of the D_4 torus vs unification


def d4_shells(n_max: int = 6) -> Dict[int, int]:
    """Number of Hurwitz integers of norm N (D_4 up to scale; D_4 dual is similar to D_4)."""
    cnt = Counter()
    rng = range(-4, 5)
    for c in itertools.product(rng, repeat=4):
        v = np.array(c) @ HURWITZ_BASIS
        nrm = int(round(v @ v))
        if 1 <= nrm <= n_max and abs(v @ v - nrm) < 1e-9:
            cnt[nrm] += 1
    return dict(sorted(cnt.items()))


def kk_unification_shift(Mc_over_Lambda: float, alpha4_inv: float = 4 * math.pi / 0.531 ** 2) -> Dict[str, float]:
    """Non-universal shift of alpha_4^-1 - alpha_L^-1 at Lambda from gauge KK modes on T^4 (D_4).

    Per KK momentum: massive vector + 3 real adjoint scalars, Delta b = (-11/3 + 1/6 + 3/6) C_2(G) = -3 C_2(G);
    SU(4) - SU(2): -3 (4 - 2) = -6.  Masses m_k = M_c sqrt(N), N = shell norm.
    """
    shells = d4_shells(int((1 / Mc_over_Lambda) ** 2) + 1)
    shift = 0.0
    states = 0
    for N, mult in shells.items():
        m = Mc_over_Lambda * math.sqrt(N)
        if m < 1.0:
            shift += 6 * mult * math.log(1.0 / m) / (2 * math.pi)
            states += mult
    return {"Mc_over_Lambda": Mc_over_Lambda, "kk_states_below_Lambda": states,
            "delta_alpha_inv_4_minus_L": shift, "relative_to_alpha4_inv": shift / alpha4_inv}


def d4_vs_hex_product() -> Dict[str, float]:
    """D_4 is not A_2 + A_2: with roots of norm 2, det D_4 = 4, det(A_2+A_2) = 9; index^2 = 9/4 is not an integer."""
    A2 = np.array([[2, -1], [-1, 2]])
    D4 = np.array([[2, -1, 0, 0], [-1, 2, -1, -1], [0, -1, 2, 0], [0, -1, 0, 2]])
    dA = float(np.linalg.det(A2)) ** 2
    dD = float(np.linalg.det(D4))
    return {"det_D4": dD, "det_A2xA2": dA, "index_squared": dA / dD, "A2xA2_sublattice_of_D4": abs(dA / dD - round(dA / dD)) < 1e-9}
