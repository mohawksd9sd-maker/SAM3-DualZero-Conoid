# Audit note — metric coefficient 16 error

**Date:** August 18, 2026  
**Trigger:** External review of `papers/SAM3_Complete_Mathematical_Foundations.tex`

## Error

The May 2026 foundations file stated

$$
f=\sqrt{u^2+16\ell_0^2\cos^2(2v)}
$$

from the parametrization $\mathbf{r}=(u\cos v, u\sin v, \ell_0\sin(2v))$.

**Correct induced metric:**

$$
|\mathbf{r}_v|^2 = u^2 + 4\ell_0^2\cos^2(2v).
$$

Coefficient **4**, not 16.

## Action taken

1. Corrected `papers/SAM3_Complete_Mathematical_Foundations.tex`  
2. Strengthened `papers/SUPERSESSION.md`  
3. Locked docs already used coefficient 4 (Notes II, XII, XXXI, core paper)

## Honesty

A full line-by-line audit of every historical `.tex` under `papers/` for residual “16” strings was not completed in earlier passes that focused on `docs/math_notes/`. That was a process failure. This note records the failure and the fix for the identified contradiction.

## Dual-Zero Reg2 remark (external review)

For $\varepsilon(n)=\omega_0(-1)^n n^{-n}$, $\mathrm{st}(\varepsilon)=0$ is immediate. The constructive finite-$N$ form (hardening doc 39) is the operational definition; ultrafilter language is not load-bearing for $G_N\propto\ell_0^2$ or G3'.
