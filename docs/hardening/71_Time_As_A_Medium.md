# 71. Time as a medium with reflecting "banks": tests against real data

**Date:** 24 November 2026 (America/Chicago)
**Status:** exploratory tests of a physical picture. The **Dual-Zero regulator is untouched**, and so are the top and Higgs results (docs 58–70).
**Idea (Shawn, 24 Nov):** time is an actual medium we are immersed in (something can exist outside it), like pond water. The ripples of creation travel out to the "banks" of time and reflect back. This builds on the ripple and bounded-pond work in docs 65/66.
**Code** (`experiments/time_medium/`):
- `time_medium.py`: likelihood, fast C_ℓ responses, ring statistic, echo delay, dispersion, future fate and α bounds;
- `report_71.py`: writes `results_doc71.json`, run as `cmb`, `rings`, `analytic` or `--figure`;
- `report_71_fig.py`: the figure.

**Figure:** `docs/hardening/figures/71_time_medium.png`.
**Tests:** `tests/test_time_medium.py` (6 tests).

---

## Plain-language summary (for Shawn)

The picture can be turned into six testable claims. **None of them shows a signal, and none of them changes Dual-Zero or the masses.**

1. **A reflecting bank in the early universe would leave an echo (a ripple pattern) in the CMB spectrum.**
   - We searched the Planck temperature spectrum for both kinds of echo.
   - The best echoes improve the fit by Δχ² = 5.9 and 8.6. Random no-echo skies do as well or better **98% and 59%** of the time.
   - So there is no echo. Our search finds the same "best" log-echo bump as Planck's own analysis (ω ≈ 32, Δχ² ≈ 8.3 vs Planck's 8.5), and Planck also judged it a chance fluctuation.
   - The echo strength must be below about 1.2–1.3% of the spectrum, which means the bank reflects less than about 0.6% of the ripple.
2. **Penrose-style concentric low-variance rings / "Hawking points".**
   - On the WMAP 9-year map, our simple ring count lies inside the range of ordinary random skies (p between 0.2 and 0.8).
   - The published follow-ups say the same about the original claims.
3. **Gravitational-wave echoes from a "bank" just outside black holes.**
   - We reproduce the predicted echo delay (0.29 s for GW150914).
   - The published LIGO/Virgo searches find no echoes, and the original 2.5σ hint fell to about 2σ or less on re-analysis.
   - **Excluded as a detected effect.** It is not ruled out at small reflection strength.
4. **Time as a dispersive medium (speed depends on frequency or energy).**
   - Gravity and light arrive together to 1 part in 10¹⁵ (GW170817).
   - Gamma rays of very different energies arrive together to 1 part in 10¹⁹ (GRB 090510).
   - Any "refractive index" of time that depends on energy must be smaller than this. A dispersive medium at a natural (Planck) strength is **excluded**.
5. **A bank in the future (a finite end of time).**
   - With standard data the universe expands forever.
   - An end ("crunch") needs both slightly closed space *and* DESI-style weakening dark energy pushed far beyond the data (about 84,000 Gyr from now).
   - A reflection from the future would also run backwards in cause and effect. **Untestable.**
6. **A refractive index of time that changes with epoch (the outlier test).**
   - If it changed the strength of electromagnetism, atomic clocks, the Oklo natural reactor and quasar spectra would see it.
   - They bound the drift to |ε| ≲ 3×10⁻⁸ (clocks).
   - If it is the same for everything, it is just a choice of clock units and cannot be measured even in principle.
   - **Excluded** (for α-changing versions) / **untestable** (for the universal version).

**Dual-Zero, top and Higgs:** unchanged.
- The top/Higgs predictions come from the a₄ term of the spectral action at the scale Λ plus ordinary running (docs 58–70).
- A medium for time changes neither the finite spectral triple nor the beta functions.
- Every version that would have shifted particle physics (an α drift) is bounded at the 10⁻⁸ level.

---

## 1. Formulations

| # | Version of "time is a medium with banks" | Observable | Model |
|---|---|---|---|
| 1a | Mirror at a past conformal time τ_b | primordial P(k) | P0[1 + A cos(ω k/k* + φ)], ω = 2k*τ_b, A ≈ 2\|r\| |
| 1b | Mirror at a fixed physical energy (a "new-physics hypersurface") | primordial P(k) | P0[1 + A cos(ω ln(k/k*) + φ)] |
| 2 | Previous-aeon / bank collisions (CCC) | concentric low-variance rings | ring σ statistic |
| 3 | Planck-length "bank" near horizons | GW echoes | Abedi–Dykaar–Afshordi delay |
| 4 | Dispersive medium | arrival-time differences | Δv/c = ½(m_g c²/hf)², \|n−1\| = E/E_QG |
| 5 | Future / finite bank | fate of a(t) | Friedmann + CPL w(a), Ω_k |
| 6 | Epoch-dependent index | α(z) | Δα/α = ε ln(1+z) |

k* = 0.05 Mpc⁻¹, using the Planck 2018 X convention (arXiv:1807.06211).

## 2. Results and verdicts

| Test | Data / source | Our number | Verdict |
|---|---|---|---|
| 1a linear echo | Planck 2018 unbinned TT, ℓ=2–2500 | best Δχ² = 5.9 at ω = 11.95 (τ_b ≈ 120 Mpc); p_local = 0.052, **p_global = 0.98** (2000 sims; the 95% best-of-scan level is 15.4); typical 95% upper A ≈ 0.012 | **Excluded** as a detectable feature (A ≲ 1.2%, \|r\| ≲ 0.6%) |
| 1b log echo | same | best Δχ² = 8.6 at ω = 1.0 (grid edge; a slow modulation degenerate with running); the best at ω ≥ 3 is 8.3 at ω = 31.9 (log10 ω = 1.50); **p_global = 0.59** (95% level 14.9); typical 95% upper A ≈ 0.013 | **Excluded** as a detection. Planck 2018 X TT: −8.5 at log10 ω = 1.51, "consistent with the null" |
| 2 CCC rings | WMAP 9-yr ILC, KQ85 mask, 2231 centres, radii 2.5–19.5° | data: 747 low rings, 33 centres with ≥ 3, 1 with ≥ 5, z_min = −2.78. ΛCDM sims (200): p_ge = 0.76, 0.80, 0.78; z_min p_le = 0.78. Observed-low-ℓ sims: p = 0.52, 0.59, 0.74 | **Survives only as "nothing unusual"**: no excess. Literature: Gurzadyan–Penrose arXiv:1011.3706 vs Moss–Scott–Zibin JCAP 04 (2011) 033, Wehus–Eriksen ApJ 733 L29, Hajian ApJ 740 52. Hawking points: An et al. 1808.01740 (99.98%) vs Jow–Scott JCAP 03 (2020) 021 (87%) |
| 3 GW echoes | ADA PRD 96 082004 (arXiv:1612.00266); Westerweck et al. PRD 97 124037; Nielsen et al. PRD 99 104012; LVK GWTC-2 PRD 103 122002; GWTC-3 tests arXiv:2112.06861 | Δt: GW150914 0.2917 s (ADA 0.2956), GW151226 0.1010 (0.1025), LVT151012 0.1773 (0.1796), agreeing within 1.3%; GW190521 ≈ 1.16 s | **Excluded as a detection** (no echoes in GWTC-2/3; ADA's p = 0.011 became 0.032). Weak reflection is untestable for now |
| 4 dispersion | GW170817/GRB170817A ApJL 848 L13; Vasileiou et al. PRD 87 122001; LHAASO arXiv:2402.06009; GWTC-3 m_g ≤ 2.42×10⁻²³ eV/c² (90%, arXiv:2112.06861) | −3×10⁻¹⁵ < Δv/c < 7×10⁻¹⁶; \|n−1\| < 3.3×10⁻¹⁹ at 31 GeV (E_QG,1 > 7.6 E_Pl); < 8.2×10⁻¹⁷ at 10 TeV (> 10 E_Pl); Δv/c ≤ 1.7×10⁻²¹ at 100 Hz | **Excluded** at linear Planck-scale strength |
| 5 future bank | Planck 2018 Ω_k = 0.0007 ± 0.0019 (+BAO); DESI DR2 w0 = −0.752, wa = −0.86 (arXiv:2503.14738) | ΛCDM (flat or Ω_k = −0.0031): expands forever. DESI CPL flat: undetermined. DESI CPL + Ω_k = −0.0031: crunch at ≈ 8.4×10⁴ Gyr, a_max ≈ 103 (an extrapolation) | **Untestable** (acausal; needs extrapolation) |
| 6 α drift | Lange et al. PRL 126 011102; Damour–Dyson NPB 480 37; Murphy et al. A&A 658 A123; Planck int. XXIV A&A 580 A22 | ε: clocks −1.45e-8 ± 1.6e-8; Oklo 1.0e-7 ± 3.6e-7; quasars −6.0e-7 ± 7.7e-7; CMB 5.1e-4 ± 5.3e-4 | **Excluded** above ~3×10⁻⁸; the universal version is **untestable** |

**Best-fit significance in plain words:** the best echo in the CMB has a local significance of about 1.9σ (linear) and 2.5σ (log, p_local = 0.014). After counting how many frequencies we tried, the chance of doing at least that well by luck is 98% and 59%. **That is zero sigma of evidence.**

## 3. Dual-Zero / top / Higgs

- No version touches the finite spectral triple, the Dual-Zero regulator, the a₄ boundary conditions at Λ, or the RG running.
- The predictions M_t and M_h (docs 58–70) are unchanged.
- The only route by which a time medium could reach particle physics is a drifting α (or μ). That route is bounded at |ε| ≲ 3×10⁻⁸ (test 6), and as in doc 65 it has no visible effect on masses.

## 4. Caveats

- **CMB:** diagonal Gaussian TT likelihood with symmetric errors, fixed Planck 2018 cosmology (only the amplitude and tilt responses are marginalized), TT only (no TE/EE).
  - The fast C_ℓ responses (transfer × P(k)) agree with full CAMB to 0.14% at ω = 10 and 0.02% at ω = 126.
  - The look-elsewhere calibration uses Gaussian sims of the same likelihood. Our linear-echo Δχ² at Planck's best frequency (log10 ω = 1.74) is 2.7, compared with Planck's 4.2. This is expected from the simpler likelihood.
- **Rings:** this is a simple statistic on the WMAP ILC (nside 128, 1° rings, 15 μK drop), not a reproduction of the Gurzadyan–Penrose pipeline. There are 200 sims per set.
- **Echo delay:** this is our implementation of ADA eqs. (2)–(5), within 1.3% of their table.
- **Future fate:** the CPL form w(a) is extrapolated far outside the data.
- **α:** the bounds assume the parametrization ε ln(1+z).

## 5. Reproduce

```
pip install -r requirements-doc71.txt        # camb, healpy
experiments/time_medium/data/fetch.sh        # WMAP 9-yr ILC + KQ85 mask from NASA LAMBDA
python experiments/time_medium/report_71.py analytic
python experiments/time_medium/report_71.py cmb      # builds templates_doc71.npz (cache), scan + 2000 sims
python experiments/time_medium/report_71.py rings    # 2 × 200 synfast sims
python experiments/time_medium/report_71.py --figure
```

Data URLs:
- https://lambda.gsfc.nasa.gov/data/map/dr5/dfp/ilc/wmap_ilc_9yr_v5.fits
- https://lambda.gsfc.nasa.gov/data/map/dr5/ancillary/masks/wmap_temperature_kq85_analysis_mask_r9_9yr_v5.fits
- The Planck 2018 TT spectrum comes from the Planck Legacy Archive (the same file as in docs 65/66).
