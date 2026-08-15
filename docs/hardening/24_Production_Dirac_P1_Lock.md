# Production Dirac P1 — Partial→Complete §2 Path

**Status:** P1 implemented and locked as production-*path* (August 2026)  
**Goal:** Move §2 from partial lock toward complete lock.

---

## 1. What P1 delivers

New module: `code/dirac_conoid_aps.py`

| Feature | Status |
|---------|--------|
| Explicit conoid metric $g_{vv}=u^2+4\ell_0^2\cos^2(2v)$ | Yes |
| Spin-connection coefficient on grid | Yes (leading $\partial_u\log f$ form) |
| 2-component spinor, full $(u,v)$ coupling | Yes |
| Periodic $v$ (bridge circle) | Yes |
| 4th-order FD option | Yes |
| APS-style boundary penalty at $u=\pm u_{\max}$ | Yes |
| Residual $\|D\psi-\lambda\psi\|/\|\psi\|$ | Yes |
| Gap scan $\|\lambda\|_{\min}$ vs $u_{\max}$ + log-log slope | Yes |
| `omega0 = 0.927` geometric only | Yes |

Pipeline integration: `master_verification_pipeline.py` calls P1 spectrum + lightweight gap scan and writes:

- `03_dirac_p1_spectrum.json`
- `05_gap_scan.json`

---

## 2. What still separates P1 from a *complete* §2 lock

| Missing (P2–P4) | Why it matters |
|-----------------|----------------|
| **P2** Spectral (nonlocal) APS projector, not only quadratic penalty | Cleaner continuum chirality control |
| **P3** Published high-resolution gap/residual tables frozen in-repo from long runs | Reproducibility without re-running heavy jobs |
| **P4** 2I isotype projection → live $\eta_{ij}$ re-integration | True regeneration of defect overlaps from eigenvectors |

P1 is necessary and now present. Complete §2 lock = P1–P4 all green.

---

## 3. Relation to doc 10 continuum residual claim

Doc 10’s residual $<10^{-3}$ and gap $\propto 1/u_{\max}$ were analysis locks.  
P1 **provides the in-repo operator and diagnostics** that can support those claims.  
Whether a given machine/run hits residual $<10^{-3}$ depends on resolution (`Nu,Nv,u_max`). The pipeline records the measured residual; it does not fabricate success.

---

## 4. How to run

```bash
# Full pipeline (geometry + P1 Dirac + gap scan)
python code/master_verification_pipeline.py

# Dirac only
python code/dirac_conoid_aps.py
python code/dirac_conoid_aps.py --gap-scan
```

---

## 5. Lock statement (P1)

> A production-path 2D Dirac operator on the right conoid is implemented in `dirac_conoid_aps.py` with metric, spin connection, APS-style boundary penalty, residual diagnostics, and gap-vs-$u_{\max}$ scanning, using geometric $\omega_0=0.927$ only. Section 2 remains short of a **complete** lock until P2–P4 (spectral APS, frozen high-res tables, isotype→$\eta_{ij}$ pipeline) are delivered. P1 is no longer a radial-sector prototype.

---

*Next: P2 spectral APS, then P3 tables, then P4 isotype overlaps — required for complete §2 lock.*
