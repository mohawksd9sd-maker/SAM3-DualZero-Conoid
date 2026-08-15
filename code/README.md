# SAM3 Code

Python prototypes and verification utilities for the SAM3-DualZero-Conoid framework.

**Claim surface:** continuum residual and locked geometric numbers live in `docs/hardening/` and `STATUS_CLAIMS_AND_RESIDUALS.md`.

## Layout (Section 2 update)

```text
code/
├── sam3_geometry_constants.py     # Pure-geometry source of truth (omega0=0.927)
├── master_verification_pipeline.py
├── full_2d_dirac_conoid.py         # PROTOTYPE Dirac (not production APS)
├── overlap_integrals.py
├── lorentzian_spectral_action.py
├── lorentzian_dynamical_gravity.py
├── newton_constant_fit.py
├── sam3_demo.py
├── zeta_stationarity_enhanced.py
├── verification/
│   ├── dirac_conoid_verification.py
│   └── zeta_stationarity.py
└── visualization/
    └── ...
```

## Preferred commands

```bash
# From repository root
python code/master_verification_pipeline.py

# Dirac prototype only
python code/full_2d_dirac_conoid.py
```

## Critical policy

- **`omega0 = 0.927` geometric only.** Legacy defaults near `0.97` are forbidden.
- Dirac script is a **prototype**. Production APS roadmap: `docs/hardening/23_Numerical_Production_Readiness.md`.
- Do not retune locked angles or masses to experiment inside these scripts.
