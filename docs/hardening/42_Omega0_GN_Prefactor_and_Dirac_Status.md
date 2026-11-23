# 42 — $\omega_0$, the $G_N$ prefactor, and the Dirac operator

**Date:** 23 November 2026 (America/Chicago)  
**Status:** residual lock. This file records what is *not* derived, and what was wrong in the Dirac prototype.  
**SSOT:** [`STATUS_CLAIMS_AND_RESIDUALS.md`](../../STATUS_CLAIMS_AND_RESIDUALS.md)

---

## 1. $\omega_0$ and $4/13$

The Dual-Zero generator
$\varepsilon(n)=\omega_0(-1)^n n^{-n}$
is a definition. Doc 35 wrote
$\omega_0=(R_{\mathrm{curv}}/D_{\mathrm{bridge}})^{4/13}\approx 0.927$
with $D_{\mathrm{bridge}}=2\pi/12$. That formula is **not derived**.

Missing, and still missing after this audit:

1. A unique geometric definition of $R_{\mathrm{curv}}$. Several natural readings at the curvature maximum ($u=0$, $|\cos(2v)|=1$, $\ell_0=1$) disagree, and none gives $0.927$:

   | $R$ | $R/D$ | $(R/D)^{4/13}$ |
   |-----|-------|----------------|
   | $1/|K|_{\max}=4$ | $7.639$ | $1.869$ |
   | $1/\sqrt{|K|_{\max}}=2$ | $3.820$ | $1.510$ |
   | $\ell_0=1$ | $1.910$ | $1.220$ |

   The target $0.927$ requires $R/D\approx 0.7816$, hence $R\approx 0.409$. That radius is not singled out by $K$ or by the embedding.

2. A derivation of the exponent $4/13$. It does not follow from the Seeley–DeWitt coefficients as written in notes 09/16/20, from dimensional analysis of $K$, or from a closed variational problem in the repository. No such derivation was found, and none is invented here.

3. A reason to pair whatever $R$ is chosen with $D=2\pi/12$ inside that power.

Until those gaps close, $\omega_0$ is an **input parameter**. Calling it “geometric only” is not a proof. Do not retune it to experiment and do not treat $0.927$ as an output of the metric.

## 2. The $G_N$ prefactor

Spectral action / $a_2$ implies the structural relation $G_N=\alpha\ell_0^2$ (Chamseddine–Connes 1997 is the standard origin of the action; it does not compute $64\pi/45$ for this metric).

The recorded normalisation $G_N=64\pi\ell_0^2/45$ is a **convention lock**. Notes 09 and 16 already said so: it is equivalent to fixing
$\mathcal{N}=45/(1024\pi^2)$
and absorbing $(\phi_2,C_{\mathrm{SA}},\mathrm{Vol}_{\mathrm{reg}})$. It is not scheme-free.

The older `newton_constant_fit.py` solved $G_{\mathrm{theory}}(\ell_0)=G_{\mathrm{obs}}$ for $\ell_0$ and then reported an exact match. That is a tautology. The file is now a convention display only.

## 3. Dirac operator

`code/dirac_conoid_aps.py` builds a real first-order matrix and replaces it by $\tfrac12(D+D^T)$. Central differences are antisymmetric; the symmetrisation cancels derivative terms. The raw matrix is not Hermitian. On a flat torus this does **not** recover the analytic Dirac spectrum.

`code/aps_hermitian.py` is a complex Hermitian discretisation. Known-answer test (antiperiodic flat torus, $L=2\pi$, $N=24$): maximum absolute error $\approx 0.00202$ on the eight copies of $\pm\sqrt{1/2}$. Convergence slope on $N\in\{8,12,16,24,32\}$ is $\approx-1.995$. Hermiticity error is at machine precision.

On the truncated conoid, “APS” is a boundary penalty. Those eigenvalues are a numerical experiment, not a continuum APS theorem, and they are not an index computation of three generations.

## 4. What would close the residuals

- A unique, motivated $R_{\mathrm{curv}}$ *and* a derivation of $4/13$, or else a permanent demotion of $\omega_0$ to a free parameter (already demoted here).
- An independent recompute of $\alpha$ in $G_N=\alpha\ell_0^2$ from $a_2$ on this $f$, with every convention written down, if a specific prefactor is to be claimed.
- A genuine APS (or $b$-calculus) index calculation on a specified compactification of the conoid, or a clearly remaining conjecture (already labelled).
- Optional: a flat-disk Bessel known-answer test in addition to the torus.

No such derivation or index calculation is supplied in this file.
