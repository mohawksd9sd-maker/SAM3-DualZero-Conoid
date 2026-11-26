# 76. Doc 75's open problems: stau LSP, two-loop soft running, m_A versus the LHC, M_h theory error (exploratory)

**Date:** 26 November 2026 (America/Chicago)
**Originator of the SAM-3 / Dual-Zero framework, of candidate #10's setting and of the question:** Shawn Dykes.
**Status:** exploratory and conditional. It uses the same assumptions as doc 75. The Dual-Zero regulator is unchanged.
**Code:** `experiments/doc76/`:
- `softsusy_2loop.py` runs SOFTSUSY with one-loop versus two-loop soft running.
- `rerun76.py` redoes the exact-unification solve with the corrected spectrum and varies the matching scale.
- `gravitino76.py` does the gravitino-LSP bookkeeping.
- `lhc76.py` gives m_A in GeV against the LHC search ranges.

Results are in `results_*.json`, and the log is in `log_rerun76.txt`.
**External tool:** SOFTSUSY 4.1.13 (B.C. Allanach, hep-ph/0104145). It is built locally and not vendored. `softsusy-4.1.13-doc76.patch` adds a one-line environment switch, `SS_SOFT_1LOOP`, that drops only the two-loop soft beta-function terms (Martin–Vaughn, hep-ph/9311340). The `SS_RGE_LOOPS` hunk in the patch is unused, because it had no effect.
**Tests:** `tests/test_doc76.py` (9 tests). They need no SOFTSUSY binary.
**Points:** the five doc 75 route-2 points (m₀/M½, A₀/M½) = (0.5, 0), (0.75, −0.2), (0.3, −0.6), (0.8, −0.6), (0, 0). All use Buttazzo-v4 ("doc 60") matching, α_s = 0.1180 and μ > 0.

Labels: **[D]** derived, **[U]** assumed, **[C]** chosen, **[F]** fitted. Pulls use σ(M_t) = 1.218 GeV and σ(M_h) = 1.763 GeV.

---

## Plain-language summary (for Shawn)

- **(b) Two-loop soft running is a small effect.** Turning on the two-loop soft terms shifts:
  - M_S/M½ by −1.3 %;
  - X̂_t by +0.01;
  - μ by +5 %;
  - m_A by +3 %.

  After re-solving unification, **M_t moves by +0.02 GeV and M_h by −0.02 to −0.19 GeV.**
- **(c) The "light m_A" was an artefact of tree-level EWSB.** The bigger finding is that the doc 75 m_A came from tree-level electroweak breaking. At tan β ≈ 60, m_A² is a near-cancellation (m²_Hd − m²_Hu). SOFTSUSY's one-loop tadpoles, with the tan β-enhanced stop and sbottom terms, lift it a lot: **m_A/M_S goes from 0.11–0.28 to 0.44–0.50, so m_A ≈ 7.7–9.1 TeV.** That is far above every Run-2 A/H → ττ search: ATLAS reaches 2.5 TeV and CMS 3.5 TeV. **The light-m_A problem is gone.** Even the doc 75 tree values were safe at three points and only marginal (≈ 2.6 TeV, inside the CMS range) at two.
- **(d) M_t and M_h after all corrections.**
  - With the loop-corrected μ and m_A, exact unification gives M_S ≈ 16.6–19.0 TeV, lower than doc 75's 18–24 TeV.
  - **M_t = 171.36–171.69 GeV (−0.66 to −0.94σ) and M_h = 125.76–126.67 GeV (+0.38 to +0.89σ).** M_h moves down by 0.3–0.6 GeV, towards the data, and M_t barely moves (+0.03 to +0.05 GeV).
  - All five points are now within 1σ in both masses (Buttazzo matching). That is still conditional on doc 75's assumptions, and m₀ and A₀ are chosen.
- **M_h theory error.** Varying the matching scale over Q ∈ [M_S/2, 2M_S], with the same physical spectrum, moves M_h by −0.37/+0.29 GeV and M_t by −0.35/+0.28 GeV.
  - Two-loop soft running contributes ≲ 0.2 GeV.
  - The one-loop EWSB shift was 0.3–0.6 GeV, so its higher orders are not negligible. I take ±0.3 GeV [C], which is not computed.
  - Without the matching scheme, the error is **about ±0.5 GeV**.
  - **The dominant piece is still the matching-scheme spread.** Buttazzo-v4 versus SMDR differed by 1.6 GeV at the doc 75 (0.5, 0) point. Doc 76 did not reduce it, and it was not rerun with SMDR. An honest total is still about ±1 GeV.
- **(a) The stau LSP is not fixed by anything derived.**
  - **Minimal R-parity violation is not available.** In the Beenakker–van den Broek–van Suijlekom (BvdBvS) spectral MSSM, R-parity is a grading built into the finite spectral triple. Its building-block rule forbids the RPV trilinears (LLE, LQD, UDD). Adding RPV would mean leaving that framework [U]. **Within it, RPV is excluded [D].**
  - **A gravitino LSP is consistent but chosen, not derived.**
    - The spectral action contains gravity but no supergravity, so a gravitino is an extra assumption [U] and its mass is chosen [C].
    - A gaugino-mediation-like guess m_{3/2} ≈ M½ Λ/(√3 M̄_P) ≈ 23–25 GeV [C] works: the stau lifetime is 0.04–36 s, within the CBBN bound of about 5×10³ s, and the stau-decay gravitino density is Ω h² = 0.004–0.065, below 0.12.
    - It forces a low reheating temperature, T_R ≲ 2×10⁶ GeV, because thermal gravitino production is boosted by the ~25 TeV gluino. **That excludes standard thermal leptogenesis.**
  - **Verdict.** The stau-LSP issue becomes "chosen extra structure [U]+[C]", not "derived". The stau is still the lightest MSSM sparticle at every point after the corrections.

---

## 1. Two-loop soft running (item b)

SOFTSUSY is run with the doc 75 boundary:
- M½, m₀ and A₀ universal at a **fixed** scale Λ (EXTPAR 0 = Λ from doc 75, about 7.4×10¹⁵ GeV);
- tan β from doc 75 and μ > 0;
- M½ = M_S(doc 75)/(M_S/M½).

It is run twice, once with and once without the two-loop soft beta terms. The gauge and Yukawa running is identical in both runs.

The ratio of the outputs at Q = M_S is the two-loop correction. It is applied multiplicatively to the doc 75 Spec, and additively for X̂_t. SOFTSUSY's own Higgs mass is not used.

| point | M_S/M½ 1L → 2L | X̂_t | μ/M_S | m_A/M_S (SOFTSUSY, loop EWSB) | τ̃_R/M_S |
|---|---|---|---|---|---|
| (0.5, 0) | 1.391 → 1.372 | −0.951 → −0.939 | 0.525 → 0.554 | 0.482 → 0.497 | 0.232 → 0.240 |
| (0.75, −0.2) | 1.425 → 1.407 | −0.976 → −0.964 | 0.502 → 0.531 | 0.458 → 0.474 | 0.314 → 0.323 |
| (0.3, −0.6) | 1.334 → 1.319 | −1.176 → −1.166 | 0.656 → 0.684 | 0.483 → 0.495 | 0.071 → 0.092 |
| (0.8, −0.6) | 1.418 → 1.402 | −1.098 → −1.088 | 0.566 → 0.594 | 0.459 → 0.475 | 0.294 → 0.307 |
| (0, 0) | 1.351 → 1.333 | −0.983 → −0.970 | 0.565 → 0.595 | 0.502 → 0.516 | 0.133 → 0.140 |

The one-loop SOFTSUSY ratios agree with doc 75's own one-loop running to a few per cent: M_S/M½ 1.39 versus 1.40, and X̂_t −0.95 versus −0.97. The remaining differences come from SOFTSUSY's own input y_t, because it takes M_t = 172.57 GeV as input instead of using our prediction.

**The derived X̂_t ≈ −1 is stable under two-loop soft running [D, within the assumptions].**

## 2. Loop-corrected EWSB and m_A (item c)

Doc 75 set μ and m_A from tree-level EWSB at M_S. Plugging SOFTSUSY's own m²_Hu and m²_Hd into the tree-level formula gives m_A/M_S = 0.19–0.29 with one-loop soft running, which matches doc 75's 0.11–0.28 to within the y_t difference. With two-loop soft running the tree value is 0.22–0.31. Adding its one-loop tadpoles gives m_A/M_S = 0.47–0.52. **So the shift comes from the loop EWSB, not from the running.**

In `rerun76.py` ('ewsb1L'), μ² and m_A² are shifted by SOFTSUSY's (loop − tree) difference at the same point, and then unification is solved again:

| point | doc 75: M_S / M_t / M_h | + 2L soft | + 1L EWSB | m_A/M_S tree → 1L | m_A [GeV] doc 75 → doc 76 | pulls (M_t, M_h) |
|---|---|---|---|---|---|---|
| (0.5, 0) | 21.6 / 171.37 / 126.65 | 21.6 / 171.39 / 126.62 | **18.6 / 171.42 / 126.25** | 0.20 → 0.47 | 4300 → 8782 | −0.89, +0.65 |
| (0.75, −0.2) | 24.1 / 171.31 / 127.04 | 24.0 / 171.33 / 127.02 | **19.0 / 171.36 / 126.46** | 0.11 → 0.44 | 2629 → 8317 | −0.94, +0.77 |
| (0.3, −0.6) | 18.1 / 171.65 / 126.26 | 18.2 / 171.67 / 126.07 | **16.6 / 171.69 / 125.76** | 0.28 → 0.48 | 5014 → 7913 | −0.66, +0.38 |
| (0.8, −0.6) | 21.7 / 171.45 / 127.19 | 21.7 / 171.47 / 127.18 | **17.5 / 171.50 / 126.67** | 0.12 → 0.44 | 2573 → 7650 | −0.82, +0.89 |
| (0, 0) | 20.3 / 171.46 / 126.25 | 20.4 / 171.48 / 126.11 | **18.2 / 171.51 / 125.78** | 0.26 → 0.50 | 5307 → 9084 | −0.82, +0.39 |

(M_S is in TeV and the masses in GeV.)

**LHC.** The published Run-2 ττ searches reach:
- ATLAS 139 fb⁻¹ (arXiv:2002.12223): 0.2–2.5 TeV. In the M_h¹²⁵ scenario, tan β > 8 is excluded at 1 TeV and tan β > 21 at 1.5 TeV.
- CMS 138 fb⁻¹ (arXiv:2208.02717): σ×BR limits up to 3.5 TeV.

All doc 76 m_A values (7.7–9.1 TeV) are beyond both. **m_A is not constrained by the LHC [D].** This is a range comparison, not a recast. No recast is needed above the search range.

The two doc 75 tree-level points near 2.6 TeV would have needed a CMS recast at tan β ≈ 60. That question no longer arises.

Caveats:
- SOFTSUSY's tadpole shift is applied as a difference computed with its own couplings. Its y_t differs from ours by about 3 %.
- The two-loop tadpoles are not included.
- m_A at about 8 TeV is far above the LHC reach, so the conclusion is robust to these.

## 3. Matching-scale error (items b and d)

The same physical spectrum is matched at Q = M_S/2 and at Q = 2M_S. Every Spec mass is divided by c = 1/2 or 2, and unification is solved again. The recovered Q/c agrees with M_S to within 10 % (tested).

| point | M_t (Q = M_S/2, M_S, 2M_S) | M_h (Q = M_S/2, M_S, 2M_S) |
|---|---|---|
| (0.5, 0) | 171.06 / 171.42 / 171.70 | 125.88 / 126.25 / 126.54 |
| (0.75, −0.2) | 171.00 / 171.36 / 171.64 | 126.11 / 126.46 / 126.74 |
| (0.3, −0.6) | 171.37 / 171.69 / 171.96 | 125.41 / 125.76 / 126.03 |
| (0.8, −0.6) | 171.15 / 171.50 / 171.77 | 126.33 / 126.67 / 126.93 |
| (0, 0) | 171.16 / 171.51 / 171.78 | 125.41 / 125.78 / 126.07 |

Theory-error budget for M_h. These are estimates, not a full analysis.

| source | size |
|---|---|
| matching scale Q ∈ [M_S/2, 2M_S] | −0.37 / +0.29 GeV |
| two-loop soft running (the full effect, as an upper bound on its residual) | ≲ 0.2 GeV |
| higher-order EWSB, half of the one-loop shift | ±0.3 GeV [C] |
| **subtotal (in quadrature)** | **≈ ±0.5 GeV** |
| matching scheme, Buttazzo-v4 vs SMDR (doc 75 at (0.5, 0): 126.65 vs 125.03) | 1.6 GeV spread, **not reduced here** |

So the honest total is still **about ±1 GeV**, and it is dominated by the matching scheme. The scale part is now under control. Rerunning the doc 76 points with SMDR matching is the next step.

The M_t scale variation (±0.3 GeV) is about a quarter of σ(M_t).

## 4. Stau LSP (item a)

At every point the lightest MSSM sparticle is the τ̃, with m_τ̃ = 1.5–6.2 TeV against a bino at 6.0–6.6 TeV. It uses the two-loop-soft ratio × the corrected M_S, without L–R mixing. A stable charged relic is excluded, so something must make the stau decay.

**Minimal R-parity violation: excluded within the framework [D].** In BvdBvS (arXiv:1409.5982, "R-parity" section), R-parity is a grading of the finite spectral triple. The third-type building blocks that would generate cubic superpotential terms must contain one or three R-odd representations. LLE, LQD and UDD are therefore structurally absent. RPV would mean adding non-spectral terms by hand [U], which goes outside the model doc 75 used. So RPV is not "minimal" here.

**Gravitino LSP: consistent, but assumed and chosen [U]+[C].** The spectral action has no supergravity, so the gravitino and its mass are additions. As a benchmark, take m_{3/2} ≈ M½ Λ/(√3 M̄_P) [C]. This is the gaugino-mediation analogy, with M̄_P = 2.435×10¹⁸ GeV. The formulas are in `gravitino76.py`, with:
- the width from Feng–Su–Takayama (hep-ph/0404198);
- the stau yield Y = κ·10⁻¹³ (m/100 GeV) with κ = 0.4–1.5 (Pradler–Steffen 0808.2462);
- thermal production from Bolz–Brandenburg–Buchmüller (hep-ph/0012052);
- the CBBN bound from Pospelov (hep-ph/0605215).

| point | m_τ̃ [GeV] | m_{3/2} [C] | τ_τ̃ [s] | τ_τ̃ at m_{3/2} = 100 GeV | m_{3/2} max (Ω_NTP ≤ 0.12) | Ω_NTP h² at the benchmark | T_R max |
|---|---|---|---|---|---|---|---|
| (0.5, 0) | 4472 | 25.0 | 0.21 | 3.3 | 64–241 | 0.012–0.047 | 1.9×10⁶ |
| (0.75, −0.2) | 6160 | 25.4 | 0.043 | 0.66 | 47–175 | 0.017–0.065 | 1.9×10⁶ |
| (0.3, −0.6) | 1532 | 22.8 | 36 | 7.1×10² | 188–705 | 0.004–0.015 | 1.9×10⁶ |
| (0.8, −0.6) | 5380 | 23.9 | 0.074 | 1.3 | 54–201 | 0.014–0.053 | 2.1×10⁶ |
| (0, 0) | 2547 | 24.4 | 3.3 | 55 | 113–424 | 0.007–0.026 | 1.8×10⁶ |

What the table shows:
- Every point passes the CBBN bound (τ ≲ 5×10³ s) and the non-thermal relic bound at the benchmark.
- Thermal gravitino production with a gluino of about 25 TeV forces T_R ≲ 2×10⁶ GeV. **That rules out standard thermal leptogenesis**, which needs T_R ≳ 10⁹ GeV. This is the price of the gravitino route.
- Hadronic-BBN limits for the τ ≳ 10 s points ((0.3, −0.6) and (0, 0) at heavier m_{3/2}) are not checked here.
- The gravitino does not touch M_t or M_h, since it couples with Planck suppression.

## 5. What changed and what did not

- **Changed.**
  - μ and m_A are now loop-corrected, and m_A is about 8 TeV.
  - M_S is now 16.6–19.0 TeV.
  - **M_h is 125.8–126.7 GeV and M_t is 171.4–171.7 GeV. Both are within 1σ at all five points**, using Buttazzo matching only.
- **Unchanged.**
  - X̂_t ≈ −1 is stable.
  - The stau is the LSP.
  - The matching-scheme spread of about 1.6 GeV is still the dominant M_h error.
  - The Dual-Zero regulator is untouched.
- **Still conditional.** All of this rests on:
  - [U] SUSY in the spectral action;
  - [U] universal soft terms of the BvdBvS form at Λ (BvdBvS prove that the NC MSSM is not exactly supersymmetric);
  - [C] μ > 0;
  - [C] the m₀ and A₀ values;
  - for a viable cosmology, [U] a gravitino with [C] its mass and a low T_R.

  **This is not a derivation of the Standard Model masses.**
- **Not done.**
  - SMDR rerun of the doc 76 points;
  - two-loop tadpoles;
  - stau L–R mixing in the LSP mass;
  - a hadronic-BBN check for the τ ≳ 10 s points;
  - an LHC recast, which is not needed because m_A is beyond the search range.
