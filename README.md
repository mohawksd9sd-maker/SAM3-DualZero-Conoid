# SAM3-DualZero-Conoid

**Geometric Unification of Gravity and the Standard Model**  
from a Right Conoid Spectral Triple with Dual-Zero Hyperreal Regulation

---

## Single source of truth

**[`STATUS_CLAIMS_AND_RESIDUALS.md`](STATUS_CLAIMS_AND_RESIDUALS.md)** — executive claims vs residuals.  
If anything conflicts with STATUS, **STATUS wins**.

| Authority | File |
|-----------|------|
| Metric / curvature / ω₀ | [`docs/hardening/35_Metric_Curvature_Omega0_Authoritative.md`](docs/hardening/35_Metric_Curvature_Omega0_Authoritative.md) |
| Dual-Zero definition | [`docs/hardening/18_DualZero_Definition_Lock.md`](docs/hardening/18_DualZero_Definition_Lock.md) |
| Production numbers + error budgets | [`docs/hardening/36_Production_Numerical_Archive.md`](docs/hardening/36_Production_Numerical_Archive.md) |
| Regulator comparison | [`docs/hardening/37_Regulator_Comparison_DZ_vs_HeatKernel_Zeta.md`](docs/hardening/37_Regulator_Comparison_DZ_vs_HeatKernel_Zeta.md) |
| Lepton oscillation / 0νββ | [`docs/hardening/38_Lepton_Predictions_Oscillation_0nubb.md`](docs/hardening/38_Lepton_Predictions_Oscillation_0nubb.md) |
| Full hardening index | [`docs/hardening/00_INDEX.md`](docs/hardening/00_INDEX.md) |
| Papers supersession | [`papers/SUPERSESSION.md`](papers/SUPERSESSION.md) |

**Rule:** derivation only, no experimental tuning, no overclaim.

---

## Key locked results (summary)

| Observable | Status |
|------------|--------|
| $G_N = 64\pi\ell_0^2/45$ | Locked ($a_2$) |
| 3 chiral generations | Locked (APS index) |
| $\omega_0\approx 0.927$ | Geometric (not a fit) |
| $\theta_{12}\approx 12.85^\circ$, $\theta_{23}\approx 2.36^\circ$ | Locked |
| $\phi=2\pi/5$ CP structure | Locked |
| $m_H$ | 125 GeV **class** (not digit) |
| Gauge unification | ~$7\%$ floor baseline; research paths separate |
| RH | Proposal **not** proof |
| $\delta_{\rm PMNS}$ | Large band $200^\circ$–$270^\circ$ |

---

## Regenerate locked numbers

```bash
pip install -r requirements.txt
python code/production_regenerate_locked.py
```

---

## Repository layout

```
├── STATUS_CLAIMS_AND_RESIDUALS.md   # SSOT
├── docs/hardening/                  # Locks 01–38
├── papers/                          # Historical LaTeX (see SUPERSESSION.md)
├── code/                            # Verification scripts
├── README.md
└── LICENSE
```

---

## Citation

```bibtex
@misc{sam3_hardened_2026,
  author       = {Shawn Dykes},
  title        = {SAM3-DualZero-Conoid (Hardened Status)},
  year         = {2026},
  howpublished = {GitHub},
  url          = {https://github.com/mohawksd9sd-maker/SAM3-DualZero-Conoid},
  note         = {STATUS file is authoritative for claims vs residuals}
}
```

**Last major update: August 2026** (docs 35–38 + STATUS SSOT + paper supersession).
