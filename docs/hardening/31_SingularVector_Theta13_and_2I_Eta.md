# Singular-Vector θ13 and Derived 2I η

**Status:** Locked as derivation record — August 2026  
**Rule:** Derivation only; archive locks not overwritten.

---

## A. Full singular-vector derivation of CKM angles

### Steps

1. **Cabibbo:** θ12 = η12 × π/12 ≈ 12.91° with η12 = 0.8607.
2. **Casimir θ23:** 2.36° (tip geometry).
3. **Tip amplitudes:** A = (1, c2/c1, c3/c1) = (1, 1.13, 2.7798).
4. **Eigenvalues:** yd = A/A3; yu with κu/κd = 1/2 on light entry, renormalized.
5. **Yukawas:**
   - Yd = R12(θ12) R23(θ23) diag(yd)
   - Yu = diag(yu) (up left angles suppressed: ℂ vs ℍ)
6. **SVD:** Y = U S V†; light-first column order.
7. **VCKM = Uu† Ud.**
8. **Extract PDG angles from |V|.**

### Raw SVD

θ12 ≈ 12.90°, θ23 ≈ 2.30°, θ13 ≈ 0.527° ≈ θ12 θ23.

### Hierarchy-weighted physical θ13

$$
\theta_{13}^{\mathrm{phys}} = \theta_{12}\theta_{23}\frac{y_1}{y_3} \approx 0.191^\circ
$$

With δCKM ≈ φ − θ13 (φ = 2π/5): J ∼ 2.8×10^{-5}, |Vub| ∼ 0.0033.

Archive bi-unitary θ13 = 0.24° remains the locked reference for frozen archive CKM reconstruction.

---

## B. Derived 2I radial–angular η

### Group data

- 12 icosahedron vertices
- 60 distinct A5 permutations (full group)
- 3-irrep: Y1m on vertices
- 5-irrep: Y2m on vertices

### Laws

- Radial: kg = Ag^{φ²}, φ² = φ+1 ≈ 2.618 (discrete icosahedral scale; best among {1, φ, 2, φ², 3})
- Angular: shared tip vector in the 3 (all generations)
- Overlap: ηij = 2√(ki kj)/(ki+kj)

### Comparison

| Quantity | Derived | Locked continuum defect |
|----------|---------|-------------------------|
| η12 | 0.987 | 0.861 |
| η13 | 0.491 | 0.544 |
| η23 | 0.562 | 0.479 |
| RMS residual | 0.093 | — |

3′ admixture weighted by hierarchy does not close the η12 residual without spoiling η13.

### Policy

Locked continuum-defect η remain inputs to CKM. Derived η is the first-principles 2I prediction recorded for comparison and future continuum-defect reconciliation.

---

*Code: `code/theta13_biunitary_derivation.py`, `code/eta_2I_derived.py`.*
