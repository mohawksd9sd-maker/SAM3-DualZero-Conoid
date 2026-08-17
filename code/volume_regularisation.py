#!/usr/bin/env python3
"""Regularised internal volume + C0 finite part for locked hat metric."""
from __future__ import annotations

import math
import numpy as np


def I_corr(u: float, nv: int = 6000) -> float:
    v = np.linspace(0.0, 2.0 * math.pi, nv, endpoint=False)
    dv = 2.0 * math.pi / nv
    if u < 1e-15:
        return float(np.sum(2.0 * np.abs(np.cos(2.0 * v))) * dv)
    return float(np.sum(np.sqrt(u**2 + 4.0 * np.cos(2.0 * v) ** 2) - u) * dv)


def C0_proxy(U: float, nu: int | None = None) -> float:
    if nu is None:
        nu = max(4000, int(40 * U))
    us = np.linspace(0.0, U, nu)
    du = us[1] - us[0]
    integral = sum(I_corr(float(u)) for u in us) * du
    return float(integral - 2.0 * math.pi * math.log(U + 1.0))


def main() -> None:
    print("C0 finite-part diagnostics")
    for u in (10.0, 20.0, 50.0):
        print(f"  I({u})={I_corr(u):.6f}  2pi/u={2*math.pi/u:.6f}")
    for U in (100.0, 200.0, 400.0):
        print(f"  U={U:.0f}  C0~{C0_proxy(U):.6f}")
    target = 45 / (1024 * math.pi**2)
    C0 = C0_proxy(400.0)
    print(f"Target product={target:.8e}; implied C_SA*phi2~{target/C0:.8e}")
    print("OK")


if __name__ == "__main__":
    main()
