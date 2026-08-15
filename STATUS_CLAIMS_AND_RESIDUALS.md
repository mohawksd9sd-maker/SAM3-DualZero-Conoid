# SAM3 — Claims vs Residuals (SINGLE SOURCE OF TRUTH)

**Date:** August 2026  
**Role:** Executive claim map. If any paper or note conflicts with this file, **this file wins**.  
**Rule:** Derivation only, no experimental tuning, no overclaim.

**Detail locks:** [`docs/hardening/`](docs/hardening/00_INDEX.md)  
**Metric / ω₀ authority:** [`docs/hardening/35_Metric_Curvature_Omega0_Authoritative.md`](docs/hardening/35_Metric_Curvature_Omega0_Authoritative.md)  
**Dual-Zero authority:** [`docs/hardening/18_DualZero_Definition_Lock.md`](docs/hardening/18_DualZero_Definition_Lock.md)  
**Production numbers:** [`docs/hardening/36_Production_Numerical_Archive.md`](docs/hardening/36_Production_Numerical_Archive.md)  
**Regulator comparison:** [`docs/hardening/37_Regulator_Comparison_DZ_vs_HeatKernel_Zeta.md`](docs/hardening/37_Regulator_Comparison_DZ_vs_HeatKernel_Zeta.md)  
**Lepton confrontation:** [`docs/hardening/38_Lepton_Predictions_Oscillation_0nubb.md`](docs/hardening/38_Lepton_Predictions_Oscillation_0nubb.md)

---

## 1. High-confidence geometric results (locked)

| Result | Origin | Confidence |
|--------|--------|------------|
| Dual-Zero $\varepsilon(n)=\omega_0(-1)^n n^{-n}$ | Analytic + information conservation | High |
| Geometric $\omega_0=(R_{\rm curv}/D_{\rm bridge})^{4/13}\approx 0.927$ | Doc 35 + 18 | High |
| Exactly three chiral generations | Index + continuum gap $\to 0$ under APS | High |
| Continuum defect $\eta_{12}\approx 0.861$, $\eta_{13}\approx 0.544$, $\eta_{23}\approx 0.479$ | Docs 32, 36 | High |
| Cabibbo $\theta_{12}\approx 12.85^\circ$ | $\eta_{12}\times\pi/12$ + $\mathcal{A}_F$ | High |
| CKM $\theta_{23}\approx 2.36^\circ$ | Casimir-weighted defect | **Locked** |
| CP phase $\phi=+2\pi/5$ | $E_3$ + $I^2=-1$ + tip orientation | **Locked** |
| $\delta_{\rm CKM}\sim 70^\circ$, $J\sim 3\times 10^{-5}$ | $\phi$ + locked angles | **Locked** (consistency) |
| $C_g=(6/5,1,4/5)$ | 2I-module | **Locked** |
| Continuum Dirac residual $<10^{-3}$ | 4th-order FD + APS | **Locked** |
| $\kappa_u/\kappa_d=1/2$ | Intertwiner norm | **Locked** |
| $G_N=64\pi\ell_0^2/45$ | Seeley $a_2$ | **Locked** |
| Higgs mass 125 GeV **class** ($\approx 124$–$127$ GeV) | Geometric $a_4$ | **Locked class** |
| Large $\delta_{\rm PMNS}$ ($\sim 200^\circ$–$270^\circ$ band) | Module-wide $\phi$ | **Locked band** |

---

## 2. Residual / approximate (not overclaimed)

| Item | Status | Open |
|------|--------|------|
| Sub-degree $\delta_{\rm CKM}$ / percent-level $J$ | Consistent at present precision | $\theta_{13}$ residual |
| Sub-GeV Higgs digit | Class only | Warped $a_4$ + matching |
| Gauge unification | Geometric floor **~$7\%$**; VL_Q research path ~$2.6\%$ (docs 33–34) | Percent-level **not** claimed as baseline |
| $M_X=\mu_{\rm meet}$ | **Not derived** | AF′ layer uses projective break; $M_X=\Lambda_0$ if vectors exist |
| Cosmological constant magnitude | Mechanism present | Magnitude lock |
| Sharp $\delta_{\rm PMNS}$, digit $m_{\beta\beta}$ | Bands only (doc 38) | RH hierarchy + Majorana phases |
| Riemann Hypothesis | Variational proposal | **Not a proof** |
| Lorentzian full causality theorem | Wick + KO recovery | Full reconstruction residual |

---

## 3. Unification (disciplined)

- Baseline geometric KK floor: **~$7\%$** (no percent-level claim).
- Research path (doc 33): VL_Q at $M_*=\sqrt{\Lambda_0 m_H}$ and $12M_*$ → two-loop residual **~$2.6\%$**.
- $M_X=\mu_{\rm meet}$ is **not** a SAM3 eigenvalue; forced UV vector scale is $\Lambda_0$ under projective AF′ reading (doc 34).

---

## 4. Lepton confrontation (doc 38)

- $\delta_{\rm PMNS}$ large ($200^\circ$–$270^\circ$): falsifiable if data demand CP conservation.
- Prefer normal hierarchy from tip weights; $m_{\beta\beta}$ few–$O(10)$ meV class under NH — **not** a digit claim.
- Inverted hierarchy would pressure tip-ordering assumptions.

---

## 5. What the model is (and is not)

**Is:** Geometric research program for SM architecture + quantitative flavor (Cabibbo, $\theta_{23}$, CP structure) from conoid + Dual-Zero + $\mathcal{A}_F$.

**Is not (yet):** Finished percent-level TOE; RH proof; free of all residuals.

---

## 6. Supersession (mandatory)

Older statements in `papers/` claiming exact $m_H=125.1$ GeV, percent-level unification as baseline, RH-as-proof, or $M_X=\mu_{\rm meet}$ as derived are **superseded** by this file and `docs/hardening/`.

See [`papers/SUPERSESSION.md`](papers/SUPERSESSION.md).

---

## 7. Hardening path status

| Block | Status |
|-------|--------|
| Priorities 1–6 + secondary 1–3 | Complete |
| Docs 28–32 precision / $\eta$ | Complete |
| Docs 33–34 unification / AF′ | Research layer complete |
| Docs 35–38 authority / archive / regulators / leptons | Complete (this update) |

---

*SSOT — derivation only, no tuning, no overclaim.*
