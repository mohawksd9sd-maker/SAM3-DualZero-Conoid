"""Exact (Fraction) one- and two-loop gauge beta coefficients from group data.

Conventions (Machacek-Vaughn NPB 222 (1983) 83; Luo-Wang-Xiao hep-ph/0211440),
two-component (Weyl) fermions, kappa = 1/2, complex scalars:

  16 pi^2 d g_a / dt = b_a g_a^3
  (16 pi^2)^2 d g_a / dt |_2loop = g_a^3 ( sum_b B_ab g_b^2 - sum_k c_ak y_k^2 )

  b_a  = -11/3 C(G_a) + 2/3 sum_F S_a(F) + 1/3 sum_S S_a(S)
  B_aa = -34/3 C(G_a)^2 + sum_F S_a(F) [2 C_a(F) + 10/3 C(G_a)]
                        + sum_S S_a(S) [4 C_a(S) + 2/3 C(G_a)]
  B_ab = sum_F 2 S_a(F) C_b(F) + sum_S 4 S_a(S) C_b(S)          (a != b)

S_a(R) is the Dynkin index under factor a times the dimension under all other
factors.  For an abelian factor with charge q (already in the chosen
normalisation) T = C = q^2.  The Yukawa coefficients are computed from the
index structure of each coupling term, see ``yukawa_c``.

Every coefficient is an exact ``fractions.Fraction``; floats appear only when
the ODE is integrated.  The optional Dual-Zero split (``dual_zero_arith``,
if present) records the exact residual lost when a Fraction is turned into an
IEEE double, so the "visible + residual == exact" bookkeeping is auditable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction as Fr
from typing import Dict, List, Sequence, Tuple

# ---------------------------------------------------------------- group data


@dataclass(frozen=True)
class Group:
    name: str
    kind: str  # "SU" or "U1"
    n: int = 0  # N for SU(N)

    @property
    def casimir_adj(self) -> Fr:
        return Fr(self.n) if self.kind == "SU" else Fr(0)

    @property
    def dim_adj(self) -> int:
        return self.n * self.n - 1 if self.kind == "SU" else 1


# irreps used here: label -> (dim, T, C) for SU(N)
def su_irrep(n: int, label: str) -> Tuple[int, Fr, Fr]:
    if label == "1":
        return 1, Fr(0), Fr(0)
    if label in ("F", "Fbar"):
        return n, Fr(1, 2), Fr(n * n - 1, 2 * n)
    if label == "adj":
        return n * n - 1, Fr(n), Fr(n)
    raise ValueError(label)


@dataclass(frozen=True)
class Field:
    """A multiplet: one irrep label per gauge factor (or U(1) charge)."""

    name: str
    reps: Tuple  # str for SU factors, Fraction charge for U1 factors
    kind: str  # "weyl" or "cscalar" (complex scalar) or "rscalar"
    mult: int = 1  # e.g. number of generations

    def data(self, groups: Sequence[Group]) -> List[Tuple[int, Fr, Fr]]:
        out = []
        for g, r in zip(groups, self.reps):
            if g.kind == "SU":
                out.append(su_irrep(g.n, r))
            else:
                q = Fr(r)
                out.append((1, q * q, q * q))
        return out

    def dim(self, groups) -> int:
        d = 1
        for dd, _, _ in self.data(groups):
            d *= dd
        return d

    def S(self, groups, a: int) -> Fr:
        dat = self.data(groups)
        other = 1
        for i, (dd, _, _) in enumerate(dat):
            if i != a:
                other *= dd
        return dat[a][1] * other

    def C(self, groups, a: int) -> Fr:
        return self.data(groups)[a][2]

    @property
    def weight(self) -> Fr:
        # real scalar counts half of a complex scalar
        return Fr(1, 2) if self.kind == "rscalar" else Fr(1)


@dataclass
class Model:
    name: str
    groups: Tuple[Group, ...]
    fields: List[Field]
    yukawas: List[Tuple[str, Dict[int, Fr]]] = field(default_factory=list)
    # each Yukawa: (name, {a: c_a}) computed by yukawa_c

    def one_loop(self) -> Tuple[Fr, ...]:
        b = []
        for a, g in enumerate(self.groups):
            v = Fr(-11, 3) * g.casimir_adj
            for f in self.fields:
                s = f.S(self.groups, a) * f.mult
                if f.kind == "weyl":
                    v += Fr(2, 3) * s
                else:
                    v += Fr(1, 3) * s * f.weight
            b.append(v)
        return tuple(b)

    def two_loop(self) -> Tuple[Tuple[Fr, ...], ...]:
        n = len(self.groups)
        B = [[Fr(0)] * n for _ in range(n)]
        for a, ga in enumerate(self.groups):
            for bb in range(n):
                v = Fr(0)
                if a == bb:
                    CG = ga.casimir_adj
                    v += Fr(-34, 3) * CG * CG
                    for f in self.fields:
                        s = f.S(self.groups, a) * f.mult
                        c = f.C(self.groups, a)
                        if f.kind == "weyl":
                            v += s * (2 * c + Fr(10, 3) * CG)
                        else:
                            v += f.weight * s * (4 * c + Fr(2, 3) * CG)
                else:
                    for f in self.fields:
                        s = f.S(self.groups, a) * f.mult
                        c = f.C(self.groups, bb)
                        if f.kind == "weyl":
                            v += 2 * s * c
                        else:
                            v += 4 * f.weight * s * c
                B[a][bb] = v
        return tuple(tuple(r) for r in B)


def yukawa_c(groups: Sequence[Group], psi1: Field, psi2: Field, n_triples: int) -> Tuple[Fr, ...]:
    """Two-loop Yukawa coefficient c_a for a Dirac-type term y psi1 phi psi2.

    c_a = 2 kappa Y_4(F)/d(G_a),  Y_4 = Tr[C_a(F) Y Y^dagger] / ... ; with
    kappa = 1/2 and a single complex scalar this reduces to
        c_a = n_triples [C_a(psi1) + C_a(psi2)] / d(G_a),
    where n_triples is the number of (psi1, phi, psi2) component triples with
    unit coefficient.  Checked on the SM top: c = (17/10, 3/2, 2).
    """
    out = []
    for a, g in enumerate(groups):
        out.append(Fr(n_triples) * (psi1.C(groups, a) + psi2.C(groups, a)) / g.dim_adj)
    return tuple(out)


def yukawa_one_loop(groups, psi1: Field, psi2: Field, n_partner1: int, n_partner2: int, n_scalar_partners: int):
    """One-loop 16 pi^2 beta_y = y [ k y^2 - sum_a g_a^2 G_a ] for y psi1 phi psi2.

    k = (n_partner1 + n_partner2)/2 + n_scalar_partners  (fermion legs + scalar
    wave function; no vertex term for a single complex scalar coupling);
    G_a = 3 [C_a(psi1) + C_a(psi2)].  SM top check: k = 9/2,
    G = (17/20, 9/4, 8).
    """
    k = Fr(n_partner1 + n_partner2, 2) + n_scalar_partners
    G = tuple(3 * (psi1.C(groups, a) + psi2.C(groups, a)) for a in range(len(groups)))
    return k, G


# ---------------------------------------------------------------- the models

GUT = Fr(3, 5)  # hypercharge normalisation: q_1^2 = (3/5) Y^2


def _y(Y: Fr) -> Fr:
    # charge in GUT normalisation, so that q^2 = 3/5 Y^2; keep exact by
    # returning a "charge squared" carrier: we store sqrt-free via q^2.
    return Y


class _U1Field(Field):
    pass


def sm_groups() -> Tuple[Group, ...]:
    return (Group("U1Y", "U1"), Group("SU2L", "SU", 2), Group("SU3c", "SU", 3))


def _sm_field(name, Y, r2, r3, kind, mult=1) -> Field:
    # U(1) entry stored as q with q^2 = 3/5 Y^2 -> we store q^2 via a trick:
    # Field.data squares the stored value, so store a value whose square is
    # 3/5 Y^2.  3/5 Y^2 is rational but its root is not; instead keep a
    # dedicated charge-squared field below.
    return _Q2Field(name, (Fr(3, 5) * Y * Y, r2, r3), kind, mult)


@dataclass(frozen=True)
class _Q2Field(Field):
    """Field whose U(1) entries are stored as charge *squared* (exact)."""

    def data(self, groups):
        out = []
        for g, r in zip(groups, self.reps):
            if g.kind == "SU":
                out.append(su_irrep(g.n, r))
            else:
                out.append((1, Fr(r), Fr(r)))
        return out


def standard_model(n_gen: int = 3) -> Model:
    G = sm_groups()
    fl = [
        _sm_field("Q", Fr(1, 6), "F", "F", "weyl", n_gen),
        _sm_field("u^c", Fr(-2, 3), "1", "Fbar", "weyl", n_gen),
        _sm_field("d^c", Fr(1, 3), "1", "Fbar", "weyl", n_gen),
        _sm_field("L", Fr(-1, 2), "F", "1", "weyl", n_gen),
        _sm_field("e^c", Fr(1), "1", "1", "weyl", n_gen),
        _sm_field("H", Fr(1, 2), "F", "1", "cscalar"),
    ]
    m = Model("SM", G, fl)
    Q, uc, H = fl[0], fl[1], fl[5]
    # top: Q_{i alpha} H_j u^c_alpha eps^{ij}: 2*3 = 6 triples
    one = _Q2Field("Q1", Q.reps, "weyl", 1)
    uc1 = _Q2Field("uc1", uc.reps, "weyl", 1)
    m.yukawas.append(("y_t", dict(enumerate(yukawa_c(G, one, uc1, 6)))))
    m.top_one_loop = yukawa_one_loop(G, one, uc1, 1, 2, 3)  # type: ignore[attr-defined]
    return m


def ps_groups() -> Tuple[Group, ...]:
    # order (SU(2)_R, SU(2)_L, SU(4)) to match the repository (b_R, b_L, b)
    return (Group("SU2R", "SU", 2), Group("SU2L", "SU", 2), Group("SU4", "SU", 4))


def pati_salam(scenario: str = "composite", n_gen: int = 3) -> Model:
    """CCvS2015 Pati-Salam content (arXiv:1507.08161).

    Fermions per generation: F_L = (1,2,4), F_R = (2,1,4bar)  [(R, L, 4) order].
    Scalars (complex): bidoublet phi = (2,2,1), Delta_R = (2,1,4);
    scenario "with15" adds a complex Sigma = (1,1,15) that is not decoupled.
    This content reproduces the repository's one-loop (b_R, b_L, b) =
    -(7/3, 3, 31/3) and -(7/3, 3, 9) (sign: here beta = +b g^3).
    """
    G = ps_groups()
    fl = [
        Field("F_L", ("1", "F", "F"), "weyl", n_gen),
        Field("F_R", ("F", "1", "Fbar"), "weyl", n_gen),
        Field("phi", ("F", "F", "1"), "cscalar"),
        Field("Delta_R", ("F", "1", "F"), "cscalar"),
    ]
    if scenario == "with15":
        fl.append(Field("Sigma", ("1", "1", "adj"), "cscalar"))
    elif scenario != "composite":
        raise ValueError(scenario)
    m = Model(f"PS_{scenario}", G, fl)
    FL1 = Field("FL1", fl[0].reps, "weyl")
    FR1 = Field("FR1", fl[1].reps, "weyl")
    # y F_L^{iA} phi_{i jdot} F_R^{jdot}_A : 2*2*4 = 16 triples
    m.yukawas.append(("y_t=y_nu", dict(enumerate(yukawa_c(G, FL1, FR1, 16)))))
    # partners: F_L comp (i,A) -> 2 F_R comps (jdot); F_R comp -> 2; phi comp -> 4 colours
    m.top_one_loop = yukawa_one_loop(G, FL1, FR1, 2, 2, 4)  # type: ignore[attr-defined]
    return m


# ---------------------------------------------------------------- SM decomposition


def sm_components_of_heavy_fields(scenario: str = "composite") -> List[Tuple[str, Field, str]]:
    """Heavy states at m_R, as SM multiplets, with their nature.

    Y = T_3R + (B-L)/2, 4 = 3_{B-L=1/3} + 1_{B-L=-1}.
    Returns (name, SM field, kind) with kind in {"vector", "cscalar",
    "rscalar"}.  Goldstones eaten by the heavy vectors are removed from the
    scalars and accounted for in the vector threshold (-7/2 T per real
    vector component pair, i.e. -11/3 + 1/6).
    """
    S = _sm_field
    out = [
        # massive vectors: leptoquark (3,1,2/3) complex, W_R (1,1,1) complex, Z' real
        ("X_LQ (3,1,2/3)", S("XLQ", Fr(2, 3), "1", "F", "vector"), "vector"),
        ("W_R (1,1,1)", S("WR", Fr(1), "1", "1", "vector"), "vector"),
        ("Z' (1,1,0)", S("Zp", Fr(0), "1", "1", "vector_real"), "vector_real"),
        # Delta_R physical: (3,1,-1/3) complex; (1,1,0) real
        ("Delta_R (3,1,-1/3)", S("D3", Fr(-1, 3), "1", "F", "cscalar"), "cscalar"),
        ("Delta_R (1,1,0) real", S("D0", Fr(0), "1", "1", "rscalar"), "rscalar"),
        # second doublet of the complex bidoublet
        ("phi: 2nd doublet (1,2,1/2)", S("H2", Fr(1, 2), "F", "1", "cscalar"), "cscalar"),
    ]
    if scenario == "with15":
        # complex 15 = 8_0 + 3_{2/3} + 3bar_{-2/3} + 1_0, all complex
        out += [
            ("Sigma (8,1,0) complex", S("S8", Fr(0), "1", "adj", "cscalar"), "cscalar"),
            ("Sigma (3,1,2/3) complex", S("S3", Fr(2, 3), "1", "F", "cscalar"), "cscalar"),
            ("Sigma (3bar,1,-2/3) complex", S("S3b", Fr(-2, 3), "1", "Fbar", "cscalar"), "cscalar"),
            ("Sigma (1,1,0) complex", S("S1", Fr(0), "1", "1", "cscalar"), "cscalar"),
        ]
    return out


def threshold_b(comp: Field, kind: str) -> Tuple[Fr, ...]:
    """One-loop SM b_i contributed by one heavy SM multiplet (with conjugate for complex)."""
    G = sm_groups()
    res = []
    for a in range(3):
        s = comp.S(G, a)
        if kind == "vector":  # complex vector V + Vbar, each eating a complex Goldstone
            res.append(2 * (Fr(-11, 3) + Fr(1, 6)) * s)
        elif kind == "vector_real":
            res.append((Fr(-11, 3) + Fr(1, 6)) * s)
        elif kind == "cscalar":
            res.append(Fr(1, 3) * s)
        elif kind == "rscalar":
            res.append(Fr(1, 6) * s)
        else:
            raise ValueError(kind)
    return tuple(res)


def massless_ps_vector_b_check() -> Tuple[Fr, ...]:
    """Sum of SM b over all PS vectors treated massless (consistency helper)."""
    raise NotImplementedError


def to_float(x: Fr) -> float:
    return float(x)


def dual_zero_record(x: Fr):
    """(visible float64, exact residual) if dual_zero_arith is importable."""
    try:
        from dual_zero_arith import split_float64  # type: ignore
    except Exception:  # pragma: no cover - optional package
        f = float(x)
        return f, x - Fr(f)
    return split_float64(x)
