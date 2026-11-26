# 73. Exact gauge unification fixes the SUSY scale: a derived top mass for candidate #10 (exploratory)

**Date:** 26 November 2026 (America/Chicago)
**Originator of the SAM-3 / Dual-Zero framework and of candidate #10's setting:** Shawn Dykes.
**Status:** exploratory. The Dual-Zero regulator is unchanged. This is a conditional result, not a theorem.
**Code:** `experiments/open_routes_72/`. Main scripts are `route1d_unif_corrected.py` (Buttazzo-v4 matching) and `route1c_unif_full.py` / `route1c_fill.py` (SMDR matching), with the machinery in `thr72.py`, `rge3.py`, `sqcd2l.py` and `common.py`. Results are in `results_route1c*.json` and `results_route1d.json`.
**Builds on:** doc 69 (candidate #10), doc 70 (SUSY thresholds, corrected 26 November 2026), and doc 72 (higher orders, open routes).
**Tests:** `tests/test_erratum_2026_11_26.py`, plus the existing suite.

---

## Plain-language summary (for Shawn)

- **What changed.**
  - In doc 70 the SUSY mass scale M_S was *fitted* so that the Higgs came out at 125.1 GeV, and the top was then 170.8 GeV (corrected value, −1.4σ).
  - Here M_S is *not* fitted. The spectral action requires the three gauge couplings to meet at one point Λ (with the trace normalisation). Requiring that meeting to be exact fixes M_S, at about 2.6–2.7 TeV for a degenerate spectrum.
  - No top or Higgs data go into M_S.
- **Result for the top: M_t ≈ 171.9 GeV with no stop mixing, and 172.5–172.8 GeV with large negative stop mixing** (μ > 0).
  - With no stop mixing the pull is −0.5σ (σ = 1.218 GeV, doc 60 budget).
  - Over the α_s band, the two matching schemes and the spectrum variants checked, μ > 0 stays within 171.3–173.5 (|pull| ≤ 1σ).
  - Among the non-excluded candidates in docs 60–72, this is the first to land within 1σ of the top mass with no number fitted to the top or the Higgs, given its assumptions.
- **But it is conditional, and the Higgs is not solved.**
  - It assumes [U] SUSY at the TeV scale in the spectral action and [U] that the extra vector-like pair's Yukawas equal y_t. It also uses a degenerate spectrum and μ > 0 [C].
  - The Higgs comes out at **117 GeV** with no stop mixing (−4.5σ). It reaches **124.0–124.3 GeV** (−0.4 to −0.6σ) only if the stop mixing X_t is chosen near −2 M_S [C]. Moving the gluino or other masses moves M_h by several GeV.
  - So the Higgs is not a prediction here.
- **Honest size of the claim.** This is a conditional derivation of M_t that sits within 1σ. It is not a derivation of both masses, and it does not overturn the doc 69 no-go: SUSY and y = y_t are still inputs that the geometry does not fix.

---

## 1. Setup and labels

- **[D] derived**: follows from the stated inputs with no fit to M_t or M_h.
- **[U] assumed**: a structural assumption not derived from Dual-Zero or the spectral action.
- **[C] chosen**: a continuous or discrete input set by hand (not fitted to M_t; where it affects M_h it is a choice, and a fit if tuned).
- **[F] fitted**: tuned to data.

| ingredient | status | source |
|---|---|---|
| spectral boundary y_t²(3+n+Δa) = (2/3) I₂ g², (3+Δa) y_b² + y_τ² = K; n = 1, dI = 4, Δa_u = 8, so y_t/g = √(5/9) | from docs 69/70 given the content | doc 69, CCM/CCvS spectral action |
| SUSY spectral boundary (SM traces) | **[U]** | doc 69; the noncommutative MSSM is not exactly SUSY (Beenakker–van den Broek–van Suijlekom, arXiv:1409.5982) |
| one Higgs-coupled vector-like PS pair, both chains with Yukawa = y_t | **[U]** ("universal" hypothesis) | doc 69 #10 |
| exact triple unification g₁ = g₂ = g₃ at Λ (with the trace normalisation) | required by the spectral boundary; imposing it exactly is the new step | doc 70 used "12" crossing only |
| **M_S** | **[D]** from exact unification | this doc |
| tan β | [D] from m_b via the H_d condition | doc 70 |
| spectrum shape: degenerate (all soft masses, μ, M_i, m_A = M_S) | [C] | variants below |
| sign μ | [C] (+ preferred) | |
| X_t / M_S | [C] (0 baseline; −2 to −2.45 for the Higgs) | |
| inputs α_s(M_Z) = 0.1180 ± 0.0009, M_Z, G_F, m_b, m_τ | measured | PDG |

**Physics pipeline** (all published inputs):
- Thresholds at M_S: BGSS arXiv:1407.4081 one-loop thresholds (general masses) and the two-loop O(α_t α_s) λ term with the corrected −X̂_t⁵, as in FlexibleSUSY HSSUSY. Also O(α_t²) λ, Δ_b and Δ_τ.
- Two-loop SQCD top matching: Bednyakov et al., via FlexibleSUSY `mssm_twoloop_mt.cpp`.
- Running: three-loop SM RGEs (Buttazzo et al. arXiv:1307.3536 App. A, plus 4-loop QCD) below M_S, and three-loop MSSM RGEs (Jack–Jones–Kord hep-ph/0408128) above it. The extra pair enters at two loops.
- Pole ↔ MS-bar matching at M_t, two variants:
  - (a) Buttazzo et al. v4 fits, with reference M_t = 173.34 after the erratum;
  - (b) SMDR v1.3, Martin–Robertson arXiv:1907.02500, at 2025 reference inputs.

## 2. Results

### 2a. Baseline and stop-mixing dependence (degenerate spectrum, α_s = 0.1180)

Buttazzo-v4 matching (corrected), all higher orders:

| sign μ | X̂_t [C] | M_S [D] (TeV) | **M_t** | M_h | tan β | pulls (M_t, M_h) |
|---|---|---|---|---|---|---|
| + | 0 | 2.72 | **171.92** | 117.13 | 68.7 | −0.48σ, −4.5σ |
| + | −1.0 | 2.62 | 172.47 | 119.80 | 65.4 | −0.02σ, −3.0σ |
| + | −1.5 | 2.59 | 172.65 | 122.16 | 63.5 | +0.12σ, −1.7σ |
| + | −2.0 | 2.56 | 172.77 | 124.02 | 61.5 | +0.22σ, −0.61σ |
| + | −2.2 | 2.56 | 172.80 | 124.32 | 60.6 | +0.25σ, −0.44σ |
| + | −2.449 | 2.55 | 172.83 | 124.09 | 59.5 | +0.27σ, −0.57σ |
| − | 0 | 3.06 | 169.48 | 116.17 | 41.8 | −2.5σ, −5.1σ |
| − | −2.2 | 2.69 | 171.83 | 123.77 | 50.8 | −0.55σ, −0.75σ |
| − | −2.449 | 2.66 | 172.02 | 123.66 | 52.1 | −0.39σ, −0.82σ |

SMDR matching, all higher orders:

| sign μ | X̂_t [C] | M_S [D] (TeV) | **M_t** | M_h | pulls |
|---|---|---|---|---|---|
| + | 0 | 1.68 | **171.94** | 114.42 | −0.46σ, −6.1σ |
| + | −2.0 | 1.72 | 172.77 | 122.35 | +0.22σ, −1.56σ |
| + | −2.449 | 1.72 | 172.82 | 122.45 | +0.26σ, −1.51σ |
| − | −2.449 | 1.65 | 171.93 | 121.70 | −0.47σ, −1.93σ |

There is no unification solution for X̂_t ≥ +2 with μ > 0. With μ < 0, X̂_t = +2 gives 165.6 (excluded).

### 2b. Sensitivities (μ > 0)

| variation | X̂_t = 0: M_S, M_t, M_h | X̂_t = −2.2: M_S, M_t, M_h |
|---|---|---|
| α_s = 0.1171 (Buttazzo v4) | 3.75 TeV, 171.25, 118.4 | 3.54 TeV, 172.13, 125.0 |
| α_s = 0.1189 (Buttazzo v4) | 1.97 TeV, 172.58, 115.7 | 1.85 TeV, 173.47, 123.5 |
| α_s = 0.1171 (SMDR) | 2.19 TeV, 171.28, 115.6 | 2.24 TeV, 172.14, 123.3 |
| α_s = 0.1189 (SMDR) | 1.30 TeV, 172.60, 113.1 | 1.32 TeV, 173.46, 122.0 |
| gluino M₃ = 2 M_S [C] | 7.5 TeV, 171.73, 121.4 | 7.0 TeV, 172.92, 127.4 |
| gluino M₃ = 0.5 M_S [C] | no solution with M_S in 1–12 TeV (gluino would be < 0.5 TeV, excluded) | same |
| m_A = 0.5 / 2 M_S [C] | 3.03 / 2.43 TeV, 171.91 / 171.93, 117.6 / 116.6 | 2.86 / 2.29 TeV, 172.79 / 172.81, 124.7 / 124.0 |

**Reading the sensitivities:**
- **M_t is robust.** For μ > 0 it stays within 171.25–173.47 across ±1σ in α_s, both matching schemes, a heavy gluino, and m_A. That is |pull| ≤ 1σ. The dominant spread is α_s, at about ±0.7 GeV.
- **The derived M_S is not robust.** Unification fixes a combination of the superpartner masses (an effective threshold scale), not one mass:
  - a factor of about 2 from α_s ± 1σ;
  - a factor of 1.6 between matching schemes, driven by 0.1% shifts in g_Y and g₂;
  - a factor of 2.8 if the gluino is twice as heavy.
  
  M_t barely cares, because it falls only about 0.3 GeV per doubling of M_S (doc 70).
- **M_h is not predicted.** It spans 113–127 GeV across these variants. It depends on X_t, the gluino ratio and α_s, all at the several-GeV level, and its own EFT theory uncertainty at tan β ≈ 60 is ±1–1.5 GeV.

## 3. Derived vs assumed vs chosen: the claim, stated precisely

**Conditional statement.** Assume:
1. [U] a TeV-scale SUSY spectral boundary with SM traces;
2. [U] candidate #10's single vector-like PS pair with Yukawas = y_t;
3. [C] a roughly degenerate superpartner spectrum with μ > 0.

Then exact gauge unification at the spectral scale fixes the SUSY threshold scale at about 2–4 TeV. The top pole mass follows with no parameter fitted to M_t or M_h:

> **M_t = 171.9 ± 0.7 (α_s) ± 0.2 (matching) ± ~1 (theory) GeV at X_t = 0. It rises to 172.5–172.8 GeV for X̂_t between −1 and −2.45.**
> Measured: 172.5 GeV. The pull is −0.5σ to +0.3σ.

The theory estimate (±~1 GeV) comes from:
- the degenerate-limit formulas;
- the missing three-loop vector-like terms;
- the β-scheme ambiguity at tan β ≈ 60;
- the missing 3-loop matching at M_S.

It is an estimate, not a computed error.

**What is not derived:**
- M_h. It needs X_t ≈ −2 M_S [C], and even then it comes out at 122.4–124.3 GeV depending on the matching. The gluino ratio can move it further either way.
- Whether SUSY exists, and why the extra Yukawas equal y_t (the doc 69 no-go stands).
- The sign of μ. With μ < 0, M_t drops to 169.5 at X_t = 0.

**What this improves:**
- Doc 70 (corrected) gave 170.8 at the Higgs-fitted M_S ≈ 30 TeV, −1.4σ.
- Unification puts M_S an order of magnitude lower and the top within 0.5σ. The price is that the Higgs is then too light unless X_t is chosen near maximal mixing.
- The two determinations of M_S are inconsistent at X_t = 0: about 2.7 TeV from unification against about 30 TeV from M_h. They agree to within a factor of about 1.5 only near X̂_t ≈ −2 (about 2.6 against about 4 TeV).

## 4. Caveats

- **Vacuum stability.** tan β ≈ 60–69 with |μ| = M_S means μ tan β ≈ 60 M_S. Stau/sbottom charge- and colour-breaking metastability was not checked in detail (doc 70 §5).
- **Gluino and stop limits.** A degenerate spectrum at 2–4 TeV is above current LHC limits for gluinos and stops (about 2.3 and 1.3 TeV for simplified models). Variants with M₃ ≤ 0.5 M_S are excluded.
- **Unification precision.** "Exact" unification uses the two-loop and partial three-loop running with one-loop thresholds at M_S and none at Λ. Unknown heavy thresholds at Λ of order 1% would move M_S by an O(1) factor, but M_t by ≲ 0.3 GeV.
- **The doc 69 no-go is not lifted.** This result sits inside assumption (4) of doc 69's no-go ("With SUSY, the Higgs can be 125, but only by fitting M_S and stop mixing"). Unification removes the M_S fit for the top, not for the Higgs.

## 5. Reproduce

```
cd experiments/open_routes_72
PYTHONPATH=. ../../.venv/bin/python route1d_unif_corrected.py   # Buttazzo-v4 matching (~25 min, 8 cores)
PYTHONPATH=. ../../.venv/bin/python route1c_unif_full.py        # SMDR matching
PYTHONPATH=. ../../.venv/bin/python route1c_fill.py
```

## 6. References

- A. H. Chamseddine, A. Connes, M. Marcolli, Adv. Theor. Math. Phys. 11 (2007) 991; A. H. Chamseddine, A. Connes, W. D. van Suijlekom, JHEP 11 (2013) 132 (spectral Pati–Salam).
- W. Beenakker, T. van den Broek, W. D. van Suijlekom, arXiv:1409.5982 (noncommutative MSSM; as cited in doc 69).
- E. Bagnaschi, G. F. Giudice, P. Slavich, A. Strumia, JHEP 09 (2014) 092, arXiv:1407.4081 (BGSS thresholds).
- P. Athron et al., FlexibleSUSY, Comput. Phys. Commun. 190 (2015) 139; HSSUSY; A. Bednyakov et al. 2-loop SQCD top mass (as implemented in FlexibleSUSY `mssm_twoloop_mt`).
- D. Buttazzo et al., JHEP 12 (2013) 089, arXiv:1307.3536v4.
- S. P. Martin, D. G. Robertson, arXiv:1907.02500 (SMDR; code v1.3 used).
- I. Jack, D. R. T. Jones, A. F. Kord, hep-ph/0408128 (3-loop MSSM RGEs).
- M. Marquard et al., PRL 114 (2015) 142002, arXiv:1502.01030 (4-loop pole–MS-bar).
- Particle Data Group, 2024 Review (α_s, M_t, M_h).

Credit: the SAM-3 / Dual-Zero framework, the spectral Pati–Salam programme in this repository, and the question that led here are Shawn Dykes's. The computations here are exploratory checks of his framework.
