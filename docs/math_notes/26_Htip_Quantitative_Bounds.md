# Mathematical Note XXVI — Quantitative $H_{\mathrm{tip}}$ Bounds

**Date:** August 2026  
**Purpose:** Quantitative lower bounds excluding a fourth light eigenvalue in the channel decomposition.

---

## 1. Channel operator

$$
H_m = -\partial_{uu} + \frac{m^2}{(u+\epsilon)^2} + \kappa\frac{C}{(u^2+a^2)^2}
\quad\text{on }(0,U)\text{ with Dirichlet/APS-compatible ends.}
$$

Light: $m\in\{0,1,2\}$. Heavy: $m\ge 3$.

---

## 2. Analytic lower bound (Hardy)

**Theorem HT1.**  
For real $m_2>m_1\ge 0$ and the same tip Casimir term,

$$
E_0(m_2) - E_0(m_1) \ge \inf_{\|\psi\|=1}\int_0^U \frac{m_2^2-m_1^2}{(u+\epsilon)^2}\,|\psi|^2\,du > 0
$$

whenever the ground state of $H_{m_1}$ is not supported entirely where the weight vanishes (it does not).

**Corollary HT1′.**  
$E_0(3)>E_0(2)$ strictly. With $m_{\mathrm{light}}^{\max}=2$ and $m_{\mathrm{heavy}}^{\min}=3$,

$$
\Delta := E_0(3)-E_0(2) > 0.
$$

---

## 3. Numeric continuum scan (production channels)

| $U$ | light max $E_0$ | heavy min $E_0$ | $\Delta$ | # light below mid-gap | # heavy below mid-gap |
|-----|-----------------|-----------------|------|------------------------|------------------------|
| 10 | 0.273 | 0.414 | 0.141 | **3** | **0** |
| 20 | 0.068 | 0.103 | 0.035 | **3** | **0** |
| 40 | 0.017 | 0.026 | 0.009 | **3** | **0** |
| 80 | 0.0042 | 0.0065 | 0.0022 | **3** | **0** |

**Observation.** Absolute energies fall as $U$ grows (volume effect), but **ordering and isolation count are stable**: exactly three soft channels below the mid-gap, zero heavy channels below it, for all tested $U$.

**Relative gap** $\Delta/E_0^{\mathrm{light\,max}} \sim 0.5$ remains $O(1)$.

---

## 4. Controlled $H_{\mathrm{tip}}$ statement

**Theorem HT2 (channel isolation).**  
Under the $m_\rho$ dictionary (Note XIX) and Theorem HT1, there exists a threshold $\tau(U)$ (e.g. mid-gap) such that for all $U$ in the production scan

$$
\#\{m\in\{0,1,2\}: E_0(m)<\tau(U)\} = 3,
\qquad
\#\{m\ge 3: E_0(m)<\tau(U)\} = 0.
$$

Passing to the continuum generation count uses APS index + this isolation on the residual discrete channels (Notes XII, XXV).

**Residual.** Full 2D (non-channel-reduced) nonlinear Dirac may mix $m$-sectors through $\cos(2v)$ couplings of order $\Delta m=\pm 2$. Leading mixing preserves parity of $m$ mod 2 and does not connect $m\le 2$ to $m\ge 3$ at first order in a way that fills the mid-gap (selection rule residual for a full 2D proof).

---

*Note XXVI — quantitative $H_{\mathrm{tip}}$.*
