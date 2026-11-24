# 67. Does the model need the "dial"? A systematic test of derived mechanisms for M_t and M_h (exploratory)

**Date:** 24 November 2026 (America/Chicago)
**Status:** exploratory. The **Dual-Zero regulator is untouched**: nothing here uses or changes \(\varepsilon(n)=\omega_0(-1)^nn^{-n}\) or \(\operatorname{Reg}_2\). The Dual-Zero "weighting" outlier in §8 is a separate thought experiment on the heat-kernel series, not a change to the regulator.
**Code:** `experiments/two_loop_pati_salam/derived_mechanisms.py` and `report_67.py`; numbers are in `results_doc67.json` (~6 s).
**Figure:** `docs/hardening/figures/67_dial_and_derived_mechanisms.png`.
**Tests:** `tests/test_derived_mechanisms.py` (8 tests).
**Pipeline:** doc 60, with the doc 63 accounting. Below m_R: two-loop SM plus NNLO matching (Buttazzo et al., JHEP 12 (2013) 089). Above m_R: Pati–Salam two-loop gauge and one-loop Yukawa/quartic running. Every pipeline number carries the doc 60 errors, ±1.2 GeV (M_t) and ±1.8 GeV (M_h). Pass means within 2σ of 172.5 ± 0.7 and 125.1 ± 0.2 after adding the theory error.

---

## Plain-language summary (for Shawn)

- **Is the "dial" needed?** It is not a dial anyone sets; it is a theorem of the spectral action.
  - The gauge kinetic term and the Higgs kinetic term both come from the same heat-kernel coefficient (a₄) with the same moment f₀ of the cutoff function. So y_t(Λ)/g(Λ) is fixed by traces of the finite Dirac operator, for any cutoff function f.
  - To change it you must either add something by hand or change the finite space, which earlier docs showed does not work either.
- **Derived mechanisms tested:** 20 configurations with no hand input. **None reaches the measured top.** Their M_t range is 189.1–193.7 GeV; we need 172.5. The best derived Higgs is 177.8 GeV; we need 125.1.
- **The singlet σ (Chamseddine–Connes 2012) does what the literature says, and only that.**
  - It lowers M_h by 10 GeV (190.5 → 180.5) through the tree-level threshold at m_R, and moves M_t by only 0.03 GeV.
  - **σ does not fix the top.** Even if we force the top to its measured value by hand, σ leaves M_h = 151 GeV.
  - Prediction: m_σ ≈ 1.2×10¹⁴ GeV (≈ 2.9 m_R).
- **Pati–Salam without the first-order condition** (Chamseddine–Connes–van Suijlekom 2013):
  - Light extra scalars make it worse (M_t 191–194).
  - Mixing the ordinary Higgs bidoublet with the (15,2,2) bidoublet *can* bring the top to 172.5. It needs one free mixing angle (θ = −0.30 or 1.35), and the neutrino Yukawa then becomes 1.87× the top's. That drives the Higgs quartic negative (unstable vacuum), so it fails badly.
- **Higher heat-kernel terms (a₆):**
  - Exactly zero for the flat cutoff function Chamseddine–Connes use.
  - About −3% in y_t²/g² for a heat-kernel-shaped f (M_t = 189.1), and −0.6% for the fermionic-entropy function (M_t = 190.1).
  - We need −36%. That would require an a₆ coefficient about 10× my estimate, at the edge of where the expansion makes sense.
- **Everything else is too small:**
  - thresholds at m_R: ±0.9 GeV;
  - thresholds at Λ: ±0.7 GeV;
  - gravity at Λ: 10⁻⁸;
  - product or "two-layer" geometries: exactly invariant;
  - the forced PS relation y_ν = y_t is already in the baseline, and removing it makes things worse (M_t 201.6).
- **Ways that do reach 172.5 all need input, and then the Higgs fails:**
  - the top dial turned by hand: M_h 151;
  - bidoublet mixing: unstable vacuum;
  - asymptotic-safety-type λ(M_Pl) = 0 with the top as input: M_h = 128.8, close to 125.1 but still 2.5σ high (±1.5 GeV theory error), so it fails the 2σ test, and it drops the spectral boundary and takes the top from data.
- **Outliers** (twisted triple, quanta of geometry, zeta-regularized trace, Dual-Zero weighting of the a_n): all reduce to the baseline. This is the same theorem: anything that treats a₄ uniformly keeps y_t/g fixed.
- **Bottom line:** within the spectral action as it stands, the 190/180 GeV problem is structural. Nothing derived moves it by more than ~1 GeV.

---

## 1. The "dial" is a theorem

In Tr f(D_A/Λ) the a₄ term gives
- the gauge kinetic term \(\frac{f_0}{2\pi^2}\cdot\frac{1}{3}\,\mathrm{Tr}_{\rm gauge}\,F^2\);
- the Higgs kinetic term \(\frac{f_0}{2\pi^2}\,\mathrm{Tr}(Y^\dagger Y)\,|DH|^2\);
- the quartic \(\frac{f_0}{2\pi^2}\mathrm{Tr}(Y^\dagger Y)^2|H|^4\).

Canonical normalization gives \(y_t^2=4g^2/a\) and \(\lambda=4g^2b/a^2\), where a and b are trace ratios (doc 60/61 notation). The single moment f₀ cancels, so these relations hold for any f and any overall normalization of the finite space. They can change only if:
- (i) the traces change (the finite space changes: docs 61–64 and §5 below);
- (ii) terms beyond a₄ contribute at the matching scale (§4);
- (iii) the relation is imposed somewhere other than the scale where it holds (§7);
- (iv) new fields mix into the light Higgs (§3).

All four are tested below.

## 2. Candidate 1: the singlet σ (Chamseddine–Connes, "Resilience of the spectral standard model", JHEP 09 (2012) 104)

**Spectral boundary at Λ (n = 1):**

| Coupling at Λ | Value |
|---|---|
| λ | 0.282 |
| λ_hσ | 0.565 (= 2λ) |
| λ_σ = 8g² | 2.26 |

**Run to m_R = 4.2×10¹³ GeV:**

| Coupling at m_R | Value |
|---|---|
| λ | 0.250 |
| λ_hσ | 0.397 |
| λ_σ | 1.19 |

The tree-level threshold is λ_eff = λ − λ_hσ²/λ_σ, so Δλ = −0.133.

| Configuration | Derived? | Params | M_t (GeV) | M_h (GeV) | Pass |
|---|---|---|---|---|---|
| no σ (CCM 2007-like content) | yes | 0 | 190.39 | 190.53 | ✗ |
| **σ at m_R, spectral λ, λ_hσ, λ_σ** | yes | 0 | **190.36** | **180.50** | ✗ |
| σ mass 0.1 m_R / 0.01 m_R | no (m_σ free) | 1 | 190.30 / 190.22 | 179.27 / 178.19 | ✗ |
| Majorana Yukawa y_N = g, 2g at Λ | no | 1 | 190.36 | 180.57, 181.22 | ✗ |
| σ + top forced by hand (r = 0.8026) | no | 1 | 172.50 | 151.37 | ✗ |

- **Prediction:** m_σ ≈ √(2λ_σ(m_R))·v_R ≈ 1.2×10¹⁴ GeV.
- **Verdict:** σ is derived and lowers the Higgs by 10 GeV, but it does nothing for the top, as expected. The top relation is the same trace relation as in Chamseddine, Connes & Marcolli (ATMP 11 (2007) 991), who quoted m_top ≈ 179 GeV in their SM running.
- With our Pati–Salam unification the miss is larger (190). Even with the top forced, σ alone reaches only 151 GeV.
- Doc 61 showed that reaching 125 needs y_ν/y_t ≈ 1.7. That makes λ negative.
- **Approximation:** above m_R the σ sector runs at one loop. The two-loop PS Yukawa proxy is inside the ±1.2/±1.8 GeV error (doc 60).
- **Twisted / grand-symmetry origin of σ** (Devastato–Lizzi–Martinetti, JHEP 01 (2014) 042; Devastato–Martinetti, Math. Phys. Anal. Geom. 20 (2017) 2): it produces the same field content, so the same numbers apply.

## 3. Candidate 2: Pati–Salam without the first-order condition

Sources: Chamseddine–Connes–van Suijlekom, J. Geom. Phys. 73 (2013) 222; JHEP 11 (2013) 132.

| Configuration | Derived? | Params | M_t | M_h | Pass |
|---|---|---|---|---|---|
| extra (1,1,15) scalars light (changes PS running) | yes | 0 | 191.17 | 181.69 | ✗ |
| extra (2,2,15) scalars light | yes | 0 | 193.66 | 187.40 | ✗ |
| light Higgs = cos θ·(1,2,2) + sin θ·(15,2,2), θ fitted | no (θ free) | 1 | 172.50 | λ < 0 (unstable) | ✗ |

**The mixing construction** (`mixed_bidoublet`):
- The spectral kinetic terms of the two bidoublets are orthogonal (Tr Y₁†Y₁₅ = 3 − 3 = 0), and each is normalized to Tr Y†Y = 4g².
- Y₁ = g(1,1,1|1) and Y₁₅ = (g/√3)(1,1,1|−3), so y_t = g(cos θ + sin θ/√3) and y_ν = g(cos θ − √3 sin θ). The quartic is λ = Tr Y⁴/(4g²).
- The top can range from 21 to 204 GeV. The two solutions for 172.5 both have |y_ν/y_t| = 1.87, which drives λ deeply negative.
- **This mechanism moves the top but is not derived (θ is set by an unknown scalar potential), and it kills the Higgs.**

## 4. Candidate 3: higher heat-kernel terms (a₆, moments f₋₂ₖ)

- **Size of the Higgs-vev terms:** corrections proportional to v²/Λ² are 3.9×10⁻²⁶, i.e. nothing.
- **What can matter:** the momentum-dependent a₆ pieces, of the form (∇F)²/Λ² and (∇E)²/Λ² (Gilkey a₆; Vassilevich, Phys. Rept. 388 (2003) 279, eq. 4.29). At p ≈ Λ they shift the ratio of the Higgs and gauge two-point coefficients by δ(y_t²/g²) = c₆·(f₋₂/f₀)·(p/Λ)².
- **Estimate of c₆:** reducing the flat-space a₆ by parts gives c₆ ≈ −0.03. This is a rough estimate with ±100% uncertainty, and I have not done the full Dirac-trace computation.
- **What is needed:** −0.356.

| Cutoff function f | f₋₂/f₀ | δ(y_t²/g²) (c₆ = −0.033) | M_t | M_h | c₆ needed for M_t = 172.5 |
|---|---|---|---|---|---|
| flat near 0 (CC choice: all f₋₂ₖ = 0) | 0 | 0 | 190.36 | 180.50 | impossible |
| e^{−u} (heat kernel) | 1 | −0.033 | 189.08 | 177.77 | −0.36 |
| fermionic entropy h(x) = x/(1+eˣ) + ln(1+e⁻ˣ) (CCvS, CMP 373 (2020) 457) | 0.180 | −0.006 | 190.13 | 180.02 | −2.0 |
| Dual-Zero-type weighting ε(6)/ε(4) = −4⁴/6⁶ | −0.0055 | +0.0002 | 190.37 | 180.52 | 65 |

**Verdict:** derived for a given f, but no natural f gets anywhere near −36%. Getting there would need |c₆·f₋₂/f₀| ≈ 0.36 at p = Λ. At that point a₈, a₁₀ and so on are equally large and the expansion is meaningless.

## 5. Candidate 4: traces over generations, the forced y_ν = y_t, product geometries

| Configuration | Derived? | Params | M_t | M_h | Pass |
|---|---|---|---|---|---|
| PS forced y_ν = y_t (n = 1): baseline | yes | 0 | 190.36 | 180.50 | ✗ |
| full 3×3 Y_ν = Y_u with realistic hierarchy (share 7×10⁻⁶) | yes | 0 | 190.36 | 180.50 | ✗ |
| no Dirac ν Yukawa (n = 0; violates PS) | no | 0 | 201.55 | 212.73 | ✗ |
| product F × F_d (d = 2, 4, 16; all traces × d) | yes | 0 | 190.36–190.37 | 180.51–180.52 | ✗ |
| two independent normalizations ("two dials") | no | 1 | 172.50 | 151.37 | ✗ |

- The forced PS relation y_ν = y_t is a real derived effect: it lowers M_t by 11 GeV (201.6 → 190.4). It is already in the baseline.
- Realistic Tr(Y⁴)/(Tr Y²)² factors change nothing (10⁻⁵ level).
- Product geometries scale every trace by the same factor, so they are exactly invariant.
- Two separate normalizations would need two spectral actions, which is a hand-set dial and no longer derived.

## 6. Candidates 5–6: gravity, asymptotic safety, thresholds

- **Gravity at Λ.** G̃ = Λ²/(8πM_Pl²) = 1.0×10⁻⁸, so gravitational corrections to the running below Λ are of order 10⁻⁷. M_t and M_h are unchanged.
- **Shaposhnikov–Wetterich** (Phys. Lett. B 683 (2010) 196). Their boundary λ(M_Pl) ≈ 0 gives **M_h = 128.8 ± 1.5 GeV** in our two-loop SM with the measured M_t. That is close to data, but:
  - it replaces the spectral boundary;
  - it takes the top from data;
  - it conflicts with unification at Λ = 1.2×10¹⁵ GeV.
- **Top from an asymptotic-safety fixed point** (Eichhorn–Held, PRL 121 (2018) 151302). This needs the gravitational fixed-point couplings as inputs, so it is not a derived spectral prediction and is not computed here.
- **Thresholds, computed rather than tuned:**
  - Heavy states (W_R, leptoquark X, Δ, σ, N) spread ×3 around m_R give a leading-log Δln y_t = 1.0%. A generous finite part, C_F g₄²/16π² × 2, adds 0.55%. Together that is **ΔM_t ≈ ±0.9 GeV** (0.75 GeV per 1% in y_t). We need −19.7% in y_t.
  - Boundary scale at Λ/3 or 3Λ: M_t = 189.7 / 191.0.
  - Kaluza–Klein/Landau towers (doc 61): M_t = 190.36 for M_c/Λ = 0.3–1.

## 7. Candidate 7: the cutoff is not the unification scale

| Cutoff / gauge-meeting scale | M_t | M_h | Comment |
|---|---|---|---|
| 0.01 | 187.09 | 180.01 | g_L, g_R, g₄ unequal at the cutoff |
| 0.1 | 188.84 | 179.46 | same |
| 5 | 191.30 | 181.57 | same |
| SM-group boundary at g₁ = g₂ (doc 61) | 185.0 | 170.1 | best case, still 10σ |

This needs one free parameter, and it violates the spectral gauge boundary itself. Even then the shift is at most 3–5 GeV.

## 8. Outliers

| Outlier | Result | Why |
|---|---|---|
| fermionic spectral action / entropy (CCvS 2020) | 190.13 / 180.02 | a specific f; its a₆ moment is small (§4) |
| twisted spectral triple, σ-dilaton (Martinetti et al.) | = candidate 1 | same field content |
| quanta of geometry, two Cliffords (Chamseddine–Connes–Mukhanov, PRL 114 (2015) 091302) | 190.36 / 180.50 | gives M₂(ℍ)⊕M₄(ℂ), i.e. PS with the same traces |
| zeta-regularized trace normalization | 190.36 / 180.50 | a₄ is the same residue; the f₀ ratio is unchanged |
| Dual-Zero (−1)ⁿn⁻ⁿ weighting of the a_n | 190.37 / 180.52 | gauge and Higgs kinetic terms both sit in a₄, so they get one weight; a₆ is suppressed further by 4⁴/6⁶ |

## 9. Ranking

Ranked by combined pull, derived first.

| Rank | Mechanism | Derived? | Params | M_t (GeV) | M_h (GeV) | Pull (M_t, M_h) | Pass |
|---|---|---|---|---|---|---|---|
| 1 | a₆ with heat-kernel f (c₆ estimated) | yes* | 0 | 189.1 ± 1.2 | 177.8 ± 1.8 | +11.8σ, +29σ | ✗ |
| 2 | **σ at m_R (CC 2012), spectral quartics** | **yes** | 0 | **190.36 ± 1.2** | **180.50 ± 1.8** | +12.7σ, +31σ | ✗ |
| 3 | fermionic-entropy f | yes* | 0 | 190.1 | 180.0 | +12.5σ, +30σ | ✗ |
| 4 | product geometries, PS full Y_ν = Y_u, outliers | yes | 0 | 190.36 | 180.5 | +12.7σ, +31σ | ✗ |
| 5 | extra PS scalars (1,1,15) / (2,2,15) | yes | 0 | 191.2 / 193.7 | 181.7 / 187.4 | worse | ✗ |
| 6 | no σ | yes | 0 | 190.39 | 190.53 | worse | ✗ |
| — | λ(M_Pl) = 0 (SW-type) | no | top input | 172.5 (input) | 128.8 ± 1.5 | M_h +2.5σ | ✗ (nearest miss; not spectral) |
| — | dial by hand, or two dials | no | 1 | 172.5 | 151.4 | M_h +14σ | ✗ |
| — | cutoff ≠ unification scale | no | 1 | 187.1–191.3 | 179.5–181.6 | ≥ +10σ | ✗ |
| — | (15,2,2) bidoublet mixing | no | 1 | 172.5 | λ < 0 | unstable | ✗ |

\*The heat-kernel and entropy rows are derived for a given f, but they depend on my rough estimate of the a₆ coefficient (§4).

**Best derived candidate:** the CC 2012 singlet σ, with no free parameter: M_t = 190.36 ± 1.2 GeV, M_h = 180.50 ± 1.8 GeV, m_σ ≈ 1.2×10¹⁴ GeV. The heat-kernel-f a₆ row is lower by 1.3 GeV, but it rests on an estimated coefficient and on choosing f.

**Verdict.** The top/Higgs relation is fixed by the a₄ structure of the spectral action. No derived mechanism tested moves M_t by more than ~1.3 GeV or M_h by more than ~13 GeV. Every mechanism that reaches the measured top needs input and then fails the Higgs. The open options are now outside the present framework:
- a computed a₆ (or a non-perturbative form factor) much larger than estimated;
- a finite space whose traces differ from Pati–Salam's (the doc 63 search found no principle forcing this).

Dual-Zero intact.
