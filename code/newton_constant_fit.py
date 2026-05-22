"""
SAM3 v4.25 - Newton's Constant and ℓ₀ Fitting
Uses the exact analytic expression from the spectral action / Seeley-DeWitt a4 coefficient.
"""

import numpy as np
from scipy.optimize import fsolve

# Observed Newton's constant (m³ kg⁻¹ s⁻²)
G_obs = 6.67430e-11

def theoretical_G(l0):
    """Exact analytic expression from SAM3 spectral action on the conoid."""
    return (64 * np.pi * l0**2) / 45

def eq(l0):
    """Solve theoretical_G(l0) = G_obs for l0."""
    return theoretical_G(l0) - G_obs

# Solve for ℓ₀ (initial guess near Planck scale)
l0_guess = 1e-35
l0 = fsolve(eq, l0_guess)[0]

print("=== SAM3 v4.25 - Newton's Constant ===")
print(f"ℓ₀ fitted          : {l0:.6e} m")
print(f"Recovered G        : {theoretical_G(l0):.6e} m³ kg⁻¹ s⁻²")
print(f"Matches observed G : Exact (by construction)")
print(f"ℓ₀ in natural units: {l0 * 1.973e-13:.6e} GeV⁻¹ (ħc conversion)")

# Save for use in other scripts
np.save('l0_fitted.npy', np.array([l0]))
print("\nℓ₀ saved to l0_fitted.npy")
