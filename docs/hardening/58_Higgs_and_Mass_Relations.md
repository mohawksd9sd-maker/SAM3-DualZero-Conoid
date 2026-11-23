# 58. Spectral-action Higgs potential and mass relations in Pati–Salam (exploratory)

**Date:** 23 November 2026 (America/Chicago)
**Status:** exploratory. This does not lock a new core theorem.
**Code:** `experiments/two_loop_pati_salam/higgs_masses.py`; numbers in `results_docs56_58.json`.
**Scales:** two-loop composite \(m_R=3.90\times10^{13}\) GeV, \(\Lambda=1.19\times10^{15}\) GeV, \(g_U=0.532\) (doc 55).

---

## Plain-language summary (for Shawn)

- **What the spectral action fixes.** At the top scale it fixes *ratios*: the top-quark coupling, the Higgs self-coupling, and the couplings of a heavy singlet \(\sigma\), all in terms of the one unified force strength. The cutoff moments \(f_2\) and \(f_4\) drop out, and \(f_0\) is traded for that strength. In Pati–Salam the neutrino and top couplings must be equal, so there is **no free knob left**. That makes these real predictions.
- **How they compare.**
  - Top quark: predicted **≈186 GeV**, measured 172.5 GeV, about **8% too heavy**.
  - Higgs, with the \(\sigma\) field: predicted **≈168 GeV**, measured 125.1 GeV, **too heavy**.
  - Higgs using the measured top mass instead: ≈151 GeV, still too heavy.
  - Without \(\sigma\): ≈176 GeV, the old 170-GeV problem.
- **The 125 GeV claim.** The literature reaches 125 GeV by treating the neutrino/top ratio as free. Here that needs ratio² ≈ 2, which Pati–Salam with one bidoublet does not allow. So **125 GeV is not predicted here**, and quoting it would be a fit.
- **What stays fitted.** The electroweak scale (246 GeV) and the breaking scale both come from \(f_2\Lambda^2\) terms that need fine-tuning. Neutrino masses fit with an \(O(1)\) Majorana coupling (about 3.6 × \(m_R\)), which is consistent but not predicted.
- **Honest verdict.** The genuine predictions miss by 8% (top) and 35% (Higgs) in this simplest version. Bigger Higgs content (more bidoublets, or the \((2,2,15)\)) could change this, but each addition adds free numbers.

---

## 1. Boundary relations at \(\Lambda\)

From CC2012 ("Resilience", arXiv:1208.1030, eqs. 9–15), with \(f_0/2\pi^2=1/4g^2\) and \(n=(y_\nu/y_t)^2\) at \(\Lambda\):
\[
y_t=\frac{2g}{\sqrt{3+n}},\quad
\lambda_h=\frac{n^2+3}{(n+3)^2}\,4g^2,\quad
\lambda_{h\sigma}=\frac{2n}{n+3}\,4g^2,\quad
\lambda_\sigma=8g^2 .
\]

| coefficient | depends on |
|---|---|
| \(g\) | \(f_0\) (normalization; equivalently \(g_U\) from doc 55) |
| \(y_t\), \(\lambda_h\), \(\lambda_{h\sigma}\), \(\lambda_\sigma\) | **only** \(g\) and \(n\); independent of \(f_0,f_2,f_4\) once \(g\) is fixed |
| Higgs and \(\sigma\) mass terms, hence \(v\) and \(w\sim m_R\) | \(f_2\Lambda^2\) (not predicted; hierarchy) |
| cosmological term | \(f_4\Lambda^4\) |
| \(G_N\) | \(f_2\Lambda^2\) with the 64π/45 convention lock (docs 23, 45) |

**PS fixes \(n\).** One bidoublet coupling \(yF_L\phi F_R\) gives \(y_\nu=y_t\) at and above \(m_R\), so \(n=1\):
\[
y_t(\Lambda)=g,\quad\lambda_h=g^2,\quad\lambda_{h\sigma}=2g^2,\quad\lambda_\sigma=8g^2 .
\]

## 2. Running

Potential: \(V=\lambda|H|^4+\kappa|H|^2\sigma^2+\tfrac{\lambda_\sigma}{4}\sigma^4\), with \(\lambda=\lambda_h\) and \(\kappa=\lambda_{h\sigma}\).

The pure-scalar one-loop betas were *derived* from the general tensor formula \(\beta_{ijkl}=\sum(\lambda_{ijmn}\lambda_{mnkl}+2\text{ perms})\) on the five real fields (tested):
\[
24\lambda^2+2\kappa^2,\qquad \kappa(12\lambda+6\lambda_\sigma+8\kappa),\qquad 18\lambda_\sigma^2+8\kappa^2 .
\]

**\(\Lambda\to m_R\) (PS).**
- Gauge couplings come from the doc 55 two-loop solution.
- \(y\) runs with \(6y^2-\tfrac94(g_R^2+g_L^2)-\tfrac{45}4g_4^2\).
- \(\lambda\) receives \(16y^2\lambda-8y^4-9\lambda(g_L^2+g_R^2)+\tfrac38[2g_L^4+(g_L^2+g_R^2)^2]\). The gauge \(g^4\) term is approximate, by analogy with the SM.
- The Majorana Yukawa of \(\sigma\) is omitted.

**At \(m_R\).**
- \(\sigma\) is integrated out at tree level: \(\lambda_{SM}=\lambda-\kappa^2/\lambda_\sigma\).
- \(y_t=y\).

**\(m_R\to M_t\) (SM).** One-loop \(\lambda\), \(y_t\); then \(m_H=\sqrt{2\lambda(M_t)}\,v\). There are no threshold corrections at \(M_t\), which gives an uncertainty of a few GeV. \(M_t^{\rm pred}\) is obtained by inverting the Buttazzo \(y_t\)–\(M_t\) slope.

## 3. Results

| scenario | \(y_t(M_t)\) pred / obs | \(M_t\) pred | \(\sqrt{\lambda_{SM}/\lambda}\) at \(m_R\) | \(m_H\) pred |
|---|---|---|---|---|
| **PS, \(n=1\), with \(\sigma\)** (all spectral) | 1.008 / 0.934 | **185.8 GeV** | 0.684 | **168.1 GeV** |
| PS, \(n=1\), no \(\sigma\) | 1.008 / 0.934 | 185.8 GeV | 1 | 175.5 GeV |
| quartic boundary only, measured \(y_t\), with \(\sigma\) | (input) | (input) | | 151.0 GeV |
| quartic boundary only, measured \(y_t\), no \(\sigma\) | (input) | (input) | | 162.7 GeV |

There is a direct Yukawa mismatch at \(\Lambda\): running the *measured* top up gives \(y(\Lambda)=0.451\), while the spectral relation requires \(y(\Lambda)=g_U=0.532\). The ratio is 0.85, a 15% miss in the coupling.

**\(n\) scan (to show what 125 GeV would need; \(n\) is not free in PS):**

| \(n\) | 0 | 0.25 | 0.5 | **1 (PS)** | 2 | 4 |
|---|---|---|---|---|---|---|
| \(M_t\) pred (GeV) | 196 | 193 | 191 | **186** | 177 | 148 |
| \(m_H\) pred (GeV) | 189 | 185 | 180 | **168** | 123 | unstable (\(\lambda<0\)) |

\(m_H\approx125\) needs \(n\approx2\), that is \(y_\nu\approx1.4\,y_t\), which requires PS-breaking Yukawa structure (a second bidoublet or a \((2,2,15)\)). Each addition brings new free couplings. That is the CC2012 route, a one-parameter fit, not a prediction.

## 4. Majorana scale and seesaw

- In CCvS, the Majorana mass comes from \(\langle\Delta_R\rangle\) (the composite \(H=\Delta\Delta\)), so \(M_N=f\,v_R\) with \(v_R\sim m_R\) and \(f\) an \(O(1)\) coupling that is **not fixed** by the spectral action's ratios.
- With \(y(m_R)=0.485\): \(m_D=84\) GeV.
- \(M_N=m_R\) gives \(m_{\nu_3}=0.18\) eV.
- \(\sqrt{\Delta m^2_{\rm atm}}=0.050\) eV needs \(M_N=1.4\times10^{14}\) GeV \(=3.6\,m_R\).
- This is consistent in order of magnitude. It is **fitted** through \(f\), and the threshold band of doc 55 (\(\pm0.6\) in \(\log_{10}m_R\)) alone covers the factor 3.6.

## 5. Verdict

| relation | type | outcome |
|---|---|---|
| \(g_4=g_L=g_R\) at \(\Lambda\) | consistency (zero dof) | passes (doc 55) |
| \(y_t(\Lambda)=g\) (PS, \(n=1\)) | **prediction** | \(M_t=186\) vs 172.5 GeV: **fails by 8%** (one-loop Yukawa running; theory error a few \%) |
| \(\lambda_h,\lambda_{h\sigma},\lambda_\sigma\) at \(\Lambda\) | **prediction** | \(m_H=168\) (151 with measured top) vs 125.1 GeV: **fails** |
| \(m_H=125\) | fit | needs \(n\approx2\), not allowed with one bidoublet |
| \(v\), \(m_R\) | not predicted | \(f_2\Lambda^2\) terms, fine-tuned |
| \(M_N\sim m_R\), \(m_\nu\) | consistent, fitted | \(M_N\approx3.6\,m_R\) |

**Honest bottom line.**
- The minimal spectral PS model makes two parameter-free mass predictions, and both miss.
- The miss is of the same type as the original CCM 170-GeV Higgs. The \(\sigma\) field reduces it, but not to 125 GeV once PS forces \(n=1\).
- Repairing it requires extra Higgs content with extra couplings, so the predictivity goes down.
- This is reported as a null result, not hidden.
