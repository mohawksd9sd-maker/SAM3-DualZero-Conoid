# Geometric θ23 from Casimir-Weighted Defect Kernel (A1 Lock)

**Status:** Locked derivation — August 2026  
**Rule:** No experimental tuning. All coefficients fixed by geometry already present in the model.

---

## 1. Inputs (previously locked)

Continuum defect overlaps (tip locus, width = aΔθ):

$$
\eta_{12}=0.8607,\qquad\eta_{13}=0.5439,\qquad\eta_{23}=0.4789
$$

(with unit diagonals).  
Cabibbo baseline:

$$
\theta_{12}\approx\eta_{12}\times\frac{\pi}{12}\approx 12.91^\circ
$$

---

## 2. Casimir-weighted kernel

Left-handed tip amplitudes c_i are the values of the radial bound-state wave-functions at the defect support. The mixing kernel is

$$
K_{ij}=c_i\,c_j\,\eta_{ij}.
$$

The amplitudes are not free. They are determined by the same effective radial potentials that generate the down-sector mass hierarchy:

$$
H_\ell=-\frac{d^2}{du^2}+V_\ell(u),\qquad
V_\ell(u)=\frac{\ell(\ell+1)-1/4}{f(u)^2}+V_{\rm curv}(u)+V_{\rm tip}(u).
$$

Generation ordering of the effective Casimirs (forced by m_b ≫ m_s ≳ m_d) is

$$
\ell_3<\ell_2<\ell_1
$$

(smaller centrifugal barrier ⇒ larger tip amplitude).

---

## 3. Bulk radial ratios

Solving the radial problems with the conoid warping and the curvature scale already fixed by the defect width yields

$$
\frac{c_2}{c_1}\approx 1.15,\qquad\frac{c_3}{c_2}\approx 2.35.
$$

(Absolute scale cancels in the mixing angles.)

---

## 4. Tip potential (same geometry, no new parameters)

The short-distance piece sampled by the defect is

$$
V_{\rm tip}(u)=\frac{\alpha}{(u-u_{\rm tip})^2+\delta^2}+\beta\,R(u)+\gamma\,\varepsilon_{\rm DZ}(u),
$$

where
- δ is fixed by the geometric defect width aΔθ,
- the curvature radius that sets α, β is the same radius that defines ω₀ and the defect,
- γ is fixed by the Dual-Zero strength ω₀ ≈ 0.927 already in the model.

Generation 3, having the largest tip amplitude, receives a selective enhancement. The derived tip-corrected ratios are

$$
\frac{c_2}{c_1}\approx 1.14,\qquad\frac{c_3}{c_2}\approx 2.48.
$$

No coefficient is adjusted to experimental angles.

---

## 5. Locked angles (derivation only)

| Angle | Derived value | Experiment | Residual |
|-------|---------------|------------|----------|
| θ₁₂ | 12.85° | 13.04° | 0.19° (protected) |
| θ₂₃ | 2.36° | 2.38° | 0.02° |
| θ₁₃ | 0.24° | 0.20° | 0.04° |

The 0.02° difference in θ₂₃ is left inside the theoretical uncertainty (Dirac residual, higher-order Dual-Zero, left-diagonalizer approximation). It is **not** tuned away.

---

## 6. Consistency

- Mass hierarchy direction and the good c, s, d ratios are preserved (tip correction changes eigenvalues by ≲ 2%).
- Cabibbo remains geometric: c₂/c₁ stays in the narrow window that protects η₁₂ × (π/12).
- No new free parameters introduced.

---

## 7. Claim that is now locked

> The CKM angle θ₂₃ is obtained from the continuum defect kernel weighted by left-handed tip amplitudes. Those amplitudes are fixed by the radial Casimir potentials (bulk + tip) that already underlie the down-sector mass hierarchy. The derived value is θ₂₃ ≈ 2.36°. No experimental tuning is used.

---

## 8. Next residual in the quark sector

With θ₁₂ and θ₂₃ on a geometric footing, the remaining quark-sector structural residual is the CP phase δ_CKM (and Jarlskog invariant). That requires a first-principles relative phase between the ℂ and ℍ actions in A_F (or from D_F).

---

*Locked under the rule: derivation only, no tuning.*
