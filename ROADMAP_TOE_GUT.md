# Roadmap: what must be found for an authentic GUT and an authentic TOE

**Date:** 23 November 2026 (America/Chicago)  
**Status:** research targets, not claims.  Nothing in this file is a derivation, a fit presented as a result, or a change to the locked core.

Honesty rule: unproven statements are labelled.  Null results stay null.  Dual-Zero is to be preserved in the well-posed form of docs 18 and 52 — the generator \(\varepsilon(n)=\omega_0(-1)^n n^{-n}\) with \(\omega_0\) an input, and the symmetric average \(\operatorname{Reg}_2\) acting on functions of a spectral parameter.  It is not a uniqueness theorem, not a heat-trace weight \(\sum\varepsilon(n)e^{-t\lambda_n^2}\), and not the SAM-2 ultrafilter entity.  Information-conserving Dual-Zero arithmetic (doc 53) may be used in computations; it removes rounding loss only.

Three generations would be a special case of a derived flux or bundle degree.  It is welcome if a principle produces it, and it is not a requirement of this roadmap.

This document states (i) what has already been established, (ii) what must still be found for an authentic grand unified theory, and (iii) what must still be found for an authentic theory of everything.  For each open item: the present status, what was tried in docs 44–54, the next calculation or theorem, and a falsifiable test.

---

## 1. What has been established

These are the parts that later work should keep, not reopen without cause.

**Locked conoid geometry (core paper; docs 35, 42–46).**  
From the embedding \(r(u,v)=(u\cos v,\ u\sin v,\ \ell_0\sin(2v))\) one has the induced metric \(f=\sqrt{u^2+4\ell_0^2\cos^2(2v)}\), an exact \(C_4\) isometry, Gaussian curvature \(K=-4\ell_0^2\cos^2(2v)/f^4\le 0\), finite area part \(C_0=2\pi\ln 2\) on the unit metric, complete-surface total curvature \(\int K\,dA=-2\pi\), radial eigenvalues \(E_0(m;U)=(j_{\nu,1}/U)^2\) with \(\nu=\sqrt{m^2+1/4}\), and APS index \(0\) for the untwisted Dirac operator on the truncated conoid.  The tip \(u=0\) is a geodesic boundary of length \(8\ell_0\) with four nodes; it does not give a derived index of \(3\).  These theorems stand independently of unification.

**Dual-Zero as a definition (docs 18, 51, 52).**  
The May / current generator and symmetric \(\operatorname{Reg}_2\) are a well-posed regulator on functions with finite one-sided limits.  Doc 52 wrote that as a standalone axiom and applied it, without fitting, to magnetized \(T^2\), unfluxed \(T^2\), \(T^2/\mathbb{Z}_4\), a monopole sphere, and the Pati–Salam / CCM product.  It does not select the flux or the moduli, and a selection that would require tuning \(\omega_0\) is not a derivation.

**A consistent unification *scheme*, not yet a GUT or a TOE (docs 45, 47–51, 54).**  
A 4D almost-commutative product

\[
  (\text{spacetime factor})
  \;\times\;
  (\text{compact magnetized surface }\Sigma)
  \;\times\;
  (\text{Pati–Salam or CCM finite triple }F)
\]

can, in one spectral framework, produce gravity (Einstein–Hilbert and higher Seeley terms from the spectral action), a gauge group (a *choice* of \(F\)), and chiral matter (index equal to the flux or bundle degree \(M\), also a choice).  The Standard Model can appear as a low-energy limit if the standard embeddings and breaking pattern are used.  The shape of the spacetime factor is negotiable: the locked conoid is consistent, but it is not what supplies the gauge group or the matter index, and it is not required for Dual-Zero.

**What Dual-Zero arithmetic does and does not change (docs 53–54).**  
Paired-zero arithmetic restores exact results of truncation and rounding, with `Fraction` as ground truth.  Re-running constants, \(\alpha\), Yukawa overlaps, spectral sums, and one-loop running found **no genuine change**: exact zeros stayed zeros, fits stayed fits, and no new selection of flux, area, or \(\tau\) appeared.  The obstruction is missing structure, not lost bits.

**What is already known to fail, and should not be revived as a claim.**

- An almost-commutative product of the raw conoid with the CCM finite triple \(F\) is 2-dimensional, not a 4D CCM model (doc 45).  A spectator conoid does not change the CCM coupling ratios or the Higgs relation at \(\Lambda\).
- The APS index of the untwisted truncated conoid is \(0\), not \(3\) (docs 44, 46).  Counting four tip nodes or twelve “bridges” is not a derivation of three generations (docs 49–51).
- The SAM-2 ultrafilter Dual-Zero is not a well-defined regulator; \(0.05\) is not the \(E_8\) adjoint Casimir; quoted values such as \(1/\alpha=137.035999084\) are experimental inputs restated with free parameters (doc 51, confirmed in doc 54).
- May 2026 2I representation theory does not prove three generations; the listed irrep dimensions do not even sum to \(|2I|\) (doc 51).
- \(\omega_0\approx 0.927\) and the exponent \(4/13\) are not derived (docs 18, 42–43, 54).  \(G_N=64\pi\ell_0^2/45\) is a convention lock (docs 18, 42, 54).
- Candidate principles surveyed in docs 49–50, and the Dual-Zero axiom test in doc 52, produced no unique flux \(M=3\) and no unique area.  Two conflicting mechanisms can already fix \(\tau\): maximizing \(\det'\Delta\) selects the hexagonal torus; \(C_4\) compatibility selects the square torus.

---

## 2. Authentic GUT — research targets

An authentic grand unified theory, in the sense of this repository, would derive a single gauge structure that contains the Standard Model, with anomaly-free matter, coupling unification that is a prediction rather than a fit, a viable breaking chain, and fermion masses and mixings as outputs — all while keeping Dual-Zero.  The items below are what must still be found.

### 2.1 Gauge group (Pati–Salam, \(\mathrm{SO}(10)\), \(\mathrm{SU}(5)\)) from the finite spectral triple

**Status:** partial.  
Pati–Salam \(\mathrm{SU}(2)_L\times\mathrm{SU}(2)_R\times\mathrm{SU}(4)\) and the Chamseddine–Connes–Marcolli algebra that yields the Standard Model are both usable as a choice of finite triple \(F\).  \(\mathrm{SO}(10)\) and \(\mathrm{SU}(5)\) appear in earlier SAM-2 / desktop text as chain claims, not as derived finite geometries in this repository.

**Update (doc 56, 23 Nov 2026).** Reproduced numerically: with a \(\nu_R\) Majorana entry the first-order condition cuts \(\mathbb H_R\oplus\mathbb H_L\oplus M_4(\mathbb C)\) to the maximal subalgebra \(\mathbb C\oplus\mathbb H\oplus M_3(\mathbb C)\); dropping it keeps PS.  The axioms (KO-6, grading, irreducibility, order zero/one) are assumed.  An isospectral counterexample proves no purely spectral regulator (Dual-Zero included) can select them.  Status: derived *from assumed axioms*; not from Dual-Zero or the conoid.

**Update (doc 59).** Best lead: Chamseddine–Connes–Mukhanov quanta of geometry give \(M_2(\mathbb H)\oplus M_4(\mathbb C)\) from Clifford algebras \(Cl(5,0)\), \(Cl(0,5)\) (verified); the grading commutant is the PS algebra.  Replaces two axioms by one new one.  A Dual-Zero link would need a new operator-level axiom (proposal only).

**Tried in docs 44–54.**  
Doc 45 uses the CCM finite triple with \(N=3\) and the fermion multiplicity as inputs.  Docs 47–48 develop the Pati–Salam product as the more flexible option in the cited literature.  Doc 49 surveys NCG classification and does not uniquely force PS, CCM, \(\mathrm{SO}(10)\), or \(\mathrm{SU}(5)\).  Doc 51 finds that the SAM-2 \(E_8\) descent is not a derivation.  Doc 54 does not change the verdict: the group remains a choice of \(F\).

**Next calculation or theorem.**  
A uniqueness (or sharp classification) theorem: under the finite-spectral-triple axioms actually used (KO-dimension, reality, first-order, orientability, and the requirement of a viable SM embedding), show that \(F\) is forced, or list the remaining discrete family and the extra assumption that would cut it to one.  Do not put the group in by hand and then call it derived.

**Falsifiable test.**  
If every consistent finite triple that unifies still requires an extra input equivalent to choosing the group, uniqueness has failed.  If a derived \(F\) predicts a gauge boson, a coupling relation, or an extra massless factor already excluded by data, that \(F\) is ruled out.

### 2.2 Anomaly freedom of the actual product spectrum

**Status:** partial.  
Standard Pati–Salam and SM fermion embeddings are anomaly-free in the usual textbook sense.  That has been *used*, not re-proved from the product’s actual zero-mode content, including any extra modes of the conoid, the orbifold, or the magnetized surface.

**Tried in docs 44–54.**  
Docs 45 and 48 assume standard content.  Docs 47 and 50 record extra orbifold and flux sectors (for example several \(T^2/\mathbb{Z}_4\) fluxes with an invariant sector of dimension \(3\)).  No complete anomaly polynomial for the product spectrum was computed.

**Next calculation or theorem.**  
Compute the gauge and mixed anomalies of every light fermion mode of the chosen product (including would-be exotics and orbifold singlets).  Show cancellation without dropping modes by hand, or state which modes must get large masses and from which term in the spectral action those masses come.

**Falsifiable test.**  
A leftover light exotic with an uncancelled gauge anomaly, or an uncancelled anomaly in the chosen spectrum, kills that product.

### 2.3 Coupling unification without fitting (one-loop / two-loop, with thresholds)

**Status:** open as a *prediction*.  
One-loop meeting of the Pati–Salam couplings, with measured SM couplings at \(M_Z\) as inputs, determines \(m_R\approx 4.205\times 10^{13}\,\mathrm{GeV}\) and \(\Lambda\approx 2.399\times 10^{15}\,\mathrm{GeV}\) (docs 48, 54).  That is a fit of the meeting condition, not a derivation of the scales or of the low-energy couplings.

**Update (doc 55, 23 Nov 2026).** Done at two loops (Machacek–Vaughn coefficients computed exactly from group data, top Yukawa, MS-bar matching, thresholds ×/÷10): \(m_R=3.90\times10^{13}\), \(\Lambda=1.19\times10^{15}\) GeV, \(\alpha_U^{-1}=44.4\) (one loop: \(4.22\times10^{13}\), \(2.41\times10^{15}\)).  Threshold band \(\log_{10}m_R\in[12.96,14.23]\), \(\log_{10}\Lambda\in[14.77,15.39]\).  Still zero degrees of freedom: a passed consistency check, not a prediction.  Status unchanged: open as a prediction.

**Tried in docs 44–54.**  
Docs 45 and 48 run one-loop (CCM and PS).  Doc 54 confirms that float64, Dual-Zero, and `mpmath` agree at the \(10^{-17}\) level on \(\log m_R\); rounding did not invent the scales.  Two-loop running and a derived threshold set were not used as predictions.

**Next calculation or theorem.**  
Derive \(g(\Lambda)\) and the breaking / threshold scales from the spectral action (Seeley coefficients, the geometry of \(\Sigma\), and the finite triple), then run down — at least two-loop, with those thresholds — and compare \((\alpha_1,\alpha_2,\alpha_3)(M_Z)\) to PDG values *without* adjusting the scales to force a meeting.

**Falsifiable test.**  
The predicted \((\alpha_1,\alpha_2,\alpha_3)(M_Z)\) miss experiment by more than a controlled theoretical error (truncation of the \(\beta\)-functions, threshold scheme, and higher Seeley terms).  Agreement after retuning \(m_R\) or \(\Lambda\) does not count.

### 2.4 Proton decay bounds

**Status:** open.  
No proton-lifetime calculation appears in docs 44–54.

**Update (doc 57, 23 Nov 2026).** In the spectral PS model \(B=(F+X)/4\) is exact perturbatively (no \(\varepsilon_{ABCD}\) arises from a trace); no gauge- or scalar-mediated nucleon decay, no \(n\)–\(\bar n\).  A generic \(d=6\) operator at \(\Lambda\) would give \(\tau\approx10^{32}\) yr (excluded), so exactness is load-bearing.  \(K_L\to\mu e\) passes by \(\sim10^7\).  Status: closed for this content (null prediction).

**Tried in docs 44–54.**  
The unification scales above were obtained as a PDG fit.  They were not converted into a decay rate, nor compared to Super-Kamiokande / Hyper-Kamiokande limits.

**Next calculation or theorem.**  
For the chosen breaking pattern (PS, \(\mathrm{SU}(5)\), or \(\mathrm{SO}(10)\)), write the leading baryon-number-violating operators, compute the effective scale from the *derived* (not fitted) heavy masses, and obtain \(\tau(p\to e^+\pi^0)\) and the principal competing modes, with a stated uncertainty.

**Falsifiable test.**  
A predicted lifetime below the current experimental lower bound, with no remaining free scale, rules out that breaking chain in this framework.

### 2.5 Symmetry breaking and the Higgs sector from the spectral action

**Status:** partial.  
The spectral action produces Higgs-like scalars and a potential, in the standard almost-commutative way.  A spectator conoid does not change the CCM Higgs relation at \(\Lambda\) (doc 45).  The product does not yet yield a unique Higgs mass or unique PS-breaking vacuum expectation values (docs 48, 54).

**Update (doc 58, 23 Nov 2026).** Spectral boundary values with PS-fixed \(n=(y_\nu/y_t)^2=1\) and the singlet \(\sigma\), run down: \(m_H\approx168\) GeV (151 GeV with the measured top) vs 125.1.  125 GeV needs \(n\approx2\), not allowed with one bidoublet.  \(v\) and \(m_R\) remain \(f_2\Lambda^2\) inputs.  Status: prediction made; it fails in the minimal content.

**Update (doc 59).** σ with own running, Majorana Yukawa and movable threshold: \(m_H=167\)–169 GeV; thresholds: 167–169; gravity \((\Lambda/M_{\rm Pl})^2\sim10^{-7}\).  Only a free \(n=(y_\nu/y_t)^2\) (extra Yukawa content, 1 parameter) reaches 125.1 GeV.

**Update (doc 60).** Full two-loop SM running below \(m_R\) with NNLO matching (Buttazzo et al.): \(m_H=180.5\pm1.8\) GeV with σ, 190.5 GeV without (vs 125.1).  Benchmark reproduced (\(\lambda(M_{\rm Pl})=-0.0144\)).

**Update (doc 61).** With the top fixed by extra Higgs-coupled fermions in \(F\), \(m_H=140\)–159 GeV for any multiplet (PS 16 pair: 146).  Reaching 125.1 needs a second parameter (larger \(y_\nu\)), which forces \(\sum m_\nu\ge0.18\) eV in the minimal seesaw.

**Tried in docs 44–54.**  
Doc 45 records the standard CCM relation and that the raw conoid \(\times F\) is the wrong dimension.  Doc 48 treats the Higgs and PS-breaking scalars as part of the product action, without a unique vacuum derived from the geometry.  Yukawa and vacuum-expectation-value scales are absorbed or scanned, not fixed.

**Next calculation or theorem.**  
Derive the full Higgs potential of the product, including the fields that break Pati–Salam (or \(\mathrm{SU}(5)\) / \(\mathrm{SO}(10)\)) to the Standard Model, with coefficients fixed by Seeley terms and the geometry.  Obtain the breaking scales, \(v\), and \(m_H\) without a fit, or prove that the potential does not determine them.

**Falsifiable test.**  
A unique \(m_H\) from the product that disagrees with \(125\,\mathrm{GeV}\) beyond the theoretical error, or the absence of any vacuum that breaks the group to the Standard Model, falsifies that Higgs sector.

### 2.6 Fermion masses and mixings as outputs

**Status:** open.  
The Cremades–Ibáñez–Marchesano overlap mechanism exists and was implemented.  Masses and CKM / PMNS angles are not outputs.  At \(\tau=i\) and vanishing Wilson lines, many Yukawa entries are structural zeros; turning on Wilson lines fills them (docs 47–48, 54).

**Update (doc 58, 23 Nov 2026).** The spectral relation \(y_t(\Lambda)=g\) (PS, \(n=1\)) predicts \(M_t\approx186\) GeV vs 172.5 (8% high).  Seesaw with \(M_N=m_R\) gives \(m_{\nu_3}\approx0.18\) eV; \(0.05\) eV needs \(M_N\approx3.6\,m_R\) (fitted Majorana coupling).

**Update (doc 59).** With \(n\) fitted to \(m_H\), \(M_t=175.5\)–176.4 GeV (one-loop) / 180 GeV (two-loop top running): the one remaining prediction misses by 2–5%; a full two-loop PS Higgs-sector analysis is the next calculation.  \(0\nu\beta\beta\): nonzero (Majorana); NO 1.5–3.7 meV, IO 18–48 meV.

**Update (doc 60).** Two-loop + NNLO matching: zero-parameter \(M_t=190.4\pm1.2\) GeV (+15σ vs 172.5); extension (b) with \(n\) fitted to \(m_H\): \(M_t\approx179\)–180 ± 1.3 GeV (≈6σ).  The top miss is real; \(y_t(\Lambda)\) must be ≈20% below \(g_U\).

**Update (doc 61).** Structure search, Dual-Zero untouched: an extra Higgs-coupled fermion trace \(x\approx2.1\) in \(F\) (1 parameter) fits \(M_t\).  Ruled out: a large \(y_\nu\) alone (Higgs destabilised), PS chains and \(\Lambda\) shifts (187–194 GeV), the SM-group/Boyle–Farnsworth variant (185–190), and twisted/grand symmetry (190–194).  Flux towers preserve \(y_t/g\) exactly (no-go).  ω₀-type factors are numerology.

**Update (doc 62).** The "Flower of Life" tested as its lattice (hexagonal \(T^2\), \(T^2/\mathbb Z_{3,6}\)) and the 4D version (\(D_4\) \(T^4\), \(T^4/\mathbb Z_3\to\) K3): neither forces 3 generations or vector-like states.  The hexagonal texture is democratic.  Its light-generation share would give \(M_t\approx172\)–174 but implies \(m_c/m_t\approx0.6\) (excluded).  \(D_4\) leaves \(M_t=190.4\) and needs \(M_c\gtrsim\Lambda\) to keep unification.

**Update (doc 63).** Principle search (anomalies, KO/Poincaré duality/orientability, first order, doubling, index, quanta of geometry, Poincaré sphere): nothing forces Higgs-coupled vector-like fermions, and orientability forbids exact VL copies.  With the spectral gauge trace counted, the top needs \(\Delta a=2.20+2.07\,\Delta N\), and the fitted Higgs is 149–161 GeV.  The ω₀³ near miss gives \(M_t=171.8\), \(M_h=139\)–151 GeV and is not counted (input ω₀, post-hoc exponent, P(chance) ≈ 84%).

**Update (doc 64).** Cube-inspired structures (A₄, S₄, O_h, Δ(27), T′, T₇ flavour groups; T³ cube and its orbifolds; Ezekiel, ark and seven-fold notes; scripture used as inspiration only): parameter-free textures are degenerate (m_c = m_t, M_t 141 or 160), fitted textures leave M_t = 190.36, M_h = 180.50.  The A₄ TBM prediction (s₁₃ = 0) is excluded at 39σ and forces V_CKM = 1 in PS.  Cube internal spaces are vector-like unless magnetized (then m_c/m_t ≥ 0.12); KK shells below Λ spoil unification.

**Update (doc 65).** "Ripple then settle" (displaced internal radion, Hubble-damped, Planck 2018 background; imagery as inspiration only): the spectral-action potential is flat in the Einstein frame, so m_φ is free.  With the natural coupling and φ_i ~ M_Pl it passes only for m_φ ≳ 100 TeV (natural Λ²/M_Pl ≈ 6×10¹¹ GeV decays at 10⁻²² s, T_RH ~ 10⁸ GeV), leaving no observable α variation.  Light versions fail EP/fifth-force tests (η ≈ 0.25κ²) or need φ_i ≲ 10⁻⁶.  It has no effect on M_t = 190.36, M_h = 180.50.

**Update (doc 66).** Coupled ripples (linear/kinetic mixing, cubic/quartic transfer, Mathieu resonance, extra dissipation, degenerate/hierarchical masses): everything still settles, and doc 65 changes only for a light partner (m₂/m₁ < 1.5×10⁻⁷) or super-gravitational damping (safe mass 94 → 9 TeV at 10³×).  Finite universe (T³, S³, Poincaré dodecahedral) vs Planck 2018 low ℓ: best Δχ² = −3.1 (T³) and −1.9 (PDS), but those sizes are excluded by matched circles and Planck+BAO Ω_k.  The allowed range gives Δχ² ≥ −1.0.  Top/Higgs unchanged.

**Update (doc 67).** The y_t/g and λ/g² boundary relations are an a₄ theorem, independent of f.  Derived mechanisms tested: CC 2012 σ (M_h 190.5 → 180.5, M_t unchanged, m_σ ≈ 1.2×10¹⁴ GeV), PS without first order, a₆ moments (flat f: 0; e^{-u}: −3%; entropy f: −0.6%; need −36%), product geometries (invariant), computed thresholds (±0.9 GeV), gravity (10⁻⁸), and outliers.  None moves M_t below 189 GeV.  Mechanisms that hit 172.5 need input and fail the Higgs (151 GeV, or unstable).

**Update (doc 68/69).**
- **Matter content (68).** Higgs-blind content gives y_t/g = √(I_L/6) ≥ 1, so the best zero-parameter top is 187.1 GeV. Fixing the top with Higgs-coupled content always leaves M_h = 147–161 GeV.
- **Multistage PS → LR → SM.** The top is flat at 191.2 GeV.
- **SUSY spectral (S0 traces).** The top is 179–185 GeV, with tan β fixed at ≈ 57. The BvdBvS traces fail unification.
- **Combination.** SUSY + 1 VL pair with universal y gives M_t = 168.4. With the share fitted, it gives 172.5 / 124 at M_S = 10 TeV, but that is 2 parameters for 2 observables.
- **Verdict: no-go for derived solutions.** The minimal extra assumption is a VL pair with c ≈ 0.88 y_t (+ SUSY at ~10 TeV for the Higgs).

**Update (doc 70).** One-loop SUSY thresholds (BGSS 1407.4081) and two-loop MSSM Yukawa RGEs were added for candidate #10.
- Δy_t and Δ_b at tan β ≈ 67 together give +2 GeV.
- With M_S fitted to M_h = 125.1 (degenerate spectrum, X_t = 0, μ > 0), M_t = 170.5 GeV, which is −1.6σ.
- Reaching 172.5 needs X_t ≈ −(1.6…2.4) M_S, a second fitted number.
- Across all scanned spectra, M_t at M_h = 125.1 spans 166.1–172.9 GeV.

**Update (doc 71).** Shawn's idea "time as a medium with reflecting banks" was tested against real data.
- Planck TT echo search: the best Δχ² is 5.9 (linear) and 8.6 (log), with look-elsewhere p = 0.98 and 0.59. Excluded as a detection (A ≲ 1.2%).
- CCC rings (WMAP 9-yr): consistent with Gaussian sims (p 0.2–0.8). GW echoes: none in GWTC-2/3.
- Dispersion: |Δv/c| < 10⁻¹⁵ (GW170817) and |n−1| < 3.3×10⁻¹⁹ (GRB 090510). α drift: |ε| ≲ 3×10⁻⁸ (clocks). A future bank is untestable.
- No effect on Dual-Zero, M_t or M_h.

**Tried in docs 44–54.**  
Docs 47–48 compute Yukawa tensors as functions of \(\tau\) and Wilson lines and label scans as underdetermined fits.  Doc 51 rejects May fitted CKM figures as claims.  Doc 54 confirms that the tiny entries at vanishing Wilson lines are not rounding artefacts (grid refinement changes them by at most \(8\times 10^{-16}\); Dual-Zero does not lift them to \(O(1)\)).

**Next calculation or theorem.**  
A principle that fixes \(\tau\), the area, and the Wilson lines (and the Higgs slice, if several zero modes compete), followed by a parameter-free computation of the Yukawa singular values and the CKM and PMNS matrices.

**Falsifiable test.**  
The derived mass ratios or mixing angles disagree with PDG values beyond the stated theoretical error.  A scan that can hit the data by moving Wilson lines is not a derivation.

---

## 3. Authentic TOE — research targets

An authentic theory of everything, in the sense of this repository, would be a single consistent framework that contains an authentic GUT, includes gravity as a quantum theory rather than only as an effective spectral-action term, and fixes the remaining free numbers — \(\omega_0\), the \(G_N\) prefactor, the flux, the moduli, and the choice of \(F\) — by a principle, while also addressing the cosmological constant, dark matter, and the low-energy Standard Model as predictions.  Dual-Zero is to be kept.

### 3.1 Quantum gravity beyond the effective spectral action

**Status:** open (effective level only).  
The spectral action supplies an Einstein–Hilbert term, a cosmological term, and higher-curvature Seeley contributions.  That is a classical / effective gravitational action, not a completed ultraviolet quantum gravity.

**Tried in docs 44–54.**  
Docs 45–50 and 52 analyse heat-kernel and Seeley densities on the product and on alternative surfaces.  No graviton-loop observable, no ultraviolet completion, and no derived black-hole entropy theorem are part of the locked or exploratory record in those documents.

**Next calculation or theorem.**  
Specify the quantum theory of this spectral action (or a controlled ultraviolet completion) and derive one observable that is not already fixed by the classical Einstein–Hilbert term — for example a leading higher-curvature correction, a well-defined gravitational cutoff, or a one-loop gravitational amplitude — with Dual-Zero used only in its defined role as a regulator of functions of a spectral parameter.

**Falsifiable test.**  
A predicted correction to Newton’s law, or a post-Newtonian or higher-curvature parameter, that lies outside experimental bounds; or an inconsistency (ghosts, negative residues, an ill-posed initial-value problem) in the higher Seeley terms once they are treated dynamically.

### 3.2 A principle that fixes \(\omega_0\), the \(G_N\) prefactor, the flux, the moduli, and the choice of \(F\)

**Status:** open.  
This is the main missing principle.  \(\omega_0\) is an input; \(G_N=64\pi\ell_0^2/45\) is a convention lock; \(M\), the area, \(\tau\), and the Wilson lines are choices (or, for \(\tau\), outputs of two *conflicting* mechanisms); \(F\) is a choice of finite geometry.

**Tried in docs 44–54.**  
Docs 42–43 and 54 test natural geometric candidates for \(\omega_0\) and the exponent \(4/13\) and do not recover \(0.927\).  Docs 44–46 rule out the conoid index and the tip as a source of \(3\).  Docs 47–50 and 52 test index theory, modular invariants, regularised determinants, orbifolds, tadpoles, product spectral-action extrema, a declared coincidence scan, and the standalone Dual-Zero axiom, on several surfaces, without a unique flux or area; \(\det'\Delta\) prefers the hexagonal torus, \(C_4\) prefers the square torus.  Doc 54 confirms that Dual-Zero arithmetic does not move those rankings.

**Next calculation or theorem.**  
State a selection principle that is not “count four nodes or twelve bridges,” is not a fit of a free parameter, and does not merely maximise a functional already known to conflict with another equally natural functional.  Show that it yields unique values for \((\omega_0,\,G_N/\ell_0^2,\,M,\,A,\,\tau,\,F)\), or a discrete list short enough to be checked item by item.  Alternatively, prove that no such principle exists inside this class of geometries.

**Falsifiable test.**  
The principle’s unique output is incompatible with a viable low-energy theory (wrong chirality, no Standard Model embedding, or couplings already excluded).  Two equally natural principles that disagree, as already happens for \(\tau\), also falsify uniqueness until an independent reason is given to keep one and discard the other.

### 3.3 Cosmological constant

**Status:** open.  
The spectral action contains a volume / cosmological term.  The observed cosmological constant is not derived.

**Tried in docs 44–54.**  
Docs 48–50 distinguish finite-part functionals from divergent ones and do not obtain the observed vacuum energy.  Dual-Zero \(\operatorname{Reg}_2\) was not used as a replacement for a residue, and doc 52 did not convert a regulated determinant into \(\rho_\Lambda\).

**Next calculation or theorem.**  
Extract the predicted cosmological term from the Dual-Zero-regulated spectral action, with the cutoff and the finite-part prescription fixed by the *same* principle that is supposed to fix \(G_N\), and compare the result to the observed dark-energy density.

**Falsifiable test.**  
A unique predicted \(\rho_\Lambda\) that differs from the observed density by many orders of magnitude, with no remaining scheme choice, is a failure of that prescription.  A result that still depends on an unfixed cutoff is not yet a prediction.

### 3.4 Dark matter

**Status:** open.  
The framework does not currently have a derived, calculable dark-matter candidate.  A May-era quoted direct-detection cross section is not a derivation and is not part of the locked or honest exploratory record (doc 51).

**Tried in docs 44–54.**  
CCM content, used as in doc 45, does not automatically supply a stable electrically neutral relic.  Pati–Salam and orbifold products (docs 47–50) may have extra states; those states were not shown to be stable, to have the right relic density, or to pass direct-detection bounds.

**Next calculation or theorem.**  
Identify any stable, electrically neutral mode of the product (a leftover PS state, a sterile sector, or a geometrical zero mode) and compute its relic density and direct-detection cross section from the *same* parameters used for the GUT, with no extra abundance fit.

**Falsifiable test.**  
No such state exists in the spectrum; or the computed relic density or spin-independent cross section is excluded by observation, once the GUT parameters are fixed.

### 3.5 Low-energy Standard Model limit with genuine predictions

**Status:** partial as a *scheme*; open as a *prediction*.  
The Standard Model can be a low-energy limit if the embeddings and the breaking pattern are chosen to be the standard ones.  No Standard Model parameter is yet an output of the geometry plus Dual-Zero.

**Tried in docs 44–54.**  
Docs 45, 48, and 54 run down with measured couplings as inputs.  Masses, mixings, and \(\alpha(M_Z)\) are not predicted.  The Dual-Zero re-run did not turn any of those inputs into outputs.

**Next calculation or theorem.**  
Produce at least one numerical Standard Model (or near-Standard-Model) observable — a coupling, a mass ratio, a rare decay, or a scale — with every input fixed by the principles of §§2–3, then compare it to data.

**Falsifiable test.**  
That observable misses experiment beyond the stated theoretical error.  Until such an observable exists, the framework remains a scheme, not a TOE.

---

## 4. Suggested order of work

These are research targets, listed in a sensible order, not a claim that the next one will succeed.

1. Finish the anomaly inventory of the actual product spectrum (§2.2).  A hidden anomaly would stop the line immediately.
2. Decide, or derive, the finite triple \(F\) (§2.1) and write the Higgs / breaking potential of that product (§2.5) with coefficients from the spectral action.
3. Search again for a selection principle for \((M,A,\tau)\) and for \(\omega_0\) and the \(G_N\) prefactor (§3.2), now constrained to be compatible with the potential of step 2, and without counting nodes or bridges.  An honest null remains acceptable.
4. Only after the scales are no longer fitted, compute coupling unification at two loops with thresholds (§2.3), proton decay (§2.4), and Yukawa outputs (§2.6).
5. Treat gravity as a quantum / higher-Seeley theory (§3.1), and only then extract a cosmological term (§3.3), a dark-matter candidate (§3.4), and one genuine low-energy prediction (§3.5).

---

## 5. Plain-language bottom line

The locked geometry and the Dual-Zero regulator are in good mathematical order, within the scope stated in the core paper and in docs 18 and 52.  There is already a consistent *scheme* that can house gravity, a gauge group, and chiral matter together, with the Standard Model as a possible low-energy limit.  That is not yet an authentic GUT, and it is not yet an authentic TOE, because the gauge group, the flux, the moduli, Newton’s prefactor, and the Dual-Zero scale are still choices or convention locks, and because masses, couplings, proton decay, the cosmological constant, and dark matter are not predictions.

What has to be found is listed above, with a next calculation and a way to fail for each item.  Dual-Zero arithmetic will keep the numerics honest.  It will not replace a missing principle.
