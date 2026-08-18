# Full repository audit — findings and fixes

**Date:** August 18, 2026  
**Scope:** Full SAM3-DualZero-Conoid tree (~190 files)  
**Constraint:** Fix errors/contradictions/overclaims **without** destroying the math model or Dual-Zero novelty

---

## Findings

### A. Live metric coefficient errors (fixed this pass)

| Location | Problem | Fix |
|----------|---------|-----|
| `docs/hardening/09_Casimir_Potentials_from_Geometry.md` | $16\ell_0^2$ | → **4** |
| `docs/hardening/20_Seeley_DeWitt_Expanded_Derivation.md` | $16\ell_0^2$ and $R$ with 32 | → **4** |
| `code/verification/dirac_conoid_verification.py` | `16 * L0**2` | → **4** |
| `code/lorentzian_spectral_action.py` | docstring $16\ell_0^2$ / $R$ 32 | → **4** |
| `docs/math_notes/16_...` $16\ell_0^2\varepsilon^2$ | Apparent conflict | **Kept** — local tip chart consistent with global 4 when $\cos(2v)\approx 2\varepsilon$; clarified |

### B. Root foundations file

| Location | Problem | Fix |
|----------|---------|-----|
| `SAM3_DualZero_Conoid_Core_Definitions.tex` | “Complete foundations” tone, no STATUS pointer | Supersession banner; Dual-Zero content **preserved** |

### C. Unification over-read

| Location | Problem | Fix |
|----------|---------|-----|
| `docs/hardening/33_Unification_VLQ_Precision_Path.md` | ~1.9% readable as locked | Banner: **research path only**; locked floor remains ~7% |

### D. Dual-Zero (preserved)

| Item | Status |
|------|--------|
| Original Dual-Zero novelty | **Preserved** — doc 18 canonical |
| $\varepsilon(n)=\omega_0(-1)^n n^{-n}$ | Locked |
| $\operatorname{Reg}_2$ | Locked |
| Geometric $\omega_0$ | Locked form |
| Not $\mathrm{st}(\varepsilon)\neq 0$ | Correct |

### E. Earlier fixes (verified still hold)

Papers metric stubs · $A_5$ isometry rejection · RH proposal-only · core modest paper

### F. Honest residuals (not fake-closed)

| Item | Why |
|------|-----|
| $\omega_0$ exponent $4/13$ | Packaging incomplete |
| $G_N$ pure prefactor scheme | $\propto\ell_0^2$ locked; digit convention |
| L4 edge-calculus citation | External theory |
| Yukawa digit hierarchy | Incomplete (known) |

---

## Authority order

1. `STATUS_CLAIMS_AND_RESIDUALS.md`  
2. `docs/hardening/18_DualZero_Definition_Lock.md`  
3. `docs/hardening/35_Metric_Curvature_Omega0_Authoritative.md`  
4. `docs/math_notes/`  
5. `papers/SAM3_Core_Geometry_and_Spectral_Results.tex`  

---

*Full repo audit August 18, 2026.*
