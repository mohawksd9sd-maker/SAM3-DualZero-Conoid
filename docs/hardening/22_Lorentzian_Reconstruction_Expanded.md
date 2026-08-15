# Lorentzian Reconstruction — Expanded Residual and Upgrade Path

**Status:** Residual discipline expanded and locked (August 2026)  
**Rule:** Derivation only; no claim of a completed Lorentzian spectral triple theorem.

This note addresses foundational item **1d**: expand the Lorentzian reconstruction status beyond a one-line residual flag, state exactly what is claimed, what is not, and what an upgrade path would require.

Cross-references: doc 17 (residual discipline), doc 21 (axioms C1–C8), Paper 21 (historical Lorentzian spectral-action text — claim language superseded where stronger than this note).

---

## 1. Physical requirement

Observed spacetime is Lorentzian. The bosonic effective action used for $G_N$, gauge kinetics, and the Higgs sector is obtained from the **Euclidean** spectral action / Seeley–DeWitt expansion (docs 13, 20). A controlled passage Euclidean $\to$ Lorentzian is therefore mandatory for physical interpretation.

---

## 2. What is claimed (locked, limited)

### 2.1 Wick rotation of the 4D factor

After the almost-commutative product is formed and the Euclidean spectral action is evaluated, the 4D metric factor is Wick-rotated in the standard QFT sense:

$$
g_{\mu\nu}^{E}\;\longrightarrow\; g_{\mu\nu}^{L},
\qquad
t\;\longrightarrow\; -it,
$$

with the usual $i\varepsilon$ / causal prescriptions of effective field theory. The resulting Lorentzian effective Lagrangian density has the Einstein–Hilbert, Yang–Mills, and Higgs kinetic/potential structures already derived geometrically.

### 2.2 KO-dimension / real structure compatibility

The finite algebra $\mathcal{A}_F$ is equipped with the standard real structure and KO-dimension **6** package used for the Standard Model in Connes–Chamseddine-type constructions. This supplies the correct chirality and charge-conjugation structure for the fermion sector after the product is formed.

### 2.3 Krein-space *intention*

The model is *intended* to admit a Krein-space reading $(\mathcal{H},\langle\cdot,\cdot\rangle_K,\beta)$ with $\beta^2=1$ and $\beta$-self-adjoint $D$ (docs 17, 21). This is the standard Lorentzian NCG language (van den Dungen–Paschke–van Suijlekom and related frameworks).

**Locked claim:**  
> Lorentzian physics is recovered by **standard Wick rotation of the 4D factor** plus **SM-compatible KO / real-structure data**. This is the claim level of ordinary almost-commutative geometry practice, not a new SAM3 theorem.

---

## 3. What is *not* claimed

| Not claimed | Why |
|-------------|-----|
| A fully constructed Lorentzian Dirac operator $D_L$ on the conoid product with proven domain theory | Only Euclidean $D_\varepsilon$ + Wick is used for spectral action |
| Proof of causality (finite propagation speed / causal propagator) for $D_L$ | Not written |
| Theorem that Euclideanisation of $D_L$ recovers the present $D_\varepsilon$ with controlled error | Not written |
| Exact cancellation of the cosmological constant as a Lorentzian theorem | Mechanism residual; magnitude residual (docs 06, 17) |
| Paper 21-style “complete Lorentzian spectral action” as finished | Superseded by this residual map |

Paper 21 remains useful as a **roadmap** of intended Krein heat-kernel steps; its abstract/conclusion language of completion is **not** the hardened claim surface.

---

## 4. Why Wick + KO is still a legitimate interim stance

1. **Spectral action technology** is heat-kernel based and is standardly Euclidean.  
2. **Almost-commutative SM geometry** has long used Euclidean derivation + Wick for 4D physics.  
3. **Locked SM/gravity numbers** ($G_N$ structure, flavor locks, Higgs class) live in the Euclidean coefficient algebra; Wick does not retune $\omega_0$ or $\{C_g\}$.  
4. Over-claiming a finished Lorentzian triple would violate the derivation-only residual rule.

---

## 5. Upgrade path (what “closing 1d” would mean)

A future upgrade that *would* allow a stronger claim must deliver, in order:

### Step L1 — Lorentzian Dirac operator

Define $D_L$ on the product geometry with:
- explicit principal symbol of Lorentzian type,
- fundamental symmetry $\beta$,
- domain specified (including APS / tip conditions lifted to the Lorentzian setting).

### Step L2 — Krein self-adjointness theorem

Prove essential $\beta$-self-adjointness of $D_L$ (or a unique self-adjoint extension selected by Dual-Zero + APS).

### Step L3 — Causal propagator

Construct the advanced/retarded propagators (or justify finite propagation speed) for the Lorentzian wave operator associated with $D_L^2$.

### Step L4 — Euclideanisation match

Prove that Wick rotation / analytic continuation of the Lorentzian spectral data recovers $D_\varepsilon$ and the Seeley–DeWitt coefficients used for $G_N$ and the Higgs class, with error bounded by Dual-Zero tails.

### Step L5 — Optional: Lorentzian spectral action

Only after L1–L4, formulate a Lorentzian spectral action whose expansion matches the bosonic Lagrangian already locked in Euclidean form.

Until L1–L4 exist as written proofs or complete references internal to the repo, the claim level remains **Wick + KO**.

---

## 6. Relation to continuum and Dual-Zero residuals

| Residual | Interaction with Lorentzian upgrade |
|----------|-------------------------------------|
| Compact resolvent of $D_\varepsilon$ (doc 21 C3) | Must have a Lorentzian analogue or a justified Euclidean-only spectral action |
| APS tip conditions (doc 10) | Must lift to Lorentzian boundary theory in L1–L2 |
| Dual-Zero A3 decay (doc 18) | Expected to help UV control in both signatures |

---

## 7. Phenomenology impact

**None of the locked flavor numbers, $G_N$ prefactor, or Higgs class depends on a completed L1–L5.**  
They depend on Euclidean coefficients + geometric inputs. Closing 1d improves **foundational integrity**, not the present numerical locks.

---

## 8. Lock statement

> Lorentzian reconstruction in SAM3 is claimed only at the level of **standard Wick rotation of the 4D factor** together with **SM-compatible KO-dimension / real-structure data**. A rigorous Lorentzian spectral triple on the conoid product, with proven causality and Euclideanisation matching the working Dirac operator $D_\varepsilon$, is **not** complete and is **not** claimed. Paper 21’s stronger “complete Lorentzian spectral action” language is superseded by this residual map. An explicit upgrade path (L1–L5) is recorded for future work.

---

*Locked under the rule: derivation only, no overclaim.*

**Foundational section 1 (1a–1d) is now complete at the expanded residual-discipline level.**  
Next block in the user’s ordered list: **§2 Numerical production readiness.**
