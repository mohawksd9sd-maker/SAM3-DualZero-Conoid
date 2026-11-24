"""Doc 64: structures inspired by Biblical images, tested as ordinary mathematics.

Exploratory.  The Dual-Zero regulator is not used or modified.  The texts are
inspiration only; every claim below stands or falls on the computation.

1. Discrete flavour groups of the cube and relatives: A4 (12), S4 = O (24, cube
   rotations), O_h (48), Delta(27), T' = SL(2,3) (24), T7 = Z7 x| Z3 (21, "seven").
   Groups are generated numerically from matrix generators; invariant Yukawa
   tensors for an assignment (L, R, H) are obtained from the group-averaged
   projector on conj(L) x R x H.  Textures, forced degeneracies, the A4
   (Altarelli-Feruglio-type) mixing prediction, and the Yukawa-sum share in the
   spectral boundary (doc 63 accounting: flavour symmetry adds no gauge-charged
   fermions, Delta N = 0).
2. The cube as internal space: T^3 on the cubic lattice, rotation and reflection
   orbifolds, and the magnetized T^2 x S^1/Z2 version; 4D chirality of the zero
   modes from the 7D Clifford algebra; KK shells and unification.
3. Notes: torus fibrations ("wheel within a wheel"), Noah's-ark ratios under the
   doc-63 look-elsewhere statistics, Fano plane / octonion cubic invariant ("seven").
"""

from __future__ import annotations

import cmath
import itertools
import math
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

import top_yukawa_search as ts

W = cmath.exp(2j * math.pi / 3)

# ------------------------------------------------------------------ group generation


def generate(gens: Dict[str, Sequence[np.ndarray]], faithful: str, max_order: int = 200):
    """BFS closure; gens[rep] = list of generator matrices in that rep (same order)."""
    reps = list(gens)
    ng = len(gens[faithful])
    ident = {r: np.eye(gens[r][0].shape[0], dtype=complex) for r in reps}
    key = lambda m: tuple(np.round(m, 8).ravel().tolist())
    elems = {key(ident[faithful]): ident}
    frontier = [ident]
    while frontier:
        new = []
        for e in frontier:
            for k in range(ng):
                ne = {r: e[r] @ gens[r][k] for r in reps}
                kk = key(ne[faithful])
                if kk not in elems:
                    elems[kk] = ne
                    new.append(ne)
        frontier = new
        if len(elems) > max_order:
            raise RuntimeError("group too large")
    return list(elems.values())


def _m(*rows):
    return np.array(rows, dtype=complex)


def one(x):
    return np.array([[x]], dtype=complex)


def group_A4():
    S = _m([1, 0, 0], [0, -1, 0], [0, 0, -1])
    T = _m([0, 1, 0], [0, 0, 1], [1, 0, 0])
    g = {"3": [S, T], "1": [one(1), one(1)], "1'": [one(1), one(W)], "1''": [one(1), one(W * W)]}
    return generate(g, "3")


def _rot(axis, ang):
    a = np.array(axis, float)
    a /= np.linalg.norm(a)
    K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + math.sin(ang) * K + (1 - math.cos(ang)) * K @ K


def group_S4():
    a, b = _rot([0, 0, 1], math.pi / 2), _rot([1, 1, 1], 2 * math.pi / 3)
    # 2-dim rep through S4 -> S3: a -> transposition, b -> 3-cycle
    t2 = _m([1, 0], [0, -1])
    c = math.cos(2 * math.pi / 3)
    s = math.sin(2 * math.pi / 3)
    r2 = _m([c, -s], [s, c])
    g = {"3": [a, b], "3'": [-a, b], "2": [t2, r2], "1": [one(1), one(1)], "1'": [one(-1), one(1)]}
    return generate(g, "3")


def group_Oh():
    a, b = _rot([0, 0, 1], math.pi / 2), _rot([1, 1, 1], 2 * math.pi / 3)
    P = -np.eye(3)
    g = {"3-": [a, b, P], "3+": [a, b, np.eye(3)], "3'-": [-a, b, P], "3'+": [-a, b, np.eye(3)],
         "1+": [one(1)] * 3, "1-": [one(1), one(1), one(-1)], "1'+": [one(-1), one(1), one(1)]}
    return generate(g, "3-")


def group_Delta27():
    C = _m([0, 1, 0], [0, 0, 1], [1, 0, 0])
    E = np.diag([1, W, W * W])
    g = {"3": [C, E], "3b": [C.conj(), E.conj()]}
    for r in range(3):
        for s in range(3):
            g[f"1_{r}{s}"] = [one(W ** r), one(W ** s)]
    return generate(g, "3")


def group_T7():
    rho = cmath.exp(2j * math.pi / 7)
    a = np.diag([rho, rho ** 2, rho ** 4])
    C = _m([0, 1, 0], [0, 0, 1], [1, 0, 0])
    g = {"3": [a, C], "3b": [a.conj(), C], "1": [one(1), one(1)], "1'": [one(1), one(W)], "1''": [one(1), one(W * W)]}
    return generate(g, "3")


def _q2(q):
    a, b, c, d = q
    return _m([a + 1j * b, c + 1j * d], [-c + 1j * d, a - 1j * b])


def _adj(U):
    """SO(3) image of U in SU(2)."""
    s = [_m([0, 1], [1, 0]), _m([0, -1j], [1j, 0]), _m([1, 0], [0, -1])]
    return np.array([[0.5 * np.trace(s[i] @ U @ s[j] @ U.conj().T).real for j in range(3)] for i in range(3)], dtype=complex)


def group_Tprime():
    s = _q2((0, 1, 0, 0))
    t = _q2((-0.5, 0.5, 0.5, 0.5))
    g = {"2": [s, t], "2'": [s, W * t], "2''": [s, W * W * t], "3": [_adj(s), _adj(t)],
         "1": [one(1), one(1)], "1'": [one(1), one(W)], "1''": [one(1), one(W * W)]}
    return generate(g, "2")


GROUPS = {"A4": group_A4, "S4": group_S4, "O_h": group_Oh, "Delta27": group_Delta27, "T'": group_Tprime, "T7": group_T7}


def rep_sum(el, names: Sequence[str]) -> np.ndarray:
    blocks = [el[n] for n in names]
    d = sum(b.shape[0] for b in blocks)
    M = np.zeros((d, d), dtype=complex)
    i = 0
    for b in blocks:
        k = b.shape[0]
        M[i:i + k, i:i + k] = b
        i += k
    return M


def invariant_yukawas(G, L: Sequence[str], R: Sequence[str], H: Sequence[str]) -> np.ndarray:
    """Basis of invariant tensors Y[i,j,k] for  conj(L)_i  R_j  H_k  (shape (n_inv, dL, dR, dH))."""
    dims = None
    P = None
    for el in G:
        A, B, C = rep_sum(el, L), rep_sum(el, R), rep_sum(el, H)
        T = np.kron(np.kron(A.conj(), B), C)
        P = T if P is None else P + T
        dims = (A.shape[0], B.shape[0], C.shape[0])
    P /= len(G)
    w, V = np.linalg.eigh((P + P.conj().T) / 2)
    basis = V[:, w > 0.5].T
    return basis.reshape((-1,) + dims)


def texture_survey(G, L, R, H, alignments: Optional[List[np.ndarray]] = None, n: int = 300, seed: int = 64):
    inv = invariant_yukawas(G, L, R, H)
    d = inv.shape[0]
    if d == 0:
        return {"n_invariants": 0}
    rng = np.random.default_rng(seed)
    dH = inv.shape[3]
    al = alignments or [None]
    out = {"n_invariants": d}
    for k, v in enumerate(al):
        r2, r3, share, gap = [], [], [], []
        for _ in range(n):
            c = rng.normal(size=d) + 1j * rng.normal(size=d)
            vv = v if v is not None else rng.normal(size=dH) + 1j * rng.normal(size=dH)
            Y = np.tensordot(np.tensordot(c, inv, axes=1), vv, axes=([2], [0]))
            s = np.linalg.svd(Y, compute_uv=False)
            s = s / s[0]
            r2.append(s[1])
            r3.append(s[2] if len(s) > 2 else 0.0)
            share.append(float(np.sum(s[1:] ** 2)))
            gap.append(float(min(abs(s[i] - s[j]) for i in range(len(s)) for j in range(i + 1, len(s)))))
        key = "random_H" if v is None else "H=" + ",".join(f"{x.real:.0f}" for x in v)
        out[key] = {"s2_min": float(np.min(r2)), "s2_max": float(np.max(r2)), "s3_max": float(np.max(r3)),
                    "forced_degenerate": bool(np.allclose(r2, 1.0) and np.allclose(r3, 1.0)),
                    "forced_rank_le_2": bool(np.max(r3) < 1e-9),
                    "forced_equal_pair": bool(np.max(gap) < 1e-9),
                    "share_median": float(np.median(share)), "share_min": float(np.min(share))}
    return out


ASSIGNMENTS = {
    "A4": [(["3"], ["3"], ["1"]), (["3"], ["1", "1'", "1''"], ["1"]), (["3"], ["1", "1'", "1''"], ["3"]),
           (["3"], ["3"], ["3"]), (["1", "1'", "1''"], ["1", "1'", "1''"], ["1"])],
    "S4": [(["3"], ["3"], ["1"]), (["3"], ["3'"], ["1"]), (["2", "1"], ["2", "1"], ["1"]), (["3"], ["3"], ["3"])],
    "O_h": [(["3-"], ["3-"], ["1+"]), (["3-"], ["3+"], ["1+"]), (["3-"], ["3-"], ["3+"])],
    "Delta27": [(["3"], ["3"], ["1_00"]), (["3"], ["3b"], ["3b"]), (["3"], ["3b"], ["3"])],
    "T'": [(["2", "1"], ["2", "1"], ["1"]), (["2", "1"], ["2", "1"], ["3"])],
    "T7": [(["3"], ["3"], ["1"]), (["3"], ["3b"], ["3"]), (["3"], ["3b"], ["3b"])],
}


def flavour_report() -> Dict[str, object]:
    out = {}
    for name, fn in GROUPS.items():
        G = fn()
        rows = {}
        for L, R, H in ASSIGNMENTS[name]:
            dH = sum(G[0][h].shape[0] for h in H)
            al = [np.array([1, 0, 0], complex), np.array([1, 1, 1], complex), None] if dH == 3 else None
            rows[f"L={'+'.join(L)}, R={'+'.join(R)}, H={'+'.join(H)}"] = texture_survey(G, L, R, H, al)
        out[name] = {"order": len(G), "assignments": rows}
    return out


# ------------------------------------------------------------------ A4 mixing (AF-type vacuum alignment)


def a4_mixing(n: int = 50, seed: int = 7) -> Dict[str, object]:
    """Charged leptons: L~3, e^c,mu^c,tau^c ~ 1,1'',1', flavon phi_T along the T-invariant direction.
    Neutrinos (Majorana, seesaw-effective): (LL)_1 xi + (LL)_3 . phi_S with phi_S along the S-invariant direction.
    Work in the basis where T is diagonal."""
    G = group_A4()
    T = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], complex)
    w_, V = np.linalg.eig(T)
    order = np.argsort(np.angle(w_) % (2 * math.pi))
    V = V[:, order]
    for el in G:
        el["3d"] = V.conj().T @ el["3"] @ V
    S = V.conj().T @ np.diag([1, -1, -1]).astype(complex) @ V
    wS, VS = np.linalg.eig(S)
    phiS = VS[:, np.argmin(abs(wS - 1))]
    wT, VT = np.linalg.eig(V.conj().T @ T @ V)
    phiT = VT[:, np.argmin(abs(wT - 1))]
    # Majorana invariants: L L phi with L in 3d (no conjugation): use conj trick, treat as conj(conj-rep)
    for el in G:
        el["3dc"] = el["3d"].conj()
    inv1 = invariant_yukawas(G, ["3dc"], ["3d"], ["1"])          # L^T M L invariant  <=> conj(conj L)
    inv3 = invariant_yukawas(G, ["3dc"], ["3d"], ["3d"])
    # charged lepton: conj(L) x (1,1'',1') x 3 (flavon) -> pick the T-aligned contraction
    invl = invariant_yukawas(G, ["3dc"], ["1", "1''", "1'"], ["3d"])
    rng = np.random.default_rng(seed)
    angs = []
    for _ in range(n):
        Ml = np.tensordot(np.tensordot(rng.normal(size=invl.shape[0]) + 0j, invl, axes=1), phiT, axes=([2], [0]))
        Mnu = (rng.normal() + 1j * rng.normal()) * inv1[0][:, :, 0]
        Mnu = Mnu + np.tensordot(np.tensordot(rng.normal(size=inv3.shape[0]) + 1j * rng.normal(size=inv3.shape[0]), inv3, axes=1), phiS, axes=([2], [0]))
        Mnu = (Mnu + Mnu.T) / 2
        # charged leptons: Ml is diagonal in this basis (checked); rows are (e, mu, tau) = couplings to (1, 1'', 1')
        assert np.abs(Ml - np.diag(np.diag(Ml))).max() < 1e-9
        wn, Un = np.linalg.eigh(Mnu @ Mnu.conj().T)
        A = np.abs(Un) ** 2
        c3 = int(np.argmin(A[0]))
        rest = [j for j in range(3) if j != c3]
        c1 = max(rest, key=lambda j: A[0, j])
        c2 = [j for j in rest if j != c1][0]
        s13 = A[0, c3]
        best = (s13, A[0, c2] / (1 - s13), A[1, c3] / (1 - s13))
        angs.append(best)
    angs = np.array(angs)
    data = {"s12": (0.307, 0.012), "s13": (0.02215, 0.00057), "s23": (0.470, 0.015)}  # NuFIT 6.0 (2024), normal ordering, rounded
    pred = {"s12": float(np.median(angs[:, 1])), "s13": float(np.median(angs[:, 0])), "s23": float(np.median(angs[:, 2]))}
    spread = {k: float(np.ptp(angs[:, i])) for k, i in (("s13", 0), ("s12", 1), ("s23", 2))}
    pulls = {k: (pred[k] - data[k][0]) / data[k][1] for k in data}
    return {"prediction_sin2": pred, "spread_over_random_couplings": spread, "data_NuFIT6_NO": data, "pulls_sigma": pulls,
            "pati_salam_consequence": "Y_u, Y_d share the T-aligned flavon -> both diagonal in the same basis -> V_CKM = 1 (V_us = 0 vs 0.2250)"}


# ------------------------------------------------------------------ pipeline consequences


def pipeline() -> Dict[str, object]:
    out = {}
    base = ts.predict(ts.Cand())
    out["data-consistent texture (share 7e-6)"] = {"Mt": base["Mt"], "Mh": base["Mh"], "free_params": "Yukawas fitted to data"}
    # forced degenerate texture Y ~ 1 (L, R triplets, H singlet): all three generations at the top Yukawa
    r = ts.predict(ts.Cand(x=2 * 4.0, x4=2 * 4.0))
    out["Y ~ 1 (degenerate, any cube group, 1 parameter)"] = {"x": 8.0, "Mt": r["Mt"], "Mh": r["Mh"], "mc_over_mt": 1.0}
    r2 = texture_pipeline(1.0, 1.0)
    out["rank-2 degenerate (S4/O_h/T' with Higgs triplet)"] = {"x": 4.0, "Mt": r2["Mt"], "Mh": r2["Mh"], "mc_over_mt": 1.0}
    return out


def texture_pipeline(share: float, s4: float, n: float = 1.0) -> Dict[str, float]:
    r = ts.predict(ts.Cand(x=(3 + n) * share, x4=(3 + n * n) * s4))
    return {"share": share, "Mt": r["Mt"], "Mh": r["Mh"]}


# ------------------------------------------------------------------ 2. cube as internal space (7D)


PAULI = [np.array([[0, 1], [1, 0]], complex), np.array([[0, -1j], [1j, 0]]), np.array([[1, 0], [0, -1]], complex)]


def gamma5() -> np.ndarray:
    return np.diag([1, 1, -1, -1]).astype(complex)


def seven_d_zero_modes() -> Dict[str, object]:
    """Constant-mode / flux zero modes in 7D = M4 x T^3, Gamma^{4+a} = gamma5 (x) sigma_a.

    - rotation g in SO(3) acts on spinors as 1 (x) U(g): commutes with gamma5 -> survivors come in
      both 4D chiralities (vector-like);
    - reflection x_a -> -x_a acts as eta gamma5 (x) sigma_a;
    - T^2 (directions 2,3) zero modes with flux M>0 have internal T^2 chirality -i sigma_2 sigma_3 = sigma_1 = +1.
    """
    g5 = np.kron(gamma5(), np.eye(2))
    def chir_count(P):
        """4D chirality of the image of projector P: (n_L, n_R)."""
        w, V = np.linalg.eigh(P)
        Vs = V[:, w > 0.5]
        if Vs.shape[1] == 0:
            return (0, 0)
        c = np.linalg.eigvalsh(Vs.conj().T @ g5 @ Vs)
        return (int(np.sum(c > 0.5)), int(np.sum(c < -0.5)))
    I8 = np.eye(8)
    out = {}
    out["T3 constant modes (no orbifold)"] = chir_count(I8)
    # Z2 rotation by pi about x1: U = i sigma_1 (lift; sign choice eta = +-1 for the orbifold action)
    for eta in (1, -1):
        U = eta * 1j * np.kron(np.eye(4), PAULI[0])
        # need an involutive action: (i sigma)^2 = -1 -> include a central phase i^-1 (discrete Wilson twist)
        Ui = -1j * U
        out[f"T3/Z2 rotation (twist {eta:+d})"] = chir_count((I8 + Ui) / 2)
    # reflection x1 -> -x1 (S^1/Z2 along x1), unfluxed T^2: both sigma_1 = +-1 constant modes
    for eta in (1, -1):
        R = eta * np.kron(gamma5(), PAULI[0])
        out[f"T2 x S1/Z2 reflection, no flux (eta {eta:+d})"] = chir_count((I8 + R) / 2)
    # flux on T^2: zero modes restricted to sigma_1 = +1 (per unit of flux), then the reflection
    Pflux = np.kron(np.eye(4), (np.eye(2) + PAULI[0]) / 2)
    for eta in (1, -1):
        R = eta * np.kron(gamma5(), PAULI[0])
        P = Pflux @ (I8 + R) / 2
        out[f"magnetized T2 x S1/Z2 (per flux unit, eta {eta:+d})"] = chir_count(P)
    # two orthogonal reflections cannot both be imposed (gamma5 sigma_2 and gamma5 sigma_3 anticommute)
    R2 = np.kron(gamma5(), PAULI[1])
    R3 = np.kron(gamma5(), PAULI[2])
    out["reflections x2 and x3 anticommute"] = bool(np.allclose(R2 @ R3, -R3 @ R2))
    # binary octahedral group 2O acts irreducibly on the internal C^2 -> no invariant constant spinor
    out["2O invariants on internal spinor"] = binary_octahedral_invariants()
    return out


def binary_octahedral_invariants() -> int:
    els = set()
    base = [(1, 0, 0, 0)] + [tuple(np.roll((1 / math.sqrt(2), 1 / math.sqrt(2), 0, 0), k)) for k in range(4)]
    # 2O: 24 Hurwitz units and 24 elements (+-1 +-1 0 0)/sqrt2 permutations
    for c in itertools.product((0.5, -0.5), repeat=4):
        els.add(c)
    for i in range(4):
        for s in (1, -1):
            v = [0.0] * 4
            v[i] = s
            els.add(tuple(v))
    r = 1 / math.sqrt(2)
    for i, j in itertools.combinations(range(4), 2):
        for si, sj in itertools.product((1, -1), repeat=2):
            v = [0.0] * 4
            v[i], v[j] = si * r, sj * r
            els.add(tuple(v))
    assert len(els) == 48
    P = sum(_q2(q) for q in els) / 48
    return int(round(np.trace(P).real))


def cubic_shells(nmax: int = 3) -> Dict[int, int]:
    cnt = {}
    for v in itertools.product(range(-3, 4), repeat=3):
        n2 = sum(x * x for x in v)
        if 1 <= n2 <= nmax:
            cnt[n2] = cnt.get(n2, 0) + 1
    return dict(sorted(cnt.items()))


def kk7_unification_shift(Mc_over_Lambda: float) -> Dict[str, float]:
    """7D gauge KK modes on the cubic T^3: per momentum a massive vector + 2 real adjoint scalars,
    Delta b = (-11/3 + 1/6 + 2/6) C2 = -19/6 C2; SU(4) - SU(2): -19/3."""
    shells = cubic_shells(int((1 / Mc_over_Lambda) ** 2) + 1)
    shift, states = 0.0, 0
    for n2, mult in shells.items():
        m = Mc_over_Lambda * math.sqrt(n2)
        if m < 1:
            shift += 19 / 3 * mult * math.log(1 / m) / (2 * math.pi)
            states += mult
    return {"Mc_over_Lambda": Mc_over_Lambda, "states": states, "delta_alpha_inv": shift}


def square_texture() -> Dict[str, object]:
    import lattice_geometries as lg
    Y = lg.triple_overlap(3, 3, 36, tau=1j)
    st = lg.texture_stats(Y)
    rng = lg.texture_range(st)
    return {"stats": st, "Mt_range_by_higgs_direction": [rng["Mt_min"], rng["Mt_max"]],
            "rows": [(o["share"], o["Mt"], o["Mh"]) for o in rng["by_higgs_direction"]]}


# ------------------------------------------------------------------ 3. notes


def ark_numbers() -> Dict[str, object]:
    dims = {"L": 300, "W": 50, "H": 30}
    vals = {}
    for (a, x), (b, y) in itertools.permutations(dims.items(), 2):
        q = x / y
        for p, lab in ((1, ""), (0.5, "^1/2"), (0.25, "^1/4"), (2, "^2")):
            v = q ** p
            if 0 < v <= 1.2:
                vals[f"({a}/{b}){lab}"] = v
    req = ts.required_ratio()
    lo, hi = req["r_1sigma"]
    hits = {k: v for k, v in vals.items() if lo <= v <= hi}
    span = 1.2
    expected = len(vals) * (hi - lo) / span
    near = min(vals.items(), key=lambda kv: abs(kv[1] - req["r"]))
    r = ts.predict(ts.Cand(r_yuk=near[1]))
    # y_t^2/(4 g^2) = 1/6 (= W/L) as a boundary value
    _, _, sol, _ = ts.background("composite")
    r6 = ts.predict(ts.Cand(r_yuk=math.sqrt(4 / 6) * 2 * sol["g_U"] / (2 * sol["g_U"])))
    return {"numbers_tried": len(vals), "values": vals, "band": [lo, hi], "hits": hits, "expected_chance_hits": expected,
            "nearest": {"name": near[0], "value": near[1], "Mt": r["Mt"], "Mh": r["Mh"]},
            "W/L=1/6 as y_t^2/4g^2": {"Mt": r6["Mt"], "Mh": r6["Mh"]}}


def fano_cubic() -> Dict[str, object]:
    """Octonion structure constants on the Fano plane as a Yukawa tensor Y_ij = f_ijk v_k."""
    lines = [(1, 2, 3), (1, 4, 5), (1, 7, 6), (2, 4, 6), (2, 5, 7), (3, 4, 7), (3, 6, 5)]
    f = np.zeros((7, 7, 7))
    for a, b, c in lines:
        for (i, j, k), s in (((a, b, c), 1), ((b, c, a), 1), ((c, a, b), 1), ((b, a, c), -1), ((a, c, b), -1), ((c, b, a), -1)):
            f[i - 1, j - 1, k - 1] = s
    rng = np.random.default_rng(1)
    v = rng.normal(size=7)
    v /= np.linalg.norm(v)
    s = np.linalg.svd(np.tensordot(f, v, axes=([2], [0])), compute_uv=False)
    return {"singular_values": s.tolist(), "pattern": "three degenerate pairs + one zero for any v (antisymmetric, G2-covariant)"}


def report() -> Dict[str, object]:
    fl = flavour_report()
    return {
        "flavour": fl,
        "a4_mixing": a4_mixing(),
        "pipeline": pipeline(),
        "seven_d": seven_d_zero_modes(),
        "cubic_shells": cubic_shells(3),
        "kk7_unification_shift": {str(f): kk7_unification_shift(f) for f in (1.0, 0.9, 0.7)},
        "square_texture": square_texture(),
        "ark": ark_numbers(),
        "fano": fano_cubic(),
    }
