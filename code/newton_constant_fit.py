#!/usr/bin/env python3
"""Display the convention-locked G_N normalisation. This is not a fit.

November 2026 honesty fix: the previous version solved G_theory(ℓ0)=G_obs
for ℓ0 and then reported that G_theory matched G_obs "exactly by construction".
That is a tautology, not a test of the prefactor 64π/45.

What is actually known (math notes 09 and 16; core paper):
  * Spectral action / Seeley–DeWitt a2 implies G_N = α ℓ0².
  * The number 64π/45 is a convention lock, equivalent to fixing
    𝒩 = 45/(1024 π²). It is not scheme-free and is not independently derived.
"""
from __future__ import annotations

import math

# CODATA-style reference in GeV^{-2}, for display of ℓ0 only.
# Using it does not test the theoretical prefactor.
G_OBS_GEV2 = 6.70883096e-39
ALPHA_LOCKED = 64.0 * math.pi / 45.0  # convention, not a derivation


def ell0_from_convention(gn: float = G_OBS_GEV2, alpha: float = ALPHA_LOCKED) -> float:
    """ℓ0 such that α ℓ0² = G_obs. This *defines* ℓ0 once α and G_obs are given."""
    return math.sqrt(gn / alpha)


def main() -> None:
    ell0 = ell0_from_convention()
    print("Newton constant — convention display, not a test")
    print(f"  recorded normalisation: G_N = (64π/45) ℓ0²")
    print(f"  status: convention lock (not scheme-free)")
    print(f"  G_obs (display only) = {G_OBS_GEV2:.8e} GeV^{{-2}}")
    print(f"  ℓ0 implied by that convention = {ell0:.8e} GeV^{{-1}}")
    print("  This last line is a unit conversion, not evidence that 64π/45 is correct.")


if __name__ == "__main__":
    main()
