#!/usr/bin/env python3
"""SAM3 continuum eta from tip heat-kernel + 2I characters (no tuning).

Law:
  k_g = A_g**(phi**2)
  eta0_ij = cos(2*pi/12) * 2*sqrt(ki*kj)/(ki+kj)
  mix = 1/2 - cos(2*pi/5) = (3-sqrt(5))/4
  eta_12 = eta0_12, eta_23 = eta0_23
  eta_13 = eta0_13 + mix*(1 - eta0_13)

Reference archive lock: (0.8607, 0.5439, 0.4789)
"""
from __future__ import annotations

import math

PHI = (1 + 5**0.5) / 2
A_TIP = (1.0, 1.13, 2.7798)
LOCKED = (0.8607, 0.5439, 0.4789)


def derived_eta(A=A_TIP):
    k = [a ** (PHI**2) for a in A]
    aw = math.cos(2 * math.pi / 12)

    def o(i, j):
        return aw * 2 * math.sqrt(k[i] * k[j]) / (k[i] + k[j])

    e12, e13, e23 = o(0, 1), o(0, 2), o(1, 2)
    mix = 0.5 - math.cos(2 * math.pi / 5)
    e13 = e13 + mix * (1.0 - e13)
    return (e12, e13, e23), mix, k


def rms(vec, target=LOCKED):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(vec, target)) / 3)


def main():
    eta, mix, k = derived_eta()
    print("k =", [round(x, 6) for x in k])
    print("mix = 1/2 - cos(2*pi/5) =", round(mix, 12))
    print("eta derived =", tuple(round(x, 6) for x in eta))
    print("eta locked  =", LOCKED)
    print("RMS =", round(rms(eta), 6))
    theta12 = math.degrees(eta[0] * math.pi / 12)
    print("theta12 from eta12*pi/12 =", round(theta12, 4), "deg")
    assert abs(mix - (3 - 5**0.5) / 4) < 1e-14
    assert rms(eta) < 0.01
    print("OK")


if __name__ == "__main__":
    main()
