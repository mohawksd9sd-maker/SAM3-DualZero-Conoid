"""Type I / magnetized-D9 tadpole enumeration on T^6.

Exploratory: not part of the locked SAM-3 core.

The RR tadpole conditions are those written as display (14) in
F. Marchesano and G. Shiu, arXiv:hep-th/0409132:

    ∑_α N_α n_α^1 n_α^2 n_α^3     = 16,
    ∑_α N_α m_α^1 m_α^2 n_α^3     = -16,
    ∑_α N_α m_α^1 n_α^2 m_α^3     = -16,
    ∑_α N_α n_α^1 m_α^2 m_α^3     = -16.

The chiral intersection index of two stacks is
    I_ab = ∏_{i=1}^3 (n_a^i m_b^i − n_b^i m_a^i).

This is a truncated, exhaustive search at small wrapping numbers.  A full
string model also needs an orientifold-image completion, K-theory charges,
and a SUSY (angle) condition that involves the unknown Kähler moduli.
Those are not solved here.  The only question asked of the enumeration is
whether, among small integer solutions of the four tadpole equations, a
pairwise |I_ab|=3 is forced, merely allowed, or absent.

The tadpole equations themselves are extra input from Type I string
theory, not a consequence of the locked conoid.
"""

from __future__ import annotations

from collections import Counter
from itertools import product
from typing import Dict, Iterable, List, Tuple

Stack = Tuple[int, int, int, int, int, int, int, int]


def tadpoles(stacks: List[Stack]) -> Tuple[int, int, int, int]:
    t000 = t110 = t101 = t011 = 0
    for N, n1, n2, n3, m1, m2, m3 in stacks:
        t000 += N * n1 * n2 * n3
        t110 += N * m1 * m2 * n3
        t101 += N * m1 * n2 * m3
        t011 += N * n1 * m2 * m3
    return t000, t110, t101, t011


def tadpoles_ok(stacks: List[Stack]) -> bool:
    return tadpoles(stacks) == (16, -16, -16, -16)


def intersection(a: Stack, b: Stack) -> int:
    _, n1, n2, n3, m1, m2, m3 = a
    _, p1, p2, p3, q1, q2, q3 = b
    return (n1 * q1 - p1 * m1) * (n2 * q2 - p2 * m2) * (n3 * q3 - p3 * m3)


def wrapping_ok(n: int, m: int) -> bool:
    return not (n == 0 and m == 0)


def _pairs(wrap_max: int) -> List[Tuple[int, int]]:
    return [
        (n, m)
        for n in range(-wrap_max, wrap_max + 1)
        for m in range(-wrap_max, wrap_max + 1)
        if wrapping_ok(n, m)
    ]


def _wrappings(wrap_max: int) -> List[Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]]:
    p = _pairs(wrap_max)
    return list(product(p, repeat=3))


def search_one_stack(wrap_max: int = 4, N_candidates: Iterable[int] = (1, 2, 4, 8, 16)) -> Dict[str, object]:
    hits = []
    for N in N_candidates:
        for (n1, m1), (n2, m2), (n3, m3) in _wrappings(wrap_max):
            st = [(N, n1, n2, n3, m1, m2, m3)]
            if tadpoles_ok(st):
                hits.append(st[0])
    return {"n_solutions": len(hits), "solutions": hits}


def search_filler_plus_one(wrap_max: int = 4, N_max: int = 16) -> Dict[str, object]:
    """Pure D9 filler (n,m)=(1,0)^3 of multiplicity N_f, plus one magnetized stack."""
    I_counter: Counter = Counter()
    samples = []
    for N_f in range(0, N_max + 1):
        filler = (N_f, 1, 1, 1, 0, 0, 0)
        for N in list(range(1, 9)) + ([16] if N_max >= 16 else []):
            for (n1, m1), (n2, m2), (n3, m3) in _wrappings(wrap_max):
                st = [filler, (N, n1, n2, n3, m1, m2, m3)]
                if tadpoles_ok(st):
                    I = intersection(st[0], st[1])
                    I_counter[I] += 1
                    if len(samples) < 20:
                        samples.append({"N_f": N_f, "magnetized": st[1], "I": I})
    abs_vals = sorted({abs(I) for I in I_counter})
    return {
        "n_solutions": int(sum(I_counter.values())),
        "I_values": sorted(I_counter.keys()),
        "abs_I_values": abs_vals,
        "any_abs_I_equals_3": 3 in abs_vals,
        "all_abs_I_even": all(v % 2 == 0 for v in abs_vals) if abs_vals else None,
        "samples": samples,
    }


def search_two_stacks(wrap_max: int = 1, N_values: Iterable[int] = (1, 2, 3, 4, 8, 16)) -> Dict[str, object]:
    """Exhaustive two-stack search at small wrapping (default |n|,|m| ≤ 1)."""
    I_counter: Counter = Counter()
    samples = []
    configs = _wrappings(wrap_max)
    Ns = list(N_values)
    for N1 in Ns:
        for wA in configs:
            (n1, m1), (n2, m2), (n3, m3) = wA
            a = (N1, n1, n2, n3, m1, m2, m3)
            # Partial charges; the second stack must make up the rest.
            t = tadpoles([a])
            need = (16 - t[0], -16 - t[1], -16 - t[2], -16 - t[3])
            for N2 in Ns:
                for wB in configs:
                    (p1, q1), (p2, q2), (p3, q3) = wB
                    b = (N2, p1, p2, p3, q1, q2, q3)
                    got = tadpoles([b])
                    if got == need:
                        I = intersection(a, b)
                        I_counter[I] += 1
                        if len(samples) < 16:
                            samples.append({"stacks": [a, b], "I_12": I})
    abs_vals = sorted({abs(I) for I in I_counter})
    return {
        "wrap_max": wrap_max,
        "n_solutions": int(sum(I_counter.values())),
        "I_12_values": sorted(I_counter.keys()),
        "abs_I_12_values": abs_vals,
        "any_abs_I_equals_3": 3 in abs_vals,
        "any_abs_I_equals_1": 1 in abs_vals,
        "all_abs_I_even": all(v % 2 == 0 for v in abs_vals) if abs_vals else None,
        "samples": samples,
    }


def report() -> Dict[str, object]:
    one = search_one_stack()
    two = search_two_stacks()
    filler = search_filler_plus_one()
    any_3 = bool(two["any_abs_I_equals_3"] or filler["any_abs_I_equals_3"])
    forced = False  # 3 is forced only if every solution has |I|=3 and solutions exist
    if two["n_solutions"] + filler["n_solutions"] > 0:
        two_only_3 = two["n_solutions"] > 0 and two["abs_I_12_values"] == [3]
        fill_only_3 = filler["n_solutions"] > 0 and filler["abs_I_values"] == [3]
        # Across both searches, "forced" would require both (if nonempty) to be only 3.
        forced = False  # we will set it only if all nonempty searches are exactly {3}
        nonempty_abs = []
        if two["n_solutions"]:
            nonempty_abs.append(set(two["abs_I_12_values"]))
        if filler["n_solutions"]:
            nonempty_abs.append(set(filler["abs_I_values"]))
        forced = bool(nonempty_abs) and all(s == {3} for s in nonempty_abs)
    return {
        "equations": "Marchesano-Shiu hep-th/0409132, display (14)",
        "truncated_search": True,
        "one_stack": one,
        "two_stacks_wrap_le_1": two,
        "filler_plus_one_magnetized": filler,
        "three_is_allowed_in_this_search": any_3,
        "three_is_forced_in_this_search": forced,
        "verdict": (
            "The four tadpole equations are a strong filter, but they come from "
            "Type I string theory, not from the conoid.  In the small-integer "
            "search, a single stack does not solve them.  Whether two-stack or "
            "filler-plus-one solutions exist, and whether |I|=3 occurs among "
            "them, is reported in the JSON; 3 is not a unique output of the "
            "equations.  The bare Dirac index M1 M2 M3 equals 3 only when a "
            "factor 3 is already chosen."
        ),
    }
