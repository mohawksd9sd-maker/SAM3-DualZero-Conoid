# Reproducible Numerical Pipeline — Frozen Specification

**Status:** Public freeze of regeneration protocol for STATUS locked numbers  
**Date:** August 2026  
**Entry point:** `code/reproduce_status_locked.py`

---

## 1. Scope

This pipeline **regenerates and checks** every high-confidence locked number listed in `STATUS_CLAIMS_AND_RESIDUALS.md` that is purely geometric / algebraic (no experimental optimizer).

It does **not** claim a finished production 2D APS eigensolver binary. Continuum residual $<10^{-3}$ remains a stage result (STATUS flag).

---

## 2. Locked outputs (must regenerate)

| Symbol | Central | Band / note |
|--------|---------|-------------|
| Metric tip coefficient | $4\ell_0^2$ | convention |
| $\omega_0$ | 0.927 | $\pm 0.005$ geometric |
| $n_{\rm bridges}$ | 12 | exact |
| $\Delta\theta$ | $2\pi/12$ | exact |
| $\eta_{12},\eta_{13},\eta_{23}$ | 0.8607, 0.5439, 0.4789 | $\pm 0.01$–$0.015$ |
| $\theta_{12}$ | $12.85^\circ$ | from $\eta_{12}\times\pi/12$ |
| $\theta_{23}$ | $2.36^\circ$ | locked central |
| $\theta_{13}$ | $0.24^\circ$ | wider residual |
| $\phi$ | $2\pi/5$ | exact |
| $\kappa_u/\kappa_d$ | $1/2$ | exact |
| $C_g$ | $(6/5,1,4/5)$ | exact |
| $G_N$ formula | $64\pi\ell_0^2/45$ | scheme O(few %) |
| $m_H$ | 125 GeV class | 124–127 GeV band |

---

## 3. How to run

```bash
pip install -r requirements.txt
python code/reproduce_status_locked.py
python code/dual_zero_constructive.py
python code/pipeline_maturity_checks.py
```

Expected: all assertions pass; printed table matches STATUS centrals within bands.

---

## 4. Error budgets

| Source | Affects | Size |
|--------|---------|------|
| Continuum discretization | $\eta$, Dirac residual | $<10^{-3}$ residual stage; $\eta$ O(1%) |
| $\omega_0$ geometric band | mode weights | $\pm 0.005$ |
| Seeley scheme moments | $G_N$ interpretation | O(1–few %) |
| Prototype APS | full 2D spectrum | **not** production-frozen |

---

## 5. Sensitivity tests included

- Cabibbo from $\eta_{12}$ vs locked $12.85^\circ$  
- $\omega_0\pm 0.005$ on Dual-Zero weight sums  
- Domain gap proxy $\propto 1/u_{\max}$  
- Metric convention flag ($4$ not $16$)

---

## 6. Forbidden

- Reading PDG values as fit targets  
- Retuning $\omega_0$  
- Claiming RH proof or percent-level unification from this script  

---

*Frozen reproducibility specification.*
