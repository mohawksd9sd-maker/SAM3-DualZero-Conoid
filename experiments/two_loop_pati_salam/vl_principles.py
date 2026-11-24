"""Doc 63: is there a principle that FORCES extra heavy Higgs-coupled (vector-like) fermions?

Exploratory.  The Dual-Zero regulator is not used or modified.

Contents
* An explicit finite Pati-Salam spectral triple (one generation, optionally with a
  vector-like copy), with pi(a), J, gamma, D: order zero, first order, orientability
  (Hochschild 0-cycle), the K-theory intersection form (Poincare duality), KO-dimension
  sign checks.
* Anomaly cancellation for flux-generated PS multiplets.
* Index / Landau levels on the magnetized surface (reference to docs 61-62).
* Quanta-of-geometry module count.
* Poincare homology sphere S^3/2I: invariant counts (Molien series and direct
  character sum over the 120 icosians), Dirac spectrum multiplicities (Baer).
* The spectral gauge-trace correction: extra gauge-charged fermions in H_F also enter
  the gauge kinetic normalisation, so y_t^2 = 4 g^2 (N_eff/3) / a.  Requirement and
  Higgs mass for k vector-like PS 16-pairs through the doc 60/61 pipeline.
* The omega_0^3 near miss propagated through the pipeline.
"""

from __future__ import annotations

import itertools
import math
from typing import Dict, List, Optional, Tuple

import numpy as np

import top_yukawa_search as ts

# ------------------------------------------------------------------ finite PS triple

Q1 = np.eye(2, dtype=complex)
QI = np.array([[1j, 0], [0, -1j]])
QJ = np.array([[0, 1], [-1, 0]], dtype=complex)
QK = np.array([[0, 1j], [1j, 0]])
QUAT = [Q1, QI, QJ, QK]


class FinitePS:
    """One generation: particle blocks (type, iso 2, colour 4); types 'L','R' and optional VL 'Lp','Rp'.

    Antiparticles are the J images.  gamma: L:+1, R:-1, Lp:-1, Rp:+1 on particles; minus on antiparticles
    (KO-dimension 6: J gamma = - gamma J).
    """

    def __init__(self, vl: bool = False):
        self.types = ["L", "R"] + (["Lp", "Rp"] if vl else [])
        self.side = {"L": "L", "R": "R", "Lp": "L", "Rp": "R"}
        self.chir = {"L": 1, "R": -1, "Lp": -1, "Rp": 1}
        self.nb = 8 * len(self.types)          # particle dimension
        self.dim = 2 * self.nb

    def _blk(self, t):
        i = self.types.index(t)
        return slice(8 * i, 8 * i + 8)

    def pi(self, qR, qL, m) -> np.ndarray:
        P = np.zeros((self.dim, self.dim), dtype=complex)
        for t in self.types:
            q = qL if self.side[t] == "L" else qR
            s = self._blk(t)
            P[s, s] = np.kron(q, np.eye(4))
            sa = slice(self.nb + s.start, self.nb + s.stop)
            P[sa, sa] = np.kron(np.eye(2), m)
        return P

    def swap(self) -> np.ndarray:
        S = np.zeros((self.dim, self.dim))
        S[: self.nb, self.nb:] = np.eye(self.nb)
        S[self.nb:, : self.nb] = np.eye(self.nb)
        return S

    def Jconj(self, X: np.ndarray) -> np.ndarray:
        """J X J^-1 with J = swap o complex conjugation."""
        S = self.swap()
        return S @ X.conj() @ S

    def gamma(self) -> np.ndarray:
        g = np.zeros(self.dim)
        for t in self.types:
            s = self._blk(t)
            g[s] = self.chir[t]
            g[self.nb + s.start: self.nb + s.stop] = -self.chir[t]
        return np.diag(g).astype(complex)

    def algebra_basis(self) -> List[np.ndarray]:
        Z2, Z4 = np.zeros((2, 2)), np.zeros((4, 4))
        out = [self.pi(q, Z2, Z4) for q in QUAT] + [self.pi(Z2, q, Z4) for q in QUAT]
        for i in range(4):
            for j in range(4):
                E = np.zeros((4, 4), dtype=complex)
                E[i, j] = 1
                out += [self.pi(Z2, Z2, E), self.pi(Z2, Z2, 1j * E)]
        return out

    def dirac(self, yuk: float = 1.0, vl_mass: float = 0.0, vl_yuk: float = 0.0, majorana: float = 0.0) -> np.ndarray:
        """D = D_particle + J D_particle J^-1 (+ Majorana nu_R <-> nu_R^c)."""
        Dp = np.zeros((self.dim, self.dim), dtype=complex)
        K = np.array([[1.0, 0.0], [0.0, 0.4]])  # bidoublet Yukawa (iso), colour-universal (PS)
        def put(a, b, M):
            sa, sb = self._blk(a), self._blk(b)
            Dp[sa, sb] += M
            Dp[sb, sa] += M.conj().T
        put("L", "R", yuk * np.kron(K, np.eye(4)))
        if "Lp" in self.types:
            put("L", "Lp", vl_mass * np.eye(8))
            put("R", "Rp", vl_mass * np.eye(8))
            put("Lp", "Rp", vl_yuk * np.kron(K, np.eye(4)))  # mirror chain: D must be odd (L' has gamma=-1)
        D = Dp + self.Jconj(Dp)
        if majorana:
            # nu_R: type R, iso 0, colour 3 (lepton); couples to its own J image
            i = self._blk("R").start + 0 * 4 + 3
            D[i, self.nb + i] += majorana
            D[self.nb + i, i] += majorana
        return D


def order_zero(F: FinitePS) -> float:
    B = F.algebra_basis()
    return max(np.abs(a @ F.Jconj(b) - F.Jconj(b) @ a).max() for a in B for b in B)


def first_order_violation(F: FinitePS, D: np.ndarray) -> float:
    B = F.algebra_basis()
    v = 0.0
    for a in B:
        C = D @ a - a @ D
        for b in B:
            Jb = F.Jconj(b)
            v = max(v, float(np.abs(C @ Jb - Jb @ C).max()))
    return v


def orientability_residual(F: FinitePS) -> float:
    """min || gamma - sum_ab c_ab pi(a) J pi(b) J^-1 ||, c_ab real (Hochschild 0-cycle)."""
    B = F.algebra_basis()
    cols = []
    for a in B:
        for b in B:
            M = a @ F.Jconj(b)
            cols.append(np.concatenate([M.real.ravel(), M.imag.ravel()]))
    A = np.array(cols).T
    g = F.gamma()
    rhs = np.concatenate([g.real.ravel(), g.imag.ravel()])
    c = np.linalg.lstsq(A, rhs, rcond=None)[0]
    return float(np.linalg.norm(A @ c - rhs) / np.linalg.norm(rhs))


def intersection_form(F: FinitePS) -> np.ndarray:
    Z2, Z4 = np.zeros((2, 2)), np.zeros((4, 4))
    E = np.zeros((4, 4), dtype=complex)
    E[0, 0] = 1
    gens = [F.pi(Q1, Z2, Z4), F.pi(Z2, Q1, Z4), F.pi(Z2, Z2, E)]
    g = F.gamma()
    return np.array([[np.trace(g @ p @ F.Jconj(q)).real for q in gens] for p in gens])


def ko_signs(F: FinitePS, D: np.ndarray) -> Dict[str, float]:
    g = F.gamma()
    S = F.swap()
    return {"J^2=+1": True,  # (S K)^2 = S S = 1
            "JD-DJ": float(np.abs(F.Jconj(D) - D).max()),
            "Jgamma+gammaJ": float(np.abs(F.Jconj(g) + g).max()),
            "Dgamma+gammaD (off-diagonal D)": float(np.abs(D @ g + g @ D).max())}


def finite_triple_report() -> Dict[str, object]:
    out = {}
    for vl in (False, True):
        F = FinitePS(vl)
        D0 = F.dirac(1.0, 0.7 if vl else 0.0, 0.5 if vl else 0.0)
        Dm = F.dirac(1.0, 0.7 if vl else 0.0, 0.5 if vl else 0.0, majorana=2.0)
        I = intersection_form(F)
        out["with_VL_pair" if vl else "PS_one_generation"] = {
            "dim_H_F": F.dim, "order_zero": order_zero(F),
            "first_order_Yukawa_and_VL_mass": first_order_violation(F, D0),
            "first_order_with_Majorana": first_order_violation(F, Dm),
            "orientability_residual": orientability_residual(F),
            "intersection_form": I.tolist(), "intersection_det": float(np.linalg.det(I)),
            "intersection_antisymmetric": bool(np.allclose(I, -I.T)),
            "ko_signs": ko_signs(F, D0),
        }
    return out


# ------------------------------------------------------------------ anomalies of flux-generated multiplets


def anomalies(M_L: int, M_R: int, vl_pairs: int = 0) -> Dict[str, int]:
    """Left-handed Weyl content: M_L x (4,2,1), M_R x (4bar,1,2), plus vl_pairs x [(4,2,1)+(4bar,2,1)] etc."""
    su4_cubed = 2 * M_L * 1 + 2 * M_R * (-1) + vl_pairs * (2 - 2)
    witten_L = (4 * M_L + 8 * vl_pairs) % 2
    witten_R = (4 * M_R + 8 * vl_pairs) % 2
    return {"SU4^3": su4_cubed, "Witten_SU2L_mod2": witten_L, "Witten_SU2R_mod2": witten_R}


# ------------------------------------------------------------------ quanta of geometry module count


def quanta_module() -> Dict[str, int]:
    """Irreducible M2(H) + M4(C) bimodule from the two Clifford spinor representations (CCM 2014)."""
    dim_spinor_minus = 4      # M2(H) (x) C = M4(C) acts on C^4
    dim_spinor_plus = 4       # M4(C) on C^4
    per_generation = dim_spinor_minus * dim_spinor_plus  # 16 Weyl = one PS generation
    return {"bimodule_dim": per_generation, "with_J_images": 2 * per_generation,
            "multiplicity_fixed": 0, "vector_like_partner_in_irrep": 0}


# ------------------------------------------------------------------ Poincare homology sphere S^3 / 2I


PHI = (1 + 5 ** 0.5) / 2


def icosians() -> List[np.ndarray]:
    els = set()
    for i in range(4):
        for s in (1, -1):
            v = [0.0] * 4
            v[i] = s
            els.add(tuple(v))
    for s in itertools.product((0.5, -0.5), repeat=4):
        els.add(tuple(s))
    base = (PHI / 2, 0.5, 1 / (2 * PHI), 0.0)
    even = [p for p in itertools.permutations(range(4)) if _parity(p) == 0]
    for p in even:
        for sg in itertools.product((1, -1), repeat=3):
            v = [0.0] * 4
            vals = [base[0] * sg[0], base[1] * sg[1], base[2] * sg[2], 0.0]
            for k in range(4):
                v[p[k]] = vals[k]
            els.add(tuple(round(x, 12) for x in v))
    return [np.array(e) for e in sorted(els)]


def _parity(p) -> int:
    inv = sum(1 for i in range(len(p)) for j in range(i + 1, len(p)) if p[i] > p[j])
    return inv % 2


def invariant_dims(jmax: int = 62) -> List[int]:
    """dim V_j^{2I}, V_j the spin-j/2 irrep (dim j+1), from the character sum over the 120 icosians."""
    G = icosians()
    assert len(G) == 120
    out = []
    for j in range(jmax + 1):
        s = 0.0
        for q in G:
            th = 2 * math.acos(max(-1.0, min(1.0, q[0])))  # SU(2) element angle
            if abs(math.sin(th / 2)) < 1e-12:
                chi = (j + 1) * (1 if q[0] > 0 else (-1) ** j)
            else:
                chi = math.sin((j + 1) * th / 2) / math.sin(th / 2)
            s += chi
        out.append(int(round(s / 120)))
    return out


def molien(jmax: int = 62) -> List[int]:
    """(1 + t^30) / ((1 - t^12)(1 - t^20)), expanded."""
    c = [0] * (jmax + 1)
    for a in range(0, jmax + 1, 12):
        for b in range(0, jmax + 1 - a, 20):
            for e in (0, 30):
                if a + b + e <= jmax:
                    c[a + b + e] += 1
    return c


def poincare_sphere_dirac(levels: int = 30) -> Dict[str, object]:
    """Dirac spectrum on S^3/2I (radius 1): eigenvalues +-(k+3/2) with multiplicities m(k+1)(k+1), m(k)(k+2) (Baer 1996)."""
    m = invariant_dims(levels + 2)
    spec = []
    for k in range(levels):
        a, b = m[k + 1] * (k + 1), m[k] * (k + 2)
        if a:
            spec.append({"|lambda|": k + 1.5, "sign": "+", "mult": a})
        if b:
            spec.append({"|lambda|": k + 1.5, "sign": "-", "mult": b})
    return {"zero_modes": 0, "lowest_levels": spec[:4], "invariants": m[:31]}


# ------------------------------------------------------------------ spectral gauge-trace correction


def requirement_formula(n: float = 1.0) -> Dict[str, float]:
    """(1 + dN/3)/(4 + da) = target y_t^2/(4 g^2) at the doc-60 boundary (b, tau neglected)."""
    _, _, sol, _ = ts.background("composite")
    target = sol["y_at_Lambda"] ** 2 / (4 * sol["g_U"] ** 2)
    return {"target_yt2_over_4g2": target, "da_at_dN0": 1 / target - (3 + n), "slope_da_per_dN": 1 / (3 * target)}


def vl_pairs_case(k: int, chains: int = 1, mass: str = "Lambda") -> Dict[str, object]:
    """k vector-like PS 16+16bar pairs, Yukawa c*y_t through `chains` Higgs couplings each (multiplicity 4 per chain)."""
    N3 = (3 + 2 * k) / 3
    db = 8 / 3 * k if mass == "m_R" else 0.0
    run = mass == "m_R"
    m = 4 * k * chains
    mk = lambda c2: ts.Cand(x=m * c2, x4=m * c2 * c2, trace_scale=N3, extra_db=db, extra_running=run)
    f = lambda c2: ts._mt(mk(c2))
    c2 = ts.solve_for(f, 172.5, 0.0, 4.0, 41)
    if not np.isfinite(c2):
        return {"k": k, "fit": None}
    r = ts.predict(mk(c2))
    return {"k": k, "chains": chains, "mass": mass, "c": math.sqrt(c2), "share_da": m * c2, "N_eff": 3 + 2 * k,
            "Mt": r["Mt"], "Mh": r["Mh"], **ts.pulls(r)}


def doc61_row_corrected() -> Dict[str, float]:
    """Doc 61 best row (x = 2.1, PS 16 pair, multiplicity 4) with the gauge trace of the pair included."""
    x = 2.096
    r0 = ts.predict(ts.Cand(x=x, x4=x * x / 4))
    r1 = ts.predict(ts.Cand(x=x, x4=x * x / 4, trace_scale=5 / 3))
    r2 = ts.predict(ts.Cand(x=x, x4=x * x / 4, trace_scale=5 / 3, extra_db=8 / 3))
    return {"doc61": {"Mt": r0["Mt"], "Mh": r0["Mh"]}, "with_gauge_trace": {"Mt": r1["Mt"], "Mh": r1["Mh"]},
            "with_gauge_trace_and_running": {"Mt": r2["Mt"], "Mh": r2["Mh"]}}


def full_copies_invariance(k: int = 2) -> Dict[str, Dict[str, float]]:
    """k extra Dirac copies of the full three-generation H_F (Poincare-sphere / Landau levels).

    Gauge trace +2*3k generation units, Yukawa trace +2*4k: the ratio 4/3 per unit is unchanged.
    """
    out = {}
    for label, run in (("at_Lambda", False), ("from_m_R", True)):
        c = ts.Cand(x=8 * k, x4=8 * k, trace_scale=1 + 2 * k, sigma_trace_scale=1.0,
                    extra_db=8.0 * k if run else 0.0, extra_running=run)
        r = ts.predict(c)
        out[label] = {"k": k, "Mt": r.get("Mt"), "Mh": r.get("Mh"), "ok": r.get("ok")}
    return out


# ------------------------------------------------------------------ omega_0^3


def omega0_cube() -> Dict[str, object]:
    w = 0.927
    out = {}
    for label, r in (("omega0^3 (0.927)", w ** 3), ("omega0=0.9265", 0.9265 ** 3), ("omega0=0.9275", 0.9275 ** 3),
                     ("required", ts.required_ratio()["r"])):
        a = ts.predict(ts.Cand(r_yuk=r))
        b = ts.predict(ts.Cand(r_yuk=r, r_quartic_power=4))
        out[label] = {"r": r, "Mt": a["Mt"], "Mh_yukawa_only": a["Mh"], "Mh_higgs_normalisation": b["Mh"],
                      "Mt_pull": (a["Mt"] - 172.5) / ts.SIG_MT}
    c5 = ts.cand5()
    lo, hi = c5["required"]["r_1sigma"]
    span = max(c5["constants"].values()) - min(c5["constants"].values())
    n_tries = len(c5["constants"])
    p_any = 1 - (1 - (hi - lo) / span) ** n_tries
    out["look_elsewhere"] = {"n_tries": n_tries, "band": [lo, hi], "span": span,
                             "expected_hits": c5["expected_chance_hits"], "p_at_least_one": p_any}
    return out


def report() -> Dict[str, object]:
    return {
        "finite_triple": finite_triple_report(),
        "anomalies": {"M_L=M_R=3": anomalies(3, 3), "M_L=3,M_R=2": anomalies(3, 2), "with 2 VL pairs": anomalies(3, 3, 2)},
        "quanta_of_geometry": quanta_module(),
        "poincare_sphere": {**poincare_sphere_dirac(), "molien_agrees": invariant_dims(62) == molien(62)},
        "requirement": requirement_formula(),
        "doc61_row_corrected": doc61_row_corrected(),
        "vl_pairs": {f"k={k}, chains={ch}, mass={ms}": vl_pairs_case(k, ch, ms)
                     for k in (1, 2, 3) for ch in (1, 2) for ms in ("Lambda", "m_R")},
        "full_copies_invariance": full_copies_invariance(2),
        "omega0_cube": omega0_cube(),
    }
