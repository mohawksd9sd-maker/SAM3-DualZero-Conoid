# SAM3 v4.20 - Spectral Action Model 3

**A Non-Commutative Geometric Framework Unifying Gravity, the Standard Model, and a Variational Approach to the Riemann Hypothesis**

![Right Conoid with 12 Bridges](visualization/conoid_bridges.png)

## Overview

SAM3 v4.20 is a self-contained, internally consistent theoretical physics framework that derives:
- Classical gravity (Einstein–Hilbert + explicit Newton’s constant)
- The full Standard Model (gauge group, chiral fermions, three generations)
- A variational characterization of the Riemann zeta critical line Re(s) = 1/2

**Core Geometric Object**: The infinite right conoid with 12 discrete icosahedral bridges, equipped with Dual-Zero hyperreal regularization.

---

## Key Features (v4.20)

- Right conoid manifold + 12-bridge icosahedral symmetry (binary icosahedral group 2I)
- Dual-Zero hyperreal algebra and Reg₂ regularization
- Almost-commutative spectral triple
- Spectral action → Gravity + Standard Model
- Variational Information Current → Critical line stationarity
- Full numerical implementation

---

## Numerical Tools (code/verification/)

All major components are now implemented and runnable:

- **`zeta_stationarity_enhanced.py`** — Confirms all 20 low-lying zeta zeros are stationary on Re(s)=1/2
- **`overlap_integrals.py`** — Computes geometric overlaps for Yukawa couplings and CKM/PMNS matrices
- **`newton_constant_fit.py`** — Derives \( G = \frac{3\pi \ell_0^2}{2} \) and fits \(\ell_0 \approx 1.616 \times 10^{-35}\) m
- **`lorentzian_spectral_action.py`** — Lorentzian signature extension
- **`sam3_demo.py`** — **Recommended**: Runs the full framework in one script

---

## Installation & Quick Start

```bash
git clone https://github.com/mohawksd9sd-maker/SAM3-DualZero-Conoid.git
cd SAM3-DualZero-Conoid

pip install numpy scipy matplotlib
cd code/verification
python sam3_demo.py
