# SAM3-DualZero-Conoid

**A Geometric Framework Deriving the Standard Model and Gravity from the Right Conoid Manifold**

**Repository Status**: Complete 9-paper series (May 2026)  
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

SAM3 is a developing theoretical framework that attempts to derive the Standard Model fermion masses, mixing angles, and classical gravity from a single geometric object: the right conoid manifold equipped with a Dual-Zero hyperreal regulator and discrete 12-bridge regularization.

The work began with the original right conoid geometry. After many iterations that produced zero Yukawa overlaps due to phase cancellation, a successful method was found: numerical 2D Dirac eigenmodes + overlapping 2I-style projectors + geometric phase factors. This approach now yields realistic hierarchical Yukawa matrices and CKM/PMNS angles on the **original conoid geometry**.

The full series consists of 9 self-contained papers that address every major concern raised in the May 2026 peer review.

---

## Paper Series (Recommended Reading Order)

1. **Paper 01** – Rigorous construction of the right conoid manifold, spin structure, and discrete bridge regularization  
2. **Paper 02** – Mathematical foundations of the Dual-Zero hyperreal regulator  
3. **Paper 03** – Explicit construction and spectral analysis of the 2D Dirac operator  
4. **Paper 04** – Explicit derivation of the 3×3 Yukawa matrices and CKM/PMNS angles  
5. **Paper 05** – Derivation of Newton’s constant (\(G_N = 64\pi \ell_0^2 / 45\)) and the cosmological constant  
6. **Paper 06** – Derivation of neutrino masses (including Majorana term) and the Higgs potential  
7. **Paper 07** – Representation theory of the binary icosahedral group \(2I\) proving exactly three chiral Standard Model generations  
8. **Paper 08** – Complete summary of results, updated predictions, and clarification of the Riemann Hypothesis variational approach  
9. **Paper 09** – Product construction for 4D gravity from the 2D conoid spectral triple (fixes dimensional mismatch)

All papers are in the `papers/` folder.

---

## Repository Structure

- `papers/` — All 9 LaTeX papers (compile each with `pdflatex`)
- `code/` — Python scripts for eigenmodes, overlap integrals, minimization of \(S_I\), 2-loop RGEs, etc.
- `figures/` — Plots of conoid geometry, Yukawa matrices, running couplings, etc.
- `history/` — Archived earlier versions showing zero-overlap tests on the conoid

---

## How to Compile and Reproduce the Results

```bash
cd papers
pdflatex SAM3_Paper_0X_*.tex   # run twice for references
