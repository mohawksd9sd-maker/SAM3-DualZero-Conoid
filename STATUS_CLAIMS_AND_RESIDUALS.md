# SAM3 — Claims vs Residuals (SINGLE SOURCE OF TRUTH)

**Date:** August 2026  
**Role:** Executive claim map. If any paper or note conflicts with this file, **this file wins**.  
**Rule:** Derivation only, no experimental tuning, no overclaim.

### Authority index

| Topic | File |
|-------|------|
| Metric / $f$ / ω₀ | [`docs/hardening/35_Metric_Curvature_Omega0_Authoritative.md`](docs/hardening/35_Metric_Curvature_Omega0_Authoritative.md) — **$f=\sqrt{u^2+4\ell_0^2\cos^2(2v)}$ only** |
| Dual-Zero definition | [`docs/hardening/18_DualZero_Definition_Lock.md`](docs/hardening/18_DualZero_Definition_Lock.md) |
| Constructive Dual-Zero + schemes | [`docs/hardening/39_DualZero_Constructive_and_Scheme_Comparison.md`](docs/hardening/39_DualZero_Constructive_and_Scheme_Comparison.md) |
| Production numbers | [`docs/hardening/36_Production_Numerical_Archive.md`](docs/hardening/36_Production_Numerical_Archive.md) |
| Pipeline maturity | [`docs/hardening/40_Numerical_Pipeline_Maturity.md`](docs/hardening/40_Numerical_Pipeline_Maturity.md) |
| Regulator comparison | [`docs/hardening/37_Regulator_Comparison_DZ_vs_HeatKernel_Zeta.md`](docs/hardening/37_Regulator_Comparison_DZ_vs_HeatKernel_Zeta.md) |
| Unification / cosmology residuals | [`docs/hardening/41_Unification_Cosmology_Residuals.md`](docs/hardening/41_Unification_Cosmology_Residuals.md) |
| Lepton confrontation | [`docs/hardening/38_Lepton_Predictions_Oscillation_0nubb.md`](docs/hardening/38_Lepton_Predictions_Oscillation_0nubb.md) |
| Papers supersession | [`papers/SUPERSESSION.md`](papers/SUPERSESSION.md) |

---

## 1. High-confidence geometric results (locked)

| Result | Confidence |
|--------|------------|
| Metric $f=\sqrt{u^2+4\ell_0^2\cos^2(2v)}$ (not $16\ell_0^2$) | **Locked convention** |
| Dual-Zero $\varepsilon(n)=\omega_0(-1)^n n^{-n}$, $\omega_0\approx 0.927$ | High |
| Constructive finite-$N$ Dual-Zero for numerics (no ultrafilter required) | **Locked policy** |
| Exactly 3 chiral generations (APS) | High |
| $\eta_{12}\approx 0.861$, $\eta_{13}\approx 0.544$, $\eta_{23}\approx 0.479$ | High |
| $\theta_{12}\approx 12.85^\circ$, $\theta_{23}\approx 2.36^\circ$ | Locked |
| $\phi=+2\pi/5$, $\delta_{\rm CKM}\sim 70^\circ$ | Locked |
| $G_N=64\pi\ell_0^2/45$ | Locked |
| $m_H$ **class** 124–127 GeV (not digit 125.1) | Locked class |
| Large $\delta_{\rm PMNS}$ band $200^\circ$–$270^\circ$ | Locked band |

---

## 2. Residuals (honest)

| Item | Status |
|------|--------|
| Production 2D APS eigensolver | **Prototype** (continuum residual $<10^{-3}$ stage-OK) |
| Gauge unification baseline | **~$7\%$ floor**; percent-level not claimed |
| VL_Q research path | ~$2.6\%$ two-loop; $M_X\neq\mu_{\rm meet}$ |
| Cosmological constant magnitude | **Open** (mechanism present) |
| Digit PMNS / $m_{\beta\beta}$ | Bands only; NH preferred |
| **Riemann Hypothesis** | **Variational proposal only — NOT a proof** |

---

## 3. Riemann Hypothesis discipline (mandatory)

- STATUS and hardening demote RH to a **variational / information-current proposal**.
- Older `papers/` language that states or implies a completed proof is **superseded** and must not be restored.
- Spectral zeta of $D$ is not a proof of the classical RH.

---

## 4. Metric discipline (mandatory)

- Only $4\ell_0^2$ tip coefficient is allowed in active claims.
- $16\ell_0^2$ forms are historical/superseded (equivalent to an illegal $\ell_0$ redefinition after $G_N$ lock).

---

## 5. Supersession

`papers/` is historical. Conflicting digit $m_H$, percent-level unification-as-fact, RH-as-proof, or $16\ell_0^2$ metric claims yield to this STATUS file.

---

*SSOT — derivation only, no tuning, no overclaim.*
