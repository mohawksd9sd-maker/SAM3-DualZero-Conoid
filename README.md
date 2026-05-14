# SAM3-DualZero-Conoid

**A Dual-Zero Hyperreal Spectral Triple on the Right Conoid with Icosahedral Symmetry**  
**Unification of Gravity and the Standard Model**

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/mohawksd9sd-maker/SAM3-DualZero-Conoid)](https://github.com/mohawksd9sd-maker/SAM3-DualZero-Conoid/stargazers)

---

## Abstract

**SAM3** is a non-commutative geometric framework that unifies **classical gravity** and the **full Standard Model** from a single geometric object: the infinite right conoid manifold equipped with a novel **Dual-Zero hyperreal regulator** and **12-bridge binary icosahedral (2I) symmetry**.

The model derives:
- Einstein gravity with explicit Newton constant \( G_N = \frac{64\pi \ell_0^2}{45} \)
- Exactly three chiral generations from 2I representation theory
- Realistic Yukawa matrices and CKM/PMNS mixing angles from eigenmode overlaps
- Neutrino masses via natural seesaw
- Stable Higgs potential
- Variational mechanism favoring the Riemann critical line

Only two fundamental parameters: the conoid scale \(\ell_0\) and regulator strength \(\omega_0\).

**Current Status**: v4.23 (May 2026) — Mathematically consistent at the classical + perturbative quantum level, highly predictive, and fully reproducible.

---

## Key Features

- **Single geometric origin** for gravity, gauge fields, Higgs, three generations, and flavor physics
- **Dual-Zero hyperreal regularization** — solves positivity and information-loss issues
- **Full 2D Dirac operator** on non-compact conoid with proven self-adjointness and normalizability
- **Almost-commutative 4D lift** yielding standard Einstein–Hilbert + SM bosonic action
- **Quantized extension** (Paper 14) with Planck-suppressed corrections
- **Variational link** to the Riemann Hypothesis critical line (Paper 15)

---

## Documents & Papers

- **Main Overview Paper (v4.23)** → [`SAM3_v4.23_Main.pdf`](SAM3_v4.23_Main.pdf)
- **Full Paper Series** (16 papers) — see [`papers/`](papers/) folder
- **Mathematical Model Summary** — [`math/SAM3_mathematical_model.md`](math/SAM3_mathematical_model.md)
- **Appendix A: Spectral Triple Axioms** — verified in Lorentzian signature

---

## Figures (v4.23)

**Scalar Curvature on the Right Conoid**  
![Scalar Curvature](figures/curvature_surface.png)

**Asymptotic Decay of Lightest 2D Zero Mode**  
![Zero Mode Asymptotics](figures/asymptotic_zero_mode.png)

---

## Code & Reproducibility

All results are fully reproducible. Main pipeline scripts:

### Core Numerical Tools
- `code/numerical/full_2d_dirac_conoid.py` — 2D Dirac spectrum
- `code/numerical/overlap_integrals.py` — Yukawa + CKM/PMNS
- `code/verification/convergence_study.ipynb` — convergence & error bars
- `code/quantum_gravity/background_field_one_loop.py` — quantum corrections

### Visualization
- `code/visualization/conoid_bridges.py` — 3D conoid with bridges
- `code/visualization/conoid_animation.py` — animated curvature & information current

**How to Run** (full pipeline):
```bash
pip install -r requirements.txt
python code/numerical/full_2d_dirac_conoid.py
python code/numerical/overlap_integrals.py
SAM3-DualZero-Conoid/
├── papers/              # All 16 LaTeX papers (PDFs + .tex)
├── code/                # Full numerical + visualization pipeline
├── figures/             # High-resolution publication figures
├── math/                # Supplementary mathematical notes
├── results/             # Archived output matrices and plots
└── docs/                # Appendices and reading guides
@misc{sam3framework2026,
  author       = {Shawn Dykes},
  title        = {SAM3: Dual-Zero Hyperreal Spectral Triple on the Right Conoid},
  year         = {2026},
  howpublished = {\url{https://github.com/mohawksd9sd-maker/SAM3-DualZero-Conoid}},
  note         = {v4.23}
}
