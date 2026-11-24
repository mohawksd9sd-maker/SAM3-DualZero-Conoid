# 69. Multistage breaking, SUSY spectral models, top-first Higgs, and combinations; global verdict on the y_t/g problem (exploratory)

**Date:** 24 November 2026 (America/Chicago)
**Status:** exploratory. The **Dual-Zero regulator is untouched**. The corrected doc 63 accounting and the doc 60 two-loop pipeline are used throughout. Pulls use σ(M_t) = 1.218 GeV and σ(M_h) = 1.763 GeV (doc 60).
**Code** (`experiments/two_loop_pati_salam/`):
- `multistage.py`: PS → LR → SM with four-group running.
- `susy_spectral.py`: SUSY spectral boundary, MSSM two-loop gauges/y_t, and the M_S matching.
- `report_69.py`: writes `results_doc69.json` and the figure.
- Route-1 machinery is in `content_engine.py` and `matter_search.py` (doc 68).

**Figure:** `docs/hardening/figures/69_multistage_susy_topfirst.png`.
**Tests:** `tests/test_beyond_dial.py` (9 tests, shared with doc 68).
**Brief (Shawn):** "Run as many tests as you need to, to solve the problem." The four routes were matter content (doc 68), multistage, SUSY spectral, and top-first Higgs, plus combinations. The stop rule was: either a derived solution, or a crisp no-go with the minimal extra assumption.

---

## Plain-language summary (for Shawn)

- **Verdict: the search is exhausted, and the answer is a no-go.** Nothing *derived* (zero free parameters, admissible finite space) gives y_t/g ≈ 0.80 at the spectral scale. So nothing derived gives M_t = 172.5 GeV.
- **Multistage breaking (PS → LR → SM)** does not help. The top stays at **191.2–191.4 GeV** wherever the intermediate scale is put. The Higgs barely moves (181.7 → 180.5). The extra scale is a free input, because no spectral quartic turns negative to generate it.
- **SUSY spectral models.** The spectral rule must be applied to H_u and H_d separately. That forces tan β ≈ 55–66 (set by m_b).
  - With only Standard-Model traces, the top comes out at **179–185 GeV** (for M_S = 1 TeV up to Λ). That is better than 190, but still 5–11σ off.
  - The Broek–van Suijlekom trace variants (gauginos and higgsinos in H_F) make it *worse* (188–195), and they also break unification by 17–57%.
  - A real bonus: the SUSY Higgs naturally lands near **118–136 GeV** for M_S of a few TeV.
- **Top-first check.** If the top is forced to be right, what does the Higgs do?
  - Without SUSY, the Higgs is always 147–161 GeV. Every non-SUSY content sits on one (M_t, M_h) line (doc 68).
  - With SUSY, the Higgs is set by M_S and stop mixing, so it is *fitted*, not predicted.
- **The closest thing to a solution is a combination:** SUSY plus one Higgs-coupled vector-like Pati–Salam family pair.
  - **With the "universal" guess** (the new Yukawas equal to the top's), y_t/g = √(5/9) = 0.745. The top is then **168.4 GeV** (flat in M_S), and the Higgs is 125 GeV at M_S ≈ 30–50 TeV with no stop mixing.
    - That is 4 GeV (3.4σ) low. It undershoots, so universal y = y_t is not the answer either.
    - SUSY threshold corrections to y_t are not in this calculation and are comparable in size, so this needs a proper threshold calculation before anyone reads anything into it.
  - **With the new Yukawa share fitted** (about 77% of universal, i.e. c ≈ 0.88 y_t), M_t = 172.5 and M_h = 124 GeV at M_S = 10 TeV, with unification within about 1%.
    - **That is 2 fitted numbers for 2 observables: a fit, not a prediction.**
- **Minimal extra assumption** needed to match both masses: low-scale SUSY in the spectral action (M_S ~ 10 TeV), plus **one Higgs-coupled vector-like Pati–Salam family pair whose Yukawa (c ≈ 0.88 y_t) is put in by hand**.
  - Caveat: the noncommutative MSSM action is itself not exactly supersymmetric (BvdBvS arXiv:1409.5982).
  - For the top alone, without SUSY, the minimum is the doc 63 fit (one VL pair, c = 0.89). It leaves M_h ≈ 151 GeV.

---

## 1. Route 2: multistage PS → SU(2)_L×SU(2)_R×U(1)_{B−L}×SU(3) → SM

**Setup.**
- Breaking scales: M_C is where SU(4) → SU(3)×U(1)_{B−L}, and m_R is where SU(2)_R × U(1)_{B−L} → U(1)_Y.
- r = log₁₀(M_C/m_R) is the input.
- Normalization: B−L enters as q = √(3/8)(B−L), with g_BL = g₄ at M_C.
- One-loop LR coefficients: b = (4.25, −2.83, −3, −7) for (BL, L, R, 3), with two-loop LR coefficients built by `_lr_coeffs`.
- The spectral boundary at Λ is unchanged: g₂L = g₂R = g₄, and y_t/g = 1.

**Results:**

| r = log₁₀(M_C/m_R) | m_R (GeV) | M_C (GeV) | Λ (GeV) | M_t | M_h |
|---|---|---|---|---|---|
| 0.001 | 3.85e13 | 3.86e13 | 2.83e15 | 191.21 | 181.74 |
| 1 | 1.20e13 | 1.20e14 | 3.95e15 | 191.19 | 181.27 |
| 2 | 3.71e12 | 3.71e14 | 5.50e15 | 191.20 | 180.94 |
| 3 | 1.15e12 | 1.15e15 | 7.68e15 | 191.24 | 180.70 |
| 4 | 3.58e11 | 3.58e15 | 1.07e16 | 191.31 | 180.56 |
| 5 | 1.11e11 | 1.11e16 | 1.50e16 | 191.40 | 180.49 |
| 6 | — | — | — | no unification | |

- The r → 0 limit reproduces the doc 67 "with σ + 15" row (191.17 / 181.69).
- **Why it is flat.** Running only redistributes g between scales. y_t/g = 1 is pinned at Λ, and the IR top is controlled by the QCD-dominated y_t flow. A different intermediate scale moves Λ, but the y_t fixed-point-like running absorbs it.

**Radiative check (could the intermediate scale be generated?).** I ran every spectral quartic from Λ down to m_R. None turns negative:
- min λ = 0.250;
- min λ_hσ = 0.397;
- min λ_σ = 1.186.

So there is no Coleman–Weinberg-type generation, and M_C and m_R stay inputs (1 parameter).

## 2. Route 3: SUSY spectral models

**Boundary.** Each Higgs doublet's kinetic term is normalized by its own Yukawa trace:
\[
y_t^2(3+n)=K,\qquad 3y_b^2+y_\tau^2=K,\qquad K=\tfrac23 I_a g_a^2 .
\]
- n = 1 means a Dirac ν Yukawa equal to y_t; n = 0 means none.
- With the CCM traces, I = (6, 6, 6) (trace S0). That gives y_t/g = 1.155 for n = 0 and 1.0 for n = 1.
- The H_d condition plus measured m_b, m_τ then **fixes tan β**: it comes out at 57–64 (42 for Δ_b = −0.3, 68 for Δ_b = +0.3).

**Running and matching.**
- Above M_S: MSSM two-loop gauge running with the standard B and c_t, c_b, c_τ (Martin–Vaughn, PRD 50 (1994) 2282), y_t at two loops (Barger–Berger–Ohmann, PRD 47 (1993) 1093), and y_b, y_τ at one loop.
- At M_S, tree-level matching: λ(M_S) = (g² + g′²)/8 · cos²2β + 3y_t⁴/(16π²) · X̂²(1 − X̂²/12).
- Below M_S: the doc 60 SM two-loop pipeline.
- Cross-check: M_S = 10 TeV, X̂ = 0 gives ≈ 124 GeV, consistent with SusyHD-type EFT results (Vega–Villadoro 2015) within the ±2 GeV EFT uncertainty.

### Scan over M_S (trace S0)

| M_S (GeV) | n = 0: M_t | M_h (X̂ = 0 … √6) | n = 1: M_t | M_h (X̂ = 0 … √6) | unif. mismatch (n = 1) |
|---|---|---|---|---|---|
| 1e3 | 184.1 | 117.9 … 135.3 | 179.2 | 115.5 … 130.9 | 0.3% |
| 3e3 | 186.0 | 128.3 … 142.3 | 180.6 | 124.3 … 136.6 | 0.7% |
| 1e4 | 187.7 | 137.8 … 149.1 | 181.8 | 132.1 … 141.9 | 1.7% |
| 1e5 | 190.2 | 152.0 … 159.7 | 183.5 | 143.1 … 149.7 | 3.4% |
| 1e6 | 192.0 | 162.3 … 167.7 | 184.5 | 150.6 … 155.1 | 4.8% |
| 1e8 | 194.2 | 175.5 … 178.5 | 185.4 | 159.0 … 161.4 | 7.3% |
| 1e12 | 195.9 | 186.9 … 188.0 | 185.1 | 163.9 … 164.8 | 11% |
| 1e14 | no boundary | | no boundary | | |

- The best case (n = 1, M_S = 1 TeV) gives M_t = 179.2 GeV, which is +5.5σ.
- **Sensitivities:** Δ_b = −0.3 gives M_t −1.3 GeV; α_s ± 0.001 gives ±0.5 GeV. Using α₂ = α₃ (which = "23") instead of α₁ = α₂ changes M_t by < 0.2 GeV.

### Broek–van Suijlekom traces

Sources: Beenakker–van den Broek–van Suijlekom, arXiv:1409.5984, eq. 25 and Remark 2.
- S1 (gauginos + 1 higgsino copy): I = (6.6, 9, 9), y_t/g = 1.414.
- S2 (2 higgsino copies): y_t/g = 1.491.

| trace | M_S | M_t | unif. mismatch |
|---|---|---|---|
| S1 | 1e3 / 1e4 | 188.4 / 192–193 | 17–36% |
| S2 | 1e3 / 1e4 | 190.3 / 192.6–195.3 | 31–57% |

Both raise y_t/g. Both fail unification, because the g₁ trace no longer matches the MSSM b₁ running.

### Top-first inversion

Fix M_t = 172.5, run up, and read y_t/g at the S0 boundary. The ratio needed is **0.72–0.80** for every tan β ∈ {5, 10, 30, 50} and M_S ∈ {1, 10, 1000} TeV. For example, 0.79 at tan β = 50 and M_S = 1 TeV.

- SUSY lowers the requirement only from 0.80 to ≈ 0.72–0.80.
- The gap to 1.0 (n = 1) or 1.155 (n = 0) remains.
- The spectral tan β (≈ 57) sits at the 0.78–0.80 end.

## 3. Route 4: top-first Higgs check

| framework | M_h when M_t is forced to 172.5 | status |
|---|---|---|
| non-SUSY PS, any admissible content (doc 68 line) | 147–161 GeV | 12–20σ off; not 125 |
| non-SUSY, doc 63 fitted VL pair (1 or 2 chains) | 160.7 / 151.0 | excluded |
| multistage PS → LR → SM | no content reaches 172.5 | — |
| SUSY (any trace) + Higgs-coupled VL share | 112.6 … 135.7 (set by M_S, X̂) | 125 reachable, but **fitted** |

The non-SUSY Higgs is tied to the top by the boundary λ = (2/3) I g² b/a², and that tie excludes it. In SUSY the tie is cut at M_S: λ is replaced by the D-term plus stop threshold, so M_h becomes a function of the free soft scale.

## 4. Combinations

**SUSY + one Higgs-coupled vector-like PS family pair.**
- Settings: ΔI = 4, both chains coupled, n = 1.
- Each Higgs's Yukawa trace gains the same share Δa (`solve(..., dI=4, da_u=Δa)`, with da_d = da_u).

| Δa (H_u share) | y_t/g | M_t (M_S = 3 TeV) | M_h (X̂ = 0 … √6) |
|---|---|---|---|
| 0 | 1.29 | 187.9 | 129.8 … 144.5 |
| 4 | 0.913 | 177.1 | 121.9 … 133.2 |
| 8 (universal y = y_t, 2 chains) | 0.745 = √(5/9) | 168.4 | 116.5 … 125.5 |
| 12 | 0.645 | 161.2 | 112.5 … 119.9 |

**Universal hypothesis (Δa = 8; zero Yukawa parameters; M_S free):**

| M_S | 1e3 | 3e3 | 1e4 | 3e4 | 1e5 | 1e6 | 1e7 | 1e8 |
|---|---|---|---|---|---|---|---|---|
| M_t | 168.1 | 168.4 | 168.5 | 168.4 | 168.1 | 167.4 | 166.4 | 165.4 |
| M_h (X̂ = 0) | 110.8 | 116.5 | 121.0 | 124.0 | 126.4 | 129.0 | 129.9 | 129.9 |
| unif. | 0.9% | 0.0% | 1.0% | 1.8% | 2.7% | 4.1% | 5.4% | 6.6% |

- M_t is a near-prediction under this hypothesis: 168.4 ± 0.1 GeV across 1–100 TeV.
- That is **−4.1 GeV (−3.4σ)**, still excluded at the doc 60 error level.
- Not included: the one-loop SUSY threshold to y_t at M_S. The gluino/stop correction is typically a few percent of y_t, sign dependent, which is several GeV in M_t. So the 3.4σ is not robust in either direction.
- M_h = 125 at M_S ≈ 40 TeV with X̂ = 0. M_S is fitted to the Higgs, so the Higgs is not a prediction.

**Fitted share (2 parameters: Δa and M_S, with X̂ = 0):**

| M_S | Δa fitted | c = √(Δa/8) | y_t/g | M_t | M_h (X̂ = 0 … √6) | tan β | unif. |
|---|---|---|---|---|---|---|---|
| 1 TeV | 5.69 | 0.84 | 0.829 | 172.5 | 112.6 … 125.6 | 55.9 | 0.7% |
| 10 TeV | 6.19 | 0.88 | 0.809 | 172.5 | 124.1 … 131.8 | 56.6 | 1.2% |
| 100 TeV | 6.27 | 0.89 | 0.806 | 172.5 | 130.7 … 135.7 | 57.4 | 2.9% |

Both masses match, with good unification and Λ ≈ 8×10¹⁵ GeV < M_Pl. But **2 continuous inputs fix 2 observables**, plus discrete choices (SUSY, which VL content, X̂ = 0). This is a **fit**, not a derivation.

Other combinations, all in doc 68 or above, change nothing:
- multistage + R-sector content: the top stays ≥ 187 GeV, since both are Higgs-blind;
- SUSY + S1/S2 traces + VL: unification fails;
- multistage + VL fit: same as doc 63, with the Higgs at 151–161 GeV.

## 5. Global ranked table (docs 60, 63, 67, 68, 69)

Ranked by derivedness first, then by distance to (172.5, 125.1). "Params" counts continuous inputs fitted to data. Discrete choices are listed separately.

| # | candidate | derived? | params | y_t/g at Λ | M_t | M_h | unif. ok? |
|---|---|---|---|---|---|---|---|
| 1 | PS + R-sector Higgs-blind content (3,1,1)+(2,1,1)×2, m_R ≥ 1e6 GeV (doc 68) | yes (discrete content) | 0 | 1.00 | 187.1 | 171.3 | yes (Λ 2.6e11) |
| 2 | SUSY spectral S0, n = 1, M_S = 1–3 TeV | partly (SUSY assumed) | 1 (M_S) + X̂ | 1.00 | 179.2–180.6 | 115.5–136.6 | yes (<1%) |
| 3 | SUSY spectral S0, n = 0 | partly | 1 + X̂ | 1.155 | 184.1–195.9 | 118–188 | ≤ 1e4 GeV only |
| 4 | Multistage PS → LR → SM | yes | 1 (r) | 1.00 | 191.2–191.4 | 180.5–181.7 | yes, r ≤ 5 |
| 5 | Baseline spectral PS (doc 60) | yes | 0 | 1.00 | 190.4 | 180.5 | yes |
| 6 | SM algebra (CCM) and Stephan vector doublets | yes | 0 | ≥ 1.00 | 189.5–195.5 | 176.6–210 | n/a (no PS unification) |
| 7 | SUSY S1/S2 (BvdBvS traces) | partly | 1 | 1.41–1.49 | 188–195 | 120–160 | **no** (17–57%) |
| 8 | Universal y = y_t, non-SUSY VL pairs (1–3 pairs, 1 or 2 chains) | hypothesis | 0 | < 1 | 154.3–183.3 | 129.9–171.6 | yes |
| 9 | 4th generation, up-type only (universal) | hypothesis | 0 | — | 174.0 | 155.1 | — (excluded by h → gg) |
| 10 | **SUSY + 1 VL pair, universal y = y_t** | hypothesis | 1 (M_S, fitted to M_h) | 0.745 | **168.4** | 125 at M_S ≈ 40 TeV | yes (≤ 2%) |
| 11 | Non-SUSY VL pair, fitted c (doc 63) | no | 1 | 0.80 | 172.5 | 151.0–160.7 | yes |
| 12 | **SUSY + 1 VL pair, fitted share** | no | 2 (Δa, M_S) | 0.81 | **172.5** | **124.1** | yes (1.2%) |

**Best candidate:**
- Matching both masses: #12 (a fit).
- Best zero-Yukawa-parameter hypothesis: #10, which is 4 GeV low.
- Best fully derived: #1, 187.1 / 171.3.

## 6. No-go statement

Take any admissible finite space for the spectral action at a₄: Pati–Salam (Chamseddine–Connes–van Suijlekom) or SM algebra, with any of the vector-like Krajewski entries, extra generations, multistage breaking, SUSY with Standard-Model traces, or the BvdBvS traces. Then:

1. **For Higgs-blind content**, y_t/g_L = √(I_L/6) ≥ 1 (doc 68 theorem). The best zero-parameter top is 187.1 GeV.
2. **Lowering y_t/g requires extra Higgs-coupled Yukawa trace**, Δa = 2.21 + 2.07 ΔN (non-SUSY) or y_t/g ≤ 0.80 (SUSY). The axioms do not fix the size of those Yukawas: they are entries of D_F.
3. **Without SUSY**, any content that hits M_t = 172.5 gives M_h = 147–161 GeV.
4. **With SUSY**, the Higgs can be 125, but only by fitting M_S and stop mixing. The top still needs (2) as a fitted share.

**Minimal extra assumption:**
- **Top alone:** one Higgs-coupled vector-like PS family pair with Yukawa c ≈ 0.89 y_t (1 parameter; M_h fails).
- **Top and Higgs:** additionally, low-scale SUSY in the spectral action with M_S ≈ 10 TeV (2 parameters).

Neither is derived. A principle that sets c ≈ 0.88 (not 1), or a mechanism that adds exactly Δa ≈ 6.2 of Yukawa trace, would be needed to promote #12 to a prediction. No such principle was found in docs 61–69.

## 7. Caveats

- **Matching and Yukawa precision.** y_b and y_τ run at one loop above M_S, and the matching is tree level plus the leading stop term. The EFT Higgs is ±2 GeV.
- **Missing threshold.** SUSY threshold corrections to y_t are not included. This matters most for #10.
- **Δ_b.** The Δ_b dependence of tan β is shown (Δ_b = ±0.3).
- **The SUSY rows are not strictly supersymmetric.** The noncommutative MSSM action is not exactly supersymmetric (BvdBvS 1409.5982), so they assume the boundary relations survive the supersymmetric completion.
- **Inadmissible structures.** SU(5)/SO(10) are inadmissible (Lizzi–Mangano–Miele–Sparano, MPLA 11 (1996) 2561). Their rows are formal.
- **4th generation.** It is excluded by Higgs data (Djouadi–Lenz PLB 715 (2012) 310; Eberhardt et al. PRL 109 (2012) 241802).

## 8. Reproduce

```
cd experiments/two_loop_pati_salam
PYTHONPATH=. ../../.venv/bin/python report_69.py      # multistage, radiative, susy_scan, susy_variants, susy_needed (~4 min)
PYTHONPATH=. ../../.venv/bin/python report_69.py combo combo_fit   # ~6 min
PYTHONPATH=. ../../.venv/bin/python report_69.py --figure
```
