# 75. Zero-dial routes for the Higgs mass in candidate #10 (exploratory)

**Date:** 26 November 2026 (America/Chicago)
**Originator of the SAM-3 / Dual-Zero framework, of candidate #10's setting and of the question:** Shawn Dykes.
**Status:** exploratory and conditional. The Dual-Zero regulator is unchanged.
**Code:** `experiments/higgs_routes_75/` (`h75.py`, `route1_3.py`, `route2_run.py`), on top of the doc 72/73 pipeline in `experiments/open_routes_72/`. The only edit there is an add-only slepton mass field `Spec.msl`; its default reproduces every earlier result (tested).
**Results:** `results_route1_3.json`, `results_route2.json`, `results_route2_batch2.json`.
**Tests:** `tests/test_higgs_routes_75.py` (6 new tests), plus the existing suite.
**Builds on:** doc 73. Exact gauge unification fixes M_S, which gives M_t = 171.9 GeV, but M_h = 117.1 GeV at X_t = 0. M_h reaches about 124 GeV only if X_t ≈ −2 M_S is chosen by hand.

Labels as in doc 73: **[D]** derived, **[U]** assumed (structural), **[C]** chosen by hand, **[F]** fitted. Pulls use σ(M_t) = 1.218 GeV and σ(M_h) = 1.763 GeV (doc 60).

---

## Plain-language summary (for Shawn)

- **Route 1, the Pati–Salam D-term boost: zero as the model stands.** In candidate #10, Pati–Salam breaks at the spectral scale Λ ≈ 10¹⁶ GeV, while the soft masses sit at the TeV–tens-of-TeV scale. The boost is set by (soft mass / breaking scale)², about 10⁻²⁵, so ΔM_h ≈ 0. It would add +2 to +5 GeV only if the breaking sector's soft mass were chosen near Λ itself [C], and up to +10 GeV in a limit that needs soft masses above the cutoff. Neither choice is fixed by the model.
- **Route 3, the extra vector-like pair: zero as the model stands.** The pair's masses sit at Λ (docs 68/69), and Martin's formula suppresses its effect by (M_S/Λ)². The result is ΔM_h ≈ 10⁻²⁶ GeV. If the pair were moved to the TeV scale [C], it would add about +2 GeV. That would be a different model, though, because it changes the running that gave the top mass, so it is not counted.
- **Route 2, deriving the stop mixing X_t: this is the step forward.**
  - Take the soft-breaking structure the spectral action allows at Λ (Beenakker–van den Broek–van Suijlekom): gaugino masses, trilinears proportional to gaugino masses, and a universal scalar mass. Then run it down to M_S.
  - The running drives X_t to about −1 × M_S almost no matter where the inputs at Λ start (X̂_t from −0.83 to −1.21 over the whole allowed window). So X_t stops being a dial. It does not reach −2.
  - The derived spectrum is not degenerate: the gluino is about 1.3 M_S, the higgsinos about 0.5 M_S and the sleptons light. Exact unification then puts M_S at about 18–24 TeV instead of 2.7.
  - **Result: M_t = 171.3–171.7 GeV (−0.7 to −1.0σ) and M_h = 126.3–127.2 GeV (+0.7 to +1.2σ) with the Buttazzo matching. The SMDR matching gives M_t = 171.4 (−0.9σ) and M_h = 125.0 (−0.04σ).**
- **Flag.** For the first time in this programme, M_h and M_t both come out within about 1σ without any number tuned to either one. The edge point (0.8, −0.6) sits at +1.2σ in M_h, and α_s −1σ pushes M_t to −1.5σ.
- **What it rests on.** This is conditional, not a theorem. It needs:
  - [U] SUSY in the spectral action;
  - [U] universal gaugino masses at Λ;
  - [U] the BvdBvS soft structure, even though BvdBvS prove their noncommutative MSSM action is not exactly supersymmetric;
  - [C] μ > 0;
  - one-loop soft running and tree-level electroweak breaking.
  
  It also has open problems: the lightest superpartner is a charged stau unless the gravitino is lighter, and m_A is fairly light (0.1–0.3 M_S).

---

## 1. Inputs common to all routes

The content and boundary are candidate #10 exactly, as in doc 73: SUSY spectral boundary with SM traces [U], one Higgs-coupled vector-like PS pair with Yukawa = y_t on both chains [U], tan β from m_b [D], and exact triple unification [D]. All matching and running are the doc 72/73 pipeline:
- BGSS thresholds with the corrected −X̂⁵;
- O(α_t²);
- 2-loop SQCD y_t;
- 3-loop SM and MSSM RGEs;
- Buttazzo-v4 ("v4") or SMDR pole matching.

An extra Δλ at M_S does not enter the M_t / tan β / M_S solve, so routes 1 and 3 change only M_h. This is checked: `mh_with(r, 0)` reproduces the doc 73 M_h to 10⁻⁶ GeV.

## 2. Route 1: Pati–Salam SU(2)_R × U(1)_{B−L} → U(1)_Y non-decoupling D-term

**Formula [D, tree level].** The Higgs carries only T₃R, so g_A = g_R. The breaking fields Σ, Σ̄ have vev u and a common soft mass m. Write S = |Σ|² − |Σ̄|² along the D-flat valley. The potential is

V(S) = m²S²/(4u²) + g_A²(h + S)²/2 + g_B²S²/2.

Minimising over S gives

g′²_eff = g′² [1 + (g_A²/g_B²) · x/(1+x)],  with x = m²/(2u²(g_A² + g_B²)) ~ m²/M_V².

This is the Batra–Delgado–Kaplan–Tait form (hep-ph/0309149). It is tested against direct minimisation and against both limits.

**PS relation.** At v_R, g_R = g₄ (spectral boundary), so g_B² = (3/2)g₄² and g_A²/g_B² = 2/3 [D]. Then Δλ = g′²(Δ − 1) cos²2β / 8 in our normalisation (V = λ|H|⁴).

**Model value of x.** v_R = Λ ≈ 1.3×10¹⁶ GeV, because candidate #10 runs the MSSM all the way to Λ. The BvdBvS scalar-mass term −4(f₂/f₀)Λ² is universal for every scalar, so lowering the MSSM scalars to M_S lowers the breaking-sector scalars too. That gives x ≈ (M_S/Λ)² = 4×10⁻²⁶ (doc 73 points) or 8×10⁻²⁴ (route 2 points). **So ΔM_h = 0.000 GeV [D].**

**Chosen values.** These need m_Σ ~ Λ, or above it. "Tracking" evaluates g′ at M_S. "Frozen" holds the g′(Λ) value from v_R down to M_S. The one-loop running of the hard term was not computed, so the two give a band.

| doc 73 point (v4, μ > 0) | M_t | M_h (route 1 derived) | x = 1 [C] tracking / frozen | x → ∞ [C] tracking / frozen |
|---|---|---|---|---|
| X̂_t = 0 | 171.92 | 117.13 | 119.39 / 122.09 | 121.65 / 127.01 |
| X̂_t = −1.0 [C] | 172.47 | 119.80 | 122.05 / 124.75 | 124.30 / 129.65 |
| X̂_t = −2.0 [C] | 172.77 | 124.02 | 126.26 / 128.94 | 128.50 / 133.82 |

- So ΔM_h is +2.2 to +4.9 GeV at x = 1 and +4.5 to +9.9 GeV for x → ∞.
- Unequal Σ and Σ̄ soft masses would also shift every sfermion mass by about g²(m_Σ² − m_Σ̄²), which would be catastrophic at m ~ Λ. So equal masses are a further [C].
- Nothing changes below Λ, so M_t and unification are unchanged.

## 3. Route 2: X_t from the spectral-action soft boundary, run down

**What the spectral action says.**
- Gaugino masses are free D_F parameters (BvdBvS Part II, arXiv:1409.5983 §4.2).
- Scalar masses are 2Σ r_iN_i|M_i|² − 4(f₂/f₀)Λ². The second term is universal and depends on a free moment f₂ of the cutoff function (eqs. *scalar-mass-term3* and *massterm2*).
- Trilinears are proportional to Yukawa × Σ r_iN_iM̄_i (eq. *trilinterm*). There is no independent A-term.
- In the noncommutative MSSM, r₁ = 9/33 and r₂ = r₃ = 1/6 for 3 generations (Part III, arXiv:1409.5984). Part III also proves that the noncommutative MSSM action is not supersymmetric for any number of generations.

So X_t at Λ is **not derivable as a number**:
- the normalisation of A relative to y_t rests on an identification that Part III shows to be inconsistent;
- f₂ is free;
- the M_i are free.

Dual-Zero (ε(n) = ω₀(−1)ⁿn⁻ⁿ) and the conoid geometry contain no SUSY-breaking parameter.

**What can be derived conditionally.**
- Assumptions: [U] universal gaugino mass M½ at Λ, [U] universal A₀ and m₀ (the BvdBvS structure at equal M_i), and [C] μ > 0.
- Running: one-loop MSSM soft RGEs (Martin–Vaughn hep-ph/9311340), with third-family y_t, y_b, y_τ and couplings from the 3-loop doc 73 MSSM run, from Λ down to M_S.
- μ and m_A come from tree-level EWSB at Q = M_S, with tan β fixed by m_b [D].
- The non-degenerate spectrum is then fed back into exact unification and iterated to convergence (|ΔM_h| < 0.05 GeV).

**Viability (not a fit).** Only part of the (m₀/M½, A₀/M½) plane gives a non-tachyonic stau_R (y_τ(Λ) ≈ 1.1 at tan β ≈ 60), μ² > 0 and m_A² > 0. At the converged couplings that window is m₀/M½ ≲ 0.85, A₀/M½ ∈ [−0.6, 0.4]. The A₀ range shrinks as m₀ grows.
- **Across the window, X̂_t = −0.83 to −1.21.** RG focusing makes A_t(M_S) ≈ −1.6 M½ + 0.34 A₀.
- **X̂_t ≈ −2 is unreachable** in this setting.
- The BvdBvS-weighted scalar boundary (+2r_iN_iM½²) gives X̂_t = −0.67 to −0.85, but it fails EWSB once iterated.

**Results.** All points are μ > 0 and converged. Masses are in units of M_S = √(m_Q m_U).

| m₀/M½, A₀/M½ [C, window] | matching, α_s | X̂_t [D] | M₃, μ, m_A, stau_R | M_S [D] (TeV) | tan β | **M_t** | **M_h** | pulls |
|---|---|---|---|---|---|---|---|---|
| 0.5, 0 | v4, 0.1180 | −0.97 | 1.33, 0.47, 0.20, 0.25 | 21.6 | 58.8 | **171.37** | **126.65** | −0.93σ, +0.88σ |
| 0, 0 | v4 | −1.00 | 1.38, 0.52, 0.26, 0.14 | 20.3 | 59.4 | 171.46 | 126.25 | −0.85σ, +0.65σ |
| 0.15, 0 | v4 | −1.00 | 1.37, 0.52, 0.26, 0.16 | 20.3 | 59.3 | 171.46 | 126.33 | −0.86σ, +0.70σ |
| 0.3, −0.6 | v4 | −1.21 | 1.40, 0.62, 0.28, 0.09 | 18.1 | 60.0 | 171.65 | 126.26 | −0.70σ, +0.66σ |
| 0.3, +0.4 | v4 | −0.86 | 1.34, 0.45, 0.21, 0.19 | 22.5 | 58.8 | 171.29 | 126.33 | −0.99σ, +0.70σ |
| 0.5, −0.3 | v4 | −1.08 | 1.35, 0.53, 0.22, 0.23 | 19.9 | 59.1 | 171.48 | 126.74 | −0.83σ, +0.93σ |
| 0.5, +0.2 | v4 | −0.90 | 1.32, 0.44, 0.19, 0.25 | 22.8 | 58.6 | 171.30 | 126.58 | −0.99σ, +0.84σ |
| 0.75, −0.2 | v4 | −1.00 | 1.29, 0.44, 0.11, 0.33 | 24.1 | 58.4 | 171.31 | 127.04 | −0.98σ, +1.10σ |
| 0.8, −0.6 | v4 | −1.13 | 1.30, 0.51, 0.12, 0.32 | 21.7 | 58.7 | 171.45 | 127.19 | −0.87σ, +1.19σ |
| 0.5, 0 | **SMDR** | −0.98 | 1.33, 0.50, 0.22, 0.24 | 12.8 | 60.3 | **171.37** | **125.03** | −0.93σ, −0.04σ |
| 0.5, 0 | v4, α_s 0.1171 | −0.96 | 1.33, 0.45, 0.19, 0.26 | 29.8 | 58.4 | 170.71 | 127.07 | −1.47σ, +1.12σ |
| 0.5, 0 | v4, α_s 0.1189 | −0.98 | 1.33, 0.50, 0.21, 0.24 | 15.8 | 59.2 | 172.02 | 126.15 | −0.39σ, +0.60σ |

Points outside the window fail EWSB on iteration. Examples are (1.0, 0), (1.0, −0.4), (1.5, −0.6), (1.5, 0.8) and (0.8, 0.3); see `results_route2*.json`.

**Reading.**
- Inside the window, M_h moves by less than 1 GeV and M_t by less than 0.4 GeV. So the two window inputs act as nuisance choices, not dials, and nothing is tuned to M_h or M_t.
- The scheme spread between v4 and SMDR (1.6 GeV) and the EFT uncertainty at tan β ≈ 60 (±1–1.5 GeV, doc 73) dominate.
- Spread from the window: M_h = 126.3–127.2 GeV (v4) and 125.0 GeV (SMDR); M_t = 171.3–171.7 GeV.
- **Estimated: M_h ≈ 126 ± 1 (scheme) ± 1.5 (theory) GeV and M_t ≈ 171.4 ± 0.7 (α_s) ± ~1 (theory) GeV.**

**Caveats.**
1. Soft RGEs are one-loop. Two-loop terms shift A_t/M½ by a few percent, so about ±0.05 in X̂_t and roughly ±0.3 GeV in M_h.
2. EWSB is tree-level at Q = M_S, and m_A² is a small difference of large terms: m_A = 0.1–0.3 M_S, and the edge of the window is set by m_A² → 0. A single SM-EFT below M_S (no 2HDM stage) is a ±~1 GeV approximation at m_A ≈ 0.1 M_S.
3. The lightest MSSM state is the stau_R (0.1–0.33 M_S, below the bino at 0.35 M_S) at every viable point. A stable charged LSP is excluded, so this needs a gravitino LSP or R-parity violation [U]. The long-lived-stau cosmology was not checked.
4. B μ is not derived (EWSB fixes it once tan β is taken from m_b).
5. Vacuum and charge/colour-breaking checks were not done beyond positive diagonal masses.
6. The BvdBvS no-go theorem means the soft structure is borrowed from an action that is not exactly supersymmetric.

## 4. Route 3: the vector-like pair with k = y_t

Martin, arXiv:0910.2732, eq. (deltamhsimple):

Δm_h² = (N_c/4π²) k⁴v² sin⁴β [f(x) + X_k²/(xM²)(1 − 1/(3x)) − X_k⁴/(12x²M⁴)],  f(x) = ln x − (5 − 1/x)(1 − 1/x)/6.

Here x = M_scalar²/M_F², and f(1 + ε) = ε/3 − ε⁴/12 + … (checked with sympy).

- **Model setting [D].** The pair's Dirac masses sit at Λ (docs 68/69, "masses at Λ"). The scalars get the same universal soft mass as everything else, so ε = (M_S/Λ)² ≈ 4×10⁻²⁶. With k = y_t(Λ) = 0.519, Δm_h² = 4×10⁻²⁴ GeV², so **ΔM_h ≈ 2×10⁻²⁶ GeV**. The second chain (H_d) carries cos⁴β and is smaller still.
- **The two-loop VL threshold** is suppressed by the same decoupling. This was not computed separately; it is O(ε) by the decoupling theorem.
- **M_t and unification are unchanged**, since nothing changes below Λ.
- **Counterfactual [C], not part of the model.** Put the pair at the TeV scale with M_F = M_S, soft mass M_S (x = 2), and k = y_t^MSSM(M_S) ≈ 0.80. Then Δm_h² ≈ 600 GeV² and ΔM_h ≈ +2.1 to +2.5 GeV (+12 to +15 GeV at maximal X_k). On the doc 73 X̂_t = 0 point this gives 119.2 GeV.
  - It changes the gauge and y_t running between M_S and Λ (Δb = +4 and k in γ_{H_u}). So the doc 73/route 2 M_t would no longer hold, and it would be a new candidate. It is not counted.

## 5. Combinations

| combination | ΔM_h | M_t | M_h | status |
|---|---|---|---|---|
| 1 + 2 + 3, all at model values | route 2 only | 171.37 (v4) / 171.37 (SMDR) | 126.65 / 125.03 | **[D] conditional on route 2's [U]** |
| route 2 + route 1 (x = 1) [C] | +2.1 to +4.2 | 171.37 | 128.7–130.9 | overshoots (+2 to +3σ) |
| route 2 + route 1 (x → ∞) [C] | +4.1 to +8.4 | 171.37 | 130.8–135.0 | excluded |
| route 2 + TeV VL [C] | +1.3 | (invalid) | 127.9 | overshoots, and invalidates M_t |
| doc 73 X̂ = 0 + route 1 (x = 1, frozen) [C] | +4.96 | 171.92 | 122.1 | −1.7σ |
| doc 73 X̂ = −1 + route 1 (x → ∞, tracking) [C] | +4.51 | 172.47 | 124.3 | −0.45σ, but two choices |

With route 2's derived X_t and spectrum, any further positive boost overshoots. Routes 1 and 3 are therefore not needed, and at their model values they are zero anyway. The NMSSM singlet fallback was not run, because it is not required.

## 6. Bottom line (claim, precisely)

Conditional statement. Assume:
1. [U] a TeV-scale-SUSY spectral boundary (doc 69 #10, SM traces, vector-like pair at Λ with y = y_t);
2. [U] universal gaugino mass, trilinear and scalar mass at Λ, in the soft-breaking structure the spectral action admits (BvdBvS Part II);
3. [C] μ > 0.

Then RG running fixes X̂_t ≈ −1.0 ± 0.2. Exact unification and m_b fix the scale M_S ≈ 13–30 TeV and tan β ≈ 59. Over the full viable window of the remaining boundary ratios:

> **M_t = 171.3–171.7 GeV (−0.7 to −1.0σ) and M_h = 126.3–127.2 GeV (v4; +0.7 to +1.2σ) or 125.0 GeV (SMDR; −0.04σ).**

No number is fitted to M_t or M_h. This is the first point in docs 60–75 where both land within about 1σ together. It is not a proof:
- SUSY, universality and the soft structure are assumptions;
- the stau-LSP and light-m_A issues are open;
- the M_h uncertainty (±~2 GeV including scheme) is comparable to the distance to 125.1.

Unlike doc 73, the Higgs no longer needs a hand-picked X_t.

## 7. Reproduce

```
cd experiments/higgs_routes_75
../../.venv/bin/python route1_3.py            # routes 1, 3 (seconds)
../../.venv/bin/python route2_run.py          # route 2, batch 1 from doc 73 (~10 min, 8 cores)
../../.venv/bin/python route2_run.py batch2   # route 2 window, SMDR, alpha_s (~25 min)
```

## 8. References

- W. Beenakker, T. van den Broek, W. D. van Suijlekom, arXiv:1409.5982, 1409.5983 (SUSY breaking: soft terms from the spectral action), 1409.5984 (noncommutative MSSM; no-go theorem). Sources are in `experiments/open_routes_72/refs/`.
- P. Batra, A. Delgado, D. E. Kaplan, T. M. P. Tait, JHEP 02 (2004) 043, hep-ph/0309149 (non-decoupling D-terms).
- S. P. Martin, Phys. Rev. D 81 (2010) 035004, arXiv:0910.2732 (vector-like matter and m_h); source in `refs/0910.2732`.
- S. P. Martin, M. T. Vaughn, Phys. Rev. D 50 (1994) 2282, hep-ph/9311340; S. P. Martin, hep-ph/9709356 (soft RGEs).
- A. H. Chamseddine, A. Connes, W. D. van Suijlekom, JHEP 11 (2013) 132 (spectral Pati–Salam).
- Pipeline references as in doc 73 (BGSS 1407.4081, FlexibleSUSY/HSSUSY, Buttazzo et al. 1307.3536v4, SMDR 1907.02500, Jack–Jones–Kord hep-ph/0408128).

Credit: the SAM-3 / Dual-Zero framework, the spectral Pati–Salam programme in this repository, and the questions that led here are Shawn Dykes's. The computations are exploratory checks of his framework.
