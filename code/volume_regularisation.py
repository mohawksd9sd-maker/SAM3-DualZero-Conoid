#!/usr/bin/env python3
"""Regularised internal volume for locked hat metric f=sqrt(u^2+4 cos^2(2v))."""
from __future__ import annotations

import math
import numpy as np


def fhat(u: np.ndarray, v: np.ndarray) -> np.ndarray:
    return np.sqrt(u**2 + 4.0 * np.cos(2.0 * v) ** 2)


def volume(U: float, nu: int = 800, nv: int = 800) -> float:
    u = np.linspace(0.0, U, nu)
    v = np.linspace(0.0, 2.0 * math.pi, nv, endpoint=False)
    du = u[1] - u[0]
    dv = v[1] - v[0]
    UU, VV = np.meshgrid(u, v, indexing="ij")
    return float(np.sum(fhat(UU, VV)) * du * dv)


def angular_f_minus_u(u: float, nv: int = 4000) -> float:
    v = np.linspace(0.0, 2.0 * math.pi, nv, endpoint=False)
    dv = 2.0 * math.pi / nv
    return float(np.sum(fhat(np.array(u), v) - u) * dv)


def main() -> None:
    print("Locked hat-metric volume diagnostics")
    for U in (1.0, 2.0, 5.0, 10.0, 20.0):
        V = volume(U)
        print(f"  U={U:5.1f}  Vol={V:12.6f}  Vol/(pi U^2)={V/(math.pi*U*U):.6f}")
    print("Asymptotic int(f-u)dv ~ 2*pi/u:")
    for u in (10.0, 20.0, 50.0):
        I = angular_f_minus_u(u)
        print(f"  u={u:5.1f}  I={I:.6f}  2pi/u={2*math.pi/u:.6f}")
    target = 45 / (1024 * math.pi**2)
    print(f"Target C_SA*phi2*Vol_reg for locked alpha = {target:.8e}")
    print("OK")


if __name__ == "__main__":
    main()
