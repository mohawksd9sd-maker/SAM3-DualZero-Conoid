# SAM3 — Public Status Summary

**Last update:** 23 November 2026 (America/Chicago)

---

## Proved (core geometry)

| Result | Statement |
|--------|-----------|
| Metric | $f=\sqrt{u^2+4\ell_0^2\cos^2(2v)}$ **only** (from the locked embedding) |
| Symmetry | $C_4$ exact; $A_5$ is **not** an isometry of $f$ |
| Curvature | $K=-4\ell_0^2\cos^2(2v)/f^4$ |
| $C_0$ exists | $\mathrm{Vol}(U)=\pi U^2+2\pi\log U+C_0+o(1)$ |
| $E_0(2)<E_0(3)$ | Variational theorem on the radial model operators |
| $G_N$ | $\propto\ell_0^2$ structurally; the prefactor $64\pi/45$ is a **convention**, not a derivation |

---

## Numerical (reproduced)

- $C_0\approx 4.3551723$ (unit metric). The older band $4.43$–$4.45$ does **not** reproduce.
- Hermitian 2D Dirac on the flat torus: known-answer error $\approx 0.002$ at $N=24$, convergence order $\approx 2$.
- The legacy symmetrised Dirac assembly fails that test.

Run `python code/core_reproducibility.py` and `pytest -q`.

---

## Not derived / not claimed

- $\omega_0\approx 0.927$ and the exponent $4/13$
- Exactly three chiral generations as an APS index theorem (this remains a conjecture / heuristic soft block $\{0,1,2\}$)
- CKM / PMNS / $\eta$ digits, Higgs mass, percent-level unification
- A proof of the Riemann hypothesis (proposal only; identification tests were null)
- A full Standard Model derivation

---

## Read

1. This page
2. `STATUS_CLAIMS_AND_RESIDUALS.md`
3. `papers/SAM3_Core_Geometry_and_Spectral_Results.tex`
4. `docs/AUDIT_CORE_SOLIDIFICATION_NOV2026.md`
5. `docs/hardening/18_DualZero_Definition_Lock.md` (Dual-Zero as a *definition*)
