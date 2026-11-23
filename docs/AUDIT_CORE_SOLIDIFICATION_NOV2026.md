# Audit: core geometry and spectral claims (23 November 2026)

This audit was run against the core paper, STATUS, PUBLIC_STATUS, the README, and the core code, with symbolic and numerical recomputation (`sympy`, `scipy`, `numpy`). Nothing here is an experimental fit. Unproven claims are labelled. Null results stay null.

Authoritative write-up of the mathematics that survive the audit: `papers/SAM3_Core_Geometry_and_Spectral_Results.tex` (November 2026) and `STATUS_CLAIMS_AND_RESIDUALS.md`.

## 1. What is correct and follows from the definitions

| Claim | Verdict |
|-------|---------|
| Locked embedding $r=(u\cos v,u\sin v,\ell_0\sin(2v))$ induces $f=\sqrt{u^2+4\ell_0^2\cos^2(2v)}$ | **True.** Sympy: $g_{uu}=1$, $g_{uv}=0$, $g_{vv}=u^2+4\ell_0^2\cos^2(2v)$. The coefficient is 4, not 16. |
| Exact $C_4$ isometry $v\mapsto v+\pi/2$ | **True** ($f$ is invariant). |
| $A_5$ is an isometry of the metric | **False.** $f(u,v)\neq f(u,v+2\pi/5)$ already at $(0.3,0.2,1)$. |
| Four tip nodes $v=\pi/4+k\pi/2$ | **True.** |
| $K=-4\ell_0^2\cos^2(2v)/f^4$ | **True** (symbolic identity $K=-f_{uu}/f$). $\|K\|_{\max}=1/(4\ell_0^2)$. |
| Weyl: $m=0$ limit-circle, $|m|\ge 1$ limit-point | **True** for $\kappa=m^2$ compared with $3/4$. |
| $E_0(m)$ strictly increases in $m$ | **True** with a complete variational (form) argument. The August core-paper proof only tested $H_{m_2}$ on a ground state of $H_{m_1}$, which gives the wrong inequality direction; the result is nevertheless correct. Caveat: $m=0$ needs a fixed self-adjoint realization. |
| $C_0$ exists | **True.** $I(u)=2\pi/u+O(u^{-3})$ at $\ell_0=1$. |

## 2. Numbers that do, and do not, reproduce

| Quantity | Earlier claim | Recomputed | Verdict |
|----------|---------------|------------|---------|
| $C_0$ | $4.43$–$4.45$ (Riemann sums in `volume_regularisation.py`) | $C_0(200)=4.355231$, $C_0(400)=4.355187$, $C_0(1000)=4.355175$, $C_0(4000)=4.3551723$ | **Old band does not reproduce.** Use $C_0\approx 4.3551723$. |
| $G_N=64\pi\ell_0^2/45$ | “Locked” as if derived | Equivalent to fixing $\mathcal{N}=45/(1024\pi^2)$ (notes 09, 16, 23) | **Convention lock, not a test.** `newton_constant_fit.py` previously solved $G(\ell_0)=G_{\mathrm{obs}}$ and reported an exact match — tautological. |
| $\omega_0=(R/D)^{4/13}\approx 0.927$, $D=2\pi/12$ | “High / geometric only” | $1/\|K\|_{\max}$ gives $1.869$; $1/\sqrt{\|K\|_{\max}}$ gives $1.510$; $R=\ell_0$ gives $1.220$. To get $0.927$ one needs $R\approx 0.409\,\ell_0$, which is not a natural unique reading. | **Not derived, and 0.927 does not follow from natural $R$.** The exponent $4/13$ has no derivation in the corpus. |
| Hermitian Dirac on the antiperiodic torus $N=24$ | (new) | $\max\|\lambda-\lambda_{\mathrm{exact}}\|\approx 0.00202$; slope $\approx-1.995$ | **Reproduces.** Lowest $\|\lambda\|=\sqrt{1/2}$. |
| Legacy `dirac_conoid_aps.py` spectrum | Used as a production-path APS solver | On a flat torus, $0.5(D+D^T)$ does not recover the Dirac tower (first nonzero analytic mode missed) | **Broken as a Dirac operator.** |
| $\eta_{ij}$, $\theta_{ij}$, $\phi=2\pi/5$, $m_H\in[124,127]$ | STATUS “locked / high” | `reproduce_status_locked.py` hardcodes them; Cabibbo is $\theta_{12}:=\eta_{12}\cdot\pi/12$; $m_H=125$ is inserted | **Do not reproduce from the metric.** Circular. |
| Zeta-stationarity scripts | Appeared to “find” zeros | $J$ depends only on $|\sigma-1/2|$, or $\nabla J=0$ by a cancelled finite difference | **Tautological** (already documented; identification test was null). |

Reproduction entry point: `python code/core_reproducibility.py` and `pytest -q`.

## 3. Unstated assumptions and overclaims

- “Three light channels” is a preferred radial block $\{0,1,2\}$ under a threshold between $E_0(2)$ and $E_0(3)$, plus a heuristic from $\cos(2v)$ and $C_4$. It is **not** an APS index computation. The paper’s earlier wording (“these inputs yield three light channels”) was too strong and is now a labelled conjecture.
- APS-compatible spin structure, anti-periodic tip links, and “standard conical/edge theory” were cited as if they closed the argument. They are hypotheses; Melrose’s book is a real reference, but it is not a calculation on this metric.
- Dual-Zero $\varepsilon(n)=\omega_0(-1)^n n^{-n}$ is a **definition**. Calling $\omega_0$ “geometric” does not make $0.927$ a theorem.
- STATUS (August 2026) overclaimed relative to the already-modest core paper: $G_N$ prefactor, $\omega_0$, three generations, $\eta$, angles, $m_H$ class.
- A twelve-bridge $A_5$ module may organise labels; it is not an isometry of $f$.

## 4. Dirac / APS solver

The prototype in `dirac_conoid_aps.py` assembles a *real* first-order matrix and replaces it by $0.5(D+D^T)$. Central differences are antisymmetric, so derivatives cancel. The raw matrix is not Hermitian.

`code/aps_hermitian.py` builds a complex Hermitian operator. On the flat torus it passes a known-answer test and shows second-order convergence. On the truncated conoid, APS is only a boundary penalty: that spectrum is a numerical experiment, not a continuum theorem, and is not used to support a generation count.

A flat-disk Bessel check was not completed in this pass; the torus already supplies an analytic spectrum.

## 5. Citations checked

Used in the core paper, and verified as real:

- Atiyah, Patodi, Singer, *Math. Proc. Cambridge Philos. Soc.* **77** (1975), 43–69.
- Melrose, *The Atiyah–Patodi–Singer Index Theorem*, A.K. Peters, Wellesley, MA, 1993.
- Reed and Simon, *Methods of Modern Mathematical Physics II*, Academic Press, 1975.
- Chamseddine and Connes, *Comm. Math. Phys.* **186** (1997), 731–750 (spectral action origin of $G_N\propto\ell_0^2$, not of the number $64\pi/45$).

No other citations were added. No agreement with experiment is claimed.

## 6. Would the core survive expert review?

The November 2026 core paper is closer to something a mathematician can read without being misled: definitions, short proofs, labelled numerical values, an explicit limitations section, and only real references.

It would still be a short geometry note, not a completed spectral-action or index-theoretic construction. A referee would reasonably ask for: a genuine APS/index calculation (or a clearly remaining conjecture); a unique derivation of $\omega_0$ or an admission that it is a free parameter (now admitted); a scheme-by-scheme recompute of $\alpha$ in $G_N=\alpha\ell_0^2$ if a specific prefactor is to be kept; and continued refusal to treat CKM, Higgs, unification, or RH as results. With those limitations respected, the proved geometric core (metric, $C_4$, curvature, $C_0$ existence, monotonicity) is small but defensible.
