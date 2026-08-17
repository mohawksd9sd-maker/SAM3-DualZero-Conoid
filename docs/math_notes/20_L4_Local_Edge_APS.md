# Mathematical Note XX — Conjecture L4: Local Edge-APS Limit

**Date:** August 2026  
**Purpose:** Attack the last major analytic gate: $\lim_{\delta\to 0}\mathrm{Index}_{\mathrm{APS}}(D_{b,\delta})$ on the local tip-node model.

---

## 1. Local model (locked)

Near a tip node, to leading order (Note XVII Lemma L1):

$$
ds^2 = du^2 + (u^2 + b^2\varepsilon^2)\,d\varepsilon^2,
\qquad b = 4\ell_0,
\quad (u,\varepsilon)\in[0,\infty)\times\mathbb{R}.
$$

Smoothing:

$$
f_\delta^2 = u^2 + b^2\varepsilon^2 + \delta^2,\qquad \delta>0.
$$

**Conjecture L4.**  
On compact truncations with APS (or Atiyah–Patodi–Singer type) boundary conditions on the artificial outer boundary,

$$
I_b := \lim_{\delta\to 0}\mathrm{Index}_{\mathrm{APS}}(D_{b,\delta})
$$

exists in $\mathbb{Z}$, is independent of the path $\delta\downarrow 0$ through positive smoothings, and equals the edge-calculus index of the singular metric $f_0^2=u^2+b^2\varepsilon^2$.

---

## 2. Why this is standard-shaped

The singular locus $\{u=\varepsilon=0\}$ is a **point** in the 2D model chart. In polar-type coordinates

$$
u = \sqrt{u^2+b^2\varepsilon^2},\qquad \tan\theta = \frac{b\varepsilon}{u},
$$

the metric is quasi-isometric to a **cone** (or incomplete edge) with smooth cross-section an interval in $\theta$. Conical and edge Dirac operators have a developed Fredholm/index theory (Melrose $b$-calculus, edge calculus, works of Piazza, Vertman, Lesch, Hartmann–Lesch–Vertman, et al.).

**Proposition L4.1 (reduction to cone class).**  
If the model $(u,\varepsilon)$ metric is quasi-isometric to a metric with a conical singularity of order 1 at the origin, with compact link, then Conjecture L4 is an instance of the known stability of APS/edge indices under conic smoothing, subject to the usual spectral condition on the link (no zero eigenvalue of the tangential operator, or projected APS conditions).

**Proof idea.** Quasi-isometry preserves the edge structure up to lower-order terms controlled in the edge calculus; smoothing $\delta>0$ is a standard regularisation whose index is constant for $\delta>0$ (Note XVII L3) and matches the singular index when the link spectrum avoids zero or APS projections are held fixed.

---

## 3. Link operator and spectral condition

On the link (angular $\theta$ direction at fixed small $\nu$), the tangential Dirac / spin operator $A_{\mathrm{link}}$ is an ordinary 1D operator on a closed interval with suitable boundary conditions induced by the global surface orientation.

**Hypothesis L4.H (link non-degeneracy).**  
$0\notin\mathrm{spec}(A_{\mathrm{link}})$, or the APS projection is defined with respect to a spectral cut that is stable under the smoothing.

When L4.H holds, the edge index is deformation-invariant and the $\delta\to 0$ limit is standard.

**Residual.** Explicit diagonalisation of $A_{\mathrm{link}}$ for $b=4\ell_0$ on the exact quadratic model — finite 1D computation, not a new theory.

---

## 4. Four nodes and global index

Global singular limit (Conjecture S) =

$$
I_{\mathrm{global}} = I_{\mathrm{bulk}} + \sum_{j=1}^{4} I_b^{(j)},
$$

with each local contribution equal by symmetry of the four nodes of $\cos(2v)=0$. Prop L5 (Note XVII): smoothing independence follows once each $I_b^{(j)}$ exists.

---

## 5. What is proved vs conjectural here

| Item | Status |
|------|--------|
| Local quadratic model | Proved (L1) |
| Index defined for $\delta>0$ | Proved (L3) |
| Reduction to cone/edge class | Prop L4.1 (standard-shaped) |
| Link non-degeneracy L4.H | **Hypothesis** (1D check residual) |
| Full edge-calculus citation write-up | Packaging residual |
| $\delta\to 0$ limit | **Conjecture L4** — reduced to L4.H + standard edge theory |

---

## 6. Professional stance for external readers

Conjecture L4 is **not** an ad hoc singularity claim. It is the assertion that the SAM3 tip nodes fall under existing conical/edge APS theory once the link spectrum condition is verified. The remaining work is:

1. Compute $\mathrm{spec}(A_{\mathrm{link}})$ on the quadratic model (explicit).  
2. Cite the matching theorem in the edge-calculus literature.  
3. Glue four nodes (Prop L5).

Until (1)–(2) are typed against a specific reference theorem, L4 stays labelled **conjecture**, not theorem.

---

*Note XX — L4 local edge APS.*
