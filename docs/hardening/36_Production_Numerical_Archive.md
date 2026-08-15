# 36 — Production Numerical Archive (Error Budgets + Regeneration)

**Status:** Production archive  
**Date:** August 2026  
**Scripts:** `code/production_regenerate_locked.py`, `code/unification_vlq_residual.py`, `code/af_prime_vprime.py`  
**SSOT for claims:** `STATUS_CLAIMS_AND_RESIDUALS.md`

Rule: values are **derived outputs**, not fit parameters.

---

## 1. Locked constants

| Symbol | Value | Error / band | Origin |
|--------|-------|--------------|--------|
| $n_{\rm bridges}$ | 12 | exact | 2I geometry |
| $\Delta\theta$ | $2\pi/12$ | exact | bridges |
| $\omega_0$ | 0.927 | $\pm 0.005$ geometric modelling | doc 35, 18 |
| $\phi$ | $+2\pi/5$ | exact (2I) | CP phase |
| $\kappa_u/\kappa_d$ | $1/2$ | exact (intertwiner) | doc 14 |
| $C_g$ | $(6/5,\,1,\,4/5)$ | exact (module) | doc 09 |

---

## 2. Continuum defect overlaps

| $\eta_{ij}$ | Central | Band |
|------------|---------|------|
| $\eta_{12}$ | 0.8607 | $\pm 0.010$ (heat-kernel / resolution) |
| $\eta_{13}$ | 0.5439 | $\pm 0.015$ |
| $\eta_{23}$ | 0.4789 | $\pm 0.015$ |

Heat-kernel continuum law (doc 32): RMS vs locked triple $\approx 0.008$.

---

## 3. Flavor angles

| Angle | Central | Band | Notes |
|-------|---------|------|-------|
| $\theta_{12}^{\rm CKM}$ | $12.85^\circ$ | $\pm 0.3^\circ$ | $\eta_{12}\times\pi/12$ |
| $\theta_{23}^{\rm CKM}$ | $2.36^\circ$ | $\pm 0.15^\circ$ | Casimir-weighted |
| $\theta_{13}^{\rm CKM}$ | $0.24^\circ$ | $\pm 0.10^\circ$ | residual-sensitive |
| $\delta_{\rm CKM}$ | $\sim 70^\circ$ | $\pm 10^\circ$ class | $\phi=2\pi/5$ |
| $J$ | $\sim 3\times 10^{-5}$ | factor $\sim 2$ | consistency |

---

## 4. Gravity / Higgs / unification

| Quantity | Value | Band |
|----------|-------|------|
| $G_N=64\pi\ell_0^2/45$ | locked formula | scheme O(1–few %) |
| $m_H$ | 125 GeV class | $124$–$127$ GeV |
| Unification residual (SM-like floor) | $\sim 7\%$ | doc 12 discipline |
| VL_Q path residual (doc 33) | $\sim 2.6\%$ two-loop | research path; $M_X\neq\mu_{\rm meet}$ |

---

## 5. Lepton sector (see also doc 38)

| Quantity | Prediction | Band |
|----------|------------|------|
| $\delta_{\rm PMNS}$ | large | $200^\circ$–$270^\circ$ |
| $\sum m_\nu$ | hierarchical light | model-dependent width |
| $m_{\beta\beta}$ | see doc 38 | confront $0\nu\beta\beta$ |

---

## 6. Regeneration protocol

```bash
pip install -r requirements.txt
python code/production_regenerate_locked.py
python code/unification_vlq_residual.py   # optional research path
python code/af_prime_vprime.py             # optional AF′ layer
```

The production script reprints locked centrals and asserts internal consistency (no experimental retuning).

---

## 7. Error-budget sources (ranked)

1. Continuum discretization / APS residual ($<10^{-3}$ Dirac; $\eta$ O(1%))
2. Heat-kernel vs defect-operator representation of $\eta$
3. Seeley coefficient / scheme matching for $G_N$, $m_H$ class
4. Two-loop / threshold modelling for gauge residuals
5. RH neutrino hierarchy detail for sharp $\delta_{\rm PMNS}$, $m_{\beta\beta}$

---

*Production archive — derivation only, no tuning.*
