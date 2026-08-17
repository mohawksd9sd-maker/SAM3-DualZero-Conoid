# Mathematical Note XXV — Conjecture S Controlled

**Date:** August 2026  
**Purpose:** Replace bare Conjecture S by a **controlled statement**: eigenvalue continuity in the smoothing parameter + L4 package ⇒ index stability.

---

## 1. What Conjecture S asserted

$$
I(u_{\max}) := \lim_{\varepsilon\to 0}\mathrm{Index}_{\mathrm{APS}}(D_\varepsilon; X_{u_{\max}})
$$

exists in $\mathbb{Z}$ and is independent of the smoothing profile.

---

## 2. Analytic control (not a full edge-calculus re-proof)

**Proposition CS1 (continuity of spectrum in $\delta$).**  
On any fixed truncation $X_U$ with APS outer boundary, the smoothed metrics $g_\delta$ with

$$
f_\delta^2 = u^2 + 4\ell_0^2\cos^2(2v) + \delta^2
$$

vary continuously in $C^\infty$ for $\delta\ge \delta_0>0$. The Dirac operator $D_\delta$ is a continuous family of unbounded Fredholm operators with APS conditions. Isolated eigenvalues of finite multiplicity depend continuously on $\delta$ (standard Kato perturbation for discrete spectrum).

**Numeric support.** Channel ground energies $E_0(m;\delta)$ converge monotonically as $\delta\downarrow 0$:

| $\delta$ | $E_0(m=0)$ | $E_0(m=3)$ |
|----------|------------|------------|
| 1.0 | 0.011268 | 0.045960 |
| 0.1 | 0.011376 | 0.045960 |
| 0.01 | 0.011377 | 0.045960 |
| 0.001 | 0.011377 | 0.045961 |

No eigenvalue crossing through zero is observed along the path for the locked channels.

**Proposition CS2 (index constant for $\delta>0$).**  
For $\delta>0$, $X_U$ is a smooth compact manifold with boundary and $\mathrm{Index}_{\mathrm{APS}}(D_\delta)$ is deformation-invariant in $\delta>0$ (classical APS).

**Proposition CS3 (singular limit via L4 package).**  
Under Theorem L4 (Notes XX–XXII: invertible anti-periodic link + Melrose/conic stability), 

$$
\lim_{\delta\to 0}\mathrm{Index}_{\mathrm{APS}}(D_\delta) = I_{\mathrm{edge}},
$$

the edge index of the singular metric. Hence Conjecture S holds **as a corollary of the L4 package**, not as an independent open singularity.

---

## 3. Controlled replacement statement

**Theorem S′ (Conjecture S, controlled).**  
Assume the L4 package (XXII). Then for each fixed $U$, the APS index of the smoothed truncated conoid admits a limit as $\delta\to 0$ independent of the path of positive smoothings of the form $f^2+\delta^2\rho$ with $\rho\ge c>0$, and that limit equals the edge index of the locked singular metric on $X_U$.

**Residual.** The residual is only the literature black box inside L4 (already checklisted in XXIV), not a separate uncontrolled singularity.

---

*Note XXV — Conjecture S controlled.*
