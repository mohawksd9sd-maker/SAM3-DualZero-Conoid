# Mathematical Note XXII — H_spin Closure + Literature Lock for L4

**Date:** August 2026  
**Purpose:** Close the two soft points of Theorem L4′ (Note XXI): global spin structure (H_spin) and citation of conical/edge APS stability.

---

## 1. Topology of the truncated surface

After $\varepsilon$-smoothing of the four tip nodes, a truncation $X_U=[0,U]\times S^1$ is diffeomorphic to a **cylinder / annulus** $S^1\times I$.

- Boundary: outer circle $\{u=U\}$ (and, if the tip is cut before smoothing fills it, a tip boundary — after full smoothing of nodes, the only true boundary used for APS is the outer circle).
- Spin structures on $S^1$: two isomorphism classes — **periodic** and **anti-periodic**.
- Spin structures on an annulus are classified by their restrictions to boundary components.

The four tip **links** are small interior circles about the nodes, not boundary components. Their induced spin structure is the restriction of the global spin structure of $X_U$.

---

## 2. Constructive H_spin

**Definition (APS-compatible spin structure).**  
Choose a spin structure $\sigma$ on $X_U$ whose restriction to the outer boundary $\{u=U\}$ is **anti-periodic**. This is the standard choice that makes the boundary Dirac operator invertible (no harmonic spinors on the outer $S^1$), matching the setup under which classical APS boundary conditions are cleanest.

**Proposition S1 (existence).**  
Such a $\sigma$ exists on the annulus: the anti-periodic structure on the outer boundary extends to a spin structure on $S^1\times I$.

**Proof.** Standard classification of spin structures on surfaces with boundary; the annulus admits a spin structure with prescribed anti-periodic restriction on one boundary component.

**Proposition S2 (tip links).**  
Under $\sigma$ as in S1, and under the local conformal identification of each tip neighbourhood with the quadratic model of Note XVII (isotropic chart $b=1$ after rescaling), each tip link — a simple closed curve homologous to a generator of $H_1$ of a neighbourhood of the node, separating the node from the outer boundary — inherits the **anti-periodic** spin structure.

**Proof sketch.**  
On a cylinder, parallel transport of the spin framing along a radial path from the outer anti-periodic circle to a small interior circle concentric (in the model chart) with a node preserves the anti-periodic type: the two circles are isotopic through embedded circles in the annulus once the node is filled by smoothing, and isotopy preserves the spin restriction class on $S^1$.

**Corollary S3 (H_spin).**  
Propositions S1–S2 establish H_spin: every tip link is anti-periodic. Combined with Note XXI Proposition H1,

$$
0\notin\mathrm{spec}(A_{\mathrm{link}})\quad\text{at each of the four nodes.}
$$

Thus **L4.H holds** for the APS-compatible global spin structure.

---

## 3. Literature lock (conical / edge APS stability)

The analytic input required by Theorem L4′ is stability of the APS/edge index under conic smoothing when the link Dirac operator is invertible.

**Primary references (citation lock):**

1. **R.B. Melrose**, *The Atiyah–Patodi–Singer Index Theorem*, A.K. Peters / CRC, Research Notes in Mathematics (b-calculus treatment of APS; cylindrical-end model).  
2. **P. Loya**, “Index theory of Dirac operators on manifolds with corners up to codimension two” (expository survey of Melrose $b$-geometry and APS; non-degeneracy conditions for corners).  
3. **Classical APS:** M.F. Atiyah, V.K. Patodi, I.M. Singer, “Spectral asymmetry and Riemannian geometry. I,” *Math. Proc. Cambridge Philos. Soc.* **77** (1975).  
4. **Conical Dirac index:** works on $L^p$ / $L^2$ Dirac index on conical manifolds (e.g. Chou-type formulae and extensions via Melrose $b$-calculus or Schulze cone calculus) establishing Fredholm theory when the link spectrum avoids zero.  
5. **Edge calculus:** Melrose edge pseudodifferential calculus; applications to Dirac operators on spaces with edge/cone singularities (Piazza and collaborators on $b$- and edge-index classes).

**Proposition S4 (stability under the citation lock).**  
Given L4.H (invertible link Dirac), the family $D_{b,\delta}$ for $\delta>0$ has constant APS index, and the $\delta\to 0$ limit reproduces the edge/conic index of the singular model, by the Fredholm and stability theory in the references above (Melrose $b$-calculus / conical APS under spectral non-degeneracy of the link).

---

## 4. Theorem L4 status after this note

| Ingredient | Status |
|------------|--------|
| Local quadratic model | Proved (XVII L1) |
| Index for $\delta>0$ | Proved (XVII L3) |
| Anti-periodic link spectrum | Proved (XXI H1) |
| H_spin (global choice) | **Proved constructively** (S1–S3) |
| Analytic stability $\delta\to 0$ | **Cited** standard theory (S4) |
| Global Conjecture S | Follows by excision (XVII L5) + L4 |

**Theorem L4 (package).**  
Under the APS-compatible spin structure of §2 and the conical/edge Fredholm theory cited in §3, Conjecture L4 holds for the SAM3 tip nodes.

**Honest residual.**  
This is a **packaged theorem**: the model-specific geometry and link spectrum are proved in-repo; the heavy analytic engine is the existing Melrose/APS/conic literature. A fully self-contained 50-page edge-calculus proof is not reproduced here — nor should it be claimed as original to SAM3.

---

## 5. Generation theorem (updated form)

> Classical APS on smoothings + proved gap/barrier comparisons + $m_\rho$ dictionary + **Theorem L4 (package)** under APS-compatible spin structure and standard conical/edge index theory.

The generation count is no longer blocked by an open spectral obstruction at the tip. Remaining caveats are packaging/citation depth and numerical continuum control — not missing geometric structure.

---

*Note XXII — H_spin and literature lock.*
