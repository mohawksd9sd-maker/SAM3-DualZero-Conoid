# Mathematical Note XXI — Link Spectrum and L4.H

**Date:** August 2026  
**Purpose:** Compute the tangential/link spectrum of the local tip model and settle when L4.H holds.

---

## 1. Local geometry

Model metric near a tip node (after coordinate normalisation):

$$
ds^2 = du^2 + (u^2 + b^2\varepsilon^2)\,d\varepsilon^2.
$$

Circle proxy at Euclidean radius $r=1$ in the $(u,\varepsilon)$-plane:

$$
u=\cos t,\quad \varepsilon=\sin t,\quad t\in[0,2\pi).\!
$$

Induced link length:

$$
L(b) = \int_0^{2\pi}\sqrt{\sin^2 t + (\cos^2 t + b^2\sin^2 t)\cos^2 t}\,dt.
$$

| $b$ | $L(b)$ |
|-----|--------|
| 0.5 | $\approx 5.977$ |
| **1.0** | **$=2\pi$** (Euclidean) |
| 2.0 | $\approx 7.333$ |
| 4.0 | $\approx 10.335$ |

(The physical $b=4\ell_0$ can be scaled into coordinates; the isotropic case $b=1$ is the conformal model after rescaling.)

---

## 2. Link operators

### 2.1 Scalar Laplacian on the link

Periodic eigenvalues:

$$
E_n = \left(\frac{2\pi n}{L}\right)^2,\qquad n\in\mathbb{Z}.
$$

**Zero mode:** $n=0$ is always present. Scalar L4.H **fails** for the Laplacian (expected; Dirac is the relevant operator).

### 2.2 Dirac operator on the link

**Periodic spin structure** (modes $e^{i 2\pi n s/L}$):

$$
\lambda \in \frac{2\pi}{L}\mathbb{Z},\qquad \min|\lambda|=0.
$$

**Anti-periodic spin structure** (modes $e^{i 2\pi (n+1/2)s/L}$):

$$
\lambda \in \frac{2\pi}{L}\Bigl(\mathbb{Z}+\tfrac12\Bigr),\qquad \min|\lambda|=\frac{\pi}{L}>0.
$$

Numeric check at $L=2\pi$:

| Structure | $\min\|\lambda\|$ |
|-----------|------------------|
| Periodic | $0$ |
| Anti-periodic | $1/2$ |

---

## 3. L4.H verdict

**Proposition H1.**  
On the local quadratic model with anti-periodic induced spin structure on the link,

$$
0 \notin \mathrm{spec}(A_{\mathrm{link}}),\qquad \min|\lambda| = \frac{\pi}{L(b)} > 0.
$$

Hence **L4.H holds** in the anti-periodic case.

**Proposition H2.**  
In the periodic case, $0\in\mathrm{spec}(A_{\mathrm{link}})$, so plain L4.H fails; the edge index still exists in the extended theory with **projected APS** conditions (kernel projected out), at the cost of tracking kernel dimension under smoothing.

---

## 4. Which spin structure does the global conoid induce?

The locked surface is orientable. A spin structure exists. Restriction to a small link about a tip node is either periodic or anti-periodic depending on the global spin structure and the framing of the node.

**Working hypothesis H_spin.**  
The global spin structure may be chosen (or is forced by APS outer boundary data) so that each of the four tip links is **anti-periodic**. This is the standard choice avoiding harmonic spinors on small circles and is compatible with APS boundary conditions used in the continuum Dirac locks.

Under H_spin, Proposition H1 applies at every node.

**Residual.** A global topological determination of the spin structure on $M_f$ with four nodes + outer boundary — one finite check in the spin-structure classification of the truncated surface.

---

## 5. Conditional theorem toward L4

**Theorem L4′ (conditional).**  
Assume:
1. H_spin (anti-periodic links), hence L4.H by Proposition H1;  
2. the standard conical/edge APS stability theorem for metrics with isolated conical singularities and invertible link Dirac operator  
   (Melrose–edge / conic APS literature).

Then Conjecture L4 holds: $\lim_{\delta\to 0}\mathrm{Index}_{\mathrm{APS}}(D_{b,\delta})$ exists, is integer, and is independent of the smoothing path.

**Proof structure.**  
L4.H $\Rightarrow$ Fredholm property of the singular edge Dirac. Stability under conic smoothing is the cited analytic theorem. Index constant for $\delta>0$ (Note XVII L3) passes to the limit.

---

## 6. Status board

| Item | Status |
|------|--------|
| Link length $L(b)$ | Computed |
| Anti-periodic Dirac: $0\notin\mathrm{spec}$ | **Proved** (Prop H1) |
| Periodic Dirac: $0\in\mathrm{spec}$ | **Proved** (Prop H2) |
| H_spin (global anti-periodic choice) | Working hypothesis |
| Full L4 | **Theorem L4′** conditional on H_spin + literature stability |

---

## 7. Bottom line

The only remaining soft points for L4 are:

1. **H_spin** — confirm anti-periodic links from global spin data;  
2. **Citation lock** — point to a specific edge/conic APS stability theorem.

The spectral obstruction ($0$ in the link spectrum) is **absent** in the preferred anti-periodic case.

---

*Note XXI — link spectrum and L4.H.*
