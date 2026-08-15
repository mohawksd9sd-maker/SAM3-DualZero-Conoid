# 34 — AF′ Unified Layer (Beyond AF)

**Status:** Research layer complete (derivation-only)  
**Date:** August 2026  
**Depends on:** doc 33 (VL_Q unification path)

---

## 1. Goal

Enlarge the finite algebra beyond

$$\mathcal{A}_F=\mathbb{C}\oplus\mathbb{H}\oplus M_3(\mathbb{C})$$

in a way **forced by 2I / conoid**, stabilize the breaking scale, and compare to $\mu_{\rm meet}$ — without continuous tuning and without claiming $M_X=\mu_{\rm meet}$.

---

## 2. Forced enlargement (Path α)

$$\mathcal{A}_F'=M_2(\mathbb{H})\oplus M_4(\mathbb{C})$$

| Input | Forces |
|-------|--------|
| 2I spinor **2** | Quaternionic $M_2(\mathbb{H})$ |
| A5 irrep **4** + **12 = 3×4** | Complex $M_4(\mathbb{C})$ |
| **4 → 1⊕3** under A4 stabilizer | $M_4\to\mathbb{C}\oplus M_3$ (lepton + color) |

After projection: recovers $\mathcal{A}_F$.

**Force level:** medium–high for matrix sizes; high for 4→1⊕3 branching.

SU(5)/SO(10) as first step: **lower** force from 2I/conoid (not chosen).

---

## 3. Projective breaking (no light X)

Tip residual A5⊃A4 with **4→1⊕3** is **representation-theoretic algebra restriction**, not spacetime Higgsing.

| Reading | Forced? | Light X at $v'$? |
|---------|---------|------------------|
| **Projective** (restrict algebra before spectral triple) | **Yes** | **No** |
| Dynamical $\Phi(x)$ with local AF′ gauge bosons | Extra assumption | Yes |

**Forced package:**

- Physical gauge group = SM
- No light X poles at $v'$
- $M_X=\Lambda_0$ if UV completion vectors exist
- Proton decay safe ($\tau_p\sim 10^{48}$ yr)

---

## 4. Finite scale $v'$ from spectral balance

### 4.1 Stationarity

Finite Dirac block (explicit model):

$$D_{F'}=\begin{pmatrix}0&\Phi\\\Phi^\dagger&0\end{pmatrix}\quad\text{on }H_L\oplus H_R$$

$$\mathrm{Tr}(D_{F'}^2)=2\,\mathrm{Tr}(\Phi^\dagger\Phi),\qquad
\mathrm{Tr}(D_{F'}^4)=2\,\mathrm{Tr}((\Phi^\dagger\Phi)^2)$$

Effective potential (Seeley $a_2$, $a_4$):

$$V(\phi)=A\Lambda_0^2 t_2\phi^2+B t_4\phi^4+C t_2 M_*^2\phi^2$$

IR scale for $\Phi$: **$m_{\rm int}=M_*$** (unique derived AF-charged intermediate; EW Higgs is tip/DZ-suppressed).

Successive UV–IR balance of the same class that defines $M_*=(\Lambda_0 m_H)^{1/2}$:

$$v'=(\Lambda_0 M_*)^{1/2}=(\Lambda_0^3 m_H)^{1/4}=\Lambda_0\,\sigma_h^{1/4}$$

### 4.2 Direction traces (O(1))

| Direction | $t_4/t_2^2$ | $(t_2/t_4)^{1/4}$ | $v'_{\rm corr}/\mu_{\rm meet}$ |
|-----------|-------------|-------------------|--------------------------------|
| Rank-1 | 1.00 | 1.00 | 0.87 |
| Full-rank equal | 0.25 | 1.41 | 1.23 |
| PS-breaking $\mathrm{diag}(1,1,1,-3)$ | 0.58 | 1.14 | **0.997** |

Representation factors are **O(1)** only; geometric mean remains in the $\mu_{\rm meet}$ ballpark.

### 4.3 Comparison policy

$v'/\mu_{\rm meet}\approx 0.87$ (bare) is a **cross-check**, not a fitting target:

- $v'$ = pure geometry ($\Lambda_0$, $m_H$)
- $\mu_{\rm meet}$ = RG diagnostic

Order-unity agreement is expected without full Einstein-frame multiplicity tables.

**Do not** replace VL_Q thresholds $(M_*,12M_*)$ by $v'$ — residual worsens.

---

## 5. Hardened statements

| ID | Statement | Force |
|----|-----------|-------|
| H1 | Projective AF′→AF; no light X; $M_X=\Lambda_0$ | **High** |
| H2 | $v'=(\Lambda_0 M_*)^{1/2}$ with $m_{\rm int}=M_*$ | **Medium–high** |
| H3 | $v'\sim\mu_{\rm meet}$ is cross-check only | Policy |
| H4 | Explicit $\mathrm{Tr}(D_{F'}^{2,4})=2\mathrm{Tr}(\Phi^\dagger\Phi)^{1,2}$; O(1) direction factors | **Closed** |

---

## 6. Numbers

| Quantity | Value |
|----------|--------|
| $\Lambda_0$ | $2.58\times 10^{19}$ GeV |
| $M_*$ | $5.68\times 10^{10}$ GeV |
| $v'_C$ (bare) | $1.21\times 10^{15}$ GeV |
| $v'_C/\mu_{\rm meet}$ | $\approx 0.87$ |
| PS-direction corrected | $\approx 1.39\times 10^{15}$ GeV ($\approx\mu_{\rm meet}$) |
| $M_X$ (forced) | $\Lambda_0$ |
| VL_Q residual (doc 33) | $\sim 2.6\%$ two-loop |

---

## 7. What is not claimed

- $M_X=\mu_{\rm meet}$
- Full classical Pati–Salam gauge group as a theorem (medium force only)
- Replacement of VL_Q thresholds by $v'$
- Complete multi-generation KO multiplicity tables for every Seeley coefficient

---

## 8. Relation to doc 33

Doc 33: VL_Q at $M_*$, $12M_*$; residual $\sim 2.6\%$; $M_X=\Lambda_0$.  
Doc 34: AF′ organizing algebra; projective break; finite $v'\sim 10^{15}$ GeV without light X.

Together: approximate unification path + geometric enlargement layer, proton-safe.
