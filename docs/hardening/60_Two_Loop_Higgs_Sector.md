# 60. Two-loop Higgs-sector calculation in the spectral Pati–Salam model (exploratory)

**Date:** 23 November 2026 (America/Chicago)
**Status:** exploratory. This does not lock a new core theorem; the Dual-Zero regulator is unchanged.
**Code:** `experiments/two_loop_pati_salam/two_loop_higgs.py`, `report_60.py`; numbers in `results_doc60.json`.
**Tests:** `tests/test_two_loop_higgs.py`.
**Authorized by:** Shawn, "Keep going." (ranked item 2 of doc 59).

---

## Plain-language summary (for Shawn)

- **The question.** Was the top-quark miss of docs 58–59 (2–5% in the one-parameter version, 8% in the minimal one) an artifact of rough one-loop running? I redid everything at two loops: full Standard Model running, proper conversion between the measured masses and the running couplings, and an honest error bar.
- **The answer: the miss is real, and it gets bigger.** With zero free parameters:
  - **Top quark:** predicted **190.4 ± 1.2 GeV**, against 172.5 ± 0.3 measured. That is 18 GeV too heavy, about **15 standard deviations**.
  - **Higgs, with the singlet \(\sigma\):** predicted **180.5 ± 1.8 GeV**, against 125.1 (about 31 standard deviations).
  - **Higgs, without \(\sigma\):** 190.5 GeV.
  - **With the extra \((2,2,15)\) field:** top 193.7 GeV, Higgs 187.4 GeV.
- **Why it got worse.** Two-loop QCD makes the top coupling grow faster on the way down from the high scale, adding about 6–7 GeV to the predicted top mass. The calculation was checked first: it reproduces the textbook Standard Model result (the Higgs self-coupling turns negative near \(10^{10}\) GeV, and at the Planck scale it equals −0.0144 against the published −0.0143). It also reproduces the measured top when fed the measured coupling (172.54 GeV).
- **The one-parameter fix (b).** Tuning the neutrino/top ratio to give a 125.1 GeV Higgs leaves the top at **179–180 GeV** (183 GeV with \((2,2,15)\)). That is still about **6 standard deviations** too heavy.
- **Bottom line.** The spectral-action boundary relation for the top coupling, \(y_t(\Lambda)=g\) in Pati–Salam, is ruled out at the unification scale this model produces. It is not a small rounding-level miss. Fixing it needs new structure that changes the top coupling at \(\Lambda\) by about 20% (0.43 needed vs 0.53 predicted), not better arithmetic.

---

## 1. What was computed

**Below \(m_R\): two-loop SM.**
- Couplings run: \((g_Y,g_2,g_3,y_t,y_b,y_\tau,\lambda)\), with \(V=\lambda|H|^4\).
- Two-loop gauge, \(y_t\) and \(\lambda\) betas from Machacek–Vaughn / Ford–Jack–Jones / Luo–Wang–Xiao. Two-loop \(y_b\) and \(y_\tau\) terms are omitted; they enter at the \(10^{-4}\) level.
- Optional three-loop pure-QCD terms (\(\gamma_m^{(2)}\), \(\beta_{QCD}^{(2)}\), \(n_f=6\)), used to estimate missing higher orders.
- The gauge coefficients are cross-checked against the exact group-theory matrix of doc 55 (tested).

**Matching at \(M_t\).** The NNLO MS-bar couplings at \(\mu=M_t\) of Buttazzo et al. (arXiv:1307.3536, eqs. 57–60) are used:
- \(y_t(M_t)=0.93690+0.00556(M_t-173.10)-0.00042\,\delta\alpha_s\), with error \(\pm0.0005\). This includes 3-loop QCD and NLO EW in the pole \(\to\) MS-bar conversion.
- \(\lambda(M_t)=0.12604+0.00206(M_h-125.15)-0.00004(M_t-173.10)\), with error \(\pm0.0003\). This includes the one- and two-loop Higgs-mass thresholds.
- Predictions invert these: \(y_t\to M_t\) pole, then \(\lambda\to M_h\) pole.

**Benchmark (two-loop + 3-loop QCD, Buttazzo inputs).**

| quantity | here | Buttazzo et al. (NNLO) |
|---|---|---|
| \(\lambda(M_{\rm Pl})\) | −0.0144 | −0.0143 |
| scale where \(\lambda=0\) | \(10^{9.8}\) GeV | \(\sim10^{10}\) GeV |
| \(y_t(M_{\rm Pl})\) | 0.391 | 0.38 (they include full 3-loop) |

At one loop the same run gives \(\lambda(M_{\rm Pl})=-0.034\), which is why one loop is not enough.

**Above \(m_R\).**
- \(m_R\) and \(\Lambda\) come from the doc 55 two-loop solve, rerun with this SM running: \(m_R=4.22\times10^{13}\) GeV, \(\Lambda=1.24\times10^{15}\) GeV, \(g_U=0.531\).
- Pati–Salam gauge couplings run at two loops (exact coefficients).
- \(y_t\), \(y_\nu\), \(\lambda\), \(\kappa\), \(\lambda_\sigma\) and \(y_N\) run with the doc 59 system at one loop. The PS two-loop Yukawa piece is estimated by an SU(4)-scaled QCD-type term and enters the error budget only. The PS segment is short: \(\ln(\Lambda/m_R)=3.4\).

**Boundary at \(\Lambda\) (CC2012, PS \(n=1\)).** \(y_t^2(3+n)+3y_b^2+y_\tau^2=4g^2\), plus the \(\lambda_h\), \(\lambda_{h\sigma}\), \(\lambda_\sigma\) relations of doc 58. \(y_b\) and \(y_\tau\) are taken from data. \(\sigma\) is integrated out at tree level at \(m_\sigma\) (default \(m_R\)).

**Closure test.** Feeding in the bottom-up \(y_t(\Lambda)\) from data instead of the spectral relation returns \(M_t=172.54\) GeV. The pipeline is consistent to 0.04 GeV.

## 2. Results (zero new parameters)

| scenario | \(M_t\) pred (GeV) | pull vs 172.5 ± 0.3 | \(M_h\) pred (GeV) | pull vs 125.1 |
|---|---|---|---|---|
| **composite + \(\sigma\)** | **190.4 ± 1.2** | **+14.7σ** | **180.5 ± 1.8** | +31σ |
| composite, no \(\sigma\) | 190.4 ± 1.2 | +14.7σ | 190.5 ± 1.2 | +56σ |
| \((2,2,15)\) light + \(\sigma\) | 193.7 ± 1.5 | +13.7σ | 187.4 ± 2.5 | +25σ |
| (for comparison) one-loop SM below \(m_R\) | 183.8 | | 175.9 | |
| quartic boundary only, measured \(y_t\) | (input) | | 151.4 | |

**Error budget, composite + \(\sigma\)** (shift in GeV, \(M_t\) / \(M_h\)):

| source | \(\delta M_t\) | \(\delta M_h\) |
|---|---|---|
| missing higher orders (adding 3-loop QCD) | +0.24 | +0.18 |
| boundary scale \(\mu_B=\Lambda\times2^{\pm1}\) | ±0.42 | ±0.42 |
| PS two-loop Yukawa (proxy) | +0.21 | +0.39 |
| \(\sigma\) threshold \(m_\sigma=m_R/10\) | −0.06 | −1.23 |
| matching (Buttazzo theory error) | ±0.09 | ±0.15 |
| **theory total** | **0.55** | **1.39** |
| \(\alpha_s\pm0.0009\) | ±0.62 | ±0.50 |
| heavy thresholds at \(m_R\) (×/÷10, std of 10 samples) | ±0.84 | ±0.96 |
| **total** | **1.18** | **1.76** |

## 3. The one-parameter extension (b) at two loops

With \(n=(y_\nu/y_t)^2\) freed by extra Yukawa content and fitted to \(m_H=125.1\):

| case | fitted \(n\) | \(M_t\) pred (GeV) |
|---|---|---|
| composite + \(\sigma\), \(y_N=0\) | 2.07 | **180.2** |
| composite + \(\sigma\), \(y_N=2g\) | 2.18 | **179.3** |
| \((2,2,15)\) light + \(\sigma\) | 2.19 | **182.8** |

Error estimate: the same budget (\(\approx1.2\) GeV), plus \(\approx0.3\) GeV from propagating the \(M_h\) error through \(n\). That gives \(M_t\approx179.3\)–180.2 ± 1.3 GeV, a pull of **+5.4σ to +6.0σ**. The one-loop estimate in doc 59 (175.5–176.4 GeV) was too optimistic: two-loop running adds about 4 GeV.

## 4. Verdict

1. **The top miss survives and grows.** At two loops with NNLO matching, the zero-parameter spectral PS model predicts \(M_t=190.4\pm1.2\) GeV, 15σ above 172.5. The one-loop number (186 GeV) underestimated the miss. The theory error (0.55 GeV) is small compared with the 18 GeV discrepancy.
2. **The Higgs miss survives:** \(180.5\pm1.8\) GeV with \(\sigma\), 190.5 GeV without. Even taking the top from data, the quartic boundary gives 151 GeV.
3. **Extension (b)** (one fitted parameter) fixes \(m_H\) but leaves \(M_t\approx180\) GeV, about 6σ high. Net predictions minus parameters = 1, and that prediction fails.
4. **What would be needed.** \(y_t(\Lambda)\) must be about 20% below \(g_U\): the data give \(y_t(\Lambda)=0.427\) against \(g_U=0.531\). That needs either a larger \(\operatorname{Tr}Y^\dagger Y\) at \(\Lambda\) from other Yukawas (for example several large Dirac neutrino Yukawas: \(n\gtrsim2.5\) breaks the Higgs, as shown in doc 59), a different boundary scale (not available, since \(\Lambda\) is fixed by unification), or a modified spectral-action normalization of the fermion kinetic terms. Each costs at least one new parameter or principle.
5. **For the roadmap.** Ranked item 2 of doc 59 is done. The top miss is a real failure of the minimal spectral PS boundary conditions at the doc 55 scale, not a numerical artifact.

## 5. Approximations stated

- The PS segment's Yukawa and quartic running is one-loop; the two-loop part is estimated with a proxy, and the segment is short.
- \(\sigma\) sector couplings are one-loop.
- \(y_b\) and \(y_\tau\) run at one loop.
- Matching uses the Buttazzo et al. NNLO fits, near their centre. \(M_W=80.384\) is kept at the fit reference; the effect on \(M_t\) and \(M_h\) is below 0.05 GeV.
- The SM Higgs is identified with the up-type bidoublet component.
