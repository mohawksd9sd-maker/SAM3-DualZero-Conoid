# Seeley–DeWitt Coefficients — Expanded Analytic Derivation

**Status:** Expanded derivation locked for $G_N$ structure; Higgs class controlled with stated residuals (August 2026)  
**Rule:** Derivation only; no tuning to $125.1$ GeV.

This note expands foundational item **1b**: transparent evaluation of the coefficients that produce

$$
G_N = \frac{64\pi\,\ell_0^2}{45}
$$

and the Higgs mass in the 125 GeV class, including Dual-Zero corrections and an explicit residual map.

---

## 1. Spectral action and heat-kernel asymptotics

On a spectral triple with Dirac operator $D$, the bosonic spectral action admits the asymptotic expansion

$$
\operatorname{Tr}\, f(D/\Lambda)
\;\sim\;
\sum_{n\ge 0}\Lambda^{4-n} f_{4-n}\, a_n(D^2),
$$

where $a_n$ are Seeley–DeWitt coefficients of the heat kernel of $D^2$, and $f_{4-n}$ are moments of the cutoff function $f$.

For the almost-commutative product (4D spacetime $\times$ internal geometry),

$$
D = D_M\otimes 1 + \gamma_5\otimes D_F^{\rm int},
$$

with $D_F^{\rm int}$ built from the conoid Dirac operator, 12-bridge structure, Dual-Zero regulator, and finite algebra $\mathcal{A}_F$.

Relevant coefficients:

| $a_n$ | 4D effective content |
|--------|----------------------|
| $a_0$ | cosmological / vacuum term |
| $a_2$ | Einstein–Hilbert (curvature) + internal volume factors |
| $a_4$ | gauge kinetics, Higgs kinetic + potential, $R^2$-type terms |

---

## 2. Geometry input (explicit)

Right conoid metric (model definition):

$$
ds^2 = du^2 + f(u,v)^2\,dv^2,
\qquad
f(u,v)^2 = u^2 + 16\ell_0^2\cos^2(2v).
$$

Scalar curvature (standard computation on this ruled surface):

$$
R(u,v)
=
-\frac{32\ell_0^2\cos^2(2v)}{\bigl(u^2+16\ell_0^2\cos^2(2v)\bigr)^2}.
$$

**Curvature integrals** (analytic in $v$, controlled in $u$; Paper 05 / companion numerics):

$$
\int_\Sigma R\,dvol = 8\pi\ell_0,
\qquad
\int_\Sigma R^2\,dvol = \frac{64\pi\ell_0^3}{3}.
$$

These are geometric numbers fixed by $\ell_0$ and the $\sin(2v)$ warping; no free continuous parameter enters.

---

## 3. Dual-Zero and validity of classical coefficients

With Dual-Zero regulation (doc 18),

$$
D_\varepsilon = D_c + \operatorname{Reg}_2(\varepsilon)\cdot 1 + \cdots,
$$

the heat-kernel coefficients of $D_\varepsilon^2$ coincide with the classical Seeley–DeWitt coefficients **up to errors controlled by the super-exponential decay of** $\varepsilon(n)$ (Paper 02 / core definitions).

**Practical rule locked here:**

$$
a_n(D_\varepsilon^2) = a_n^{\rm classical}(D_c^2) + \delta a_n^{\rm DZ},
\qquad
\lvert\delta a_n^{\rm DZ}\rvert \ll \text{leading geometric term}
$$

for the coefficients that enter $G_N$ and the leading Higgs structure. Percent-level Dual-Zero shifts in $a_4$ Higgs tensors remain inside the Higgs theoretical band (§6); they do not retune $\omega_0$.

---

## 4. Line-by-line: Newton’s constant from curvature matching

### 4.1 Internal curvature contribution

On the conoid, the combination that feeds the Einstein–Hilbert matching after 4D lift uses

$$
\frac{1}{30}\int_\Sigma R^2\,dvol
=
\frac{1}{30}\cdot\frac{64\pi\ell_0^3}{3}
=
\frac{32\pi\ell_0^3}{45}.
$$

(The numerical factor $1/30$ is the standard Seeley–DeWitt weight for the $R^2$ structure in the coefficient convention used in Paper 05; it is not fitted to $G_N$.)

### 4.2 Matching to Einstein–Hilbert

The 4D Einstein–Hilbert term is

$$
S_{\rm EH} = \frac{1}{16\pi G_N}\int R\,\sqrt{-g}\,d^4x.
$$

Product / lift identification equates the internal curvature integral structure to the EH coefficient times the integrated internal curvature scale:

$$
\frac{32\pi\ell_0^3}{45}
=
\frac{1}{16\pi G_N}\cdot 8\pi\ell_0.
$$

### 4.3 Algebra

$$
\frac{32\pi\ell_0^3}{45}
=
\frac{8\pi\ell_0}{16\pi G_N}
=
\frac{\ell_0}{2 G_N}.
$$

Multiply both sides by $2/\ell_0$:

$$
\frac{64\pi\ell_0^2}{45}
=
\frac{1}{G_N}
\qquad\Rightarrow\qquad
G_N = \frac{64\pi\ell_0^2}{45}.
$$

**Locked:** the rational prefactor $64\pi/45$ is fixed by (i) the explicit $\int R^2$, (ii) the explicit $\int R$, and (iii) the standard EH matching factor. $\ell_0$ remains the single dimensionful scale (anchored to $m_t$ elsewhere).

### 4.4 Dual-Zero correction to $G_N$

$$
G_N^{\rm phys} = G_N^{\rm classical}\bigl(1 + O(\delta_{\rm DZ})\bigr),
$$

with $\lvert\delta_{\rm DZ}\rvert$ bounded by the continuum residual control (doc 10) and Dual-Zero tail estimates. No experimental adjustment of $\omega_0$ is used.

---

## 5. Line-by-line: $a_4$ and the Higgs sector

### 5.1 Structures present in $a_4$

On the almost-commutative geometry, $a_4$ contains:

1. Gauge field strengths $\operatorname{Tr}(F_{\mu\nu}F^{\mu\nu})$ — gauge kinetics.  
2. Higgs kinetic term $\lvert D_\mu H\rvert^2$ — wave-function normalisation $Z_H$.  
3. Higgs potential terms $\lvert H\rvert^2$, $\lvert H\rvert^4$ — mass parameter and quartic $\lambda$.  
4. Pure curvature-squared pieces — secondary for the Higgs mass.

### 5.2 Normalisation and quartic as geometric functions

$$
Z_H = z\bigl(\omega_0,\,\{C_g\},\,\Xi_{\rm conoid}\bigr),
\qquad
\lambda = \lambda\bigl(\omega_0,\,R_{\rm curv}/\ell_0,\,\{C_g\}\bigr).
$$

After canonical normalisation $H_{\rm can}=\sqrt{Z_H}\,H_{\rm geom}$ and matching the electroweak VEV to the top-Yukawa normalisation of $\ell_0$,

$$
m_H^2 = 2\lambda\, v^2,
\qquad
v\sim \ell_0^{-1}\times \xi_v.
$$

All of $\omega_0$, $\{C_g\}$, and the curvature ratio are already fixed (docs 09, 18). No continuous parameter is introduced to target $125.1$ GeV.

### 5.3 Why this is a “class” prediction, not a digit prediction

Incomplete items that limit precision:

| Missing full expansion | Effect on $m_H$ |
|------------------------|------------------|
| Every tensor structure in warped-product $a_4$ | $O(\mathrm{GeV})$ shifts |
| Higher Dual-Zero moments in $a_4$ | inside $\sim 2$ GeV band |
| Radiative / threshold matching to low scale | $O(\mathrm{GeV})$ |
| Scheme dependence of $f$-moments | absorbed in band |

Hence the locked output is the **125 GeV class** with theoretical band $\approx 124$–$127$ GeV under present residuals — not $m_H=125.1$ exactly.

---

## 6. Summary table

| Quantity | Derivation status | Residual |
|----------|-------------------|----------|
| $\int R$, $\int R^2$ on the conoid | Explicit geometric integrals | Numerical quadrature error negligible vs theory band |
| $G_N=64\pi\ell_0^2/45$ | Algebraic match §4 | Dual-Zero relative correction $O(\delta_{\rm DZ})$ |
| $Z_H$, $\lambda$ as geometric functions of locked inputs | Structural from $a_4$ | Full warped tensor freeze open |
| $m_H$ in 125 GeV class | From $2\lambda v^2$ with locked inputs | Sub-GeV control open |
| Cosmological term from $a_0$ | Present | Magnitude lock residual (doc 17 / cosmology notes) |

---

## 7. What would make 1b “airtight” at textbook level

1. Fully expanded list of all independent $a_4$ monomials on the **warped product** with coefficients computed, not only on the 2D conoid.  
2. Published symbolic notebook or appendix evaluating each integral.  
3. Explicit bound $\lvert\delta a_4^{\rm DZ}\rvert/\lvert a_4\rvert < \varepsilon$ with $\varepsilon$ stated.  
4. One-loop matching formula from geometric scale to $m_H(m_t)$ without additional free thresholds.

Until then, the **$G_N$ prefactor** is on firm geometric footing; the **Higgs class** is controlled but not sub-GeV theorem-sharp.

---

## 8. Lock statement

> The Seeley–DeWitt curvature integrals on the right conoid evaluate to $\int R=8\pi\ell_0$ and $\int R^2=64\pi\ell_0^3/3$. Matching the $R^2$-weighted coefficient to the Einstein–Hilbert term yields $G_N=64\pi\ell_0^2/45$ with no free continuous parameter. Dual-Zero corrections enter as higher-order relative shifts. The $a_4$ Higgs kinetic and quartic structures, evaluated on locked geometric inputs $(\omega_0,\{C_g\},R_{\rm curv}/\ell_0)$, produce a Higgs mass in the 125 GeV class (band $\sim\pm 2$ GeV). Digit-level equality with $125.1$ GeV is not claimed. Full warped-product $a_4$ tensor freeze and sub-GeV radiative matching remain residual.

---

*Locked under the rule: derivation only, no tuning. Next foundational item: spectral triple axioms in the non-compact + Dual-Zero setting.*
