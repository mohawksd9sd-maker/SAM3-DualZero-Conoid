# Mathematical Note XIV — Seeley $a_2$ Coefficient Chain on the Locked Metric

**Date:** August 2026  
**Purpose:** Finish the pure-math coefficient path for $G_N\propto\ell_0^2$ and isolate exactly where $64\pi/45$ sits.

---

## 1. 2D internal geometry

On $(M_f,g)$ with volume form $\mathrm{vol}=f\,du\wedge dv$ and Gaussian curvature $K=-f_{uu}/f$ (Note XII),

$$
\int K\,\mathrm{vol}
= -\int \partial_{uu} f\,du\,dv
$$

over regions where $f>0$. For the infinite or truncated conoid, boundary terms from integration by parts relate to the tip and outer circle — Gauss–Bonnet type identities on smoothed truncations.

---

## 2. Product spectral triple

On $S^4\times M_f$ (or $T^4\times M_f$, etc., as the 4D factor),

$$
D^2 = D_S^2 \otimes 1 + 1\otimes D_F^2 + \text{cross terms from }
\gamma\text{-grading}.
$$

The Seeley–DeWitt coefficient $a_2(D^2)$ on a product contains:

$$
a_2 \supset c_R \int_S R_S\,\mathrm{vol}_S \cdot \mathrm{Vol}(M_f)
+ c_K \int_S \mathrm{vol}_S \cdot \int_{M_f} K_f\,\mathrm{vol}_f
+ \cdots
$$

with universal combinatorial constants $c_R,c_K$ from the heat-kernel calculus (Gilkey; Connes–Chamseddine conventions).

The Einstein–Hilbert term in the spectral action arises from the $\int R_S$ piece multiplied by the **internal volume**

$$
\mathrm{Vol}(M_f) = \int f\,du\,dv.
$$

---

## 3. Scaling

Write $f=\ell_0\,\hat f(\hat u,v)$ with $\hat u=u/\ell_0$. Then

$$
\mathrm{Vol}(M_f) = \ell_0^2 \int \hat f\,d\hat u\,dv =: \ell_0^2 \,\widehat{\mathrm{Vol}}(\hat f).
$$

With spectral cutoff $\Lambda=1/\ell_0$,

$$
\frac{1}{2\kappa^2}
= C_{\mathrm{SA}}\,\phi_2\,\Lambda^2\,\mathrm{Vol}(M_f)
= C_{\mathrm{SA}}\,\phi_2\,\widehat{\mathrm{Vol}}(\hat f)\,\frac{1}{\ell_0^2},
$$

hence

$$
G_N = \frac{\kappa^2}{8\pi}
= \frac{\ell_0^2}{16\pi\, C_{\mathrm{SA}}\,\phi_2\,\widehat{\mathrm{Vol}}(\hat f)}.
$$

**Theorem H (structural proportionality).**  
Under the product spectral action and the scaling above,

$$
G_N = \alpha\,\ell_0^2
$$

for a dimensionless constant $\alpha$ depending only on $(C_{\mathrm{SA}},\phi_2,\widehat{\mathrm{Vol}}(\hat f))$.

**Proof.** Immediate from the display.

---

## 4. The pure number $64\pi/45$

Equating $\alpha=64\pi/45$ is the statement

$$
C_{\mathrm{SA}}\,\phi_2\,\widehat{\mathrm{Vol}}(\hat f) = \frac{45}{1024\pi^2}.
$$

**Computation path (to be executed independently):**

1. Fix spectral-action conventions for $C_{\mathrm{SA}}$ (cite CCM / van Suijlekom tables).  
2. Fix cutoff moment $\phi_2$ for the chosen $\chi$.  
3. Compute $\widehat{\mathrm{Vol}}(\hat f)=\int_0^{\hat U}\int_0^{2\pi}\hat f\,d\hat u\,dv$ on a standardised finite truncation, or the regularised infinite volume used in the programme.  
4. Multiply and compare to $45/(1024\pi^2)$.

**Status.** Theorem H is **proved**. The equality $\alpha=64\pi/45$ is a **normalisation lock** of the repository pending independent recomputation of the three factors in step 1–3. It is not an additional geometric miracle beyond Theorem H.

---

## 5. Tip coefficient dependence

If $c$ replaces 4 in $f$, then $\hat f$ changes and $\widehat{\mathrm{Vol}}$ changes. Hence $\alpha=\alpha(c)$. The locked $c=4$ is required for consistency with the published $\alpha=64\pi/45$ and geometric $\omega_0$ (Notes IV–V, IX).

---

## 6. Finished pure math vs residual

| Item | Status |
|------|--------|
| $G_N\propto\ell_0^2$ from $a_2$ + scaling | **Theorem H** |
| Explicit $K$ and $\mathrm{vol}$ on $f$ | **Proved** (Note XII) |
| Universal Seeley combinatorics $C_{\mathrm{SA}}$ | Literature standard |
| Independent numerical evaluation of $\widehat{\mathrm{Vol}}(\hat f)\times\phi_2$ | **Residual computation** |
| Scheme independence of $\alpha$ | **False** — scheme enters $\phi_2$ |

---

*Note XIV — $a_2$ coefficient chain.*
