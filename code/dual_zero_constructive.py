#!/usr/bin/env python3
"""Constructive Dual-Zero weights — no ultrafilter required for production."""
from __future__ import annotations

import math
from typing import List

OMEGA0 = 0.927


def epsilon(n: int, omega0: float = OMEGA0) -> float:
    if n <= 0:
        raise ValueError("n must be positive")
    return omega0 * ((-1) ** n) * (n ** (-n))


def weights(n_max: int, omega0: float = OMEGA0, signed: bool = False) -> List[float]:
    out = []
    for n in range(1, n_max + 1):
        e = epsilon(n, omega0)
        out.append(e if signed else abs(e))
    return out


def reg2(seq: List[float]) -> List[float]:
    """Symmetric Reg2 pairing on a 1-based conceptual sequence stored 0-based."""
    out = []
    n = len(seq)
    k = 0
    while 2 * k + 1 < n:
        out.append(0.5 * (seq[2 * k] + seq[2 * k + 1]))
        k += 1
    if 2 * k < n:
        out.append(seq[2 * k])
    return out


def tail_bound(n: int, omega0: float = OMEGA0) -> float:
    return omega0 * math.exp(-n * math.log(n))


def main() -> None:
    w = weights(20)
    print("Dual-Zero constructive weights |eps(n)|")
    for n, val in enumerate(w, 1):
        print(f"  n={n:2d}  |eps|={val:.6e}  tail_bound={tail_bound(n):.6e}")
    w2 = reg2(w)
    print(f"Reg2 length={len(w2)}  first={w2[0]:.6e}")
    # sensitivity band on omega0
    for dw in (-0.005, 0.0, 0.005):
        s = sum(weights(15, OMEGA0 + dw))
        print(f"  sum|eps| n<=15 at omega0={OMEGA0+dw:.3f}: {s:.6e}")
    print("OK")


if __name__ == "__main__":
    main()
