# 43 — APS index attempt, ω₀ search, and G_N scheme table

**Date:** 23 November 2026 (America/Chicago)  
**SSOT:** [`STATUS_CLAIMS_AND_RESIDUALS.md`](../../STATUS_CLAIMS_AND_RESIDUALS.md)  
**Code:** `code/aps_disk_modes.py`, `code/aps_projection.py`, `code/omega0_search.py`, `code/gn_prefactor_schemes.py`

---

## 1. A theorem that did close: $C_0=2\pi\ln 2$

On the unit metric $\ell_0=1$, the regularised volume finite part is exactly $C_0=2\pi\ln 2$. The proof is in the core paper (Fourier series of $\ln(\cos t)$ and an elementary radial antiderivative). Quadrature is consistent: $(C_0(U)-2\pi\ln 2)\,U^2$ is approximately constant. The older band $4.43$–$4.45$ remains withdrawn.

This does **not** determine $\omega_0$ or $\alpha$.

---

## 2. APS index and “three light channels”

Known answers on the disk are due to Falomir, Gamboa Saraví and Santangelo, *J. Math. Phys.* **39** (1998), 532–544 (arXiv:hep-th/9609194): for $\kappa=0$, no zero modes and $\lambda=\pm j_{n,l}/R$; for $k<\kappa\le k+1$, the index is $k+1$.

What was implemented:

- A *spectral projection* (not a penalty) of a boundary operator, on the truncated conoid, on top of the Hermitian 2D Dirac of `aps_hermitian.py`.
- A mode-by-mode radial SAT scheme on the disk (`aps_disk_modes.py`).

What held, and what did not:

- On the disk, the $n=1$ family approaches the first zero of $J_1$ to about $0.02$ at $N=80$. The scheme is not exactly Hermitian, some eigenvalues are non-real and must be discarded, the $J_0$ family is less stable under an imaginary-part cut, and a numerical count of zero modes at $\kappa\neq 0$ did **not** reproduce the Falomir index. That test remains open.
- On a truncated conoid $u\in[0.5,U]$, the restricted operator is Hermitian (error $\sim 10^{-17}$). Low-lying eigenvalues come in $\pm$ pairs with $\langle\gamma^5\rangle\approx 0$. In a $14\times 14$ scan, $|\lambda|_{\min}\approx 0.123,\,0.033,\,0.014$ at $U=3,5,7$. No isolated triplet of chiral zero modes is seen. The extracted discrete boundary operator had a four-dimensional kernel, already in tension with a 1D Dirac operator on a circle ($h\in\{0,1\}$), so a numerical “index” from that run is **not** a reliable APS index.

**Verdict.** Conjecture “three light Dirac channels / APS index 3” is **not supported** by these numerics and is **not cleanly refuted**. It remains **open**. The radial soft block $\{0,1,2\}$ is a separate heuristic and is not an index theorem.

---

## 3. $\omega_0$ and $4/13$

A systematic search (`code/omega0_search.py`) found no unique geometric $R_{\mathrm{curv}}$ and no derivation of $4/13$. Natural radii still give $\omega_0>1.22$ under $(R/D)^{4/13}$. The exponents $p$ that would be needed for $0.927=(R/D)^p$ are negative, far from $4/13$. Closest simple constants: $\sqrt{6/7}\approx 0.9258$ and $13/14\approx 0.9286$; both differ from $0.927$ by more than $10^{-3}$ and are not derivations. Dual-Zero weights scale linearly with $\omega_0$. The parameter remains a **free input**.

---

## 4. $G_N=\alpha\ell_0^2$ by scheme

Formula used (notes 09/14): $\alpha=1/(16\pi\,C_{\mathrm{SA}}\,\phi_2\,\mathrm{Vol}_{\mathrm{reg}})$ with $\Lambda=1/\ell_0$ and $G_N=\kappa^2/(8\pi)$.

For $\mathrm{Vol}_{\mathrm{reg}}=C_0=2\pi\ln 2$ and $\phi_2=\tfrac12$ (sharp cutoff or $f(v)=e^{-v^2}$):

| $C_{\mathrm{SA}}$ (hypothesis, not derived on the conoid) | $\alpha$ | $\alpha/(64\pi/45)$ |
|---|---:|---:|
| $1/(24\pi^2)$ | $2.164$ | $0.484$ |
| $1/(4\pi^2)$ | $0.361$ | $0.081$ |

Using $f(v)=e^{-v}$ ($\phi_2=1$) halves those values. Using a truncated area $\pi U^2+2\pi\log U+C_0$ changes $\alpha$ by a large factor. The recorded $64\pi/45$ is still a **convention lock**, equivalent to $C_{\mathrm{SA}}\phi_2\mathrm{Vol}=45/(1024\pi^2)$. No unique geometric $\alpha$ is claimed. The CCM Standard Model Einstein–Hilbert coefficient is for a finite Hilbert space, not the conoid, and was not used to produce an $\alpha$.

---

*Doc 43 — 23 November 2026.*
