# Mathematical Note XVI — Conjecture S Attack + Internal Volume Regularisation

**Date:** August 2026  
**Purpose:** Next pure-math layer after Notes XII–XIV: (i) path to Conjecture S (stratified APS), (ii) honest regularisation of $\widehat{\mathrm{Vol}}(\hat f)$ for the $a_2$ coefficient.

---

## Part A — Conjecture S (smoothing independence)

### A.1 Statement (recall)

$$
f_\varepsilon^2 = u^2 + 4\ell_0^2\cos^2(2v) + \varepsilon^2\rho(v),\qquad \rho\ge c>0.
$$

Conjecture S: $\lim_{\varepsilon\to 0}\mathrm{Index}_{\mathrm{APS}}(D_\varepsilon;X_{u_{\max}})$ exists in $\mathbb{Z}$ and is independent of smooth $\rho$.

### A.2 Singularity type (from Note XII)

- Degeneracy only at **four isolated tip nodes** $(0,\pi/4+k\pi/2)$.
- Away from nodes, $f|_{u=0}=2\ell_0|\cos(2v)|>0$ — the “tip circle” is mostly a smooth boundary-like level set, not a full cone.
- Near a node, set $v=\pi/4+\varepsilon$, then
  $$
  f^2 \approx u^2 + 16\ell_0^2\varepsilon^2
  $$
  (leading order). This is a **quadratic cone / corner** metric in coordinates $(u,\varepsilon)$.

### A.3 Attack route (literature-shaped)

| Step | Task | Status |
|------|------|--------|
| S1 | Treat each node as a local model $ds^2=du^2+(u^2+a^2\varepsilon^2)d\varepsilon^2$ (up to angular redefinition) | Local model identified |
| S2 | Apply **APS for manifolds with conical / edge singularities** (Melrose, Piazza, Vertman, Lesch, etc.) to the local model | External literature |
| S3 | Gluing: index of smoothed global metric = bulk contribution + 4× local node contribution | Standard gluing |
| S4 | Show local node contribution independent of smoothing profile $\rho$ for $\rho(v_\mathrm{node})>0$ | Goal of Conjecture S |

**Proposition S0 (reduction).**  
If the Dirac index on the local quadratic model $f^2=u^2+a^2\varepsilon^2$ is smoothing-independent, and the metric is smooth and non-degenerate off a neighbourhood of the four nodes, then Conjecture S holds by excision/gluing.

**Proof idea.** Standard index excision: difference of two smoothings supported near nodes; each node contributes a local index density; bulk cancels.

**Residual.** Full write-up of S2–S4 as a standalone lemma citing edge-calculus APS. This is the remaining pure-math bottleneck for an unconditional generation theorem — it is **standard-shaped**, not exotic.

### A.4 Interim professional stance

Until S2–S4 are typeset against the edge-calculus literature, generation count remains **Theorem D (conditional on S + H_tip + H_eq)** as in Note XII. Numerics (gap $\propto 1/u_{\max}$, residual $<10^{-3}$) continue to support the continuum limit.

---

## Part B — Internal volume regularisation

### B.1 Divergence structure (proved numerically + asymptotically)

With $\ell_0=1$,

$$
\widehat{\mathrm{Vol}}(U) := \int_0^{U}\int_0^{2\pi} \sqrt{u^2+4\cos^2(2v)}\,dv\,du.
$$

**Lemma V1.** For large $u$,

$$
\int_0^{2\pi}\bigl(f(u,v)-u\bigr)\,dv = \frac{2\pi}{u} + O(u^{-3}).
$$

**Proof.** $\sqrt{u^2+a}-u = a/(\sqrt{u^2+a}+u)$ with $a=4\cos^2(2v)$; expand and integrate $\int\cos^2(2v)\,dv=\pi$.

**Corollary V2.**

$$
\widehat{\mathrm{Vol}}(U) = \pi U^2 + 2\pi \log U + C_0 + o(1)
$$

as $U\to\infty$, for a finite constant $C_0$ (tip finite part).

**Consequence.** The internal conoid is **noncompact** with quadratically divergent volume. One cannot insert an infinite $\mathrm{Vol}(M_f)$ naively into $a_2$.

### B.2 Admissible regularisations (professional options)

| Scheme | Definition | Effect on $\alpha$ in $G_N=\alpha\ell_0^2$ |
|--------|------------|----------------------------------------|
| **Hard cutoff** | $\widehat{\mathrm{Vol}}(U_0)$ at fixed $U_0=O(1)$ | $\alpha=\alpha(U_0)$; order-one ambiguity |
| **Log subtraction** | $\pi U^2+2\pi\log U$ subtracted; use $C_0$ | Finite but depends on subtraction scheme |
| **Zeta / heat-kernel relative** | Define $a_2$ via relative traces on product without absolute volume | Preferred NCG style |
| **Spectral cutoff identity** | Set $\Lambda\sim 1/\ell_0$ and absorb $\widehat{\mathrm{Vol}}$ into moment conventions | Matches repository lock philosophy |

### B.3 Numerical diagnostics (August 2026)

| $U$ | $\widehat{\mathrm{Vol}}(U)$ | $\widehat{\mathrm{Vol}}-\pi U^2$ |
|-----|---------------------------|--------------------------------|
| 1 | $\approx 8.97$ | — |
| 2 | $\approx 21.80$ | — |
| 10 | $\approx 333.5$ | $\approx 19$ |
| 20 | $\approx 1281$ | $\approx 24$ |

Asymptotic $\int(f-u)\,dv \sim 2\pi/u$ verified to relative error $<1\%$ for $u\ge 20$.

Target combination for locked $\alpha=64\pi/45$:

$$
C_{\mathrm{SA}}\,\phi_2\,\widehat{\mathrm{Vol}}_{\mathrm{reg}} = \frac{45}{1024\pi^2}\approx 4.45\times 10^{-3}.
$$

This **fixes the product** of Seeley combinatorics, cutoff moment, and regularised volume — it does **not** independently predict all three.

### B.4 Honest status of $64\pi/45$

| Claim | Status |
|-------|--------|
| $G_N\propto\ell_0^2$ (Theorem H) | **Proved** under product $a_2$ + scaling |
| Absolute prefactor $64\pi/45$ | **Convention lock** absorbing $(\phi_2,C_{\mathrm{SA}},\mathrm{Vol}_{\mathrm{reg}})$ |
| Unique preferred $\mathrm{Vol}_{\mathrm{reg}}$ from geometry alone | **Not yet** — needs zeta/relative $a_2$ write-up |

---

## Part C — Updated pure-math backlog

| Priority | Item |
|----------|------|
| 1 | Typeset Proposition S0 + local conical model against edge-APS references |
| 2 | Define $\mathrm{Vol}_{\mathrm{reg}}$ via relative heat kernel on the product (remove hard $U_0$) |
| 3 | Analytic $H_{\mathrm{tip}}$ (fourth mode) |
| 4 | Production APS numerics (engineering) |

---

*Note XVI — Conjecture S path and volume regularisation.*
