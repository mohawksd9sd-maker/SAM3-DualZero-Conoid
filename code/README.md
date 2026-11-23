# SAM3 Code

Python geometry, Dirac discretisations, and verification utilities.

**Claim surface:** `STATUS_CLAIMS_AND_RESIDUALS.md` and the November 2026 core paper. Do not treat older “locked” phenomenological numbers as theorems.

## Preferred commands

```bash
# From repository root, after pip install -r requirements.txt
python code/core_reproducibility.py
pytest -q

# Hermitian Dirac known-answer tests (flat torus)
python code/aps_hermitian.py
```

`code/reproduce_status_locked.py` is a historical, largely tautological locker. It is not evidence.

## Core modules (November 2026)

```text
code/
├── core_geometry.py            # metric, C4, curvature, C0, exact E0(m)
├── aps_hermitian.py            # Hermitian Dirac; torus known answers
├── aps_disk_modes.py           # disk APS, Bessel known-answer attempts
├── aps_projection.py           # APS spectral projection (conoid + disk helpers)
├── aps_index_theorem.py        # product-collar APS index of the truncated conoid is 0
├── omega0_search.py            # search for a derivation of ω0; none found
├── gn_prefactor_schemes.py     # scheme table for α in G_N=α ℓ0²
├── unification_derivation_attempts.py  # honest attempts; all failed
├── almost_commutative_product.py # conoid × CCM finite triple F; KO-dimensions
├── conoid_heat_kernel.py         # area, ∫K=−2π, Gauss–Bonnet identity
├── ccm_oneloop_rge.py            # CC2010 one-loop running of CCM boundary conditions
├── u1_twist_and_tip.py           # natural flux is −1, not in (2,3]; tip geometry
├── core_reproducibility.py     # one-script reproduction of the core paper
├── dirac_conoid_aps.py         # LEGACY: not a Dirac operator (see header)
├── newton_constant_fit.py      # convention display; not a fit
├── volume_regularisation.py    # older Riemann sums; C0 band withdrawn
├── verification/               # includes the tautology demo and identification test
└── ...
```

## Policy

- Metric tip coefficient is 4, not 16.
- $\omega_0=0.927$ is an *input*, not a derived output (doc 42).
- Do not use spectra from `dirac_conoid_aps.py` as APS evidence.
- Do not retune leftover phenomenological constants to experiment and call that a derivation.
