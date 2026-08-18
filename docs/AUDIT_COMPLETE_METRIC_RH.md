# Full papers/ audit — complete

**Date:** August 18, 2026

## What was wrong

Multiple historical `.tex` files under `papers/` still used

$$
f=\sqrt{u^2+16\ell_0^2\cos^2(2v)}
$$

which contradicts the induced metric of the stated parametrization (coefficient **4**) and the locked docs.

## Files scanned

All 38+ `.tex` files under `papers/` were downloaded and scanned for:

- metric coefficient `16\ell_0`
- RH “proved / theorem” overclaim language
- $A_5$ metric isometry overclaims

## Files that had the metric-16 error (corrected 16→4, curvature 32→4)

- SAM3_Complete_Mathematical_Foundations.tex (earlier fix)
- SAM3_Complete_Mathematical_Foundations1.tex
- SAM3_Consolidated_Proofs.tex
- SAM3_Paper_03_Dirac_Operator_Final.tex
- SAM3_Paper_04_Yukawa_Derivation_Final.tex
- SAM3_Paper_05_Gravity_Final.tex
- SAM3_Paper_17_Rigorous_Foundations.tex
- SAM3_Paper_18_Numerical_Robustness_and_Reproducibility.tex
- SAM3_v4.20_full_paper.tex
- SAM3_v4.22_Addendum.tex
- SAM3-DeformedHopfBundle.tex (induced form)
- Plus supersession banners on the full remaining paper set

## Policy

Every historical paper now carries:

```
% SUPERSEDED where conflicting: STATUS_CLAIMS_AND_RESIDUALS.md / docs/math_notes/
% LOCKED metric: coefficient 4, not 16
% RH = proposal only; A5 is not a metric isometry
```

## Authoritative sources

| Topic | Source |
|-------|--------|
| Metric | math notes + core paper |
| Generations / $G_N$ | Notes XII–XXXI + core paper |
| Claims / residuals | STATUS_CLAIMS_AND_RESIDUALS.md |
| Supersession list | papers/SUPERSESSION.md |

## Residual honesty

Older papers still contain phenomenological overclaims in body text (e.g. exact $m_H$ digits, “full SM derived”). Those are **not** deleted line-by-line in every paragraph; they are **superseded by policy**. The core public paper does not make those claims.

## Dual-Zero Reg2

For $\varepsilon(n)\propto n^{-n}$, $\mathrm{st}=0$ is immediate. Operational definition is constructive finite-$N$ (hardening doc 39).
