# 57. Proton decay and rare decays in the spectral Pati–Salam model (exploratory)

**Date:** 23 November 2026 (America/Chicago)
**Status:** exploratory. This does not lock a new core theorem.
**Code:** `experiments/two_loop_pati_salam/phenomenology.py`; numbers in `results_docs56_58.json`.
**Scales used:** two-loop composite \(m_R=3.90\times10^{13}\) GeV, \(\Lambda=1.19\times10^{15}\) GeV, \(\alpha_U^{-1}=44.4\) (doc 55).

---

## Plain-language summary (for Shawn)

- **Force carriers do not decay protons.** In SU(5)-type theories, protons decay through heavy \(X,Y\) bosons. Pati–Salam does not have them. Its new heavy boson (the \(SU(4)\) "leptoquark") turns a quark into a lepton, but it keeps baryon number and lepton number each conserved.
- **The Higgs fields do not either, in this model.** The rule is simple. Baryon number can only break through a term with a four-index "epsilon" contraction in \(SU(4)\). The spectral action is built from traces of matrices, and traces never make an epsilon. So in this model the proton is stable at every order of perturbation theory. Only ultra-tiny tunnelling effects remain, and they cannot destroy a single proton.
- **Why this matters.** If some generic baryon-violating term *did* exist at the top scale \(\Lambda\), the proton would live about \(10^{32}\) years. Super-Kamiokande has already ruled that out: the bound is \(>2.4\times10^{34}\) years. Exact baryon number is essential to the model, and the model has it.
- **Rare kaon decay \(K_L\to\mu e\).** It needs the leptoquark above about 1400 TeV. Here it is about \(10^{10}\) TeV, so it passes by a factor of roughly ten million.

---

## 1. Operator analysis

**Charges.** Let \(F=\#4-\#\bar4\) be the \(SU(4)\) index number. \(F_L\) and \(\Delta_R\) have \(F=+1\); \(F_R\) (left-handed \(\bar4\)) has \(-1\); \(\phi\), \(\Sigma\) and the gauge bosons have \(0\). Components of a 4 carry \(X=B-L\): \(+\tfrac13\) for quarks and \(-1\) for leptons. Then
\[
B=\frac{F+X}{4},\qquad L=\frac{F-3X}{4}
\]
reproduces \(B,L\) for every component.

**Lemma.** An \(SU(4)\)-invariant monomial has \(\Delta F=0\) if it uses only \(\delta\)-contractions, and \(\Delta F=\pm4\) for each \(\varepsilon_{ABCD}\). The vev \(\langle\Delta_R\rangle\) sits in the lepton component (\(F=1,X=-1\Rightarrow B=0\)). It breaks \(X\) and \(L\), but not \(B\). **Hence \(B\) is exact iff no \(\varepsilon\) term is present.**

| operator | contraction | \(\Delta F\) | \(\Delta B\) |
|---|---|---|---|
| Dirac Yukawa \(F_L\phi F_R\) (top \(=\nu_D\)) | \(\delta\) | 0 | 0 |
| Majorana \(F_RF_R\Delta\Delta\) (\(\nu_R\nu_R\langle\Delta\rangle^2\)) | \(\delta\) | 0 | 0 |
| leptoquark current \(\bar q\gamma^\mu\ell X_\mu\) | \(\delta\) | 0 | 0 |
| \(u^ce^c\Delta_q\langle\Delta_\ell\rangle\) (from the Majorana term) | \(\delta\) | 0 | 0 |
| \(\varepsilon\Delta^4\) (\(\supset qqq\ell\)) | \(\varepsilon\) | 4 | 1 |
| \(\varepsilon F_LF_L\Delta\Delta\to qq\Delta_q\langle\Delta_\ell\rangle\) | \(\varepsilon\) | 4 | 1 |
| \(d=6\) \(qqq\ell\) | \(\varepsilon\) | 4 | 1 |

**Renormalizable couplings of \(\Delta_R=(2,1,4)\) to fermions.** The bilinears are \((4,2,1)^2=(6\oplus10,1\oplus3,1)\), \((\bar4,1,2)^2=(\bar6\oplus\overline{10},1,1\oplus3)\) and \((4,2,1)(\bar4,1,2)=(1\oplus15,2,2)\). None contains a single \(4\) or \(\bar4\), so there are none. The colour-triplet scalar \(\Delta_R\supset(3,1,-\tfrac13)\) couples to fermions only through the Majorana-type term, and only in the \(q\ell\) channel (\(\Delta B=0\)).

**Spectral action.**
- \(\operatorname{Tr}f(D_A/\Lambda)\) and \(\langle J\psi,D_A\psi\rangle\) are traces and bilinears of operators on \(H_F\), so only \(\delta\)-contractions appear and no \(\varepsilon\) term is generated at \(\Lambda\).
- \(U(1)_F\) is vector-like under \(SU(4)\), so it is non-anomalous there, and the RG flow does not generate \(\varepsilon\) terms below \(\Lambda\).
- \(U(1)_F\) is anomalous under \(SU(2)_L\) and \(SU(2)_R\). The resulting instantons violate \(B\) only in units of \(\Delta B=3\), with rate \(\propto e^{-16\pi^2/g^2}\sim e^{-560}\).

**Conclusion.** \(\tau_p=\infty\) in perturbation theory; there is no \(p\to e^+\pi^0\), \(p\to\bar\nu K^+\), or similar mode. Likewise \(n\)–\(\bar n\) (\(\Delta B=2\)) is forbidden. (If \(\Delta_R\) were replaced by \((10,1,3)\), as in Mohapatra–Marshak models, \(\Delta B=2\) could appear. That is not the CCvS content.)

## 2. What a generic B-violating operator would give

Take \(\mathcal L\supset\kappa\,A\,g_U^2\,qqq\ell/M^2\), with \(A\approx2.5\), lattice \(W_0=0.131\) GeV², and an SU(5)-like chirality factor:
\[
\Gamma=\frac{m_p}{32\pi}\Big(1-\frac{m_\pi^2}{m_p^2}\Big)^2|C|^2W_0^2\times5 .
\]
This is an order-of-magnitude estimate (factor \(\sim3\) in \(\tau\)).

| \(M\) | \(\tau(p\to e^+\pi^0)\) for \(\kappa=1\) | vs Super-K \(2.4\times10^{34}\) yr |
|---|---|---|
| \(\Lambda_{2\text{-loop}}=1.19\times10^{15}\) GeV | \(1.1\times10^{32}\) yr | excluded unless \(\kappa<0.067\) |
| \(\Lambda_{1\text{-loop}}=2.41\times10^{15}\) GeV | \(1.9\times10^{33}\) yr | excluded |
| \(\Lambda\) (with 15) \(=2.70\times10^{15}\) GeV | \(3.0\times10^{33}\) yr | excluded |
| \(m_R=3.9\times10^{13}\) GeV | \(1.3\times10^{26}\) yr | excluded |

So the model is **only** viable because \(B\) is exact (section 1). Physics *above* \(\Lambda\) that generated \(\varepsilon\)-type operators (for example gravitational effects) would have to be suppressed by more than \(M_{\rm Pl}\)-scale factors.

## 3. Rare meson decays and the SU(4) leptoquark

\(M_X\simeq g_4v_R/\sqrt2\) with \(v_R\sim m_R\), so \(M_X\sim(0.3\text{–}3)\,m_R\ge1.2\times10^{10}\) TeV.

| bound | value | margin |
|---|---|---|
| \(K_L\to\mu^\pm e^\mp\) (Valencia–Willenbrock 1994, permutation mixing) | \(M_X>1400\) TeV | \(10^{6.9}\) |
| general mixing (Smirnov 2018, \(K_L,B,B_s\to\ell\ell'\)) | \(M_X>86\) TeV | \(10^{8.1}\) |
| \(\mu\to e\) conversion, \(\pi\to e\nu/\mu\nu\) | \(\lesssim10^3\) TeV | passes |
| \(n\)–\(\bar n\) | \(\tau>4.7\times10^8\) s (Super-K 2021) | forbidden by exact \(B\) |

**Passes all of them.** The flip side is that these rare decays are unobservable in this model. A positive signal of \(K_L\to\mu e\) at current sensitivity would falsify a single-scale PS with \(m_R\sim10^{13}\) GeV.

## 4. Verdict

- Proton decay **does not constrain** the spectral PS model: \(B\) is exact perturbatively, which is a structural result (no \(\varepsilon\) in a trace). It is also a **null prediction**: Hyper-Kamiokande should see nothing from this sector.
- Generic \(d=6\) operators at \(\Lambda\) would be excluded by about \(10^{2}\) in lifetime, so exactness is load-bearing.
- \(K_L\to\mu e\) and related bounds pass by about seven orders of magnitude.
