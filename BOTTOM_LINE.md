# SAM-3 — Bottom line

**Date:** 23 November 2026 (America/Chicago)  
**This file is the short public statement of where the work stands.**  
The single source of truth for claim status remains [`STATUS_CLAIMS_AND_RESIDUALS.md`](STATUS_CLAIMS_AND_RESIDUALS.md).  If this file and that one ever conflict, that one wins.

Honesty rule: unproven statements are labelled.  Null results stay null.

---

## What is proven on the locked conoid

From the embedding \(r(u,v)=(u\cos v,\ u\sin v,\ \ell_0\sin(2v))\):

- The induced metric is \(f=\sqrt{u^2+4\ell_0^2\cos^2(2v)}\) (the coefficient is 4, not 16).
- The metric has an exact \(C_4\) isometry \(v\mapsto v+\pi/2\).  \(A_5\) is *not* an isometry.
- Gaussian curvature \(K=-4\ell_0^2\cos^2(2v)/f^4\le 0\).  \(K\) is unbounded near the four tip nodes, with \(\max_v|K(u,\cdot)|=1/(4u^2)\) for \(0<u\le 2\ell_0\), but is integrable.
- The area of the truncated conoid has a finite part \(C_0=2\pi\ln 2\) on the unit metric.
- The complete-surface total curvature is \(\int K\,dA=-2\pi\).
- On the radial model operators, \(E_0(m;U)=(j_{\nu,1}/U)^2\) with \(\nu=\sqrt{m^2+1/4}\), and \(E_0(m)\) is strictly increasing in \(m\).
- The APS index of the *untwisted* Dirac operator on the truncated conoid (product collar, bounding spin structure at both ends) is \(0\), independently of the cuts and of \(\ell_0\).  It is not 3.
- The metric completion at \(u=0\) is a geodesic boundary circle of length \(8\ell_0\), with a \(C^\infty\) metric degenerate at the four nodes.  It is not a cone, and it does not give a derived index of 3.

These are theorems of the locked core.  They are unchanged by the later exploratory work.

---

## What the unification experiments showed (docs 44–48)

Honest attempts to *derive* unification-relevant structure from the locked geometry all failed for the quantities that would make a model (docs 44–45).  The singular tip does not repair the index (doc 46).

A survey of other surfaces and internal spaces (doc 47) found one clean *mechanism* for three chiral zero modes — a chosen integer flux or bundle degree on a compact surface, in a 4D product with a CCM or Pati–Salam finite triple — and found that Pati–Salam is a more flexible internal space in the cited literature.  In every case, the integer 3 is put in by hand.

Developing that product (doc 48): conoid \(\times\) magnetized \(\Sigma\) \(\times\) the Pati–Salam finite triple is a consistent 4D almost-commutative geometry (KO-dimension \(2+2+6\equiv 2\)).  The Pati–Salam gauge relation \(g_R=g_L=g\) at the cutoff is derived (a spectator argument).  The heat-kernel integrals of the product, including \(C_0\) and \(\int K=-2\pi\), are derived.  The one-loop RG pipeline, with PDG inputs, determines

\[
  m_R\approx 4.20\times 10^{13}\,\mathrm{GeV},\qquad
  \Lambda\approx 2.40\times 10^{15}\,\mathrm{GeV}
\]

from the measured couplings plus the Pati–Salam meeting condition.  That is a determination, not a prediction of those couplings.  Nothing in the combined geometry fixes the flux to 3, or uniquely fixes the area, complex structure, or Wilson lines of \(\Sigma\).  The spectral action of a magnetized torus prefers *smaller* \(\lvert M\rvert\), not \(M=3\).  Charged-lepton mass ratios are not derived; a labelled, underdetermined fit can accommodate them from some starting points.  The Higgs mass is not a unique prediction of the product.

---

## What is not derived

The following remain free inputs, conventions, or choices.  They are not theorems of the locked geometry, and they were not derived in the exploratory experiments.

- The Dual-Zero scale \(\omega_0\) and the exponent \(4/13\).
- The prefactor \(\alpha\) in \(G_N=\alpha\ell_0^2\) (the recorded value \(64\pi/45\) is a convention lock).
- The flux \(M=3\) (or a bundle degree 3) that would give three chiral generations on a compact surface.
- The moduli of that surface: area, complex structure \(\tau\), and Wilson lines.
- Gauge group, unique mass ratios, and a unique Higgs mass, as outputs of the locked conoid.

The Riemann hypothesis is not a claim of this repository.  A non-circular identification test found no evidence that Dual-Zero critical points match zeta zeros.

---

## The missing principle

The locked conoid is in good mathematical order, as far as the theorems above go.  What the unification programme still lacks is a *principle that fixes the flux at 3 and the surface moduli*.

Until that principle is found and derived — not fitted, and not imposed by counting 4 nodes or 12 bridges — three generations, the Yukawa texture, and a unique 4D product model remain choices rather than outputs of the geometry.

Exploratory code for the product and the failed searches lives in `experiments/` and is documented in docs 47–48.  A broader survey of candidate principles, with computations, is in [`docs/hardening/49_Missing_Principle_Survey.md`](docs/hardening/49_Missing_Principle_Survey.md).  A further round of tests, still with no accidental fit, is in [`docs/hardening/50_Further_Candidate_Tests.md`](docs/hardening/50_Further_Candidate_Tests.md).  A review of earlier SAM-2, desktop math-model, and May 2026 Dual-Zero formulations is in [`docs/hardening/51_SAM2_Lines_Review.md`](docs/hardening/51_SAM2_Lines_Review.md): the regulator to keep is the current definition, not the SAM-2 ultrafilter entity and not the May 2I generation argument.  None of those lines fills the missing principle.  The standalone Dual-Zero axiom was then applied, without fitting, to the magnetized torus, the unfluxed torus, \(T^2/\mathbb{Z}_4\), a monopole sphere, and the Pati–Salam / CCM product ([`docs/hardening/52_DualZero_Axiom_Selection_Test.md`](docs/hardening/52_DualZero_Axiom_Selection_Test.md)).  It does not select the flux or the moduli.  This work is not part of the locked core.
