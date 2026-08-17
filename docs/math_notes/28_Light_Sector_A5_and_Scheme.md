# Mathematical Note XXVIII — Light-Sector $A_5$ Refinement + Scheme Separation

**Date:** August 2026  
**Purpose:** Items 6–7: refine inside the light sector; separate proved vs numeric; scheme note for $64\pi/45$; Lorentzian residual flag.

---

## 1. Full $A_5$ averaging (refinement)

**Standard character projectors** on $\mathcal{H}_{\mathrm{br}}=\mathbb{C}^{12}$:

$$
P_\rho = \frac{\dim\rho}{60}\sum_{g\in A_5}\chi_\rho(g^{-1})\,\rho_{\mathrm{Perm}}(g).
$$

| $\rho$ | $\dim$ | Block |
|--------|--------|-------|
| $1$ | 1 | light |
| $3$ | 3 | light |
| $3'$ | 3 | light |
| $5$ | 5 | heavy |
| $4$ | 4 | absent in $\mathrm{Perm}_{12}$ |

**Status.** Fourier $P_{\mathrm{light}}$ (rank 5) already isolates the soft barrier sector containing $1\oplus 3\oplus 3'$ after the known decomposition $\mathrm{Perm}_{12}\cong 1\oplus 3\oplus 3'\oplus 5$. Full 60-element averaging refines **inside** the light block; it does **not** reopen the heavy/light gap controlled by $m_\rho$.

**Residual.** Explicit matrix elements of all 60 permutations of the icosahedron vertices in code — bookkeeping, not a new principle.

---

## 2. Proved vs numeric (clear separation)

| Claim | Analytic | Numeric support |
|-------|----------|-----------------|
| APS index on smoothings | Proved | — |
| $C_4$ equivariance | Proved | — |
| $E_0(m)$ monotone in $m^2$ | Proved (HT1) | Confirmed |
| Isolation 3+0 channels | Proved ordering + dictionary | Production pipeline XXVII |
| Gap $\Delta>0$ | Proved (HT1′) | Quantified vs $U$ |
| Conjecture S | Corollary of L4 package | Smoothing path continuous |
| $G_N\propto\ell_0^2$ | Proved | — |
| $64\pi/45$ | Convention lock | Factor table XXIII |
| Continuum residual $<10^{-3}$ in old 2D FD | — | **Prototype only**; channel pipeline supersedes for isolation |

---

## 3. Scheme dependence of $64\pi/45$

Higher Seeley–DeWitt terms affect the Higgs **class**, not the structural $G_N\propto\ell_0^2$ theorem. The pure prefactor absorbs $(C_{\mathrm{SA}},\phi_2,C_0)$ and is **scheme-dependent** by construction (Notes XIV, XXIII). No claim of scheme-free digit identity beyond proportionality.

---

## 4. Lorentzian / causality residual

Wick-rotation / Lorentzian reconstruction remains at residual discipline level (Note VII). No pure-math generation or $G_N\propto\ell_0^2$ claim depends on a completed Lorentzian theorem.

---

## 5. Uniqueness

Absolute uniqueness is **not** claimed (Note IV, X). Joint geometric axioms prefer $N=12$, $c=4$; nearby deformations fail those axioms.

---

*Note XXVIII — light sector and scheme separation.*
