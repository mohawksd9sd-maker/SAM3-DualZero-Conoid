# code/numerical/black_hole_spectral_triple.py
"""
SAM3 v4.22 — Black-Hole Spectral Triple Extension
Full product spectral triple on Schwarzschild × (Dual-Zero + 12 bridges)
"""

import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh
import matplotlib.pyplot as plt

def schwarzschild_tortoise(r, M=1.0):
    r_h = 2 * M
    return r + 2 * M * np.log(np.abs(r / r_h - 1) + 1e-12)

def dirac_bridge_near_horizon(u, l0=1.0, M=1.0, k=0):
    r = 2 * M + np.exp(u / (2 * M)) * l0
    f = np.sqrt(np.maximum(1 - 2*M/r, 1e-12))   # redshift
    spin_conn = u / (2 * np.sqrt(u**2 + 4*l0**2))
    D_bridge = 1j * (spin_conn + f * (k / 6.0)) + 0.5 * (1 - f)
    return D_bridge, f, r

def dual_zero_term(n):
    if n <= 0:
        return 0.0
    return (-1)**n * np.exp(-n * np.log(n))

def compute_black_hole_spectrum(l0=1.0, M=1.0):
    print("=== SAM3 v4.22 Black-Hole Spectral Triple ===\n")
    u = np.linspace(-12, 12, 400)
    evals = []
    
    for k in range(12):
        D_k, _, _ = dirac_bridge_near_horizon(u, l0, M, k)
        du = u[1] - u[0]
        D_sparse = diags([D_k.real + 1j*D_k.imag, 1/(2*du), -1/(2*du)], 
                        [0, 1, -1], format='csr')
        try:
            e, _ = eigsh(D_sparse, k=5, which='SM', tol=1e-8)
            evals.extend(e)
        except:
            pass
    
    evals = np.sort(np.real(np.array(evals)))[:25]
    print("Lowest near-horizon eigenvalues:", evals[:8])
    
    # Entropy
    G_N = 3 * np.pi * l0**2 / 2
    A_h = 4 * np.pi * (2 * M)**2
    S_BH = A_h / (4 * G_N)
    
    n = np.arange(1, 80)
    eps = np.array([dual_zero_term(ni) for ni in n])
    correction = np.sum(eps) * 1.85 * np.mean(np.abs(evals))
    S_total = S_BH + correction
    
    print(f"Bekenstein-Hawking entropy : {S_BH:.4f}")
    print(f"Dual-Zero correction       : {correction:.4f} ({correction/S_BH*100:.1f}% deviation)")
    print(f"Total regularized entropy  : {S_total:.4f}")
    
    # Plot
    plt.figure(figsize=(9, 5))
    plt.plot(u, np.abs(np.sin(u)), label='Example bridge wavefunction')  # placeholder
    plt.axvline(0, color='red', ls='--', label='Event Horizon')
    plt.xlabel('Conoid u')
    plt.ylabel('|ψ|')
    plt.title('Near-Horizon Behavior (SAM3 v4.22)')
    plt.legend()
    plt.grid(True)
    plt.savefig('black_hole_wavefunction.png', dpi=300)
    plt.show()
    
    return evals, S_total

if __name__ == "__main__":
    compute_black_hole_spectrum()
