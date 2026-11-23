# 47. Alternative surfaces and internal spaces (exploratory)

**Date:** 23 November 2026 (America/Chicago)  
**Status:** Exploratory survey.  **Not part of the locked SAM-3 core.**  
**Code:** `experiments/alt_geometries/`  
**Tests:** `tests/test_alt_geometries.py`  
**Reproduction:** `python experiments/alt_geometries/report.py` (writes `reproducibility/alt_geometries_report.json`) and `pytest -q tests/test_alt_geometries.py`.

Honesty rule: unproven statements are labelled.  Null results stay null.  Citations were fetched and checked; nothing here is an invented derivation.  Number-matching that is only a count is flagged as numerology.

The locked core (right-conoid metric \(f=\sqrt{u^2+4\ell_0^2\cos^2(2v)}\), \(C_0=2\pi\ln 2\), exact \(E_0(m)\), APS index \(0\) of the untwisted Dirac operator on the truncated conoid, singular tip as a geodesic boundary of length \(8\ell_0\)) is unchanged.  Docs 44–46 still stand.

---

## Question

The locked conoid does not produce three chiral generations, a gauge group, unique mass ratios, or coupling unification (docs 44–46).  This survey asks whether a *different* surface or internal space can, and whether any such structure is forced by the conoid itself.

---

## 1. Surfaces that could give three generations

### 1.1 Twisted Dirac on a compact Riemann surface

**Facts used (standard, not re-proved).**  Riemann–Roch: for a holomorphic line bundle \(L\) of degree \(d\) on a compact Riemann surface of genus \(g\),

\[
\chi(L)=\dim H^0(L)-\dim H^1(L)=d+1-g.
\]

A spin structure is a theta characteristic \(S\) (so \(\deg S=g-1\)).  The index of the Dirac operator twisted by a holomorphic line bundle of degree \(d\) is

\[
\chi(S\otimes L)=\deg(S\otimes L)+1-g=d.
\]

The chiral index equals the degree (the flux) and is **independent of genus**.

**Is 3 natural or a choice?**  A choice of degree.  For every genus, Dirac index \(3\) means \(d=3\).

Additional negatives, to avoid numerology:

- No *connected* compact surface, orientable or not, with or without boundary, has Euler characteristic \(3\).  The maximum is \(2\) (the sphere).  (A disjoint union such as sphere \(\sqcup\) disk has \(\chi=3\), but that is not a connected base and is not a derivation.)
- The Hopf line bundle \(O(1)\) on \(\mathbb{CP}^1\) has degree \(1\), hence Dirac index \(1\), not \(3\).
- \(O(2)=TS^2\) has degree \(2\), hence Dirac index \(2\).  It does have \(\chi(O(2))=3\): these are the three holomorphic sections of the tangent bundle, i.e. the conformal Killing fields of the sphere (the Lie algebra of \(\mathrm{PSL}(2,\mathbb{C})\)).  Those are vector fields, not chiral fermion zero modes.  Identifying them with generations is numerology.

**Verdict:** *neutral* as a mechanism (index \(=\) flux is clean); *dead end* as a derivation of the number \(3\).

### 1.2 Magnetized torus

**Literature.**  Cremades–Ibáñez–Marchesano, JHEP 05 (2004) 079, hep-th/0404229 (CIM).  On \(T^2\) with integer flux \(M\), the Dirac index is \(M\): there are \(|M|\) zero modes of one chirality and none of the other (CIM §3.1.2, and the standard Atiyah–Singer evaluation).  Wavefunctions and normalisation: CIM (3.35) and (3.44).  Yukawa couplings are overlap integrals of those wavefunctions and depend on the complex structure \(\tau\) and on Wilson lines (CIM abstract).

**Is 3 natural or a choice?**  A choice of flux.  Dirac quantization only forces \(M\in\mathbb{Z}\); the smallest positive integer is \(1\).

**Computed Yukawas.**  For two fermion stacks of flux \(3\) and a Higgs stack of flux \(6\) (the unique additive assignment that gives three zero modes on both fermion stacks), the Yukawa is a \(3\times 3\times 6\) tensor: six Higgs zero modes, each giving a \(3\times 3\) matrix.  Taking a single Higgs slice is an extra choice.  Overall scale is absorbed into the Higgs vev; only singular-value ratios are compared to data.

Charged-lepton pole-mass ratios (PDG 2024, comparison data, not a fit target):

\[
\frac{m_\mu}{m_e}\approx 206.768,\qquad \frac{m_\tau}{m_e}\approx 3477.23,\qquad \frac{m_\tau}{m_\mu}\approx 16.817.
\]

Sample singular-value ratios from the CIM wavefunctions (zero relative Wilson lines unless stated):

| moduli | Higgs slices (alternating pair) | ratios (ascending) |
|--------|----------------------------------|--------------------|
| \(\tau=i\) | even / odd | \(1:1:8.105\) and \(1:32.97:32.97\) |
| \(\tau=2i\) | even / odd | \(1:1:65.94\) and \(1:2174:2174\) |
| \(\tau=0.5i\) | even / odd | \(1:1:2.732\) and \(1:4.068:4.068\) |
| \(\tau=e^{i\pi/3}\) | even / odd | \(1:1:6.160\) and \(1:18.81:18.81\) |
| \(\tau=i\), relative Wilson lines \(\zeta_I=0\), \(\zeta_J=0.2\), \(\zeta_K=0.1+0.15i\) | two patterns | \(1:8.153:18.67\) and \(1:3.854:10.64\) |

A common translation of all three stacks does not change the ratios.  Relative Wilson lines between stacks lift the two-fold degeneracy, as they should.  In every sample the ratios depend on the remaining moduli, and none is the charged-lepton hierarchy (which has three well-separated, non-degenerate masses with a much larger span).  These are samples, not predictions.  A dedicated fit of \(\tau\) and the Wilson lines could no doubt get closer; that would be a fit, not a derivation, and nothing in the conoid fixes those moduli.

Orthonormality of the CIM zero modes was checked to \(\max\|G-I\|<10^{-12}\) on a \(24\times 24\) grid for \(N=1,2,3\) and several \(\tau\).

**Verdict:** *neutral* as a mechanism (index \(=\) flux is standard and clean); *dead end* as a derivation of the number \(3\) or of unique mass ratios.

### 1.3 Conoid variants (frequency \(n\), caps, “closed” surfaces)

The embedding family that keeps the spirit of the locked right conoid is

\[
r_n(u,v)=\bigl(u\cos v,\ u\sin v,\ \ell_0\sin(nv)\bigr),
\]

with induced metric \(f_n=\sqrt{u^2+n^2\ell_0^2\cos^2(nv)}\).  For \(n=2\) this is exactly the locked metric (a consistency check, not a replacement).

Computed and proved in this family:

| quantity | value | equals 3? |
|----------|-------|-----------|
| Isometry | \(C_{2n}\) (\(v\mapsto v+\pi/n\)) | no (\(2n\ne 3\)) |
| Tip nodes | \(2n\) | no |
| Tip-circle length | \(4n\ell_0\) | no (for integer \(n\)) |
| Gaussian curvature | \(K=-n^2\ell_0^2\cos^2(nv)/f_n^4\) | — |
| Complete total curvature | \(\int K\,dA=-2\pi\), independent of \(n\) | \(\lvert\int K\rvert/2\pi=1\), not 3 |
| Untwisted APS index on \([a,b]\times S^1\) (bounding spin structures) | \(0\), independent of \(n\) and of the metric | no |

Setting \(n=3\) because one wants three generations only changes the isometry to \(C_6\) and the node count to \(6\); the index stays \(0\).  That is a name, not a derivation.

**Closed or capped surfaces.**  The metric completion at \(u=0\) is still a geodesic circle (now of length \(4n\ell_0\)) with \(2n\) metric-degeneracy points, not a cone (same analysis as doc 46).  Collapsing the tip to a point is not isometric.  A smooth disk cap is not uniquely determined by the embedding, because the metric on the tip circle degenerates at the nodes.  If one nonetheless produces a smooth sphere or a torus, the untwisted Dirac index is \(0\), and index \(3\) still requires a degree-\(3\) twist.  The node count is \(2n\), never \(3\).

**Verdict:** *dead end* for the generation count, and for a unique closed conoid-like surface.

---

## 2. Internal spaces

### 2.1 CCM classification (recorded, not re-proved)

**Literature.**  Chamseddine–Connes, J. Geom. Phys. 58 (2008) 38–47, arXiv:0706.3688.  KO-dimension \(6\), the order-zero condition, irreducibility, and symplectic linearity lead to an algebra of the form \(M_a(\mathbb{H})\oplus M_{2a}(\mathbb{C})\).  The case \(a=2\) that reproduces the known fermion quantum numbers, together with a grading, is the Pati–Salam algebra \(\mathbb{H}_R\oplus\mathbb{H}_L\oplus M_4(\mathbb{C})\).  The first-order condition then selects the maximal subalgebra \(\mathbb{C}\oplus\mathbb{H}\oplus M_3(\mathbb{C})\).  The generation multiplicity \(N\) is an input (“We will restrict ourselves to \(N=3\)”).

The “\(3\)” in \(M_3(\mathbb{C})\) is the colour algebra, coming from the first-order reduction of \(M_4(\mathbb{C})\).  It is not the generation count.  Identifying those two threes is a confusion, not a derivation.

None of the classification axioms is supplied by the locked conoid.  The almost-commutative product was already analysed in doc 45: the raw product conoid \(\times F\) is two-dimensional.

**Verdict:** *neutral*.  Real constraints on the finite algebra, once one accepts the stated axioms; not a SAM-3 output.

### 2.2 Pati–Salam finite spectral triple

**Literature.**  Chamseddine–Connes–van Suijlekom, JHEP 11 (2013) 132, arXiv:1304.8050: dropping the first-order condition leaves \(\mathbb{H}_R\oplus\mathbb{H}_L\oplus M_4(\mathbb{C})\), with inner-automorphism group \(\mathrm{SU}(2)_R\times\mathrm{SU}(2)_L\times\mathrm{SU}(4)\), and one generation of fermions in \((2,1,4)+(1,2,4)\).  The SM algebra is the maximal first-order subalgebra.  The generation count is still an input.

Chamseddine–Connes–van Suijlekom, JHEP 11 (2015) 011, arXiv:1507.08161 (CCvS2015): one-loop unification of the three Pati–Salam couplings with an intermediate breaking scale \(m_R\), for several Dirac-operator scenarios.  A real singlet \(\sigma\) can make a \(125\,\mathrm{GeV}\) Higgs compatible and can stabilise the vacuum, with a relation involving \(\rho=m_t/m_\nu\) and the unification scale.  That is a literature result, not a unique mass prediction, and it does not use the conoid.

**One-loop reproduction (this repository).**  The matching relations and beta coefficients are taken from CCvS2015.  Standard Model running below \(m_R\) uses the CC2010 couplings at \(M_Z\) already in `code/ccm_oneloop_rge.py`, so the comparison with doc 45 is consistent; a residual against the CCvS2015 quoted scales from a different \(M_Z\) input is expected.

| scenario | \((b_R,b_L,b)\) | computed \(m_R\), \(\Lambda\) (CC2010 inputs) | CCvS2015 quote | relative \(\ln\) error |
|----------|-----------------|-----------------------------------------------|----------------|------------------------|
| composite / lepton–quark unification | \((7/3,\ 3,\ 31/3)\) | \(5.43\times 10^{13}\,\mathrm{GeV}\), \(3.05\times 10^{15}\,\mathrm{GeV}\) | \(4.25\times 10^{13}\), \(2.5\times 10^{15}\) | \(0.245\), \(0.198\) |
| \((1,1,15)\) not decoupled | \((7/3,\ 3,\ 9)\) | \(5.21\times 10^{13}\,\mathrm{GeV}\), \(7.35\times 10^{15}\,\mathrm{GeV}\) | \(4.1\times 10^{13}\), \(6.3\times 10^{15}\) | \(0.239\), \(0.154\) |

In both cases a unique \(m_R\) produces an exact triple meeting (spread in \(1/g^2\) at \(\Lambda\) is \(\sim 10^{-15}\)).  The \(\sim 20\%\)–\(28\%\) shift in the scales is the input-coupling residual, not a failure of the running.  At a point where \(g_R=g_L=g\), the matching reduces to the same relation \(g_3^2=g_2^2=\tfrac53 g_1^2\) as in CCM; the new content is the intermediate PS-running segment, which can make the three couplings meet.

**Verdict:** *promising* as a literature internal-space alternative to CCM (unification with an intermediate scale; Higgs mass compatible with \(125\,\mathrm{GeV}\) in the cited analysis).  *Dead end* as something derived from the conoid.  Generations remain an input.

### 2.3 \(C_4\), four nodes, twelve bridges

The locked isometry group is cyclic of order \(4\).  Over \(\mathbb{C}\) it has four one-dimensional irreps.  Its group algebra is \(\mathbb{C}\oplus\mathbb{C}\oplus\mathbb{C}\oplus\mathbb{C}\), with unitaries \(\mathrm{U}(1)^4\), not \(\mathbb{C}\oplus\mathbb{H}\oplus M_3(\mathbb{C})\) and not \(\mathbb{H}_R\oplus\mathbb{H}_L\oplus M_4(\mathbb{C})\).  An abelian isometry group does not produce a nonabelian gauge algebra by taking its irreps.

Flagged as numerology, not derivations:

- four tip nodes \(=\) four irreps of \(C_4\) (both sides are the order of the same cyclic group);
- the twelve-bridge labelling \(D=2\pi/12\) (a convention in STATUS) against \(3\times 4\).

**Verdict:** *dead end*.

---

## 3. Higher-dimensional products

KO-dimensions add.  The CCM fermionic setup wants total KO-dimension \(\equiv 2\pmod{8}\) (as in \(4+6=10\)).

| product | continuous dim | KO dim | 4D heat kernel? | generations |
|---------|----------------|--------|-----------------|-------------|
| conoid \(\times F\) | 2 | \(2+6\equiv 0\) | no | none (doc 45) |
| 4D manifold \(\times F\) | 4 | \(4+6\equiv 2\) | yes | \(N=3\) is an input |
| conoid \(\times T^2\times F\) | 4 | \(2+2+6\equiv 2\) | yes | flux \(M\) on \(T^2\); \(M=3\) is a choice |
| conoid \(\times S^2\times F\) | 4 | \(2+2+6\equiv 2\) | yes | degree \(d\) on \(S^2\); \(d=3\) is a choice |

**What fixes the flux?**  Nothing examined here:

- Dirac quantization gives \(M\in\mathbb{Z}\), not specifically \(3\);
- conoid total curvature \(\lvert\int K\rvert/2\pi=1\), not \(3\);
- four nodes or \(C_4\) give \(4\), not \(3\) (and \(4-1=3\) would be numerology);
- the Hopf bundle has degree \(1\); \(TS^2\) has degree \(2\);
- “the smallest integer that gives at least three zero modes” is circular.

The conoid, in these products, is a spectator \(2\)-factor.  It remains incomplete, with a geodesic tip boundary (doc 46), and it does not determine the flux on the other factor.

**Verdict:** *promising* as a way to reach a 4D heat kernel and the CCM KO-dimension; *dead end* as a derivation of the flux.

---

## 4. Ranked directions

1. **A 4D product with a magnetized compact surface, times a CCM or Pati–Salam finite triple** (for example conoid \(\times T^2_{\mathrm{flux}\,3}\times F\)).  *Promising as a package, with an explicit caveat.*  This is the only setup in the survey that is simultaneously four-dimensional and has a clean geometric mechanism for exactly three chiral zero modes — namely a chosen integer flux or bundle degree equal to \(3\).  Gauge content and coupling relations then come from \(F\), not from the conoid.  The number \(3\) itself is still a choice, and Yukawa mass ratios depend on moduli that are not fixed.

2. **Pati–Salam finite spectral triple as the internal space.**  *Promising as a literature alternative; not derived from the conoid.*  One-loop unification with an intermediate \(m_R\) reproduces (to the input-coupling residual above) the CCvS2015 numbers.  The Higgs mass can be compatible with \(125\,\mathrm{GeV}\) in the cited analysis, unlike the CC2010 CCM example of \(\sim 170\,\mathrm{GeV}\).  The generation count is still an input.

3. **CCM finite triple as classified (already in doc 45).**  *Neutral.*  Tight constraints on the algebra, once the axioms are granted.  One-loop running of \(g_3^2=g_2^2=\tfrac53 g_1^2\) does not meet at one scale; the Higgs example is \(\sim 170\,\mathrm{GeV}\); \(N=3\) is an input.  The raw product conoid \(\times F\) is 2D.

4. **Frequency-\(n\) conoids, caps, and “closed” conoid-like surfaces.**  *Dead end.*

5. **\(C_4\) representations, four nodes, or twelve-bridge labelling as a finite algebra or fermion content.**  *Dead end.*

6. **Euler characteristic, Hopf bundle, or \(TS^2\) as a source of the integer \(3\).**  *Dead end.*

---

## 5. What this does *not* change

- The APS index of the untwisted Dirac operator on the truncated conoid is still \(0\).
- The singular tip is still a geodesic boundary of length \(8\ell_0\) with four nodes, not a cone.
- \(\omega_0\), the exponent \(4/13\), and the \(G_N\) prefactor \(\alpha\) are still not derived.
- No new core theorem is claimed.

---

## 6. How to reproduce

```bash
python experiments/alt_geometries/report.py
pytest -q tests/test_alt_geometries.py
```
