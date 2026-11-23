# SAM3 — Public Status Summary

**Last update:** 23 November 2026 (America/Chicago)

---

## Proved (core geometry)

| Result | Statement |
|--------|-----------|
| Metric | $f=\sqrt{u^2+4\ell_0^2\cos^2(2v)}$ **only** (from the locked embedding) |
| Symmetry | $C_4$ exact; $A_5$ is **not** an isometry of $f$ |
| Curvature | $K=-4\ell_0^2\cos^2(2v)/f^4\le 0$, integrable, but **unbounded** near the four tip nodes (the older global bound $1/(4\ell_0^2)$ is withdrawn) |
| $C_0$ | exists, and equals $2\pi\ln 2$ on the unit metric (**theorem**) |
| $E_0(2)<E_0(3)$ | Variational theorem on the radial model operators |
| Exact $E_0(m;U)$ | $(j_{\nu,1}/U)^2$ with $\nu=\sqrt{m^2+1/4}$; $E_0(0)=\pi^2/U^2$ (radial model, not the 2D Dirac operator) |
| APS index on the truncated conoid | $0$ for the *untwisted* Dirac operator, product collar, bounding spin structure.  Independent of the cuts and of $\ell_0$.  Not equal to $3$. |
| Singular tip $u=0$ | A geodesic boundary circle of length $8\ell_0$ with four metric-degeneracy points; not a cone.  Does **not** give a derived index of $3$ (doc 46). |
| Total curvature of the complete conoid | $\int K\,dA=-2\pi$; Gauss–Bonnet on every truncation $X_{a,b}$ is an identity |
| $G_N$ | $\propto\ell_0^2$ structurally; the prefactor $64\pi/45$ is a **convention**, not a derivation |

---

## Numerical (reproduced)

- $C_0=2\pi\ln 2\approx 4.35517218$ (unit metric, theorem). The older band $4.43$–$4.45$ does **not** reproduce.
- Exact $E_0(m)$ at $U=20$: $0.024674,\,0.039801,\,0.067954,\,0.103387$ for $m=0,1,2,3$ (finite differences agree to $\sim 10^{-6}$).
- Hermitian 2D Dirac on the flat torus: known-answer error $\approx 0.002$ at $N=24$, convergence order $\approx 2$.
- The legacy symmetrised Dirac assembly fails that test.

Run `python code/core_reproducibility.py` and `pytest -q`.

---

## Not derived / not claimed

- $\omega_0\approx 0.927$ and the exponent $4/13$
- Exactly three chiral generations as the APS index of the *untwisted* Dirac operator on the truncated conoid: **refuted** (the index is $0$).  Index $3$ would need an underived Falomir flux $\kappa\in(2,3]$.  The singular tip is a geodesic boundary with four nodes, not a cone, and does not give a derived index of $3$ (doc 46).
- Gauge group, mass ratios, $\omega_0$, $4/13$, the $G_N$ prefactor $\alpha$, and coupling unification from the locked geometry: attempted honestly and **not derived** (docs 44–45)
- Almost-commutative product with CCM $F=(\mathbb{C}\oplus\mathbb{H}\oplus M_3(\mathbb{C}))$: the raw product conoid $\times F$ is 2D, not a 4D unification model.  A spectator conoid does not change $g_3^2=g_2^2=\tfrac53 g_1^2$ or the CCM Higgs relation at $\Lambda$.  One-loop running of those conditions does not unify at one scale; the CCM Higgs example remains $\sim 170\,\mathrm{GeV}$.  $N=3$ is an input of $F$.  See doc 45.
- CKM / PMNS / $\eta$ digits, Higgs mass, percent-level unification
- A proof of the Riemann hypothesis (proposal only; identification tests were null)
- A full Standard Model derivation

Exploratory survey of other surfaces and internal spaces (doc 47, `experiments/alt_geometries/`): **not part of the locked core**.  No alternative examined there derives the integer 3 or unique mass ratios from the conoid.  The cleanest generation *mechanism* in that survey is a chosen flux on a compact surface, in a 4D product with a CCM or Pati–Salam finite triple.

---

## Read

1. This page
2. `STATUS_CLAIMS_AND_RESIDUALS.md`
3. `papers/SAM3_Core_Geometry_and_Spectral_Results.tex`
4. `docs/AUDIT_CORE_SOLIDIFICATION_NOV2026.md`
5. `docs/hardening/18_DualZero_Definition_Lock.md` (Dual-Zero as a *definition*)
6. `docs/hardening/44_E0_Exact_APS_Index_Unification_Attempts.md`
7. `docs/hardening/45_Almost_Commutative_CCM_Product.md`
8. `docs/hardening/46_Singular_Tip_Analysis.md`
9. `docs/hardening/47_Alternative_Geometries_Exploratory.md` (exploratory; not core)
