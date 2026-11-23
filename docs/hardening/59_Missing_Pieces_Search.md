# 59. Search for the missing pieces: masses, new predictions, gauge-group selection (exploratory)

**Date:** 23 November 2026 (America/Chicago)
**Status:** exploratory. This does not lock a new core theorem, and the Dual-Zero regulator is unchanged (docs 18, 52).
**Code:** `experiments/two_loop_pati_salam/missing_pieces.py`, `report_59.py`; numbers in `results_doc59.json`.
**Tests:** `tests/test_missing_pieces.py`.
**Authorized by:** Shawn, "Ok look for the missing pieces."

---

## Plain-language summary (for Shawn)

- **Can anything fix the top and Higgs masses without adding a knob?** **No.** Four known fixes were tested as real calculations:
  - **(a) Heavy singlet \(\sigma\).** Gave it its own running, its neutrino coupling, and its own mass threshold, each varied over sensible ranges. Higgs stays at **167–169 GeV** (149–152 GeV with the measured top). No fix.
  - **(b) Extra Higgs content** that lets the neutrino and top couplings differ. This does fix the Higgs at 125.1 GeV, but it costs **one free number**. With that number used up, the top comes out **175.5–176.4 GeV** (one-loop) or **~180 GeV** (two-loop top running), against 172.5. The one remaining prediction still misses, by 2–5%.
  - **(c) Heavy-particle thresholds**, the ×/÷10 band of doc 55. The masses barely move: top 184.7–186.7 GeV, Higgs 167–169 GeV.
  - **(d) Gravity and higher spectral terms.** Too small by about ten million times (\((\Lambda/M_{\rm Pl})^2\approx2\times10^{-7}\)). Hitting the data would need the top coupling at \(\Lambda\) lowered by 15% and the Higgs self-coupling halved.
- **Score.** Predictions minus parameters is never positive *with* all hits. The best case, (b), is 2 masses − 1 parameter = 1 prediction, and that prediction (the top mass) misses.
- **New testable predictions.**
  - The new heavy particles (\(\sigma\), \(W_R\), \(Z'\), leptoquark) all sit near \(10^{13}\)–\(10^{14}\) GeV, far beyond any collider.
  - Testable now: the proton should never decay (doc 57); neutrinos are Majorana, so neutrinoless double-beta decay must happen.
  - With normal ordering and a nearly massless lightest neutrino, the rate is \(|m_{\beta\beta}|\approx1.5\)–3.7 meV, below the next generation of experiments. Inverted ordering would give 18–48 meV, which they can see.
- **Gauge group.** The best published lead is Chamseddine–Connes–Mukhanov's "quanta of geometry": a quantization rule built from Clifford algebras produces exactly \(M_2(\mathbb H)\oplus M_4(\mathbb C)\). The code checks those Clifford algebras. Adding a left/right grading cuts this down to the Pati–Salam algebra (also checked).
  - This swaps two assumed axioms for one new one, which is real progress but not a derivation from nothing.
  - The Dual-Zero regulator still cannot pick the group (doc 56 theorem). The only possible link is a *new* proposal: read Dual-Zero's ± pair as the two Clifford signs. That is not tested and is not part of Dual-Zero today.
- **Top missing pieces, ranked:**
  1. The Clifford/"quanta" principle (fixes the group's origin).
  2. A full two-loop Higgs-sector calculation in Pati–Salam (decides if the 2–5% top miss is real).
  3. A principle that fixes \(m_R\) or \(\Lambda\) (the only way unification becomes a prediction).
  4. Extra Higgs content (fixes the Higgs, costs a parameter).
  5. Gravity corrections: ruled out as a fix.

---

## 1. Masses: four candidate repairs, computed

**Model.** This is the doc 58 setup, generalized:
- independent \(y_t\) and \(y_\nu\);
- singlet \(\sigma\) with quartic \(\lambda_\sigma\), portal \(\kappa\), and Majorana Yukawa \(y_N\) (one dominant \(\nu_R\)), with Machacek–Vaughn terms \(Y_2(S)=y_N^2\) and \(H=6y_N^4\) per Weyl \(N\);
- a movable \(\sigma\) threshold \(m_\sigma\in[m_R/10,m_R]\), with the SM + \(\sigma\) segment in between;
- spectral boundary values at \(\Lambda\) (CC2012) as functions of \(g_U\) and \(n=(y_\nu/y_t)^2\).

With \(n=1\) and \(y_N=0\) it reproduces doc 58 (185.76 GeV and 168.12 GeV; tested).

### (a) The \(\sigma\) singlet (Chamseddine–Connes 2012; also Devastato–Lizzi–Martinetti "grand symmetry", where \(\sigma\) comes from the grand algebra; and Boyle–Farnsworth, where \(\sigma\) is complex with \(B-L=2\))

| \(y_N(\Lambda)\) | \(m_\sigma/m_R=0.1\) | 0.3 | 1 |
|---|---|---|---|
| 0 | 167.3 | 167.7 | 168.1 |
| \(g/2\) | 167.3 | 167.7 | 168.1 |
| \(g\) | 167.3 | 167.7 | 168.2 |
| \(2g\) (spectral value for one dominant \(\nu_R\)) | 167.9 | 168.2 | 168.7 |

These are \(m_H\) values in GeV, with \(M_t\) predicted at 185.8 GeV throughout. Using the measured top instead gives \(m_H=149.4\)–151.7 GeV. **No fix, no new parameter.** The tree-level \(\sigma\) threshold already gives the full reduction factor (0.68 in doc 58). Running \(y_N\) and moving the threshold change \(m_H\) by \(<2\) GeV.

### (b) Extended content, \(y_\nu\ne y_t\) (CCvS 2013/2015 Dirac operators without first order; a \((2,2,15)\) Yukawa)

In PS with one bidoublet, \(n=1\). A second Yukawa structure (for example a \((2,2,15)\) coupling) frees \(n\), at a cost of **one parameter**.

| content and running | \(n\) fitted to \(m_H=125.1\) | \(M_t\) predicted |
|---|---|---|
| composite, \(y_N=0\), one-loop \(y_t\) | 1.99 | **176.4 GeV** |
| composite, \(y_N=2g\), one-loop \(y_t\) | 2.09 | **175.5 GeV** |
| composite, \(y_N=0\), SM two-loop \(y_t\) | 2.06 | **180.8 GeV** |
| composite, \(y_N=2g\), SM two-loop \(y_t\) | 2.16 | **179.9 GeV** |
| complex \((2,2,15)\) light down to \(m_R\) (new two-loop unification: \(m_R=3.86\times10^{13}\), \(\Lambda=1.45\times10^{15}\), \(\alpha_U^{-1}=41.2\)) | 2.11 | **179.0 GeV** |

Fitting \(n\) to the top instead (\(n\approx2.45\)) gives \(m_H=72\) GeV, and the \((2,2,15)\) case is unstable. **One parameter cannot hit both masses.** The leftover prediction \(M_t\) is 2–5% high.

The size of the shift from one-loop to two-loop top running (+5 GeV) is itself the current theory error. A complete two-loop PS-segment and threshold analysis is needed before calling this a firm failure (rank 2 below).

Caution: Besnard (J. Phys. A 55 (2022) 065201) shows that a weakened first-order condition applied to Pati–Salam *removes* the \(\nu_R\) Majorana term. That would remove \(\sigma\) and the seesaw. Extended-content routes must avoid that condition.

### (c) PS thresholds at \(m_R\) (doc 55 band, 40 samples, \(n=1\) with \(\sigma\))

\(M_t\in[184.7,186.7]\) GeV, \(m_H\in[167.2,169.0]\) GeV, \(\log_{10}\Lambda\in[14.6,15.4]\). The boundary relations depend only on \(g_U\), which the thresholds hardly move (\(\alpha_U^{-1}=44.1\)–44.8). **No fix.** There are no thresholds "at \(\Lambda\)": the spectral action defines the theory there and has no heavier states.

### (d) Gravity and higher spectral moments

- Gravitational corrections to running below \(\Lambda\) scale as \((\Lambda/\bar M_{\rm Pl})^2=2.4\times10^{-7}\).
- The \(a_6\) Seeley term multiplies dimension-6 operators by \(f_{-2}/\Lambda^2\). It does not change the dimension-4 ratios, which come from \(a_4\) and are independent of the moments (doc 58).
- To hit the data, the boundary values would need \(y_t(\Lambda)\to0.847\,y_t\) and, with that top, \(\lambda_h(\Lambda)\to0.47\,\lambda_h\). Those are 15% and 53% corrections, which cannot come from \(10^{-7}\) effects.
- Fitting them would be **2 parameters for 2 masses, so 0 predictions**.

### Ledger

| repair | new parameters | mass observables | net predictions | hits |
|---|---|---|---|---|
| minimal spectral PS (doc 58) | 0 | 2 | 2 | 0 |
| (a) \(\sigma\), \(y_N\), threshold (motivated ranges) | 0 | 2 | 2 | 0 |
| (b) free \(n\) (extra Yukawa content) | 1 | 2 | 1 | 0 of the remaining 1 (\(M_t\) 2–5% high) |
| (c) thresholds | 0 | 2 | 2 | 0 |
| (d) gravity / \(a_6\) | 0 (too small) or 2 (fit) | 2 | 2 or 0 | 0 or trivial |

**Nothing fixes both masses with zero new parameters.** The literature claims of \(m_H\approx125\) GeV (CC2012; CCvS2015) correspond to row (b): one fitted parameter.

## 2. New testable predictions

| item | value | testable? |
|---|---|---|
| \(\sigma\) mass | \(\sqrt{2\lambda_\sigma}\,w\sim m_R\sim10^{13}\)–\(10^{14}\) GeV | no |
| \(W_R\), \(Z'\), \(X_{LQ}\) | \(\sim m_R\) (\(K_L\to\mu e\) passes by \(10^7\), doc 57) | no |
| proton decay | none (exact \(B\), doc 57) | yes, as a null result (Hyper-K) |
| \(n\)–\(\bar n\) | none | yes, null result |
| Majorana neutrinos / \(0\nu\beta\beta\) | nonzero. With lightest mass 0 (NuFIT 6.0): normal ordering \(|m_{\beta\beta}|=1.5\)–3.7 meV; inverted 18–48 meV | inverted ordering is reachable by LEGEND-1000 / nEXO; normal ordering is not |
| top mass in route (b) | 175–181 GeV | already disfavoured |

The PS relation \(m_D\approx M_u\) is known to favour strongly hierarchical \(\nu_R\) masses and normal ordering. That is a tendency, not computed here. If it holds, next-generation \(0\nu\beta\beta\) sees nothing from this model. **No new prediction is both distinctive and near-term testable**, apart from the nulls.

## 3. Gauge-group selection without assuming the axioms

| principle | what it gives | assumed instead | link to Dual-Zero |
|---|---|---|---|
| **Quanta of geometry** (Chamseddine–Connes–Mukhanov, JHEP 12 (2014) 098; PRL 114 (2015) 091302): two-sided higher Heisenberg relation \(\tfrac1{4!}\langle Y[D,Y]^4\rangle=\gamma\), \(Y^2=1\) | Clifford algebras \(C_+=Cl(5,0)\cong M_2(\mathbb H)\oplus M_2(\mathbb H)\) and \(C_-=Cl(0,5)\cong M_4(\mathbb C)\), hence \(M_2(\mathbb H)\oplus M_4(\mathbb C)\). **Verified** here: \(Cl(5,0)\) has central volume element with \(\omega^2=+1\) and 16-dimensional irreducible span (one \(M_2(\mathbb H)\)); \(Cl(0,5)\) spans all 32 dimensions, \(M_4(\mathbb C)\). Grading commutant in \(M_2(\mathbb H)\) has real dimension 8, \(=\mathbb H_R\oplus\mathbb H_L\), giving the **PS algebra** | the 4D quantization relation, real structure, grading | the two signs \(\kappa=\pm\) (two quanta) form a ± pair like Reg₂'s \(\lambda\pm\delta\). This is an analogy only; making it a theorem would need a new operator-level Dual-Zero axiom |
| KO-dimension 6 from Lorentzian signature (Barrett JMP 48 (2007) 012303; Connes JHEP 11 (2006) 081) | KO-6 removes fermion doubling and allows the Majorana term | Lorentzian signature, physical fermion content | none |
| Second-order / non-associative (Boyle–Farnsworth NJP 16 (2014) 123027; NJP 17 (2015) 023021) | SM \(\times U(1)_{B-L}\) plus complex \(\sigma\) (\(B-L=2\)) | their reformulated axioms | none; selects \(B-L\), not PS |
| Weak order-one (Besnard 2022) | in \(B-L\) extension: two Higgs doublets + \(\sigma\); in PS: **kills the Majorana term** | weak C1 | none |
| Krein / twisted spectral triples (Bizi–Brouder–Besnard JMP 59 (2018); Devastato–Farnsworth–Lizzi–Martinetti JHEP 03 (2018) 089) | Lorentzian structure from a twist; \(\sigma\) from grand symmetry | twist automorphism | the twist is a \(\mathbb Z_2\) flip, structurally similar to Dual-Zero's ± symmetry; not a derivation |

**Dual-Zero.** The doc 56 theorem stands: the current regulator (a functional of the spectrum) is blind to \(A\), \(J\) and \(\gamma\). None of the published principles is a spectral functional; all are operator-level conditions. A link would therefore need a new axiom, for example "the Dual-Zero pair is realised by \(Y_\pm\) with \(Y_\pm^2=1\)". That is a hypothesis to test, not a result, and it leaves the existing regulator definition intact.

## 4. Ranked missing pieces

| rank | missing piece | fixes | costs | status |
|---|---|---|---|---|
| 1 | **Quanta-of-geometry / Clifford principle** for \(F\) | origin of \(M_2(\mathbb H)\oplus M_4(\mathbb C)\supset\) PS; replaces irreducibility + "\(a=2\)" | a new axiom (higher Heisenberg relation); grading and \(J\) still assumed; no mass fix | published; Clifford structure verified here |
| 2 | **Full two-loop PS Higgs-sector analysis** (two-loop \(y_t\), \(y_\nu\), quartics above and below \(m_R\); one-loop threshold matching of \(\lambda\)) | decides whether route (b)'s 2–5% top miss is real | no parameters, only work | open; current spread 5 GeV |
| 3 | **A principle that fixes \(m_R\) or \(\Lambda\)** (for example \(f_2\)-moment ratio fixing \(w/\Lambda\)) | turns doc 55's zero-dof meeting into a prediction of \(\sin^2\theta_W\) or \(\alpha_s\) | a new principle; none known | open |
| 4 | **Extended scalar content** (\(n\ne1\)) | \(m_H=125.1\) | 1 parameter + extra multiplets; \(M_t\) still 2–5% high; must avoid Besnard's condition | computed (route b) |
| 5 | Gravity / higher moments | nothing | — | ruled out (\(10^{-7}\)) |

**Verdict.**
- The mass problem is real: no zero-parameter repair exists among (a)–(d).
- The gauge-group problem has one serious published lead (rank 1), which does not involve Dual-Zero as currently defined.
- Dual-Zero remains a well-posed regulator and computational tool. Making it select structure would require a new, explicitly stated operator-level axiom.
