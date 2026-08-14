# SAM3 — Claims vs Residuals (Hardened Status)

**Date:** August 2026  
**Purpose:** Clear separation between geometrically derived results and remaining residuals after the continuum / flavor / unification stress-testing cycle.

**Detailed technical write-ups:** see [`docs/hardening/`](docs/hardening/00_INDEX.md) (CKM/quark, continuum Dirac/APS, unification KK floor, neutrino/PMNS, localization/Casimir, cosmology/Higgs notes).

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
| Quark mass ratios (c, s, d) from radial + Dual-Zero | Casimir localization + regulator | Good |
| APS-controlled Dirac; gap \( \propto 1/u_{\rm max}\to 0 \) | Domain-extension numerics | High |
| Analytic \( G_N \) relation from spectral action | Seeley–DeWitt / heat kernel on the geometry | High (coefficient details residual) |

---

## 2. Predictive but still approximate / residual

| Item | Current status | What is still open |
|------|----------------|--------------------|
| CKM \( \theta_{23} \) | Undershoots experiment (~1.2° vs ~2.4°) | Sharper Casimir / 2–3 block geometry |
| CKM \( \delta \), Jarlskog | Phase structure present; quadrant/magnitude not locked | Relative \( \mathbb{C}/\mathbb{H} \) phase from explicit \( D_F \) |
| Light up-quark mass | Factor ~2 tension | Higher-order radial / Dual-Zero refinement |
| Gauge unification | Geometric floor **~7%** relative mismatch | Longer KK tower, scheme matching, or new geometric threshold |
| Higgs mass 125 GeV class | Emerges under spectral-action approximations | Full Seeley coefficient lock + radiative details |
| Neutrino \( m_{\beta\beta} \), \( \sum m_\nu \), \( \delta_{\rm PMNS} \) | Sharp predictions from defect + seesaw | Continuum zero-mode vs Casimir localization consistency |
| Cosmological constant magnitude | Mechanism (warp modulus / residual vacuum) exists | Final magnitude lock and kinetic normalization of modulus |
| Dirac operator residual | Measure-weighted ~ \( 2.7\times 10^{-2} \) | Target \( <10^{-3} \) (higher-order / FEM) |

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
- The KK contribution \( \Delta\alpha^{-1}\sim O(10) \) is real and of the correct size; the residual floor is a genuine geometric limitation under current assumptions.

---

## 5. What the model is (and is not)

**Is:**
- A coherent geometric research program deriving SM *architecture* (group, 3 families, chiral fermions, hierarchical Yukawas, seesaw pattern) and several quantitative relations from one conoid + Dual-Zero + \( \mathcal{A}_F \) object.
- Falsifiable in the lepton sector on near-term observables (\( m_{\beta\beta} \), \( \delta_{\rm PMNS} \), \( \sum m_\nu \)).

**Is not (yet):**
- A finished, percent-level Theory of Everything with all SM numbers derived to experimental precision.
- Free of residual O(1) coefficients in every mixing angle and threshold.

---

## 6. Recommended next public steps

1. Keep this status file and `docs/hardening/` updated with every major numerical or geometric lock.
2. Formalize the continuum defect + Cabibbo derivation (see `papers/SAM3_Addendum_Cabibbo_Defect_Operator.tex`).
3. Expand the master verification pipeline so it regenerates the numbers in this document from live kernels within stated tolerances.
4. Treat the ~7% unification floor as a prediction of the present geometry until a new geometric threshold is derived.

---

*This document records the state after the August 2026 hardening cycle (continuum defect, APS/gap, Cabibbo geometric origin, KK unification floor, Claims vs Residuals discipline). Detailed sector notes live in `docs/hardening/`.*
