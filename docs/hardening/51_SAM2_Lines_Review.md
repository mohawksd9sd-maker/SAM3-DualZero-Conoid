# 51 — Review of SAM-2, desktop math-model, and May 2026 Dual-Zero lines

**Date:** 23 November 2026 (America/Chicago)  
**Status:** exploratory review.  This document does not lock a new core theorem, does not restore any superseded May 2026 claim, and does not change the locked conoid geometry.  
**Ranking criterion (clarified):** keep the Dual-Zero *regulator* math intact or improve it, and among those options choose the line with the most realistic path toward a theory of everything.  Geometry and shape are negotiable.

Original SAM-2 PDFs, desktop math-model RTFs/TXT, and the May 14, 2026 local clone were read from local zips and are **not** in this repository.

---

## 1. What was reviewed

Three local archives, after unzip, path-normalization, and SHA-256 deduplication of zip-internal Desktop/OneDrive duplicates:

| Archive | Distinct files used |
|---------|---------------------|
| `sam2_models.zip` | SAM2 PDFs; SAM2.1 page fragments; SAM2.2 long text, HSTO text, four one-page PDFs, and an early `SAM3_v4.20_full_paper.tex.txt` |
| `math_models.zip` | `BILL.rtf`, `complete toe and gut math 0 foundational.rtf`, `einstiens dream math.rtf`, `einstiens dream math with field fixes.rtf`, `hsto grok 4.5.txt`, `jeff.rtf`, `jill.rtf`, `model 21 toe gut.rtf`, `newtons update.rtf`, `toe and gut math complete 1 hybrid foundational.rtf` |
| `sam3_may_clone.zip` | May 14, 2026 snapshot of `SAM3-DualZero-Conoid`, including paper 1.3 (Dual-Zero axiom), Papers 02, 05, and 07, and the v4.21/v4.22 math-model notes |

Honesty about filenames:

- The SAM-2 files titled “55 pages” are **8 PDF pages**, not 55.  The shorter SAM2 PDFs are 4 or 5 pages.  They are length variants of one note, dated 25–26 April 2026, version 2.21, titled “SAM2: A Hyperreal Dual-Zero Theory of Everything.”
- SAM2.1 “pages 11–20” etc. are 1–2 page fragments (one file is a 3.4 KB `.tex` stub), not a completed 55-page paper.  The extracted text of `SAM2_v2.21_55pages_full` in the SAM2 and SAM2.1 folders is identical.
- Several math-model RTFs are near-duplicates of one another (Einstein ± “field fixes”; `jeff` ≈ `model 21`; foundational / hybrid pair).  They are treated as variants of one algebraic line, not as independent theories.

Checks used in this review live in `experiments/sam2_review/` and `tests/test_sam2_review.py`.  They re-implement the stated formulas; they do not copy the source documents.

---

## 2. Dual-Zero, stated precisely, across versions

There are two genuinely different regulator definitions in the corpus.  Everything else is a variant or a later claim attached to one of them.

### 2.1 SAM-2 / desktop math-model definition (April 2026 and the RTF line)

- A dual-zero *entity* \([0,-0]\) is adjoined to \(\mathbb{R}\), giving a set \(S=\mathbb{R}\cup\{[0,-0]\}\).
- A number system \(\mathbb{R}_{[0,-0]}=S^{\mathbb{N}}/U\) is declared, with
  \[
  [0,-0]=\bigl[(0,-\tfrac12,0,-\tfrac14,0,-\tfrac16,\ldots)\bigr].
  \]
  Odd terms are \(0\); even terms are \(-1/n\).
- The SAM-2 notes and several RTFs take \(U=U_c\) to be a “constructive ultrafilter” whose base satisfies \(n_{k+1}>2n_k\).  The “foundational” RTF instead writes a free (non-principal) ultrafilter \(\mathcal{U}\), which is the standard (non-constructive) object.
- A piecewise map \(\operatorname{Reg}_2\) is written: the identity for \(\lvert x\rvert>10^{-64}\), and a formula involving an undefined \(H_{[0,-0]}\) below that threshold.  “Reg” in the first branch is also left undefined.

### 2.2 May 2026 / current SAM-3 definition (the regulator that still exists)

From paper 1.3 and Paper 02 in the May clone, and from the locked definition in doc 18:

- Generator
  \[
  \varepsilon(n)=\omega_0(-1)^n n^{-n},\qquad n\in\mathbb{N},\quad \omega_0\text{ an input}.
  \]
- A truncated arithmetic \(a+\varepsilon b+\varepsilon^2 c\), with products cut off at \(\varepsilon^2\).
- A symmetric average, used as a proposed regularisation of a function of a real variable,
  \[
  \operatorname{Reg}_2(f)(\lambda)=\lim_{\delta\to 0^+}\frac{f(\lambda+\delta)+f(\lambda-\delta)}{2}.
  \]
- This is a definition of a regulator, not a theorem about \(\zeta(s)\), and not a uniqueness theorem.  The November 2026 audit already records that \(\omega_0\) and the exponent \(4/13\) are inputs (docs 18, 42; `STATUS_CLAIMS_AND_RESIDUALS.md`).

The two definitions are **not** the same object.  The May/current sequence is nowhere zero and decays as \(e^{-n\log n}\).  The SAM-2 sequence is a standard null sequence in \(\mathbb{R}\) and vanishes on all odd indices.

---

## 3. Distinct lines

### Line A — SAM-2 v2.21 “hyperreal TOE”

**Sources.** SAM2 PDFs (4–8 pages); SAM2.1 fragments; SAM2.2 `SAM2.txt` and `1. Introduction and Historical Cont.txt` (long expansions of the same claims).

**Dual-Zero.** Definition 2.1, plus a running kernel
\[
f(k)=\ell_{\mathrm{Pl}}\Bigl(\frac{k_{\mathrm{Pl}}}{k}\Bigr)^{1/3}\Bigl(1+0.05\,\log_{10}^{-1}(k/k_{\mathrm{GUT}})\Bigr)^{-1},
\]
with the coefficient \(0.05\) attributed to “the smallest nontrivial \(E_8\) adjoint Casimir,” and a chain \(E_8\to\mathrm{SO}(10)\to\mathrm{SU}(5)\to\mathrm{SM}\).

**Unification claims.** A parameter-free TOE with “20 exactly derived” quantities, including \(\alpha=1/137.035999\) and \(m_h=125.25\,\mathrm{GeV}\).  Proofs are deferred (“available upon request”).  The “55-page paper” does not exist in the files that were reviewed.

### Line B — Desktop math-model RTFs (hybrid Dual-Zero / Einstein–Newton / SO(10) or \(E_8\))

**Sources.** `BILL.rtf`; both Einstein-dream RTFs; `newtons update.rtf`; `complete toe and gut math 0 foundational.rtf`; `toe and gut math complete 1 hybrid foundational.rtf`; `jeff.rtf`; `jill.rtf`; `model 21 toe gut.rtf`.

**Dual-Zero.** The same definition 2.1, with local variations: free ultrafilter versus “constructive” \(U_c\); a “cosmological” dual zero with entries \(\pm 10^{-10}\); occasional “field fixes”; a running \(f(k)\) of the same shape, sometimes written with a numerical prefactor \(3.88\times 10^{35}\) and a free \(\beta\).

**Unification claims.** The algebra is said to “provide a framework” for quantum gravity and a GUT, variously \(\mathrm{SO}(10)\), “\(E_8\)-like,” or (in `jill.rtf`) a 10-dimensional string manifold.  `newtons update.rtf` writes \(\dim(\mathrm{TOE})=28\).  None of these files derives a unique gauge group, a generation count, or a constant from the regulator alone.

### Line C — HSTO / HSC software

**Sources.** `SAM2.2/hsto updatedd sam2 522026.txt`; `math models/hsto grok 4.5.txt`; `ai code for HSTO/samson hsto.rtf`.

**Dual-Zero.** Incidental.  The cleaned HSTO text is a C++/CUDA “Hyperreal Sequence Compression” project with a license key and an optional Lagrangian containing \((k_{\mathrm{Pl}}/k)^{1/3}\).  The Samson RTF is a terminal log of a failing Python script, not a mathematical model.

**Unification claims.** None that can be read as a TOE.

### Line D — May 14, 2026 SAM-3, including the shape-independent core

**Sources.** The May clone: paper 1.3, Paper 02 (regulator), Paper 05 (gravity), Paper 07 (2I generations), and the accompanying math-model notes.  The early `SAM3_v4.20_full_paper.tex.txt` in the SAM2.2 folder is a bridge into this line.

**Dual-Zero.** Definition 2.2.  This is the only place in the desktop corpus where the regulator is written as a definite sequence plus a definite symmetric average, and where that definition can be stated without the conoid.

**Attached claims (not part of the regulator definition).** A uniqueness lemma (information conservation, commutation with \(\sin(2v)\) and with 12-bridge / 2I projectors, a variational Riemann-hypothesis principle); a “\(10\div 3=3.\overline{3}\) information loss” motivation; a 12-bridge icosahedral discretisation justified as the minimal \(2I\)-invariant choice; a claimed proof that \(2I\) acting on the 12 bridges produces exactly three chiral Standard Model generations; \(G_N=64\pi\ell_0^2/45\).

**What the November 2026 audit already superseded.** \(\omega_0\) is not derived; \(64\pi/45\) is a convention lock, not a scheme-free constant; the untwisted truncated-conoid APS index is \(0\), not \(3\); Yukawa / CKM / Higgs-mass “locks” are not derived; 12-bridge and 2I counting are not a derivation of three generations (`STATUS_CLAIMS_AND_RESIDUALS.md`, `papers/SUPERSESSION.md`, docs 42–44, 49–50).  Those verdicts are left in place.  The question for this review is only whether the *shape-independent regulator* in definition 2.2 is worth keeping, and whether anything else in the May bundle improves a TOE path once the superseded claims are stripped off.

### Line E — Current (November 2026) SAM-3 programme

Not a desktop-zip “new model,” but the honest baseline this review is measured against: locked right-conoid geometry; Dual-Zero kept as definition 2.2 with \(\omega_0\) an input; exploratory almost-commutative product with a CCM or Pati–Salam finite triple and a magnetized surface (docs 45–50).  The flux \(M=3\) and the surface moduli are not derived.

---

## 4. Math verdicts (what is correct, what is not)

### 4.1 Definition 2.1 (SAM-2 / Line A / Line B) is not a coherent regulator

1. **The stated “constructive ultrafilter” is not an ultrafilter.**  A computable family of sets with \(n_{k+1}>2n_k\) generates a filter, not an ultrafilter.  A free ultrafilter on \(\mathbb{N}\) is a non-constructive object (its existence uses a form of the axiom of choice; no such ultrafilter is computable).  Replacing it with a named “constructive” base does not produce the hyperreal field the notes assume.

2. **The Dual-Zero class can be identically zero.**  The SAM-2 sequence is \(0\) on every odd index and \(-1/n\) on every even index.  It converges to \(0\) in \(\mathbb{R}\).  If the (ultra)filter contains the even numbers — which is allowed by the stated doubling base, since that base may be chosen inside the evens — then the sequence is equivalent to the zero sequence, and \([0,-0]=0\).  The entity that was supposed to be the regulator then collapses.  (Checked in `tests/test_sam2_review.py`.)

3. **The piecewise \(\operatorname{Reg}_2\) is not a field homomorphism, and is not fully defined.**  `Reg` and \(H_{[0,-0]}\) are unspecified in the source.  Any stand-in that follows the written threshold rule fails additivity at the cutoff \(10^{-64}\): two sub-threshold values can sum to a super-threshold value, and the two sides of \(\operatorname{Reg}_2(a+b)=\operatorname{Reg}_2(a)+\operatorname{Reg}_2(b)\) disagree.  The threshold itself is ad hoc.

4. **The coefficient \(0.05\) is not an \(E_8\) Casimir.**  The standard adjoint quadratic Casimir of \(E_8\) (equivalently, the dual Coxeter number) is \(30\), not \(0.05\).  The running kernel \(f(k)\) also takes \(\ell_{\mathrm{Pl}}\), \(k_{\mathrm{Pl}}\), and \(k_{\mathrm{GUT}}\) as inputs.  Changing the free coefficient \(\beta\) or \(k_{\mathrm{GUT}}\) changes the output; a printed match to a CODATA value of \(\alpha\) is a fit, not a unique derivation.  The quoted figures in the long SAM2.2 text (`alpha(m_Z)=0.007297352569`, `1/alpha=137.035999084`) are experimental values restated.

5. **“20 exactly derived parameters” are not derived in the files.**  The note is 4–8 pages, proofs are deferred, and the inputs just listed are free.  This is not a TOE by the standard of a mathematical derivation.

Line B inherits (1)–(3) and, in several files, (4).  “Field fixes” and the switch from \(U_c\) to a genuine free ultrafilter make the setup closer to ordinary nonstandard analysis, but they do not define a new regulator with new physical output, and they do not remove the collapse of \([0,-0]\) on ultrafilters that contain the evens.  Declaring \(\mathrm{SO}(10)\) or \(E_8\) or \(\dim=28\) in the prose does not derive those choices from Dual-Zero.

### 4.2 Definition 2.2 (May / current) *is* a coherent regulator — with a smaller, precise scope

1. **The sequence is well-defined.**  \(\varepsilon(n)=\omega_0(-1)^n n^{-n}\) is an explicit real sequence, never zero for \(\omega_0\neq 0\), and decays faster than any exponential: \(\lvert\varepsilon(n)\rvert=\exp(-n\log n)\).  It cannot collapse by the even-filter mechanism that kills definition 2.1.  That is a genuine improvement of the regulator math, already present in the May 2026 axiom paper and retained in the locked definition (doc 18).

2. **The symmetric average is a standard operation.**  For a smooth function it returns \(f(\lambda)+O(\delta^2)\).  At a jump it returns the average of the one-sided limits.  It is a legitimate regularisation of pointwise values.  It is not, by itself, a theorem about the Riemann zeta function, and it does not determine \(\omega_0\).

3. **The “\(10\div 3\) information loss” motivation is false in \(\mathbb{Q}\) and in \(\mathbb{R}\).**  \(\frac{10}{3}\cdot 3=10\) exactly in the rationals, and \(0.\overline{9}=1\) in \(\mathbb{R}\).  Whatever one wants from a regulator, it cannot be grounded on a claim that ordinary arithmetic loses information in this way.

4. **Uniqueness of the regulator is not proved.**  The May uniqueness lemma mixes a definition with geometry-dependent requirements (commutation with \(\sin(2v)\), 12-bridge / 2I projectors) and a variational RH principle that this repository does not claim.  Once those extras are dropped, what remains is a definition, which is the honest status already recorded in docs 18 and 42.

5. **Weighting a heat trace by \(\varepsilon(n)\) does not reproduce the Weyl law.**  May Paper 02 writes a regularised heat trace \(\operatorname{Tr}_{\operatorname{Reg}}(e^{-tD^2})=\sum_n\varepsilon(n)\,e^{-t\lambda_n^2}\).  On the model spectrum \(\lambda_n=n\), the unweighted sum tracks the Weyl leading term as \(t\to 0\), while the \(\varepsilon\)-weighted sum remains \(O(1)\) and does not.  Super-exponential decay means that \(\varepsilon(n)\) is already negligible past the first several modes, so this weighting cannot act as a spectral cutoff that retains the volume term.  If Dual-Zero is to be used in a spectral action, it cannot be inserted in that way.  That is an enhancement the definition still needs: a precise rule for *how* the regulator acts on a spectrum, consistent with the Seeley–DeWitt expansion one actually wants.

### 4.3 May Paper 07 (2I ⇒ three generations) is not a proof

This is the main May-clone candidate for filling the generation gap in docs 47–50.  It does not.

1. **The character table in the paper is wrong.**  Paper 07 lists the complex irrep dimensions of \(2I\cong\mathrm{SL}(2,5)\) as \(1,2,2,3,3,4,5,6\).  The sum of squares is \(104\), not \(\lvert 2I\rvert=120\).  The standard dimensions are \(1,2,2,3,3,4,4,5,6\) (sum of squares \(120\)).  A 4-dimensional irrep is missing.

2. **The paper’s own embedding is inconsistent.**  The abstract and an early section produce three generations from three 2-dimensional irreps (including a “\(\chi_2''\)” said to arise as a tensor product).  The stated theorem instead uses two 2-dimensional irreps and one 3-dimensional irrep, then “quotients by the centre.”  Those are different constructions.  In any case, \(2\otimes 2=1\oplus 3\) in \(\mathrm{SU}(2)\); a third 2-dimensional irrep is not obtained that way.  The standard table has *two* 2-dimensional irreps, not three.

3. **The claimed permutation representation is not the icosahedron.**  Paper 07 writes \(\mathbf{12}=\mathbf{1}\oplus\mathbf{2}\oplus\mathbf{2}'\oplus\mathbf{3}\oplus\mathbf{4}\) for “the 12 bridges.”  The rotation group of the icosahedron is \(A_5\), of order 60, acting on 12 vertices; its permutation representation over \(\mathbb{C}\) is \(\mathbf{1}\oplus\mathbf{3}\oplus\mathbf{3}'\oplus\mathbf{5}\).  \(A_5\) has no 2-dimensional complex irrep (its irrep dimensions \(1,3,3,4,5\) square-sum to 60).  The binary cover \(2I\) does not act faithfully by permutation of those 12 vertices, because the kernel \(\{\pm 1\}\) acts trivially on them.

4. **“Projecting isolates three copies” puts 3 in by hand.**  Even if the representation theory were repaired, choosing a group because it has a 3-dimensional irrep, or because an icosahedron has 12 vertices, and then projecting onto three copies, is the same class of counting already rejected in docs 49–50.  Twelve vertices are not three generations.  The locked APS index of the untwisted truncated conoid is \(0\), not \(3\) (doc 44).  Dual-Zero is not what produces the integer 3 in this argument; the group-and-discretisation choice is.

### 4.4 Line C is not a TOE line

HSTO/HSC is a software sketch.  It does not preserve or enhance the regulator, and it has no unification content that can be tested as a physical model.

---

## 5. Does any SAM-2 or May idea fill the flux = 3 / moduli gap?

No.  That is a checked statement, not a preference.

- The gap, as left in docs 47–50: a magnetized compact surface (or a bundle of degree \(M\)) in a 4D almost-commutative product can produce \(M\) chiral zero modes, but \(M=3\) is chosen; the spectral action prefers smaller \(\lvert M\rvert\); Kronecker \(\det'\Delta\) and the locked \(C_4\) prefer different complex structures; no standard abelian \(T^6\) orbifold in the census has \(\lvert\chi\rvert/2=3\).
- Line A / B do not supply a principle that fixes \(M\) or the moduli.  Their \(E_8\) / \(\mathrm{SO}(10)\) language is an assumed chain, and their numerical “hits” on \(\alpha\) and \(m_h\) are fits to inputs.
- Line D’s 2I / 12-bridge argument does not survive the representation-theory checks in §4.3, and it does not become valid when the geometry is changed.  Replacing the conoid by another surface and still putting \(2I\) on 12 points is the same count.
- Definition 2.2 itself cannot be expected to select \(M=3\).  Because \(\varepsilon(n)\) is negligible beyond the first few indices, it does not act as a cutoff that could favour a particular flux or a particular \(\tau\) in a heat-kernel or determinant computation.  That is consistent with the weighted-heat-trace test in §4.2.

The missing principle recorded in `BOTTOM_LINE.md` is unchanged.

---

## 6. Ranking, under the clarified criterion

Geometry is negotiable.  The ranking is by (1) integrity or improvement of the Dual-Zero regulator, then (2) realistic unification path.

**Recommended combination.**  Keep and tighten definition 2.2 — the May 2026 / current generator \(\varepsilon(n)=\omega_0(-1)^n n^{-n}\) together with the symmetric average \(\operatorname{Reg}_2\) — *stripped* of the uniqueness lemma, the \(10\div 3\) motivation, the RH variational claim, the 12-bridge / 2I generation “proof,” and the Paper 02 heat-trace weighting \(\sum\varepsilon(n)e^{-t\lambda_n^2}\).  Attach that regulator, as a definition, to the November 2026 almost-commutative programme (a 4D product with a CCM or Pati–Salam finite triple and a compact surface whose flux and moduli are still to be derived, on a geometry that need not remain the conoid).  This is the only combination in the corpus that both preserves a well-posed Dual-Zero regulator and still has a unification path a mathematician can work on.

Why this wins on (1): definition 2.2 is already an enhancement of definition 2.1.  It is explicit, does not collapse under a choice of ultrafilter, and has a standard interpretation as a regularisation.  The current locked wording in doc 18 is the right wording, provided one also refuses the unsound heat-trace insertion.

Why this wins on (2): the \(E_8\) “20 exact parameters” path (Line A) and the RTF GUT sketches (Line B) are not realistic, because their regulator is not well-defined and their numerical claims are not derivations.  Restoring May 2I / 12-bridge as a TOE engine is not realistic, because the representation theory as written is wrong and would not derive 3 even if it were repaired.  The NCG / Pati–Salam (or magnetized-surface) product is the only unification mechanism in the reviewed material that is standard, internally consistent, and already tested honestly — and it still has a gap, which must remain labelled as a gap.

**Not recommended, in descending order of relevance.**

- Line D *as a finished May 2026 TOE*, with 2I, 12 bridges, and a derived \(G_N\), should not be restored.  Keep only the regulator definition.
- Line B does not improve the regulator and does not add a usable unification principle.  The occasional use of a genuine free ultrafilter is formally closer to Robinson nonstandard analysis, but that does not salvage \([0,-0]\) as defined, and it is strictly weaker than definition 2.2.
- Line A does not preserve a coherent Dual-Zero regulator and does not provide a realistic TOE path.
- Line C is not a candidate.

---

## 7. Concrete next step that would test the recommended combination

Write the Dual-Zero regulator as a standalone axiom, independent of the conoid, with two properties only:

- the sequence \(\varepsilon(n)=\omega_0(-1)^n n^{-n}\), \(\omega_0\) an input;
- the symmetric average \(\operatorname{Reg}_2\) acting on functions of a spectral parameter, not as a weight \(\varepsilon(n)\) on the heat trace.

Then put that axiom on a product geometry that already has a standard generation mechanism — the magnetized surface \(\times\) Pati–Salam (or CCM) product of docs 47–48, or another compact surface if the conoid is dropped — and compute, without fitting, whether the regulator changes any selection of flux or moduli (spectral action, regularised determinant, or a well-defined \(\operatorname{Reg}_2\) of the same spectral functions).  The expected honest outcome, given the decay of \(\varepsilon(n)\), is that it will *not* select \(M=3\) or a unique \(\tau\).  If that null result is confirmed, the regulator can still be kept as arithmetic regularisation, and the missing principle has to come from somewhere else.  If a selection appears without a parameter being chosen to make it so, that would be the first genuine enhancement of Dual-Zero toward a TOE, and it should be reported as such.

Do not spend further effort trying to repair Line A’s ultrafilter, the \(0.05\) running kernel, or Paper 07’s character table in the hope that they will produce three generations or a unique \(\alpha\).  Those constructions fail for reasons already checked.

---

## 8. Tests run

`experiments/sam2_review/regulator_checks.py`, collected in `tests/test_sam2_review.py`:

| Check | Result |
|-------|--------|
| \(\varepsilon(n)\) never vanishes; \(\lvert\varepsilon(n)\rvert=\exp(-n\log n)\), faster than \(e^{-4n}\) at \(n=100\) | pass |
| SAM-2 sequence converges to \(0\); vanishes on odds, nonzero on evens (even-filter collapse) | pass |
| \(\frac{10}{3}\cdot 3=10\) in \(\mathbb{Q}\); \(0.\overline{9}=1\) | pass |
| Piecewise SAM-2 \(\operatorname{Reg}_2\) fails additivity at the \(10^{-64}\) threshold | pass |
| Symmetric \(\operatorname{Reg}_2\) recovers a smooth value to \(O(\delta^2)\); averages a jump | pass |
| \(\varepsilon(n)\)-weighted heat trace fails the Weyl leading term; the unweighted sum tracks it | pass |
| \(E_8\) adjoint Casimir is \(30\), not \(0.05\) | pass (textbook value, not a numerical fit) |
| Standard \(2I\) dimensions square-sum to \(120\); Paper 07’s list square-sums to \(104\); claimed \(\mathbf{12}\) is not the \(A_5\) icosahedral permutation representation; \(12\neq 3\) | pass |
| The SAM-2 running kernel moves when \(\beta\) or \(k_{\mathrm{GUT}}\) is changed | pass |

These tests confirm the verdicts in §4.  They do not produce a new derivation of a physical constant.

---

## 9. What this review does not change

- Locked conoid geometry, \(C_4\), \(K\), \(C_0=2\pi\ln 2\), \(\int K=-2\pi\), exact \(E_0\), APS index \(0\), and the tip analysis stand.
- Dual-Zero remains a **definition**, with \(\omega_0\) an input (doc 18).
- \(G_N=\alpha\ell_0^2\) with \(64\pi/45\) a convention lock.
- Flux \(M=3\) and the surface moduli are still not derived.  The missing principle in `BOTTOM_LINE.md` is unchanged.
- No standalone paper is implied by this document.
