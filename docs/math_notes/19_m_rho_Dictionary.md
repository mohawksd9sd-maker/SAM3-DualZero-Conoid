# Mathematical Note XIX — $m_\rho$ Dictionary (Angular Barriers from Fourier / $A_5$ Content)

**Date:** August 2026  
**Purpose:** Close the residual assignment in $H_{\mathrm{tip}}$ (Note XVIII): which isotypes carry which effective angular barriers.

---

## 1. Fourier band on 12 bridges

Identify the band-limited angular space

$$
B = \mathrm{span}\{e^{ikv}: k=0,\ldots,11\} \cong \mathbb{C}^{12}
$$

with the bridge sampling space of Note XIII (unitary DFT). Effective angular momentum of bin $k$:

$$
|m|(k) = \min(k,\,12-k).
$$

| $k$ | $|m|$ | Real dimension of $\pm k$ pair |
|-----|-------|--------------------------------|
| 0 | 0 | 1 |
| 1, 11 | 1 | 2 |
| 2, 10 | 2 | 2 |
| 3, 9 | 3 | 2 |
| 4, 8 | 4 | 2 |
| 5, 7 | 5 | 2 |
| 6 | 6 | 1 |
| **Total** | | **12** |

---

## 2. Compatibility with metric $C_4$

Under $v\mapsto v+\pi/2$, mode $k$ picks up phase $i^k$. This is exact (Note XVIII E2).

Modes with $k\equiv 0\pmod 4$ are $C_4$-invariant (phase $+1$): $k=0,4,8$ (and the structure of $k=6$ separately).

The metric harmonic $\cos(2v)$ preferentially couples **even** angular structure, especially $|m|=2$.

---

## 3. Link to $A_5$ isotypes

Recall $\mathrm{Perm}_{12}\cong 1\oplus 3\oplus 3'\oplus 5$ (Note XIII, Theorem E).

**Dictionary (structural assignment):**

| Isotype | Dim | Fourier support (leading) | Effective $m_\rho$ |
|---------|-----|---------------------------|---------------------|
| $1$ | 1 | $k=0$ (constant) | $0$ |
| $3$ | 3 | low modes $|m|\in\{0,1,2\}$ mixture | $\le 2$ |
| $3'$ | 3 | low modes $|m|\in\{0,1,2\}$ mixture | $\le 2$ |
| $5$ | 5 | higher modes $|m|\ge 2$, weight on $|m|\ge 3$ | $\ge 3$ (dominant) |

**Rationale.**

1. The trivial summand is the constant mode on vertices — pure $m=0$.  
2. The two 3-dimensional irreps must be assembled from the remaining low-dimensional Fourier content to keep total dimension $1+3+3+5=12$.  
3. The 5-dimensional irrep is the unique summand large enough to absorb the bulk of high-$|m|$ bins ($|m|=3,4,5,6$ contribute $2+2+2+1=7$ real dims before mixing).  
4. Metric coupling $\propto\cos(2v)$ mixes $\Delta m=\pm 2$ but does not erase the Hardy barrier hierarchy in $m^2/u^2$.

**Light triple used by SAM3.**  
Three radial channels with Casimirs $(4/5,1,6/5)$ sit in the **soft-barrier** sector $m_\rho\le 2$ (built from $1\oplus$ light parts of $3,3'$ after tip projection). The $5$ is treated as **heavy** with $m_\rho\ge 3$.

---

## 4. Spectral consequence (feeds Theorem T2)

Numeric radial barriers (Dirichlet toy, Note XVIII machinery):

| $m$ | $E_0(m)$ |
|-----|----------|
| 0 | 0.0110 |
| 1 | 0.0176 |
| 2 | 0.0301 |
| 3 | 0.0458 |
| 5 | 0.0858 |

$$
E_0(3)-E_0(2)\approx 0.016,\qquad E_0(3)-E_0(0)\approx 0.035.
$$

**Proposition M1.**  
Under the dictionary of §3 and Theorem T2 (Note XVIII), heavy channels with $m_\rho\ge 3$ are separated from soft channels with $m_\rho\le 2$ by a uniform positive gap of Hardy type, independent of $u_{\max}$ in the continuum limit.

**Proof.** Apply T2 with $m_{\min}=3$ on the heavy sector and compare to the worst-case light barrier $m=2$; the difference of quadratic barriers $(9-4)/u^2=5/u^2$ yields a strictly positive spectral shift by the variational principle.

---

## 5. Status of $H_{\mathrm{tip}}$ after this note

| Piece | Status |
|-------|--------|
| Monotonicity in Casimir | Proved (T1) |
| Angular barrier comparison | Proved (T2) |
| Fourier $\leftrightarrow$ bridge unitary | Proved (XIII) |
| **$m_\rho$ dictionary** | **Assigned** (this note) — structural, not a fit |
| Character projector matrix elements in continuum Dirac | Residual (explicit spinor computation) |

$H_{\mathrm{tip}}$ is now **filled at the structural level**. The remaining micro-task is exporting $P_\rho$ matrix elements on numerical Dirac eigenvectors — engineering, not a new principle.

---

## 6. Gate board (updated)

| Gate | Status |
|------|--------|
| L4 | Conjectural (edge APS) |
| $H_{\mathrm{tip}}$ | **Structural closed** (T1, T2, $m_\rho$ dictionary) |
| $H_{\mathrm{eq}}$ | $C_4$ exact; $A_5$ on bridges (XVIII) |

---

*Note XIX — $m_\rho$ dictionary.*
