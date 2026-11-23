# SAM3-DualZero-Conoid

**Geometric / spectral research on a right conoid with Dual-Zero regularisation**

Honesty rule: unproven statements are labelled as such. Null results stay null.

---

## Start here (outsiders)

1. **[`PUBLIC_STATUS_SUMMARY.md`](PUBLIC_STATUS_SUMMARY.md)** — proved vs numerical vs not derived
2. **[`papers/SAM3_Core_Geometry_and_Spectral_Results.tex`](papers/SAM3_Core_Geometry_and_Spectral_Results.tex)** — current core paper (November 2026)
3. **[`STATUS_CLAIMS_AND_RESIDUALS.md`](STATUS_CLAIMS_AND_RESIDUALS.md)** — SSOT
4. **[`docs/AUDIT_CORE_SOLIDIFICATION_NOV2026.md`](docs/AUDIT_CORE_SOLIDIFICATION_NOV2026.md)** — audit of claims vs evidence
5. **[`docs/hardening/18_DualZero_Definition_Lock.md`](docs/hardening/18_DualZero_Definition_Lock.md)** — Dual-Zero as a definition

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
- Flat-torus Hermitian Dirac, $N=24$: $\max|\lambda-\lambda_{\mathrm{exact}}|\approx 0.00202$, convergence slope $\approx-1.995$
- $G_N=64\pi\ell_0^2/45$ is a **convention lock**, not an independent derivation
- $\omega_0\approx 0.927$ and the exponent $4/13$ are **not derived**

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
| Public summary | `PUBLIC_STATUS_SUMMARY.md` |
| SSOT | `STATUS_CLAIMS_AND_RESIDUALS.md` |
| Core paper | `papers/SAM3_Core_Geometry_and_Spectral_Results.tex` |
| November 2026 audit | `docs/AUDIT_CORE_SOLIDIFICATION_NOV2026.md` |
| $\omega_0$, $G_N$ prefactor, Dirac | `docs/hardening/42_...` |
| Exact $E_0$, APS index $0$, unification attempts | `docs/hardening/44_...` |
| Dual-Zero (definition) | `docs/hardening/18_...` |
| Paper supersession | `papers/SUPERSESSION.md` |

**RH:** proposal only.  
**Unification, CKM, Higgs mass:** not derived in the core.  Honest attempts to derive a gauge group, mass ratios, $\omega_0$, $\alpha$, or coupling unification from the locked geometry all failed (doc 44).

**Last update:** 23 November 2026 (America/Chicago).
