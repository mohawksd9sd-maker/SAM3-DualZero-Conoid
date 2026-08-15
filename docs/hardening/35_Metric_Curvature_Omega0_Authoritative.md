# 35 — Authoritative Metric, Curvature, and ω₀

**Status:** SINGLE AUTHORITATIVE REFERENCE for metric / curvature / ω₀  
**Date:** August 2026  
**Rule:** All other files must cite this note (or doc 18 for Dual-Zero axioms) rather than re-deriving conflicting values.

---

## 1. Right-conoid metric (canonical)

Coordinates $(u,v)$ with $u\ge 0$ (radial) and $v\in\mathbb{R}/2\pi\mathbb{Z}$ (angular):

$$
ds^2 = du^2 + f(u,v)^2\,dv^2,
\qquad
f(u,v)^2 = u^2 + a^2\cos^2(nv).
$$

Locked discrete data:

| Symbol | Value | Meaning |
|--------|-------|--------|
| $n_{\rm bridges}$ | 12 | Binary-icosahedral bridges |
| $\Delta\theta$ | $2\pi/12$ | Mean bridge spacing $D_{\rm bridge}$ |
| Tip modulation | $\cos(2v)$ class (even under $v\to v+\pi$) | Matches bridge grading |

The overall radial unit is set by $\ell_0$ when the product geometry is formed with 4D spacetime.

**Spin connection / Dirac:** standard 2D Riemannian spin connection from $f$; APS boundary conditions at the tip/outer end as in the continuum Dirac locks (docs 10, 23–25).

---

## 2. Curvature quantities used by the model

| Quantity | Role |
|----------|------|
| Tip curvature maxima | Defect locus for continuum $\eta_{ij}$ (doc 32) |
| $R_{\rm curvature}$ | Local axial curvature radius entering $\omega_0$ |
| $D_{\rm bridge}\sim 2\pi/12$ | Angular bridge scale entering $\omega_0$ |
| Casimir tip potential | Generation radial weights $C_g=(6/5,1,4/5)$ (doc 09/16) |

Gaussian / mean curvature formulae follow from the standard 2D metric $du^2+f^2 dv^2$; explicit component expansions live in the gravity/Seeley notes (docs 13, 20). This document freezes the **inputs** those expansions must use.

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
| Origin | Conoid curvature / bridge data only |
| Free fit? | **No** |
| Retune to $m_H$ or angles? | **Forbidden** |
| Canonical Dual-Zero use | $\varepsilon(n)=\omega_0(-1)^n n^{-n}$ (doc 18) |

**Exponent 4/13:** fixed by the Seeley / spectral-dimension balance used in the Dual-Zero lock (doc 18); not adjusted per observable.

---

## 4. Dual-Zero sequence (pointer)

$$
\varepsilon(n)=\omega_0(-1)^n n^{-n},
\qquad
\operatorname{Reg}_2(f)(n)=\frac{f(2n)+f(2n+1)}{2}.
$$

Full axioms A1–A5: **doc 18** (do not duplicate conflicting statements).

---

## 5. Scale identification

| Scale | Definition |
|-------|------------|
| $\ell_0$ | Fundamental length; $G_N=64\pi\ell_0^2/45$ (Seeley $a_2$) |
| $\Lambda_0=1/\ell_0$ | UV geometric scale |
| $m_H$ class | 125 GeV class from $a_4$ (band, not digit) |
| $M_*=\sqrt{\Lambda_0 m_H}$ | Intermediate VL_Q scale (doc 33) |

---

## 6. Supersession

Any older metric, curvature radius, or $\omega_0$ formula in `papers/` that conflicts with §§1–3 is **superseded** by this note and by `STATUS_CLAIMS_AND_RESIDUALS.md`.

---

*Authoritative metric / curvature / ω₀ lock — August 2026.*
