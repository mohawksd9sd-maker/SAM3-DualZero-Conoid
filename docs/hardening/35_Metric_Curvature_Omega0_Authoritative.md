# 35 — Authoritative Metric, Curvature, and ω₀

**Status:** SINGLE AUTHORITATIVE REFERENCE — metric / curvature / ω₀  
**Date:** August 2026 (metric convention locked)  
**Rule:** All other files must use this convention. Conflicting $4\ell_0^2$ vs $16\ell_0^2$ forms are **superseded**.

---

## 1. Locked right-conoid metric

Coordinates: $u\ge 0$ (radial), $v\in\mathbb{R}/2\pi\mathbb{Z}$ (angular).

$$
\boxed{
ds^2 = du^2 + f(u,v)^2\,dv^2,
\qquad
f(u,v) = \sqrt{\,u^2 + 4\ell_0^2\cos^2(2v)\,}
}
$$

**Convention lock:**

| Item | Locked choice |
|------|----------------|
| Tip coefficient | **$4\ell_0^2$** (not $16\ell_0^2$) |
| Angular harmonic | $\cos(2v)$ (even, bridge-compatible) |
| $n_{\rm bridges}$ | 12 |
| $D_{\rm bridge}=\Delta\theta$ | $2\pi/12$ |

### Why $4\ell_0^2$ (not $16\ell_0^2$)

- Matches the spin-connection / Dirac discretizations used in the continuum residual locks.
- $16\ell_0^2$ appeared in older draft normalizations equivalent to absorbing a factor $2$ into a redefinition of $\ell_0$ or of the angular period; **that redefinition is forbidden** once $G_N=64\pi\ell_0^2/45$ is locked.
- Any file still writing $f^2=u^2+16\ell_0^2\cos^2(\cdot)$ must be read as **superseded** by this box.

### Product geometry

4D spacetime $\times$ conoid: overall scale of the internal metric is carried by $\ell_0$; Seeley–DeWitt coefficients use this $f$ only.

---

## 2. Curvature (consistent with locked $f$)

For $ds^2=du^2+f^2 dv^2$, the Gaussian curvature is

$$
K = -\frac{1}{f}\,\partial_{uu} f
$$

(with standard 2D formula for this diagonal metric). Tip curvature maxima occur where $\lvert\cos(2v)\rvert$ extremizes the angular profile at fixed small $u$ — **defect locus** for continuum $\eta_{ij}$ (doc 32).

| Quantity | Role |
|----------|------|
| $R_{\rm curvature}$ | Local axial curvature radius from $K$ / tip geometry |
| $D_{\rm bridge}$ | $2\pi/12$ |
| Casimir tip potential | $C_g=(6/5,1,4/5)$ generation weights |

Seeley–DeWitt $a_2,a_4$ expansions **must** use this $f$; mixing $4$ vs $16$ in different files invalidates coefficient comparison.

---

## 3. Geometric ω₀ (locked)

$$
\omega_0
=
\left(
\frac{R_{\rm curvature}}{D_{\rm bridge}}
\right)^{4/13}
\approx 0.927.
$$

| Property | Statement |
|----------|-----------|
| Free fit? | **No** |
| Retune to $m_H$ / angles? | **Forbidden** |
| Metric dependence | $R_{\rm curvature}$ computed from **locked** $f$ only |

---

## 4. Dual-Zero pointer

$$
\varepsilon(n)=\omega_0(-1)^n n^{-n},
\qquad
\operatorname{Reg}_2(f)(n)=\frac{f(2n)+f(2n+1)}{2}.
$$

Axioms A1–A5: **doc 18**. Constructive numerical realization: **doc 39**.

---

## 5. Scales

| Scale | Definition |
|-------|------------|
| $\ell_0$ | $G_N=64\pi\ell_0^2/45$ |
| $\Lambda_0=1/\ell_0$ | UV geometric scale |
| $m_H$ class | 125 GeV class from $a_4$ |
| $M_*=\sqrt{\Lambda_0 m_H}$ | VL_Q intermediate (doc 33) |

---

## 6. Supersession

- $f=\sqrt{u^2+16\ell_0^2\cos^2(\cdot)}$ → **superseded**
- Any $\omega_0$ from a mixed metric → **superseded**
- Papers/ must defer to this note + STATUS

---

*Metric convention locked August 2026 — $4\ell_0^2$ only.*
