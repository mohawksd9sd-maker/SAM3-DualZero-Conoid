# 74. Sound from the banks: Shawn Dykes's sound / frequency / chirp ideas tested against real data

**Date:** 26 November 2026 (America/Chicago)
**Originator of the ideas:** Shawn Dykes (26 Nov 2026). Any credit for these ideas goes to Shawn Dykes.
**Status:** exploratory toy-model tests. The **Dual-Zero regulator, the top and the Higgs results are untouched.**
**Code** (`experiments/time_medium_sound/`):
- `sound_banks.py`: toy cavity, low-ℓ statistics, focus filter, tone/comb/chirp spectra, speech-phrase model;
- `lowell_focus_rings.py`: map tests on Planck PR3 SMICA (+ WMAP 9 ILC);
- `report_74.py`: driver (`toy tones chirp chirp_lee chirp_lee_exact lowell focus rings rings_obs`);
- results: `results_doc74.json` (toy, tones, chirp) and `results_maps.json` (map tests).

**Tests:** `tests/test_sound_banks.py` (5 tests, all pass).
**Builds on:** doc 66 (bounded pond / finite topology, matched circles, coherent mode phases) and doc 71 (echo features, CCC rings on WMAP, GW echoes).

---

## What had already been tested (not re-run)

| Idea | Where | Result |
|---|---|---|
| Reflecting bank → linear / log oscillations in P(k) ("pure tone" as a small ripple on the spectrum) | doc 71 §1a/1b | no signal, A ≲ 1.2–1.3% |
| Penrose/CCC rings, WMAP 9 | doc 71 §2 | nothing unusual |
| GW echoes, dispersion, future bank, α drift | doc 71 §3–6 | excluded / untestable |
| Finite "pond" (torus, sphere, dodecahedron), low quadrupole, matched circles | doc 66 B | best fits excluded by circles; allowed gain Δχ² ≥ −1 |
| All modes in phase in a finite box → C₂ and odd ℓ vanish | doc 66 "mode phases" | excluded (D₃ = 937, D₅ = 1502 μK²) |
| Finite-information causal diamond echo delays | sam3-tests/nullcone | consistent, no new limit |

Everything below is **new**.

## Plain-language summary (for Shawn)

1. **Sound driven inward from the banks.** In the toy model the in-phase drive really does focus in the middle (a sphere gives a centre/edge gain of kR/sin kR, ×21 at kR = 3). It also selects only the fully symmetric patterns: in a cube, an observer at the focus sees only ℓ = 4, 6, 8…, and an observer off the focus sees a pattern lined up around one axis (m = 0). The real sky shows **none of these**:
   - no common axis of m = 0 patterns (p = 0.50 Planck, 0.13 WMAP);
   - the real quadrupole and octopole *are* lined up (axes 8° apart, p ≈ 0.01; planar and aligned together p ≈ 0.0006). But they are flat "planar" patterns (power in |m| = ℓ), the **opposite** of what a focus makes. This is the known "axis of evil" anomaly, not a confirmation;
   - parity: a symmetric in-phase drive makes even ℓ stronger. The sky has **odd ℓ stronger** (R = 0.66 at ℓ ≤ 20, p = 0.005 locally), so the sign is wrong. An antiphase (opposite banks out of step) drive would get the sign right, but along one axis it would also make odd ℓ axisymmetric, and ℓ = 3 is strongly non-axisymmetric (p = 0.97). It stays a lead only, not evidence;
   - no focus spot: the best concentric "focus" pattern (hot centre, (l, b) = (321°, −33°)) has global p = 0.13.
   **Verdict: fail for the simple version; inconclusive for tuned versions.**
2. **One original frequency.** A single tone cannot make the CMB. It would make one bump in the spectrum, not the series of acoustic peaks: Δχ² = +2.7×10⁵ to +9.5×10⁴ worse than standard for narrow tones; even a tone spread over a factor ~20 in scale is still +276 worse. A tone matched to the BAO scale (r_d = 147 Mpc) is +4.9×10⁵ worse. A tone *with its overtones* (n·k₀) only fits once the overtones are so dense and broad that they blur into a smooth spectrum (k₀ ≲ 8×10⁻⁴ Mpc⁻¹ with 35% widths, Δχ² = +12…+25; narrower combs fail by ≥ 38). The acoustic peaks come from sound in the hot plasma (sound horizon r_* = 144.4 Mpc, r_d = 147.1 Mpc, derived by CAMB from the plasma sound speed and time). They do not come from the pitch of the first sound. Small sharp tones on top of the standard spectrum are limited to a few % (w = 0.3: B < 1–4%; w = 0.03: B < 3–15%), and the largest local hint is Δχ² = 3.0. **Verdict: fail (single tone); no hint of a tone feature.**
3. **Changing frequency / "let there be light".** A sweep maps to a tilt (stationary phase). A linear sweep gives n_s = 2, and ω ∝ t² gives n_s = 1.5. Both are excluded (Planck n_s = 0.9649 ± 0.0042). An **exponential sweep gives exactly n_s = 1**, and a rate that drifts 3.5% per e-fold gives n_s = 0.965 with zero running (Planck running −0.0045 ± 0.0067). That *passes*, but it is mathematically the same as standard slow-roll inflation (exponential stretching), so it is not a new prediction. A spoken phrase:
   - its sound spectrum (pitch harmonics + formants) used as the spectrum: Δχ² = +2.0×10⁵. **Excluded**;
   - its loudness pattern laid along scale (earlier words → bigger structures): the best placement squeezes the phrase into 0.5 e-folds at k ≈ 0.001–0.0017 Mpc⁻¹ (ℓ ≈ 14–24, the known ℓ≈20 dip). It *improves* the fit by Δχ² = 8.4, global p = 0.016 with a Gaussian likelihood. **With the correct low-ℓ likelihood it drops to Δχ² = 4.3, p = 0.16.** Not significant. Over larger spans the gaps between words are excluded.
   **Verdict: smooth exponential sweep passes but equals inflation; speech-like imprint fails or is inconclusive.**
4. **Penrose rings on Planck** (doc 71 had only WMAP): with ΛCDM sims the Planck sky has *fewer* low-variance rings than expected (697 vs 923, p_le = 0.045; families ≥ 3: 19 vs 56, p_le = 0.015), which is the opposite of the CCC excess. With sims that use the observed low-ℓ power (as in doc 71) it is ordinary: 697 vs 793 (p_ge = 0.75), families 19 vs 40 (p_ge = 0.92), z_min p = 0.69. The deficit comes from the known lack of large-angle power, not from rings.
   Simple Hawking-point count: fewer high-variance 4° discs than sims (3 vs 8.9, p = 0.91; 6 vs 8.9, p = 0.70 with observed low-ℓ power). **Verdict: no rings, no Hawking points.**

**Nothing here is significant.** The only sub-3σ items (the axis of evil, the parity asymmetry and the ℓ≈20 dip) are well-known anomalies. Here they came out with the wrong sign or shape for the simple banks model, or vanished with a correct likelihood.

---

## 1. Toy model (derived vs assumed)

- **Assumed:** time-medium ripples obey the scalar Helmholtz equation (∇² + k²)Φ = 0 inside a bounded domain. The banks impose Φ = drive on the boundary. The CMB temperature traces Φ on the observer's last-scattering sphere (Sachs–Wolfe-like, ΔT ∝ Φ). Wavenumber maps linearly to temporal frequency.
- **Derived:**
  - Sphere: Φ = j₀(kr)/j₀(kR), so the centre gain is |kR/sin kR| (1.19, 2.20, 21.3, 74.6 at kR = 1, 2, 3, 3.1; it diverges at the resonances kR = nπ).
  - Cube (finite differences, 41³, 2% damping): centre gain 3.2, 5.1, 23.2 at kL = 2, 3.7, 5. For an observer at the focus with r = 0.6 L, ≥ 97.6% of the anisotropic power is in ℓ = 4, the rest in ℓ = 6, 8, and **ℓ = 2, 3, 5, 7 are exactly zero** (cubic symmetry). Off the focus the sky is dipole-dominated (87–98%).
  - Off-focus sphere: Φ = Σ(2ℓ+1) j_ℓ(kd) j_ℓ(kr) P_ℓ(cos θ), so only m = 0 about the focus axis.

## 2. Results table

| Test | Data | Prediction | Our number | Verdict |
|---|---|---|---|---|
| Common m=0 axis, ℓ=2–10 | Planck PR3 SMICA inpainted; WMAP9 ILC; 10⁴ isotropic sims | high | S = 0.229 (p = 0.50); WMAP 0.262 (p = 0.13) | fail |
| Per-ℓ m=0 dominance | same | high | all p ≥ 0.05 (ℓ=9 p = 0.048, 9 trials) | fail |
| Quad–oct planar axes | same | (focus: m=0, not planar) | 8.1° apart, p = 0.0098; planar+aligned p = 0.0006 (WMAP 3.2°, 0.0003); axis (l, b) ≈ (240°, 55–63°) | known anomaly, wrong shape for the model |
| Parity R = ⟨D_even⟩/⟨D_odd⟩ | Planck 2018 TT (Commander ℓ<30), 2×10⁴ χ² sims | ≫ 1 (in-phase) | 0.38 (ℓ≤5) … 0.66 (ℓ≤20, p = 0.005) … 0.79 (ℓ≤30, p = 0.016) | wrong sign |
| Focus spot (concentric sinc(κθ), κ = 15–90, 1818 centres) | SMICA 2°, common mask, 300 sims | a significant spot | max z = 4.26 (κ = 40, (321°, −33°)); global p = 0.13 | none |
| Single tone (line in P(k)) | Planck 2018 TT ℓ=2–2500 | — | Δχ² = +2.98×10⁵ (w=0.02) … +276 (w=3) | fail |
| BAO tone | same | — | +4.86×10⁵ (2π/r_d), +5.33×10⁵ (π/r_d) | fail |
| Harmonic comb n·k₀ | same | — | allowed only if k₀ ≲ 7.7×10⁻⁴ Mpc⁻¹ with 35% widths (effectively continuous) | fail as a tone |
| Bump on ΛCDM | same | — | max local Δχ² = 3.0; 95% B: w=0.3 1.0–36% (median 3.8%), w=0.1 median 5.8%, w=0.03 median 15% | no feature |
| Sweep families | Planck 2018 X n_s = 0.9649 ± 0.0042, dn_s/dlnk = −0.0045 ± 0.0067 | n_s | linear 2.0; t² 1.5; exp 1.000; exp with 3.5%/e-fold drift 0.965 (α = 0) | first two fail; exp passes (= inflation) |
| Speech spectrum as P(k) | Planck TT | — | best Δχ² = +1.99×10⁵ | fail |
| Speech envelope along ln k | Planck TT | — | −8.4 (Gaussian, p_glob 0.016) → −4.3 (exact low-ℓ, f_sky = 0.86, p_glob = 0.16) | inconclusive / not significant |
| CCC rings (Planck) | SMICA 1°, common mask, 200 sims | excess | 697 low rings, 19 families ≥3, 1 ≥5, z_min −2.88; ΛCDM sims p_ge = 0.96 / 0.985 / 0.87 / 0.42; observed-low-ℓ sims p_ge = 0.75 / 0.92 / 0.72 / 0.31 | no excess |
| Hawking-like 4° discs | same | excess | 3 vs 8.9 expected, p_ge = 0.91 (observed-low-ℓ sims: 6 vs 8.9, p = 0.70) | none |

## 3. Caveats

- **Toy model:** a static Helmholtz cavity is not a cosmology. No expansion, no plasma transfer function and no ISW are included. The mapping from Φ to ΔT is assumed.
- **Low-ℓ statistics:**
  - full-sky inpainted maps (standard for ℓ ≤ 10);
  - an axis grid at nside 16 (≈ 3.7°), used identically for data and sims;
  - the sims use Planck best-fit C_ℓ (the statistics are normalized per ℓ);
  - the quad–oct and parity p-values are *a posteriori*, as in the literature.
- **Parity sims:** full-sky χ²_{2ℓ+1}. The real cut sky has slightly more variance, so the p-values here are slightly optimistic.
- **TT likelihood:** diagonal Gaussian with symmetric errors, nuisance amplitude + tilt only, fixed Planck 2018 cosmology, and lensing via the fiducial C_L^φφ (as in doc 71). The k grid dq = 6.6×10⁻⁵ Mpc⁻¹ limits the narrowest lines (w_eff ≥ 3dq/k₀).
- **Speech:** a *parametric* model of a male voice saying "let there be light" (four syllables, F0 85–152 Hz, formants of /ɛ/, /i/, /aɪ/). It is not a recording. The mapping from time to ln k and the placement were scanned (look-elsewhere included).
- **Rings / Hawking points:** these are our simplified statistics, not the Gurzadyan–Penrose or An–Meissner–Nurowski–Penrose pipelines.

## 4. Sources

- Planck PR3 SMICA map `COM_CMB_IQU-smica_2048_R3.00_full.fits` and common mask `COM_Mask_CMB-common-Mask-Int_2048_R3.00.fits` (IRSA/PLA mirror).
- Planck 2018 TT spectrum and best-fit theory (PLA R3.01, as in docs 65/66/71).
- WMAP 9 ILC (LAMBDA).
- Planck 2018 X (arXiv:1807.06211): n_s, running, features.
- Planck 2018 VI (arXiv:1807.06209): r_d; our CAMB value is 147.06 Mpc, r_* = 144.40 Mpc.
- Planck 2018 VII (arXiv:1906.02552) and Planck 2015 XVI (arXiv:1506.07135): anomalies.
- de Oliveira-Costa et al. PRD 69 063516 (2004); Copi, Huterer, Schwarz & Starkman, review arXiv:1510.07929.
- Land & Magueijo PRD 72 101302 (2005); Kim & Naselsky ApJ 714 L265 (2010): parity.
- Planck 2015 XVIII (arXiv:1502.01593): topology / matched circles.

## 5. Reproduce

```
cd experiments/time_medium_sound
# data/: smica.fits and mask.fits from
#  https://irsa.ipac.caltech.edu/data/Planck/release_3/all-sky-maps/maps/component-maps/cmb/COM_CMB_IQU-smica_2048_R3.00_full.fits
#  https://irsa.ipac.caltech.edu/data/Planck/release_3/ancillary-data/masks/COM_Mask_CMB-common-Mask-Int_2048_R3.00.fits
python report_74.py toy tones chirp chirp_lee chirp_lee_exact
DOC74_OUT=results_maps.json python report_74.py lowell focus rings rings_obs
```
