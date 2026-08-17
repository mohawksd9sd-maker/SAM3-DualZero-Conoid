#!/usr/bin/env python3
"""Production channel pipeline: tip isolation under m_rho dictionary.

Outsider-runnable. Exit 0 iff isolation (3 light, 0 heavy) holds for all U.
"""
from __future__ import annotations

import json
import sys
import numpy as np
from scipy.linalg import eigh_tridiagonal

U_LIST = (10.0, 20.0, 40.0, 80.0)
N_GRID = 4000
LIGHT = (0, 1, 2)
HEAVY = (3, 4, 5, 6)


def channel_e0(m: float, U: float, n: int = N_GRID) -> float:
    u = np.linspace(1e-4, U, n + 2)[1:-1]
    du = u[1] - u[0]
    V = (m**2) / (u + 1e-4)**2 + 1.0 / (u**2 + 1.0)**2
    diag = 2.0 / du**2 + V
    off = np.full(n - 1, -1.0 / du**2)
    return float(
        eigh_tridiagonal(diag, off, select="i", select_range=(0, 0), eigvals_only=True)[0]
    )


def run() -> dict:
    rows = []
    ok = True
    for U in U_LIST:
        light = [channel_e0(m, U) for m in LIGHT]
        heavy = [channel_e0(m, U) for m in HEAVY]
        gap = min(heavy) - max(light)
        tau = 0.5 * (max(light) + min(heavy))
        n_light = sum(1 for e in light if e < tau)
        n_heavy = sum(1 for e in heavy if e < tau)
        if n_light != 3 or n_heavy != 0 or gap <= 0:
            ok = False
        rows.append(
            {
                "U": U,
                "light_max": max(light),
                "heavy_min": min(heavy),
                "gap": gap,
                "n_light_below_tau": n_light,
                "n_heavy_below_tau": n_heavy,
            }
        )
    return {"ok": ok, "rows": rows}


def main() -> None:
    report = run()
    print(json.dumps(report, indent=2))
    sys.exit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
