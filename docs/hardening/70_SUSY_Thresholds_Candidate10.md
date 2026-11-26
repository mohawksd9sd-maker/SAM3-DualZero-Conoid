# 70. SUSY threshold corrections for candidate #10 (exploratory)

**Date:** 24 November 2026 (America/Chicago)
**Status:** exploratory. The **Dual-Zero regulator is untouched**. The spectral boundary and the content are exactly doc 69 candidate #10: SUSY spectral boundary with Standard-Model traces, plus one Higgs-coupled vector-like Pati–Salam family pair, with both chains having Yukawa = y_t ("universal"). That gives y_t/g = √(5/9) = 0.745, n = 1, and tan β fixed by m_b. The only change is the matching at M_S, together with the MSSM two-loop RGEs for y_b and y_τ.
**Code** (`experiments/two_loop_pati_salam/`):
- `susy_thresholds.py`: thresholds, two-loop MSSM RGEs, and the solver `solve_thr`;
- `report_70.py`: writes `results_doc70.json`;
- `report_70_fig.py`: the figure.

**Figure:** `docs/hardening/figures/70_susy_thresholds.png`.
**Tests:** `tests/test_susy_thresholds.py` (3 tests). The docs 68/69 tests stay in `tests/test_beyond_dial.py` (9 tests).
> **Erratum (26 November 2026, America/Chicago).** Two bugs were fixed in place and every number in this doc was rerun (`results_doc70.json`, figure):
> 1. In `susy_thresholds.py` the two-loop O(α_t α_s) quartic threshold had the X̂_t⁵ coefficient as −1/4. BGSS (arXiv:1407.4081, eq. for Δλ^{2ℓ}) and FlexibleSUSY's HSSUSY have −1. This changes M_h only when X_t ≠ 0: about +0.2 GeV at X̂_t = −2 and +0.7 GeV at X̂_t = −√6, at fixed M_S and tan β (validation rows). The fitted M_S at large negative X_t drops by 7–18%.
> 2. The doc 60 matching used 173.10 instead of 173.34 as Buttazzo v4's reference top mass (see doc 60's erratum). This raises every M_t by **+0.24 GeV**.
>
> Net effect: the degenerate, X_t = 0, μ > 0 benchmark goes from 170.54 (−1.6σ) to **170.78 (−1.4σ)**. With X_t ≈ −2 M_S, 172.5 is now reached with M₃ = M_S. Conclusions are unchanged: there is still no derived match. Doc 69's #10 value of 168.4 shifts to about 168.6 on the same basis. Doc 72 adds the two-loop SQCD top threshold (+0.14 to +0.34 GeV) and three-loop running (net ≈ −0.1 to −0.15 GeV). Doc 73 replaces the fitted M_S with the one fixed by exact unification.

**Question (from doc 69):** candidate #10 gave M_t = 168.4 GeV, 4.1 GeV low, without SUSY thresholds. Do the standard thresholds change that? Can M_t = 172.5 and M_h = 125.1 *both* be reached with no fitted number beyond M_S?

---

## Plain-language summary (for Shawn)

- **The thresholds help, and in the right direction.**
  - The standard one-loop SUSY corrections at M_S raise the predicted top by **about 2 GeV**.
  - That comes from the top-Yukawa threshold (+0.9 GeV), the large-tan β bottom correction Δ_b, which pushes tan β from 56 to 67 (+1.0 GeV), and 3-loop QCD in the SM running (+0.15 GeV).
- **Simplest spectrum** (every superpartner at one mass M_S, no stop mixing, μ > 0), with M_S set so that M_h = 125.1:
  - M_S = 30 TeV and **M_t = 170.8 GeV**: 1.7 GeV, or 1.4σ, low.
  - With μ < 0 the top is **169.2 GeV** (2.75σ low).
  - The parameter-free "miss" shrinks from 4.1 GeV to 1.7 GeV (corrected values).
- **Both 172.5 and 125.1 are reached** only by also choosing large *negative* stop mixing, X_t ≈ −2 M_S, with μ > 0 and M_S ≈ 3.2–4 TeV. That gives **M_t = 172.5–173.3 GeV with M_h = 125.1**.
  - X_t is a free soft-breaking number: nothing in the spectral geometry fixes it. So hitting both masses uses **two fitted numbers (M_S, X_t) for two observables**.
  - It is a fit, not a prediction.
- **Across all the "reasonable" spectra** I scanned (sign of μ, gluino from 0.3× to 3× M_S, X_t from −√6 to +√6 M_S), the top at M_h = 125.1 spans **166.3–173.3 GeV**. The spread comes from the soft-term choices, not from the geometry.
- **Honest bottom line.** With the extra inputs the geometry does not fix, the stand-ins below all fail to make a derived match:
  - the SUSY scale fitted to the Higgs;
  - sign μ = +;
  - a degenerate spectrum;
  - zero mixing.

  Candidate #10 then gives M_t = 170.8 ± ~1 (theory) GeV, which is about 1–1.4σ low. It is not excluded, but it is not a derived match either. It also still rests on three structural assumptions that are not derived: SUSY itself, the extra vector-like pair, and its Yukawa being exactly y_t.
- **Plain SUSY without the vector-like pair stays far off.** It still gives 180–185 GeV even with thresholds.

---

## 1. What was added

All formulas are from Bagnaschi–Giudice–Salvioni–Strumia, arXiv:1407.4081 ("BGSS"), unless noted. Their λ is twice ours (V = λ/2 |H|⁴ vs λ|H|⁴).

| piece | implementation |
|---|---|
| top Yukawa | ŷ_t(MSSM, DR) = y_t(SM, MS)/sin β · (1 + Δg_t^reg + Δg_t^φ + Δg_t^χ), BGSS eqs. (22)–(25). The SUSY-QCD part is −(4/3)g₃²[ln(M₃²/M_S²) + 2F̃₆ − (X_t/M₃)F̃₉]. Stop/higgsino, wino and bino parts are evaluated at m_Q = m_U = m_A = M₁ = M₂ = \|μ\| = M_S. |
| bottom Yukawa | ŷ_b = y_b(1 + δ_ne)/(cos β (1 + Δ_b)), resummed. The tan β-enhanced Δ_b = gluino–sbottom (2α_s/3π)M₃μ tan β I(m², m², M₃²) + higgsino–stop (y_t²/16π²)μA_t tan β I + wino −(3/2)(g²/16π²)M₂μ tan β I. I checked the gluino term against the F̃₉ form of BGSS to better than 1% (test). |
| tau Yukawa | Δ_τ = (μ tan β/16π²)[g′² M₁ I − g² M₂ I] (degenerate; approximate, varied ×0…×2). |
| gauge | DR→MS conversion (g₃: +g₃²/32π², g₂: +g₂²/48π²) and the gluino log −2(g₃²/16π²)ln(M₃/M_S). |
| Higgs quartic | BGSS eq. (8):<br>• tree (g² + g′²)/8 · cos²2β;<br>• Δλ^reg (9);<br>• Δλ^φ (10) in the degenerate-scalar limit with the D-term mixing and heavy-Higgs pieces;<br>• Δλ^χ (11), (13) at \|μ\| = M_{1,2};<br>• the two-loop O(g₃² y_t⁴) term (36);<br>• the tan β-enhanced sbottom/stau trilinears X_b = X_τ = A − μ tan β, with couplings y^SM/(1 + Δ). |
| RGEs above M_S | MSSM two-loop gauge, y_t, y_b, y_τ (Martin–Vaughn PRD 50 (1994) 2282; Barger–Berger–Ohmann PRD 47 (1993) 1093). |
| RGEs below M_S | SM two-loop plus three-loop QCD (doc 60 pipeline). |

**Spectrum inputs (not fixed by the geometry):**
- M_S: all sfermions, m_A, M₁, M₂ and |μ|;
- r₃ = M₃/M_S;
- sign μ;
- X_t/M_S (common A for t, b, τ).

Only |μ| = M_S is implemented for the higgsino–gaugino λ pieces; the code asserts it.

**EFT check.** I ran the plain MSSM with tan β = 20 and M_t = 173.34 (figure panel d):
- X_t = 0: M_h = 116.3 GeV at 2 TeV, 123.9 at 10 TeV and 126.3 at 20 TeV;
- M_S = 2 TeV: 125.1 at X_t = +2 M_S and 123.3 at X_t = −2 M_S.

This matches the SusyHD EFT curves (Vega–Villadoro, JHEP 07 (2015) 159, fig. 3) to within their ≈ ±1–2 GeV band.

## 2. Candidate #10: step by step

Degenerate spectrum, X_t = 0, M₃ = M_S = 40 TeV:

| step | M_t | M_h | tan β |
|---|---|---|---|
| doc 69 pipeline (tree matching, 2-loop SM) | 168.59 | 124.70 | 55.6 |
| + 3-loop QCD in SM running | 168.74 | 124.75 | 55.6 |
| + y_t, non-enhanced y_b, gauge thresholds (Δy_t = −0.46%) | 169.64 | 125.55 | 55.9 |
| + Δ_b (= +0.34: gluino 0.46, wino −0.12), Δ_τ (−0.05), μ > 0 | 170.64 | 126.45 | 66.9 |
| + all Higgs-quartic loop pieces (μ > 0) | **170.64** | **125.80** | 66.9 |
| same, μ < 0 (Δ_b = −0.23) | 169.22 | 124.52 | 45.1 |

- **Why Δ_b raises M_t.** A positive Δ_b means a smaller ŷ_b for the same m_b. The spectral H_d condition, 3y_b² + y_τ² = K, then needs a larger tan β. The larger tan β changes the y_t running, and that helps the top. A negative Δ_b does the opposite.
- **Fixing M_S by M_h = 125.1** (degenerate, X_t = 0, r₃ = 1):

| sign μ | M_S (fitted) | **M_t** | tan β | Δ_b | unification |
|---|---|---|---|---|---|
| + | 29.6 TeV | **170.78** (−1.4σ) | 67.1 | 0.35 | −1.9% |
| − | 53.4 TeV | 169.15 (−2.75σ) | 45.4 | −0.22 | −2.2% |

- **Sensitivity at the μ > 0 benchmark (M_t at M_h = 125.1):**
  - α_s = 0.1170 / 0.1190: 170.2 / 171.4;
  - unification read off from α₂ = α₃ instead of α₁ = α₂: 171.7;
  - Δ_τ × 0 / × 2: 170.6 / 171.0;
  - sbottom/stau trilinears off: 170.8;
  - the two-loop λ term vanishes at X_t = 0.
- **Not included here:** the two-loop SUSY-QCD top threshold. Doc 72 computes it (Bednyakov et al. via FlexibleSUSY): +0.14 GeV at X_t = 0 and +0.34 GeV at X̂_t = −2.
- **Rough theory error on M_t:** ±1–1.5 GeV (an estimate, not a computed error).
- M_t falls only about 0.3 GeV per doubling of M_S. So the M_h theory error (±1–2 GeV, which shifts the fitted M_S by up to a factor of ~2) costs only about ±0.3 GeV in M_t.

## 3. Spectrum scan

- **Grid:** sign μ = ±; M₃/M_S = 0.3, 1, 3; X_t/M_S ∈ {−√6, −2, −1, 0, 1, 2, √6}; M_S = 2–160 TeV.
- **Read-out:** M_t at the M_S where M_h = 125.1.

| sign μ | M₃/M_S | X_t/M_S = −√6 | −2 | −1 | 0 | +1 | +2 | +√6 |
|---|---|---|---|---|---|---|---|---|
| + | 0.3 | 171.1 | 171.2 | 171.0 | 170.6 | 170.6 | 170.8 | 170.5 |
| + | 1 | **172.5** | **172.5** | 171.6 | 170.8 | 170.4 | 169.9 | 169.3 |
| + | 3 | **173.3** | **173.2** | **172.2** | 171.2 | 170.7 | 170.0 | 169.4 |
| − | 0.3 | 171.7 | 171.5 | 170.7 | 169.9 | 169.4 | 168.6 | 168.1 |
| − | 1 | 171.7 | 171.4 | 170.3 | 169.2 | 168.2 | 167.0 | 166.4 |
| − | 3 | 172.1 | 171.8 | 170.6 | 169.3 | 168.3 | 167.0 | 166.3 |

The fitted M_S ranges from 3.2 to 53 TeV (panel c). It is about 3.2–4 TeV in the bold cells and 25–55 TeV at X_t = 0.

**The bold cells are within 0.8 GeV (≈ 0.65σ) of 172.5 with M_h = 125.1.** (After the erratum, every cell with X̂_t ≤ −2, and the μ > 0, M₃ = M_S, X̂_t = −1 cell, is within 1σ.) The bold cells need:
- μ > 0;
- large negative stop mixing, X_t ≈ −(2…2.45) M_S, i.e. X_t opposite in sign to M₃;
- M₃ ≥ M_S;
- M_S ≈ 3.2–4 TeV.

Where the r₃ = 0.3 rows need M_S ≈ 3–7 TeV, the gluino is only ≈ 1–2.2 TeV, at or below the LHC limit. Unification stays within 3.5% everywhere. tan β ranges over 37–74 and Δ_b over −0.37…+0.88.

## 4. Parameter count and verdict

| scenario | fitted continuous | discrete / structural inputs | M_t at M_h = 125.1 | verdict |
|---|---|---|---|---|
| doc 69 #10 (tree matching) | M_S | SUSY, VL pair, y = y_t | 168.4 (≈ 168.6 corrected) | −3.4σ (−3.2σ) |
| #10 + thresholds, degenerate, X_t = 0, μ > 0 | M_S | + sign μ, degenerate spectrum, X_t = 0 | **170.8 ± ~1.2 (th)** | −1.4σ (exp.), ~−1.0σ incl. theory est. |
| #10 + thresholds, μ < 0 | M_S | same | 169.2 | −2.75σ |
| #10 + thresholds, X_t fitted | **M_S, X_t** | + sign μ, M₃ ≥ M_S | 172.5 reached at X_t ≈ −(2…2.45) M_S with M₃ = M_S (M_S ≈ 3.9–4.0 TeV), or at X_t ≈ −1.3 M_S with M₃ = 3 M_S | fit: 2 for 2 |
| plain SUSY (no VL), thresholds, n = 1 | M_S | sign μ | 180.7 (μ < 0) – 185.7 (μ > 0) at 3–10 TeV | excluded |

**Answer:** no. With M_S as the only fitted number, M_t = 172.5 and M_h = 125.1 are *not both* reached.
- The best "no-extra-number" spectrum (degenerate, X_t = 0, μ > 0) gives 170.8 GeV, which is 1.7 GeV low.
- Reaching 172.5 (to ≤ 0.3 GeV) needs X_t ≈ −(1.3…2.45) M_S, a second fitted continuous number. Sign μ and the gluino ratio are additional inputs.
- The thresholds turn a 3.4σ miss into a ≈ 1.4σ near-miss. That is suggestive but not a derivation, and it rests on the structural assumptions of #10:
  - SUSY;
  - one extra Higgs-coupled vector-like PS pair;
  - its Yukawa fixed at y_t (the "universal" guess).

  None of these is forced by the axioms (docs 63, 68, 69).

## 5. Caveats

- **Degenerate-limit formulas.** The one-loop λ threshold uses the degenerate-scalar limit (m_Q = m_U = m_D = m_L = m_E = m_A = M_S). The higgsino–gaugino pieces are implemented only at |μ| = M₁ = M₂ = M_S. The two-loop O(α_s α_t) λ term (BGSS eq. 36) is the M₃ = M_S formula, also used for M₃ ≠ M_S. This mostly affects M_h, and so the fitted M_S, not M_t.
- **Δ_τ and the bino** are approximate (degenerate). Their effect is ±0.2–0.4 GeV in M_t.
- **Vacuum stability at large tan β.** tan β ≈ 60–74 with |μ| = M_S means μ tan β ≈ 67 M_S. Charge/colour-breaking (stau) metastability bounds grow roughly linearly with the slepton masses and should be satisfied for degenerate multi-TeV sleptons, but I did not check them in detail.
- **β convention.** tan β is the spectral output (from the H_d condition plus m_b). The scheme of β (BGSS eq. 7) is a higher-order ambiguity.
- **The SUSY boundary is assumed.** As in doc 69, the noncommutative MSSM action is not exactly supersymmetric (BvdBvS arXiv:1409.5982). So the SUSY spectral boundary relations are an assumption.

## 6. Reproduce

```
cd experiments/two_loop_pati_salam
PYTHONPATH=. ../../.venv/bin/python report_70.py validate breakdown variants plain scan   # ~3 min on 8 cores
PYTHONPATH=. ../../.venv/bin/python report_70.py scan_low                              # adds M_S = 2, 3 TeV
PYTHONPATH=. ../../.venv/bin/python report_70.py --figure
```
