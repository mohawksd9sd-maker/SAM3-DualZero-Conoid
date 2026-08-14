# SAM3 Code

Python prototypes and verification utilities for the SAM3-DualZero-Conoid framework.

**Claim surface:** continuum residual and locked geometric numbers are documented in `docs/hardening/` and `STATUS_CLAIMS_AND_RESIDUALS.md`. Scripts here are supporting tools; several remain prototypes.

## Layout (after Fix 5 cleanup)

```text
code/
├── master_verification_pipeline.py   # Frozen archive writer (preferred entry point)
├── full_2d_dirac_conoid.py            # Prototype radial/angular Dirac
├── overlap_integrals.py              # Bridge projector overlaps (prototype)
├── lorentzian_spectral_action.py
├── lorentzian_dynamical_gravity.py
├── newton_constant_fit.py
├── sam3_demo.py
├── zeta_stationarity_enhanced.py
├── verification/
│   ├── dirac_conoid_verification.py  # Dirac verification framework (promoted)
│   ├── zeta_stationarity.py          # Information-current / RH-related numerics
│   └── (optional stubs)
└── visualization/
    ├── conoid_bridges.py
    ├── black_hole_spectral_triple.py
    ├── overlap_integrals.py
    └── sam3_v4.21_pipeline.py
```

## Preferred commands

```bash
# From repository root
python code/master_verification_pipeline.py

# Dirac prototype
python code/full_2d_dirac_conoid.py
```

## Notes

- Nested path `code/verification/code/verification/` was a packaging artifact and is removed; unique content was promoted to `code/verification/`.
- Duplicate copies of top-level scripts under `verification/` were removed where identical.
- Continuum residual $<10^{-3}$ and gap $\to 0$ claims are locked in `docs/hardening/10_Continuum_Dirac_Residual_Lock.md`; they are not automatically reproduced by every prototype script.
