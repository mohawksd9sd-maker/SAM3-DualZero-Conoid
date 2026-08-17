# Mathematical Note XXIX — Analytic Closure of S′ and $H_{\mathrm{tip}}$

**Date:** August 2026  
**Purpose:** Highest-priority pure-math residuals: make generation-count hypotheses as non-conditional as the available analytic toolkit allows.

---

## Part I — Theorem S′ (smoothing independence)

### I.1 Statement

**Theorem S′.**  
Let $X_U$ be the truncated conoid with APS boundary conditions at the outer boundary and APS-compatible spin structure (Note XXII). Let $g_\delta$ be the metric with

$$
f_\delta^2 = u^2 + 4\ell_0^2\cos^2(2v) + \delta^2\rho(v),\qquad \rho\ge c>0\ \mathrm{smooth}.
$$

Then for every $\delta>0$, $\mathrm{Index}_{\mathrm{APS}}(D_\delta;X_U)\in\mathbb{Z}$ is independent of $\delta$ and of $\rho$. Moreover, under the L4 package (Notes XX–XXIV: invertible anti-periodic link Dirac + standard conical/edge Fredholm theory),

$$
\lim_{\delta\to 0}\mathrm{Index}_{\mathrm{APS}}(D_\delta;X_U)
$$

exists and equals the edge index of the singular locked metric on $X_U$.

### I.2 Proof structure (fully explicit dependencies)

| Step | Argument | Type |
|------|----------|------|
| 1 | $g_\delta$ smooth non-degenerate for $\delta>0$ | Elementary |
| 2 | APS index defined and $\mathbb{Z}$-valued | Classical APS (Atiyah–Patodi–Singer 1975) |
| 3 | Path $\delta\mapsto g_\delta$ is continuous in smooth metrics | Elementary |
| 4 | APS index invariant under continuous deformation | Classical APS |
| 5 | Link Dirac invertible (anti-periodic) | XXI–XXII **proved** |
| 6 | $\delta\to 0$ limit = edge index | **L4 package** (Melrose $b$-calculus / conical APS under spectral non-degeneracy) |
| 7 | Independence of $\rho$ | Excision + local model uniqueness (XVII L5) |

**Conditional content.** Only step 6 uses external edge-calculus theory as a black box. All model-specific geometry and the link spectral condition are internal.

**Non-conditional content for $\delta>0$.** Steps 1–4 give unconditional index stability among all positive smoothings — no singularity theory required.

---

## Part II — $H_{\mathrm{tip}}$ without numeric dependence

### II.1 Strict monotonicity (analytic)

**Theorem HT1 (restated, self-contained).**  
Let $W(u)=(u+\epsilon)^{-2}$ with $\epsilon>0$, and

$$
H_m = -\partial_{uu} + m^2 W(u) + V_{\mathrm{tip}}(u)
$$

on $(0,U)$ with Dirichlet (or APS-compatible) boundary conditions, where $V_{\mathrm{tip}}$ is independent of $m$ and bounded below. Then for $m_2>m_1\ge 0$,

$$
E_0(m_2) > E_0(m_1).
$$

**Proof.**  
Let $\psi$ be a normalised ground state of $H_{m_1}$. Then

$$
\langle\psi, H_{m_2}\psi\rangle - \langle\psi, H_{m_1}\psi\rangle
= (m_2^2-m_1^2)\int_0^U W|\psi|^2\,du.
$$

The integral is strictly positive: $W>0$ a.e. and $\psi\not\equiv 0$. Therefore $\langle H_{m_2}\rangle_\psi > E_0(m_1)$, so $E_0(m_2)=\inf \langle H_{m_2}\rangle > E_0(m_1)$.

### II.2 Three-plus-zero isolation (analytic)

**Definition.** Soft set $M_{\mathrm{soft}}=\{0,1,2\}$, heavy set $M_{\mathrm{heavy}}=\{3,4,\ldots\}$.

**Theorem HT2′ (strict channel ordering).**  
Under Theorem HT1,

$$
\max_{m\in M_{\mathrm{soft}}} E_0(m) = E_0(2) < E_0(3) = \min_{m\in M_{\mathrm{heavy}}} E_0(m).
$$

**Proof.** HT1 with consecutive integers.

**Corollary HT3 (isolation by threshold).**  
For every $U\in(0,\infty)$ and every $\tau$ with

$$
E_0(2;U) < \tau < E_0(3;U),
$$

one has

$$
\#\{m\in M_{\mathrm{soft}}: E_0(m)<\tau\} = 3,
\qquad
\#\{m\in M_{\mathrm{heavy}}: E_0(m)<\tau\} = 0.
$$

**Proof.** Immediate from HT2′ and the ordering $E_0(0)<E_0(1)<E_0(2)<E_0(3)<\cdots$.

**Remark (no numeric dependence).**  
HT1–HT3 are pure variational theorems. They do not use floating-point spectra. Numerics in Note XXVI only **illustrate** the size of $\Delta=E_0(3)-E_0(2)$; the isolation statement is analytic once the $m_\rho$ dictionary assigns soft/heavy labels (Note XIX).

### II.3 Dictionary dependence (explicit)

The only model input is:

> Soft channels are those with effective $m\in\{0,1,2\}$; heavy channels have $m\ge 3$.

This is the Fourier content of the light block $1\oplus 3\oplus 3'$ vs the $5$ inside $\mathrm{Perm}_{12}$ (Notes XIII, XIX, XXIII). If that dictionary is granted, HT3 is unconditional.

---

## Part III — Generation theorem (analytic form)

**Theorem G3′.**  
Assume:
1. Locked metric and APS outer boundary on $X_U$;  
2. APS-compatible spin structure (XXII);  
3. Theorem S′ (smoothing limit);  
4. Bridge Fourier / $m_\rho$ dictionary (XIX);  
5. Theorems HT1–HT3 (channel isolation).

Then the continuum near-zero sector, after residual discrete channel projection, consists of **exactly three** soft channels; heavy channels lie strictly above any threshold between $E_0(2)$ and $E_0(3)$.

Passing $U\to\infty$ under APS gap collapse on collars (XII Theorem C) yields three continuum light chiral sectors in the sense of the generation-count schema (VIII, XII).

**Conditional package residual.**  
Only S′ step 6 (edge-calculus black box) and the representation-theoretic dictionary (4) remain as external/model inputs. The inequality $E_0(2)<E_0(3)$ is **not** numeric.

---

*Note XXIX — analytic S′ and $H_{\mathrm{tip}}$ closure.*
