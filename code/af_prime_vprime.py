#!/usr/bin/env python3
"""AF' finite scale v' = (Lambda0 * M_star)**0.5 and direction factors.

Structural Tr(D_F'^2)=2 Tr(Phi^dag Phi), Tr(D_F'^4)=2 Tr((Phi^dag Phi)^2).
Does not replace VL_Q thresholds; does not set M_X = mu_meet.
"""
from __future__ import annotations

import math
import numpy as np

G_N = 6.70883096e-39
ell0 = math.sqrt(45 * G_N / (64 * math.pi))
Lambda0 = 1.0 / ell0
mH = 125.0
M_star = math.sqrt(Lambda0 * mH)
v_C = math.sqrt(Lambda0 * M_star)
mu_meet_ref = 1.39e15


def direction_t4(kind: str) -> float:
    if kind == "rank1":
        return 1.0
    if kind == "full_rank":
        return 0.25
    if kind == "PS":
        v = np.diag([1.0, 1.0, 1.0, -3.0])
        v = v / math.sqrt(float(np.trace(v.conj().T @ v).real))
        return float(np.trace((v.conj().T @ v) @ (v.conj().T @ v)).real)
    raise ValueError(kind)


def main():
    print(f"Lambda0 = {Lambda0:.6e} GeV")
    print(f"M*      = {M_star:.6e} GeV")
    print(f"v'_C    = {v_C:.6e} GeV")
    print(f"v'_C / mu_meet_ref = {v_C / mu_meet_ref:.4f}")
    for kind in ("rank1", "full_rank", "PS"):
        t4 = direction_t4(kind)
        corr = v_C * (1.0 / t4) ** 0.25
        print(f"  {kind:<10} t4={t4:.4f}  v_corr={corr:.6e}  ratio={corr / mu_meet_ref:.3f}")
    print(f"M_X (projective) = Lambda0 = {Lambda0:.6e} GeV")
    assert 0.5 < v_C / mu_meet_ref < 2.0
    print("OK")


if __name__ == "__main__":
    main()
