# SAM3 — Public Status Summary

**Last update:** August 2026  
**Pure math:** [`docs/math_notes/15_Pure_Math_Completion_Status.md`](docs/math_notes/15_Pure_Math_Completion_Status.md)

---

## Locked

| Result | Statement |
|--------|-----------|
| Metric | $f=\sqrt{u^2+4\ell_0^2\cos^2(2v)}$ |
| Symmetry | $C_4$ exact |
| 3 generations | APS + channel isolation + L4/S′ package |
| $G_N$ | $\propto\ell_0^2$ proved; prefactor convention-locked |

---

## Pure math residuals (post XXV–XXVIII)

| Item | Status |
|------|--------|
| Conjecture S | **Controlled** (Thm S′) |
| $H_{\mathrm{tip}}$ | **Quantitative bounds**; 3+0 isolation |
| Production numerics | **Channel pipeline** (`code/production_channel_pipeline.py`) |
| External edge-APS review | Still needed |
| Full 60-element $A_5$ matrices | Refinement only |
| Lorentzian | Residual |

---

## Run

```bash
python code/production_channel_pipeline.py  # expect ok: true
```
