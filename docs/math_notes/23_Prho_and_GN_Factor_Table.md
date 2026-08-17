# Mathematical Note XXIII — $P_\rho$ Projectors + $G_N$ Factor Table

**Date:** August 2026  
**Purpose:** Close two micro-residuals: explicit projectors implementing the $m_\rho$ dictionary, and a transparent $C_{\mathrm{SA}}\phi_2 C_0$ factor table.

---

## Part A — Fourier-sector projectors (operational $P_\rho$)

On the 12-bridge space $\mathbb{C}^{12}$ with unitary DFT basis $e^{ikv}$, define orthogonal projectors by angular momentum content (Note XIX):

$$
P_{\mathrm{light}} = \sum_{|m|\in\{0,1,2\}} \lvert k_m\rangle\langle k_m\|,\qquad
P_{\mathrm{heavy}} = \sum_{|m|\in\{3,4,5,6\}} \lvert k_m\rangle\langle k_m\|.
$$

**Numeric verification:**

| Object | Value |
|--------|-------|
| $\mathrm{rank}\,P_{\mathrm{light}}$ | 5 ($=1+2+2$) |
| $\mathrm{rank}\,P_{\mathrm{heavy}}$ | 7 ($=2+2+2+1$) |
| Hermiticity error | $<10^{-15}$ |
| Idempotence error | $<10^{-14}$ |
| $P_{\mathrm{light}}+P_{\mathrm{heavy}}$ | $I_{12}$ |

**Interpretation.**  
$P_{\mathrm{light}}$ is the operational projector for soft-barrier channels ($m_\rho\le 2$) used by $H_{\mathrm{tip}}$. Full $A_5$ character projectors $P_\rho$ refine this into $1\oplus 3\oplus 3'$ inside the light block and isolate the $5$ inside the heavy block; the Fourier split already implements the barrier dichotomy required by Theorems T1–T2.

**C5 check.**  
A standard icosahedral $C_5$ (two 5-cycles, two fixed vertices) has $\mathrm{tr}=2$, matching $\chi_{\mathrm{Perm}}(5\text{-cycle})=2$. Eigenvalues of this permutation matrix are the expected 5th roots of unity with multiplicities compatible with $1\oplus 3\oplus 3'\oplus 5$.

**Code:** `code/prho_projectors.py`

---

## Part B — $G_N$ factor table

From Note XVII:

$$
C_0 \approx 4.45,\qquad
C_{\mathrm{SA}}\,\phi_2\,C_0 = \frac{45}{1024\pi^2}\approx 4.453\times 10^{-3}
$$

for the locked $\alpha=64\pi/45$. Hence

$$
C_{\mathrm{SA}}\,\phi_2 \approx 1.001\times 10^{-3}.
$$

| Assumed $C_{\mathrm{SA}}$ | Numerical value | Implied $\phi_2$ |
|--------------------------|-----------------|------------------|
| $1/(24\pi^2)$ | $4.22\times 10^{-3}$ | $\approx 0.237$ |
| $1/(16\pi^2)$ | $6.33\times 10^{-3}$ | $\approx 0.158$ |
| $1/(48\pi^2)$ | $2.11\times 10^{-3}$ | $\approx 0.474$ |
| $1/(2\pi^2)$ | $5.07\times 10^{-2}$ | $\approx 0.020$ |

**Theorem-level statement (unchanged).**  
$G_N=\alpha\ell_0^2$ with $\alpha$ fixed by the product $C_{\mathrm{SA}}\phi_2 C_0$. Individual factors are **scheme conventions**, not independent geometric predictions. The table makes the lock auditable.

---

*Note XXIII.*
