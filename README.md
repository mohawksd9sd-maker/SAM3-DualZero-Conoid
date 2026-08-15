# SAM3-DualZero-Conoid

**Geometric Unification of Gravity and the Standard Model**  
from a Right Conoid Spectral Triple with Dual-Zero Regulation

---

## Single source of truth

**[`STATUS_CLAIMS_AND_RESIDUALS.md`](STATUS_CLAIMS_AND_RESIDUALS.md)** — if anything conflicts, **STATUS wins**.

| Authority | Document |
|-----------|----------|
| **Metric (locked)** | $f=\sqrt{u^2+4\ell_0^2\cos^2(2v)}$ — [doc 35](docs/hardening/35_Metric_Curvature_Omega0_Authoritative.md) |
| Dual-Zero + constructive numerics | [doc 18](docs/hardening/18_DualZero_Definition_Lock.md), [doc 39](docs/hardening/39_DualZero_Constructive_and_Scheme_Comparison.md) |
| Production numbers | [doc 36](docs/hardening/36_Production_Numerical_Archive.md) |
| Pipeline maturity | [doc 40](docs/hardening/40_Numerical_Pipeline_Maturity.md) |
| Unification / cosmology residuals | [doc 41](docs/hardening/41_Unification_Cosmology_Residuals.md) |
| Lepton tests | [doc 38](docs/hardening/38_Lepton_Predictions_Oscillation_0nubb.md) |
| Paper supersession | [papers/SUPERSESSION.md](papers/SUPERSESSION.md) |

**Rule:** derivation only, no experimental tuning, no overclaim.  
**RH:** variational proposal **only** — not a proof.

---

## Regenerate / checks

```bash
pip install -r requirements.txt
python code/production_regenerate_locked.py
python code/dual_zero_constructive.py
python code/pipeline_maturity_checks.py
```

---

## Locked highlights

| Item | Status |
|------|--------|
| Metric tip coefficient | **$4\ell_0^2$ only** |
| $\omega_0\approx 0.927$ | Geometric |
| $G_N$, 3 generations, CKM $\theta_{12,23}$, $\phi=2\pi/5$ | Locked |
| $m_H$ | Class, not digit |
| Unification | ~$7\%$ floor baseline |
| APS production solver | Prototype (STATUS flag) |
| RH | Not a proof |

**Last update: August 2026** (metric lock, constructive Dual-Zero, pipeline maturity, residual discipline).
