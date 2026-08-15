# 37 — Regulator Comparison Tables (Dual-Zero vs Heat-Kernel / Zeta)

**Status:** Explicit scheme tables for key observables  
**Date:** August 2026  
**Canonical Dual-Zero:** docs 18, 35, 39

---

## Table A — What each scheme is

| Scheme | Definition | Constructive production use |
|--------|------------|-----------------------------|
| **Dual-Zero** | $\varepsilon(n)=\omega_0(-1)^n n^{-n}$, Reg₂ | Finite-$N$ weights; no ultrafilter required (doc 39) |
| **Heat kernel** | $\mathrm{Tr}\,e^{-tD^2}$; Seeley $a_{2k}$ | $G_N$, $m_H$ class, continuum $\eta$ |
| **Zeta** | $\zeta_D(s)=\mathrm{Tr}\lvert D\rvert^{-s}$ | Equivalent spectral language to heat kernel |
| Hard cutoff | $\theta(\Lambda-\lvert\lambda\rvert)$ | Benchmark only; not Dual-Zero philosophy |

---

## Table B — Key observables (scheme roles)

| Observable | Primary scheme | Dual-Zero role | Zeta role | Locked claim level |
|------------|----------------|----------------|-----------|--------------------|
| **$G_N$** | Heat kernel $a_2$ | Subleading mode weights only | Same $a_2$ physics if same metric | Formula $64\pi\ell_0^2/45$ |
| **$m_H$** | Heat kernel $a_4$ | UV silence; **not** digit tuner | Same class | 125 GeV **class** |
| **3 generations** | APS continuum spectrum | Not the carrier of the count | N/A | Locked schema |
| **$\eta_{ij}$** | Continuum heat-kernel / defect | Optional shifts; $\omega_0$ fixed | Optional packaging | Archive centrals ± band |
| **Yukawa hierarchy** | Tip Casimir + geometry | Super-exponential UV weights | Spectral sums must agree on standard parts | Ratio class locked |
| **Unification residual** | β-functions + thresholds | Reweight only; no miracle | N/A | ~$7\%$ floor baseline |
| **RH language** | — | Motivates information-current **proposal** | Spectral zeta ≠ classical RH proof | **Not a proof** |

---

## Table C — Scheme independence policy

| Allowed | Forbidden |
|---------|-----------|
| Heat kernel ↔ zeta agreement on locked **classes** | Retuning $\omega_0$ to absorb scheme mismatch |
| Finite-$N$ Dual-Zero for numerics | Requiring non-constructive ultrafilters in production |
| Stating O(few %) scheme uncertainty on $G_N$ interpretation | Digit $m_H=125.1$ from any single scheme |
| Keeping unification / RH secondary | Claiming percent-level unification from Dual-Zero alone |

---

## Table D — Numerical probe (constructive Dual-Zero)

Run `python code/dual_zero_constructive.py`:

| Check | Expected |
|-------|----------|
| $\lvert\varepsilon(n)\rvert$ decay | Super-exponential; negligible by $n\sim 20$ |
| Reg₂ pairing | Well-defined finite list |
| $\omega_0\pm 0.005$ | Weight sums move slightly; angles **not** retuned |

---

*Explicit scheme-comparison tables — August 2026.*
