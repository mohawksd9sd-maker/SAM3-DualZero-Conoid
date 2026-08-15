# Mathematical Note V — Tip Coefficient Deformation ($c\neq 4$)

**Date:** August 2026  
**Status:** Controlled proxy + residual for full APS  
**Locked metric:** $c=4$ in $f=\sqrt{u^2+c\ell_0^2\cos^2(2v)}$

---

## 1. Setup

Hold $\ell_0$ fixed from $G_N=64\pi\ell_0^2/45$. Vary tip coefficient $c$ and track schematic tip scale, $\omega_0$ rescaling, and Cabibbo proxy.

Tip scale $\sim\sqrt{c}\,\ell_0$. If $\omega_0$ is recomputed from curvature $\propto\sqrt{c}$:

$$
\frac{\omega_0(c)}{\omega_0(4)} = \left(\frac{c}{4}\right)^{2/13}.
$$

Defect-overlap proxy (order-of-magnitude width sensitivity):

$$
\eta(c) \approx \eta(4)\,\bigl[1+\kappa(\sqrt{c/4}-1)\bigr],\qquad \kappa\sim 0.08.
$$

---

## 2. Numerical proxy table

| $c$ | tip/tip$_4$ | $\omega_0$ factor | $\eta_{12}$ proxy | Cabibbo proxy | $\Delta$ vs $12.85^\circ$ |
|-----|------------|-------------------|-------------------|---------------|-------------------------|
| 1 | 0.50 | 0.81 | 0.826 | $12.39^\circ$ | $-0.5^\circ$ |
| 2 | 0.71 | 0.90 | 0.841 | $12.61^\circ$ | $-0.2^\circ$ |
| **4** | **1** | **1** | **0.861** | **$12.91^\circ$** | **$\sim 0$** |
| 8 | 1.41 | 1.11 | 0.889 | $13.34^\circ$ | $+0.5^\circ$ |
| 16 | 2.00 | 1.24 | 0.930 | $13.94^\circ$ | $+1.1^\circ$ |

---

## 3. Conclusions

1. At fixed $\ell_0$, $c\neq 4$ moves Cabibbo by **$O(0.1^\circ$–$1^\circ)$** in this proxy.  
2. $c=16$ also forces $\omega_0$ rescaling $\sim +24\%$ if curvature tracks $\sqrt{c}$ — incompatible with locked $\omega_0\approx 0.927$ without retuning.  
3. **Full 2D APS eigensolves at each $c$ remain prototype work** (STATUS flag). This note is a controlled sensitivity bound, not a replacement APS archive.

---

## 4. Residual

Production APS spectra on manufactured grids for $c\in\{1,2,4,8,16\}$ with frozen $(N_u,N_v,u_{\max})$.

---

*Tip coefficient deformation — August 2026.*
