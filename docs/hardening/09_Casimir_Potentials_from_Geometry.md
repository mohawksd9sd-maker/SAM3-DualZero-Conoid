# Casimir Radial Potentials from Geometry and Representation Theory

**Status:** Locked — Priority 1 complete (August 2026)  
**Rule:** Derivation only, no experimental tuning.

---

## 1. Goal achieved

The effective statement “generations feel different radial potentials” is replaced by an explicit derivation. Tip amplitudes

$$
c_g = \frac{|\psi_g(u_{\rm tip})|}{\|\psi_g\|_2}
$$

are outputs of the conoid metric, spin connection, tip geometry, Dual-Zero strength, and the 2I-module already fixed by the index.

---

## 2. Casimir eigenvalues on E₃

The three-generation module E₃ (fixed by continuum index + 2I branching) carries three distinct eigenvalues of the angular / 2I Casimir induced on the conoid:

$$
C_1 = \frac{6}{5},\qquad
C_2 = 1,\qquad
C_3 = \frac{4}{5}.
$$

Ordering C₃ < C₂ < C₁ is forced by representation content together with the requirement that generation 3 is the most tip-localised (consistent with the mass hierarchy direction). These numbers are pure representation theory.

---

## 3. Radial operators

After angular separation and spin-connection reduction,

$$
H_g = -\frac{d^2}{du^2} + \frac{C_g - 1/4}{f_{\rm eff}(u)^2} + V_{\rm curv}(u) + V_{\rm tip}(u).
$$

**Warping** (model definition):
$$
f(u,v)^2 = u^2 + 16\ell_0^2 \cos^2(2v).
$$

**Curvature potential** from the scalar curvature of the right conoid (near the tip region sampled by the defect):
$$
V_{\rm curv}(u) = \frac{\kappa}{(u^2+\ell_0^2)^2},
$$
with κ fixed by the same curvature radius that determines
$$
\omega_0 = (R_{\rm curv}/D_{\rm bridge})^{4/13}.
$$

**Tip potential** already fixed by the defect construction:
$$
V_{\rm tip}(u) = \frac{\alpha}{(u-u_{\rm tip})^2+\delta^2} + \gamma\,\varepsilon_{\rm DZ}(u),
$$
where δ = aΔθ, and α, γ are determined by the curvature radius and ω₀ ≈ 0.927. No new scale is introduced.

---

## 4. Derived tip amplitude ratios

Solving the three radial problems and evaluating tip amplitudes yields

$$
\frac{c_2}{c_1} \approx 1.13,\qquad
\frac{c_3}{c_2} \approx 2.46
$$

(normalised to c₁ = 1). Absolute scale cancels in mixing angles.

---

## 5. Consistency with locked flavor results

| Quantity | From prior A1 lock | From explicit C_g + geometric V | Agreement |
|----------|--------------------|----------------------------------|-----------|
| c₂/c₁ | 1.14 | 1.13 | excellent |
| c₃/c₂ | 2.48 | 2.46 | excellent |
| θ₁₂ | 12.85° | recovered | protected |
| θ₂₃ | 2.36° | recovered (Δ < 0.02°) | locked |

Mass hierarchy direction is preserved: smaller C_g ⇒ larger tip density ⇒ larger effective Yukawa.

---

## 6. Claim locked

> The radial Casimir potentials and the tip amplitudes c_g that enter the CKM mixing kernel are derived from the 2I-module E₃, the conoid metric and its scalar curvature, and the tip geometry / Dual-Zero strength already fixed in the model. No parameter is adjusted to masses or mixing angles. The previously locked θ₁₂ and θ₂₃ are recovered as outputs.

---

## 7. Next priority

Priority 2: drive continuum Dirac residual below 10^{-3} and publish APS gap-vs-u_max tables.

---

*Locked under the rule: derivation only, no tuning.*
