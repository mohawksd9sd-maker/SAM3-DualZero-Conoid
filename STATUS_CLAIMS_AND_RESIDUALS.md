# SAM3 — Claims vs Residuals (SINGLE SOURCE OF TRUTH)

**Date:** 23 November 2026 (America/Chicago)  
**Role:** Executive claim map. If any paper or note conflicts with this file, **this file wins**.  
**Rule:** Derivation only. No invented results. Unproven statements are labelled conjecture, heuristic, convention, or numerical observation. Null results stay null.

The August 2026 edition of this file listed several phenomenological numbers as “locked” or “high confidence.” Those listings were stronger than the evidence and are **superseded** by the tables below. The modest core paper `papers/SAM3_Core_Geometry_and_Spectral_Results.tex` (November 2026) is the written mathematics that this file summarises.

### Authority index

| Topic | File |
|-------|------|
| Core paper (current) | [`papers/SAM3_Core_Geometry_and_Spectral_Results.tex`](papers/SAM3_Core_Geometry_and_Spectral_Results.tex) |
| November 2026 audit | [`docs/AUDIT_CORE_SOLIDIFICATION_NOV2026.md`](docs/AUDIT_CORE_SOLIDIFICATION_NOV2026.md) |
| ω₀, 64π/45, Dirac status | [`docs/hardening/42_Omega0_GN_Prefactor_and_Dirac_Status.md`](docs/hardening/42_Omega0_GN_Prefactor_and_Dirac_Status.md) |
| Metric convention (coeff.\ 4) | [`docs/hardening/35_Metric_Curvature_Omega0_Authoritative.md`](docs/hardening/35_Metric_Curvature_Omega0_Authoritative.md) — **$f=\sqrt{u^2+4\ell_0^2\cos^2(2v)}$ only**; the ω₀ formula in that file is **not derived** (see doc 42) |
| Dual-Zero *definition* | [`docs/hardening/18_DualZero_Definition_Lock.md`](docs/hardening/18_DualZero_Definition_Lock.md) |
| Reproduction | `python code/core_reproducibility.py` and `pytest -q` |
| Papers supersession | [`papers/SUPERSESSION.md`](papers/SUPERSESSION.md) |

---

## 1. Proved from the locked embedding

| Result | Status |
|--------|--------|
| Induced metric $f=\sqrt{u^2+4\ell_0^2\cos^2(2v)}$ (coefficient 4, not 16) | **Proposition** |
| Exact $C_4$ isometry $v\mapsto v+\pi/2$ | **Proposition** |
| $A_5$ is not a metric isometry of $f$ | **Proposition** (counterexample) |
| Four tip nodes $v=\pi/4+k\pi/2$ | **Proposition** |
| $K=-4\ell_0^2\cos^2(2v)/f^4$, so $\|K\|_{\max}=1/(4\ell_0^2)$ | **Proposition** |
| $C_0=\lim(\int_0^U I(u)\,du-2\pi\log U)$ exists | **Proposition** |
| $E_0(m_2)>E_0(m_1)$ for $m_2>m_1\ge 1$ (unique SA extensions); also for $m_1=0$ on a fixed Dirichlet/APS realization | **Theorem** |
| $E_0(2)<E_0(3)$ on those realizations | **Corollary** |
| Weyl: $m=0$ limit-circle, $\|m\|\ge 1$ limit-point ($\kappa=m^2$ vs $3/4$) | **Proposition** (standard) |

---

## 2. Numerical observations (reproduced)

| Quantity | Value | Notes |
|----------|-------|--------|
| $C_0$ (unit metric $\ell_0=1$) | $\approx 4.3551723$ | $C_0(1000)\approx 4.3551745$, $C_0(4000)\approx 4.3551723$. The older band $4.43$–$4.45$ **does not reproduce**. |
| Dirichlet $E_0(m)$ on $(0,20)$, $N=400$ | $0.02467,\ 0.03980,\ 0.06795,\ 0.10339$ for $m=0,1,2,3$ | Consistent with monotonicity; $m=0$ is cutoff-dependent. |
| Hermitian Dirac on the antiperiodic flat torus, $N=24$ | $\max\|\lambda-\lambda_{\mathrm{exact}}\|\approx 0.00202$ | Lowest $\|\lambda\|=\sqrt{1/2}$. |
| Convergence slope $\log\mathrm{err}/\log N$ | $\approx -1.995$ | $N\in\{8,12,16,24,32\}$; consistent with second-order differences. |
| Legacy real assembly + $\tfrac12(D+D^T)$ | **fails** the torus known-answer test | Not a Dirac operator. |

Reproduce: `python code/core_reproducibility.py` (writes `reproducibility/core_results.json`) and `pytest -q`.

---

## 3. Definitions and conventions (not theorems)

| Item | Status |
|------|--------|
| Dual-Zero generator $\varepsilon(n)=\omega_0(-1)^n n^{-n}$ | **Definition** |
| Twelve-bridge spacing $D=2\pi/12$ | **Convention / discrete labelling** |
| $G_N=\alpha\ell_0^2$ | **Structural** (spectral action $a_2$) |
| Recorded normalisation $G_N=64\pi\ell_0^2/45$ | **Convention lock**, equivalent to fixing $\mathcal{N}=45/(1024\pi^2)$. **Not scheme-free, not independently derived.** |
| Constructive finite-$N$ Dual-Zero for numerics | **Policy**, not a uniqueness theorem |

---

## 4. Not established (open, heuristic, or withdrawn as locks)

| Item | Honest status |
|------|----------------|
| $\omega_0\approx 0.927$ and the exponent $4/13$ in $\omega_0=(R_{\mathrm{curv}}/D)^{4/13}$ | **Not derived.** Natural $R\in\{1/\|K\|_{\max},\,1/\sqrt{\|K\|_{\max}},\,\ell_0,\,2\ell_0\}$ all give $\omega_0>1.22$, not $0.927$. The value $0.927$ would need $R\approx 0.409\,\ell_0$, which is not a unique geometric prescription. See doc 42. |
| Exactly three chiral generations / APS index 3 | **Conjecture.** The soft block $\{0,1,2\}$ is a radial-model heuristic ($\cos(2v)$ and $C_4$). No continuum index is computed. |
| $\eta_{12}\approx 0.861$, $\eta_{13}\approx 0.544$, $\eta_{23}\approx 0.479$ | **Not derived** in the core. Earlier “locks” are withdrawn. |
| $\theta_{12}\approx 12.85^\circ$, $\theta_{23}\approx 2.36^\circ$, $\phi=2\pi/5$, $\delta_{\mathrm{CKM}}$ | **Not derived.** Some scripts define $\theta_{12}:=\eta_{12}\cdot\pi/12$ and then “check” the same relation. |
| $m_H$ in $124$–$127\,\mathrm{GeV}$ | **Not derived.** At least one script inserts $125\,\mathrm{GeV}$ by hand. |
| Gauge unification, VL_Q, cosmological constant, PMNS digits | **Open / not claimed.** A ~$7\%$ unification “floor” is not a theorem. |
| Production APS index on the conoid | **Not proved.** Hermitian discretisation is verified on the *flat torus*. Conoid + APS penalty is truncated numerics. |
| Riemann hypothesis | **Variational proposal only — not a proof.** A non-circular identification test found **no evidence** that Dual-Zero / information-current critical points match zeta zeros (`RESULTS_zeta_identification.md`). |
| Identification of SAM-3 with the Standard Model | **Not claimed.** |

---

## 5. Circular or misleading scripts (do not cite as evidence)

| Script | Problem |
|--------|---------|
| `code/reproduce_status_locked.py` | Echoes hardcoded constants and asserts them against themselves. |
| `code/newton_constant_fit.py` (old) | Solved $G_{\mathrm{theory}}(\ell_0)=G_{\mathrm{obs}}$ and reported an exact match. Now a convention display only. |
| `code/zeta_stationarity.py`, `zeta_stationarity_enhanced.py` | Tautological; see `code/verification/README_stationarity_flaw.md`. |
| `code/dirac_conoid_aps.py` | Symmetrised real assembly is not a Dirac operator. Use `code/aps_hermitian.py`. |
| `code/volume_regularisation.py` | Riemann sums produced the withdrawn $C_0$ band $4.43$–$4.45$. |

---

## 6. Riemann Hypothesis discipline (mandatory)

- STATUS demotes RH to a **variational / information-current proposal**.
- Older `papers/` language that states or implies a completed proof is **superseded**.
- Spectral zeta of $D$ is not a proof of the classical RH.
- Null identification results stay null.

---

## 7. Metric discipline (mandatory)

- Only the $4\ell_0^2$ tip coefficient is allowed in active claims.
- $16\ell_0^2$ forms are historical/superseded.

---

## 8. Supersession

`papers/` is historical except the November 2026 core paper. Conflicting claims of a derived $64\pi/45$, a derived $\omega_0$ or $4/13$, a computed APS generation count, digit $m_H$, percent-level unification-as-fact, RH-as-proof, the $C_0$ band $4.43$–$4.45$, or a $16\ell_0^2$ metric yield to this STATUS file and the core paper.

---

*SSOT — November 2026 solidification. No tuning, no overclaim.*
