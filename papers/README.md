# SAM3 Papers

**Important — August 2026 hardening supersession**

The LaTeX sources in this directory are the May 2026 paper series (Flagship, v4.19–v4.22, Papers 02–23, addenda, etc.).

Where those papers conflict with the **August 2026 hardening layer**, the hardening layer is authoritative.

## Authoritative status (read these first)

| Document | Role |
|----------|------|
| [`../STATUS_CLAIMS_AND_RESIDUALS.md`](../STATUS_CLAIMS_AND_RESIDUALS.md) | Executive map of locked vs residual claims |
| [`../docs/hardening/00_INDEX.md`](../docs/hardening/00_INDEX.md) | Full lock notes (Priorities 1–6 + secondary 1–3) |
| [`../docs/hardening/16_Frozen_Numerical_Archive.md`](../docs/hardening/16_Frozen_Numerical_Archive.md) | Frozen geometric numbers |
| [`../README.md`](../README.md) | Public summary aligned with hardening |

**Rule in force:** derivation only, no experimental tuning, no overclaim.

---

## Claims that are superseded if they appear in these papers

| Older paper language | Hardened replacement |
|----------------------|----------------------|
| Higgs mass exactly **125.1 GeV** (digit-level match) | **125 GeV class** (approx. 124–127 GeV theoretical band); not digit-tuned |
| Gauge unification near **10^{15.8} GeV** as a successful percent-level result | KK thresholds of order \(O(10)\); residual relative mismatch **~7%**; **percent-level unification is not claimed** |
| CKM / PMNS “deviations < 0.3%” or perfect table matches | Locked geometric angles/phase with stated residuals; precision limited by residual \(\theta_{13}\) and related uncertainties |
| Riemann Hypothesis **proved** or “enforced if and only if” as a finished theorem | **Variational / information-current proposal only** — not a proof of RH |
| Cosmological constant magnitude fully locked to observation | **Mechanism present**; magnitude lock remains residual |
| Continuum Dirac residual left as large prototype values without update | Residual **< 10^{-3}** locked under 4th-order FD + APS gap \(\to 0\) |
| \(\theta_{23}\) or \(\delta_{\rm CKM}\) left as open free structure | \(\theta_{23}\approx 2.36^\circ\) and \(\phi=2\pi/5\) **locked** from geometry / representation theory |
| Light up-quark factor ~2 left unresolved | Resolved by intertwiner norm \(\kappa_u/\kappa_d=1/2\) |

---

## What remains valid in these papers

- Right-conoid geometry and 12-bridge / 2I structure
- Dual-Zero regulator form and geometric derivation of \(\omega_0\)
- Seeley–DeWitt route to the \(G_N = 64\pi\ell_0^2/45\) structure
- Three-generation index / representation motivation
- Product construction and spectral-action architecture
- Paper 11’s **careful** statement that the RH connection is not a proof of the classical Riemann Hypothesis (prefer that wording over stronger RH papers)

---

## Recommended reading order for new readers

1. Repository [`README.md`](../README.md)
2. [`STATUS_CLAIMS_AND_RESIDUALS.md`](../STATUS_CLAIMS_AND_RESIDUALS.md)
3. [`docs/hardening/`](../docs/hardening/00_INDEX.md) lock notes of interest
4. Individual papers in this folder **as historical / technical development**, not as the final claim surface

---

## Cabibbo / defect addendum

[`SAM3_Addendum_Cabibbo_Defect_Operator.tex`](SAM3_Addendum_Cabibbo_Defect_Operator.tex) is aligned with the hardening layer on the continuum defect and Cabibbo derivation. For \(\theta_{23}\) and the CP phase, see also:

- `docs/hardening/07_Geometric_Theta23_Casimir.md`
- `docs/hardening/08_Geometric_CKM_Phase.md`
- `docs/hardening/11_Explicit_DF_and_CKM.md`

---

*This notice was added as Fix 3 of the August 2026 repository consistency pass.*
