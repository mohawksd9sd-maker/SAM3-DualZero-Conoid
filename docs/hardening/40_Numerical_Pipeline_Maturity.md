# 40 — Numerical Pipeline Maturity

**Status:** Hardening priority note + minimal reproducibility pack  
**Date:** August 2026  
**STATUS flag:** production 2D APS eigensolvers remain **prototype-level**; continuum residual $<10^{-3}$ is stage-appropriate, not final production.

---

## 1. Current maturity

| Component | Maturity | Notes |
|-----------|----------|-------|
| Continuum residual 4th-order FD | Good for stage | $<10^{-3}$ at moderate resolution |
| APS gap $\propto 1/u_{\rm max}\to 0$ | Locked claim | Continuum zero-mode limit |
| Full 2D APS eigensolver in `code/` | **Prototype** | Not a frozen production binary |
| Frozen grids + manufactured residuals | **This note + script** | Minimal pack |
| $\omega_0$ / domain sensitivity | **This note + script** | Required discipline |

---

## 2. Reproducibility requirements (next priority)

1. **Frozen grid parameters** — $(N_u,N_v,u_{\rm max},\ell_0)$ written to JSON/sidecar next to outputs.  
2. **Manufactured residual tests** — impose smooth test spinors; report $\lVert D_{\rm num}\psi-D_{\rm exact}\psi\rVert$.  
3. **Domain sensitivity** — scan $u_{\rm max}$; confirm gap scaling and $\eta$ stability within archive bands.  
4. **$\omega_0$ sensitivity** — vary $\omega_0$ in $\pm 0.005$ (geometric band); locked angles must not be retuned.  
5. **No experimental fit loops** — scripts must not read PDG targets as optimizers.

---

## 3. Minimal pack in repo

| File | Role |
|------|------|
| `code/pipeline_maturity_checks.py` | Manufactured residual proxy, domain/$\omega_0$ sensitivity on analytic probes |
| `code/production_regenerate_locked.py` | Locked centrals |
| `code/dual_zero_constructive.py` | Constructive Dual-Zero weights |

Full production APS solver remains future engineering work; STATUS continues to flag prototype status until a frozen eigensolver hash is published.

---

## 4. Pass criteria (stage)

| Check | Pass |
|-------|------|
| Manufactured residual proxy | decreases with resolution order |
| Gap proxy vs $u_{\rm max}$ | monotone decrease |
| $\eta$ proxy vs $\omega_0\pm 0.005$ | stays within doc 36 bands |
| Cabibbo from $\eta_{12}$ | no retune |

---

*Pipeline maturity — honest prototype flag retained.*
