# Precision Push — Derivation Only (Completable Items)

**Status:** Pushed without experimental retuning (August 2026)  
**Rule:** Only items that can advance from existing locked geometry.

---

## 1. Scope

| Item | Action |
|------|--------|
| $\theta_{13}$ | Geometric chain estimate + consistency with locked bi-unitary value |
| $\delta_{\rm CKM}$, $J$ | Explicit reconstruction from locked angles + $\phi=2\pi/5$ |
| Light Yukawa residual | Residual control under $\kappa_u/\kappa_d=1/2$ |
| $\delta_{\rm PMNS}$ band | Geometry-limited narrowing rule |
| Higgs sub-GeV | Path only — no false digit |

**Not pushed:** percent-level unification, $\Lambda$ magnitude, RH proof.

---

## 2. Geometric $\theta_{13}$ chain

Cabibbo is locked as $\theta_{12}\approx\eta_{12}\times\pi/12$.

Generation 1–3 tip hierarchy:

$$
\frac{c_3}{c_1}=\frac{c_3}{c_2}\cdot\frac{c_2}{c_1}\approx 2.46\times 1.13\approx 2.78.
$$

**Reduced estimate (no free continuous parameter):**

$$
\theta_{13}\sim\frac{\eta_{13}}{\eta_{12}}\cdot\frac{c_1}{c_3}\cdot\theta_{12}
\approx 0.632\times 0.360\times 12.85^\circ
\approx 2.92^\circ.
$$

This overestimates the locked bi-unitary value $\theta_{13}\approx 0.24^\circ$ because full hierarchical Yukawa diagonalization adds further 1–3 suppression beyond tip-amplitude ratios alone.

**Locked precision statement:**  
$\theta_{13}\approx 0.24^\circ$ remains the output of continuum defect + Casimir Yukawa bi-unitary (doc 11). A reduced $\eta$–$C_g$ formula that recovers $0.24^\circ$ without singular vectors is **not** claimed. The chain explains $\theta_{13}\ll\theta_{12}$. Experiment $\approx 0.20^\circ$ — residual $\sim 0.04^\circ$.

---

## 3. Explicit CKM reconstruction

Script: `code/ckm_from_geometry.py`

**Inputs (locked):** $\theta_{12}=12.85^\circ$, $\theta_{23}=2.36^\circ$, $\theta_{13}=0.24^\circ$, $\phi=2\pi/5$.  
**Rephasing map:** $\delta_{\rm CKM}\approx\phi-\theta_{13}$.

**Regenerated geometric outputs (no retuning):**

| Observable | Value |
|------------|-------|
| $\delta_{\rm CKM}$ | $\approx 71.8^\circ$ |
| $J$ | $\approx 3.55\times 10^{-5}$ |
| $\|V_{ud}\|$ | $\approx 0.975$ |
| $\|V_{us}\|$ | $\approx 0.222$ |
| $\|V_{ub}\|$ | $\approx 0.0042$ |
| $\|V_{cb}\|$ | $\approx 0.041$ |
| $\|V_{tb}\|$ | $\approx 0.999$ |

Jarlskog formula:

$$
J=\frac18\sin 2\theta_{12}\sin 2\theta_{23}\sin 2\theta_{13}\cos\theta_{13}\sin\delta.
$$

**Locked claim:** CKM magnitudes and CP observables are reconstructible from the locked angle set + $\phi$; no free CKM parameter.

---

## 4. Light Yukawa residual control

Under $\kappa_u/\kappa_d=1/2$ (doc 14): leading light-up factor-$\sim 2$ tension is removed. Remaining light-mass digit residuals are attributed to higher-order continuum overlaps and Dual-Zero moments — **not** to a missing free parameter. No PDG retuning.

---

## 5. $\delta_{\rm PMNS}$ band discipline

Large phase from $\phi=2\pi/5$ stays locked. Narrowing the $200^\circ$–$270^\circ$ band requires a **derived** RH radial hierarchy $(1,r_2,r_3)$ from conoid localization. Until that is frozen with error bars, no single-degree central value is claimed.

---

## 6. Higgs sub-GeV path

Still 124–127 GeV class. Path = warped $a_4$ + radiative matching. No invented digit.

---

## 7. Lock statement

> Completable precision items were advanced only from locked $\eta_{ij}$, $C_g$, $\phi$, and bi-unitary structure. $\theta_{13}$ remains bi-unitary-locked at $\approx 0.24^\circ$; $\delta_{\rm CKM}\approx 71.8^\circ$ and $J\approx 3.55\times 10^{-5}$ are reconstructed from locked inputs; light-Yukawa residual is higher-order continuum/Dual-Zero under $\kappa_u/\kappa_d=1/2$; $\delta_{\rm PMNS}$ stays a large band. No experimental retuning.

---

*Derivation only. Run: `python code/ckm_from_geometry.py`.*
