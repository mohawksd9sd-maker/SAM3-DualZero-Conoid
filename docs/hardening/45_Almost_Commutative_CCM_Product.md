# 45 — Almost-commutative product with the CCM finite triple

**Date:** 23 November 2026 (America/Chicago)
**SSOT:** `STATUS_CLAIMS_AND_RESIDUALS.md`
**Rule:** derivation only; only verified literature; null results stay null.

No standalone paper was written.

Literature actually used (fetched, not invented):

- A. H. Chamseddine, A. Connes, M. Marcolli, *Gravity and the standard model with neutrino mixing*, Adv. Theor. Math. Phys. **11** (2007) 991–1089, arXiv:hep-th/0610241.  (**CCM2007**)
- A. H. Chamseddine, A. Connes, *Noncommutative geometry as a framework for unification… Part I*, Fortschr. Phys. **58** (2010) 553–600, arXiv:1004.0464.  (**CC2010**)

The finite spectral triple \(F\) is the standard one of those papers: algebra \(\mathbb{C}\oplus\mathbb{H}\oplus M_3(\mathbb{C})\), KO-dimension 6, metric dimension 0.  CCM2007 states explicitly that the multiplicity \(N=3\) “is an input” and “is not predicted by our model in its present form.”

Repository draft Paper 09 is **not** a source.  It assigns KO-dimension 4 to \(F\) (the literature value is 6) and claims that the product of the 2D conoid with \(F\) yields 4D Einstein–Hilbert gravity.  Both claims are inconsistent with CCM and with the dimension of the heat kernel.

---

## 1. Forming the product: dimensional honesty

The canonical spectral triple on a Riemannian spin \(n\)-manifold has KO-dimension \(n\bmod 8\).  KO-dimensions of a product add.  The CCM fermionic action is built for total KO-dimension \(\equiv 2\pmod{8}\), which is what \(M^4\times F\) (\(4+6=10\equiv 2\)) provides.

| Geometry | Cont. dim | KO-dim | Matches CCM fermions? | 4D heat kernel? | Verdict |
|----------|-----------|--------|------------------------|-----------------|---------|
| conoid \(\times F\) | 2 | \(2+6=0\) | no | no | **Failed** as a 4D unification model |
| \(M^4\times\) conoid \(\times F\) | 6 | \(4+2+6=4\) | no | only under an extra “internal compactification” hypothesis | **Partially derived**, with that hypothesis |
| (conoid \(\times\Sigma^2)\times F\) | 4 | \(2+2+6=2\) | yes | yes | **Partially derived**, assuming a choice of \(\Sigma^2\) |
| \(M^4\times F\) (plain CCM) | 4 | \(4+6=2\) | yes | yes | **Derived in the literature**, independent of the conoid |

The raw product conoid \(\times F\) produces a *two-dimensional* spectral action (\(\Lambda^2\mathrm{Area}+\)curvature/boundary terms).  It does not yield 4D Einstein–Hilbert plus 4D Yang–Mills.  That is the dimensional mismatch, and it is not repaired by tensoring with the metric-dimension-zero algebra \(F\).

The only option that is both 4-dimensional and of KO-dimension 2, and that actually uses the conoid, is \(Y\times F\) with \(Y=\)conoid\(\times\Sigma^2\).  Every volume and curvature statement about \(Y\) then depends on a 2-manifold \(\Sigma^2\) that is **not determined** by the locked conoid.

---

## 2. What the conoid changes in the spectral action

**Spectator argument (derived, assuming \(C\) is a commutative Riemannian factor tensored with \(F\)).**
Inner fluctuations of \(A_F\) are gauge fields on \(\mathcal{H}_F\), constant along \(C\).  Every 4D Yang–Mills term in \(a_4\) is multiplied by the same integral \(\int_C\mathrm{vol}\).  Therefore the relative coefficients of \(\mathrm{Tr}\,B^2\), \(\mathrm{Tr}\,W^2\) and \(\mathrm{Tr}\,V^2\) remain those of CCM, and

\[
  g_3^2=g_2^2=\frac53 g_1^2
\]

at \(\Lambda\) is **unchanged**.  The Higgs quartic at \(\Lambda\) is a ratio of traces on \(F\) (CC2010 §6) and is likewise unchanged.  A spectator area *does* rescale the map from the moment \(F_0\) to \(g^2\) and from \(F_2\) to \(G_N\).

**Heat-kernel integrals of the locked conoid (derived).**

- Area of \(X_{a,b}\): \(A(a,b)=\pi(b^2-a^2)+\int_a^b I(u)\,du\).  On the unit metric, \(A(0,b)=\pi b^2+2\pi\log b+C_0+o(1)\) with the exact finite part \(C_0=2\pi\ln 2\).  For general \(\ell_0\): \(A(0,b)=\pi b^2+2\pi\ell_0^2\log(b/\ell_0)+2\pi\ell_0^2\ln 2+o(1)\).
- Curvature integral, exact antiderivative:
  \(\int_{X_{a,b}}K\,dA=\int_0^{2\pi}\bigl(a/f(a,v)-b/f(b,v)\bigr)\,dv\).
  The angular integral is \(4u\,K(k)/\sqrt{u^2+4\ell_0^2}\) with \(k^2=4\ell_0^2/(u^2+4\ell_0^2)\).
- Gauss–Bonnet on the annulus (\(\chi=0\)) is the identity
  \(\int K\,dA+\int_{u=b}(f_u/f)\,ds-\int_{u=a}(f_u/f)\,ds=0\).
- Complete-surface limit: \(\int_{(0,\infty)\times S^1}K\,dA=-2\pi\).

These enter \(a_0\) (area, times fibre rank) and \(a_2\) (a universal multiple of \(\int R\) plus boundary terms).  They do **not** uniquely fix the cutoff moments \(F_0,F_2,F_4\).  In plain CCM those three moments are initial conditions for \((g^2,G_N,\Lambda_{\mathrm{cosmo}})\), not predictions (CC2010, below (6.1)).  Replacing the internal volume by \(C_0=2\pi\ln 2\) is a scheme, already recorded as such in docs 43–44, not a uniqueness theorem for \(\alpha\).

**Boundary / tip contributions.**  The two boundary circles contribute the geodesic-curvature terms above.  The inner contribution tends to 0 as \(a\to 0\) (like \(a\log(\ell_0/a)\)).  The outer contribution tends to \(2\pi\) as \(b\to\infty\).  See §5 for the singular tip itself.

---

## 3. One-loop running of the CCM boundary conditions

Beta functions and the unification relation are taken from CC2010 (6.1)–(6.8), in the hypercharge convention used there:

\[
  \beta_{g_i}=(4\pi)^{-2}b_i g_i^3,\qquad b=\bigl(\tfrac{41}{6},-\tfrac{19}{6},-7\bigr).
\]

With CC2010’s own inputs at \(M_Z=91.188\,\mathrm{GeV}\)
(\(g_1,g_2,g_3)=(0.3575,0.6514,1.221)\)), one-loop running gives the pairwise scales

| Condition | Scale |
|-----------|--------|
| \(\alpha_2=\alpha_3\) | \(1.20\times 10^{17}\,\mathrm{GeV}\) |
| \(\tfrac53\alpha_1=\alpha_2\) | \(1.33\times 10^{13}\,\mathrm{GeV}\) |
| \(\tfrac53\alpha_1=\alpha_3\) | \(3.10\times 10^{14}\,\mathrm{GeV}\) |

The three couplings do **not** meet at one scale (CC2010 already says this).  At \(10^{17}\,\mathrm{GeV}\) the relative spread among \(\alpha_2^{-1}\), \(\alpha_3^{-1}\) and \(\tfrac35\alpha_1^{-1}\) is about \(16\%\).  The conoid, as a spectator, does not change this running.

The CC2010 cutoff-function example \(\lambda_0=0.356\) at \(10^{17}\,\mathrm{GeV}\) gives \(\lambda(M_Z)\sim 0.241\) and \(m_H\sim 170\,\mathrm{GeV}\), against the observed Higgs mass \(\approx 125.20\,\mathrm{GeV}\).  That discrepancy is in the literature; the conoid does not remove it.

Verdict: **derived as a reproduction of CCM/SM one-loop facts**; **failed** as a conoid improvement of those facts.

---

## 4. Does the conoid fix \(\omega_0\), \(\alpha\), or the generation count?

| Question | Verdict |
|----------|---------|
| \(\omega_0\) and \(4/13\) | **Failed** (unchanged: no unique geometric derivation; doc 44) |
| \(G_N\) prefactor \(\alpha\) | **Failed** to uniquely fix it.  Exact \(C_0\) and \(\int K=-2\pi\) enter the gravitational coefficients, but \(F_2\) and the volume scheme remain free. |
| Generation count | **Failed.**  \(N=3\) is an input of \(F\) (CCM2007).  The untwisted APS index on the truncated conoid is 0 (doc 44). |
| CCM ratios \(g_3^2=g_2^2=\tfrac53 g_1^2\) at \(\Lambda\) | **Unchanged** by a spectator conoid (**derived** under that assumption). |
| CCM Higgs-mass relation at \(\Lambda\) | **Unchanged** by a spectator conoid; the one-loop 170 GeV vs 125 GeV discrepancy remains. |

---

## 5. Other attempts

**Natural \(U(1)\) twist for index 3.**  Falomir index 3 needs \(\kappa\in(2,3]\).  The only natural closed 2-form built from the metric curvature has flux \(\int K\,dA/2\pi=-1\), not in \((2,3]\).  The spin connection is already in the untwisted Dirac operator.  The isometry group \(C_4\) does not single out that holonomy.  **Failed.**

**Singular tip.**  The locked embedding \(r(u,v)=(u\cos v,\,u\sin v,\,\ell_0\sin(2v))\) is an embedding for \(u>0\).  At \(u=0\) the image is the segment \(\{0\}\times\{0\}\times[-\ell_0,\ell_0]\) on the \(z\)-axis.  The four coordinate nodes \(v=\pi/4+k\pi/2\) map to the two endpoints \(z=\pm\ell_0\), each with two preimages.  Along the open segment two ruling lines cross (a self-intersection of the image in \(\mathbb{R}^3\)).  The abstract metric on \(u>0\) is smooth.  The APS index of every truncation \(X_{a,b}\) with \(a>0\) is 0, so cutting closer to the tip does not produce index 3.  The singular space obtained by adding \(u=0\) is not a smooth compact manifold with boundary; we do not invent an index for it.  **Partially derived** (geometry and the \(a\to 0\) limit); the singular-space index remains open and is not an index-3 theorem.

---

## Code and tests

- `code/almost_commutative_product.py`
- `code/conoid_heat_kernel.py`
- `code/ccm_oneloop_rge.py`
- `code/u1_twist_and_tip.py`
- `tests/test_almost_commutative_product.py`
- JSON under `reproducibility/`
