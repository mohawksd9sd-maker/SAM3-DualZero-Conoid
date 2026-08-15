# Mathematical Note IV — Uniqueness Preference and Adversarial Robustness

**SAM3 Dual-Zero Conoid**  
**Date:** August 2026  
**Status:** Preference under axioms — **not** an absolute uniqueness theorem  
**Authority:** STATUS; Math Notes I–II  
**Rule:** Derivation only; adversarial honesty.

---

## Abstract

We stress-test the locked geometric package against deformations of (i) bridge number $N$, (ii) metric tip coefficient $c$ in $f=\sqrt{u^2+c\ell_0^2\cos^2(2v)}$, and (iii) UV regulator. The package is **preferred** under the joint requirements of binary-icosahedral residual symmetry, the locked $G_N$–$\ell_0$ relation, and geometric $\omega_0$. Absolute uniqueness among all possible internal geometries is **not** established.

---

## 1. Axiom package (what “preferred” means)

A geometry is scored against:

| Axiom | Content |
|-------|--------|
| **A** | Internal 2D Riemannian metric of conoid type with tip modulation |
| **B** | Residual finite symmetry from **binary icosahedral / $A_5$** structure |
| **C** | APS Dirac continuum limit with finite light chiral multiplicity |
| **D** | Spectral-action $a_2$ → $G_N=64\pi\ell_0^2/45$ with **one** scale $\ell_0$ |
| **E** | Regulator strength $\omega_0$ fixed by curvature / bridge ratio (no experimental fit) |
| **F** | Cabibbo-scale angle $\sim\eta_{12}\pi/N$ compatible with defect overlaps |

---

## 2. Bridge number $N$

Continuum-style overlap law with angle $\cos(2\pi/N)$ (and C5 mix on the $(1,3)$ channel when $N=12$):

| $N$ | Cabibbo proxy $\eta_{12}\pi/N$ | 2I residual? | Notes |
|-----|-------------------------------|--------------|-------|
| 6–10 | $14^\circ$–$16^\circ$ class | No | No binary-icosahedral bridge count |
| **12** | $\approx 12.7^\circ$–$12.85^\circ$ | **Yes** | Locked |
| 14–24 | falls toward $7^\circ$–$11^\circ$ | No | Generation schema of Note I fails |

**Result:** $N=12$ is **required** for the joint 2I + Cabibbo story. Other $N$ are different models, not small perturbations of SAM3.

---

## 3. Tip coefficient $c$ ($4$ vs $16$ vs others)

Locked metric:

$$
f=\sqrt{u^2+c\ell_0^2\cos^2(2v)},\qquad c=4.
$$

| $c$ | Joint $G_N$–$\ell_0$–$\omega_0$ | Verdict |
|-----|-------------------------------|--------|
| 4 | Consistent | **Locked** |
| 16 | Equivalent to rescaling $\ell_0$ after $G_N$ lock — **forbidden** | Superseded |
| other | $\omega_0\propto c^{2/13}$ shifts if curvature tracks $\sqrt{c}$ | Requires retuning $\omega_0$ or $G_N$ formula |

Schematic: relative $\omega_0$ factor $(c/4)^{2/13}$ gives $\approx 1.24$ at $c=16$ (would push $\omega_0\sim 1.15$ if naively rescaled).

**Result:** $c=4$ is **high preference** under axioms D–E; not a free knob.

---

## 4. Regulator deformations

| Change | Effect on $G_N$ | Effect on 3 generations | Effect on IR Yukawa class |
|--------|------------------|-------------------------|---------------------------|
| Dual-Zero $\omega_0\pm 5\%$ | Leading $a_2$ unchanged | Unchanged (APS carrier) | Small |
| Replace DZ by $e^{-n}$ weights | Leading $a_2$ unchanged | Unchanged | UV pollution differs |
| Replace DZ by $n^{-3}$ | Leading $a_2$ unchanged | Unchanged | Heavier UV tails |
| Drop APS | — | **Generation claim fails** | — |

**Result:** $G_N$ and generation count are **robust** to regulator scheme at leading order; Dual-Zero is **not** the load-bearing definition of either. UV-sensitive claims are **not** robust to arbitrary regulators.

---

## 5. Angular harmonic $\cos(2v)$

| Harmonic | Grading / bridge compatibility | Verdict |
|----------|--------------------------------|--------|
| $\cos(2v)$ | Even under $v\to v+\pi$; matches locked construction | Preferred |
| $\cos(v)$ | Different tip defect multiplicity | Different model |
| $\cos(3v)$ | Misaligned with C5 tip story | Different model |

---

## 6. Scorecard

| Deformation | Survives? | Strength |
|-------------|-----------|----------|
| $N=12$ fixed by 2I + Cabibbo | Yes, required | High preference |
| $c=4$ fixed by $G_N$+$\omega_0$ | Yes, required | High preference |
| Small $\omega_0$ band | Yes | Robust |
| DZ ↔ heat kernel for **leading** $G_N$ | Yes | Robust |
| Absolute uniqueness of conoid among all metrics | **No** | Open |
| Uniqueness among all NCG finite algebras | **No** | Open |

---

## 7. Theorem-shaped statements (careful wording)

**Proposition (Preference, not uniqueness).**  
Within the axiom package A–F, the simultaneous requirements of binary-icosahedral residual symmetry, Cabibbo scaling $\sim\pi/N$, and a single-scale $G_N(\ell_0)$ relation select $N=12$ and tip coefficient $c=4$ over the nearby discrete alternatives tested above.

**Non-claim.**  
There is no theorem in this note that every consistent spectral triple yielding the Standard Model must use this right conoid.

---

## 8. Residuals for external attack

1. Full continuum APS spectra at $c\neq 4$ with fixed $\ell_0$ (quantitative $\Delta\eta$).  
2. Whether another finite group (not 2I) with different $N$ could reproduce three families + Cabibbo-scale angle.  
3. Independent re-derivation of defect overlaps.  
4. Absolute uniqueness — out of scope until broader classification results exist.

---

## 9. Relation to community calibration

This note **raises internal robustness** under adversarial deformation. It does **not** replace external scrutiny or peer review. Serious geometric programs remain ahead on community calibration until Notes I–II and this robustness analysis are checked outside the collaboration.

---

*Uniqueness preference + adversarial robustness — August 2026.*
