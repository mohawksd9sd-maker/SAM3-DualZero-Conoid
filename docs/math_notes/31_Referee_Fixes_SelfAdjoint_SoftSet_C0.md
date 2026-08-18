# Mathematical Note XXXI — Referee Fixes: Self-Adjointness, Soft Set, $C_0$

**Date:** August 2026  
**Purpose:** Close the peer-review concerns on domain theory, soft/heavy partition, and $C_0$ auditability.

---

## 1. Self-adjointness of $H_m$ at the tip

### 1.1 Setup

$$
H_m = -\partial_{uu} + \frac{m^2}{(u+\epsilon)^2} + V_{\mathrm{tip}}(u)
\quad\text{on }(0,U).
$$

Near $u=0$, the dominant singular term is the inverse-square potential $m^2/u^2$ (after $\epsilon\to 0^+$ where allowed).

### 1.2 Weyl limit-point / limit-circle classification

**Classical fact** (Weyl–Kodaira; Reed–Simon II; inverse-square analysis).  
For $-\mathrm{d}^2/\mathrm{d}u^2 + c/u^2$ on $(0,1]$:

- **Limit-point** at $0$ if $c\ge 3/4$ — unique self-adjoint extension (no boundary condition needed at $0$).  
- **Limit-circle** at $0$ if $c<3/4$ — a one-parameter family of boundary conditions is required.

**Application:**

| $m$ | $m^2$ | Classification at $u=0$ |
|-----|-------|-------------------------|
| 0 | 0 | **Limit-circle** — BC required |
| 1 | 1 | **Limit-point** ($1>3/4$) |
| $\ge 2$ | $\ge 4$ | **Limit-point** |

### 1.3 How the model pins the $m=0$ realization

**Proposition SA1.**  
For $m\ge 1$, $H_m$ is essentially self-adjoint on $C_c^\infty(0,U)$ (with the outer APS/Dirichlet condition at $U$). Theorem HT1 applies to this unique realization.

**Proposition SA2.**  
For $m=0$, the tip is limit-circle. The self-adjoint realization is fixed by the **APS / conic boundary condition** induced by the global spin structure and the local conical model (Notes XXI–XXII): the anti-periodic link condition selects a specific domain among the limit-circle extensions.

**Proposition SA3 (ordering preserved).**  
Under the APS-compatible tip condition for $m=0$ and the unique SA extensions for $m\ge 1$, the variational proof of HT1 still gives

$$
E_0(0) < E_0(1) < E_0(2) < E_0(3) < \cdots
$$

because the quadratic-form comparison only uses the difference of potentials $m_2^2 W - m_1^2 W\ge 0$ on a common form domain compatible with the chosen tip condition (the form domain for limit-circle $m=0$ under APS is the one continuously connected to the $\epsilon>0$ Friedrichs-type regularization used in the production pipeline).

**Residual.** A fully typeset limit-circle parametrix matching APS to a specific boundary parameter $\gamma_{\mathrm{APS}}$ is still packaging; the classification and the uniqueness for $m\ge 1$ are standard.

---

## 2. Soft set $\{0,1,2\}$ from geometry (not only $A_5$)

### 2.1 Referee concern

$A_5$ acts on the discrete bridge space, not as isometries of $f$. The soft/heavy split must not rest only on an asserted $A_5$ label.

### 2.2 Geometric preference order

**Step G1 (Hardy).**  
Tip energy increases strictly with $m^2$ (HT1). The lowest channels are the smallest non-negative integers $m=0,1,2,3,\ldots$

**Step G2 (metric harmonic).**  
The locked metric depends on $\cos(2v)$, which couples angular Fourier modes with $\Delta m=\pm 2$. The natural non-zero harmonic of the geometry is **$m=2$**, not $m=3$.

**Step G3 ($C_4$ isometry).**  
Exact isometry $v\mapsto v+\pi/2$ grades modes by $i^m$. This preserves a $\mathbb{Z}/4$ structure and is compatible with a soft block built from $m=0,1,2$ before the first heavy Hardy step $m=3$.

**Proposition Soft1 (geometric soft set).**  
The combination of (G1)–(G3) selects $\{0,1,2\}$ as the unique initial segment of three consecutive angular momenta that (i) minimises Hardy energy and (ii) includes the metric harmonic $m=2$. Replacing $2$ by $3$ would exclude the metric harmonic and include a strictly heavier Hardy channel.

**Role of $A_5$.**  
Once the soft set is fixed geometrically, the 12-bridge $A_5$-module organises generation labels *inside* that soft sector. $A_5$ is **not** used to choose which $m$ are soft; that choice is metric + Hardy + $C_4$.

**Honest residual.**  
Why *exactly three* soft slots (rather than two or four) still uses the discrete bridge count $N=12$ and the generation programme’s identification of three light families. Soft1 explains **which** $m$ are soft; the integer three is tied to the three-generation claim and the $1\oplus 3\oplus 3'$ content after heavy $m\ge 3$ are cut by Hardy.

---

## 3. Derivation of $C_0$

### 3.1 Expansion (proved)

With $\hat f=\sqrt{u^2+4\cos^2(2v)}$ ($\ell_0=1$),

$$
\widehat{\mathrm{Vol}}(U)=\int_0^U\!\int_0^{2\pi}\hat f\,dv\,du
= \pi U^2 + 2\pi\log U + C_0 + o(1).
$$

**Lemma.** $\int_0^{2\pi}(\hat f-u)\,dv = 2\pi/u + O(u^{-3})$ as $u\to\infty$.

**Proof.** $\sqrt{u^2+a}-u=a/(\sqrt{u^2+a}+u)$, $a=4\cos^2(2v)$, $\int_0^{2\pi}\cos^2(2v)\,dv=\pi$.

### 3.2 Definition of $C_0$

$$
C_0 := \lim_{U\to\infty}\Bigl(
\int_0^U\int_0^{2\pi}(\hat f-u)\,dv\,du - 2\pi\log(U+1)
\Bigr).
$$

### 3.3 Numeric evaluation (reproducible)

| $U$ | $C_0$ proxy |
|-----|-------------|
| 200 | 4.404 |
| 400 | 4.420 |
| 800 | 4.428 |

**Working value:** $C_0\approx 4.43$–$4.45$ (converging; script `code/volume_regularisation.py`).

This is an **explicit integral definition + convergent numerical evaluation**, not an unexplained constant.

---

## 4. Mapping to referee concerns

| Concern | Fix |
|---------|-----|
| Domain / self-adjointness at tip | §1 Weyl classification + APS pins $m=0$ |
| Soft/heavy only from $A_5$ | §2 geometric Soft1: Hardy + $\cos(2v)$ + $C_4$ |
| $C_0$ unauditable | §3 definition + table + script |
| Corollary trivial given partition | Agree; content is Soft1 + HT1, not the corollary alone |
| Edge calculus cited | Still packaged (checklist XXIV); not re-proved |
| Euclidean only | Still residual; stated as such |

---

*Note XXXI — referee fixes.*
