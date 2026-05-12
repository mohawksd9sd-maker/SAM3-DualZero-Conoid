# Series Correction Note (May 2026)

**Important Update on Newton’s Constant**

In earlier versions of this work (v4.22 and before), we stated
\[
G_N = \frac{3\pi \ell_0^2}{2}.
\]

**Paper 05** contains the correct derivation from the Seeley–DeWitt coefficients and the explicit curvature integrals on the right conoid metric. The mathematically consistent result is
\[
G_N = \frac{64\pi \ell_0^2}{45}.
\]

**Consequence for all dimensionful quantities**:
All numerical results that depend on the fundamental length scale \(\ell_0\) (masses, neutrino mass sum, dark matter cross-section, proton lifetime, etc.) must be re-evaluated using the updated relation
\[
\ell_0 = \sqrt{\frac{45 G_N}{64\pi}}.
\]

Dimensionless quantities (CKM/PMNS angles, mass ratios, Yukawa matrix elements after normalization) remain unchanged.

This correction has been applied to all subsequent papers in the series.
# SAM3-DualZero-Conoid
**A Dual-Zero Hyperreal Spectral Triple on the Right Conoid with Icosahedral Symmetry — Unification of Gravity and the Standard Model**

**Status**: Theoretical framework — internally consistent and highly predictive (**v4.20 + v4.22 Addendum**). Open for peer review, collaboration, and further validation.

**License**: [CC-BY-SA 4.0](LICENSE)

---

## Abstract

SAM3 v4.20 is a non-commutative geometric framework that unifies gravity and the Standard Model from a **single geometric object**: the infinite right conoid, equipped with a custom **Dual-Zero hyperreal algebra** and **12-bridge icosahedral symmetry**.

The model is built on:
- Infinite ruled conoid manifold with 12 discrete bridges
- Finite algebra \(\mathcal{A}_F = \mathbb{C} \oplus \mathbb{H} \oplus M_3(\mathbb{C})\)
- Binary icosahedral symmetry \((2I)\) acting on the bridges
- Dual-Zero hyperreal regularization

### Key Results (v4.20)

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

### v4.22 Addendum (May 2026) — New Developments

- **Full 2D zero-mode asymptotic analysis**: Proved that the lightest modes of the complete 2D Dirac operator are normalizable with \(\psi_+(u) \sim u^{-1/2}\) decay.
- **Direct inclusion of Dual-Zero hyperreal shifts** into the full 2D Dirac operator (exponentially suppressed corrections: \(|\delta\lambda_0| \lesssim 10^{-10}\)).
- **Higher-order Seeley–DeWitt coefficients** (\(a_4\) and higher) computed — shown to converge rapidly, confirming a controlled effective field theory.

---

## Documents

- **Full Merged Paper (v4.22)**: [`SAM3_v4.22_full_paper.pdf`](SAM3_v4.22_full_paper.pdf)  
  **LaTeX source**: [`SAM3_v4.22_full_paper.tex`](SAM3_v4.22_full_paper.tex)
- **Mathematical Model Summary** — [`math/SAM3_mathematical_model.md`](math/SAM3_mathematical_model.md)

---

## Figures (v4.22)

**Scalar Curvature Surface**  
![Scalar Curvature R(u,v) on the Right Conoid](figures/curvature_surface.png)

**Asymptotic Behavior of the 2D Zero Mode**  
![Asymptotic 2D Zero Mode ψ₊(u) ∼ u^{-1/2}](figures/asymptotic_zero_mode.png)

---

## Code & Verification

### Visualization
- `code/visualization/conoid_bridges.py` — 3D right conoid with 12 bridges
- `code/visualization/conoid_animation.py` — Rotating conoid with evolving \(|J|\) coloring

### Numerical Pipeline
- `code/numerical/full_2d_dirac_conoid.py` — Full 2D Dirac spectrum
- `code/numerical/overlap_integrals.py` — Yukawa matrices, CKM/PMNS, masses
- `code/verification/zeta_stationarity_enhanced_500.py` — Riemann zeros stationarity
- `code/lorentzian_dynamical_gravity.py` — Lorentzian signature + back-reaction

### How to Run
```bash
# Full 2D Dirac spectrum
python code/numerical/full_2d_dirac_conoid.py

# Yukawa + CKM/PMNS + masses
python code/numerical/overlap_integrals.py

# Riemann stationarity check
python code/verification/zeta_stationarity_enhanced_500.py
