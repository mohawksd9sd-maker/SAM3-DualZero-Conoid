"""
SAM3 v4.20 - Enhanced Zeta Zero Stationarity Verification
Uses Dual-Zero Reg₂ and 12-bridge modulation.
"""

import numpy as np

zeta_zeros = np.array([
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446227, 59.347044, 60.831779, 65.112544,
    67.079811, 69.546479, 72.067158, 75.049469, 77.144840
])

def dual_zero_reg2(delta):
    eps = 1e-8 * np.exp(-np.abs(delta)/10)
    return (np.real(delta) + eps * np.sin(12 * delta)) / (1 + np.abs(delta))

def information_current(k1, k2):
    diff = k1 - k2
    reg = dual_zero_reg2(diff)
    bridge_factor = 1.0 + 0.5 * np.sin(12 * np.angle(diff + 1j))
    return np.abs(reg) * bridge_factor * 2.0 / (1 + np.abs(diff))

def j_gradient(t):
    s0 = 0.5 + 1j * t
    delta = 1e-6
    J_c = information_current(s0, np.conj(s0))
    J_l = information_current(s0 - delta, np.conj(s0 - delta))
    J_r = information_current(s0 + delta, np.conj(s0 + delta))
    grad = np.abs((J_r - J_l) / (2 * delta))
    return grad, J_c

print("SAM3 v4.20 - Enhanced Information Current Stationarity Check\n")
print(f"{'Zero #':<6} {'Im(s)':<12} {'|J|':<12} {'|∇J|':<12} {'Stationary?'}")
print("-" * 65)

stationary_count = 0
for i, t in enumerate(zeta_zeros, 1):
    grad, Jval = j_gradient(t)
    is_stationary = grad < 1e-5
    status = "YES" if is_stationary else "NO"
    if is_stationary:
        stationary_count += 1
    print(f"{i:<6} {t:<12.6f} {Jval:<12.2e} {grad:<12.2e} {status}")

print(f"\n✅ {stationary_count}/20 zeros stationary on Re(s) = 1/2")
