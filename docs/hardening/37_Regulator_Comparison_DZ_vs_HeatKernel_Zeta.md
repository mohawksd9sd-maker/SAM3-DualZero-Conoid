# 37 — Regulator Comparison: Dual-Zero vs Heat-Kernel / Zeta

**Status:** Side-by-side comparison for key observables  
**Date:** August 2026  
**Canonical Dual-Zero:** docs 18 + 35

---

## 1. What each regulator is

| Regulator | Definition (schematic) | Role in SAM3 |
|-----------|------------------------|--------------|
| **Dual-Zero** | $\varepsilon(n)=\omega_0(-1)^n n^{-n}$, $\operatorname{Reg}_2$ | UV / information-conserving spectral regulator |
| **Heat kernel** | $\mathrm{Tr}\,e^{-tD^2}$; Seeley–DeWitt $a_{2k}$ | Spectral action, $G_N$, Higgs class, continuum $\eta$ law |
| **Zeta** | $\zeta_D(s)=\mathrm{Tr}\,|D|^{-s}$; analytic continuation | Spectral asymptotics; optional alternative to heat kernel |

They are **not** interchangeable slogans: Dual-Zero regulates the discrete/infinite mode sum; heat kernel / zeta implement the spectral action and continuum geometric densities.

---

## 2. Observable-by-observable

### 2.1 Newton constant $G_N$

| Method | Result | Status |
|--------|--------|--------|
| Heat kernel / Seeley $a_2$ | $G_N=64\pi\ell_0^2/45$ | **Locked** |
| Zeta (related Seeley) | Same leading $a_2$ physics | Consistent if same metric |
| Dual-Zero alone | Does **not** replace $a_2$ | DZ enters mode weights, not the Einstein term by itself |

### 2.2 Higgs mass class

| Method | Result | Status |
|--------|--------|--------|
| Heat kernel $a_4$ | 125 GeV **class** (124–127 GeV band) | Locked class |
| Dual-Zero | Suppresses / weights UV; **not** digit tuner | Must not be fit to 125.1 GeV |
| Zeta | Equivalent spectral data with different presentation | No extra digit claim |

### 2.3 Continuum defect overlaps $\eta_{ij}$

| Method | Result | Status |
|--------|--------|--------|
| Heat-kernel tip split (doc 32) | Law with mix $\tfrac12-\cos(2\pi/5)$; RMS $\approx 0.008$ vs locked | Breakthrough path |
| Direct continuum defect integrals | $\eta_{12}\approx 0.861$, $\eta_{13}\approx 0.544$, $\eta_{23}\approx 0.479$ | Locked archive |
| Dual-Zero | Optional eigenvalue shifts; must not retune $\omega_0$ to force $\eta$ | Discipline |

### 2.4 Yukawa hierarchy / radial weights

| Method | Result | Status |
|--------|--------|--------|
| Casimir tip potential + geometry | $C_g$, tip amplitudes | Locked |
| Dual-Zero mode weights $|\varepsilon(n)|$ | Super-exponential UV silence | Supports hierarchy, not a free lever |
| Zeta spectral sums | Alternative packaging of same spectrum | Must agree on physical standard parts |

### 2.5 Gauge unification residual

| Method | Result | Status |
|--------|--------|--------|
| SM running + geometric thresholds | $\sim 7\%$ floor (doc 12 discipline) | Not percent-level claim |
| VL_Q research path (doc 33) | $\sim 2.6\%$ two-loop with forced $M_*$ | Research; $M_X=\Lambda_0$ |
| Dual-Zero reweight of towers | Does not by itself remove the floor | Scanned; no miracle |

### 2.6 Riemann Hypothesis language

| Method | Result | Status |
|--------|--------|--------|
| Variational / information-current (Dual-Zero motivated) | **Proposal only** | **Not a proof** |
| Zeta of $D$ | Spectral zeta ≠ proof of classical RH | Discipline |

---

## 3. Policy

1. Use **heat kernel / Seeley** for $G_N$, $m_H$ class, continuum $\eta$ derivation.  
2. Use **Dual-Zero** as the UV regulator and information-conserving mode weight with **fixed** $\omega_0$.  
3. Use **zeta** only as an equivalent spectral language, not a second free regulator.  
4. Never retune $\omega_0$ or switch regulators to chase a single experimental digit.

---

*Regulator comparison lock — August 2026.*
