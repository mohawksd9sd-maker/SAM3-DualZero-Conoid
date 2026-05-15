# SAM3-DualZero-Conoid

**A Dual-Zero Hyperreal Spectral Triple on the Right Conoid with Icosahedral Symmetry — Derivation of Gravity and the Standard Model**

This repository contains the complete SAM3 framework: a geometric unification program that derives both classical gravity and the Standard Model from a single geometric object — the **right conoid** equipped with a **Dual-Zero hyperreal spectral triple** and **binary icosahedral (2I) symmetry**.

## Overview

SAM3 constructs an almost-commutative spectral triple over a 2D right conoid manifold. Using the rigorously defined **Dual-Zero hyperreal regulator** (Paper 02), the framework derives:

- Newton’s constant: \( G_N = \frac{64\pi \ell_0^2}{45} \)
- Three chiral fermion generations via \(2I\) symmetry
- Hierarchical Yukawa couplings and CKM/PMNS mixing angles from regularized Dirac eigenmode overlaps
- Neutrino masses and Higgs potential
- A consistent 4D lift via almost-commutative product construction

The project emphasizes mathematical rigor, numerical reproducibility, and iterative improvement.

## Recent Updates (May 2026)

- **Paper 02** has been fully rewritten with a rigorous construction of the Dual-Zero hyperreal regulator using the ultrapower and the symmetric regularization operator \(\mathrm{Reg}_2\).
- All subsequent papers (03, 04, 05, 10, 12, 13) have been updated to consistently use the regularized operator \(D_\varepsilon\).
- The previous nilpotent-ring approach to the regulator has been deprecated.
- Newton’s constant has been corrected to the current value \( G_N = \frac{64\pi \ell_0^2}{45} \).
- Paper 13 now provides an overall assessment of rigor and lists remaining tasks.
- The Appendix has been updated to reflect the regularized Lorentzian spectral triple.

## Repository Structure
paper/          # All LaTeX papers and appendix
code/           # Numerical pipeline and verification scripts
figures/        # Plots and visualizations
math/           # Mathematical model documentation
history/        # Archived earlier versions

## Main Papers

| Paper | Focus | Status |
|-------|-------|--------|
| Paper 02 | Dual-Zero Hyperreal Regulator | Rigorously updated (ultrapower + \(\mathrm{Reg}_2\)) |
| Paper 03 | Dirac Operator on the Conoid | Updated with regularized operator |
| Paper 04 | Yukawa Derivations | Updated with regularized eigenmodes |
| Paper 05 | Derivation of Gravity | Corrected \(G_N\), regulator-consistent |
| Paper 10 | Dimensional Lift & Lorentzian Axioms | Updated |
| Paper 12 | Numerical Implementation & Convergence | Updated |
| Paper 13 | Overall Rigor and Unification Status | Updated |
| Appendix A | Connes Spectral Triple Axioms | Updated for regularized Lorentzian case |

## Reproducibility

All numerical results are produced using the regularized operator \(D_\varepsilon\). The pipeline is documented in the `code/` directory and is deterministic once grid parameters are fixed. Convergence and error analysis are provided in Paper 12.

## Current Status

The framework has reached a substantially higher level of mathematical consistency following the rigorous treatment of the regulator in Paper 02. The core structures (Dirac operator, spectral action, dimensional lift) are now well-founded.

**Main remaining tasks** include:
- Increasing predictivity in the flavor sector (Paper 04)
- Further verification of Lorentzian axioms
- Sharpening phenomenological predictions

## License

This work is licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

## Citation

```bibtex
@misc{sam3_2026,
  author       = {Shawn Dykes},
  title        = {SAM3-DualZero-Conoid},
  year         = {2026},
  howpublished = {\url{https://github.com/mohawksd9sd-maker/SAM3-DualZero-Conoid}},
  note         = {In collaboration with Grok (xAI)}
}
