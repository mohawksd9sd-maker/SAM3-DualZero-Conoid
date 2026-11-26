# 72. Open routes for M_t and M_h on top of candidate #10 (exploratory)

Originator of the SAM-3 / Dual-Zero framework: **Shawn Dykes**. This doc follows up docs 69 and 70. The Dual-Zero regulator is unchanged.
Code: `experiments/open_routes_72/`. Every number below comes from a script there. Results JSON: `results_route*.json`.
Pulls use the doc 60 values σM_t = 1.218 GeV and σM_h = 1.763 GeV, with targets 172.5 and 125.1.

Labels: **[D]** derived (no fitted input), **[F]** fitted to data, **[C]** chosen (a discrete or continuous input set by hand), **[U]** unproven assumption.

## 0. Two bugs found in earlier pipelines (fixed in the repo on 26 November 2026)
1. **Doc 70 `susy_thresholds.py`, two-loop O(α_t α_s) λ threshold.**
   - The code had −X̂_t⁵/4. BGSS (arXiv:1407.4081) and FlexibleSUSY's HSSUSY have −X̂_t⁵.
   - I confirmed this with FlexibleSUSY's general-mass formula in the degenerate limit (x_t = 2.449: 0.003248 against 0.003260).
   - Effect: zero at X_t = 0, about +0.25 GeV on M_h at X̂_t = −2.
2. **Doc 60 `two_loop_higgs.py` matching.**
   - The code used the Buttazzo et al. v4 central couplings (1307.3536v4) but expanded them around v2's M_t = 173.10 instead of v4's 173.34.
   - Effect: M_t read about 0.24 GeV too low.
   - Cross-check with SMDR v1.3 (Martin–Robertson 1907.02500; built locally, `calc_fit` at five (M_t, M_h) points): y_t(M_t) = 0.931530 + 0.005562 (M_t − 172.5) and λ = 0.126087 + 0.002051 (M_h − 125.1). Relative to the pre-fix doc 60 matching that is +0.41 GeV in M_t and −0.06 GeV in M_h. SMDR also moves g_Y and g₂ by about 0.1% and 0.03%, which matters for unification (§ Route 1).

Shawn approved fixing both in place (`MT_REF = 173.34`; coefficient −1). Docs 60 and 70 were rerun and carry dated errata. The tables below use the corrected code; the "pre-erratum" row shows the old value. The test suite passes with updated reference values. In the scripts here, matching mode `doc60` is now the corrected repo matching (identical to `v4ref`), and `prefix` reproduces the old one.

## Route 3: higher orders with no new dials [D]
Cumulative steps, each one a full re-solve of the spectral boundary (`route3_higher_order.py`). Ingredients:
- 2-loop SQCD y_t matching: Bednyakov et al., via FlexibleSUSY `mssm_twoloop_mt.cpp`, wrapped with ctypes.
- O(α_t²) λ.
- 3-loop SM RGEs: Buttazzo et al. App. A plus 4-loop QCD. Validated: λ(M_Pl) = −0.0144 against the paper's −0.0143.
- 3-loop MSSM RGEs: Jack–Jones–Kord hep-ph/0408128, DRED. Gauge coefficients checked against the paper. The extra vector-like pair is included only up to 2 loops.

| step | doc 70 #10 (M_S = 29.6 TeV, X_t = 0) | M_S = 2.66 TeV, X_t = 0 | M_S = 2.53 TeV, X̂_t = −2 |
|---|---|---|---|
| pre-erratum doc 70 | 170.54 / 125.13 | 171.66 / 116.96 | 172.39 / 123.51 |
| + X⁵ fix | 170.54 / 125.13 | 171.66 / 116.96 | 172.39 / 123.75 |
| + matching ref. fix (173.34) = **corrected doc 70** | **170.78 / 125.13** | 171.90 / 116.95 | 172.64 / 123.74 |
| + O(α_t²) λ | 170.78 / 125.16 | 171.90 / 117.02 | 172.64 / 123.86 |
| + 2L SQCD y_t | 170.92 / 125.28 | 172.13 / 117.15 | 172.97 / 124.13 |
| + 3L SM RGEs | 170.88 / 125.24 | 172.09 / 117.13 | 172.93 / 124.11 |
| + 3L MSSM RGEs (**all corrections**) | **170.78 / 125.16** | **171.93 / 117.03** | **172.77 / 123.98** |
| alt.: SMDR v1.3 matching | 170.52 / 124.79 | 171.73 / 116.75 | 172.58 / 123.68 |

(The repo `solve_thr` after the fix reproduces the "corrected doc 70" row to ≤ 0.02 GeV.)

**Verdict.**
- The reference-point fix gives +0.24 GeV on M_t.
- The higher orders together add at most +0.33 GeV before the 3-loop MSSM running and net ≈ 0 to +0.13 GeV after it. M_h moves by ≤ ±0.4 GeV.
- None of this closes the doc 70 gap. With M_S fitted to M_h = 125.1, #10 gives **M_t = 170.8 (−1.4σ)** with Buttazzo-v4 matching and 170.45 (−1.7σ) with SMDR matching (route 2, row 1).

## Route 1: derive M_S (no fit to M_h)
**Dual-Zero, spectral action, conoid.**
- These supply only one scale, Λ, so they cannot generate M_S ≪ Λ.
- M_S = Λ ≈ 6e12 GeV gives M_t ≈ 160.7. Excluded.
- ω₀-type factors are numerology (docs 52 and 61).
- So this route has no [D] answer.

**Unification-derived M_S.**
- The spectral boundary needs g₁ = g₂ = g₃ at Λ, with the trace normalisation.
- Requiring exact triple unification fixes M_S (in practice the SUSY threshold scale) without any top or Higgs input.
- The inputs are [U]: SUSY, the universal Yukawa y = y_t of #10, and a degenerate spectrum.

| matching | X̂_t | sign μ | M_S (TeV) | M_t | M_h | pulls |
|---|---|---|---|---|---|---|
| doc 60 (pre-fix) | 0 | + | 2.66 | 171.66 | 116.98 | −0.69σ, −4.6σ |
| all route-3 fixes + v4 ref | 0 | + | 2.72 | 171.92 | 117.13 | −0.48σ, −4.5σ |
| all fixes + v4 ref | −2 [C] | + | 2.56 | 172.77 | 124.02 | +0.22σ, −0.61σ |
| all fixes + SMDR | 0 | + | 1.68 | 171.94 | 114.42 | −0.46σ, −6.1σ |
| all fixes + SMDR | −2 [C] | + | 1.72 | 172.77 | 122.35 | +0.22σ, −1.56σ |
| all fixes + SMDR | −2.449 [C] | + | 1.72 | 172.82 | 122.45 | +0.26σ, −1.51σ |
| all fixes + SMDR | −2.449 | − | 1.65 | 171.93 | 121.70 | −0.47σ, −1.93σ |
| all fixes + SMDR | 0 | − | 1.48 | 169.15 | 112.22 | −2.75σ, −7.3σ |
| SMDR, α_s = 0.1171 / 0.1189 | 0 | + | 2.19 / 1.30 | 171.28 / 172.60 | 115.6 / 113.1 | |
| SMDR, α_s = 0.1171 / 0.1189 | −2 | + | 2.23 / 1.32 | 172.10 / 173.43 | 123.0 / 121.6 | |

There are no unification solutions for X̂_t ≥ +2 with μ > 0.

("v4 ref" is the corrected repo matching after the erratum. Doc 73 has the full corrected table, including μ < 0, the α_s and matching bands, and the gluino and m_A variants.)

**Verdict.**
- **M_t is a genuine output of unification plus the spectral boundary.** It lands at 171.9–172.8 for μ > 0. That is within 0.5σ, and it holds across the X_t, α_s and matching variants.
- This is an improvement on doc 70's 170.5. The extra assumption is exact unification, [U], in place of fitting M_S to M_h.
- **M_h is not derived.**
  - With X_t = 0 it is 114–117 (−4.5 to −6σ).
  - It needs near-maximal negative stop mixing [C], and even then it is 122.4–124.0 (−0.6 to −1.6σ).
- The derived M_S is exponentially sensitive to the low-energy gauge couplings. It moves from 2.6 TeV to 1.7 TeV between Buttazzo-v4 and SMDR inputs, and by a factor of 1.7 within α_s ± 1σ. That leaves M_h uncertain by about ±1.5 GeV.
- **Not significant as a prediction.** M_t ≈ 172.8 is in range, but it depends on [U] SUSY, [U] the universal y_t, and [C] X_t. M_h stays below 125.

## Route 2: full threshold scan (M_S [F] to M_h = 125.1, everything else scanned)
`route2_threshold_scan.py`, with all fixes and SMDR matching. The input count is beyond M_S.

| shape (units of M_S) | extra inputs | M_S (TeV) | M_t | pull | unif. mismatch |
|---|---|---|---|---|---|
| degenerate, X_t = 0 | 0 | 34.1 | 170.45 | −1.68σ | −2.4% |
| X̂_t = −2.449 / −2 / −1 | 1 | 4.0 / 4.1 / 14.5 | 172.43 / 172.35 / 171.40 | −0.06 / −0.12 / −0.90σ | −0.7% / −0.7% / −1.7% |
| X̂_t = +1 | 1 | 23 | 169.95 | −2.10σ | |
| μ = −1 / 0.3 / −0.3 | 1–2 | 64 / 38 / 44 | 168.80 / 169.74 / 169.33 | −3.0 / −2.3 / −2.6σ | |
| M₃ = 0.3 / 3 | 1 | 38 / 38 | 170.18 / 170.66 | −1.9 / −1.5σ | |
| m_U = 0.5 / 2 | 1 | 65 / 17 | 169.79 / 171.38 | −2.2 / −0.9σ | |
| m_Q = 0.5 / 2 | 1 | 48 / 24 | 170.63 / 170.39 | −1.5 / −1.7σ | |
| m_A = 0.3 / 3 | 1 | 34 / 34 | 170.52 / 170.38 | ≈ −1.7σ | |
| M₃ = 3, X̂_t = −2 | 2 | 3.3 | 173.35 | +0.69σ | +0.8% |

No M_h = 125.1 solution exists for:
- |μ| = 3 M_S, either sign: large tan β ≈ 60, and sbottom/stau Δ_b terms drive λ down.
- X̂_t ≥ +2: M_h is too high at every M_S above 0.8 TeV.

**Verdict.**
- Both masses can be hit within 1σ, but only with **at least two continuous inputs** (M_S [F] and X_t [C]; optionally M₃). The best case is X̂_t ≈ −2.0 to −2.45, M_S ≈ 4 TeV, giving 172.4 / 125.1.
- This is a fit, not a prediction.
- One consistency point: the Higgs-fitted M_S (about 4 TeV) is within about a factor of 2 of the unification-derived M_S (1.7–2.6 TeV). The unification mismatch is −0.7%.
- μ < 0, light m_U, or large |μ| make M_t worse. Heavy m_U and a heavy gluino help slightly.

## Route 4: finite internal spaces beyond Pati–Salam (already covered; summary)
No new admissible algebra changes the trace rule y_t/g_L = √(I_L/6) for Higgs-blind content (doc 68 theorem). Values at the spectral scale, taken from docs 61, 68 and 69:

| finite space | y_t/g at Λ | M_t (GeV) | source |
|---|---|---|---|
| CCM SM algebra C⊕H⊕M₃ (g₂ = g₃ boundary) | ≥ 1.00 (1.155 for n = 0) | 189.5–195.5 | docs 61, 69 #6 |
| Boyle–Farnsworth / B−L + complex σ | 1.00 | 185–190 | doc 61 (6) |
| LR C⊕H_L⊕H_R⊕M₃ / multistage PS → LR → SM | 1.00 | 191.2–191.4 | doc 69 #4 |
| Pati–Salam (Chamseddine–Connes–van Suijlekom) | 1.00 | 190.4 | doc 60 |
| grand algebra / twisted (Devastato–Lizzi–Martinetti) | 1.00 | 190–194 | doc 61 (7) |
| PS + Higgs-blind R-sector content | 1.00 | 187.1 | doc 69 #1 |
| SUSY S0 (CCM traces), n = 1 / 0 | 1.00 / 1.155 | 179–196 | doc 69 |
| SUSY S1 / S2 (BvdBvS traces) | 1.414 / 1.491 | 188–195 | doc 69 |
| SO(10) / SU(5) | — | inadmissible (self-conjugate fundamental: Lizzi–Mangano–Miele–Sparano 1996) | doc 68 |
| needed | 0.72–0.80 | 172.5 | doc 69 |

**Verdict.** No zero-parameter finite space gives y_t/g ≤ 0.80. Getting there needs extra Higgs-coupled Yukawa trace (Δa), as in #10. The doc 69 no-go stands.

## Overall
- **Follow-up:** doc 73 writes up the unification-fixed M_S result on its own, with the corrected numbers.
- No route gives a derived prediction of both masses within about 1σ.
- The most interesting new result (exploratory, not significant): imposing exact gauge unification instead of fitting M_S raises the #10 top to **M_t ≈ 171.9–172.8 (|pull| ≤ 0.5σ)** with no top input.
  - It still rests on [U] SUSY and [U] the universal Yukawa.
  - The Higgs comes out at 114–117 GeV, or 122–124 with chosen near-maximal negative X_t, so it stays 0.6–1.6σ low at best.
- Theory systematics on this M_h: EFT at tan β ≈ 60, the derived M_S's sensitivity to α_s and g_Y, and missing 3-loop vector-like terms. Together they are about ±1.5 GeV.

## Scripts
- `common.py`: pulls and the matching variants (`set_matching`).
- `thr72.py`: general BGSS thresholds.
- `sqcd2l.py` and `fs_ext/`: 2L SQCD.
- `rge3.py`: 3-loop SM and MSSM RGEs.
- `check72.py`: validation.
- `route1_derive_MS.py`, `route1b_unif_MS.py`, `route1c_unif_full.py`, `route1c_fill.py`: route 1.
- `route2_threshold_scan.py`: route 2.
- `route3_higher_order.py`: route 3.
- `smdr/`: SMDR v1.3 build and fit points.
- `refs/`: arXiv sources used.
