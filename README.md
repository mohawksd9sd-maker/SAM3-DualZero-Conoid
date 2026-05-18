# SAM3-DualZero-Conoid

**A Dual-Zero Hyperreal Spectral Triple on the Right Conoid with Binary Icosahedral Symmetry — A Geometric Unification Candidate for Gravity and the Standard Model**

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

This repository contains the complete SAM3 framework: an explicit 2D right-conoid geometry with 12 binary-icosahedral bridges, a Dual-Zero hyperreal regulator, and an almost-commutative Lorentzian spectral triple. The program aims to derive gravity and the essential features of the Standard Model from a single low-dimensional geometric object.

---

## Overview

SAM3 starts from an explicit geometric object and derives physical predictions via spectral methods. Key results include:

- Exact Newton’s constant: \(G_N = \frac{64\pi \ell_0^2}{45}\)
- Exactly three chiral fermion generations from 2I representation theory
- Hierarchical Yukawa matrices and realistic CKM/PMNS mixing from geometric eigenmode overlaps
- Neutrino masses via geometric seesaw
- Higgs sector with quartic potential
- Consistent 4D lift via almost-commutative product

The framework emphasizes mathematical rigor (Paper 17), numerical robustness (Paper 18), and predictivity (Paper 19).

---

## Recent Major Upgrades (May 2026)

- **Paper 17**: Complete rigorous foundations — analytic Dirac properties, full Lorentzian NCG axiom verification (compact resolvent, bounded commutators), and essential uniqueness argument.
- **Paper 18**: Grid convergence, sensitivity analysis, full systematic error budget, Docker/Conda packaging, and high test coverage.
- **Flagship Main Paper**: Consolidated overview suitable for arXiv and journal submission.
- Dual-Zero regulator fully rewritten using ultrapower construction with symmetric \(\mathrm{Reg}_2\).
- All Higgs mass predictions standardized to \(126.2 \pm 2.05\) GeV (total theoretical uncertainty).

---

## Quick Start

1. Read the **[Flagship Main Paper](papers/SAM3_Flagship_Main_Paper.tex)** (recommended entry point).
2. Explore the detailed paper series in the `papers/` folder.
3. Reproduce numerical results (Docker support coming soon):

```bash
docker build -t sam3 . && docker run sam3
