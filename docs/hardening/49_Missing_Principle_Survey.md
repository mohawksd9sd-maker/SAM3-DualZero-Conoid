# 49. Survey of candidate principles for the flux, the moduli, and the generation count

**Date:** 23 November 2026 (America/Chicago)  
**Status:** exploratory; not part of the locked core.  
**Code:** `experiments/missing_principle/`  
**Tests:** `tests/test_missing_principle.py`  
**JSON:** `reproducibility/missing_principle_report.json`

Honesty rule: unproven statements are labelled.  Null results stay null.  Number-matching that is only a count is flagged as numerology.  Citations are from sources consulted for this note, not invented.

This note does two jobs.  It records, briefly and in plain language, how the November 2026 Alpöge/Claude Lean proof of the Riemann hypothesis is said to work, and what of that method is (and is not) public.  It then surveys a much wider range of mathematics and mathematical physics for a principle that could fix the flux at 3, fix the surface moduli, or otherwise derive the generation count for SAM-3, and it tests four mechanisms in code.

---

## 1. What is already settled, and what is missing

The locked conoid theorems, the unification experiments of docs 44–48, and the list of underived inputs are stated in [`BOTTOM_LINE.md`](../../BOTTOM_LINE.md).  In short:

- The conoid itself is in good mathematical order: the metric, \(C_4\), curvature, \(C_0=2\pi\ln 2\), \(\int K=-2\pi\), exact \(E_0(m)\), APS index 0, and the tip structure are theorems.
- The 4D product conoid \(\times\) magnetized \(\Sigma\) \(\times\) a CCM or Pati–Salam finite triple is a consistent almost-commutative geometry, but the integer 3 and the moduli of \(\Sigma\) (area, \(\tau\), Wilson lines) are choices.  The spectral action of a magnetized torus prefers smaller \(\lvert M\rvert\), not \(M=3\).
- The Dual-Zero inputs \(\omega_0\), the exponent \(4/13\), and the prefactor \(\alpha\) in \(G_N=\alpha\ell_0^2\) are not derived either.

The missing principle, for the product programme, is something that *fixes the flux at 3 and the surface moduli*.

---

## 2. How the November 2026 Riemann proof works (plain language)

On 20 November 2026, Levent Alpöge announced, in a four-page note at `https://alpo.ge/remark.pdf`, a Lean formalization of the Riemann hypothesis and of the generalised Riemann hypothesis for Dirichlet \(L\)-functions, developed with Claude.  The Lean FRO and the Mathlib Initiative reported (21 November) that the formalization meets Buzzard’s four criteria: the statement is Mathlib’s `RiemannHypothesis`, it compiles, it was checked by a comparator / `con-leche` comparison, and it was replayed on independent kernels, including formally verified ones.  Andrew Sutherland’s page (updated 23 November 2026, 14:35 UTC, which is 8:35 AM America/Chicago) records a successful compile of 175,187 modules on Lean/Mathlib v4.33.1, with only the three standard Lean axioms, and notes that some additional kernel checks were still running at that time.

**What the argument is, as now explained in human language.**  There is not yet a complete traditional writeup by the author.  The best currently available accounts are Alpöge’s remark, a 265-page working draft of Rubinstein with Claude, Codex and Gemini specialised to \(\zeta\) (v2, 22 November 2026), and two Hexagon outlines (Slijepcevic; Jaswal), all labelled as work in progress.  Rubinstein’s draft is explicit: it proves that a one-sided bound on a smoothed prime-power sum \(G(x)\) on a sparse sequence of long intervals implies RH; it reduces that bound to a main inequality (M) plus two character estimates; and it *does not prove (M)*.  It reduces (M), and with it RH, to thirteen numbered hypotheses stated in classical terms, none of which is proved outright in that paper.  Several steps are taken from the Lean development.  So the *ideas* of the proof are public; a fully digested human proof of the arithmetic heart is not, as of 22–23 November 2026.

With that caveat, the method, as described by Alpöge and by Rubinstein’s eight-step plan, is as follows.

1. *A Chebyshev comparison, not a direct attack on zeros.*  The classical idea is that a nonzero integer is at least as large as the product of the prime powers that divide it.  A one-sided upper bound \(G(x)\le x^{1/2+\varepsilon}\) on a smoothed, centred count of prime powers, valid on intervals \([Y,Y^{3/2}]\) with \(Y\) arbitrarily large, excludes zeros of \(\zeta\) in \(\operatorname{Re}s>1/2\), by a Landau-type criterion on Mellin transforms.  (An earlier form of the same step, in the announcement, was a positivity \(W\ge 0\) in the Guinand–Weil explicit formula, obtained from a Stepanov-style determinant.  Rubinstein presents the final analytic step as the Landau criterion, and treats the Weil-positivity language as an earlier formulation.)

2. *The “integer” is a map of lattices.*  Over function fields, Stepanov’s proof of the analogue of RH uses an auxiliary function that vanishes to high order at many points; the multiplicity is cheap.  Over \(\mathbb{Z}\), high-order vanishing is not cheap.  The replacement is a linear map between Hermitian lattices of large rank, coming from a *chain of theta lifts* between (mostly totally definite) unitary groups.  Each lift plays the role of one more order of vanishing.  For a prime-power sum of length \(x\), the chain is about \(\sqrt{x}\) lifts long.  That is where the exponent \(1/2\) comes from: an error \(x/m\) at the ends of the chain balances an accumulated error \(m\) at \(m\approx\sqrt{x}\).  (A slightly worse bookkeeping, \(x/m+m^2\), would have given the exponent \(2/3\).)

3. *Divisibility versus size, through slopes.*  A lower bound on the divisibility of the iterated lift, at primes that remain prime in an auxiliary CM field (the model case is the lemniscate, complex multiplication by \(\mathbb{Z}[i]\)), is compared with an upper bound on the size (the norm, or the covolume) of the same map.  The comparison is a slope inequality for a map of lattices (Bost; filtration by slopes of Stuhler and Grayson).  The main terms, through the term linear in the length, are shown to cancel, using period formulae (Kronecker / Chowla–Selberg), mass formulae (Siegel), the inner-product formula for theta lifts (Rallis), and Weyl’s dimension formula.  Denominators along the chain are controlled by Galois cohomology / Iwasawa-theoretic bounds.  A relative trace formula (Jacquet) is used to show that a family of such maps fills almost the whole target lattice, so that a mean slope, not just the largest slope, is controlled.

4. *From special primes to all primes.*  The inequality (M) first controls a sum over certain residue classes (cells of a table built from an Iwasawa-type tower and a Behrend construction).  Averaging, and two estimates for auxiliary Dirichlet characters, produce the bound on \(G(x)\).

**Workflow.**  Alpöge guided the analogy (Stepanov, a toy CM setting, Chebyshev).  He reports that Claude suggested the \(\sqrt{X}\) length of the lift chain and carried a large part of the technical finish.  The argument was released *in Lean only*, because, in his words, he had not mastered a human writeup.  The formalization is about 17 million lines in 175,187 modules, on Lean 4.33.1, depending on Mathlib only for the ambient library.  The top-level file `Main.lean` has five theorems.  All five reduce to one core statement, `everyCharacter`: no Dirichlet \(L\)-function has a zero with \(\operatorname{Re}s>1/2\) (with the usual caveat at \(s=1\) for the trivial character).  Mathlib’s `RiemannHypothesis`, and the critical-line statements for \(\zeta\) and for Dirichlet \(L\)-functions, follow from that by the Euler product and the functional equation.  The rest of the archive is organised in large libraries (`Development`, `Formalism`, `GroundTheory`, `ReciprocityTheory`, `CompanionTheory`, `PositivityTheory`, …).  This layout was read from a public description of the archive and from the text of `Main.lean`.  The 14-part tarball itself was not downloaded or rebuilt in this repository; the certification reported above is that of the Lean FRO, Mathlib Initiative, and Sutherland, not an independent rebuild here.

**What transfers, and what does not.**  The proof is a theorem about primes and \(L\)-functions.  Its specific objects — iterated theta lifts, CM inert primes, Iwasawa towers, Galois cohomology of Tate twists — do not act on the conoid, and they do not, by themselves, prefer the integer 3.  Three broader *styles* of argument are worth testing on SAM-3: (i) positivity / one-sided bounds / regularized determinants and trace formulae, as a way of selecting a geometric parameter by a spectral inequality; (ii) slope or stability inequalities for lattices or bundles; (iii) the human-plus-AI-plus-Lean workflow, as a process for searching and then certifying a uniqueness statement, not as a substitute for the missing principle.  Connes’ earlier spectral approach to RH (Weil positivity on the adele class space) is a *different* programme from Alpöge’s, and is also not a derivation of the generation count.  The appearance of the lemniscate (CM by \(i\)) in the model divisibility calculation is suggestive of the square torus, but treating that as a reason to set \(\tau=i\) in SAM-3 would be numerology, and is not used as such below.

---

## 3. Computations on SAM-3

Four mechanisms that can be stated precisely on the locked conoid or on the magnetized-torus factor were tested.  None is part of the locked core.

### 3.1 Extremizing \(\det'\Delta\) on a unit-area flat torus (Kronecker / Osgood–Phillips–Sarnak)

For a unit-area flat torus of modulus \(\tau\), Kronecker’s first limit formula identifies the height \(Z'(0)\) of the Laplacian, up to an additive constant, with \(-\log\bigl(\operatorname{Im}(\tau)\,|\eta(\tau)|^4\bigr)\).  Consequently \(\det'\Delta=\exp(-Z'(0))\) is maximized exactly where the modular function

\[
  F(\tau)=\sqrt{\operatorname{Im}(\tau)}\,|\eta(\tau)|^2
\]

is maximized.  Osgood, Phillips and Sarnak (J. Funct. Anal. 80 (1988) 148–211) proved that this maximum, among unit-area flat tori, is attained at the hexagonal lattice.  This module does not re-prove that theorem.  It evaluates \(F\) from the Dedekind product, checks modular invariance under \(\tau\mapsto\tau+1\) and \(\tau\mapsto-1/\tau\), and searches the standard fundamental domain.

Computed values:

- \(F(i)\approx 0.590170299508\)
- \(F(e^{2\pi i/3})=F(e^{i\pi/3})\approx 0.596450134364\)
- The grid maximum in the fundamental domain sits at the hexagonal vertex, at distance 0 from \(\tau=-1/2+i\sqrt{3}/2\).
- Among rectangular tori (\(\operatorname{Re}\tau=0\), \(\operatorname{Im}\tau\ge 1\)), the maximum is at the square torus \(\tau=i\).
- A sample modular-invariance error is at machine precision (\(\sim 10^{-16}\)).

**Verdict: promising for \(\tau\) only, and in conflict with \(C_4\).**  If the principle is “maximize \(\det'\) of the scalar Laplacian at fixed area, among flat tori”, then \(\tau\) is fixed uniquely (up to \(\mathrm{SL}(2,\mathbb{Z})\)) to the hexagonal value \(e^{2\pi i/3}\).  The area is not fixed, and the flux is not touched.  The hexagonal torus has a \(\mathbb{Z}_6\) automorphism, not a \(\mathbb{Z}_4\).  A requirement that \(\Sigma\) share the conoid’s \(C_4\) symmetry would instead select \(\tau=i\), which is only a critical point among rectangular tori and is *not* the global maximizer of \(\det'\Delta\).  Any missing principle has to choose, or resolve, this tension.  It is not resolved here.

### 3.2 The zeta-regularized determinant of the *magnetized* Dirac operator

The Dirac spectrum on a flat torus of area \(A\) and integer flux \(M>0\) is the Landau-level spectrum \(E_n=\pm\sqrt{4\pi n M/A}\) with multiplicity \(M\), plus \(M\) zero modes of one chirality.  It is independent of \(\tau\).  The zeta function of \(D^2\) on the nonzero eigenspaces is exact,

\[
  \zeta_{D^2}(s)=2M\bigl(4\pi M/A\bigr)^{-s}\zeta(s),
\]

and \(\zeta'_{D^2}(0)=M\log(2M/A)\), hence

\[
  \log\det'\lvert D\rvert=-\frac{M}{2}\log(2M/A).
\]

This closed form was checked against a truncated Landau-level sum at \(s=2\) and against the classical values \(\zeta(0)=-1/2\), \(\zeta'(0)=-\frac12\log(2\pi)\).

At fixed area, treating \(M\) as real, this has a single stationary point at \(M=A/(2e)\), and it is a *maximum* of \(\log\det'\lvert D\rvert\).  As a function of \((M,A)\) jointly it has no interior critical point.  Minimizing \(\det'\) instead of maximizing it sends \(M\to\infty\) and is useless as a selection principle.

Numbers: at the area \(A=6e\approx 16.30969097\) that places the continuous maximum at 3, the integer that maximizes \(\log\det'\lvert D\rvert\) is indeed \(M=3\), with \(\log\det'\lvert D\rvert=3/2\) exactly, and the neighbours are smaller (\(M=2\) gives \(\approx 1.4055\), \(M=4\) gives \(\approx 1.4246\)).  At unit area the preferred integer is \(M=1\), not 3.

**Verdict: dead end for uniqueness.**  The functional does not depend on \(\tau\), so it cannot fix the complex structure.  Placing its maximum at \(M=3\) is a choice of area, \(A=6e\), not a derivation of 3.  Combined with a volume term in the spectral action one might hope to freeze the density \(M/A\), but that still leaves a one-parameter family, and the heat-kernel / spectral-action analysis of doc 48 already prefers smaller \(\lvert M\rvert\).

### 3.3 Zero-mode counts on the magnetized orbifold \(T^2/\mathbb{Z}_4\)

The only modulus in the standard fundamental domain for which \(T^2\) admits a \(\mathbb{Z}_4\) rotation is \(\tau=i\).  That is a genuine compatibility condition with the conoid’s \(C_4\).  The \(M\) magnetized zero modes then transform under the modular \(S\)-action, which at \(\tau=i\) is that rotation, by the unitary discrete Fourier matrix

\[
  C_{jk}=M^{-1/2}\exp(2\pi i\, jk/M).
\]

The matrix is unitary to \(\sim 10^{-15}\) and satisfies \(C^4=I\) to \(\sim 10^{-14}\).  Projector traces give the dimension of each charge sector \(\eta\in\{1,i,-1,-i\}\).  For vanishing Scherk–Schwarz phases, the counts for \(M=1,\ldots,24\) agree exactly with Kobayashi–Nagamoto, Phys. Rev. D 96 (2017) 096011, Table III (arXiv:1709.09784).  In particular the invariant (\(\eta=+1\)) count is \(\lfloor M/4\rfloor+1\).

A 3-dimensional *invariant* sector occurs for \(M=8,9,10,11\), not for a unique flux, and not for \(M=0\) or \(M=3\) (which has a single invariant mode).  Other sectors have dimension 3 on other ranges (for example \(\eta=i\) at \(M=11,12,13,14\)).  Abe et al., Nucl. Phys. B 890 (2015), Table 6, record a similar range for Scherk–Schwarz phases \(\alpha=(1/2,1/2)\) (the \(+1\) sector has dimension 3 at \(M=10,11,12,13\)); that table was not recomputed here.

**Verdict: dead end for uniqueness; usable as a construction once \(M\) is chosen.**  The orbifold redistributes \(M\) modes; it does not produce the integer 3 from the geometry alone.  Getting three invariant generations still requires a choice of flux in a short list.  That is better bookkeeping than an unprojected flux \(M=3\), not a derivation.

### 3.4 The \(C_4\)-equivariant index of the locked conoid

The isometry is the translation \((u,v)\mapsto(u,v+k\pi/2)\) with \(v\sim v+2\pi\).  This has a fixed point if and only if \(k\equiv 0\pmod{4}\).  The four tip nodes, at \(u=0\) and \(v=\pi/4+m\pi/2\), are cycled by the generator (the cycle is \((0\,1\,2\,3)\)), so none is fixed.  The action is free on the truncated and on the complete conoid.  (The \(R^3\) embedding sends all four nodes to the origin; the fixed-point question is asked intrinsically.)

A free action has vanishing Lefschetz numbers for every non-identity element.  The identity contributes the locked ordinary APS index, which is 0.  Every character-valued index is therefore 0.  Equivalently, the index on the quotient is 0.

**Verdict: dead end.**  Equivariant index theory on the conoid does not produce three generations.

---

## 4. Broader survey, with verdicts

The headings below include mechanisms that were not implemented as new code in this note.  Verdicts are *promising*, *untested*, or *dead end*, always with respect to *deriving* the flux, the moduli, or the generation count from the locked geometry or from a precisely stated extra principle.  “Promising” does not mean “already derived”.

### Index theory and \(K\)-theory

- *Ordinary APS index on the truncated conoid, and the tip.*  Already computed: index 0, not 3 (docs 44, 46).  **Dead end.**
- *\(C_4\)-equivariant / orbifold index on the conoid.*  Computed in §3.4: all characters vanish.  **Dead end.**
- *Index on a compact surface, or on \(T^2\) or \(S^2\) with a line bundle or monopole.*  The index equals the degree or the flux, which is a choice (doc 47; CIM, JHEP 05 (2004) 079).  No connected compact surface has Euler characteristic 3.  **Dead end** as a derivation of 3.
- *Magnetized \(T^2/\mathbb{Z}_4\).*  Computed in §3.3.  **Dead end for uniqueness**; a construction after a choice of \(M\).
- *NCG classification, KO-dimension, Barrett, Dungen–van Suijlekom.*  Chamseddine–Connes, “Why the Standard Model”, arXiv:0706.3688, classify irreducible finite real spectral triples of KO-dimension 6: the algebra is a real form of \(M_k(\mathbb{C})\oplus M_k(\mathbb{C})\), and with a quaternion-linearity hypothesis the Standard Model algebra is singled out at \(k=4\) (16 fermions *per generation*).  The same paper states that the number of generations is still an input.  Barrett (hep-th/0608221) independently arrived at KO-dimension 6, for a Lorentzian reason; that fixes the finite *algebra*, not \(N=3\).  A later survey of Chamseddine and van Suijlekom (arXiv:1904.12392) likewise treats the uniqueness of the finite geometry at low energy, and of Pati–Salam at high energy, without deriving \(N=3\).  I did not find, in the sources consulted for this note, a theorem of Dungen–van Suijlekom (or of Connes) that derives three generations from \(K\)-theory.  **Dead end for the generation count**; already useful for the choice of finite algebra.

### Modular forms, modular invariance, and arithmetic geometry

- *\(\mathrm{SL}(2,\mathbb{Z})\) identification of \(\tau\).*  This only says that \(\tau\) may be taken in a fundamental domain.  It does not pick a point.  **Dead end** by itself.
- *Extremizing a modular-invariant spectral invariant (\(\det'\Delta\), the Kronecker height, \(\sqrt{\operatorname{Im}\tau}\,|\eta(\tau)|^2\)).*  Computed in §3.1.  **Promising for \(\tau\)** (hexagonal), not for the area or the flux, and in conflict with \(C_4\).
- *\(C_4\) compatibility.*  The unique point of the fundamental domain whose torus has a \(\mathbb{Z}_4\) automorphism is \(\tau=i\).  **Promising for \(\tau\)** under that extra symmetry assumption, in conflict with \(\det'\)-maximization, and silent about the area and the flux.
- *CM points and class numbers.*  The two elliptic points \(\tau=i\) and \(\tau=e^{2\pi i/3}\) are the most distinguished CM points (class number one, the Gaussian and Eisenstein integers).  This is the same pair already selected by the two mechanisms above, not a third independent principle, and it does not decide between them.  Using the lemniscate in the RH proof as a reason to set \(\tau=i\) here would be numerology.  **Untested as a physical principle**; **dead end** as an independent derivation.

### Representation theory and flavor symmetries

Finite groups with a 3-dimensional irrep (\(A_4\), \(S_4\), \(\Delta(27)\), …) are widely used in flavor model building *after* three generations are assumed.  Choosing a group because it has a 3-dimensional irrep puts the integer 3 in by hand.  The conoid’s isometry group is \(C_4\), whose irreducible representations are all 1-dimensional; McKay correspondence for a cyclic subgroup of \(\mathrm{SU}(2)\) does not produce a preferred 3.  **Dead end**, and numerology if used only to match the count 3.

### Algebraic geometry (Calabi–Yau, del Pezzo)

In the heterotic string, the net number of generations can be \(\lvert\chi\rvert/2\) of a Calabi–Yau threefold.  That is a genuine, classical mechanism (the Tian–Yau manifold with \(\chi=-6\) is the textbook example).  It does not use the locked conoid, and it would *replace* the magnetized-surface factor by a different compactification, not fix the flux on \(T^2\).  Del Pezzo surfaces similarly appear in some F-theory or heterotic constructions; they are not the conoid.  **Untested as a SAM-3 extension**; **dead end** as a derivation from the locked geometry.  Building a different model around a CY with \(\chi=\pm 6\) would be a change of programme, and would still require an honest check that the conoid (or some 4D spacetime) can be coupled to it.

### Topology, characteristic classes, Chern–Simons levels, anomalies

Dirac quantization already forces the flux to be an integer; it does not force the integer 3.  Anomaly cancellation and tadpole conditions can constrain fluxes in string compactifications, typically once a background (a CY, a number of D-branes, an Euler characteristic) has been chosen.  No such tadpole was found that isolates \(M=3\) on conoid \(\times T^2\times F\).  A Chern–Simons level of 3 is likewise a choice.  **Untested** in detail on this product, and there is no present reason to expect uniqueness.

### Spectral theory, trace formulae, positivity, Selberg

The spectral action on the magnetized torus was already tested in doc 48 and prefers smaller \(\lvert M\rvert\).  **Dead end** for \(M=3\).  The fluxed Dirac determinant of §3.2 is **dead end** for uniqueness.  The unfluxed Laplacian determinant of §3.1 is **promising for \(\tau\)**.  Selberg’s trace formula applies to compact hyperbolic surfaces, not to the conoid (non-constant \(K\le 0\), non-compact) and not to a flat torus.  **Dead end.**  Weil positivity and Connes’ adele-class trace formula are about RH, not about the flux.  **Dead end** for this problem.

### Variational principles, spectral action, torsion

See doc 48 and §3.2.  Without putting the integer 3 into the functional (for example by tuning the area), the obvious spectral functionals do not have a unique minimum at \(M=3\).  Torsion or a change of cutoff function was not exhaustively scanned; nothing in the heat-kernel expansion suggests a distinguished integer 3.  **Dead end** for the functionals tested; **untested** for an as-yet-unwritten functional that is actually derived from the geometry.

### Moduli stabilization (flux compactification, KKLT and related)

In string theory, 3-form fluxes can stabilize complex-structure moduli of a Calabi–Yau, typically by *choosing* a flux lattice vector, not by deriving a unique small integer such as 3.  The magnetized-torus Dirac spectrum is independent of \(\tau\), so a flux \(M\) on \(T^2\) does not stabilize \(\tau\) by itself (consistent with §3.2).  **Untested** as a direct application here, and not presently applicable in its standard form (there is no CY 3-form flux on this product).  **Dead end** as a source of unique \(M=3\).

### Number theory beyond the determinant

Zeta-regularized determinants are the content of §§3.1–3.2.  No other number-theoretic identity was found that forces the flux to be 3.  **Dead end** for the generation count, except insofar as §3.1 fixes \(\tau\).

### Covers, nodes, and other numerology

A 3-sheeted cover, or an appeal to the four nodes or twelve bridges of the conoid, puts the desired integer in by hand or matches the wrong integer (4, not 3).  **Dead end**; numerology.

### The AI-plus-Lean workflow

**Promising as a process, not as a principle.**  Formalizing the locked core in Lean, and then searching for a uniqueness theorem for the flux or the moduli, would be the analogue of Alpöge’s workflow.  It cannot replace the missing mathematical principle: Lean will certify a theorem only once there is one.  No Lean formalization of SAM-3 was started in this note.

---

## 5. Ranked candidates

1. **Extremize \(\det'\Delta\) among unit-area flat tori** — *promising for \(\tau=e^{2\pi i/3}\)*; classical; does not fix area or flux; conflicts with \(C_4\).
2. **Require a \(C_4\) isometry compatible with the conoid** — *promising for \(\tau=i\)*, and for considering \(T^2/\mathbb{Z}_4\); an extra symmetry assumption, not a consequence of the spectral action; silent about area and flux; conflicts with (1).
3. **Magnetized \(T^2/\mathbb{Z}_4\) zero-mode counts** — *dead end for uniqueness*, but the right bookkeeping if (2) is adopted and a flux is then chosen from the short list that gives a 3-dimensional sector (\(M=8,9,10,11\) in the invariant sector, for \(\alpha=0\)).
4. **NCG classification of the finite algebra** — already used; *dead end for \(N=3\)*, which remains an input; *promising* only in the weaker sense that it continues to constrain the internal space (CCM / Pati–Salam).
5. **Fluxed Dirac \(\det'\) or the spectral action** — *dead end* for unique \(M=3\) and for \(\tau\) (spectrum independent of \(\tau\); spectral action prefers small \(\lvert M\rvert\); \(\det'\) at fixed area only ties \(M\) to \(A\)).
6. **\(C_4\)-equivariant index on the conoid** — *dead end* (all characters 0).
7. **Calabi–Yau \(\lvert\chi\rvert/2=3\)** — a real mechanism in a *different* programme; *untested* here; *dead end* as a derivation from the locked conoid.
8. **Anomaly / tadpole / Chern–Simons / KKLT-style flux stabilization** — *untested* in detail and not presently adapted to this geometry; no evidence they isolate 3.
9. **Flavor groups, McKay, 3-covers, node-counting** — *dead end* / numerology.
10. **AI-plus-Lean search** — *promising as a workflow* once a candidate uniqueness statement exists.

The one structural finding that is new, relative to docs 47–48, is the **conflict between (1) and (2)**.  Two honest, classical principles fix \(\tau\), and they fix it to two different values.  Neither fixes the flux or the area.  The integer 3 is still not derived.

---

## 6. Reproduce

```bash
python experiments/missing_principle/report.py
pytest -q tests/test_missing_principle.py
```

The locked core, and the tests of docs 44–48, are unchanged.
