# 55. Two-loop Pati–Salam unification with thresholds (exploratory)

**Date:** 23 November 2026 (America/Chicago)
**Status:** exploratory calculation, not part of the locked SAM-3 core.
**Code:** `experiments/two_loop_pati_salam/` (`group_theory.py`, `rge.py`, `analysis.py`, `phenomenology.py`); numbers in `results_doc55.json`.
**Tests:** `tests/test_two_loop_pati_salam.py`.

---

## Plain-language summary (for Shawn)

- **What was done.** The three measured forces at the Z mass were run up in energy with the full two-loop equations. Above a breaking scale \(m_R\) they become the three Pati–Salam forces \(SU(4)\times SU(2)_L\times SU(2)_R\). The code then looked for the one \(m_R\) and the one top scale \(\Lambda\) where all three Pati–Salam forces are equal. Nothing was hand-adjusted.
- **Result.** A clean solution exists at two loops:
  \(m_R \approx 3.9\times10^{13}\) GeV, \(\Lambda \approx 1.2\times10^{15}\) GeV, and a shared strength \(\alpha_U^{-1}\approx 44.4\).
  At one loop the same inputs give \(m_R\approx 4.2\times10^{13}\) GeV and \(\Lambda\approx 2.4\times10^{15}\) GeV. Two loops moves \(m_R\) by about 8% and lowers \(\Lambda\) by about a factor of 2.
- **The honest catch.** There are three measured numbers and three unknowns (\(m_R\), \(\Lambda\) and the common coupling), so a meeting is close to guaranteed whenever a solution exists. That makes it a **consistency check that passes**, not a prediction of the forces. The real test is whether a solution exists at sensible scales, and it does.
- **Uncertainty.** The input errors matter little: \(\pm 0.008\) in \(\log_{10}m_R\) and \(\pm 0.03\) in \(\log_{10}\Lambda\). The masses of the heavy particles matter a lot. If each heavy mass is allowed to sit anywhere from 10 times below to 10 times above \(m_R\), then \(m_R\) ranges from \(9\times10^{12}\) to \(1.7\times10^{14}\) GeV and \(\Lambda\) from \(6\times10^{14}\) to \(2.5\times10^{15}\) GeV.
- **Proton and rare decays.** The Pati–Salam force carriers do not make protons decay. The model's proton is stable in perturbation theory (doc 57). The \(SU(4)\) leptoquark at \(\sim10^{13}\) GeV is about \(10^7\) times above the \(K_L\to\mu e\) bound, so it passes easily.
- **Neutrinos.** A right-handed neutrino mass near \(m_R\) gives \(m_\nu\sim0.2\) eV through the seesaw. The measured scale is \(\sim0.05\) eV, so the Majorana mass must be about 3.6 times \(m_R\) (\(M_N\approx1.4\times10^{14}\) GeV). That is a natural order of magnitude, not a prediction.

---

## 1. Setup

**Inputs at \(M_Z=91.1876\) GeV** (MS-bar): \(\alpha_s=0.1180(9)\), \(\hat\alpha^{-1}=127.95(1)\), \(\sin^2\hat\theta_W=0.23122(6)\), \(M_t=172.5(3)\) GeV.
\(y_t(M_t)\) comes from the Buttazzo et al. (arXiv:1307.3536) NNLO fit, \(y_t(M_t)=0.9338\).
The repository's earlier value \(\hat\alpha^{-1}=127.930\) is also run, as a cross-check against docs 48 and 54.

**Field content above \(m_R\)** (CCvS2015, arXiv:1507.08161; ordered \((SU(2)_R,SU(2)_L,SU(4))\)):
- Fermions: three generations of \(F_L=(1,2,4)\) and \(F_R=(2,1,\bar4)\) (Weyl).
- Scalars (complex): bidoublet \(\phi=(2,2,1)\) and \(\Delta_R=(2,1,4)\). The "with 15" scenario adds a complex \(\Sigma=(1,1,15)\).

This content reproduces the repository's one-loop \((b_R,b_L,b_4)=-(7/3,3,31/3)\) and \(-(7/3,3,9)\) exactly (tested).

**Beta functions** (Machacek–Vaughn, Weyl fermions, complex scalars), computed in exact `Fraction`s from Dynkin indices and Casimirs:
\[
16\pi^2\frac{dg_a}{dt}=g_a^3\Big[b_a+\frac{1}{16\pi^2}\Big(\sum_b B_{ab}g_b^2-c_a y^2\Big)\Big].
\]
- One loop: \(b_a=-\tfrac{11}{3}C(G_a)+\tfrac23\sum_F S_a(F)+\tfrac13\sum_S S_a(S)\).
- Two loop, diagonal: \(B_{aa}=-\tfrac{34}{3}C(G_a)^2+\sum_F S_a(2C_a+\tfrac{10}{3}C(G_a))+\sum_S S_a(4C_a+\tfrac23 C(G_a))\).
- Two loop, off-diagonal: \(B_{ab}=2\sum_F S_aC_b+4\sum_S S_aC_b\).

| check | computed | literature |
|---|---|---|
| SM \(b\) | \((41/10,-19/6,-7)\) | same |
| SM \(B_{ij}\) | \([[199/50,27/10,44/5],[9/10,35/6,12],[11/10,9/2,-26]]\) | same (MV83; Martin hep-ph/9709356) |
| SM top two-loop \(c_a\) | \((17/10,3/2,2)\) | same |
| SM top one-loop | \(9/2\,y^2-(17/20,9/4,8)\cdot g^2\) | same |
| QCD \(n_f\) | \(B=-102+38n_f/3\) | same |

**Computed PS two-loop matrix** (composite; rows and columns \(R,L,4\)):
\[
B^{PS}=\begin{pmatrix}50/3&3&75/2\\3&8&45/2\\15/2&9/2&-206/3\end{pmatrix},
\qquad c^{PS}=(4,4,4),
\]
with one-loop \(16\pi^2\dot y=y(6y^2-\tfrac94g_R^2-\tfrac94g_L^2-\tfrac{45}4g_4^2)\), for \(y=y_t=y_{\nu}\) (one bidoublet coupling).
With \(\Sigma\) the only change is \(B_{44}=6\).

**Matching at \(m_R\)** (one-loop MS-bar, with thresholds):
\[
\alpha_1^{-1}=\tfrac35\alpha_R^{-1}+\tfrac25\alpha_4^{-1}+\delta_1,\quad
\alpha_2^{-1}=\alpha_L^{-1}+\delta_2,\quad
\alpha_3^{-1}=\alpha_4^{-1}+\delta_3,
\]
\[
\delta_i=-\sum_c\frac{b_{c,i}}{2\pi}\ln\frac{M_c}{m_R}-\frac{T_i(V)}{12\pi}.
\]
The heavy states are:
- leptoquark vector \(X(3,1,\tfrac23)\), \(W_R^\pm\) and \(Z'\), with their eaten Goldstones;
- physical scalars \(\Delta_R\supset(3,1,-\tfrac13)\) and a real \((1,1,0)\);
- the second doublet of \(\phi\);
- in the with-15 scenario, the components of \(\Sigma\).

The decomposition passes an exact sum rule: SM \(b\) + heavy \(b\) = projected PS \(b\) (tested).

**Conditions (no free knob):** at \(\Lambda\), \(g_L=g_R\) (the spectral-action normalization) **and** \(g_4=g_L\). These are two equations for the two unknowns \(m_R,\Lambda\).

**Solution window.** The \(L=R\) meeting above \(m_R\) exists only for \(m_R<m_R^*\), where \(m_R^*\) is the scale at which the matched \(\alpha_R^{-1}\) and \(\alpha_L^{-1}\) already coincide. Two-loop composite: \(m_R^*=4.6\times10^{13}\) GeV. The solver brackets the root inside \((m_R^*/10^4,\,m_R^*)\).

## 2. Results

| run | \(m_R\) (GeV) | \(\Lambda\) (GeV) | \(\alpha_U^{-1}\) | spread at \(\Lambda\) |
|---|---|---|---|---|
| composite, 1-loop, \(\hat\alpha^{-1}=127.930\) (repo) | \(4.205\times10^{13}\) | \(2.399\times10^{15}\) | 45.05 | \(<10^{-12}\) |
| composite, 1-loop, 127.95 | \(4.224\times10^{13}\) | \(2.414\times10^{15}\) | 45.05 | \(<10^{-12}\) |
| **composite, 2-loop + \(y_t\) + MS-bar matching** | \(\mathbf{3.903\times10^{13}}\) | \(\mathbf{1.189\times10^{15}}\) | **44.43** | \(<10^{-12}\) |
| composite, 2-loop, no MS-bar constant | \(3.722\times10^{13}\) | \(1.188\times10^{15}\) | 44.43 | \(<10^{-12}\) |
| with 15, 1-loop | \(4.050\times10^{13}\) | \(5.843\times10^{15}\) | 45.48 | |
| **with 15, 2-loop** | \(\mathbf{3.744\times10^{13}}\) | \(\mathbf{2.704\times10^{15}}\) | **44.82** | |

The one-loop run reproduces docs 48 and 54 (\(4.205\times10^{13}\), \(2.399\times10^{15}\)) to four digits.
Doc 48's *partial* two-loop run (SM \(B_{ij}\) only, no Yukawa, PS one-loop) gave \(3.73\times10^{13}\) and \(1.29\times10^{15}\). The full two-loop result agrees with it to 5% in \(m_R\) and 8% in \(\Lambda\).

The mismatch is zero to machine precision because the system is exactly determined. That is the point of section 4.

**Input uncertainties** (two-loop composite, \(\pm1\sigma\), \(\Delta\log_{10}\)):

| input | \(m_R\) | \(\Lambda\) |
|---|---|---|
| \(\alpha_s\pm0.0009\) | \(\pm0.0068\) | \(\pm0.026\) |
| \(\sin^2\theta_W\pm0.00006\) | \(\mp0.0031\) | \(\pm0.0013\) |
| \(\hat\alpha^{-1}\pm0.010\) | \(\pm0.0010\) | \(\pm0.0013\) |
| \(M_t\pm0.3\) | \(<10^{-6}\) | \(<10^{-4}\) |
| quadrature | **0.0076** | **0.026** |

**Threshold band.** Every heavy multiplet mass is set to \(M_c=m_R\cdot10^{u}\), with \(u\sim U[-1,1]\) drawn independently, over 300 samples. A solution existed in 300 of 300 samples.

| quantity | 5% | median | 95% |
|---|---|---|---|
| \(\log_{10}m_R\) | 12.96 | 13.57 | 14.23 |
| \(\log_{10}\Lambda\) | 14.77 | 15.06 | 15.39 |
| \(\alpha_U^{-1}\) | 44.11 | 44.44 | 44.79 |

The band is dominated by \(X_{LQ}\) and \(W_R\). Each one alone, moved by a factor of 10, shifts \(\log_{10}m_R\) by \(\approx\mp0.5\). The scalars shift it by \(\lesssim0.04\). With 15, the band is \(\log_{10}m_R\in[12.78,14.16]\) and \(\log_{10}\Lambda\in[15.00,15.83]\).

**Why \(\Lambda\) is fragile.** Above \(m_R\), \(\alpha_L^{-1}-\alpha_R^{-1}\) closes at \(\Delta b/2\pi=(2/3)/2\pi\approx0.11\) per e-fold, so a 0.1 shift in the matched gap moves \(\Lambda\) by \(e^{1}\). A two-loop shift of \(\Lambda\) by a factor of 2 therefore costs very little in couplings. It also means \(\Lambda\) is the least robust output.

## 3. Proton decay, rare decays, seesaw (details in doc 57)

- **Gauge-mediated proton decay: absent.** The \(SU(4)\) vector leptoquark couples \(\bar q\gamma^\mu\ell\). Giving it \(B=\tfrac13, L=-1\) makes every gauge vertex conserve \(B\) and \(L\) separately. Pati–Salam has no SU(5)-type \(X,Y\) bosons.
- **Scalars.** \(\Delta_R=(2,1,4)\) has no renormalizable Yukawa coupling to two fermions. The fermion bilinears are \((6+10)\), \((1+15)\) and so on, never a lone 4. The coupling \(F_RF_R\Delta\Delta\) (the source of the Majorana mass) conserves \(B\). Doc 57 proves \(B=(F+X)/4\) is exact whenever there is no \(\varepsilon_{ABCD}\) term, and the spectral action contains none. Result: no \(p\to e^+\pi^0\) at any perturbative order; only \(\Delta B=3\) instantons remain (\(\sim e^{-16\pi^2/g^2}\)).
- **If** a generic \(B\)-violating \(d=6\) operator \(\kappa g_U^2/\Lambda^2\) were present, then \(\tau(p\to e^+\pi^0)\approx1.1\times10^{32}\) yr at two loops. That is below the Super-K bound of \(2.4\times10^{34}\) yr, so it would require \(\kappa<0.07\). Exact \(B\) is therefore essential, not optional.
- **\(K_L\to\mu e\).** The bound is \(M_X>1400\) TeV (Valencia–Willenbrock 1994), or 86 TeV with general mixing (Smirnov 2018). Here \(M_X\sim(0.3\text{–}3)\,m_R\gtrsim10^{10}\) TeV, a margin of about \(10^{6.9}\). **Passes.**
- **\(n\)–\(\bar n\) (\(\Delta B=2\)).** Forbidden by the same exact \(B\). The bound \(\tau_{n\bar n}>4.7\times10^8\) s is trivially satisfied.
- **Seesaw.** \(y(m_R)=0.485\), so \(m_D=y\,v/\sqrt2=84\) GeV. With \(M_N=m_R\), \(m_{\nu_3}=0.18\) eV. Matching \(\sqrt{\Delta m^2_{\rm atm}}=0.050\) eV needs \(M_N=1.4\times10^{14}\) GeV \(\approx3.6\,m_R\). That is consistent, with an \(O(1)\) Majorana coupling that is free.

## 4. Verdict

1. **Does it unify without tuning?** Yes, in the narrow sense. With the stated field content, two-loop running, top Yukawa and MS-bar matching, there is a unique \((m_R,\Lambda)\) with \(g_4=g_L=g_R\) at \(\Lambda\), and no parameter is adjusted. The solution sits at physically sensible scales: \(M_Z\ll m_R<\Lambda<M_{\rm Pl}\), with \(g_U\approx0.53\) perturbative. It survives two loops and the full ×/÷10 threshold band (300/300).
2. **Is it a prediction?** **No.** Three measured couplings fix exactly three unknowns (\(m_R,\Lambda,g_U\)), which leaves zero degrees of freedom. The only falsifiable content was *existence* of a solution inside the window \(m_R<m_R^*\) with \(m_R<\Lambda<M_{\rm Pl}\). It passed. The doc 48 statement "not a prediction of the couplings at \(M_Z\)" stands.
3. **Seesaw.** \(m_R\sim10^{13.6\pm0.6}\) GeV is the right range for type-I seesaw. It needs \(M_N\approx3.6\,m_R\) with a free coupling.
4. **Still inputs.** The field content and choice of \(F\); the heavy spectrum (thresholds, \(\pm0.6\) in \(\log_{10}m_R\)); the Majorana coupling; \(\omega_0\); the \(G_N\) prefactor; flux and moduli. To make this a prediction, the spectral action or the geometry must fix \(m_R\) or \(\Lambda\) independently. Then sin²θ_W (or α_s) would become an output.

## 5. Approximations stated

- \(y_t\) runs at one loop, and only the third-generation Yukawa enters the two-loop gauge terms.
- The SM Higgs is taken as the up-type component of \(\phi\), with \(y_t=y_\nu\) at \(m_R\).
- Threshold matching is one-loop MS-bar.
- The \(M_Z\to M_t\) segment runs gauge-only (\(\sim10^{-5}\) effect).
- Exact `Fraction` coefficients are converted to float64 once. `dual_zero_record` (doc 53) stores the exact residual of that conversion, so no coefficient information is lost.
