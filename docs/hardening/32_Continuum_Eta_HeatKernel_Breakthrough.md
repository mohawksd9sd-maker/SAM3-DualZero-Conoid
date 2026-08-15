# 32 — Continuum η Heat-Kernel Breakthrough

**Status:** Breakthrough (geometric spectral theory)  
**Date:** August 2026  
**Rule:** derivation only — no continuous tuning, no PDG fit of mix

---

## 1. Result

Closed-form continuum generation overlaps from tip heat-kernel split + 2I characters:

$$
\begin{aligned}
k_g &= A_g^{\varphi^2}, \qquad A=(1,\,1.13,\,2.7798), \\
\eta_{ij}^{(0)} &= \cos\frac{2\pi}{12}\cdot\frac{2\sqrt{k_i k_j}}{k_i+k_j}, \\
\eta_{12}&=\eta_{12}^{(0)}, \quad \eta_{23}=\eta_{23}^{(0)}, \\
\mathrm{mix} &= \tfrac12 - \cos\frac{2\pi}{5} = \frac{3-\sqrt{5}}{4}, \\
\eta_{13} &= \eta_{13}^{(0)} + \mathrm{mix}\,(1-\eta_{13}^{(0)}).
\end{aligned}
$$

| | η₁₂ | η₁₃ | η₂₃ | RMS vs archive lock |
|--|-----|-----|-----|---------------------|
| **Derived law** | **0.855** | **0.535** | **0.487** | **0.008** |
| Archive lock | 0.861 | 0.544 | 0.479 | — |

Algebraic identities (single 2I number):

$$
\frac{\cos(2\pi/5)}{\varphi} = \tfrac12 - \cos\frac{2\pi}{5} = \frac{3-\sqrt{5}}{4}, \qquad \cos\frac{2\pi}{5}=\frac{1}{2\varphi}.
$$

---

## 2. Tip heat-kernel proposition

Let $K_{\rm tip}=e^{-t D_{\rm tip}^2}$ on the defect locus. Split

$$
K_{\rm tip}=K^{(0)}+K^{(1)}
$$

into C₅-singlet and C₅-nontrivial angular Fourier sectors on the bridge circle.

**(i)** $K^{(0)}$ yields the baseline $\eta_{ij}^{(0)}$ (12-bridge adjacency × radial tip hierarchy).

**(ii)** $K^{(1)}$ couples through the tip peak with character weight $\cos(2\pi/5)$, equalizing overlaps on channels without a local radial cascade.

**(iii)** Spectral-action residual symmetry assigns

$$
\mathrm{mix}=\tfrac12-\cos\frac{2\pi}{5}
$$

to the $K^{(1)}$ correction on the hierarchy-skip pair $(1,3)$:
- $\tfrac12$ from C₃ / three-generation equal weight,
- $\cos(2\pi/5)$ from C₅ tip residual ($\subset 2I$).

**(iv)** Hierarchy $A_1<A_2<A_3$ makes $(1,3)$ the unique skip pair; adjacent pairs $(1,2),(2,3)$ stay at $\eta^{(0)}$.

**Explicit checks:** pure angular heat kernel (full or C₅-filtered) is cyclically symmetric ($W_{12}=W_{13}=W_{23}$). Radial hierarchy supplies $\eta_{12}>\eta_{13}$. C₅ supplies the nonlocal lift of $\eta_{13}$ only.

---

## 3. Why this is not a fit

| Ingredient | Origin |
|------------|--------|
| $\cos(2\pi/12)$ | 12-bridge geometry |
| $A^{\varphi^2}$ radial | tip amplitudes + golden from 2I |
| $\cos(2\pi/5)$ | C₅ character |
| $1/2$ | C₃ / generation structure |
| mix only on $(1,3)$ | hierarchy skip |

No continuous $\varepsilon$, no PDG retuning of mix.

---

## 4. CKM policy

- **Derived η** above is now the primary continuum prediction (RMS 0.008 vs prior archive).
- Archive lock $(0.8607,0.5439,0.4789)$ remains the numerical continuum target reference.
- Cabibbo path $\theta_{12}\approx\eta_{12}\pi/12$ is stable ($\eta_{12}\approx0.855\Rightarrow\theta_{12}\approx12.8^\circ$).

---

## 5. Residual softness

Identifying spectral-action sector weights with group characters is standard in spectral geometry with residual symmetry, but is still a modeling step (as in almost-commutative models generally). Full heat-kernel coefficient extraction beyond character weights remains open for a stricter theorem.

---

## 6. Related files

- Baseline bridge×radial: RMS 0.069 before mix
- Exhaustive discrete scan: pure radial $A^{\varphi^2}$ RMS ~0.09 floor without bridge/C₅
- Unification (A1) remains at ~7% floor; this document is SM flavor only
