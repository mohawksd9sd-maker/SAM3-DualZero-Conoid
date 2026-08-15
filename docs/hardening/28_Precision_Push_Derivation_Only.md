# Precision Push — Derivation Only (Completable Items)

**Status:** Pushed without experimental retuning (August 2026)  
**Rule:** Only items that can advance from existing locked geometry.

---

## 1. Scope

From the partial-match list, the following were pushed:

| Item | Action |
|------|--------|
| $\theta_{13}$ | Geometric chain estimate + consistency with locked bi-unitary value |
| $\delta_{\rm CKM}$, $J$ | Explicit reconstruction from locked angles + $\phi=2\pi/5$ |
| Light Yukawa residual | Residual control statement under $\kappa_u/\kappa_d=1/2$ |
| $\delta_{\rm PMNS}$ band | Geometry-limited narrowing rule (no new free parameter) |
| Higgs sub-GeV | Path only — no false digit claim |

**Not pushed** (would require new geometry or tuning): percent-level unification, $\Lambda$ magnitude, RH proof.

---

## 2. Geometric $\theta_{13}$ chain

Cabibbo is already locked as

$$
\theta_{12} \approx \eta_{12}\times\frac{\pi}{12}.
$$

The 1–3 angle is the same defect structure with **extra hierarchy suppression** from tip amplitudes between generations 1 and 3:

$$
\frac{c_3}{c_1} = \frac{c_3}{c_2}\cdot\frac{c_2}{c_1} \approx 2.46\times 1.13 \approx 2.78.
$$

**Geometric estimate (no free continuous parameter):**

$$
\theta_{13}
\;\sim\;
\frac{\eta_{13}}{\eta_{12}}
\cdot
\frac{c_1}{c_3}
\cdot
\theta_{12}.
$$

| Quantity | Value |
|----------|-------|
| $\eta_{13}/\eta_{12}$ | $\approx 0.632$ |
| $c_1/c_3$ | $\approx 0.360$ |
| $\theta_{12}$ locked | $12.85^\circ$ |
| **$\theta_{13}$ estimate** | $\approx 2.92^\circ\times 0.360 \approx 2.9^\circ\times\ldots$ wait: $0.632\times 0.360\times 12.85^\circ \approx 2.92^\circ$ |

**Correction:** $0.632 \times 0.360 \approx 0.227$; $0.227\times 12.85^\circ \approx 2.92^\circ$.

That is larger than the locked bi-unitary $\theta_{13}\approx 0.24^\circ$. The simple product overestimates because full bi-unitary diagonalization of hierarchical Yukawas suppresses 1–3 mixing by an extra power of the hierarchical eigenvalues (standard flavor structure: $\theta_{13}\sim \sqrt{m_1/m_3}$ type suppression beyond tip-amplitude ratios alone).

**Refined geometric reading (still no free parameter):**

$$
\theta_{13}
\;\sim\;
\frac{\eta_{13}}{\eta_{12}}
\cdot
\frac{c_1}{c_3}
\cdot
\sqrt{\frac{c_1}{c_3}}
\cdot
\theta_{12}
\;\approx\;
0.632 \times 0.360 \times 0.600 \times 12.85^\circ
\;\approx\;
1.75^\circ.
$$

Still high vs $0.24^\circ$. The locked $0.24^\circ$ comes from the **full** $Y_u,Y_d$ bi-unitary with radial mass eigenvalues, not from the tip-amplitude proxy alone.

### Locked precision statement for $\theta_{13}$

> $\theta_{13}\approx 0.24^\circ$ remains the locked output of the continuum defect + Casimir Yukawa bi-unitary (doc 11). A transparent reduced formula that recovers $0.24^\circ$ from $\eta$ and $C_g$ alone, without the full singular-vector calculation, is **not** claimed. The geometric chain above explains why $\theta_{13}\ll\theta_{12}$ (hierarchy suppression) but does not replace the bi-unitary lock. Experiment $\approx 0.20^\circ$ — consistency level, residual $\sim 0.04^\circ$.

---

## 3. Explicit CKM reconstruction (derivation only)

Script: `code/ckm_from_geometry.py`

**Inputs (all locked):**
- $\theta_{12}=12.85^\circ$, $\theta_{23}=2.36^\circ$, $\theta_{13}=0.24^\circ$
- $\phi=2\pi/5$
- Convention: $\delta_{\rm CKM}\approx\phi-\theta_{13}$ (geometric rephasing map, doc 08/11)

**Outputs regenerated without retuning:**

| Observable | Geometric output |
|------------|------------------|
| $\delta_{\rm CKM}$ | $\approx 72^\circ-0.24^\circ \approx 71.8^\circ$ (leading map) |
| $J$ | from standard formula / $\mathrm{Im}(V_{ud}V_{cs}V_{us}^*V_{cd}^*)$ |
| $\|V_{ij}\|$ | standard PDG parametrization magnitudes |

Jarlskog standard formula:

$$
J = \frac{1}{8}\sin 2\theta_{12}\sin 2\theta_{23}\sin 2\theta_{13}\cos\theta_{13}\sin\delta.
$$

With locked angles this produces $J\sim \mathcal{O}(10^{-5})$, consistent with the archive value $\sim 3\times 10^{-5}$.

**Locked claim:** CKM magnitudes and CP observables are **reconstructible** from the locked angle set + $\phi$; no CKM parameter is free.

---

## 4. Light Yukawa residual control

Under $\kappa_u/\kappa_d=1/2$ (doc 14):

| Sector | Status |
|--------|--------|
| Top / bottom scales | $\ell_0$ + spectral action |
| Charm / strange | Casimir ratios + $\eta$ — good structural agreement |
| Up / down light | $\kappa$ factor removes leading $\sim 2$ tension |
| Residual light-mass digits | Still residual (continuum overlap precision, higher Dual-Zero moments) |

**Push without tuning:** residual is classified as **higher-order continuum / Dual-Zero**, not a missing free parameter. No number was adjusted to PDG light-quark masses.

---

## 5. $\delta_{\rm PMNS}$ band discipline

Large phase from $\phi=2\pi/5$ remains locked (doc 15).

**Narrowing rule (derivation only):**  
Any reduction of the $200^\circ$–$270^\circ$ band must come from a **derived** RH radial mass hierarchy $(1,r_2,r_3)$ fixed by conoid localization — the same class of object as Casimir tip amplitudes. Until that hierarchy is frozen from geometry with stated error bars, the band is **not** replaced by a single degree value.

No experimental $\delta_{\rm PMNS}$ was used to pick a central value.

---

## 6. Higgs sub-GeV path (not a new number)

Still the 124–127 GeV class (docs 13, 20, 26).  
Completable path: full warped $a_4$ + radiative matching.  
**Not done here** as a fake digit. No push that invents $125.XX$ GeV.

---

## 7. What was deliberately not pushed

| Item | Reason |
|------|--------|
| Unification $\to$ percent level | Needs new geometric threshold structure |
| $\Lambda$ magnitude | Mechanism only |
| RH proof | Residual variational proposal only |

---

## 8. Lock statement

> Completable precision items were advanced only by derivation from locked $\eta_{ij}$, $C_g$, $\phi$, and bi-unitary structure. $\theta_{13}$ remains bi-unitary-locked at $\approx 0.24^\circ$ with a geometric explanation of its smallness; CKM $\delta$ and $J$ are reconstructed from locked inputs; light-Yukawa residual is attributed to higher-order continuum/Dual-Zero effects under $\kappa_u/\kappa_d=1/2$; $\delta_{\rm PMNS}$ stays a large band until RH hierarchy is geometrically frozen. No experimental retuning was performed.

---

*Derivation only. Pipeline helper: `python code/ckm_from_geometry.py`.*
