# 63. Is there a principle that forces heavy Higgs-coupled (vector-like) fermions? (exploratory)

**Date:** 23 November 2026 (America/Chicago)
**Status:** exploratory. The **Dual-Zero regulator is untouched**: nothing here uses or changes \(\varepsilon(n)=\omega_0(-1)^nn^{-n}\) or \(\operatorname{Reg}_2\).
**Code:** `experiments/two_loop_pati_salam/vl_principles.py` and `report_63.py`; numbers in `results_doc63.json`. The pipeline extensions are in `top_yukawa_search.py`: `trace_scale`, `extra_db`, `extra_running`, `sigma_trace_scale`.
**Tests:** `tests/test_vl_principles.py`.
**Context:** the original doc 61 brief asked for a rule that *forces* the extra Higgs-coupled fermions and fixes their number and Yukawa share. Shawn also asked why the ω₀³ near-miss was not counted.

---

## Plain-language summary (for Shawn)

- **Verdict: nothing in the framework forces the extra heavy fermions.** I tested seven candidate rules:
  - anomaly cancellation;
  - the KO-dimension / Poincaré-duality / orientability axioms of the finite space;
  - the first-order condition;
  - fermion-doubling removal;
  - the index theorem on the magnetized surface;
  - the Clifford "quanta of geometry" constraint;
  - the Poincaré homology sphere as internal shape.
- **What they do instead.** None of them fixes the number or the Yukawa share. Two actively push the other way:
  - **Orientability** forbids an exact vector-like copy: the chirality operator cannot be built from the algebra once a copy with flipped chirality is present.
  - **The Poincaré sphere** forces vector-like modes in fixed counts (2 at the lowest level). But they are full copies of the matter, and full copies provably leave the top unchanged (190.4 GeV). It also kills the chiral Standard Model.
- **An honest correction to doc 61.** In the spectral action, extra fermions charged under the gauge group also add to the gauge-coupling normalization, not just to the Yukawa sum. Counting that properly:
  - doc 61's "share 2.1 → top 172.5, Higgs 146" row actually gives **top 192.6 GeV** (worse than no extra fermions);
  - the real requirement is a Yukawa share of **2.20 + 2.07 per added generation-equivalent of gauge charge**;
  - for one vector-like Pati–Salam family pair that is a share of about **6.2–6.4**;
  - fitted that way, the Higgs comes out at **149–161 GeV**, depending on how the pair couples to the Higgs and how many pairs there are.
  - Since no rule fixes those choices, this is a family of fits, not a sharp prediction. Every member fails the Higgs (125.1) by at least 13σ.
- **The ω₀³ near-miss.** Multiplying the top coupling at the unification scale by ω₀³ = 0.7966 (instead of the needed 0.8026) gives **M_t = 171.8 GeV** (0.5σ low; 171.7–172.0 for ω₀ = 0.927 ± 0.0005). The Higgs comes out at **150.5 GeV** if only the Yukawa is rescaled, or **138.8 GeV** if the factor rescales the whole Higgs normalization.
  - **Why it is not counted:**
    - ω₀ is itself an input, not derived (doc 42);
    - the power 3 was picked after looking;
    - with 16 numbers tried, the chance that at least one lands in the window by luck is about 84%;
    - nothing in the theory says "multiply the top coupling by ω₀³".
  - **It also does not "work":** it fixes the top but still misses the Higgs by 25–14 GeV.

---

## 1. The requirement, done properly

**Normalization.** In the spectral action both kinetic terms come from traces over the same Hilbert space \(H_F\):
- the gauge term from \(\operatorname{Tr}_{H_F}T_a^2\);
- the Higgs term from \(a=\operatorname{Tr}Y^\dagger Y\).

With \(N_{\rm eff}\) counting the gauge trace in units of one chiral generation (the CCM normalization has \(N_{\rm eff}=3\)):
\[
y_t^2=\frac{4g^2\,(N_{\rm eff}/3)}{a},\qquad
\lambda=\frac{4g^2(N_{\rm eff}/3)\,b}{a^2},\qquad
\lambda_{h\sigma}=\frac{4g^2(N_{\rm eff}/3)\,2n}{a}.
\]
\(\lambda_\sigma\) carries the same factor unless the σ/ν_R sector is copied too.

**Doc 61 assumption.** Doc 61 kept \(N_{\rm eff}=3\). That is only right for gauge-singlet extra fermions, and those cannot couple to the \((2,2,1)\) Higgs bidoublet.

**Requirement.** The data at the doc 60 boundary give \(y_t^2/4g^2=0.1612\). Writing \(\Delta N\) for the added gauge trace and \(\Delta a\) for the added Yukawa trace (in \(y_t^2\) units), the requirement becomes
\[
\Delta a = 2.20 + 2.07\,\Delta N .
\]

**Consequences.**
- **Full copies.** A Dirac copy of the whole three-generation \(H_F\) has \(\Delta N=6\) and \(\Delta a=8\), the same ratio 4/3 as the SM. It leaves \(y_t\) exactly unchanged (computed: \(M_t=190.36\), \(M_h=180.51\)). This is the general form of the doc 61 tower identity.
- **Doc 61 best row recomputed.** A VL PS 16-pair with \(\Delta a=2.1\) and \(\Delta N=2\) gives **\(M_t=192.6\)** (193.9 with its running from \(m_R\)) and \(M_h=185\)–188. It fails.

**Vector-like PS 16+16̄ pairs, fitted to \(M_t=172.5\)** (one Higgs chain \(L H R\), or two chains \(L H R\) plus mirror \(L' H R'\); the grading forbids \(L' H R\), which the explicit triple confirms):

| pairs \(k\) | chains | masses at | \(c=y_X/y_t\) | \(\Delta a\) | \(M_h\) (GeV) | pull |
|---|---|---|---|---|---|---|
| 1 | 1 | Λ / \(m_R\) | 1.26 / 1.24 | 6.35 / 6.17 | 160.7 / 160.6 | +20σ |
| 1 | 2 | Λ / \(m_R\) | 0.89 / 0.88 | 6.35 / 6.16 | 151.0 / 150.8 | +15σ |
| 2 | 1 | Λ / \(m_R\) | 1.15 / 1.13 | 10.5 / 10.2 | 159.5 / 159.5 | +19σ |
| 2 | 2 | Λ / \(m_R\) | 0.81 / 0.80 | 10.5 / 10.2 | 149.4 / 149.3 | +14σ |
| 3 | 2 | Λ / \(m_R\) | 0.78 / 0.77 | 14.6 / 14.3 | 148.8 / 148.7 | +13σ |

**Reading.**
- Each row has one fitted parameter (\(c\)) and a discrete choice \((k,\text{chains})\).
- \(M_h\) is 149–161 GeV, never 125.
- A principle that fixed \((k,\text{chains},c)\) would turn one row into a sharp prediction. Every row fails.

## 2. The candidate principles

| # | principle | computed / checked | forces VL? | fixes \(N\) and share? |
|---|---|---|---|---|
| 1 | anomaly cancellation | \(SU(4)^3\) anomaly of flux-generated \(M_L(4,2,1)+M_R(\bar4,1,2)\) is \(2M_L-2M_R\); Witten \(SU(2)\) anomalies vanish | no: forces only \(M_L=M_R\); VL pairs are anomaly-free automatically | no |
| 2a | KO-dimension 6 signs | explicit triple: \(J^2=1\), \(JD=DJ\), \(J\gamma=-\gamma J\), \(D\gamma=-\gamma D\) hold with and without a VL pair | no (sign conditions only); the grading forbids the \(L' H R\) Yukawa | no |
| 2b | Poincaré duality | intersection form on \(K_0\) (rank 3) is antisymmetric (KO 6): PS gives \(\begin{psmallmatrix}0&0&-2\\0&0&2\\2&-2&0\end{psmallmatrix}\), det 0; adding a VL pair makes it identically 0 | no; PD **cannot** hold for any \(H_F\) over this algebra (odd-rank antisymmetric form) | no |
| 2c | orientability (\(\gamma=\sum a\,JbJ^{-1}\)) | PS one generation: residual \(4\times10^{-16}\) (orientable); with a VL pair: residual 1.0 | **forbids** exact VL copies | no |
| 3 | first-order condition | Yukawa and VL Dirac masses satisfy it exactly; the Majorana \(\nu_R\) term violates it (2.0), as in CCvS 2013 | no (it constrains \(D\), never the content of \(H_F\)); its violation gives the composite Higgs/σ, not fermions | no |
| 4 | doubling / quadrupling removal | the projection acts identically on gauge and Yukawa traces | no (it removes states) | no (ratio unchanged) |
| 5 | index theorem on the magnetized surface | index = \(M\), with no opposite-chirality zero modes (docs 61–62); massive Landau levels are full copies, so \(y_t/g\) is invariant (§1) | no finite VL count; towers do not change the top | no |
| 6 | quanta of geometry (CCM 2014) | the irreducible \(M_2(\mathbb H)\oplus M_4(\mathbb C)\) bimodule is \(4\times4=16\) (32 with \(J\)-images) = one PS generation, with no VL partner; the multiplicity (generations) is free | no | no |
| 7 | Poincaré homology sphere \(S^3/2I\) | invariants of the 120 icosians agree with the Molien series \((1+t^{30})/((1-t^{12})(1-t^{20}))\); Dirac spectrum (Bär): **no zero modes**, lowest level \(\tfrac32\) with multiplicity 2, next 12.5 (×12), 13.5 (×14) | **yes, all modes are VL** (odd-dimensional, no chirality), with fixed counts | the count yes, but each mode is a full copy of \(H_F\): share ratio 4/3, so \(M_t=190.36\), \(M_h=180.5\) (at Λ); also no chiral SM |

**Notes on the entries.**
- **Poincaré duality.** The failure for (2b) is algebraic: in KO-dimension 6 the form \(\cap(p,q)=\operatorname{Tr}(\gamma pJqJ^{-1})\) is antisymmetric, and \(K_0(\mathbb H_R\oplus\mathbb H_L\oplus M_4(\mathbb C))\) has rank 3. Changing the fermion content cannot help; only changing the algebra could.
- **Orientability.** The result for (2c) is the opposite of what was wanted. An exact vector-like partner sits in the same algebra representation with the opposite grading, so no element \(\sum a\,JbJ^{-1}\) can tell the two apart.
- **Poincaré sphere.** It is the only shape that forces a fixed count. But it forces full copies, and §1 shows full copies cannot move \(y_t\).
- **Magnetized surface with the finite space.** The surface changes the total KO bookkeeping. That constrains the signs of \(J\) and \(\gamma\) on \(F\), not the multiplicities, so it does not force VL states either. This is sign bookkeeping only, with no separate computation.

## 3. Verdict on the principle search

**Null.** No rule in this list forces Higgs-coupled vector-like fermions with a fixed number and share. One rule (orientability) forbids exact vector-like copies. The only shape that forces vector-like modes (the Poincaré sphere) forces full copies, which leave the top at 190.4 GeV and destroy chirality.

The extra-fermion repair therefore stays a **fit**:
- one continuous parameter plus discrete choices;
- with the gauge trace counted correctly, \(\Delta a\approx6.2\)–14.6;
- Higgs 149–161 GeV, failing by at least 13σ.

The "sharp ~146 GeV" prediction of doc 61 does not survive the correction. The nearest sharp version, a single VL pair with both chains, gives about 151 GeV.

## 4. The ω₀³ near-miss

**Needed factor:** \(r=y_t(\Lambda)/y_t^{\rm spec}=0.8026\), with ±1σ band \([0.7914,0.8141]\).

| factor | \(r\) | \(M_t\) (GeV) | pull | \(M_h\), Yukawa only | \(M_h\), Higgs normalization (\(\lambda\propto r^4\)) |
|---|---|---|---|---|---|
| \(\omega_0^3\), \(\omega_0=0.927\) | 0.79660 | **171.85** | −0.53σ | **150.5** | **138.8** |
| \(\omega_0=0.9265\) | 0.79531 | 171.71 | −0.65σ | 150.3 | 138.5 |
| \(\omega_0=0.9275\) | 0.79789 | 171.99 | −0.42σ | 150.7 | 139.1 |
| exact requirement | 0.80263 | 172.50 | 0 | 151.4 | 140.2 |

**Why it is not counted as a result, even though the top lands within 1σ:**
1. **Hand input.** \(\omega_0\approx0.927\) is not derived. Natural geometric radii do not give it; it needs \(R\approx0.409\,\ell_0\) (docs 42, 46). A factor built from an undetermined input is a fit in disguise.
2. **Post-hoc exponent.** The power 3 was chosen after seeing the target. \(\omega_0^{1/2},\omega_0,\omega_0^2,\omega_0^{13/4}\) were also tried and miss.
3. **Look-elsewhere.** 16 candidate numbers spanning \([0.76,0.96]\) were tried against a 0.023-wide window. That gives 1.75 expected chance hits, and **P(at least one hit) = 84%**. Two hits (\(\omega_0^3\) and \(4/5\)) is what chance predicts.
4. **No mechanism.** Nothing in the spectral action multiplies \(y_t\) (and only \(y_t\)) by a power of the Dual-Zero weight. Using \(\omega_0\) that way would be a new rule added to fit, not a consequence of the regulator. Dual-Zero stays as defined.
5. **It does not fix the Higgs.** \(M_h=139\)–151 GeV against 125.1.

**Status:** recorded as a numerical coincidence; not adopted.

## 5. Approximations

- The finite triple is one generation with a colour-universal bidoublet Yukawa. Orientability is tested as a real least-squares problem over the 40-dimensional real algebra.
- The K-theory generators are \(1_{\mathbb H_R}\), \(1_{\mathbb H_L}\), \(e_{11}\in M_4(\mathbb C)\).
- \(N_{\rm eff}\) scaling is applied uniformly to \(y_t^2\), \(\lambda\), \(\lambda_{h\sigma}\) (and \(\lambda_\sigma\), except for full copies).
- The running of VL states from \(m_R\) uses a universal one-loop \(\Delta b=8/3\) per pair.
- The Poincaré-sphere Dirac multiplicities use Bär's formula for the left quotient with the trivial flat bundle.
