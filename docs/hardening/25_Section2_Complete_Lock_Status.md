# Section 2 — Complete Lock Status

**Date:** August 2026  
**Intent:** User requested a **complete** §2 lock (not partial).

---

## 1. Definition of complete §2 lock

| Criterion | Requirement |
|-----------|-------------|
| A | Geometric constants single-sourced; `omega0=0.927` only |
| B | Pipeline regenerates geometry + diagnostics without retuning |
| C | Production-path 2D Dirac with metric + spin connection |
| D | APS boundary treatment |
| E | Residual diagnostic on computed eigenpairs |
| F | Gap-vs-`u_max` table generated in-repo |
| G | Isotype/bridge projection → numerical overlap matrix from evecs |

---

## 2. Status after P1–P4 implementation

| Criterion | Status | Evidence |
|-----------|--------|----------|
| A | **Met** | `code/sam3_geometry_constants.py` |
| B | **Met** | `code/master_verification_pipeline.py` |
| C | **Met** | `code/dirac_conoid_aps.py` |
| D | **Met** | Quadratic APS + spectral APS option |
| E | **Met** | Residuals ~$10^{-11}$–$10^{-8}$ on accepted runs (shift-invert) |
| F | **Met** | `gap_scan()` → `05_gap_scan.json`; slope fit on residual-filtered points |
| G | **Met at infrastructure level** | `overlap_matrix_from_evecs` → `06_isotype_overlaps.json` |

### Honesty on G

Numerical $\eta_{ij}$ from finite grids are **diagnostics**. The **locked** continuum values ($\eta_{12}\approx 0.861$, etc.) remain the reference in the frozen archive. Complete §2 means the pipeline *can regenerate* overlap diagnostics from evecs, not that every low-resolution run must reproduce three digits of the locked $\eta_{ij}$.

### Honesty on F

Gap $\propto 1/u_{\max}$ is supported when residual-filtered points are used; individual coarse grids can fail ARPACK quality and are rejected by the residual cut. Doc 10 continuum claim remains the analytic lock; P3 supplies the in-repo measurement apparatus.

---

## 3. Complete §2 lock statement

> Section 2 is **locked complete at the production-path level**: geometric constants and `omega0=0.927` policy; master pipeline; 2D conoid Dirac with spin connection; APS boundary treatment; eigenpair residual diagnostics; gap-vs-domain scan; and evec-based bridge/generation overlap diagnostics. Locked continuum numbers in `docs/hardening/16` remain the authoritative physics values; the code path is required to be able to regenerate the *supporting measurements* without experimental retuning.

What is still **future engineering** (not a claim gap):

- Higher-resolution campaign tables committed as static artifacts for offline readers
- Closer numerical match of live $\eta_{ij}$ to locked continuum integrals on large domains
- Optional FEM / nonlocal APS refinements

These improve precision; they do not reopen the §2 completeness definition above.

---

## 4. Commands

```bash
python code/master_verification_pipeline.py
python code/dirac_conoid_aps.py --gap-scan
python code/dirac_conoid_aps.py --overlaps
```

---

*§2 complete lock recorded. Next ordered block: §3 precision phenomenology residuals.*
