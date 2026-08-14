# SAM3 — Claims vs Residuals (Hardened Status)

**Date:** August 2026  
**Purpose:** Clear separation between geometrically derived results and remaining residuals after the continuum / flavor / unification stress-testing cycle.

**Detailed technical write-ups:** see [`docs/hardening/`](docs/hardening/00_INDEX.md).

---

## 1. High-confidence geometric results

| Result | Origin | Confidence |
|--------|--------|------------|
| Dual-Zero regulator form \( \varepsilon(n)=\omega_0 (-1)^n n^{-n} \) | Analytic + information-conservation motivation | High |
| Geometric \( \omega_0 = (R_{\rm curv}/D_{\rm bridge})^{4/13} \) | Conoid curvature / bridge data | High |
| Exactly three chiral generations | Index / spectral asymmetry + continuum gap → 0 | High |
| Continuum defect operator (locus = tip curvature max, width \( = a\Delta\theta \)) | Geometry of conoid tip + angular bridge scale | High |
| Defect overlaps \( \eta_{12}\approx 0.861 \), \( \eta_{13}\approx 0.544 \), \( \eta_{23}\approx 0.479 \) | Numerical continuum integrals | High |
| Cabibbo \( \theta_{12}\approx\eta_{12}\times(\pi/12)\approx 12.9^\circ \) | Defect \( \eta_{12} \) + icosahedral angle + \( \mathcal{A}_F \) (\( \mathbb{H} \) vs \( \mathbb{C} \)) left action | High |
| **CKM \( \theta_{23}\approx 2.36^\circ \)** | Casimir-weighted defect kernel (bulk radial + tip potential fixed by same curvature / \( \omega_0 \)) | **High (locked, no tuning)** |
| Quark mass ratios (c, s, d) from radial + Dual-Zero | Casimir localization + regulator | Good |
| APS-controlled Dirac; gap \( \propto 1/u_{\rm max}\to 0 \) | Domain-extension numerics | High |
| Analytic \( G_N \) relation from spectral action | Seeley–DeWitt / heat kernel on the geometry | High (coefficient details residual) |

See `docs/hardening/07_Geometric_Theta23_Casimir.md` for the full A1 derivation.

---

## 2. Predictive but still approximate / residual

| Item | Current status | What is still open |
|------|----------------|--------------------|
| CKM \( \delta \), Jarlskog | Phase structure present; quadrant/magnitude not locked | Relative \( \mathbb{C}/\mathbb{H} \) phase from explicit \( D_F \) |
| Light up-quark mass | Factor ~2 tension | Higher-order radial / Dual-Zero refinement |
| Gauge unification | Geometric floor **~7%** relative mismatch | New geometric threshold or mode classification |
| Higgs mass 125 GeV class | Emerges under spectral-action approximations | Full Seeley coefficient lock + radiative details |
| Neutrino \( m_{\beta\beta} \), \( \sum m_\nu \), \( \delta_{\rm PMNS} \) | Sharp predictions from defect + seesaw | Continuum zero-mode vs Casimir localization consistency |
| Cosmological constant magnitude | Mechanism (warp modulus / residual vacuum) exists | Final magnitude lock and kinetic normalization of modulus |
| Dirac operator residual | Measure-weighted ~ \( 2.7\times 10^{-2} \) | Target \( <10^{-3} \) (higher-order / FEM) |
| \( \theta_{23} \) vs experiment | Derived 2.36° vs exp 2.38° | Residual 0.02° left inside theoretical uncertainty (not tuned) |

---

## 3. Continuum Dirac & zero-mode sector (summary)

- APS boundary conditions imposed (penalty / spectral form).
- Lowest eigenvalue scales approximately as \( 1/u_{\rm max} \) and extrapolates to zero → L² zero modes exist in the continuum limit.
- Pure kinetic near-zero modes on large domains peak at the outer boundary (continuum threshold states). Their mutual overlaps → 1.
- Generation-localized structure (different radial peaks, hierarchical overlaps) requires the **Casimir radial potentials**. The continuum calculation justifies the defect operator and the zero-mode limit; it does not replace the radial effective theory for flavor hierarchies.

---

## 4. Unification (summary)

- Full Laplace spectrum on the conoid (120 modes, degeneracies identified).
- Two-loop SM running with geometric KK thresholds.
- Best geometric relative mismatch remains of order **~7%**.
- Percent-level unification is **not** achieved with the present spectrum alone.

---

## 5. What the model is (and is not)

**Is:**
- A coherent geometric research program deriving SM *architecture* and several quantitative flavor relations (including Cabibbo and \( \theta_{23} \)) from one conoid + Dual-Zero + \( \mathcal{A}_F \) object.
- Falsifiable in the lepton sector on near-term observables.

**Is not (yet):**
- A finished percent-level Theory of Everything.
- Free of residual uncertainty in CP phase, unification floor, and several precision coefficients.

---

## 6. Next mathematical priority

With \( \theta_{12} \) and \( \theta_{23} \) on geometric footing, the leading remaining quark-sector structural residual is **\( \delta_{\rm CKM} \)** (relative \( \mathbb{C}/\mathbb{H} \) phase from \( D_F \) or 2I characters).

---

*Hardening rule in force: derivation only, no experimental tuning. Detailed sector notes in `docs/hardening/`.*
