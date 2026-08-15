# 33 — Unification: VL_Q Precision Path

**Status:** Precision-class research result (derivation-only)  
**Date:** August 2026  
**Rule:** no continuous tuning, no PDG fits, no ad hoc M_X = μ_meet

---

## 1. Summary

Approximate gauge coupling unification with forced intermediate vector-like quark doublets:

$$
\begin{aligned}
M_* &= \sqrt{\Lambda_0 m_H}, \\
M_2 &= 12 M_*, \\
&\text{VL }Q\text{ at }M_*\text{ and }M_2, \\
M_X &= \Lambda_0 \quad \text{(if heavy completion vectors exist)}.
\end{aligned}
$$

| Quantity | Result |
|----------|--------|
| One-loop residual | ≈ 1.9% |
| Two-loop residual | ≈ 2.6% |
| Meeting scale μ_meet | ∼ 1.4×10¹⁵ GeV (diagnostic) |
| Proton lifetime (M_X=Λ₀) | ∼ 10⁴⁸ yr ≫ Super-K |
| Collider / EW | Safe (M_* ∼ 5.7×10¹⁰ GeV) |

This is **precision-class** (MSSM-order residual), not a fitted GUT, and not a claim of exact single-scale unification.

---

## 2. Forced masses (alphabet only)

| Symbol | Origin |
|--------|--------|
| Λ₀ = 1/ℓ₀ | Seeley–DeWitt a₂ + G_N |
| m_H class | Seeley–DeWitt a₄ |
| M_* = √(Λ₀ m_H) | Same alphabet (geometric mean UV–IR) |
| 12 M_* | Bridge number N=12 |
| M_X = Λ₀ | Only UV geometric mass available for completion vectors |

**Rejected as non-derived:** M_X = μ_meet (standard GUT lore; μ_meet is RG diagnostic, not a spectral eigenvalue or VEV in present AF).

---

## 3. Content: VL quark doublets and R_Q

### 3.1 AF map (explicit one-family matrices)

$$\mathcal{A}_F = \mathbb{C}\oplus\mathbb{H}\oplus M_3(\mathbb{C})$$

C5 ⊂ 2I action:

$$
\begin{aligned}
\rho_{3'}(g_5) &= \mathrm{diag}(e^{2\pi i/5}, e^{-2\pi i/5}, 1), \\
\rho_2(g_5) &= \mathrm{diag}(e^{i\pi/5}, e^{-i\pi/5}), \\
U(g)|L\rangle &= \rho_2(g)|L\rangle, \\
U(g)|Q\rangle &= \bigl(\rho_2(g)\otimes\rho_{3'}(g)\bigr)|Q\rangle, \\
U(g)|u_R\rangle &= \rho_{3'}(g)|u_R\rangle, \quad
U(g)|d_R\rangle = \rho_{3'}(g)|d_R\rangle, \\
U(g)|e_R\rangle &= |e_R\rangle, \quad U(g)|\nu_R\rangle = |\nu_R\rangle.
\end{aligned}
$$

Characters: χ_{3'} = φ, χ_3 = 1/φ, χ₂ = 2 cos(π/5) = φ.  
Enrichment: |χ_Q / χ_L| = φ when color carries 3′ (forced for quark enrichment).

### 3.2 2I table

Full binary icosahedral group generated in SU(2): **120 elements**, conjugacy traces matching 2I (including ±φ, ±1/φ classes). Weak ρ₂ is J-compatible (pseudoreal via iσ_y). Color 3′ is complex; paired by standard CCM J_F.

### 3.3 Selection rule R_Q

First intermediate C5-nontrivial tower is 3′-enriched (M₃-charged): VL quark doublets, not full VL generations (full VL gen worsens residual).

---

## 4. Residual results

| Setup | Residual |
|-------|----------|
| SM one-loop | ∼ 8.8% |
| SM two-loop | ∼ 7.8% |
| VL_Q one-loop at M_*, 12 M_* | **∼ 1.9%** |
| VL_Q two-loop | **∼ 2.6%** |
| Full VL generation at same scales | ∼ 19% (fails) |

Two-loop uses SM B-matrix with one-loop VL_Q thresholds (standard approximation).

---

## 5. Proton decay

| Scenario | Verdict |
|----------|---------|
| VL_Q alone | No B-violation → no dim-6 qqql from this sector |
| M_X = μ_meet, O(1) amplitude | **Not derived**; would fail Super-K |
| **M_X = Λ₀ (forced)** | τ_p ∼ 10⁴⁸ yr → **safe** |

**Why M_X ≠ μ_meet is forced:**  
μ_meet is an RG diagnostic. Present AF has no unified generators and no GUT Higgs VEV at 10¹⁵ GeV. The only UV mass fixed by a₂ + G_N is Λ₀. Identifying M_X with μ_meet is external GUT lore, not a SAM3 eigenvalue.

---

## 6. Phenomenology safety

| Constraint | Status |
|------------|--------|
| LHC VLQ searches | Safe (M_* ≫ TeV) |
| EW precision (v/M_*)² | ∼ 10⁻¹⁷ |
| η / CKM / Dual-Zero locks | Untouched |

---

## 7. What is claimed vs not claimed

**Claimed**

- Forced VL_Q thresholds and residual ∼ 2.6% (two-loop)
- Explicit ρ_{3'}, ρ₂, 2I (120), J-structure on weak sector
- M_X = Λ₀ if completion vectors exist; proton decay safe
- Precision-class approximate unification without continuous tuning

**Not claimed**

- Exact single-scale gauge unification
- M_X = μ_meet
- Full two-loop VL two-loop B coefficients for every multiplet
- Complete GUT algebra (SU(5)/SO(10)) derived from conoid
- Proton decay rate from a unified group broken at μ_meet

---

## 8. Future layer (explicitly open)

To derive M_X = μ_meet (or an independent GUT scale comparable to it) requires a **new** geometric layer:

1. Enlarge finite geometry beyond AF so that H and M₃ embed in a simple unified algebra, forced by 2I/conoid.
2. Stabilize a GUT-breaking modulus/VEV from the spectral action.
3. Compare that mass to μ_meet.

That work is **out of scope** for this document and is not required for the precision residual result above.

---

## 9. Relation to prior hardening

- Continuum η heat-kernel law: doc 32 (flavor; independent)
- Dual-Zero / G_N / generations: docs 18–20
- This doc: gauge unification path only
