# 61. Search for the structure that lowers the spectral top Yukawa (exploratory)

**Date:** 23 November 2026 (America/Chicago)
**Status:** exploratory. No new core theorem is locked. The **Dual-Zero regulator is untouched**: the generator \(\varepsilon(n)=\omega_0(-1)^n n^{-n}\) and the symmetric \(\operatorname{Reg}_2\) of docs 18 and 52 appear nowhere in the modified pieces. Every candidate changes the finite geometry \(F\), the spectrum, or the gauge group, never the regulator.
**Code:** `experiments/two_loop_pati_salam/top_yukawa_search.py` and `report_61.py`; numbers are in `results_doc61.json`.
**Tests:** `tests/test_top_yukawa_search.py`.
**Authorized by:** Shawn: "Search for the next structure that does that while keeping dual zero intact."

---

## Plain-language summary (for Shawn)

- **The target.** Doc 60 showed that the spectral rule gives the top quark a coupling of 0.531 at the unification scale. The measured top needs about 0.427, about 20% lower. I tested seven kinds of new structure in the doc 60 two-loop pipeline. Each one gets a parameter count, the predicted top and Higgs masses, and whether Dual-Zero survives. Dual-Zero survives in all seven, because none of them touches the regulator.
- **What works for the top.** Adding extra heavy fermions ("vector-like" states, heavier than \(10^{13}\) GeV) that also couple to the Higgs. The spectral rule fixes the *sum* of all Yukawa couplings squared. If new fermions take part of that sum, the top gets less. One number is needed (the extra share, about 2.1 in top units), so the top mass is **fitted, not predicted**.
  - The Higgs mass then comes out at **140–159 GeV** depending on what the new fermions are. A full extra copy of a Pati–Salam family gives 146 GeV. That is still far from 125 (about 10–19 standard deviations).
  - Neutrino masses stay viable.
- **What fixes both, at a price.** The extra fermions plus a larger tau-neutrino Yukawa (two numbers) give 172.5 and 125.1 together. That is a fit with nothing left over to predict.
  - It runs into a real problem: the simplest seesaw then makes neutrinos too heavy, with a mass sum of at least 0.18 eV. Cosmology allows below 0.12 eV.
- **What does not work:**
  - **A big tau-neutrino Yukawa alone.** It fixes the top, but the singlet σ then drags the Higgs negative (an unstable vacuum). The neutrinos also come out too heavy.
  - **Moving the unification scale** (other breaking chains, extra scalars, a higher or lower boundary). Every Pati–Salam chain gives 189–194 GeV. The top would only come out right if the boundary sat near \(10^{8}\) GeV, where the forces do not unify, and the Higgs would then be 190 GeV.
  - **Flux/Landau-level towers from the magnetized surface.** This is a clean no-go. The extra modes change the top coupling and the gauge coupling by exactly the same amount, so their ratio cannot move. The top shifts by 0.006 GeV.
  - **A "natural" factor from Dual-Zero (ω₀ = 0.927).** The needed factor is 0.803 (0.791–0.814). \(\omega_0^3=0.797\) and \(4/5\) land in that window. About 1.75 hits are expected by chance from the list tried, and neither is derived, so this is **numerology**. Even taken at face value, it leaves the Higgs at 140–151 GeV.
  - **The Boyle–Farnsworth / Connes–Chamseddine Standard-Model-group version:** 185–190 GeV.
  - **Twisted spectral triples / grand symmetry:** 190–194 GeV, unchanged from doc 60, because they do not change the trace rule.
- **Bottom line.** No structure tested fixes the top *as a prediction*. The cheapest honest repair is one extra-fermion parameter, which fixes the top but not the Higgs. Fixing both needs two parameters and conflicts with neutrino masses in the minimal seesaw. The top and Higgs failures of the spectral rule therefore point to an \(F\) that holds more Higgs-coupled fermions, plus something beyond the minimal σ for the Higgs.

---

## 1. Setup

**Pipeline (doc 60).**
- Below \(m_R\): two-loop SM running, with the Buttazzo et al. NNLO matching at \(M_t\).
- Above \(m_R\): Pati–Salam two-loop gauge running, with one-loop Yukawa and quartic running.
- Baseline: \(m_R=4.22\times10^{13}\) GeV, \(\Lambda=1.24\times10^{15}\) GeV, \(g_U=0.531\).
- Baseline result: \(M_t=190.36\), \(M_h=180.50\) GeV.
- Error bars are those of doc 60, about ±1.2 GeV (\(M_t\)) and ±1.8 GeV (\(M_h\)). Pulls use these errors combined with the measurement errors.

**Generalized spectral boundary at \(\Lambda\)** (CC2012 traces, in units of \(y_t\)):
- \(a=\operatorname{Tr}Y^\dagger Y/y_t^2=3+n+x\) (plus \(b\) and \(\tau\)).
- \(b=\operatorname{Tr}(Y^\dagger Y)^2/y_t^4=3+n^2/p+x_4\).
- \(y_t^2=4g^2/a\), \(\lambda=4g^2b/a^2\), \(\lambda_{h\sigma}=4g^2\,2n/a\), \(\lambda_\sigma=8g^2\).
- Here \(n=\sum_i y_{\nu_i}^2/y_t^2\), shared equally by \(p\) generations, and \((x,x_4)\) is the trace of extra Higgs-coupled fermions.
- With \(p=1\) and \(x=x_4=0\) this is the doc 58–60 boundary exactly (tested).

**Required.** \(y_t(\Lambda)=0.427\) (data) against 0.531, so \(a\approx6.2\) in place of 4.

## 2. Candidates

### (1) Large Dirac neutrino Yukawa (generation structure in the trace)

| case | \(n\) for \(M_t=172.5\) | \(M_h\) (GeV) | seesaw |
|---|---|---|---|
| \(p=1\), σ, \(y_N=0\) | 3.02 | **−1.8** (λ<0: unstable) | \(M_N\) must be \(3.8\times10^{14}\) GeV, so \(y_N\approx4.8\) (non-perturbative); \(m_\nu=0.45\) eV at \(M_N=m_R\) |
| \(p=1\), σ, \(y_N=2g\) | 3.02 | 42.6 | same |
| \(p=3\) (democratic), σ | 2.47 | λ ≪ 0 | \(m_\nu\approx0.14\) eV each at \(M_N=m_R\); excluded by Σ\(m_\nu\) |
| \(p=1\), no σ | 3.05 | 172.5 | as above |
| \(p=3\), no σ | 3.05 | 159.7 | as above |

- **Parameters:** 1 (\(n\)).
- **Realization:** a \((2,2,15)\) Yukawa admixture (pure \((2,2,15)\) gives \(y_\nu=-3y_t\), so \(n=9\)). The mixing angle is the parameter.
- **Verdict:** fixes \(M_t\) by construction but destroys the Higgs once the spectral σ portal is included, since \(\lambda_{h\sigma}\propto n\). Without σ the Higgs is 160–173 GeV. A type-I seesaw needs a non-perturbative \(y_N\).
- **Dual-Zero intact:** yes.

### (2) Extra fermions in \(F\): vector-like states or extra copies (Dirac mass \(\ge m_R\))

The extra Yukawa trace is fixed by \(M_t\): \(x=2.10\). Its distribution, \(x_4=x^2/m\) for multiplicity \(m\), then predicts \(M_h\):

| content | \(m\) | \(y_X/y_t\) | \(M_t\) | \(M_h\) (GeV) | pull \(M_h\) |
|---|---|---|---|---|---|
| VL lepton doublet+singlet | 1 | 1.45 | 172.5 (fit) | 159.0 | +19σ |
| VL quark doublet+singlet | 3 | 0.84 | 172.5 (fit) | 148.1 | +13σ |
| **VL PS 16+16̄** | 4 | 0.72 | 172.5 (fit) | **146.4** | **+12σ** |
| two VL 16 pairs | 8 | 0.51 | 172.5 (fit) | 143.5 | +10σ |
| three VL 16 pairs | 12 | 0.42 | 172.5 (fit) | 142.4 | +10σ |
| limit \(x_4\to0\) | ∞ | →0 | 172.5 | 140.2 | +8.5σ |

**Discrete zero-continuous-parameter choices with \(y_X=y_t\):**

| choice | \(M_t\) | \(M_h\) |
|---|---|---|
| +1 VL quark pair | 166.3 | 141.9 |
| +1 full PS 16 copy | 160.1 | 133.5 |
| +2 VL lepton pairs | **173.2** (+0.6σ) | 152.0 |

\(y_X=y_t\) is not forced by the spectral action, since Yukawas in \(D_F\) are free matrices. So the last row is a choice, not a prediction.

Lowering \(m_\sigma\) or raising \(y_N\) moves \(M_h\) by only about 2 GeV.

**Neutrinos.** Because \(y_\nu\) drops with \(y_t\), the seesaw limit relaxes: \(m_\nu^{\min}=0.041\) eV with a perturbative \(y_N\), compared with 0.062 eV in the doc 60 baseline.

- **Parameters:** 1 (\(x\)), plus the discrete multiplet.
- **New testable prediction:** \(M_h\ge140\) GeV for any content. This fails.
- **Dual-Zero intact:** yes.

### (3) Changing \(\Lambda\): breaking chain, scalar thresholds, boundary scale

**PS chains (boundary at the unification point):**

| chain | \(\Lambda\) (GeV) | \(M_t\) | \(M_h\) |
|---|---|---|---|
| composite | \(1.24\times10^{15}\) | 190.4 | 180.5 |
| \((1,1,15)\) light | \(2.80\times10^{15}\) | 191.2 | 181.7 |
| \((2,2,15)\) light | \(1.51\times10^{15}\) | 193.7 | 187.4 |

**Moving the boundary off the meeting point:** \(\mu_B/\Lambda=0.01\to5\) gives \(M_t=187.1\to191.3\). A higher \(\Lambda\) makes it worse; a lower one helps slowly.

**Data ratio** \(y_t(\mu)/g_2(\mu)\) along SM running:
- 0.82 at \(10^{15}\) GeV;
- 0.77 at \(10^{18}\) GeV;
- 1 at \(10^{8.2}\) GeV.

With an SM-group boundary forced at \(10^{8.16}\) GeV, \(M_t=172.5\) with no parameters, but \(M_h=190\) GeV, and \(g_1,g_2,g_3\) are far from equal there. New matter would have to bring unification down to \(10^8\) GeV and then also fix the Higgs.

- **Parameters:** 0 for the chains; 1 (\(\Lambda\)) plus new matter otherwise.
- **Verdict:** no.
- **Dual-Zero intact:** yes.

### (4) Magnetized-surface Landau-level towers (repo machinery: `ps_conoid_product/flux_mechanisms.py`)

**Spectrum.**
- Levels sit at \(E_k=M_c\sqrt k\), each with degeneracy \(|M|=3\) (index = flux).
- Each level carries a Dirac copy of the three-generation matter, giving \(\Delta b=8\) per level (universal).
- The Higgs couples level \(k\) to level \(k\) with the zero-mode Yukawas.

**Exact identity.** Per level, the tower adds
\[
\delta\frac{d\ln(y_t/g)}{dt}\propto 2(3+n)y_t^2-\tfrac83\cdot3\,g^2=0\quad\text{when } y_t^2(3+n)=4g^2 ,
\]
so the spectral relation is tower-invariant. This holds for every \(n\) (tested).

| \(M_c/\Lambda\) | levels at \(\Lambda\) | \(g(\Lambda)\) | \(M_t\) | \(M_h\) |
|---|---|---|---|---|
| 1 | 1 | 0.531 | 190.36 | 180.5 |
| 0.5 | 4 | 0.543 | 190.36 | 181.0 |
| 0.3 | 11 | 0.574 | 190.36 | 182.1 |
| <0.15 | — | Landau pole below \(\Lambda\) | — | — |

If the Higgs did not couple to the towers, the top would get worse (192–196 GeV).

**Caveat:** non-universal gauge KK modes are not included; they would move the unification point rather than \(y_t/g\).

- **Parameters:** 1 (\(M_c\)).
- **Verdict:** a structural no-go.
- **Dual-Zero intact:** yes.

### (5) Canonical factor (Dual-Zero / geometry), checked as numerology

**Required factor:** \(r=y_t/y_t^{\rm spec}=0.803\), with \([0.791,0.814]\) for ±1σ on \(M_t\).

**Tested list (14 numbers):** \(\omega_0^{k}\) for \(k=\tfrac12,1,2,3,\tfrac{13}4\), \(4/5\), \(\sqrt{2/3}\), \(\sqrt{5/8}\), \(\pi/4\), \(\sqrt{3/5}\), \(e^{-1/4}\), \(\sqrt{4/7}\), \(1/\sqrt\varphi\), …, plus Dual-Zero generator values \(1+\varepsilon(n)\) and \(\operatorname{Reg}_2\) averages.

**Hits:** \(\omega_0^3=0.797\) and \(4/5\). The expected number of chance hits is 1.75. The Dual-Zero generator values (0.97–1.23) do not hit.

**Effect on the Higgs:** even if imposed, \(M_h=151\) GeV (Yukawa factor only) or 140 GeV (a Higgs-normalization factor, \(\lambda\propto r^4\)).

- **Parameters:** 0 nominally, but the choice of the factor is the parameter.
- **Verdict:** numerology, not counted.
- **Dual-Zero intact:** yes. Using \(\omega_0\) as a Yukawa factor would be a *new* use, not a change of the regulator. It is not adopted.

### (6) Boyle–Farnsworth second-order / \(B-L\) + complex σ (SM gauge group, spectral boundary at \(g_2=g_3\) or \(g_1=g_2\))

The \(B-L\) gauge factor and the complex σ leave \(\operatorname{Tr}Y^\dagger Y\) and the \(SU(2)\) normalization unchanged, so the CC trace boundary applies with \(g=g_2\).

| boundary | \(\log_{10}\Lambda\) | \(m_\sigma=M_N\) | \(M_t\) | \(M_h\) |
|---|---|---|---|---|
| \(g_2=g_3\) | 16.47 | \(10^{11}\) / \(10^{13}\) | 188.8 / 189.5 | 174.2 / 176.6 |
| \(g_2=g_3\), no σ | 16.47 | — | 189.5 | 186.8 |
| \(g_1=g_2\) | 13.08 | \(10^{11}\) / \(10^{13}\) | 185.0 / 185.8 | 170.1 / 175.4 |
| \(g_2=g_3\), \(n\) fitted | 16.47 | \(10^{13}\) | 172.5 (fit, \(n=2.96\)) | 72.2 |

- **Parameters:** 0 (or 1 with \(n\)).
- **Verdict:** no. This is the known CCM top problem, now at two loops.
- **Dual-Zero intact:** yes.

### (7) Twisted spectral triples / grand symmetry (Devastato–Lizzi–Martinetti)

The twist produces σ (and in some versions a vector \(X_\mu\)) without changing the Yukawa traces. The scalar content is that of the PS rows:

| version | \(M_t\) | \(M_h\) |
|---|---|---|
| grand symmetry (σ from twist), composite | 190.4 | 180.5 |
| + \((2,2,15)\) | 193.7 | 187.4 |
| + \((1,1,15)\) | 191.2 | 181.7 |

- **Parameters:** 0.
- **Verdict:** no.
- **Dual-Zero intact:** yes.

### Combination (1)+(2): extra fermions plus a larger \(y_\nu\) (two parameters)

| content | \(n\) | \(x\) | \(M_t\) | \(M_h\) |
|---|---|---|---|---|
| VL PS 16 pair | 1.80 | 1.27 | 172.5 | 125.1 |
| VL quark pair | 1.83 | 1.24 | 172.5 | 125.1 |

Zero predictions remain.

**Test.** Type-I seesaw with the largest perturbative \(y_N(m_R)=2.0\), so that \(y_N(\Lambda)\le\sqrt{4\pi}\):
- \(m_\nu^{\min}=0.073\) eV;
- \(\sum m_\nu\ge0.18\) eV, above the cosmological 0.12 eV.

Feeding that \(y_N\) back moves \(M_h\) to 127.9 GeV. The point survives only with a non-minimal neutrino sector (for example inverse or type-II seesaw).

- **Dual-Zero intact:** yes.

## 3. Ranking

| rank | structure | added params | \(M_t\) (GeV) | \(M_h\) (GeV) | new testable output | Dual-Zero |
|---|---|---|---|---|---|---|
| 1 | (2) VL / extra Higgs-coupled fermions in \(F\) | 1 (\(x\)) | 172.5 (fit) | 140–159 (PS 16 pair: 146 ± 1.8) | \(M_h\ge140\): **fails**; \(m_\nu\) viable | intact |
| 2 | (1)+(2) combination | 2 | 172.5 (fit) | 125.1 (fit) | Σ\(m_\nu\ge0.18\) eV: **in tension** (minimal seesaw) | intact |
| 3 | (1) large \(y_\nu\) alone | 1 | 172.5 (fit) | <0 with σ; 160–173 without | non-perturbative \(y_N\) | intact |
| 4 | (3) \(\Lambda\) shift | 0 / 1+ | 187–194; 172.5 only at \(10^{8.2}\) | 180–190 | — | intact |
| 5 | (6) SM-group / BF | 0 | 185–190 | 170–187 | — | intact |
| 6 | (7) twisted / grand | 0 | 190–194 | 181–187 | — | intact |
| 7 | (4) flux towers | 1 | 190.36 (unchanged) | 180–182 | no-go identity | intact |
| — | (5) ω₀-type factor | (0) | numerology | 140–151 | — | intact, not adopted |

## 4. Verdict

1. **The search is honestly null.** No structure keeps the parameter count at zero and gets the top right. The cheapest repair is one parameter: an extra Higgs-coupled fermion trace \(x\approx2.1\) (in \(y_t^2\) units) in \(F\), at or above \(m_R\). It fits \(M_t\) and leaves \(M_h=140\)–159 GeV, a failed prediction.
2. **Two parameters fit both masses** (\(n\approx1.8\), \(x\approx1.3\)) but predict a neutrino mass sum of at least 0.18 eV in the minimal type-I seesaw. That is excluded by cosmology unless the neutrino sector is enlarged.
3. **Clean negative results:**
   - flux towers preserve \(y_t/g\) exactly;
   - no PS breaking chain or boundary-scale shift helps;
   - SM-group and twisted variants keep the CCM top problem;
   - ω₀-type factors are numerology.
4. **Dual-Zero is intact in every case.** The top and Higgs problem is in the finite geometry (Yukawa content) and the Higgs sector, not in the regulator.
5. **Next step (§3.1 of the roadmap):** derive from an axiom (for example the quanta-of-geometry Clifford principle of doc 59) whether \(F\) must contain extra Higgs-coupled multiplets, and with what multiplicity. Then the \(x\) of candidate (2) would no longer be free, and \(M_h\approx146\) GeV would be a sharp, failing prediction unless the Higgs sector is extended too.

## 5. Approximations

- The PS segment (Yukawa, quartic, σ) runs at one loop, as in doc 60.
- Extra fermions decouple at \(m_R\).
- Vector-like states are degenerate.
- Flux towers use a continuous level count, universal matter towers only, and no gauge KK modes.
- The seesaw uses tree-level type-I with \(v_R\approx m_R/g_R\).
- Error bars are those of doc 60, not recomputed per candidate.
