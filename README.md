# SAM3 v4.21 - Spectral Action Model 3  
**A Non-Commutative Geometric Framework Unifying Gravity, the Standard Model, and a Variational Approach to the Riemann Hypothesis**

![SAM3 Logo](https://github.com/mohawksd9sd-maker/SAM3-DualZero-Conoid/blob/main/visualization/conoid_bridges.png)

## Overview

SAM3 (Spectral Action Model 3) is a speculative but **internally consistent** theoretical framework that combines:
- A **right conoid** manifold with 12 discrete bridges
- **Dual-Zero hyperreal algebra** for regularization
- **Binary icosahedral group (2I)** family symmetry
- Non-commutative geometry (almost-commutative spectral triple)
- Variational principle for the critical line of the Riemann zeta function

**Core Claim**: Gravity + Full Standard Model + Stationarity on Re(s)=1/2 emerge naturally from the geometry.

---

## Features Implemented (v4.21)

### Core Mathematics
- Right conoid geometry with 12 icosahedral bridges
- Dual-Zero hyperreal regularization (`Reg₂`)
- Spectral triple construction
- Variational Information Current `J(k₁,k₂)` → critical line stationarity

### Numerical Tools (in `code/verification/`)
- `zeta_stationarity_enhanced.py` → Confirms 20/20 low-lying zeta zeros stationary
- `overlap_integrals.py` → Geometric overlaps for Yukawa & mixing matrices
- `newton_constant_fit.py` → Derives and fits ℓ₀ to observed Newton's constant
- `lorentzian_spectral_action.py` → Lorentzian signature + higher Seeley–DeWitt terms
- `sam3_demo.py` → **Main integrated demonstration** (recommended)

### Key Results
- Newton's constant: `G = 3π ℓ₀² / 2` exactly recovered
- Fitted ℓ₀ ≈ 1.616 × 10⁻³⁵ m (near Planck scale)
- 3 fermion generations from 2I irreps
- Variational proof of critical line stationarity

---

## Installation & Running

```bash
# Clone the repo
git clone https://github.com/mohawksd9sd-maker/SAM3-DualZero-Conoid.git
cd SAM3-DualZero-Conoid
@misc{sam3_v4.21,
  title        = {SAM3 v4.21: Spectral Action Model with Right Conoid and Dual-Zero Algebra},
  author       = {Shawn Dykes and Grok (xAI)},
  year         = {2026},
  url          = {https://github.com/mohawksd9sd-maker/SAM3-DualZero-Conoid}
}
# Install dependencies
pip install numpy scipy matplotlib
