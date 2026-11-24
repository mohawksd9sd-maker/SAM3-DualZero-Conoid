# 68. Matter-content search: can the finite space itself give y_t/g ≈ 0.80? (exploratory)

**Date:** 24 November 2026 (America/Chicago)
**Status:** exploratory. The **Dual-Zero regulator is untouched**: only the finite content \(H_F\), and through it the gauge traces, the Yukawa trace and the running, is changed. \(\varepsilon(n)=\omega_0(-1)^nn^{-n}\) and \(\operatorname{Reg}_2\) are not used.
**Code:**
- `experiments/two_loop_pati_salam/content_engine.py`: the general boundary and unification engine.
- `experiments/two_loop_pati_salam/matter_search.py`: the route-1 scans.
- `experiments/two_loop_pati_salam/report_68.py`: writes `results_doc68.json` and the figure.

**Figure:** `docs/hardening/figures/68_matter_content_search.png`.
**Tests:** `tests/test_beyond_dial.py` (shared with doc 69).
**Brief (Shawn):** "Run as many tests as you need to, to solve the problem." Route 1 was the top priority.

---

## Plain-language summary (for Shawn)

- **The problem in one line.** The spectral rule fixes the top coupling relative to the gauge coupling at the unification scale: y_t/g = 1.00 in our Pati–Salam model. The measured top needs about 0.80 (in absolute terms, 0.53 vs 0.43).
- **What I searched.** Every way of changing the *content* of the finite space that the axioms allow:
  - extra vector-like copies of each building block of the Pati–Salam algebra;
  - building blocks that need an extra ℂ summand;
  - the Standard-Model-algebra version, including Stephan's vector doublets;
  - extra generations;
  - Higgs-coupled extra fermions;
  - SO(10)/SU(5)-like structures.
- **How each was scored.** For each content I recomputed, with no knobs:
  - the trace-derived boundary;
  - where (and whether) the couplings unify, using the content's own two-loop running;
  - the top and Higgs masses.

  In total that is 468 trace-only contents and about 120 explicit ones.
- **Result: no content with zero free parameters gives the measured top.**
  - Extra fermions that do not touch the Higgs can only *raise* y_t/g. The exact rule is y_t/g = √(I_L/6), where I_L is the SU(2)_L trace.
  - The best zero-parameter direction adds SU(2)_R-only fermions. It lowers the unification scale and gets the top down to **187.1 GeV** before the right-handed scale falls below the leptoquark bound. Pushed further, it gives 185.5 GeV, and then there is no solution at all.
- **Higgs-coupled extra fermions can fix the top, but always with a free Yukawa** (that is the doc 63 result, reproduced exactly). The Higgs then lands at **151–161 GeV**.
- **"Universal Yukawa" guesses** (every new Higgs coupling equal to the top's) are zero-parameter hypotheses. They give discrete values that jump over 172.5:
  - 183.3 or 166.0 GeV for one vector-like family;
  - 174.0 GeV for a fourth generation with only up-type Yukawas.

  The fourth generation is experimentally dead, and its Higgs is 155 GeV anyway.
- **SU(5)/SO(10)** are not allowed by the axioms (Lizzi–Mangano–Miele–Sparano 1996). Even formally, the SO(10)-like version gives m_b = m_t.
- **A striking pattern.** Every non-supersymmetric content falls on one line in the (M_t, M_h) plane. Wherever that line crosses M_t = 172.5, the Higgs is ≈ 147–161 GeV, never 125.
  - So "fix the top" and "fix the Higgs" are *not* independent problems in this framework.
  - Fixing the top by content always leaves the Higgs about 25–35 GeV too heavy.
- **Inversion (what would be needed).**
  - The added Higgs-coupled Yukawa trace must be Δa = 2.21 + 2.07 ΔN, where ΔN is the added gauge trace in generation units.
  - The smallest admissible content that can do it is one vector-like Pati–Salam family pair, with its Yukawa set to c = 0.89 y_t (both chains) or 1.26 y_t (one chain).
  - It is axiom-admissible, but nothing in the axioms fixes c (doc 63). It is a fit, and it leaves M_h ≈ 151 GeV.

---

## 1. The generalized spectral boundary

For an almost-commutative geometry, count Weyl fermions in \(H_F\), with the J-images handled uniformly as in CCM. The a₄ term gives:
- the gauge kinetic term of factor a ∝ f₀ I_a, where \(I_a=\sum_{\rm Weyl\in H_F}S_a(R)\) (Dynkin index × dimension under the other factors);
- the Higgs kinetic term ∝ f₀ a y_t², where a = Tr Y†Y / y_t².

Hence:
\[
I_a\,g_a^2(\Lambda)=\text{common},\qquad y_t^2\,a=\tfrac23 I_a g_a^2,\qquad \lambda=\tfrac23 I_a g_a^2\,b/a^2 .
\]

**Checks:**
- Three generations give I_a = 6 for every factor, which is the doc 58–60 boundary.
- The engine reproduces the doc 60 baseline exactly: M_t = 190.36, M_h = 180.50, m_R = 4.22×10¹³ GeV, Λ = 1.24×10¹⁵ GeV.
- **Literature check (test).** The Beenakker–van den Broek–van Suijlekom MSSM content has gauginos in n⊗n° and one higgsino copy (arXiv:1409.5984). It gives I = (6.6, 9, 9), hence g₃² = g₂² = (11/9) g_Y², which is their eq. (25). Their two-copy variant gives g₃² = (10/9)g₂² = (4/3)g_Y², their Remark 2. Both are reproduced.
- **Literature check (trend).** Stephan's vector doublets (arXiv:0706.3112) lower the cutoff. We get Λ = 2.2×10¹¹, 5.4×10⁸ and 1.4×10⁷ GeV for 1, 2 and 3 doublets at 10 TeV; he gets 5.3×10¹¹, 10⁹ and 2.8×10⁷ with 2007 inputs. Same trend, same order of magnitude.

**Unification.** The condition becomes \(\alpha_a^{-1}/I_a\) equal at Λ. Unequal traces move Λ and m_R, and both are re-solved with:
- exact two-loop coefficients for SM/PS plus the extra fields (`group_theory`);
- step thresholds at the stated masses.

**A theorem for Higgs-blind content.** With Δa = 0 the boundary is y_t/g_L = √(I_L/6) ≥ 1. Extra fermions that do not couple to the Higgs can therefore never lower the ratio. They can only move Λ, and the screen shows that a lower Λ is the only thing that lowers M_t.

## 2. Trace-only screen (all reachable ΔI, masses at Λ, 0 parameters)

With the ℂ-extended entries, every integer \(\Delta I=(\Delta I_R,\Delta I_L,\Delta I_4)\ge0\) can be reached. I screened:
- a coarse grid 0–12 in steps of 2;
- a fine grid 0–4 in steps of 1.

That is 468 contents. 125 of them have a unification solution, and 343 have none (the meeting window is narrow).
- **Minimum M_t = 187.08 GeV**, at ΔI = (6, 0, 0) (only SU(2)_R grows). There M_h = 171.3, Λ = 2.6×10¹¹ GeV, m_R = 1.0×10⁶ GeV.
- Every other solution is heavier, up to 212 GeV.

## 3. Admissible single entries, with running

Ordering is (R, L, 4). Masses are at Λ (trace only) or at m_R (running from m_R). Multiplicity k = 1–3, or more for the SU(2)_R entries. None of these has a Higgs Yukawa; masses are Dirac/Majorana terms in D_F.

| Entry (Krajewski) | ΔI per unit | Result |
|---|---|---|
| (1,2,4)+c.c. [H_L⊗M₄°] | (0,4,2) | no unification solution |
| (2,1,4)+c.c. [H_R⊗M₄°] | (4,0,2) | k=1: 195.3 / 188.2 (Λ=6.4×10¹⁷); k≥2 none |
| (2,2,1) [H_L⊗H_R°] | (1,1,0) | none |
| (3,1,1)+(1) [H_R⊗H_R°] | (2,0,0) | k=1,2,3 at Λ: 189.7/178.2, 188.7/175.2, **187.1/171.3**; at m_R: 189.6/177.9, 188.3/174.2, 185.5/168.2 (m_R = 28 TeV ✗); k≥4 none |
| (1,3,1)+(1) [H_L⊗H_L°] | (0,2,0) | none |
| (1,1,15)+(1) [M₄⊗M₄°] | (0,0,4) | none |
| (1,1,4)+c.c. [ℂ⊗M₄°] | (0,0,1) | k=1: 195.1 / 188.4; k≥2 none |
| (1,2,1)×2 [H_L⊗ℂ°] | (0,1,0) | none |
| (2,1,1)×2 [H_R⊗ℂ°] | (1,0,0) | k=1…7: 190.1 → 185.9 GeV, M_h 179.4 → 169.0; m_R falls below 10⁶ GeV at k=7 ✗ |

The **SU(2)_R-only direction** is the best zero-parameter route found (figure, panel b). The multiplicity k is a discrete choice.
- y_t/g stays exactly 1.
- Λ falls from 10¹⁵ to 10¹¹ GeV.
- m_R is dragged down with it.

It stops at M_t = 187.1 GeV with m_R ≥ 10⁶ GeV. That bound comes from the PS leptoquark sitting at m_R here (K_L → μe), so it is a rough lower limit. Even ignoring the bound, it stops at 185.5 GeV with m_R ≈ 30 TeV, and beyond that no solution exists. **It fails by ≥ 12σ on the top.**

**SM-algebra (CCM, ℂ⊕ℍ⊕M₃(ℂ)) with a g₂ = g₃ boundary:**

| Content | M_t (GeV) | M_h (GeV) | Comment |
|---|---|---|---|
| baseline | 189.5 | 176.6 | g₁ off by 20% at Λ = 2.9×10¹⁶ GeV |
| vector doublets ×1/2/3 (10 TeV) | 191.9 / 193.6 / 195.5 | 190 / 200 / 210 | — |
| VL quark doublet | 202–248 | — | — |
| VL quark singlets, octet | — | — | no boundary below 10¹⁹ GeV |
| VL charged lepton (Stephan 2005) | 189.5–190.1 | — | g₁ off by 35–65% |
| wino-like triplet | 192.6–200.6 | — | — |

All are worse than the baseline, and each needs its Dirac mass as an input.

## 4. Higgs-coupled content: always a fit

| Content (masses at Λ) | Params | Fitted share Δa | c = y/y_t | M_t | M_h | Pull M_h |
|---|---|---|---|---|---|---|
| VL 16+16̄ pair, one chain L H R | 1 | 6.35 | 1.26 | 172.5 (fit) | 160.7 | +20σ |
| VL 16+16̄ pair, two chains | 1 | 6.35 | 0.89 | 172.5 (fit) | 151.0 | +15σ |
| same, masses at m_R | 1 | 6.18 | 1.24 / 0.88 | 172.5 (fit) | 160.6 / 150.9 | +20σ / +15σ |
| electroweakino-like (2,2,1)+singlet; (2,2,1)+triplets; VL leptons (1,2,1) | 1 | — | — | no unification solution for any share | — | — |

These reproduce doc 63 to 0.1 GeV.

**Universal-Yukawa hypothesis** (every new Higgs coupling equal to y_t, so 0 continuous parameters):

| Content | Δa | y_t/g | M_t | M_h |
|---|---|---|---|---|
| 1 VL pair, 1 chain | 4 | 0.913 | 183.3 | 171.6 |
| 1 VL pair, 2 chains | 8 | 0.745 | 166.0 (−5.3σ) | 144.3 |
| 2 pairs, 1 chain | 8 | 0.882 | 180.5 | 168.2 |
| 2 pairs, 2 chains | 16 | 0.683 | 158.2 | 134.5 |
| 3 pairs, 1 / 2 chains | 12 / 24 | 0.866 / 0.655 | 179.0 / 154.3 | 166.5 / 129.9 |
| 4th PS generation, y_u4 = y_ν4 = y_t, y_d4 = y_e4 = 0 (formal) | 4 | 0.816 | 174.0 (+1.2σ) | 155.1 |
| 4th PS generation, all y = y_t (formal) | 8 | 0.667 | 156.0 | 129.6 |
| SO(10)-like 10_H, y_t = y_b = y_τ = y_ν, one Higgs (formal) | 4 | 0.707 | 161.3 | 135.0 |

**Notes on the formal rows:**
- **Fourth generation.** A chiral fourth generation gets its mass only from v. LHC Higgs rates and direct searches exclude it (Djouadi–Lenz, PLB 715 (2012) 310; Eberhardt et al., PRL 109 (2012) 241802). The universal-up-type row is the only discrete hit near the top, and it is both excluded and 17σ off on the Higgs.
- **SO(10).** It is inadmissible as a spectral triple: only fundamental representations are allowed, and the SO(10) fundamental is self-conjugate (Lizzi, Mangano, Miele, Sparano, Mod. Phys. Lett. A 11 (1996) 2561). With one light Higgs it also forces m_b = m_t.

## 5. Inversion: the minimal content that would give 0.80

**Requirement.** With masses at Λ and universal traces (table `requirement`):

| ΔN | 0 | 1 | 2 | 3 | 4 | 6 |
|---|---|---|---|---|---|---|
| Δa needed | 2.21 | 4.28 | 6.35 | 8.43 | 10.5 | 14.6 |
| M_h at the fit | 146.6 | 153.7 | 160.7 | 166.5 | 171.1 | 177.7 |

So **Δa = 2.21 + 2.07 ΔN**, confirming doc 63.

**Why ΔN = 0 is out.** It would need gauge-singlet Higgs-coupled fermions, and a Higgs Yukawa needs an SU(2)-charged partner. Non-universal colourless versions (electroweakino-like, VL leptons) break the unification condition.

**The minimal admissible solution** is one VL Pati–Salam family pair (ΔN = 2), with Δa = 6.35 set by one fitted Yukawa:
- it is admissible except that orientability forbids an *exact* VL copy (doc 63), so the pair must differ in D_F;
- M_h = 151–161 GeV.

## 6. Verdict (route 1)

- **No zero-parameter content reaches the measured top while unification works.** The closest is the SU(2)_R-only direction at 187.1 GeV (185.5 GeV if the leptoquark bound is ignored).
- **Every content that does reach 172.5 has a free Yukawa** (or is excluded), and its Higgs is ≥ 144 GeV. All non-SUSY contents lie on one M_t–M_h line that crosses 172.5 near M_h ≈ 147–161 (figure, panel a).
- **The top-first check (route 4) therefore fails for every route-1 candidate.** Supersymmetric contents are in doc 69.

**Approximations:**
- Above m_R, the extra fields enter the gauge running at two loops but the Yukawa/quartic running at one loop.
- Thresholds are steps.
- The SU(2)_R-direction bound on m_R is rough (leptoquark at m_R).
- The universal-Yukawa rows treat the new Higgs-coupled block like the third generation.
