# SAM3-DualZero-Conoid

**A Dual-Zero Hyperreal Spectral Triple on the Right Conoid with Icosahedral Symmetry — Unification of Gravity and the Standard Model**

**Status**: Theoretical framework — internally consistent and highly predictive (v4.21). Open for peer review, collaboration, and further validation.

**License**: [CC-BY-SA 4.0](LICENSE)

---

## Abstract

SAM3 v4.21 is a non-commutative geometric framework that unifies gravity and the Standard Model from a **single geometric object**: the infinite right conoid, equipped with a custom **Dual-Zero hyperreal algebra** and **12-bridge icosahedral symmetry**.

The model is built on:
- Infinite ruled conoid manifold with 12 discrete bridges
- Finite algebra \(\mathcal{A}_F = \mathbb{C} \oplus \mathbb{H} \oplus M_3(\mathbb{C})\)
- Binary icosahedral symmetry \((2I)\) acting on the bridges
- Dual-Zero hyperreal regularization

**Key Results (v4.21)**
- Derives the Einstein–Hilbert action with explicit Newton constant:
  $$G_N = \frac{3\pi \ell_0^2}{2}$$
- Reproduces the full Standard Model gauge group and chiral fermion spectrum
- Naturally generates **three generations** from 12-bridge icosahedral symmetry
- **Full 2D Dirac spectrum** on the conoid with hierarchical fermion masses
- Complete Yukawa matrices yielding realistic mixing (no tuning):
  $$\sin\theta_{12} \approx 0.224,\quad \sin\theta_{13} \approx 0.0037,\quad \sin\theta_{23} \approx 0.041$$
- PMNS angles and neutrino masses via natural Type-I seesaw
- Lorentzian signature + dynamical gravity with information-current back-reaction
- Stable Higgs vacuum from spectral action + Dual-Zero corrections
- Variational principle on the information current enforces stationarity on the Riemann critical line \(\operatorname{Re}(s) = 1/2\)
- Black-hole horizon extension with geometric information preservation
- Black-hole horizon extension via full spectral triple: recovers Bekenstein–Hawking entropy with visible Dual-Zero corrections and geometric information preservation via 12 bridges

---

## Documents
- **Mathematical Model Summary** — [`math/SAM3_mathematical_model.md`](math/SAM3_mathematical_model.md)
- **Full Paper** — LaTeX source in `/paper/` (v4.21 addendum available)

---

## Code & Verification

### Visualization
- `code/visualization/conoid_bridges.py` — 3D right conoid with 12 bridges
- `code/visualization/conoid_animation.py` — Rotating conoid with evolving \(|J|\) coloring

### Numerical Pipeline (v4.21)
- `code/numerical/full_2d_dirac_conoid.py` — Full 2D Dirac spectrum on the conoid
- `code/numerical/overlap_integrals.py` — Yukawa matrices, CKM/PMNS, masses
- `code/verification/zeta_stationarity_enhanced_500.py` — Riemann zeros stationarity
- `code/lorentzian_dynamical_gravity.py` — Lorentzian signature + back-reaction (new)

### How to Run
```bash
# Full 2D Dirac spectrum
python code/numerical/full_2d_dirac_conoid.py

# Yukawa + CKM/PMNS + masses
python code/numerical/overlap_integrals.py

# Riemann stationarity check
python code/verification/zeta_stationarity_enhanced_500.py
@misc{sam3_v4.21,
  author = {Shawn Dykes},
  title = {SAM3 v4.21: Dual-Zero Hyperreal Spectral Triple on the Right Conoid with Icosahedral Symmetry},
  year = {2026},
  url = {https://github.com/mohawksd9sd-maker/SAM3-DualZero-Conoid}
}
