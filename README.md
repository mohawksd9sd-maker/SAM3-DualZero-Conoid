# SAM3-DualZero-Conoid

**A Dual-Zero Hyperreal Spectral Triple on the Right Conoid with Icosahedral Symmetry — Derivation of Gravity and the Standard Model**

**Status**: Theoretical framework – internally consistent, partially predictive, ready for further development and numerical verification.

**License**: [CC-BY-SA 4.0](LICENSE)

---

## Abstract

SAM3 (Spectral Action Model 3) is a novel non-commutative geometric framework that derives the Standard Model of particle physics and classical gravity from a single geometric object: the **right conoid surface** equipped with a custom **Dual-Zero hyperreal algebra** and **12-bridge icosahedral symmetry**.

The model combines:
- An infinite ruled conoid manifold \( M_c \) with 12 discrete bridges
- A finite non-commutative algebra \( \mathcal{A}_F = \mathbb{C} \oplus \mathbb{H} \oplus M_3(\mathbb{C}) \)
- Binary icosahedral symmetry \( 2I \) acting as a Grand Symmetry / family symmetry
- A novel **Dual-Zero hyperreal regularization** that resolves finite-vs-infinite spectrum issues

**Key results**:
- Derives Einstein–Hilbert gravity with explicit Newton’s constant \( G \)
- Reproduces the full SM gauge group, chiral fermions, and three generations
- Predicts CKM/PMNS mixing matrices as geometric overlap integrals
- Provides a variational proof that the information current \( |J| \) is stationary on the critical line \( \operatorname{Re}(s) = 1/2 \) of the Riemann zeta function

---

## 📄 Full Paper

- **[Complete paper v4.20 (LaTeX)](paper/SAM3_v4.20_full_paper.tex)**
- **[Short abstract](paper/SAM3_v4.20_abstract.tex)** (if available)

---

## 🧪 Code & Verification

- `code/visualization/conoid_bridges.py` → Generates 3D right conoid with 12 bridges + overlap heatmap
- `code/verification/zeta_stationarity.py` → Verifies stationarity of the information current at the first 20 zeta zeros

**Run example**:
```bash
cd code/verification
python zeta_stationarity.py

@misc{sam3_v4.20,
  author = {Shawn Dykes},
  title = {SAM3 v4.20: Dual-Zero Hyperreal Spectral Triple on the Right Conoid with Icosahedral Symmetry},
  year = {2026},
  url = {https://github.com/mohawksd9sd-maker/SAM3-DualZero-Conoid}
}
