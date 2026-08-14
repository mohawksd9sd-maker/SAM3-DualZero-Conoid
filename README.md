# SAM3-DualZero-Conoid

**Geometric Unification of Gravity and the Standard Model**  
from a Right Conoid Spectral Triple with Dual-Zero Hyperreal Regulation

---

## Overview

SAM3 (Spectral Action Model 3) is a minimal noncommutative geometric framework that derives **gravity together with the architecture of the Standard Model** from a single explicit geometric object:

> An infinite right conoid equipped with twelve binary-icosahedral bridges and regulated by a Dual-Zero hyperreal construction.

The model is controlled by **one fundamental free parameter**:

- **`ℓ₀`** — anchored to the top-quark mass.

The Dual-Zero regulator strength **`ω₀`** is **geometrically derived** from the conoid:

$$
\omega_0 = \left( \frac{R_{\rm curvature}}{D_{\rm bridge}} \right)^{4/13} \approx 0.927
$$

where \( R_{\rm curvature} \) is the local curvature radius along the conoid axis, and \( D_{\rm bridge} \) is the average angular spacing of the 12 icosahedral bridges.

---

## Key Results & Current Status (Hardened — August 2026)

| Observable | Status | Notes |
|------------|--------|-------|
| **Newton's Constant** | \( G_N = 64\pi \ell_0^2 / 45 \) | Locked from Seeley–DeWitt \(a_2\) |
| **Chiral Generations** | Exactly 3 | Index + continuum gap \(\to 0\) under APS |
| **Cabibbo \( \theta_{12} \)** | \( \approx 12.85^\circ \) | \( \eta_{12}\times\pi/12 \); continuum defect + \( \mathcal{A}_F \) |
| **CKM \( \theta_{23} \)** | \( \approx 2.36^\circ \) | **Locked** — Casimir-weighted defect (no tuning) |
| **CKM \( \delta \) / Jarlskog** | \( \phi=2\pi/5 \); \( \delta\sim 70^\circ \), \( J\sim 3\times 10^{-5} \) | **Locked** phase from \( E_3 \) + \( I^2=-1 \) + tip orientation |
| **Quark mass ratios** | Good (c, s, d); light up resolved | Radial + Dual-Zero; \( \kappa_u/\kappa_d=1/2 \) |
| **Continuum Dirac residual** | \( <10^{-3} \) | 4th-order FD; gap \( \propto 1/u_{\rm max}\to 0 \) |
| **PMNS / \( m_{\beta\beta} \)** | Predictive; large \( \delta_{\rm PMNS} \) | Same \( \phi=2\pi/5 \) in lepton sector |
| **Higgs mass** | 125 GeV class (\( \approx 124\)–\(127\) GeV band) | Geometric \(a_4\); not digit-tuned |
| **Gauge unification** | Geometric floor **~7%** | O(10) KK thresholds; **percent-level not claimed** |
| **Cosmological constant** | Mechanism present | Magnitude lock residual |
| **Riemann Hypothesis** | Variational proposal | **Not** a proof — residual discipline |

Authoritative maps:
- **[STATUS_CLAIMS_AND_RESIDUALS.md](STATUS_CLAIMS_AND_RESIDUALS.md)** — executive residual map
- **[docs/hardening/](docs/hardening/00_INDEX.md)** — full lock notes (Priorities 1–6 + secondary 1–3)
- **[docs/hardening/16_Frozen_Numerical_Archive.md](docs/hardening/16_Frozen_Numerical_Archive.md)** — frozen number archive

**Rule in force:** derivation only, no experimental tuning, no overclaim.

---

## Major Advances (Post-v4.26 Hardening)

1. **Continuum defect operator** — locus = tip curvature max, width \( = a\Delta\theta \); \( \eta_{12}\approx 0.861 \), \( \eta_{13}\approx 0.544 \), \( \eta_{23}\approx 0.479 \).
2. **Geometric Cabibbo** — \( \theta_{12}\approx\eta_{12}\times(\pi/12) \) via \( \mathcal{A}_F \) (\( \mathbb{H} \) vs \( \mathbb{C} \)).
3. **Casimir-weighted \( \theta_{23} \)** — bulk \( C_g \) + tip potential fixed by same curvature / \( \omega_0 \).
4. **CP phase \( \phi=2\pi/5 \)** — unique from 2I-module \( E_3 \), quaternionic relation, tip orientation; applies to quarks and leptons.
5. **APS + residual control** — gap \( \to 0 \); continuum residual \( <10^{-3} \) at moderate resolution.
6. **Explicit \( D_F \) + complex CKM** — magnitudes and phase geometric outputs.
7. **Unification demotion** — ~7% geometric floor; no percent-level claim.
8. **Light up mass** — closed by intertwiner norm \( \kappa_u/\kappa_d=1/2 \).
9. **Claims vs residuals discipline** — older paper language superseded where it conflicts with this layer.

---

## Foundational Components

1. **Right Conoid Geometry** — Infinite discrete spectrum.
2. **Binary Icosahedral Bridges** (12) — Three chiral generations.
3. **Dual-Zero Hyperreal Regulation** — Information-conserving regularization with geometrically derived \( \omega_0 \).
4. **Spectral Action** — Gravity, Higgs sector, and Standard Model gauge fields.
5. **Almost-commutative finite algebra** \( \mathcal{A}_F = \mathbb{C} \oplus \mathbb{H} \oplus M_3(\mathbb{C}) \) — Up/down distinction and CP structure.

---

## Repository Structure

```bash
SAM3-DualZero-Conoid/
├── docs/hardening/  # Authoritative lock notes (Priorities 1–6 + secondary)
├── papers/          # LaTeX sources (May 2026; superseded where noted)
├── figures/         # Plots and geometry visuals
├── code/            # Python verification & visualization
├── STATUS_CLAIMS_AND_RESIDUALS.md
├── requirements.txt
├── LICENSE
└── README.md
```

> **Note:** Claims in older `papers/` (Flagship, v4.22, Papers 08/19/22, etc.) that conflict with `docs/hardening/` — especially exact \( m_H=125.1 \) GeV, percent-level unification, and RH-as-proof language — are **superseded** by the August 2026 hardening layer.

---

## Citation

```bibtex
@misc{sam3_hardened_2026,
  author       = {Shawn Dykes},
  title        = {SAM3-DualZero-Conoid: Geometric Unification from a Right Conoid Spectral Triple (Hardened Status)},
  year         = {2026},
  howpublished = {GitHub repository},
  url          = {https://github.com/mohawksd9sd-maker/SAM3-DualZero-Conoid},
  note         = {In collaboration with Grok (xAI); August 2026 hardening locks for continuum defect, CKM angles/phase, residual control, and calibrated residuals},
  institution  = {Independent}
}
```

---

## Contact & Collaboration

Open to discussions, independent verification, peer review, and collaboration.  
Feel free to open an Issue or start a Discussion.

Built with curiosity and rigor.  
**Last major status update: August 2026** (Priorities 1–6 + secondary 1–3 locked).
