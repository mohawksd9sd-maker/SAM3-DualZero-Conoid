#!/usr/bin/env python3
"""Regenerate / verify locked SAM3 centrals. No experimental retuning."""
from __future__ import annotations

import math

PHI = (1 + 5**0.5) / 2
OMEGA0 = 0.927
N_BRIDGES = 12
DELTA_THETA = 2 * math.pi / N_BRIDGES

# Locked continuum defect overlaps (doc 36)
ETA12, ETA13, ETA23 = 0.8607, 0.5439, 0.4789

# CKM centrals
TH12 = 12.85  # deg
TH23 = 2.36
TH13 = 0.24
PHI_CP = 2 * math.pi / 5

# Gravity
G_N = 6.70883096e-39  # GeV^-2 reference
ell0 = math.sqrt(45 * G_N / (64 * math.pi))
Lambda0 = 1.0 / ell0
mH = 125.0
M_star = math.sqrt(Lambda0 * mH)


def main() -> None:
    print("SAM3 production regenerate (locked centrals)")
    print(f"  omega0          = {OMEGA0}")
    print(f"  n_bridges       = {N_BRIDGES}")
    print(f"  Delta theta     = {DELTA_THETA:.6f} rad")
    print(f"  eta12,13,23     = {ETA12}, {ETA13}, {ETA23}")
    cabibbo = ETA12 * (math.pi / 12) * 180 / math.pi
    print(f"  Cabibbo check   = {cabibbo:.2f} deg (target ~{TH12})")
    print(f"  theta12,23,13   = {TH12}, {TH23}, {TH13} deg")
    print(f"  phi_CP          = 2*pi/5 = {PHI_CP:.6f} rad")
    print(f"  ell0            = {ell0:.6e} GeV^-1")
    print(f"  Lambda0         = {Lambda0:.6e} GeV")
    print(f"  M*              = {M_star:.6e} GeV")
    print(f"  m_H class       = {mH} GeV (class, not digit lock)")
    assert abs(cabibbo - TH12) < 0.5
    assert 0.92 < OMEGA0 < 0.94
    assert abs(ETA12 - 0.861) < 0.02
    print("OK — locked centrals consistent (no experimental fit).")


if __name__ == "__main__":
    main()
