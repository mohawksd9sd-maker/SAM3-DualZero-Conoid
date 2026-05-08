# SAM3-DualZero-Conoid

**A Dual-Zero Hyperreal Spectral Triple on the Right Conoid with Icosahedral Symmetry — Derivation of Gravity and the Standard Model**

**Status**: Theoretical framework – internally consistent, partially predictive, ready for further development and numerical verification.

**License**: CC-BY-SA 4.0

---

## Abstract

SAM3 (Spectral Action Model 3) is a novel non-commutative geometric framework that attempts to derive the Standard Model of particle physics and classical gravity from a single geometric object: the **right conoid surface** equipped with a custom **Dual-Zero hyperreal algebra** and 12-bridge icosahedral symmetry.

The model combines:
- An infinite ruled conoid manifold \(M_c\) with 12 discrete bridges
- A finite non-commutative algebra \(\mathcal{A}_F = \mathbb{C} \oplus \mathbb{H} \oplus M_3(\mathbb{C})\)
- Binary icosahedral symmetry \(2I\) acting as a Grand Symmetry / family symmetry
- A novel **Dual-Zero hyperreal regularization** that resolves finite-vs-infinite spectrum issues

**Key results**:
- Derives Einstein–Hilbert gravity + explicit Newton’s constant \(G\)
- Reproduces the full SM gauge group, chiral fermions, and three generations
- Predicts CKM/PMNS mixing as geometric overlap integrals
- Provides a variational proof that the information current \(J\) is stationary on the critical line \(\operatorname{Re}(s) = 1/2\)

---

## 📄 Full Paper

- [Complete paper (LaTeX)](paper/SAM3_v4.19_full.tex)
- [Short abstract](paper/SAM3_v4.19_abstract.tex)

---

## 🧪 Code & Verification

- `code/verification/zeta_stationarity.py` → Checks stationarity at the first 20 zeta zeros
- `code/visualization/conoid_bridges.py` → 3D plot of the right conoid with 12 bridges

Run example:
```bash
cd code/verification
python zeta_stationarity.py
