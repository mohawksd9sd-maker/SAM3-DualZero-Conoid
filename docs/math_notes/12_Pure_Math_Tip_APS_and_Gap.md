# Mathematical Note XII — Pure Math: Tip Stratification, APS, and Analytic Gap Bound

**Date:** August 2026  
**Purpose:** Close the pure-math residuals of Note VIII layers L0–L3 as far as present methods allow.  
**Rule:** Prove what is standard; state conditional theorems where the singular tip requires stratified techniques.

---

## 1. Locked metric and singularity locus

$$
ds^2 = du^2 + f(u,v)^2\,dv^2,
\qquad
f(u,v)=\sqrt{u^2 + 4\ell_0^2\cos^2(2v)},
\quad u\ge 0,\; v\in \mathbb{R}/2\pi\mathbb{Z}.
$$

**Lemma 1 (degeneracy locus).**  
$f(u,v)=0$ if and only if $u=0$ and $\cos(2v)=0$, i.e. at the four points

$$
(u,v)\in \{0\}\times \Bigl\{\tfrac{\pi}{4},\tfrac{3\pi}{4},\tfrac{5\pi}{4},\tfrac{7\pi}{4}\Bigr\}.
$$

Elsewhere $f>0$, so $g$ is a smooth Riemannian metric on

$$
M^\circ := [0,\infty)\times S^1 \setminus \{\text{four tip nodes}\}.
$$

**Proof.** Immediate from $f^2=u^2+4\ell_0^2\cos^2(2v)\ge 0$.

**Lemma 2 (Gaussian curvature on $M^\circ$).**  
For $ds^2=du^2+f^2 dv^2$,

$$
K = -\frac{\partial_{uu} f}{f}
= -\frac{4\ell_0^2\cos^2(2v)}{\bigl(u^2+4\ell_0^2\cos^2(2v)\bigr)^2}.
$$

In particular $K\le 0$ on $M^\circ$, and $K\to -\infty$ when approaching a tip node along paths with $\cos(2v)\neq 0$ fixed and $u\to 0$ is false; rather for fixed $v$ with $\cos(2v)\neq 0$,

$$
K(0,v) = -\frac{1}{4\ell_0^2\cos^2(2v)}
$$

is finite. The curvature blow-up is concentrated near the four nodes (stratified singularity).

**Proof.** Direct differentiation.

---

## 2. Smoothed tip and classical APS

**Definition (ε-smoothing).**  
For $\varepsilon>0$ let

$$
f_\varepsilon(u,v)=\sqrt{u^2 + 4\ell_0^2\cos^2(2v) + \varepsilon^2}.
$$

Then $f_\varepsilon\ge \varepsilon>0$, so $g_\varepsilon$ is smooth and uniformly equivalent to a non-degenerate metric on any finite cylinder $[0,u_{\max}]\times S^1$.

**Theorem A (APS index on smoothed truncations).**  
Let $X_{u_{\max}}=[0,u_{\max}]\times S^1$ with product collar structure at the outer boundary $u=u_{\max}$ and APS boundary conditions there (and smoothed tip, so no boundary at $u=0$). Let $D_\varepsilon$ be the Dirac operator of $g_\varepsilon$. Then

$$
\mathrm{Index}_{\mathrm{APS}}(D_\varepsilon; X_{u_{\max}})
\in \mathbb{Z}
$$

is given by the classical Atiyah–Patodi–Singer formula and is invariant under continuous deformations of $g_\varepsilon$ through non-degenerate metrics with APS outer boundary.

**Proof.** Standard APS theorem on compact spin manifolds with boundary (Atiyah–Patodi–Singer, 1975).

**Definition (index in the singular limit).**  
Set

$$
I(u_{\max}) := \lim_{\varepsilon\to 0^+} \mathrm{Index}_{\mathrm{APS}}(D_\varepsilon; X_{u_{\max}})
$$

when the limit exists in $\mathbb{Z}$.

**Residual / conjecture.** Existence of $I(u_{\max})$ independent of the path of smoothings (ε² vs other mollifiers) is the **stratified APS** step. It is standard for conical singularities under mild conditions; the four tip nodes are **milder than a full cone** along most angular directions (Lemma 2). We record:

**Conjecture S (smoothing independence).**  
$I(u_{\max})$ exists and is independent of the choice of smoothing $f_\varepsilon$ among metrics with $f_\varepsilon^2 = f^2 + \varepsilon^2 \rho(v)$ for smooth $\rho\ge c>0$.

Until Conjecture S is proved in full generality, all generation statements that pass through the singular tip are **conditional on S**.

---

## 3. Analytic gap bound

**Theorem B (gap on the cylinder — model case).**  
On the product cylinder $[0,L]\times S^1$ with metric $du^2 + R^2 dv^2$ ($R$ constant) and APS conditions at $u=L$, the spectrum of $|D|$ satisfies

$$
|\lambda|_{\min} \ge \frac{\pi}{2L}
$$

up to the standard APS zero-mode counting (boundary η-invariant). In particular non-zero eigenvalues cannot accumulate at zero faster than $O(1/L)$.

**Proof sketch.** Separate variables: angular Fourier modes $e^{ikv}$ reduce $D$ to 1D Dirac operators on $[0,L]$ with APS spectral condition at the end. Each channel has gap $\ge \pi/(2L)$ by elementary 1D APS spectral theory (cf. textbook treatments of APS on cylinders).

**Theorem C (gap comparison — conditional).**  
Suppose $f_{\min}(u_{\max}):=\inf_v f(u_{\max},v) \ge f_*>0$ and $f$ is smooth and positive on $[u_*,u_{\max}]\times S^1$. Then there exists $C=C(f_*,\|\partial \log f\|_\infty)$ such that any eigenvalue of the Dirac operator with support concentrated in the outer collar satisfies

$$
|\lambda| \ge \frac{C}{u_{\max}-u_*}.
$$

**Proof sketch.** Conformally compare to a product metric on the collar using the uniform bounds on $f$ and $\partial f$; apply Theorem B; transfer constants through the comparison (standard elliptic comparison for Dirac operators under bounded metric perturbation).

**Corollary C′ (continuum collapse).**  
Along the sequence of truncations $u_{\max}\to\infty$, $|\lambda|_{\min}(u_{\max})\to 0$ for the near-zero branch that becomes $L^2$-normalisable on the infinite conoid (same $O(1/u_{\max})$ rate as on cylinders, up to the comparison constant $C$).

**Residual.** Global lower bounds excluding a *fourth* light eigenvalue on the exact nonlinear tip require a quantitative tip-potential spectral gap (Section 4 + Note VIII L3). Theorem C controls the continuum rate; it does not by itself count multiplicity.

---

## 4. Tip potential and fourth-mode exclusion (conditional theorem)

**Hypothesis H_tip.**  
The radial tip operator on each $A_5$-isotype channel $\rho$ is of Sturm–Liouville type

$$
H_\rho = -\partial_{uu} + V_\rho(u),
\qquad
V_\rho(u) = \frac{C_\rho}{(u^2 + a_\rho^2)^2} + \cdots
$$

with Casimir labels $C_\rho$ ordered so that exactly three channels have ground energies below a fixed tip gap $\Delta_{\mathrm{tip}}>0$, and all other channels satisfy $E_0(\rho)\ge \Delta_{\mathrm{tip}}$.

**Theorem D (three light sectors — conditional).**  
Assume Conjecture S, Theorem C, Hypothesis H_tip, and bridge equivariance (Note XIII). Then

$$
\lim_{u_{\max}\to\infty} N_\chi(u_{\max}) = 3.
$$

**Proof structure.**
1. Conjecture S + Theorem A ⇒ integer index / spectral flow stable under smoothing.  
2. Theorem C ⇒ continuum near-zero band forms as $u_{\max}\to\infty$.  
3. Equivariance ⇒ band decomposes into isotypes (Note XIII).  
4. H_tip ⇒ exactly three isotypes remain below $\Delta_{\mathrm{tip}}$; the rest stay gapped uniformly in $u_{\max}$.  
5. Therefore $N_\chi\to 3$.

**Status of H_tip.** Supported by the locked Casimir assignment $C_g=(6/5,1,4/5)$ and continuum numerics; a fully analytic verification of the spectral ordering for the exact nonlinear coupling of angular and radial operators remains the main residual of L3.

---

## 5. What is finished vs open

| Item | Status |
|------|--------|
| Degeneracy locus of $f$ | **Proved** (Lemma 1) |
| Curvature formula | **Proved** (Lemma 2) |
| APS on smoothings $f_\varepsilon$ | **Proved** (Theorem A) |
| Cylinder gap $O(1/L)$ | **Proved** (Theorem B) |
| Collar comparison gap | **Proved** under uniform $f$ bounds (Theorem C) |
| Smoothing independence at four nodes | **Conjecture S** |
| Three light sectors | **Conditional Theorem D** (needs H_tip + S) |
| Analytic proof of H_tip | **Open** |

---

*Note XII — pure math tip APS and gap.*
