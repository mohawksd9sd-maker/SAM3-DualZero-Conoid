#!/usr/bin/env python3
"""SAM3 unification residual: VL_Q at M*=sqrt(Lambda0*m_H) and 12*M*.

Derivation-only scales. Reports one-loop and two-loop residuals.
Does not claim M_X = mu_meet.
"""
from __future__ import annotations

import math
import numpy as np

PHI = (1 + 5**0.5) / 2
G_N = 6.70883096e-39  # GeV^-2
ell0 = math.sqrt(45 * G_N / (64 * math.pi))
Lambda0 = 1.0 / ell0
mH = 125.0
M_star = math.sqrt(Lambda0 * mH)
M2 = 12 * M_star
MZ = 91.1876
b_SM = np.array([41 / 10, -19 / 6, -7.0])
inv0 = np.array([59.0, 29.6, 8.5])
B_SM = np.array(
    [[199 / 50, 27 / 10, 44 / 5], [9 / 10, 35 / 6, 12], [11 / 10, 9 / 2, -26]],
    dtype=float,
)


def db_VL_Q() -> np.ndarray:
    Y = 1.0 / 3.0
    return 2 * np.array([0.5 * Y**2 * 2 * 3, 0.5 * 3, 0.5 * 2])


def run(mu_end: float, thresholds, two_loop: bool = True, nsteps: int = 2000) -> np.ndarray:
    inv = inv0.astype(float).copy()
    mus = np.logspace(math.log10(MZ), math.log10(mu_end), nsteps)
    th = sorted(thresholds, key=lambda x: x[0])
    for i in range(len(mus) - 1):
        mu, mu2 = mus[i], mus[i + 1]
        dt = math.log(mu2 / mu)
        b = b_SM.copy()
        for m, db in th:
            if mu >= m:
                b = b + db
        if two_loop:
            alpha = 1.0 / np.maximum(inv, 1e-12)
            inv = inv + (-b / (2 * math.pi) - (B_SM @ alpha) / (8 * math.pi**2)) * dt
        else:
            inv = inv - b / (2 * math.pi) * dt
    return inv


def best_residual(thresholds, two_loop: bool = True):
    best, best_mu, best_inv = 999.0, None, None
    for logmu in np.linspace(13, 17.5, 200):
        mu = 10**logmu
        inv = run(mu, thresholds, two_loop=two_loop)
        res = 100 * (max(inv) - min(inv)) / (abs(np.mean(inv)) + 1e-30)
        if res < best:
            best, best_mu, best_inv = res, mu, inv.copy()
    return best, best_mu, best_inv


def main():
    th = [(M_star, db_VL_Q()), (M2, db_VL_Q())]
    print(f"Lambda0 = {Lambda0:.6e} GeV")
    print(f"M*      = {M_star:.6e} GeV")
    print(f"12 M*   = {M2:.6e} GeV")
    print(f"M_X     = Lambda0 (forced UV; not mu_meet)")
    r1, mu1, _ = best_residual(th, two_loop=False)
    r2, mu2, inv2 = best_residual(th, two_loop=True)
    print(f"One-loop residual = {r1:.3f}% at mu ≈ {mu1:.3e} GeV")
    print(f"Two-loop residual = {r2:.3f}% at mu ≈ {mu2:.3e} GeV")
    assert r2 < 5.0, "two-loop residual left precision class"
    print("OK")


if __name__ == "__main__":
    main()
