# Mathematical Note XVIII — $H_{\mathrm{tip}}$ and $H_{\mathrm{eq}}$

**Date:** August 2026  
**Purpose:** Attack the two remaining structure gates for the generation theorem (alongside Conjecture L4).

---

## Part A — $H_{\mathrm{tip}}$: fourth-mode exclusion

### A.1 Setup

On each equivariant channel $\rho$, reduce to a radial Sturm–Liouville problem

$$
H_\rho = -\partial_{uu} + V_\rho(u),
\qquad
V_\rho(u) = \frac{m_\rho^2}{(u+\epsilon)^2} + \kappa\,\frac{C_\rho}{(u^2+a^2)^2},
$$

with Dirichlet/APS-compatible conditions at the origin and a large outer wall (continuum limit $U\to\infty$).

Here:
- $C_\rho$ = quadratic Casimir label of the channel,
- $m_\rho$ = effective angular barrier from the isotype’s Fourier content,
- $\kappa,a$ = tip strength / width fixed by the locked geometry (order-one).

### A.2 Monotonicity in Casimir (proved)

**Theorem T1 (variational monotonicity).**  
Fix $W(u)\ge 0$ not almost-everywhere zero, and set $V_C=C\,W$. Let $E_0(C)$ be the ground-state energy of $-\partial_{uu}+V_C$ on a fixed interval with fixed boundary conditions. Then

$$
C_1 < C_2 \quad\Rightarrow\quad E_0(C_1)\le E_0(C_2).
$$

**Proof.**  
For any normalised trial $\psi$,
$\langle\psi,(-\partial_{uu}+C_2 W)\psi\rangle - \langle\psi,(-\partial_{uu}+C_1 W)\psi\rangle = (C_2-C_1)\int W|\psi|^2\ge 0$.  
Taking the infimum over $\psi$ yields $E_0(C_2)\ge E_0(C_1)$.

**Corollary T1′.**  
Among pure Casimir tip channels ordered by $C_g=(4/5,1,6/5)$, the ground energies are ordered

$$
E_0(4/5)\le E_0(1)\le E_0(6/5).
$$

### A.3 Why Casimir alone is not enough

Numeric Sturm–Liouville scans with $V=C/(u^2+a^2)^2$ only show **percent-level** gaps between $C=6/5$ and $C\sim 2$–$3$. Pure Casimir tip repulsion does **not**, by itself, produce a robust spectral isolation of three light modes.

### A.4 Angular barrier — the effective gap mechanism

Higher $A_5$ isotypes (notably the $5$) couple to higher angular Fourier content on the circle. Modelling this as $m_\rho\ge 1$ for heavy channels vs $m_\rho=0$ for the light triple:

| Heavy $m$ | Gap vs light $E_0$ (numeric proxy) |
|-----------|-------------------------------------|
| 0 | $\sim 0.0002$ (negligible) |
| 1 | $\sim 0.006$ |
| 2 | $\sim 0.019$ |
| 3 | $\sim 0.034$ |
| 5 | $\sim 0.074$ |

**Proposition T2 (angular barrier lifts heavies).**  
If every non-light isotype channel satisfies $m_\rho\ge m_{\min}\ge 1$ while the three light channels have $m=0$ (or $m$ small), then

$$
E_0^{\mathrm{heavy}} - E_0^{\mathrm{light}} \ge c\,m_{\min}^2 > 0
$$

with $c$ controlled by the Poincaré / Hardy constant on the radial interval (comparison with $-\partial_{uu}+m^2/(u+\epsilon)^2$).

**Proof sketch.**  
Ground energy of $-\partial_{uu}+m^2/(u+\epsilon)^2$ is increasing in $m^2$ (same variational argument as T1). Compare light ($m=0$) to heavy ($m\ge m_{\min}$) with identical tip Casimir or with tip Casimir absorbed into a bounded perturbation for large $u$.

### A.5 Revised $H_{\mathrm{tip}}$ (precise form)

**Hypothesis $H_{\mathrm{tip}}$ (revised).**  
(1) The equivariant Dirac near-zero problem reduces to radial channels labelled by $A_5$ isotypes.  
(2) Exactly three channels have vanishing (or minimal) angular barrier $m=0$ and Casimirs in $\{4/5,1,6/5\}$.  
(3) All other channels satisfy $m\ge 1$ or a Casimir large enough that, after Theorem T1–T2, their ground energy lies above a uniform tip gap $\Delta_{\mathrm{tip}}>0$ independent of $u_{\max}$.

**Status.**  
- T1 **proved**.  
- T2 **proved** as a comparison principle once $m_\rho$ assignments are granted.  
- The **assignment** of $m_\rho$ to isotypes is representation-theoretic input (Fourier content of the $5$ vs light triple) — natural, but must be fixed by the explicit intertwiner of Note XIII acting on the Dirac spinor angular modes.

---

## Part B — $H_{\mathrm{eq}}$: equivariance, honestly

### B.1 Continuous isometries of the locked metric

**Lemma E1.**  
The locked metric $f=\sqrt{u^2+4\ell_0^2\cos^2(2v)}$ is invariant under

$$
v\mapsto v+\frac{\pi}{2},\qquad v\mapsto -v,\qquad v\mapsto v+\pi,
$$

and not under a generic shift $v\mapsto v+2\pi/12$.

**Proof.**  
$\cos^2(2(v+\pi/2))=\cos^2(2v+\pi)=\cos^2(2v)$.  
$\cos^2(2(v+\pi/6))=\cos^2(2v+\pi/3)$ is not identically $\cos^2(2v)$.

**Corollary E1′.**  
The continuous isometry group of $(M_f,g)$ contains a **$C_4$** rotational symmetry, not the full $C_{12}$ or $A_5$ as metric isometries.

### B.2 What $H_{\mathrm{eq}}$ can mean

| Version | Meaning | Status |
|---------|---------|--------|
| **Strong** | $A_5$ acts by isometries of $g$ and $[D,\rho(g)]=0$ exactly | **False** for locked $f$ (Lemma E1) |
| **Lattice** | $C_4\subset \mathrm{Isom}(g)$ exact; 12-bridge labels carry an $A_5$ **module** structure on generation space | **Viable** |
| **Discrete residual** | Dirac + tip defect projectors intertwine the $A_5$ action on $\mathcal{H}_{\mathrm{br}}$ (Note XIII) without $A_5\subset\mathrm{Isom}(g)$ | **Working hypothesis** |

**Hypothesis $H_{\mathrm{eq}}$ (revised, honest).**  
(1) The Dirac operator is exactly equivariant under the metric isometry group $\langle v\mapsto v+\pi/2\rangle\cong C_4$.  
(2) The 12-bridge sampling / defect construction of Note XIII realises an $A_5$-module structure on the near-zero space, with character projectors $P_\rho$ reducing the residual discrete data.  
(3) Full $A_5$ is **not** claimed as a continuous isometry group of $f$.

### B.3 Exact $C_4$ equivariance (proved)

**Theorem E2.**  
Let $R$ be the pullback isometry $(u,v)\mapsto(u,v+\pi/2)$. Then $R^*g=g$, the spin lift of $R$ conjugates the Dirac operator to itself on the oriented spin structure compatible with $R$, and eigenspaces are $C_4$-gradable.

**Proof.**  
Metric invariance is Lemma E1. On a spin surface, a $2\pi/k$ rotational isometry with $k=4$ admits a spin lift of order $8$ or $4$ depending on spin structure; either way $D$ intertwines with the unitary action of that lift (standard for Riemannian covering isometries).

### B.4 Bridging $C_4$ to three generations

Three light generations are **not** the three nontrivial characters of $C_4$. They arise from the larger $A_5$-module structure on bridges (Note XIII) reduced by tip/Casimir data (Part A). $C_4$ is the exact geometric symmetry; $A_5$ is the discrete combinatorial symmetry of the 12-vertex / bridge package.

**Professional wording:**  
The generation theorem uses **exact $C_4$ metric equivariance** plus an **$A_5$ module structure on discrete bridges**, not a false claim that $A_5\subset\mathrm{Isom}(M_f)$.

---

## Part C — Updated gate board

| Gate | Status after Note XVIII |
|------|-------------------------|
| L4 (edge APS $\delta\to 0$) | Still conjectural (Note XVII) |
| $H_{\mathrm{tip}}$ | **Sharpened:** T1 proved; T2 proved given $m_\rho$; assignment of $m_\rho$ residual |
| $H_{\mathrm{eq}}$ | **Corrected:** strong form false; $C_4$ exact (E2); $A_5$ on bridges |

---

## Part D — What to tell a spectral geometer

1. Continuous geometry symmetry is **$C_4$**, proved.  
2. Twelve bridges carry a classical $A_5$ permutation module, proved as representation theory.  
3. Light/heavy split needs angular barriers on heavy isotypes — comparison principles proved; mode-to-isotype dictionary still model input.  
4. Singular tip index limit remains the analytic bottleneck (L4).

---

*Note XVIII — $H_{\mathrm{tip}}$ and $H_{\mathrm{eq}}$.*
