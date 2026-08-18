# SAM3-DualZero-Conoid

**Geometric / spectral research on a right conoid with Dual-Zero regulation**

---

## Start here (outsiders)

1. **[`PUBLIC_STATUS_SUMMARY.md`](PUBLIC_STATUS_SUMMARY.md)** — locked vs residual  
2. **[`docs/math_notes/`](docs/math_notes/)** — generations; metric + $G_N$  
3. **[`papers/SAM3_Core_Geometry_and_Spectral_Results.tex`](papers/SAM3_Core_Geometry_and_Spectral_Results.tex)** — modest paper  
4. **[`STATUS_CLAIMS_AND_RESIDUALS.md`](STATUS_CLAIMS_AND_RESIDUALS.md)** — SSOT  
5. **[`docs/hardening/18_DualZero_Definition_Lock.md`](docs/hardening/18_DualZero_Definition_Lock.md)** — **original Dual-Zero math**

**Core-first:** unification and RH narratives are secondary until core math is externally checked.

---

## Locked metric (mandatory)

$$
f(u,v)=\sqrt{u^2+4\ell_0^2\cos^2(2v)}
$$

($4\ell_0^2$ only — not $16\ell_0^2$.)

---

## Dual-Zero (novel — original math)

- Generator $\varepsilon(n)=\omega_0(-1)^n n^{-n}$ with geometric $\omega_0$
- Dual average $\operatorname{Reg}_2$ on **spectral mode data**
- Information-conserving alternative to hard UV cutoffs
- **Not** the claim $\mathrm{st}(n^{-n})\neq 0$

Canonical: [`docs/hardening/18_DualZero_Definition_Lock.md`](docs/hardening/18_DualZero_Definition_Lock.md)

---

## Reproduce

```bash
python code/reproduce_status_locked.py
python code/dual_zero_constructive.py
python code/production_channel_pipeline.py
```

---

## Authority table

| Topic | Document |
|-------|----------|
| Public summary | `PUBLIC_STATUS_SUMMARY.md` |
| Metric / ω₀ | `docs/hardening/35_...` |
| **Dual-Zero (original)** | **`docs/hardening/18_...`** + doc 39 |
| Pipeline | production channel pipeline |
| Paper supersession | `papers/SUPERSESSION.md` |
| Contradiction audit | `docs/AUDIT_CONTRADICTIONS.md` |

**RH:** proposal only.  
**Unification:** ~7% floor; percent-level not claimed.

**Last update:** August 18, 2026 (metric audit + Dual-Zero novelty lock).
