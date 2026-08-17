#!/usr/bin/env python3
"""Fourier-sector projectors implementing the m_rho light/heavy split on 12 bridges."""
from __future__ import annotations

import numpy as np


def fourier_projector_m(m_set: set[int], N: int = 12) -> np.ndarray:
    P = np.zeros((N, N), dtype=complex)
    for k in range(N):
        m = min(k, N - k)
        if m in m_set:
            v = np.exp(2j * np.pi * k * np.arange(N) / N) / np.sqrt(N)
            P += np.outer(v, np.conj(v))
    return P


def main() -> None:
    P_light = fourier_projector_m({0, 1, 2})
    P_heavy = fourier_projector_m({3, 4, 5, 6})
    print("rank light", np.linalg.matrix_rank(P_light, tol=1e-8))
    print("rank heavy", np.linalg.matrix_rank(P_heavy, tol=1e-8))
    print("herm err", np.linalg.norm(P_light - P_light.conj().T))
    print("idem err", np.linalg.norm(P_light @ P_light - P_light))
    print("OK")


if __name__ == "__main__":
    main()
