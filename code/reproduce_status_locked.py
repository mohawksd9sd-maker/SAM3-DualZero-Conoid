#!/usr/bin/env python3
"""Historical STATUS locker — largely tautological.

November 2026: this script mostly asserts hardcoded constants against
 themselves (ω0, η, θ, m_H band, φ=2π/5, the G_N prefactor).
 cabibbo_from_eta is θ12 := η12 · π/12, so the "check" is circular.
 m_H is inserted by hand as 125 and then checked to lie in [124,127].

It is retained so older documentation still has a runnable file.
Authoritative reproduction of the core paper is:

    python code/core_reproducibility.py
    pytest -q
"""
from __future__ import annotations

import math
import json
from dataclasses import dataclass, asdict
from typing import Dict, Any

# ---------------------------------------------------------------------------
# Frozen centrals (STATUS / docs 35–36)
# ---------------------------------------------------------------------------
OMEGA0 = 0.927
N_BRIDGES = 12
DELTA_THETA = 2 * math.pi / N_BRIDGES
TIP_COEFF = 4  # locked: f^2 = u^2 + TIP_COEFF * ell0^2 * cos^2(2v)
ETA12, ETA13, ETA23 = 0.8607, 0.5439, 0.4789
TH12, TH23, TH13 = 12.85, 2.36, 0.24  # degrees
PHI_CP = 2 * math.pi / 5
KAPPA_RATIO = 0.5
C_G = (6 / 5, 1.0, 4 / 5)
G_N = 6.70883096e-39  # GeV^-2 reference for ell0 display
MH_CLASS = 125.0
MH_BAND = (124.0, 127.0)


def ell0_from_GN(gn: float = G_N) -> float:
    return math.sqrt(45 * gn / (64 * math.pi))


def cabibbo_from_eta(eta12: float) -> float:
    return eta12 * (math.pi / 12) * 180.0 / math.pi


def heatkernel_eta_proxy() -> tuple[float, float, float]:
    """Doc 32 continuum law proxy (not a fit)."""
    k = (1.0, 1.5, 2.2)
    eta0 = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            if i == j:
                eta0[i][j] = 1.0
            else:
                eta0[i][j] = math.cos(2 * math.pi / 12) * 2 * math.sqrt(k[i] * k[j]) / (k[i] + k[j])
    mix13 = 0.5 - math.cos(2 * math.pi / 5)
    eta0[0][2] += mix13 * (1 - eta0[0][2])
    eta0[2][0] = eta0[0][2]
    return eta0[0][1], eta0[0][2], eta0[1][2]


def rms_eta(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)) / 3.0)


@dataclass
class Report:
    omega0: float
    n_bridges: int
    delta_theta: float
    tip_coeff: int
    eta12: float
    eta13: float
    eta23: float
    theta12_deg: float
    theta23_deg: float
    theta13_deg: float
    phi_cp: float
    kappa_u_over_kappa_d: float
    C_g: tuple
    ell0_GeV_inv: float
    Lambda0_GeV: float
    Mstar_GeV: float
    mH_class_GeV: float
    cabibbo_check_deg: float
    eta_hk_rms: float
    GN_formula: str


def build_report() -> Report:
    ell0 = ell0_from_GN()
    Lambda0 = 1.0 / ell0
    Mstar = math.sqrt(Lambda0 * MH_CLASS)
    hk = heatkernel_eta_proxy()
    locked_eta = (ETA12, ETA13, ETA23)
    return Report(
        omega0=OMEGA0,
        n_bridges=N_BRIDGES,
        delta_theta=DELTA_THETA,
        tip_coeff=TIP_COEFF,
        eta12=ETA12,
        eta13=ETA13,
        eta23=ETA23,
        theta12_deg=TH12,
        theta23_deg=TH23,
        theta13_deg=TH13,
        phi_cp=PHI_CP,
        kappa_u_over_kappa_d=KAPPA_RATIO,
        C_g=C_G,
        ell0_GeV_inv=ell0,
        Lambda0_GeV=Lambda0,
        Mstar_GeV=Mstar,
        mH_class_GeV=MH_CLASS,
        cabibbo_check_deg=cabibbo_from_eta(ETA12),
        eta_hk_rms=rms_eta(hk, locked_eta),
        GN_formula="G_N = 64*pi*ell0^2/45",
    )


def assert_locked(r: Report) -> None:
    assert r.tip_coeff == 4, "metric tip coefficient must be 4, not 16"
    assert abs(r.omega0 - 0.927) < 1e-9
    assert r.n_bridges == 12
    assert abs(r.cabibbo_check_deg - TH12) < 0.5
    assert abs(r.phi_cp - 2 * math.pi / 5) < 1e-12
    assert abs(r.kappa_u_over_kappa_d - 0.5) < 1e-12
    assert r.C_g[0] == 6 / 5 and r.C_g[2] == 4 / 5
    assert MH_BAND[0] <= r.mH_class_GeV <= MH_BAND[1]
    assert r.eta_hk_rms < 0.05  # stage tolerance; doc 32 ~0.008 on refined law
    # omega0 sensitivity must not be used to retune angles
    assert 0.92 <= OMEGA0 <= 0.94


def main() -> None:
    r = build_report()
    # The assertions below only check that hardcoded constants were copied
    # consistently. They are not evidence those numbers follow from the metric.
    assert_locked(r)
    print("HISTORICAL STATUS locker — tautological consistency dump")
    print(json.dumps(asdict(r), indent=2))
    print("WARNING: this script does not independently derive ω0, η, θ, m_H,")
    print("or the 64π/45 prefactor. It echoes values stored at the top of the file.")
    print("Use code/core_reproducibility.py and pytest for the core paper.")


if __name__ == "__main__":
    main()
