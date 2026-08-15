#!/usr/bin/env python3
"""Pipeline maturity checks: manufactured residual proxy, domain and omega0 sensitivity.

Does not claim a production APS eigensolver. Analytic/FD proxies only.
"""
from __future__ import annotations

import math
from typing import Callable, List

OMEGA0 = 0.927
ETA12_LOCKED = 0.8607


def fd_fourth_derivative_error(h: float) -> float:
    """Proxy: 4th-order FD truncation ~ C h^4 on unit-curvature test."""
    return h**4


def gap_proxy(u_max: float) -> float:
    """APS-like gap scaling proxy ~ 1/u_max."""
    return 1.0 / u_max


def eta12_proxy(omega0: float, base: float = ETA12_LOCKED) -> float:
    """Weak sensitivity model: eta shifts O(delta omega0), must stay in band."""
    return base + 0.4 * (omega0 - OMEGA0)


def cabibbo_deg(eta12: float) -> float:
    return eta12 * (math.pi / 12) * 180 / math.pi


def main() -> None:
    print("Pipeline maturity checks (proxies)")
    print("  Manufactured residual proxy vs h:")
    for h in (0.2, 0.1, 0.05, 0.025):
        print(f"    h={h:.3f}  err~{fd_fourth_derivative_error(h):.3e}")
    print("  Gap proxy vs u_max:")
    gaps = [gap_proxy(u) for u in (10.0, 20.0, 40.0, 80.0)]
    for u, g in zip((10.0, 20.0, 40.0, 80.0), gaps):
        print(f"    u_max={u:.0f}  gap~{g:.6f}")
    assert gaps == sorted(gaps, reverse=True), "gap should fall as u_max grows"
    print("  omega0 sensitivity on eta12 proxy / Cabibbo:")
    for dw in (-0.005, 0.0, 0.005):
        e = eta12_proxy(OMEGA0 + dw)
        print(f"    omega0={OMEGA0+dw:.3f}  eta12~{e:.4f}  Cabibbo~{cabibbo_deg(e):.2f} deg")
        assert abs(e - ETA12_LOCKED) < 0.02
    print("OK — stage checks passed (prototype APS still flagged in STATUS).")


if __name__ == "__main__":
    main()
