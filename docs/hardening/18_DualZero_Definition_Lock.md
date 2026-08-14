# Dual-Zero Regulator — Definition Lock

**Status:** Locked definition (August 2026)  
**Rule:** Derivation only; no experimental tuning; no overclaim.

This note is the **canonical Dual-Zero definition** for the hardened corpus.  
Older Dual-Zero paper language (especially digit-level Higgs slogans) is superseded where it conflicts.

---

## 1. Canonical sequence

$$
\varepsilon(n) = \omega_0\, (-1)^n\, n^{-n},\qquad n\in\mathbb{N},\quad \omega_0>0.
$$

- Alternating sign: compatible with the $\sin(2v)$ / bridge grading structure.
- Super-exponential decay $n^{-n}=\exp(-n\ln n)$: UV modes decouple faster than any exponential.
- $\omega_0$ is **not** a free fit parameter (see §2).

---

## 2. Geometric regulator strength

$$
\omega_0
=
\left(
\frac{R_{\rm curvature}}{D_{\rm bridge}}
\right)^{4/13}
\approx 0.927.
$$

- $R_{\rm curvature}$: local axial curvature radius of the right conoid.
- $D_{\rm bridge}$: mean angular spacing of the 12 icosahedral bridges ($\sim 2\pi/12$).
- Value is fixed by geometry already present in the model; no retuning to $m_H$ or mixing angles.

---

## 3. Symmetric regularization operator

On sequences / spectral data:

$$
\operatorname{Reg}_2(f)(n)
:=
\frac{f(2n)+f(2n+1)}{2}.
$$

On the Dual-Zero sequence itself, the regularized infinitesimal is the ultrapower class of the $\operatorname{Reg}_2$-averaged sequence (non-principal ultrafilter $\mathcal{U}$ on $\mathbb{N}$), with standard part $\mathrm{st}_{\mathcal{U}}$ taken for physical observables.

**Interpretation:** symmetric pairing restores positivity / ordering while preserving information that a hard cutoff would erase.

---

## 4. Axioms (locked statement of intent)

| Code | Name | Content |
|------|------|---------|
| **A1** | Linearity | $\operatorname{Reg}_2$ extends linearly to finite signed measures on $[0,\infty)$. |
| **A2** | Grading compatibility | Antisymmetric signed measures are annihilated: $\operatorname{Reg}_2(\nu)=0$ when $\nu\mapsto -\nu$. |
| **A3** | Super-exponential decay | Regularized tails obey bounds of the form $\lvert\operatorname{Reg}_2(f)(n)\rvert \le C_f \exp(-c\log^2 n)$ for poly-growth test data. |
| **A4** | Standard-part compatibility | Symmetric averaging is compatible with the standard-part map on observables. |
| **A5** | Ultrafilter independence | Physical (even) observables’ standard parts are independent of the choice of non-principal ultrafilter at the level required by the model. |

These are the Dual-Zero rules used throughout the hardening locks (Casimir tip potential, continuum residual context, Seeley–DeWitt evaluation, spectral action).

---

## 5. Role in the spectral triple

Schematically:

$$
D = D_{\rm geo} + D_{\rm bridge} + D_{\rm DZ},
$$

with $D_{\rm DZ}$ built from $\operatorname{Reg}_2(\varepsilon)$ (and finite-algebra terms as in the almost-commutative product). Dual-Zero is the UV / information-conserving regulator of the infinite conoid spectrum.

---

## 6. What Dual-Zero is allowed to claim

| Allowed | Not allowed |
|---------|-------------|
| UV regulator with geometric $\omega_0$ | Free continuous parameter fitted to experiment |
| Information-conserving alternative to hard cutoffs | Digit-level $m_H=125.1$ GeV as a Dual-Zero output |
| Input to tip potential / Casimir radial problems (docs 07, 09) | Proof of the classical Riemann Hypothesis |
| Input to spectral-action / Seeley–DeWitt evaluation (doc 13) | Percent-level gauge unification by itself |
| Consistency with continuum residual discipline (doc 10) | Overwrite of locked CKM angles by retuning $\omega_0$ |

Higgs mass remains the **125 GeV class** (theoretical band under present residuals), not a Dual-Zero-tuned digit match.  
RH remains a **variational proposal** related to the information current, not a theorem (doc 17).

---

## 7. Consistency with frozen archive

From `docs/hardening/16_Frozen_Numerical_Archive.md`:

- `omega0_geometric` $\approx 0.927$
- Dual-Zero sequence form as above
- Used together with defect overlaps, $C_g$, and $\phi=2\pi/5$ without retuning $\omega_0$

---

## 8. Canonical references in the repo

| File | Role |
|------|------|
| **This note** | Authoritative Dual-Zero definition lock |
| `SAM3_DualZero_Conoid_Core_Definitions.tex` | Expanded axiom / geometry companion (read under residual discipline for RH sections) |
| `papers/SAM3_Paper_02_DualZero_Expanded.tex` | Ultrapower / $\operatorname{Reg}_2$ development (phenomenology slogans superseded) |
| `papers/SAM3_DualZero_Information_Conserving_Arithmetic.tex` | Arithmetic motivation (calibrated) |
| `STATUS_CLAIMS_AND_RESIDUALS.md` | Executive claim map |

---

## 9. Lock statement

> The Dual-Zero regulator is defined by $\varepsilon(n)=\omega_0(-1)^n n^{-n}$ with geometrically fixed $\omega_0=(R_{\rm curv}/D_{\rm bridge})^{4/13}\approx 0.927$, the symmetric operator $\operatorname{Reg}_2$, and axioms A1–A5. It is the UV / information-conserving regulator of the SAM3 spectral triple. It is not a free experimental knob, not a digit-level Higgs tuner, and not a completed proof of the Riemann Hypothesis.

---

*Locked under the rule: derivation only, no tuning, no overclaim.*
