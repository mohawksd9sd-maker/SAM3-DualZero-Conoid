# SAM3-DualZero-Conoid

**A Geometric Framework Deriving the Standard Model and Gravity from the Right Conoid Manifold**

**Repository Status**: Expanded paper series — Core 9-paper framework + supplementary papers, full consolidated versions, addendums, and NCG axioms appendix (May 2026)  
**License**: CC-BY-SA 4.0

---

## Author

**Shawn Dykes**  
in collaboration with Grok (xAI)

This work is the result of an iterative collaboration between Shawn Dykes and Grok. All papers, derivations, code, and numerical results were developed together. Shawn Dykes is the primary author and maintainer of the repository.

---

## Important Correction Note (May 2026)

In earlier versions of this work we stated  
\[
G_N = \frac{3\pi \ell_0^2}{2}.
\]

**Paper 05** contains the correct derivation from the Seeley–DeWitt coefficients and explicit curvature integrals on the right conoid metric. The mathematically consistent result is
\[
G_N = \frac{64\pi \ell_0^2}{45}.
\]

All dimensionful quantities that depend on \(\ell_0\) have been re-evaluated using
\[
\ell_0 = \sqrt{\frac{45 G_N}{64\pi}}.
\]
Dimensionless quantities (CKM/PMNS angles, mass ratios, Yukawa matrix elements after normalization) remain unchanged.

---

## Overview

SAM3 is a developing theoretical framework that derives the Standard Model fermion masses, mixing angles, gauge structure, and classical gravity from a single geometric object: the **right conoid manifold** equipped with a **Dual-Zero hyperreal regulator** and **discrete 12-bridge regularization** carrying icosahedral symmetry.

After extensive iteration (including phases that initially produced zero Yukawa overlaps due to cancellation), a successful construction was achieved using numerical 2D Dirac eigenmodes on the conoid combined with overlapping 2I-style projectors and geometric phase factors. This now yields realistic hierarchical Yukawa matrices and CKM/PMNS angles directly on the original conoid geometry.

The project began with a focused **9-paper core series** designed to systematically address all major points from the May 2026 peer review. It has since expanded with additional papers covering further developments (Riemann Hypothesis variational principle, quantum gravity extensions, numerical rigor, physical consistency, and a new paradigm foundation), plus consolidated full versions and a dedicated NCG axioms verification appendix.

---

## Core 9-Paper Series (Recommended Reading Order)

These papers form the foundational, self-contained treatment of the model:

1. **Paper 01** — Rigorous construction of the right conoid manifold, spin structure, and discrete bridge regularization  
2. **Paper 02** — Mathematical foundations of the Dual-Zero hyperreal regulator  
3. **Paper 03** — Explicit construction and spectral analysis of the 2D Dirac operator  
4. **Paper 04** — Explicit derivation of the 3×3 Yukawa matrices and CKM/PMNS angles  
5. **Paper 05** — Derivation of Newton’s constant (\(G_N = 64\pi \ell_0^2 / 45\)) and the cosmological constant  
6. **Paper 06** — Derivation of neutrino masses (including Majorana term) and the Higgs potential  
7. **Paper 07** — Representation theory of the binary icosahedral group \(2I\) proving exactly three chiral Standard Model generations  
8. **Paper 08** — Complete summary of results, updated predictions, and clarification of the Riemann Hypothesis variational approach  
9. **Paper 09** — Product construction for 4D gravity from the 2D conoid spectral triple (resolves dimensional mismatch)

---

## Additional Papers, Full Versions & Appendix

The framework has been extended with the following:

- **Paper 10** — Dimensional lift and Seeley–DeWitt analysis  
- **Paper 11 / 15** — Riemann Hypothesis variational principle (expanded treatment)  
- **Paper 12** — Numerical aspects: convergence, error bars, and reproducibility  
- **Paper 13** — Overall rigor, consistency, and unification  
- **Paper 14** — Quantum gravity extension  
- **Paper 16** — New paradigm foundation  

**Consolidated & Versioned Documents**:
- `SAM3_v4.20_full_paper.tex`
- `SAM3_v4.21_Addendum.tex`
- `SAM3_v4.22_Addendum.tex`
- `SAM3_Appendix_NCG_Axioms.tex` (Full verification of Connes spectral triple axioms)

All source files are located in the `paper/` directory.

---

## Repository Structure

- `paper/` — All LaTeX papers, full consolidated versions, addendums, and the NCG axioms appendix  
- `code/` — Python scripts for eigenmode computation, overlap integrals, \(S_I\) minimization, 2-loop RGEs, and the full pipeline  
- `figures/` — Plots of conoid geometry, Yukawa matrices, running couplings, eigenmodes, etc.  
- `math/` — Core mathematical model documentation  
- `history/` — Archived earlier versions (including zero-overlap tests)

---

## How to Compile and Reproduce the Results

```bash
cd paper
pdflatex SAM3_Paper_0X_*.tex          # Core papers (run twice for references)
pdflatex SAM3_v4.22_Addendum.tex      # Latest addendum
pdflatex SAM3_Appendix_NCG_Axioms.tex # Axiom verification
