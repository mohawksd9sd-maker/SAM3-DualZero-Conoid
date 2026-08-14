# Geometric Relative Phase φ = 2π/5 and CKM CP Structure

**Status:** Phase locked from first principles — August 2026  
**Rule:** Derivation only, no experimental tuning.

---

## 1. Locked geometric result

The relative phase between the ℂ and ℍ actions inside

$$
\mathcal{A}_F = \mathbb{C} \oplus \mathbb{H} \oplus M_3(\mathbb{C})
$$

is uniquely fixed to

$$
\phi = +\frac{2\pi}{5}.
$$

### Inputs used (all already present in the model)

1. **Three-generation module E₃** fixed by the continuum index + 2I branching.
2. **Quaternionic relation** I² = −1 that defines the complex structure inside ℍ.
3. **Tip orientation** of the conoid defect (eliminates φ = 0 and fixes the overall sign).

### Elimination of other discrete candidates

| Candidate | Eliminated by |
|-----------|----------------|
| 0 | Tip orientation |
| ±π/5 | Fails to reproduce I² = −1 on the down-type block |
| ±π/2 | Does not preserve the cyclic (order-5) grading of E₃ |
| ±2π/5 | Sign fixed to + by tip orientation |

No continuous parameter enters.

---

## 2. Present consequence for CKM CP violation

Inserted into the locked real angles

$$
\theta_{12}\approx 12.85^\circ,\quad
\theta_{23}\approx 2.36^\circ,\quad
\theta_{13}\approx 0.24^\circ
$$

the geometric phase yields

$$
\delta_{\rm CKM} \sim 70^\circ,\qquad
J \sim 3\times 10^{-5}.
$$

This is **consistent** with experiment at the present precision of the angles. It is not claimed as a sub-degree derivation of δ_CKM; the dominant uncertainties remain the small residual in θ₁₃ and the conventional alignment between the finite-geometry phase and the PDG phase convention.

---

## 3. What is fully first-principles vs what remains open

| Item | Status |
|------|--------|
| φ = +2π/5 | **Locked** — pure representation theory + tip orientation |
| Real CKM angles θ₁₂, θ₂₃ | **Locked** — defect + Casimir (docs 01, 07) |
| Full map φ → PDG δ_CKM at high precision | Open — needs explicit D_F matrix elements and convention-independent extraction |
| Jarlskog to percent-level | Open — limited by θ₁₃ residual and continuum Dirac residual |

---

## 4. Path to a complete first-principles δ_CKM

To convert the locked φ into a theorem-level δ_CKM the following remain:

1. Write the explicit finite Dirac operator D_F in a CCM-compatible basis with the three-generation 2I module.
2. Evaluate the invariant relative argument of the up and down Yukawa blocks without choosing a preferred phase convention by hand.
3. Propagate that argument through the same bi-unitary diagonalization that produces the locked real angles, obtaining δ_CKM as an output rather than a consistency check.
4. Recompute J from the full complex CKM matrix and confirm stability under the residual uncertainties of θ₁₃ and the Dirac operator.

Until those steps are closed, the honest claim is the one locked above: the geometric phase is φ = 2π/5; the resulting CP violation is consistent with observation.

---

*Locked under the rule: derivation only, no tuning. Next exploration targets the explicit D_F map from φ to δ_CKM.*
