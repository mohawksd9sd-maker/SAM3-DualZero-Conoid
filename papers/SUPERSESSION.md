# Papers directory — SUPERSESSION BANNER

**Effective:** August 2026  
**Authority:** [`STATUS_CLAIMS_AND_RESIDUALS.md`](../STATUS_CLAIMS_AND_RESIDUALS.md) + [`docs/math_notes/`](../docs/math_notes/)

---

## Rule

Every `.tex` file here is historical or expanded source unless listed as current core.
**STATUS + `docs/math_notes/` supersede** all conflicting claims.

---

## Current core paper (modest)

- [`SAM3_Core_Geometry_and_Spectral_Results.tex`](SAM3_Core_Geometry_and_Spectral_Results.tex) — three light sectors + $G_N\propto\ell_0^2$ only

---

## Known concrete errors corrected

| File | Error | Correction |
|------|-------|------------|
| `SAM3_Complete_Mathematical_Foundations.tex` | Stated $f=\sqrt{u^2+16\ell_0^2\cos^2(2v)}$ | **Must be 4**, from own parametrization $\mathbf{r}=(u\cos v,u\sin v,\ell_0\sin 2v)$ |
| Same + curvature | Used 16 in $R$ | $K=-4\ell_0^2\cos^2(2v)/(u^2+4\ell_0^2\cos^2(2v))^2$ |
| Same | “All theorems rigorously proven” + RH language | Historical index only; RH = **proposal** |

Any other file still showing coefficient **16** is stale and wrong.

---

## Specifically superseded language

| Older language | Superseded by |
|----------------|---------------|
| $f^2=u^2+16\ell_0^2\cos^2(\cdot)$ | **$4\ell_0^2$ only** |
| Exact $m_H=125.1$ GeV | 125 GeV **class** |
| Percent-level unification as fact | ~$7\%$ floor |
| RH proved / theorem | **Proposal only** |
| Free / fitted $\omega_0$ | Geometric $\omega_0\approx 0.927$ |
| $A_5$ isometries of the continuum metric | **False**; $C_4$ only |
| Ultrafilter required for numerics | Constructive finite-$N$ |
| Full SM derived in foundations file | Not claimed in core paper |

---

## Banner for every paper preamble

```tex
% SUPERSEDED where conflicting: STATUS_CLAIMS_AND_RESIDUALS.md
% Metric: f=sqrt(u^2+4 ell0^2 cos^2(2v)) only.
% RH = variational proposal only — not a proof.
% A5 is NOT an isometry group of the locked metric (C4 only).
```

---

*Supersession — August 2026 (metric error fix pass).*
