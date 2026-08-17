# Mathematical Note XXVII — Production Channel Pipeline

**Date:** August 2026  
**Purpose:** Elevate continuum numerical support from ad hoc prototype to a **frozen, outsider-runnable channel pipeline** (item 4).

---

## 1. Design choice

The generation theorem’s spectral isolation is **channel-decomposed** under the Fourier/$m_\rho$ split. The production numerical support is therefore the family of 1D Sturm–Liouville problems $H_m$, not an unreduced 2D FD Dirac with assembly sign risks.

This matches the pure-math reduction (Notes XVIII–XIX) and is reproducible at high resolution.

---

## 2. Frozen protocol

```text
code/production_channel_pipeline.py
```

| Parameter | Frozen value |
|-----------|--------------|
| $U$ scan | $\{10,20,40,80\}$ |
| Grid $n$ | 4000 interior points |
| $\epsilon$ soft floor | $10^{-4}$ |
| Tip $(a,\kappa,C)$ | $(1,1,1)$ |
| Light $m$ | $0,1,2$ |
| Heavy $m$ | $3,4,5,6$ |
| Threshold | mid-gap $\tau$ |

**Outputs:** gap vs $U$, isolation counts, JSON report, exit code 0 iff isolation $(3,0)$ holds for all $U$.

---

## 3. Acceptance criteria

| Test | Criterion |
|------|-----------|
| Isolation | 3 light / 0 heavy below $\tau$ at every $U$ |
| Gap positivity | $\Delta>0$ all $U$ |
| Smoothing continuity | $E_0(\delta)$ Cauchy as $\delta\downarrow 0$ |

---

## 4. Relation to full 2D APS

A full 2D APS eigensolver remains desirable as a cross-check. It is **not** the load-bearing numerical object for $H_{\mathrm{tip}}$ once the channel reduction is accepted. STATUS should cite this pipeline for isolation claims.

---

*Note XXVII — production channel pipeline.*
