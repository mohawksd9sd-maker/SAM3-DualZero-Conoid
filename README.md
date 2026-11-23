# SAM3-DualZero-Conoid

**Geometric / spectral research on a right conoid with Dual-Zero regularisation**

Honesty rule: unproven statements are labelled as such. Null results stay null.

**Start here:** [`BOTTOM_LINE.md`](BOTTOM_LINE.md) — what is proven, what the unification experiments showed, and the missing principle.

**GUT / TOE targets:** [`ROADMAP_TOE_GUT.md`](ROADMAP_TOE_GUT.md) — what has been established, and what must still be found for an authentic GUT and an authentic TOE, with falsifiable tests.  Research targets, not claims.

---

## Start here (outsiders)

1. **[`BOTTOM_LINE.md`](BOTTOM_LINE.md)** — short public statement of where the work stands
2. **[`ROADMAP_TOE_GUT.md`](ROADMAP_TOE_GUT.md)** — research targets for an authentic GUT and an authentic TOE
3. **[`PUBLIC_STATUS_SUMMARY.md`](PUBLIC_STATUS_SUMMARY.md)** — proved vs numerical vs not derived
4. **[`papers/SAM3_Core_Geometry_and_Spectral_Results.tex`](papers/SAM3_Core_Geometry_and_Spectral_Results.tex)** — current core paper (November 2026)
5. **[`STATUS_CLAIMS_AND_RESIDUALS.md`](STATUS_CLAIMS_AND_RESIDUALS.md)** — SSOT
6. **[`docs/AUDIT_CORE_SOLIDIFICATION_NOV2026.md`](docs/AUDIT_CORE_SOLIDIFICATION_NOV2026.md)** — audit of claims vs evidence
7. **[`docs/hardening/18_DualZero_Definition_Lock.md`](docs/hardening/18_DualZero_Definition_Lock.md)** — Dual-Zero as a definition

**Core-first:** unification and RH narratives are secondary. The Riemann hypothesis is a proposal only; a non-circular identification test in this repository found no evidence that Dual-Zero critical points match zeta zeros.

---

## Locked metric (from the embedding)

$$
f(u,v)=\sqrt{u^2+4\ell_0^2\cos^2(2v)}
$$

($4\ell_0^2$ only — not $16\ell_0^2$.) This, the exact $C_4$ isometry, the curvature formula, $C_0=2\pi\ln 2$, $E_0(m_2)>E_0(m_1)$, the exact formula $E_0(m;U)=(j_{\nu,1}/U)^2$, and the APS index $0$ of the untwisted Dirac operator on the truncated conoid, are proved in the core paper.

---

## Reproduce the core paper

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python code/core_reproducibility.py
pytest -q
```

Key reproduced numbers (unit metric $\ell_0=1$):

- $C_0=2\pi\ln 2\approx 4.35517218$ (proved on the unit metric; the older band $4.43$–$4.45$ does **not** reproduce)
- $E_0(m;U)=(j_{\nu,1}/U)^2$ with $\nu=\sqrt{m^2+1/4}$; $E_0(0)=\pi^2/U^2$.  At $U=20$: $0.024674,\,0.039801,\,0.067954,\,0.103387$ for $m=0,1,2,3$
- APS index of the *untwisted* Dirac operator on the truncated conoid (bounding spin structure) is $0$, not $3$.  See doc 44.
- The tip $u=0$ is a geodesic boundary of length $8\ell_0$ with four metric-degeneracy points, not a cone; it does not give a derived index of $3$.  $|K|$ is unbounded near the nodes (the older bound $1/(4\ell_0^2)$ is withdrawn).  See doc 46.
- Complete-conoid total curvature $\int K\,dA=-2\pi$.  Raw conoid $\times F$ is 2D, not a 4D CCM model (doc 45).
- Flat-torus Hermitian Dirac, $N=24$: $\max|\lambda-\lambda_{\mathrm{exact}}|\approx 0.00202$, convergence slope $\approx-1.995$
- $G_N=64\pi\ell_0^2/45$ is a **convention lock**, not an independent derivation
- $\omega_0\approx 0.927$ and the exponent $4/13$ are **not derived**

Exploratory, not core: alternative surfaces and internal spaces are surveyed in [`docs/hardening/47_Alternative_Geometries_Exploratory.md`](docs/hardening/47_Alternative_Geometries_Exploratory.md) and `experiments/alt_geometries/`.  They do not change the locked theorems.  No alternative examined there derives the integer 3 from the conoid.

A follow-up, also exploratory, develops the product conoid × magnetized surface × Pati–Salam in [`docs/hardening/48_PS_Conoid_Product.md`](docs/hardening/48_PS_Conoid_Product.md) and `experiments/ps_conoid_product/`.  The flux and the surface moduli remain unfixed; the integer 3 is still a choice.

A broader survey of candidate principles (index theory, modular invariance, regularized determinants, orbifold zero modes, NCG classification, and others), with four computations, is in [`docs/hardening/49_Missing_Principle_Survey.md`](docs/hardening/49_Missing_Principle_Survey.md) and `experiments/missing_principle/`.  Nothing tested there derives a unique flux \(M=3\) or a unique area.  Two conflicting mechanisms can fix \(\tau\): maximizing \(\det'\Delta\) selects the hexagonal torus; \(C_4\) compatibility selects the square torus.

A further round of candidate tests (standard \(T^6\) orbifolds, tadpoles, \(T^2/\mathbb{Z}_N\) for \(N=2,3,4,6\), the product spectral action including the tip, and a declared coincidence scan) is in [`docs/hardening/50_Further_Candidate_Tests.md`](docs/hardening/50_Further_Candidate_Tests.md) and `experiments/further_candidates/`.  No accidental fit was found.  The bottom line is unchanged.

A review of the SAM-2, desktop math-model, and May 14, 2026 Dual-Zero lines is in [`docs/hardening/51_SAM2_Lines_Review.md`](docs/hardening/51_SAM2_Lines_Review.md) and `experiments/sam2_review/`.  Original desktop sources are not in this repository.  The well-posed regulator is the current definition \(\varepsilon(n)=\omega_0(-1)^n n^{-n}\) with the symmetric average \(\operatorname{Reg}_2\); the SAM-2 ultrafilter entity and the May 2I / 12-bridge generation claims do not survive honest checks.  Nothing in that review derives the flux or the moduli, or changes the locked core.

The standalone Dual-Zero axiom, and a no-fitting selection test on magnetized \(T^2\), unfluxed \(T^2\), \(T^2/\mathbb{Z}_4\), a monopole sphere, and the Pati–Salam / CCM product, is in [`docs/hardening/52_DualZero_Axiom_Selection_Test.md`](docs/hardening/52_DualZero_Axiom_Selection_Test.md) and `experiments/dual_zero_axiom/`.  Nothing is selected without tuning.  The missing principle is unchanged.

Information-conserving Dual-Zero arithmetic (paired visible + exact residual) is in `dual_zero_arith/` and [`docs/hardening/53_DualZero_Information_Conserving_Arithmetic.md`](docs/hardening/53_DualZero_Information_Conserving_Arithmetic.md).  It removes rounding and truncation loss only, not modelling error.  A re-run of the numerical claims in the model lines is in [`docs/hardening/54_DualZero_Rerun_of_All_Models.md`](docs/hardening/54_DualZero_Rerun_of_All_Models.md) and `experiments/dual_zero_toe/`.  No genuine change: exact zeros stayed zeros, fits stayed fits, and no unique flux or moduli appeared.  Research targets for an authentic GUT and an authentic TOE are in [`ROADMAP_TOE_GUT.md`](ROADMAP_TOE_GUT.md).

Two-loop Pati–Salam unification with thresholds, and its spin-offs, are in `experiments/two_loop_pati_salam/` and docs 55–58: [`55`](docs/hardening/55_Two_Loop_Unification.md) (two-loop meeting at \(m_R\approx3.9\times10^{13}\), \(\Lambda\approx1.2\times10^{15}\) GeV — a zero-dof consistency check, not a prediction), [`56`](docs/hardening/56_Gauge_Group_From_Axioms.md) (PS/SM from assumed NCG axioms; a spectral regulator such as Dual-Zero cannot select them), [`57`](docs/hardening/57_Proton_Decay_PS.md) (baryon number exact in the spectral PS model; \(K_L\to\mu e\) passes), [`58`](docs/hardening/58_Higgs_and_Mass_Relations.md) (parameter-free top and Higgs relations miss: \(M_t\approx186\), \(m_H\approx168\) GeV).

The older script `code/reproduce_status_locked.py` mostly asserts hardcoded constants against themselves; do not treat it as evidence.

---

## Dual-Zero (definition)

- Generator $\varepsilon(n)=\omega_0(-1)^n n^{-n}$
- $\omega_0$ is an **input** until a derivation exists (it does not, as of November 2026)
- Dual average $\operatorname{Reg}_2$ on spectral mode data is a proposed regularisation, not a theorem about $\zeta(s)$

Canonical definition: [`docs/hardening/18_DualZero_Definition_Lock.md`](docs/hardening/18_DualZero_Definition_Lock.md)

---

## Authority table

| Topic | Document |
|-------|----------|
| Bottom line | `BOTTOM_LINE.md` |
| Public summary | `PUBLIC_STATUS_SUMMARY.md` |
| SSOT | `STATUS_CLAIMS_AND_RESIDUALS.md` |
| Core paper | `papers/SAM3_Core_Geometry_and_Spectral_Results.tex` |
| November 2026 audit | `docs/AUDIT_CORE_SOLIDIFICATION_NOV2026.md` |
| $\omega_0$, $G_N$ prefactor, Dirac | `docs/hardening/42_...` |
| Exact $E_0$, APS index $0$, unification attempts | `docs/hardening/44_...` |
| Almost-commutative product with CCM $F$ | `docs/hardening/45_...` |
| Singular tip $u\to 0$ | `docs/hardening/46_...` |
| Alternative geometries (exploratory) | `docs/hardening/47_...` |
| Pati–Salam product (exploratory) | `docs/hardening/48_...` |
| Missing-principle survey (exploratory) | `docs/hardening/49_...` |
| Further candidate tests (exploratory) | `docs/hardening/50_...` |
| SAM-2 / May-clone Dual-Zero review (exploratory) | `docs/hardening/51_...` |
| Dual-Zero axiom selection test (exploratory) | `docs/hardening/52_...` |
| Dual-Zero information-conserving arithmetic (exploratory) | `docs/hardening/53_...` |
| Dual-Zero re-run of model claims (exploratory) | `docs/hardening/54_...` |
| GUT / TOE research targets | `ROADMAP_TOE_GUT.md` |
| Dual-Zero (definition) | `docs/hardening/18_...` |
| Paper supersession | `papers/SUPERSESSION.md` |

**RH:** proposal only.  
**Unification, CKM, Higgs mass:** not derived from the conoid.  The product with the CCM finite triple $F$ is 2D unless an extra 4D (or $\Sigma^2$) factor is assumed; a spectator conoid does not change the CCM coupling ratios or the Higgs relation at $\Lambda$ (doc 45).

**Last update:** 23 November 2026 (America/Chicago).
