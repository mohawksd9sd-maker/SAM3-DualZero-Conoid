# Mathematical Note XVII — Relative Volume Regularisation + Local Conical APS Lemma

**Date:** August 2026  
**Purpose:** Define $\mathrm{Vol}_{\mathrm{reg}}$ without hard $U_0$; write local conical model lemmas for Conjecture S.

---

## Part I — Relative volume regularisation

### I.1 Expansion (proved)

$$
\widehat{\mathrm{Vol}}(U)=\pi U^2 + 2\pi\log U + C_0 + o(1),
$$

using $\int_0^{2\pi}(f-u)\,dv = 2\pi/u + O(u^{-3})$ for $f=\sqrt{u^2+4\cos^2(2v)}$.

### I.2 Finite part $C_0$

$$
C_0 := \lim_{U\to\infty}\Bigl(\int_0^U\int_0^{2\pi}(f-u)\,dv\,du - 2\pi\log(U+1)\Bigr).
$$

| $U$ | $C_0$ proxy |
|-----|-------------|
| 100 | 4.394 |
| 200 | 4.425 |
| 400 | 4.440 |
| 800 | 4.448 |

**Working value:** $C_0 \approx 4.45$.

### I.3 Relative heat content

Compare locked $g$ to reference $f_0=u$:

$$
H_{\mathrm{rel}}(t)=\mathrm{Tr}(e^{-t\Delta_g}-e^{-t\Delta_{g_0}}).
$$

**Proposition R1.** Relative $a_0$ is determined by $C_0$ (log divergences cancel).

**Proposition R2.** Relative $a_2$ density involves $\int(K_g-K_{g_0})\mathrm{vol}$; for $f_0=u$, $K_{g_0}=0$ off the tip, so only tip/outer boundary terms remain.

### I.4 Implication for $G_N$

Theorem H: $G_N=\alpha\ell_0^2$ stands. Prefer $\widehat{\mathrm{Vol}}_{\mathrm{reg}}:=C_0\approx 4.45$.  
Locked $\alpha=64\pi/45$ then implies $C_{\mathrm{SA}}\phi_2\approx 10^{-3}$ as a consistency check on conventions — not an independent triple derivation.

---

## Part II — Local conical APS

### II.1 Local model

**Lemma L1.** Near each tip node $v=\pi/4+k\pi/2$, to leading order

$$
ds^2=du^2+(u^2+b^2\varepsilon^2)\,d\varepsilon^2,\qquad b=4\ell_0.
$$

### II.2 Smoothing

**Lemma L2.** $f_{b,\delta}^2=u^2+b^2\varepsilon^2+\delta^2$ ($\delta>0$) is smooth and non-degenerate.

**Proposition L3.** $\mathrm{Index}_{\mathrm{APS}}(D_{b,\delta})$ is well-defined in $\mathbb{Z}$ and invariant under deformations through $\delta>0$.

### II.3 Limit and gluing

**Conjecture L4.** $\lim_{\delta\to 0}\mathrm{Index}_{\mathrm{APS}}(D_{b,\delta})$ exists and equals the edge-calculus index of the singular model.

**Proposition L5 (conditional on L4).** Global Conjecture S follows by excision: differences of smoothings are supported at nodes and cancel by L4.

---

## Status board

| Item | Status |
|------|--------|
| Volume asymptotics | **Proved** |
| $C_0\approx 4.45$ | **Computed** |
| Local model L1–L3 | **Proved** |
| L4 $\delta\to 0$ | **Conjecture** (edge APS) |
| Global S from L4 | **Conditional** Prop L5 |

**Remaining gates for unconditional generation+$G_N$ structure:** L4, $H_{\mathrm{tip}}$, $H_{\mathrm{eq}}$.

---

*Note XVII.*
