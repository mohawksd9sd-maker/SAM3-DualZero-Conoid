# SAM3-DualZero-Conoid

**Geometric / spectral research on a right conoid with Dual-Zero regulation**

---

## Start here (outsiders)

1. **[`PUBLIC_STATUS_SUMMARY.md`](PUBLIC_STATUS_SUMMARY.md)** — locked vs residual in one screen  
2. **[`docs/math_notes/`](docs/math_notes/)** — three generations (APS+2I); metric + $G_N$  
3. **[`papers/SAM3_Core_Geometry_and_Spectral_Results.tex`](papers/SAM3_Core_Geometry_and_Spectral_Results.tex)** — modest paper draft  
4. **[`STATUS_CLAIMS_AND_RESIDUALS.md`](STATUS_CLAIMS_AND_RESIDUALS.md)** — full SSOT

**Core-first policy:** unification and Riemann-hypothesis narratives are **secondary** until the two mathematical notes are externally checked.

---

## Locked metric (mandatory)

$$
f(u,v)=\sqrt{u^2+4\ell_0^2\cos^2(2v)}
$$

($4\ell_0^2$ only — not $16\ell_0^2$.)

---

## Reproduce

```bash
python code/reproduce_status_locked.py
python code/dual_zero_constructive.py
python code/pipeline_maturity_checks.py
```

---

## Authority table

| Topic | Document |
|-------|----------|
| Public summary | `PUBLIC_STATUS_SUMMARY.md` |
| Metric / ω₀ | `docs/hardening/35_...` |
| Dual-Zero + schemes | docs 18, 37, 39 |
| Pipeline maturity | doc 40 |
| Paper supersession | `papers/SUPERSESSION.md` |
| Expert outreach draft | `docs/outreach/Expert_Outreach_Draft.md` |

**RH:** proposal only — not a proof.  
**Unification:** ~7% floor baseline; percent-level not claimed.

**Last update:** August 2026 (core math notes + public summary + modest paper).
