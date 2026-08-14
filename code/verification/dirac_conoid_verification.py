"""
SAM3 — Numerical verification framework for the 2D Dirac operator on the right conoid

- Discretization sketch on a finite grid
- Lowest-eigenvalue workflow hooks
- Asymptotic check helpers for light modes
- Dual-Zero weight sequence helper

Note: This is a verification framework / prototype. Authoritative continuum residual
and gap→0 locks live in docs/hardening/10_Continuum_Dirac_Residual_Lock.md.
Promoted from nested path code/verification/code/verification/ during Fix 5 cleanup.
"""

import numpy as np
from scipy.sparse import diags, eye, csr_matrix

# ========================= PARAMETERS =========================
L0 = 1.0
N_u = 200
N_v = 64
u_max = 20.0
du = u_max / (N_u - 1)
dv = np.pi / (2 * N_v)
omega0 = 1e-6

# Grid
u = np.linspace(du / 2, u_max, N_u)
v = np.linspace(0, np.pi / 2, N_v, endpoint=False)
U, V = np.meshgrid(u, v, indexing="ij")
f = np.sqrt(U**2 + 16 * L0**2 * np.cos(2 * V) ** 2)


def build_dirac_matrix_placeholder():
    """Placeholder sparse layout for documentation / further development."""
    D_u = diags([-1 / (2 * du), 0, 1 / (2 * du)], [-1, 0, 1], shape=(N_u, N_u)).tocsr()
    D_v = diags([-1 / (2 * dv), 0, 1 / (2 * dv)], [-1, 0, 1], shape=(N_v, N_v)).tocsr()
    D_v = D_v.tolil()
    D_v[0, -1] = -1 / (2 * dv)
    D_v[-1, 0] = 1 / (2 * dv)
    D_v = D_v.tocsr()
    print("Dirac matrix construction framework ready.")
    print(f"Grid size: {N_u} x {N_v} → spinor dim scale = {2 * N_u * N_v}")
    return D_u, D_v


def check_asymptotics(norm_u):
    """Fit log-log slope of radial density at large u (expect ~ -1 for 1/u decay of density measures)."""
    mask = u > u_max * 0.6
    slope, _ = np.polyfit(np.log(u[mask]), np.log(np.maximum(norm_u[mask], 1e-30)), 1)
    print(f"Asymptotic slope: {slope:.4f}")
    return slope


def dual_zero_weights(n_max=1000, omega0_local=None):
    w0 = omega0 if omega0_local is None else omega0_local
    n = np.arange(1, n_max + 1)
    return w0 * ((-1) ** n) * n ** (-n)


if __name__ == "__main__":
    build_dirac_matrix_placeholder()
    _ = dual_zero_weights(20)
    print("Verification modules loaded. See docs/hardening/10 for continuum residual lock.")
