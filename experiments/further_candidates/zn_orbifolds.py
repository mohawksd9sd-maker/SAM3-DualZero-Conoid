"""Zero-mode counts on magnetized T^2/Z_N for N=2,3,4,6.

Exploratory: not part of the locked SAM-3 core.

Z2 counts are computed from the permutation action ψ^j(z) ↦ ψ^{M-j}(−z)
(Kobayashi–Nagamoto, Phys. Rev. D 96 (2017) 096011, arXiv:1709.09784,
eq. (24)), by taking ranks of (I±P)/2.  Z4 counts are imported from the
independent DFT computation of doc 49.  Z3 (even M) and Z6 use the
closed counting formulae of Kobayashi–Nagamoto, Table VII, and are
labelled as literature formulae (checked against their Tables 1, 5 and
III where those overlap).  Scherk–Schwarz phases are held at α=0, the
case of those tables; the same paper notes that SS phases and discrete
Wilson lines can change the invariant count, which would only add more
choices, not remove the existing ones.

A “minimal flux” principle means: the smallest positive M such that some
stated sector has dimension 3, or, alternatively, the count at the
smallest positive flux M=1.  C4 compatibility: Z4 requires τ=i; Z2 is
compatible with any τ (and with the conoid’s C4, since Z2 ⊂ C4); Z3 and
Z6 require the hexagonal modulus and are not C4 compatible.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np

_HERE = Path(__file__).resolve().parent
_Z4 = _HERE.parent / "missing_principle"
if str(_Z4) not in sys.path:
    sys.path.insert(0, str(_Z4))

from z4_orbifold import literature_counts_alpha0, sector_counts as z4_sector_counts  # noqa: E402


def z2_matrix(M: int) -> np.ndarray:
    """Permutation matrix for j ↦ (M−j) mod M, on the basis e_0,…,e_{M-1}."""
    P = np.zeros((M, M), dtype=float)
    for j in range(M):
        P[(M - j) % M, j] = 1.0
    return P


def z2_counts(M: int) -> Dict[str, int]:
    if M <= 0:
        raise ValueError("M must be positive")
    P = z2_matrix(M)
    even_tr = float(np.trace((np.eye(M) + P) / 2.0))
    odd_tr = float(np.trace((np.eye(M) - P) / 2.0))
    even = int(round(even_tr))
    odd = int(round(odd_tr))
    if even + odd != M:
        raise RuntimeError(f"Z2 counts for M={M} do not sum to M")
    return {"+1": even, "-1": odd}


def z2_literature(M: int) -> Dict[str, int]:
    """Kobayashi–Nagamoto Table 1, equivalently Table VII."""
    return {"+1": M // 2 + 1, "-1": (M - 1) // 2}


def z3_literature_even(M: int) -> Dict[str, int]:
    """Kobayashi–Nagamoto Table 5, for even M only.

    M=6n, 6n+2, 6n+4.  Invariant count is always 2⌊M/6⌋+1.
    """
    if M % 2 != 0 or M <= 0:
        raise ValueError("this table is for positive even M")
    n, r = divmod(M, 6)
    # r is 0, 2, or 4
    inv = 2 * n + 1
    if r == 0:
        return {"+1": inv, "omega": 2 * n, "omega_bar": 2 * n - 1}
    if r == 2:
        return {"+1": inv, "omega": 2 * n, "omega_bar": 2 * n + 1}
    return {"+1": inv, "omega": 2 * n + 2, "omega_bar": 2 * n + 1}


def z3_invariant(M: int) -> int:
    """I^{(3)} = 2⌊M/6⌋+1, Kobayashi–Nagamoto (89).

    Stated in that paper as the invariant count, with the generic
    ⌊M/3⌋+1 failing at M=6n+4.  Their detailed table is for even M;
    this closed form is used here for even M, and for odd M it is
    reported separately as the same formula, not independently recomputed.
    """
    return 2 * (M // 6) + 1


def z6_literature(M: int) -> Dict[str, int]:
    """Kobayashi–Nagamoto Table VII, including the even-N invariant formula.

    For small M some floors can be −1 before +1; the formulae are used
    as written and then checked to be nonnegative and to sum to M when
    they should.  The paper’s detailed Z6 analysis is for even M.
    """
    inv = M // 6 + 1
    g1 = (M - 4) // 6 + 1  # e^{iπ/3}
    g2 = (M - 2) // 6 + 1  # e^{2πi/3}
    g3 = M // 6            # e^{iπ} = −1
    g4 = (M - 4) // 6 + 1  # e^{4πi/3}
    g5 = (M - 2) // 6      # e^{5πi/3}
    return {
        "+1": inv,
        "e^{i pi/3}": g1,
        "e^{2 i pi/3}": g2,
        "-1": g3,
        "e^{4 i pi/3}": g4,
        "e^{5 i pi/3}": g5,
    }


def first_M_with_sector_dim(counts_fn, dim: int, M_min: int, M_max: int, step: int = 1) -> Optional[int]:
    for M in range(M_min, M_max + 1, step):
        counts = counts_fn(M)
        if any(v == dim for v in counts.values()):
            return M
    return None


def first_M_with_invariant_dim(counts_fn, dim: int, key: str, M_min: int, M_max: int, step: int = 1) -> Optional[int]:
    for M in range(M_min, M_max + 1, step):
        if counts_fn(M)[key] == dim:
            return M
    return None


def report() -> Dict[str, object]:
    z2_sample = {M: z2_counts(M) for M in range(1, 17)}
    z2_mismatches = [M for M in range(1, 25) if z2_counts(M) != z2_literature(M)]
    z4_sample = {M: z4_sector_counts(M) for M in (1, 3, 4, 8, 9, 11, 12)}
    z3_sample = {M: z3_literature_even(M) for M in range(2, 19, 2)}
    z6_sample = {M: z6_literature(M) for M in range(2, 25, 2)}
    # For Z6, check sums for even M where all entries are nonnegative.
    z6_sum_ok = []
    z6_sum_bad = []
    for M in range(2, 25, 2):
        s = sum(z6_literature(M).values())
        if s == M:
            z6_sum_ok.append(M)
        else:
            z6_sum_bad.append({"M": M, "sum": s, "counts": z6_literature(M)})

    summary = {
        "Z2": {
            "tau": "any (z -> -z)",
            "C4_compatible": True,
            "computed": True,
            "invariant_at_M_1": z2_counts(1)["+1"],
            "first_M_with_a_3-dimensional_sector": first_M_with_sector_dim(z2_counts, 3, 1, 24),
            "first_M_with_invariant_3": first_M_with_invariant_dim(z2_counts, 3, "+1", 1, 24),
            "invariant_3_for_M": [M for M in range(1, 25) if z2_counts(M)["+1"] == 3],
        },
        "Z3": {
            "tau": "exp(2 pi i / 3)  (not C4 compatible)",
            "C4_compatible": False,
            "computed": False,
            "source": "Kobayashi-Nagamoto Table 5 and eq. (89), even M",
            "invariant_at_M_2": z3_literature_even(2)["+1"],
            "first_even_M_with_a_3-dimensional_sector": first_M_with_sector_dim(z3_literature_even, 3, 2, 24, 2),
            "first_even_M_with_invariant_3": first_M_with_invariant_dim(z3_literature_even, 3, "+1", 2, 24, 2),
            "invariant_3_for_even_M": [M for M in range(2, 25, 2) if z3_literature_even(M)["+1"] == 3],
        },
        "Z4": {
            "tau": "i  (C4 compatible)",
            "C4_compatible": True,
            "computed": True,
            "invariant_at_M_1": z4_sector_counts(1)["+1"],
            "first_M_with_a_3-dimensional_sector": first_M_with_sector_dim(z4_sector_counts, 3, 1, 24),
            "first_M_with_invariant_3": first_M_with_invariant_dim(z4_sector_counts, 3, "+1", 1, 24),
            "invariant_3_for_M": [M for M in range(1, 25) if z4_sector_counts(M)["+1"] == 3],
        },
        "Z6": {
            "tau": "exp(2 pi i / 3)  (not C4 compatible)",
            "C4_compatible": False,
            "computed": False,
            "source": "Kobayashi-Nagamoto Table VII",
            "invariant_at_M_2": z6_literature(2)["+1"],
            "first_even_M_with_invariant_3": first_M_with_invariant_dim(z6_literature, 3, "+1", 2, 30, 2),
            "invariant_3_for_even_M": [M for M in range(2, 31, 2) if z6_literature(M)["+1"] == 3],
        },
    }
    return {
        "z2_sample": {str(M): c for M, c in z2_sample.items()},
        "z2_mismatches_with_Table_1": z2_mismatches,
        "z3_sample_even": {str(M): c for M, c in z3_sample.items()},
        "z4_sample": {str(M): c for M, c in z4_sample.items()},
        "z6_sample_even": {str(M): c for M, c in z6_sample.items()},
        "z6_formula_sums_to_M": z6_sum_ok,
        "z6_formula_sum_failures": z6_sum_bad,
        "summary": summary,
        "minimal_positive_flux_does_not_give_3": True,
        "verdict": (
            "At the smallest positive flux, no Z_N in {2,3,4,6} has a "
            "3-dimensional sector (Z2 and Z4 at M=1 have a single invariant "
            "mode).  A 3-dimensional invariant sector first appears at M=4 "
            "(Z2), M=6 (Z3, even), M=8 (Z4), and M=12 (Z6).  Those are "
            "ranges, not a unique M, and they are selected by asking for 3.  "
            "C4 compatibility picks Z2 or Z4, and still does not uniquely "
            "select 3.  Z3 and Z6 require the hexagonal modulus, in conflict "
            "with C4."
        ),
    }
