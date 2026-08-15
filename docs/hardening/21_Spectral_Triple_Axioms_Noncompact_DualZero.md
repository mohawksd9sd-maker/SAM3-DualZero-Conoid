# Spectral Triple Axioms — Non-Compact Conoid + Dual-Zero

**Status:** Expanded functional-analytic checklist locked; compact resolvent and full Lorentzian causality remain residual where stated (August 2026)  
**Rule:** Derivation only; no overclaim of completed operator theory.

This note addresses foundational item **1c**: complete, explicit statements of the spectral triple axioms for the **infinite-volume right conoid** with **Dual-Zero / hyperreal regulation**, including what is established, what is by construction, and what is residual.

---

## 1. Data of the triple

$$
(\mathcal{A},\,\mathcal{H},\,D_\varepsilon)
$$

with

$$
\begin{aligned}
\mathcal{A} &= C^\infty_{\mathrm{DZ}}(M)\otimes \mathbb{C}[2I]\otimes \mathcal{A}_F,\\
\mathcal{H} &= L^2(M,S)\otimes \mathbb{C}^{120}\otimes {}^*\mathbb{C}_{\mathrm{DZ}},\\
D_\varepsilon &= D_{\mathrm{geo}} + D_{\mathrm{bridge}} + D_{\mathrm{DZ}},
\end{aligned}
$$

where:

- $M$ is the right conoid (non-compact, 2D continuum + 12-bridge structure),
- $\mathcal{A}_F=\mathbb{C}\oplus\mathbb{H}\oplus M_3(\mathbb{C})$,
- $D_{\mathrm{DZ}}$ implements Dual-Zero regulation (doc 18),
- Lorentzian reading uses a Krein structure $(\mathcal{H},\langle\cdot,\cdot\rangle_K,\beta)$ with $\beta^2=1$ (doc 17 residual for full causality).

Euclidean spectral-action calculations use the standard positive heat-kernel setting after regulation; Lorentzian physics is recovered by Wick rotation + KO data unless a full Lorentzian triple is claimed (it is not — doc 17).

---

## 2. Axiom-by-axiom statements

### Axiom C1 — Algebra and representation

**Statement.** $\mathcal{A}$ is a unital involutive algebra represented by bounded operators on $\mathcal{H}$ (or on the positive-definite completion induced by $\beta$ in the Krein setting).

**Status.** **Satisfied by construction.**  
$C^\infty$ functions with Dual-Zero values act by multiplication; $\mathbb{C}[2I]$ and $\mathcal{A}_F$ act by the regular / standard finite representations. Smooth compactly supported (or Dual-Zero-regulated) cutoffs keep multiplication operators bounded on the $L^2$ space used for the continuum factor.

---

### Axiom C2 — Self-adjointness (or Krein self-adjointness)

**Statement (Euclidean reading).** $D_\varepsilon$ is essentially self-adjoint on a dense domain $\mathrm{Dom}(D_\varepsilon)\subset\mathcal{H}$.  
**Statement (Lorentzian reading).** $D_\varepsilon$ is $\beta$-self-adjoint: $D_\varepsilon^\dagger=\beta D_\varepsilon\beta=D_\varepsilon$ on the appropriate domain.

**Status.** **Partially established.**  
- $D_{\mathrm{geo}}$ on the conoid with APS / suitable tip boundary conditions is treated as essentially self-adjoint in the continuum residual program (docs 10, 02).  
- Bridge terms are finite-rank / multiplication-type in the discrete 2I directions.  
- Dual-Zero perturbation is relatively bounded with relative bound $0$ at the level of the super-exponential sequence (Paper 02 functional calculus claim).  

**Residual.** A single published theorem with explicit domain, deficiency indices, and boundary form for the *full* $D_\varepsilon$ on the infinite conoid is still a functional-analysis deliverable, not a completed reference in the repo.

---

### Axiom C3 — Compact resolvent

**Statement.** $(D_\varepsilon-\lambda)^{-1}$ is compact for $\lambda\notin\mathrm{spec}(D_\varepsilon)$ (Euclidean / positive completion).

**Status.** **Intended mechanism locked; full proof residual.**  

**Mechanism:** The bare geometric Dirac operator on a non-compact conoid need not have compact resolvent. Dual-Zero regulation supplies super-exponential damping of the high mode tail (axiom A3 of doc 18), which is the model’s replacement for a hard compactification. Bridge terms do not reintroduce continuous spectrum in the discrete $2I$ directions.

**Residual (honest).**  
A complete proof that $\mathrm{Reg}_2$ turns the resolvent compact *on the specific conoid metric with APS tip conditions*, with explicit operator-norm estimates, is **not** claimed as finished. This is the single most important open functional-analytic item in 1c.

---

### Axiom C4 — Bounded commutators

**Statement.** For all $a\in\mathcal{A}$, the commutator $[D_\varepsilon,a]$ extends to a bounded operator on $\mathcal{H}$.

**Status.** **Satisfied for the geometric and finite parts under standard smooth-function hypotheses.**  
- $[D_{\mathrm{geo}},f]$ is Clifford multiplication by $df$ (bounded for $f$ with bounded gradient in the regulated algebra).  
- Finite and bridge contributions give bounded commutators by construction.  

**Residual.** Hyperreal-valued algebra elements require that “bounded” be read after standard part for physical observables; this is consistent with doc 18 A4 but should be spelled in any journal-level write-up.

---

### Axiom C5 — First-order condition

**Statement.** For all $a,b\in\mathcal{A}$,

$$
[[D_\varepsilon,a],b^0]=0
$$

(with $b^0=Jb^*J^{-1}$ in the real case).

**Status.** **Satisfied by the product structure.**  
- Geometric Dirac operators on commutative spin manifolds satisfy the first-order condition.  
- Finite CCM-type $D_F$ is constructed to satisfy it.  
- Bridge terms that act as multiplication in the continuous variables and finite matrices in the $2I$ factor preserve the double-commutator vanishing when they do not introduce derivative order in the algebra variables.

**Residual.** A line-by-line verification for every generator of $\mathbb{C}[2I]$ in the presence of Dual-Zero is bookkeeping, not a conceptual obstruction.

---

### Axiom C6 — Real structure $J$

**Statement.** There exists an anti-unitary $J$ with the KO-dimension signs:

$$
J^2=\varepsilon,\quad JD=\varepsilon' DJ,\quad J\gamma=\varepsilon''\gamma J
$$

(with $\varepsilon,\varepsilon',\varepsilon''\in\{\pm 1\}$ fixed by KO-dimension), implementing the opposite algebra $a\mapsto Ja^*J^{-1}$.

**Status.** **Satisfied at the level of the finite SM algebra + standard spin real structure on the continuum factor.**  
KO-dimension 6 for the finite part is the usual SM choice. Continuum even-dimensional spin structure supplies a compatible charge conjugation.

**Residual.** Global sign bookkeeping on the full product with bridges should be tabulated once in an appendix; not expected to change physics outputs of the hardening layer.

---

### Axiom C7 — Grading $\gamma$

**Statement.** A $\mathbb{Z}_2$-grading $\gamma$ ($\gamma^*=\gamma$, $\gamma^2=1$) anticommutes with $D_\varepsilon$ and commutes with $\mathcal{A}$ (even triple).

**Status.** **Satisfied.**  
Product grading $\gamma_5^{\rm tot}=\gamma_5^{c}\otimes\gamma_5^{F}$ (Paper 11 product construction) anticommutes with the total Dirac operator when each factor does. Dual-Zero terms are chosen grading-compatible (doc 18 A2).

---

### Axiom C8 — Orientability / Poincaré duality (K-theoretic)

**Statement.** The fundamental class in $KR$-homology pairs correctly with $K$-theory of $\mathcal{A}$ (Poincaré duality in the appropriate KO-dimension).

**Status.** **Inherited from CCM finite geometry + oriented continuum factor; not re-proved from scratch here.**  

**Residual.** A self-contained $K$-homology computation for the regulated non-compact conoid is beyond the present lock; the model relies on the standard almost-commutative duality package.

---

## 3. Non-compact-specific issues (summary)

| Issue | Model response | Claim level |
|-------|----------------|-------------|
| Continuous spectrum of non-compact $M$ | Dual-Zero super-exponential regulation | Mechanism locked; compact-resolvent **proof residual** |
| Essential self-adjointness at tip | APS boundary conditions | Implemented in continuum program; full domain theorem residual |
| Hyperreal-valued algebra | Standard part for observables (A4) | Consistent with doc 18 |
| Lorentzian causality | Wick + KO (doc 17) | Full Lorentzian triple **not claimed complete** |

---

## 4. What 1c does *not* claim

- A finished proof of compact resolvent for $D_\varepsilon$ in a standard functional-analysis reference sense.  
- A complete Lorentzian spectral triple with proven causal propagation (doc 17).  
- A new $K$-theory computation replacing CCM duality.

---

## 5. What 1c *does* lock

- Precise axiom list adapted to non-compact + Dual-Zero.  
- Clear separation of **by construction / partially established / residual**.  
- Identification of **compact resolvent** as the principal remaining functional-analytic bottleneck.  
- Alignment with Dual-Zero definition (doc 18), continuum residual (doc 10), and Lorentzian residual discipline (doc 17).

---

## 6. Lock statement

> The SAM3 spectral triple is defined as $(\mathcal{A},\mathcal{H},D_\varepsilon)$ on the non-compact right conoid with Dual-Zero regulation. Algebra representation, first-order condition, bounded commutators (smooth regime), real structure, and grading hold by the standard almost-commutative and geometric constructions, adapted to Dual-Zero. Compact resolvent is the intended consequence of Dual-Zero super-exponential damping of the non-compact spectrum; a complete operator-theoretic proof of compactness on this metric with APS conditions remains residual. Full Lorentzian causality is not claimed (doc 17). Poincaré duality is inherited from the CCM finite package plus oriented continuum structure, not re-derived here.

---

*Locked under the rule: derivation only, no overclaim. Next foundational item: 1d Lorentzian reconstruction residual expansion / upgrade path.*
