# Exhaustive Precision Continuation

**Status:** Recorded August 2026  
**Rule:** Derivation only; no experimental retuning; no overwrite of locked continuum η or θ13 archive value.

---

## 1. Singular-vector θ13

### Construction

1. θ12 = η12 × π/12 (Cabibbo)
2. θ23 = 2.36° (Casimir tip geometry)
3. yd ∝ A = (1, 1.13, 2.7798); yu with κu/κd = 1/2 on light entry
4. Yd = R12(θ12) R23(θ23) diag(yd); Yu = diag(yu)
5. VCKM = Uu† Ud (light-first SVD)

### SVD output

| Angle | SVD |
|-------|-----|
| θ12 | 12.90° |
| θ23 | 2.30° |
| θ13 | 0.527° (= θ12 θ23 Givens product) |

### Corrected reduced formula

$$
\theta_{13}^{\mathrm{phys}} = \theta_{12}\,\theta_{23}\,\frac{y_1}{y_3}
= \theta_{12}\,\theta_{23}\,\frac{1}{c_3/c_1}
\approx 0.191^\circ
$$

| Path | θ13 | J | |Vub| |
|------|-----|---|------|
| Phys (reduced) | 0.191° | 2.84×10^{-5} | 0.0033 |
| Archive bi-unitary | 0.24° | 3.56×10^{-5} | 0.0042 |
| Experiment | 0.20° | ∼3×10^{-5} | ∼0.0037 |

**Policy:** Archive θ13 = 0.24° remains the bi-unitary reference. 0.191° is the corrected reduced companion formula. Do not use the discarded 1.84° blend.

---

## 2. Derived 2I η law

$$
k_g = A_g^{\varphi^2},\quad \varphi^2 \approx 2.618,\quad A = (1,\,1.13,\,2.7798)
$$

$$
\eta_{ij} = \frac{2\sqrt{k_i k_j}}{k_i+k_j}
$$

Angular structure: shared tip vector in the 3 of A5 (all generations).

| | η12 | η13 | η23 | RMS |
|--|-----|-----|-----|-----|
| Derived | 0.987 | 0.491 | 0.562 | 0.093 |
| Locked continuum defect | 0.861 | 0.544 | 0.479 | — |

**Policy:** Locked continuum-defect η (docs 01, 16) remain CKM inputs. Derived η is the pure 2I prediction. Full match is not claimed; residual is structural (c2/c1 ≈ 1).

---

## 3. Frozen RH hierarchy and δPMNS

$$
(r_1,r_2,r_3) = (1,\,0.884956,\,0.359738)
$$

Origin: Mg ∝ 1/Ag tip amplitudes.

**δPMNS band:** [193.6°, 255.3°] (center ∼224.5°). Previous [200°, 270°] narrowed by geometry only.

---

## 4. Higgs class band

$$
m_H \in [123.3,\,126.7]\ \mathrm{GeV}
$$

Class claim only; ω0 = 0.927 fixed; no digit claim.

---

## 5. Forbidden

- Replace locked θ13 or locked continuum η
- Move ω0
- Claim percent-level unification or RH proof

---

*See also doc 31. Code: theta13_biunitary_derivation.py, eta_2I_derived.py, rh_hierarchy_freeze.py.*
