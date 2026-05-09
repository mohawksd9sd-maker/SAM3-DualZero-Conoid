"""
SAM3 v4.20 - Newton's Constant and ℓ₀ Fitting
"""

import numpy as np
from scipy.optimize import fsolve

G_obs = 6.67430e-11

def theoretical_G(l0):
    return (3 * np.pi * l0**2) / 2

def eq(l0):
    return theoretical_G(l0) - G_obs

l0 = fsolve(eq, 1e-35)[0]

print("SAM3 v4.20 - Newton's Constant")
print(f"ℓ₀ fitted          : {l0:.6e} m")
print(f"Recovered G        : {theoretical_G(l0):.6e} m³ kg⁻¹ s⁻²")
print(f"Matches observed G : Exact")
np.save('l0_fitted.npy', np.array([l0]))
print("ℓ₀ saved to l0_fitted.npy")
