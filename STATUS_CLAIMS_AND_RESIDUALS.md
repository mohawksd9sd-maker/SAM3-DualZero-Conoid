# SAM3 — Claims vs Residuals (Hardened Status)

**Date:** August 2026 (updated after Priorities 1–6 + secondary 1–3)  
**Purpose:** Clear separation between geometrically derived results and remaining residuals.  
**Rule:** Derivation only, no experimental tuning, no overclaim.

**Authoritative detail:** [`docs/hardening/`](docs/hardening/00_INDEX.md)  
**Frozen numbers:** [`docs/hardening/16_Frozen_Numerical_Archive.md`](docs/hardening/16_Frozen_Numerical_Archive.md)

---

## 1. High-confidence geometric results (locked)

| Result | Origin | Confidence |
|--------|--------|------------|
| Dual-Zero regulator \( \varepsilon(n)=\omega_0 (-1)^n n^{-n} \) | Analytic + information conservation | High |
| Geometric \( \omega_0 = (R_{\rm curv}/D_{\rm bridge})^{4/13}\approx 0.927 \) | Conoid curvature / bridge data | High |
| Exactly three chiral generations | Index + continuum gap \( \to 0 \) under APS | High |
| Continuum defect (locus = tip max, width \( = a\Delta\theta \)) | Tip geometry + bridge angle | High |
| Defect overlaps \( \eta_{12}\approx 0.861 \), \( \eta_{13}\approx 0.544 \), \( \eta_{23}\approx 0.479 \) | Continuum integrals | High |
| Cabibbo \( \theta_{12}\approx 12.85^\circ \) | \( \eta_{12}\times\pi/12 \) + \( \mathcal{A}_F \) | High |
| CKM \( \theta_{23}\approx 2.36^\circ \) | Casimir-weighted defect (doc 07, 09) | **Locked** |
| CP phase \( \phi=+2\pi/5 \) | \( E_3 \) + \( I^2=-1 \) + tip orientation (doc 08) | **Locked** |
| \( \delta_{\rm CKM}\sim 70^\circ \), \( J\sim 3\times 10^{-5} \) | \( \phi \) + locked real angles (doc 11) | **Locked** (consistency precision) |
| Casimir eigenvalues \( C_g=(6/5,1,4/5) \) and tip amplitudes | 2I-module + conoid potentials (doc 09) | **Locked** |
| Continuum Dirac residual \( <10^{-3} \); gap \( \propto 1/u_{\rm max}\to 0 \) | 4th-order FD + APS (doc 10) | **Locked** |
| Explicit \( D_F \) on \( E_3 \); complex CKM as geometric output | \( \mathcal{A}_F \) + locked magnitudes/phase (doc 11) | **Locked** |
| Light up mass factor resolved | \( \kappa_u/\kappa_d=1/2 \) intertwiner norm (doc 14) | **Locked** |
| \( G_N=64\pi\ell_0^2/45 \) | Seeley–DeWitt \( a_2 \) (doc 13) | **Locked** |
| Higgs mass in 125 GeV class (\( \approx 124\)–\(127\) GeV band) | Geometric \( a_4 \) (doc 13) | **Locked** (class, not digit) |
| Large \( \delta_{\rm PMNS} \) (\( \sim 200^\circ\)–\(270^\circ \) band) | Same module-wide \( \phi \) (doc 15) | **Locked** (band) |

---

## 2. Residual / approximate (not overclaimed)

| Item | Current status | What remains open |
|------|----------------|-------------------|
| Sub-degree \( \delta_{\rm CKM} \) / percent-level \( J \) | Consistent at present angle precision | Limited by residual \( \theta_{13} \) and convention alignment |
| Sub-GeV Higgs mass | Class prediction with \( \sim 2 \) GeV band | Full warped \( a_4 \) + radiative matching |
| Gauge unification | Geometric floor **~7%** | New geometric threshold required for improvement; **percent-level not claimed** (doc 12) |
| Cosmological constant magnitude | Mechanism (warp / residual vacuum) present | Final magnitude lock + modulus kinetic normalization |
| Sharp degree-level \( \delta_{\rm PMNS} \) | Large phase locked; precise value band-only | RH hierarchy detail |
| Production 2D APS eigensolver in `code/` | Continuum claims locked; kernels still prototype | Engineering pipeline archive |
| Lorentzian spectral triple (full causality theorem) | Standard Wick + KO recovery | Full Lorentzian reconstruction not claimed complete (doc 17) |
| Riemann Hypothesis | Variational / information-current proposal | **Not a proof** (doc 17) |

---

## 3. Continuum Dirac & zero-mode sector

- APS boundary conditions; \( |\lambda|_{\min}\propto 1/u_{\rm max}\to 0 \) ⇒ continuum \( L^2 \) zero modes.
- Continuum residual of 4th-order FD below \( 10^{-3} \) at moderate resolution (manufactured residual tests).
- Pure kinetic near-zero modes on large domains are threshold-like; generation localization uses derived Casimir radial potentials (doc 09).

---

## 4. Unification

- KK thresholds of order \( \Delta\alpha^{-1}\sim O(10) \).
- Residual relative mismatch after two-loop running ≈ **7%**.
- **Percent-level unification is not claimed.**

---

## 5. What the model is (and is not)

**Is:**
- A coherent geometric research program deriving SM *architecture* and quantitative flavor relations (Cabibbo, \( \theta_{23} \), CP phase structure, light-up resolution) from one conoid + Dual-Zero + \( \mathcal{A}_F \) object.
- Falsifiable on lepton-sector observables (\( m_{\beta\beta} \), \( \delta_{\rm PMNS} \), \( \sum m_\nu \)).

**Is not (yet):**
- A finished percent-level Theory of Everything.
- A proof of the Riemann Hypothesis.
- Free of all residual uncertainty (unification floor, CC magnitude, sub-GeV Higgs, production code archive).

---

## 6. Supersession note

Older statements in `papers/` (Flagship, v4.22, Papers 08/19/22, etc.) that claim exact \( m_H=125.1 \) GeV, percent-level unification, RH-as-proof, or a fully locked cosmological constant magnitude are **superseded** by this status file and by `docs/hardening/`.

---

## 7. Completion of planned hardening path

| Block | Status |
|-------|--------|
| Primary Priorities 1–6 | Complete and locked |
| Secondary 1 (lepton phase) | Complete and locked |
| Secondary 2 (frozen archive) | Complete and locked |
| Secondary 3 (Lorentzian + RH discipline) | Complete and locked |

---

*Hardening rule in force: derivation only, no experimental tuning, no overclaim.*
