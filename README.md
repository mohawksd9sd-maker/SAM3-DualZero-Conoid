# SAM3-DualZero-Conoid

**A Dual-Zero Hyperreal Spectral Triple on the Right Conoid with Icosahedral Symmetry — Derivation of Gravity and the Standard Model**

**Status**: Theoretical framework – internally consistent, partially predictive, with new numerical support for the fermion sector (v4.20). Ready for further development and scrutiny.

**License**: [CC-BY-SA 4.0](LICENSE)

---

## Abstract

SAM3 v4.20 is a novel non-commutative geometric framework that attempts to unify gravity and the Standard Model from a single geometric object: the **infinite right conoid** equipped with a custom **Dual-Zero hyperreal algebra** and **12-bridge icosahedral symmetry**.

The model combines:
- An infinite ruled conoid manifold with 12 discrete bridges
- Finite algebra \(\mathcal{A}_F = \mathbb{C} \oplus \mathbb{H} \oplus M_3(\mathbb{C})\)
- Binary icosahedral symmetry \(2I\) acting on the bridges
- Dual-Zero hyperreal regularization

**Key Results**:
- Derives the Einstein–Hilbert term with explicit Newton’s constant \( G_N = \frac{3\pi \ell_0^2}{2} \)
- Reproduces the full SM gauge group and chiral fermions
- Naturally yields three generations from 12-bridge icosahedral symmetry
- Variational principle on the information current forces stationarity on the Riemann critical line \(\operatorname{Re}(s) = 1/2\)
- **New in v4.20**: Effective 1D Dirac spectrum on the 12 bridges + numerical Yukawa overlap integrals yielding realistic Cabibbo-like mixing (\(\sin\theta_{12} \approx 0.224\))

---

## 📄 Documents

- **[Full Paper — SAM3 v4.20](SAM3_v4.20_full_paper.tex)** (LaTeX)
- **[Mathematical Model Summary](math/SAM3_mathematical_model.md)**

---

## 🧪 Code & Verification

### Visualization
- `code/visualization/conoid_bridges.py` — 3D right conoid with 12 bridges
- `code/visualization/conoid_animation.py` — Rotating conoid with evolving |J| coloring

### Verification & Numerical Work
- `code/verification/zeta_stationarity_enhanced_500.py` — Stationarity check for first 500 zeta zeros
- `code/numerical/dirac_eigenmodes_conoid.py` — **New**: Computes effective Dirac spectrum and overlaps on the 12 bridges

### How to Run
```bash
# Stationarity check
python code/verification/zeta_stationarity_enhanced_500.py

# Conoid visualization
python code/visualization/conoid_bridges.py

# Dirac eigenmodes (new)
python code/numerical/dirac_eigenmodes_conoid.py
