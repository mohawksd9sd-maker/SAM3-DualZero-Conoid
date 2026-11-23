# 48. Conoid × magnetized surface × Pati–Salam (exploratory)

**Date:** 23 November 2026 (America/Chicago)  
**Status:** Exploratory development of the top-ranked direction of doc 47.  **Not part of the locked SAM-3 core.**  
**Code:** `experiments/ps_conoid_product/`  
**Tests:** `tests/test_ps_conoid_product.py`  
**Reproduction:** `python experiments/ps_conoid_product/report.py` (writes `reproducibility/ps_conoid_product_report.json`) and `pytest -q tests/test_ps_conoid_product.py`.

Honesty rule: unproven statements are labelled.  Fits are labelled as fits.  Null results stay null.  Citations were fetched and checked.

The locked core (right-conoid metric, \(C_0=2\pi\ln 2\), exact \(E_0(m)\), APS index \(0\) of the untwisted Dirac operator, singular tip as a geodesic boundary of length \(8\ell_0\)) is unchanged.  Docs 44–47 still stand.

---

## The geometry

Let \(X_{a,b}\) be the truncated right conoid and \(\Sigma\) a compact orientable surface (\(T^2\) or \(S^2\)), possibly with a \(U(1)\) flux of integer Chern number \(M\).  The continuous 4-geometry is the Riemannian product \(Y=X_{a,b}\times\Sigma\).  The finite spectral triple \(F_{\mathrm{PS}}\) is that of Chamseddine–Connes–van Suijlekom, JHEP 11 (2013) 132, arXiv:1304.8050: algebra \(\mathbb{H}_R\oplus\mathbb{H}_L\oplus M_4(\mathbb{C})\), KO-dimension 6, one-generation fermions in \((2,1,4)+(1,2,4)\).

KO-dimensions add: \(2+2+6=10\equiv 2\pmod{8}\), matching the CCM fermionic setup (doc 45).  The heat kernel is four-dimensional.

**Two caveats, kept in view throughout.**

1. \(Y\) is not Lorentzian Minkowski space.  Interpreting the spectral action on \(Y\times F_{\mathrm{PS}}\) as a model of our \(3+1\) world uses the same Euclidean-to-Lorentzian step as CCM, plus the identification of \(Y\) with the 4-manifold in that construction.  Gravity extracted from \(a_2\) is gravity *on \(Y\)*.

2. Generations and the finite multiplicity cannot both be set to 3 without over-counting.
   - *Option A.* \(N_F=3\) is an input of \(F_{\mathrm{PS}}\); \(\Sigma\) need not carry flux.  The CCvS Higgs numerics apply as in the literature.  Flux does not explain the generation count.
   - *Option B* (the intended package). \(N_F=1\); three chiral zero modes come from flux \(M=3\) on \(\Sigma\).  The CCvS/CC2012 traces on a finite Dirac operator whose generation index already sits in \(D_F\) do **not** apply off the shelf.  We do not invent a replacement \(a_4\) computation.
   - \(N_F=3\) *and* flux 3 would give nine generations and is not used.

---

## 1. Spectral action and heat-kernel coefficients

**Geometric integrals (derived).**  For a Riemannian product,
\[
  \mathrm{vol}(Y)=\mathrm{Area}(X)\,\mathrm{Area}(\Sigma),
\]
\[
  \int_Y R=\mathrm{Area}(\Sigma)\int_X R_X+\mathrm{Area}(X)\int_\Sigma R_\Sigma,
\]
with the 2D convention \(R=2K\).  On the unit metric,
\[
  \mathrm{Area}(X_{0,b})=\pi b^2+2\pi\log b+C_0+o(1),\qquad C_0=2\pi\ln 2,
\]
and \(\int_X K\,dA\to-2\pi\) as \(a\to 0\), \(b\to\infty\), so \(\int_X R\to-4\pi\).

- For \(\Sigma=T^2\) (flat, \(\int R_\Sigma=0\)): \(\int_Y R\to-4\pi\,\mathrm{Area}(T^2)\), which is finite.  The volume and any flux Yang–Mills integral still diverge with \(\mathrm{Area}(X)\).
- For \(\Sigma=S^2\): \(\int R_\Sigma=8\pi\), and \(\int_Y R\) diverges as \(\mathrm{Area}(X)\cdot 8\pi\).

\(C_0\) is the finite part of \(\mathrm{Area}(X)\) after subtracting \(\pi b^2\) and the logarithm.  It does **not** cancel the volume divergence, nor the flux term for \(M\neq 0\).

**Flux Maxwell term (derived scaling).**  For a constant-curvature \(U(1)\) flux of Chern number \(M\) on \(\Sigma\),
\[
  \int_Y|F_\Sigma|^2=\mathrm{Area}(X)\frac{(2\pi M)^2}{\mathrm{Area}(\Sigma)}.
\]
Nonnegative, zero only at \(M=0\), and divergent with \(\mathrm{Area}(X)\) for \(M\neq 0\).

**Gravitational coupling.**  On a closed 4-manifold the Einstein–Hilbert coefficient \(1/(16\pi G)\) in the spectral action is local and is built from the cutoff moments \(f_2,f_0\) and traces on \(F\) (CC2010, after (5.46) and §6).  It does *not* involve \(C_0\) or \(\int K\).  Those change integrated terms on a truncation, not the local value of \(G\).  Identifying \(G_Y\) with Newton’s constant in observed spacetime is an extra assumption.  Even as a coupling on \(Y\), the moments remain free, so \(G_Y\) is not uniquely derived.  Same scheme-dependence as in docs 43–45.

**Gauge couplings at \(\Lambda\) (derived, under the CCvS spectral action on \(Y\times F_{\mathrm{PS}}\)).**  Normalizing the \(F_0 a_4\) Yang–Mills terms requires \(g_R=g_L=g\) at \(\Lambda\) (CCvS2015).  A commutative factor \(Y\) multiplies every term by the same volume and does not change the ratios (spectator argument of doc 45, applied to \(F_{\mathrm{PS}}\)).  Matching at a breaking scale \(m_R\) is CCvS2015 (25):
\[
  \frac{1}{g_1^2}=\frac23\frac{1}{g^2}+\frac{1}{g_R^2},\qquad
  \frac{1}{g_2^2}=\frac{1}{g_L^2},\qquad
  \frac{1}{g_3^2}=\frac{1}{g^2},
\]
with \(g_1\) the SM hypercharge coupling.  At a point where \(g_R=g_L=g\) this is the same relation \(g_3^2=g_2^2=\tfrac53 g_1^2\) as in CCM.

**Higgs / \(\sigma\) sector at \(\Lambda\).**  The CC2012 tree-level couplings (arXiv:1208.1030, eqs. (12)–(15)), with \(n\) a Yukawa-ratio parameter, *not* the flux, are
\[
  \lambda_h=4g^2\frac{n^2+3}{(n+3)^2},\quad
  \lambda_{h\sigma}=4g^2\frac{2n}{n+3},\quad
  \lambda_\sigma=8g^2.
\]
The light-Higgs reduction factor at tree level is \(\sqrt{1-\lambda_{h\sigma}^2/(\lambda_h\lambda_\sigma)}=\sqrt{(3-n^2)/(n^2+3)}\) for \(n^2<3\).  At \(n=0\) it is \(1\); at \(n=1\) it is \(1/\sqrt{2}\).  CCvS2015 states that after running, a \(125\,\mathrm{GeV}\) Higgs is compatible for a range of \(\rho=m_t/m_\nu\) and \(\Lambda\), with \(m_\sigma\) of order \(10^{12}\,\mathrm{GeV}\).  That is a literature result with free parameters, not a unique prediction, and it applies off the shelf only in option A.  In option B we do not invent a replacement computation.

---

## 2. Does anything fix flux \(=3\) or the moduli?

Checked, and all failed.

| Attempt | Selects \(M=3\)? | Fixes moduli uniquely? | Verdict |
|---------|--------------------|-------------------------|---------|
| Dirac quantization | no (\(M\in\mathbb{Z}\); smallest positive is 1) | no | failed |
| Anomaly cancellation | no (a single bundle copies an already anomaly-free generation \(M\) times, for every \(M\)) | no | failed |
| KO-dimension or \(J\) | no (independent of the connection on \(\Sigma\)) | no | failed |
| Tadpole / Maxwell eom | no (constant flux solves \(d{*}F=0\) for every integer \(M\); there is no string tadpole in this spectral action) | no | failed |
| Tip length \(8\ell_0\) or \(C_4\) matched to the torus lattice | no | no | failed; unprincipled / numerology (the tip circle is not a cycle of \(\Sigma\); \(C_4\) acts on the conoid factor, not on \(\Sigma\)) |
| \(\lvert\int_X K\rvert/2\pi=1\) used as a flux | would give 1, not 3 | no | failed |
| Spectral-action minimization over \((M,A)\) | no; prefers the *smallest* \(\lvert M\rvert\) | no unique area; \(\tau\) does not enter the spectrum | failed |

The last item is a real computation.  The Dirac spectrum on a flat magnetized \(T^2\) of area \(A\) and flux \(M>0\) is the standard Landau tower \(E_n=\pm\sqrt{4\pi n\lvert M\rvert/A}\) with degeneracy \(\lvert M\rvert\), plus \(\lvert M\rvert\) zero modes of one chirality.  The heat kernel is closed-form,
\[
  \mathrm{Tr}\,e^{-tD_\Sigma^2}=\lvert M\rvert\,\coth\bigl(2\pi t\lvert M\rvert/A\bigr),
\]
checked against a direct Landau sum (relative error \(<10^{-10}\)) and against the Weyl limit \(A/(2\pi t)\).  The small-\(t\) expansion is
\[
  \frac{A}{2\pi t}+\frac{2\pi t M^2}{3A}+O(t^3).
\]
The first \(M\)-dependent term is positive and, at fixed area, is minimized by the smallest \(\lvert M\rvert\).  A scan of \(\mathrm{Tr}\,f(D_\Sigma/\Lambda)\) with \(f(x)=e^{-x^2}\) over \(M=1,\ldots,6\) and a range of areas confirms that every fixed-area slice prefers \(M=1\), never \(M=3\).  The eigenvalues do not depend on the complex structure \(\tau\), so this action cannot fix \(\tau\) either.  A common Wilson line is a translation and does not change eigenvalues.

**Headline of this section:** nothing in the combined geometry fixes the flux to 3, or uniquely fixes the area, complex structure, or Wilson lines of \(\Sigma\).

---

## 3. One-loop (and partial two-loop) RG pipeline

The CCvS2015 procedure uses the measured SM couplings at \(M_Z\) as *inputs*, runs them to a variable \(m_R\), and adjusts \(m_R\) until \(g_R,g_L,g\) meet.  That **determines** \((m_R,\Lambda)\) from the data plus the PS boundary condition.  It is **not** a prediction of the couplings at \(M_Z\).  Because the geometry does not fix \(m_R\) or \(\Lambda\), there is no top-down prediction of \((g_1,g_2,g_3)(M_Z)\).  Running down from the fitted scales only returns the inputs by construction.

**Inputs at \(M_Z\).**

| Quantity | Value | Source |
|----------|-------|--------|
| \(M_Z\) | \(91.1879\,\mathrm{GeV}\) | PDG 2026 Physical Constants |
| \(\alpha_s(M_Z)\) | \(0.1180\) | PDG 2026 Physical Constants |
| \(\sin^2\theta_W(M_Z)\big\|_{\overline{\mathrm{MS}}}\) | \(0.23122\) | PDG 2026 Physical Constants |
| \(\hat\alpha^{-1}(M_Z^2)\) | \(127.930\) | PDG 2024 recommendation (the 2026 constants table does not recommend a new \(\alpha(M_Z)\)) |

These give \((\alpha_1,\alpha_2,\alpha_3)=(0.010168,\ 0.033807,\ 0.1180)\) in the CC2010 convention \(\alpha_1=g'^2/(4\pi)\).  We also rerun with the CC2010 inputs of doc 45 for comparison.

The PS segment is always one-loop, with CCvS2015 beta coefficients.  CCvS2015 did not publish two-loop PS \(\beta\)-functions; we do not invent them.  Below \(m_R\) we use either one-loop SM or a *partial* two-loop SM (gauge matrix \(B_{ij}\) of Machacek–Vaughn, GUT normalisation, two-loop Yukawa contributions omitted).

| Run | \(m_R\) (GeV) | \(\Lambda\) (GeV) | vs CCvS2015 quote | relative \(\ln\) error |
|-----|---------------|-------------------|-------------------|------------------------|
| Composite, one-loop, CC2010 inputs | \(5.43\times 10^{13}\) | \(3.05\times 10^{15}\) | \(4.25\times 10^{13}\), \(2.5\times 10^{15}\) | \(0.245\), \(0.198\) |
| Composite, one-loop, PDG inputs | \(4.20\times 10^{13}\) | \(2.40\times 10^{15}\) | same quote | \(0.011\), \(0.041\) |
| Composite, partial two-loop SM, PDG inputs | \(3.73\times 10^{13}\) | \(1.29\times 10^{15}\) | same quote | \(0.131\), \(0.661\) |
| With the \((1,1,15)\), one-loop, PDG inputs | \(4.03\times 10^{13}\) | \(5.80\times 10^{15}\) | \(4.1\times 10^{13}\), \(6.3\times 10^{15}\) | \(0.017\), \(0.082\) |

With current PDG inputs, the one-loop composite determination sits within a few percent of the CCvS2015 quoted scales.  The partial two-loop SM running below \(m_R\) lowers \(\Lambda\) by a factor of about two but leaves a triple meeting (spread in \(1/g^2\) at \(\Lambda\) is \(\sim 10^{-14}\)) and keeps both scales in the same ballpark.  That shift is an uncertainty of the approximation, not a new geometric prediction.

---

## 4. Yukawas and masses

The \((I,J,K)=(3,3,6)\) overlap tensor of doc 47 is reused.  Six Higgs zero modes, each giving a \(3\times 3\) Yukawa.  Overall scale is absorbed into the Higgs vev; only mass *ratios* are compared to the charged-lepton pole ratios (PDG 2024) \(m_\mu/m_e\approx 206.768\), \(m_\tau/m_e\approx 3477.23\).

**Principled minimization.**  The Dirac spectrum on a magnetized flat torus does not depend on \(\tau\), so the spectral action of \(D_\Sigma\) cannot fix \(\tau\).  A target-blind Frobenius-norm scan over a grid of \(\mathrm{Im}\,\tau\), a relative Wilson line, and the six Higgs slices has a minimizer whose singular-value ratios are \(1:1:2.95\), nowhere near the lepton hierarchy.  We do not invent an \(a_4\) Yukawa potential beyond that.

**Labelled fit** (not a derivation).  Five continuous parameters (\(\log\mathrm{Im}\,\tau\), \(\mathrm{Re}/\mathrm{Im}\,\zeta_J\), \(\mathrm{Re}/\mathrm{Im}\,\zeta_K\)) plus one discrete Higgs-slice choice, against two observables, with \(\zeta_I=0\) and \(\mathrm{Re}\,\tau=0\) held fixed as stated restrictions.  The system is underdetermined.

- From a seed at \(\mathrm{Im}\,\tau=1\), the search remains far from the target (ratios \(\approx 1:551:1213\), log-error \(\approx 2.07\)).
- From a seed at \(\mathrm{Im}\,\tau=2\), on Higgs slice 0, the same search *accommodates* the two ratios to high accuracy: \(\mathrm{Im}\,\tau\approx 3.541\), \(\zeta_J\approx 0.073+0.253i\), \(\zeta_K\approx 0.078+0.505i\), ratios \(\approx 1:205.54:3477.10\) against \(1:206.77:3477.23\), log-error \(\approx 3.5\times 10^{-5}\).  Nelder–Mead’s formal success flag was false (it ran out of iterations); the residual, not the flag, is the relevant figure.

A 5-parameter fit to two numbers can accommodate those numbers from some starting points and fail from others.  That is not a unique minimum, and it is not a prediction of the geometry.  Quark ratios and mixing angles were not included; adding them would add observables but also more Yukawa tensors (up and down, possibly more moduli).

**Higgs mass with \(\sigma\).**  As in §1: a literature compatibility statement in option A, not a unique number, and not applicable off the shelf in option B.

---

## 5. Verdict

| Item | Status |
|------|--------|
| 4D KO-dimension \(2+2+6\equiv 2\) | **Derived** (arithmetic of KO-dimensions) |
| PS gauge relation \(g_R=g_L=g\) at \(\Lambda\), and the matching (25) | **Derived**, assuming the CCvS spectral action on \(Y\times F_{\mathrm{PS}}\) (spectator) |
| Heat-kernel integrals of \(Y\), including \(C_0\) and \(\int K=-2\pi\), and the flux term \(\propto M^2/A\) | **Derived** |
| \(G_N\) (or even \(G_Y\)) | **Not uniquely derived** (unfixed moments; identification of \(Y\) with observed spacetime is an assumption) |
| Flux \(M=3\) | **Not derived.**  Every mechanism checked failed; the spectral action prefers smaller \(\lvert M\rvert\).  \(M=3\) remains a **choice**. |
| Area, \(\tau\), Wilson lines of \(\Sigma\) | **Not uniquely derived.**  \(\tau\) does not enter the Dirac spectrum. |
| \((m_R,\Lambda)\) from the RG pipeline | **A determination from measured couplings plus the PS meeting condition**, not a geometric prediction.  With PDG inputs, one-loop composite values are \(m_R=4.20\times 10^{13}\,\mathrm{GeV}\), \(\Lambda=2.40\times 10^{15}\,\mathrm{GeV}\). |
| Couplings at \(M_Z\) | **Not predicted** (they are inputs of the pipeline) |
| Charged-lepton mass ratios | **Not derived.**  A labelled, underdetermined fit can accommodate them from some seeds. |
| Higgs mass | **Not a unique prediction** of the product.  CCvS compatibility with \(125\,\mathrm{GeV}\) is literature, option A only. |

**What would be falsifiable, if the free choices were frozen?**  The PS meeting condition plus one-loop (or partial two-loop) running would then predict a pair \((m_R,\Lambda)\) once the couplings are measured — but the couplings are already used to find that pair, so the only sharp claim still in play is that a physically plausible \(m_R\) *exists*.  It does, near \(10^{13}\,\mathrm{GeV}\).  That is a consistency check of the PS embedding plus the SM/PS beta functions, and it does not use the conoid.

**What is still free:** the flux (if one wants three generations, \(M=3\) is put in); the moduli of \(\Sigma\); the cutoff moments \(f_0,f_2,f_4\); the outer cutoff of the conoid; the Yukawa-ratio parameter \(n\) (or \(\rho\)) in the literature Higgs analysis; and the Euclidean-to-Lorentzian plus “\(Y\) is spacetime” step.

---

## 6. How to reproduce

```bash
python experiments/ps_conoid_product/report.py
pytest -q tests/test_ps_conoid_product.py
```
