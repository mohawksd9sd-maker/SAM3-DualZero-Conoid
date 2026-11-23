# 50. Further candidate tests: looking for an accidental fit

**Date:** 23 November 2026 (America/Chicago)  
**Status:** exploratory; not part of the locked core.  
**Code:** `experiments/further_candidates/`  
**Tests:** `tests/test_further_candidates.py`  
**JSON:** `reproducibility/further_candidates_report.json`

Honesty rule: unproven statements are labelled.  Null results stay null.  A “fit” is counted only if three generations, or a unique modulus, comes out with no parameter chosen to make it so.  Near-misses are reported as near-misses.  Citations are from sources consulted for this note.

This is a sequel to docs 47–49.  The question is whether some standard construction — a Calabi–Yau or toroidal orbifold, a tadpole constraint, a different \(T^2/\mathbb{Z}_N\), a spectral action that includes the tip, or a numerical coincidence with the recorded SAM-3 constants — *accidentally* isolates the integer 3 or fixes the surface moduli, without hand tuning.

It does not.  The bottom line of [`BOTTOM_LINE.md`](../../BOTTOM_LINE.md) is unchanged.

---

## 1. Calabi–Yau and toroidal-orbifold Euler characteristics

The net generation count of a Calabi–Yau threefold, with the spin connection embedded in the gauge group, is \(\lvert\chi\rvert/2\) (Dixon–Harvey–Vafa–Witten, Nucl. Phys. B 261 (1985) 678–705, and the standard embedding of the heterotic string).

The stringy Euler characteristic of an orbifold \(M/G\) was computed here from the DHVW formula

\[
  \chi=\frac1{|G|}\sum_{gh=hg}\chi\bigl(\mathrm{Fix}(g)\cap\mathrm{Fix}(h)\bigr)
\]

for two classical examples, and matches the textbooks:

- \(T^6/\mathbb{Z}_3\) (the Z-manifold: three hexagonal tori, 27 fixed points of a non-identity element): \(\chi=72\), so 36 generations.
- \(T^6/(\mathbb{Z}_2\times\mathbb{Z}_2)\) (the standard action that flips two tori at a time): \(\chi=96\), so 48 generations.

Hodge numbers of the standard abelian \(T^6\) orbifolds (point group plus lattice) were taken from Reffert, hep-th/0609040, Tables 2.3–2.4, and the same table in Lüst–Reffert–Scheidegger–Stieberger, hep-th/0609014, Table 2.1.  For each row, \(\chi=2(h^{1,1}-h^{2,1})\) was computed, and \(\lvert\chi\rvert/2\) recorded.  There are 26 entries in that table.  **None has \(\lvert\chi\rvert/2=3\).**  The generation counts that occur are 24, 36, 48, 60, 72, 84 and 90.  The smallest value in the table is 24.

The entries whose point group contains a \(\mathbb{Z}_4\) (so that at least one torus must admit a \(C_4\) rotation, and therefore have \(\tau=i\)) are the three \(\mathbb{Z}_4\) orbifolds, the \(\mathbb{Z}_8\) and \(\mathbb{Z}_{12}\) orbifolds, \(\mathbb{Z}_2\times\mathbb{Z}_4\), and \(\mathbb{Z}_4\times\mathbb{Z}_4\).  Their generation counts are 24, 60 or 90, never 3.  In particular, every \(\mathbb{Z}_4\) entry has \(\chi=48\) and 24 generations.  Compatibility with the conoid’s \(C_4\) is possible, and it does not yield 3.

The Tian–Yau manifold does have three generations (\(\chi=-6\)), as a free \(\mathbb{Z}_3\) quotient of a complete-intersection Calabi–Yau with \(\chi=-18\).  That is a genuine construction in a *different* programme.  It does not use the locked conoid, and it uses a \(\mathbb{Z}_3\), not the conoid’s \(C_4\).  Combining the two by hand would be a change of model, not an accidental fit of SAM-3.

A magnetized \(T^2\times T^2\times T^2\) has Dirac index \(M_1 M_2 M_3\).  The only positive solutions with each \(\lvert M_i\rvert\le 10\) and product 3 are the permutations of \((1,1,3)\).  The 3 is an input.

**Verdict: dead end** as a derivation from the locked geometry, or from the standard abelian orbifolds together with \(C_4\).  Tian–Yau is a known 3-generation construction, not a SAM-3 fit.

---

## 2. Anomaly / tadpole constraints

The Type I RR tadpole conditions used here are those written as display (14) in Marchesano–Shiu, arXiv:hep-th/0409132:

\[
  \sum_\alpha N_\alpha n_\alpha^1 n_\alpha^2 n_\alpha^3=16,\qquad
  \sum_\alpha N_\alpha m_\alpha^1 m_\alpha^2 n_\alpha^3=-16,
\]

and the two cyclic magnetic counterparts.  The chiral index of two stacks is \(I_{ab}=\prod_i(n_a^i m_b^i-n_b^i m_a^i)\).  These equations are extra input from Type I string theory, not a consequence of the conoid.  A full string model also needs orientifold images, K-theory charges, and a SUSY angle condition that involves the unknown Kähler moduli; those are not solved here.

An exhaustive small-integer search was run:

- One stack, wrapping numbers \(\lvert n\rvert,\lvert m\rvert\le 4\), \(N\in\{1,2,4,8,16\}\): **no solutions**.
- One magnetized stack plus a filling stack of pure D9-branes, same bounds: **no solutions**.
- Two stacks, wrapping numbers \(\lvert n\rvert,\lvert m\rvert\le 1\), \(N\in\{1,2,3,4,8,16\}\): **384 solutions, all with \(I_{12}=0\)**.

So in this window the tadpoles can be satisfied, but only by non-chiral configurations.  A pairwise \(\lvert I\rvert=3\) is neither forced nor even realized.  (That all realized indices were even is consistent with a known observation, in the \(B=0\) Type I analysis cited in JHEP 02 (2001) 030, that some of these constructions force an even generation number; the search is too small to promote that observation to a theorem here.)

Larger wrapping, a nonzero NS \(B\)-field, or more stacks can *allow* three-generation models in the literature (that is the point of turning on \(B=1/2\) in those papers).  Allowed is not forced, and none of those constructions is derived from the conoid.

**Verdict: dead end** for uniqueness.  The tadpoles are not a SAM-3 principle, and in the search they do not isolate 3.

---

## 3. Magnetized \(T^2/\mathbb{Z}_N\) for \(N=2,3,4,6\)

Zero-mode counts, with vanishing Scherk–Schwarz phases:

- \(\mathbb{Z}_2\) (any \(\tau\), compatible with \(C_4\)): computed from the permutation \(\psi^j\mapsto\psi^{M-j}\).  The counts match Kobayashi–Nagamoto, Phys. Rev. D 96 (2017) 096011, Table 1, for \(M=1,\ldots,24\).  Invariant dimension \(\lfloor M/2\rfloor+1\).  At \(M=1\) this is 1, not 3.  A 3-dimensional invariant sector occurs at \(M=4,5\).
- \(\mathbb{Z}_4\) (\(\tau=i\), \(C_4\) compatible): independent DFT computation of doc 49, matching their Table III.  At \(M=1\) the invariant count is 1.  A 3-dimensional invariant sector occurs at \(M=8,9,10,11\).
- \(\mathbb{Z}_3\) (hexagonal \(\tau\), not \(C_4\) compatible): literature formulae, Table 5 and eq. (89), for even \(M\).  The invariant count is \(2\lfloor M/6\rfloor+1\), which is *not* \(\lfloor M/3\rfloor+1\) at \(M=6n+4\).  At the smallest even flux \(M=2\) the invariant count is 1.  A 3-dimensional invariant sector occurs at even \(M=6,8,10\).
- \(\mathbb{Z}_6\) (hexagonal \(\tau\), not \(C_4\) compatible): literature formulae, Table VII.  The invariant count is \(\lfloor M/6\rfloor+1\).  At \(M=2\) this is 1.  A 3-dimensional invariant sector occurs at even \(M=12,14,16\) (and 17 if odd \(M\) is included).  The six sector formulae sum to \(M\) for even \(M=2,\ldots,30\).

The “minimal positive flux” principle gives one invariant mode, not three, in every \(C_4\)-compatible case.  Asking for the smallest \(M\) *such that a sector has dimension 3* does produce a short list, but that asks for 3 in advance, and the list is a range, not a unique flux.  Scherk–Schwarz phases and discrete Wilson lines, as the same paper notes, can change the counts; that adds more choices, it does not remove the ones already present.

**Verdict: dead end for uniqueness.**  Usable bookkeeping once a flux is chosen, as already concluded for \(\mathbb{Z}_4\) in doc 49.

---

## 4. Spectral action on the truncated product, including the tip

The 4D product \(Y=X_{a,b}\times T^2\) has, from doc 48,

\[
  \mathrm{vol}(Y)=\mathrm{Area}(X)\,A,\qquad
  \int_Y R=A\int_X R_X,\qquad
  \int_Y\lvert F\rvert^2=\mathrm{Area}(X)\,(2\pi M)^2/A,
\]

with \(\int_X R_X\to-4\pi\) and \(\mathrm{Area}(X)\sim\pi b^2+C_0\) on the unit metric, \(C_0=2\pi\ln 2\).  The tip is a geodesic boundary of length \(8\ell_0\) (doc 46); the leading boundary Seeley term is proportional to \(\mathrm{vol}(\partial Y)=(L_{\mathrm{tip}}+L_{\mathrm{outer}})A\).  The four nodes are not assigned an invented contribution.  The fluxed Dirac spectrum is independent of \(\tau\).

The Wilson coefficients \(f_4,f_2,f_0,f_{\partial}\) and the cutoff \(\Lambda\) are **not derived from the conoid**.  They are left as explicit inputs.  Two functionals were studied: the truncated action at finite outer radius \(b\), and the finite-part action that retains only \(C_0\), \(\int R\), the flux term built from \(C_0\), and the tip.

In both cases, \(\partial S/\partial M\propto f_0\,\mathrm{Area}(X)\,M/A\) vanishes only at \(M=0\), unless the Yang–Mills coefficient is tuned to zero.  There is no interior extremum that selects \(M=3\).  At fixed \(M\neq 0\) a stationary area can exist, but it is proportional to \(\lvert M\rvert\) and depends on the underived coefficients and on \(\Lambda\).  At \(M=0\) the action is linear in \(A\): either \(A\) is driven to a boundary, or the linear coefficient is tuned to zero and \(A\) is a flat direction.  The tip term \(8\ell_0 A\) shifts that linear coefficient and does not create a preferred integer flux.  \(\tau\) does not enter.

**Verdict: dead end** for unique \(M=3\) or a unique area.  (The earlier Kronecker/\(\det'\Delta\) mechanism of doc 49 remains the one way, among these functionals, to fix \(\tau\), and it still conflicts with \(C_4\).)

---

## 5. Numerical coincidences

A predeclared list of 15 source constants (locked geometric numbers, plus \(F(i)\), \(F(e^{2\pi i/3})\), \(\lvert\eta(i)\rvert\), and \(1/(2e)\) from docs 49–50) was closed before the comparison.  The integer 13 is not a source, because it appears only inside the underived exponent \(4/13\).  The recorded (also underived) scale \(D=2\pi/12\) is included and flagged.  From these sources, 347 simple combinations (the numbers, reciprocals, square roots, logs, two-term ratios, and, flagged, ratios raised to the input power \(4/13\)) were compared to three targets: the quoted \(\omega_0\approx 0.927\), the exponent \(4/13\), and the integer 3.  That is 1,041 comparisons.  A hit was a relative error below 0.5%, or, for the three-digit target 0.927, an absolute error below 0.001.

Hits, all labelled coincidences:

- \((\pi/4)^{4/13}\approx 0.92837\) versus \(\omega_0\approx 0.927\) (relative error \(0.15\%\)).  This uses the underived exponent \(4/13\) as a probe, and the 4 is the number of nodes (or the order of \(C_4\)).  It is close to the already-recorded remark, in doc 42, that 0.927 would require a ratio \(R/D\approx 0.7816\) (and \(\pi/4\approx 0.7854\)).  It is not a derivation of \(\omega_0\) or of \(4/13\).
- The same number again, with \(C_4\) in place of the node count.
- \(\bigl(F(e^{2\pi i/3})/\lvert\eta(i)\rvert\bigr)^{4/13}\approx 0.92508\) versus 0.927 (relative error \(0.21\%\)).  Again the exponent is an input.
- \(\bigl(1/(2e)\bigr)/F(e^{2\pi i/3})\approx 0.30839\) versus \(4/13\approx 0.30769\) (relative error \(0.23\%\)).  This one does *not* put \(4/13\) into the expression.  It is the closest unforced proximity in the list: the magnetized-determinant density of doc 49, divided by the hexagonal Kronecker function, is numerically close to the recorded exponent.  It is still a coincidence in a 1,041-comparison search, and there is no principle here that produces the exponent.

Near-misses (relative error below 2%, not hits): \(8/e\approx 2.943\) versus 3 (the tip length over \(e\), 1.9%); \(4/C_0\approx 0.918\) versus 0.927; and a handful of other ratios.  There was no exact hit on the integer 3.

**Verdict: no derivation.**  The look-elsewhere count is 1,041.  The three-digit target 0.927 is a loose target.  None of these proximities is promoted to a claim.

---

## 6. Ranked list

| # | Candidate | Result | Why |
|---|-----------|--------|-----|
| 1 | Standard abelian \(T^6\) orbifolds, \(\lvert\chi\rvert/2\) | **Dead end** | 26 entries, none give 3; smallest is 24.  DHVW checks: \(\mathbb{Z}_3\) gives 36, \(\mathbb{Z}_2\times\mathbb{Z}_2\) gives 48. |
| 2 | The same, restricted to \(C_4\)-compatible point groups | **Dead end** | \(\mathbb{Z}_4\) gives 24; others give 24, 60 or 90. |
| 3 | Tian–Yau \(\chi=-6\) | **Not a SAM-3 fit** | A real 3-generation construction in a different programme, using a free \(\mathbb{Z}_3\), not the conoid. |
| 4 | Magnetized \(T^2\times T^2\times T^2\), index \(M_1 M_2 M_3\) | **Dead end** | Equals 3 only for permutations of \((1,1,3)\). |
| 5 | Type I tadpoles (Marchesano–Shiu (14)), small wrapping | **Dead end** | 3 is not forced; in the search it is not even realized (\(I=0\) or no solution). |
| 6 | \(T^2/\mathbb{Z}_N\) zero modes, \(N=2,3,4,6\) | **Dead end for uniqueness** | Minimal flux gives 1 invariant mode; a 3-dimensional sector appears only after choosing \(M\) in a range. |
| 7 | Spectral action on conoid \(\times T^2\), including the tip | **Dead end** | \(\partial S/\partial M=0\) only at \(M=0\); a stationary area, if it exists, is proportional to \(\lvert M\rvert\) and depends on underived coefficients.  \(\tau\) does not enter. |
| 8 | Kronecker \(\det'\Delta\) / \(C_4\) conflict for \(\tau\) | *(already in doc 49)* | Still the only promising mechanisms for \(\tau\), and they still disagree.  Not re-opened as a new fit. |
| 9 | Numerical coincidences with \(\omega_0\), \(4/13\), and 3 | **Coincidences, not fits** | 1,041 comparisons; the closest unforced proximity is \(\bigl(1/(2e)\bigr)/F(\rho)\approx 4/13\) at 0.23%.  Look-elsewhere applies. |

---

## 7. Reproduce

```bash
python experiments/further_candidates/report.py
pytest -q tests/test_further_candidates.py
```

The locked core, and the tests of docs 44–49, are unchanged.
