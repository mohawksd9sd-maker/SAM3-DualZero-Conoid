# Papers directory — SUPERSESSION BANNER

**Effective:** 23 November 2026 (America/Chicago), extending the 18 August 2026 metric/RH audit.  
**Authority:** [`STATUS_CLAIMS_AND_RESIDUALS.md`](../STATUS_CLAIMS_AND_RESIDUALS.md) + the current core paper.

History is retained. Conflicting claims are withdrawn, not deleted.

---

## Rule

Every `.tex` file here is historical or expanded source unless listed as current core.  
**STATUS + the November 2026 core paper supersede** all conflicting claims, including older language *in this file*.

---

## Current core paper (modest)

- [`SAM3_Core_Geometry_and_Spectral_Results.tex`](SAM3_Core_Geometry_and_Spectral_Results.tex) — **November 2026 revision**

The August 2026 core draft is superseded on: the $C_0$ band $4.43$–$4.45$; an incomplete monotonicity argument; and any reading of “three light channels” or $G_N=\alpha\ell_0^2$ as stronger than the labelled statements now in the file.

As of 23 November 2026 the APS index of the *untwisted* Dirac operator on the truncated conoid (product collar, bounding spin structure) is a theorem and equals $0$; older language that leaves “three generations as an APS index” merely open, or that treats it as a locked claim, is superseded by STATUS and doc 44.  The singular-tip limit is not covered by that theorem.

---

## Metric lock (mandatory)

$$
f=\sqrt{u^2+4\ell_0^2\cos^2(2v)}
$$

Coefficient **4 only**. Any `16\ell_0` form is an error.

**August 18, 2026 audit:** historical papers scanned; metric-16 occurrences corrected; supersession banners added. See [`docs/AUDIT_COMPLETE_METRIC_RH.md`](../docs/AUDIT_COMPLETE_METRIC_RH.md).

---

## Specifically superseded language

| Older language | Superseded by |
|----------------|---------------|
| $f^2=u^2+16\ell_0^2\cos^2(\cdot)$ | **$4\ell_0^2$ only** |
| $C_0\approx 4.43$–$4.45$ or $C_0\approx 4.3551723$ as a mere decimal | **$C_0=2\pi\ln 2$** (theorem, unit metric) |
| $G_N=64\pi\ell_0^2/45$ as a scheme-free or independently derived constant | $G_N=\alpha\ell_0^2$ structural; $64\pi/45$ is a **convention lock** |
| $\omega_0=(R/D)^{4/13}\approx 0.927$ as a derived output | **Not derived**; $\omega_0$ is an input until a derivation exists |
| Exactly three chiral generations / APS index 3 as a theorem for the *untwisted* truncated conoid | **Refuted**: the product-collar APS index is $0$ (doc 44, Theorem in the core paper).  Index $3$ needs an underived Falomir flux.  The singular tip $a\to 0$ remains open and is not an index-3 theorem.  Soft block $\{0,1,2\}$ is a radial-model heuristic |
| $\eta_{ij}$, CKM/PMNS angles, $m_H$ class $124$–$127\,\mathrm{GeV}$ as locked geometric results | **Not derived** in the core |
| Exact $m_H=125.1$ or $126.2$ GeV as theorem | Not claimed |
| Percent-level unification as fact | Not claimed |
| RH proved / theorem | **Proposal only**; identification tests in this repo were **null** |
| $A_5$ isometries of the continuum metric | **False**; $C_4$ only |
| Full SM derived in foundations files | Not claimed in the core paper |
| Product of the 2D conoid with $F$ as a “dimensional lift” to 4D Einstein gravity, or KO-dimension 4 for $F$ (Paper 09) | **Incorrect.** $F$ has KO-dimension 6 (CCM2007).  Conoid $\times F$ is 2-dimensional.  See doc 45. |
| Spectra from `code/dirac_conoid_aps.py` as APS evidence | Legacy assembly is **not** a Dirac operator; use `code/aps_hermitian.py` |
| Ultrafilter required for numerics | Constructive finite-$N$ (policy) |
| August 2026 STATUS “high / locked” listings for $\omega_0$, $G_N$ prefactor, $\eta$, angles, $m_H$ | November 2026 STATUS |

---

## Banner (on corrected or stub papers)

```tex
% SUPERSEDED where conflicting: STATUS_CLAIMS_AND_RESIDUALS.md (Nov 2026)
%   and papers/SAM3_Core_Geometry_and_Spectral_Results.tex
% LOCKED metric: coefficient 4, not 16.
% RH = proposal only. A5 is NOT a metric isometry (C4 only).
% C0 ≈ 4.3551723, not 4.43--4.45. 64π/45 and ω0 are not independent derivations.
```

Papers 11 and 15 (RH), the flagship stub, and other historical `SAM3_Paper_0*.tex` files remain in the tree as history. They are not current claims.

---

*Supersession — 18 August 2026 metric/RH audit; 23 November 2026 solidification.*
