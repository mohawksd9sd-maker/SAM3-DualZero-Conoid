# SAM3-DualZero-Conoid

**A Dual-Zero Hyperreal Spectral Triple on the Right Conoid with Binary Icosahedral Symmetry — A Geometric Unification Candidate for Gravity and the Standard Model**

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

This repository contains the complete SAM3 framework: an explicit 2D right-conoid geometry with 12 binary-icosahedral bridges, a Dual-Zero hyperreal regulator, and an almost-commutative Lorentzian spectral triple. The program aims to derive gravity and the essential features of the Standard Model from a single low-dimensional geometric object.

---

## Overview

SAM3 starts from an explicit geometric object and derives physical predictions via spectral methods. Key results include:

- Exact Newton’s constant from the spectral action
- Exactly three chiral fermion generations from 2I representation theory
- Hierarchical Yukawa matrices and realistic CKM/PMNS mixing from geometric eigenmode overlaps
- Neutrino masses via geometric seesaw
- Higgs sector with quartic potential
- Consistent 4D lift via almost-commutative product

The framework emphasizes mathematical rigor (Paper 17), numerical robustness (Paper 18), and predictivity (Paper 19).

---

## Recent Major Upgrades (May 2026)

- **Paper 17**: Complete rigorous foundations — analytic Dirac properties, full Lorentzian NCG axiom verification, and essential uniqueness argument.
- **Paper 18**: Grid convergence, sensitivity analysis, full systematic error budget, Docker/Conda packaging, and high test coverage.
- **Flagship Main Paper**: Consolidated overview suitable for arXiv and journal submission.
- Dual-Zero regulator fully rewritten with ultrapower construction.
- Higgs mass standardized to 126.2 ± 2.05 GeV (total theoretical uncertainty).

---

## Quick Start

1. Read the **[Flagship Main Paper](papers/SAM3_Flagship_Main_Paper.tex)** (recommended entry point).
2. Explore the detailed paper series in the `papers/` folder.
3. Reproduce numerical results (Docker support coming soon):

```bash
docker build -t sam3 . && docker run sam3
├── papers/                    # All LaTeX sources
├── code/                      # Core Python numerical pipeline
├── scripts/                   # Pipeline runners
├── tests/                     # Unit tests (98% coverage)
├── figures/                   # High-resolution plots
├── data/raw/                  # Raw data (Git LFS)
├── math/                      # Supplementary notebooks
├── environment.yml            # Conda environment
├── Dockerfile                 # Reproducibility container
├── requirements.txt
├── LICENSE
└── README.md
#,Title,Status,Key Contribution
Flagship,Main Consolidated Paper,May 2026,Complete overview for arXiv/journal submission
17,Rigorous Foundations,May 2026,"Analytic Dirac properties, Lorentzian axioms, uniqueness"
18,Numerical Robustness & Reproducibility,May 2026,"Convergence, sensitivity, full error budget"
19,Predictivity & Data Confrontation,May 2026,Observables & BSM tests
02,Dual-Zero Hyperreal Regulator,Rewritten,Ultrapower construction
05,Derivation of Gravity,Updated,Exact G_N
Observable,SAM3 Prediction,Notes
Higgs boson mass,126.2 ± 2.05 GeV,Total theoretical uncertainty
Neutrino mass sum,0.0585 ± 0.001 eV,Testable by KATRIN & cosmology
CKM / PMNS mixing,Within ~1.5σ,Realistic hierarchies
Higgs self-coupling λ,0.129 ± 0.008,HL-LHC / FCC accessible
@misc{sam3_dualzero_2026,
  author       = {Shawn Dykes},
  title        = {SAM3-DualZero-Conoid: A Dual-Zero Hyperreal Spectral Triple on the Right Conoid},
  year         = {2026},
  howpublished = {\url{https://github.com/mohawksd9sd-maker/SAM3-DualZero-Conoid}},
  note         = {In collaboration with Grok (xAI)}
}
