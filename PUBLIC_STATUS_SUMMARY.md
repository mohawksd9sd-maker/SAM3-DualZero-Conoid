# SAM3 — Public Status Summary (for outside readers)

**Last update:** August 2026  
**Full authority:** [`STATUS_CLAIMS_AND_RESIDUALS.md`](STATUS_CLAIMS_AND_RESIDUALS.md)  
**Short math notes:** [`docs/math_notes/`](docs/math_notes/)  
**Modest paper draft:** [`papers/SAM3_Core_Geometry_and_Spectral_Results.tex`](papers/SAM3_Core_Geometry_and_Spectral_Results.tex)

This page is the **one-screen** view of what is locked versus residual. Older papers that conflict with this summary are superseded ([`papers/SUPERSESSION.md`](papers/SUPERSESSION.md)).

---

## Locked (high confidence)

| Result | One-line statement |
|--------|--------------------|
| **Metric** | $f=\sqrt{u^2+4\ell_0^2\cos^2(2v)}$ only (not $16\ell_0^2$) |
| **3 generations** | APS Dirac + 12-bridge / 2I structure → three continuum chiral sectors |
| **Newton constant** | $G_N=64\pi\ell_0^2/45$ from spectral-action $a_2$ |
| **Dual-Zero regulator** | $\varepsilon(n)=\omega_0(-1)^n n^{-n}$, $\omega_0\approx 0.927$ geometric; not a free fit |
| **CKM structure** | $\theta_{12}\approx 12.85^\circ$, $\theta_{23}\approx 2.36^\circ$, phase $\phi=2\pi/5$ |
| **Higgs** | 125 GeV **class** (band), not a tuned digit |

---

## Residual (not overclaimed)

| Topic | Status |
|-------|--------|
| Production 2D APS eigensolver | Prototype |
| Gauge unification | ~$7\%$ geometric floor; percent-level **not** claimed |
| Cosmological constant magnitude | Open |
| Digit PMNS / $m_{\beta\beta}$ | Bands only |
| **Riemann Hypothesis** | Variational **proposal only** — **not a proof** |

---

## What to read first (outsiders)

1. This summary  
2. [Math Note I — three generations](docs/math_notes/01_Three_Generations_APS_2I.md)  
3. [Math Note II — metric and $G_N$](docs/math_notes/02_Metric_and_Newton_Constant.md)  
4. [Core paper draft (modest)](papers/SAM3_Core_Geometry_and_Spectral_Results.tex)  
5. [Reproducible pipeline](docs/math_notes/03_Reproducible_Pipeline.md) — `python code/reproduce_status_locked.py`

Unification narratives, AF′ enlargements, and RH language are **secondary** until the two core mathematical notes have been externally checked.

---

## Reproduce locked numbers

```bash
python code/reproduce_status_locked.py
python code/dual_zero_constructive.py
python code/pipeline_maturity_checks.py
```

---

*Public summary — derivation only, no experimental tuning, no overclaim.*
