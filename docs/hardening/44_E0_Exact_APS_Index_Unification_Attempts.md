# 44 — Exact \(E_0(m)\), the truncated-conoid APS index, and unification attempts

**Date:** 23 November 2026 (America/Chicago)
**SSOT:** `STATUS_CLAIMS_AND_RESIDUALS.md`
**Rule:** derivation only; null results stay null.

This note records three pieces of mathematics, in the order they were
asked for.  No standalone paper was written.

---

## 1. Channel energies: exact formula

On the model operator
\[
  H_m = -\frac{d^2}{du^2} + \frac{m^2}{u^2}
  \qquad\text{on }(0,U),
\]
with the regular solution at \(u=0\) (Friedrichs / the unique SA
extension for \(\lvert m\rvert\ge 1\); the regular choice for \(m=0\))
and Dirichlet at \(u=U\), the substitution \(\psi=\sqrt{u}\,y\) reduces
the eigenvalue equation to Bessel’s equation of order
\(\nu=\sqrt{m^2+1/4}\).  The regular solution is \(y(z)=J_\nu(z)\) with
\(z=\sqrt{E}\,u\), and \(\psi(U)=0\) forces

\[
  E_0(m;U) = \Bigl(\frac{j_{\nu,1}}{U}\Bigr)^2,
  \qquad \nu=\sqrt{m^2+\tfrac14},
\]

where \(j_{\nu,1}\) is the first positive zero of \(J_\nu\).  In
particular \(j_{1/2,1}=\pi\), so \(E_0(0;U)=\pi^2/U^2\).

This is a theorem about the *radial model operators*, not about the 2D
Dirac operator on the conoid.

**Checks.** The Dirichlet finite-difference values at \(U=20\), \(N=800\)
agree with the exact formula to a relative error of about \(1.3\)–\(2.2\times 10^{-6}\).
The ratios \(E_0(m)/E_0(n)\) are independent of \(U\):

| ratio | exact value |
|-------|-------------|
| \(E_0(1)/E_0(0)\) | \(1.61308526\) |
| \(E_0(2)/E_0(0)\) | \(2.75408479\) |
| \(E_0(3)/E_0(0)\) | \(4.19012623\) |
| \(E_0(2)/E_0(1)\) | \(1.70733987\) |

**Bounds (rigorous).** Monotonicity gives \(E_0(m)\ge E_0(0)=\pi^2/U^2\).
The standard inequality \(j_{\nu,1}>\nu\) (\(\nu\ge 0\)) gives the
sometimes-sharper lower bound \(E_0(m)>(m^2+1/4)/U^2\).  The \(m=0\)
ground state as a trial function gives

\[
  E_0(m) \le \frac{\pi^2 + 2\pi m^2 \int_0^\pi (\sin t/t)^2\,dt}{U^2},
\]

with \(\int_0^\pi (\sin t/t)^2\,dt \approx 1.41815157613\).  Equality holds
at \(m=0\).

Code: `code/core_geometry.py` (`E0_exact` and the bounds).
Tests: `tests/test_E0_exact.py`.
JSON: `reproducibility/E0_exact.json`.

---

## 2. APS index of the untwisted Dirac operator on the truncated conoid

Let \(X_{a,b}=[a,b]\times S^1\) with \(0<a<b<\infty\) carry the locked
metric \(du^2+f^2\,dv^2\).  This is a smooth compact oriented 2-manifold
with boundary, diffeomorphic to a closed annulus.

**Theorem.** After the product-collar deformation required by the
Atiyah–Patodi–Singer theorem (the metric is made of product type near
each boundary, without changing the induced boundary metrics):

1. The bulk \(\hat A\)-density vanishes in dimension 2 (the first
   Pontryagin form is a 4-form).
2. Each boundary operator is unitarily equivalent to the standard 1D
   Dirac operator \(i\,d/ds\) on a circle of length \(L(u)=\oint f(u,\cdot)\,dv\).
   (The non-product term \(\tfrac12\partial_u\log f\) is removed by the
   collar deformation; it is not an input to the product-collar formula.)
3. For the *antiperiodic* (bounding) spin structure on each end — the
   structure that extends over a disk cap — the spectrum is
   \(\{(2\pi/L)(k+1/2):k\in\mathbb{Z}\}\), so \(\eta=h=0\) and
   \(\bar\eta=0\) at each end.
4. Therefore

   \[
     \operatorname{ind} D_{\mathrm{APS}}(X_{a,b}) = 0.
   \]

   The value is independent of \(a\), \(b\), and \(\ell_0\).  It is not
   equal to 3.

For a *periodic* spin structure on a boundary component one has
\(h=1\), \(\eta=0\), \(\bar\eta=1/2\).  In every standard orientation
convention the resulting index lies in \(\{-1,0,1\}\), never 3.

**What this does and does not refute.**

- The claim that the APS index of the *untwisted* 2D Dirac operator on
  the truncated conoid equals 3 is **refuted**.
- The singular-tip limit \(a\to 0\) is *not* covered: the metric fails
  to be smooth at the four tip nodes, and APS as stated applies to a
  smooth compact manifold with boundary.  That singular problem remains
  open; it is not an index-3 theorem either.
- A nonzero index *can* be arranged by coupling to an auxiliary \(U(1)\)
  connection with boundary holonomy \(\kappa\).  Falomir, Pisani and
  Wipf (J. Phys. A 33 (2000) 1927) give \(\operatorname{index}=k+1\)
  for \(k<\kappa\le k+1\) on the disk, so index 3 requires
  \(\kappa\in(2,3]\).  That flux is **not derived** from the locked
  metric: the spin connection of \(f\) is already part of the untwisted
  Dirac operator and must not be counted twice.

**Diagnostic (not an index input).** On a raw \(u=\mathrm{const}\)
slice, before the product-collar deformation, the zeroth-order term
\(W=\tfrac12\partial_u\log f=u/(2f^2)\) has mean holonomy

\[
  \xi(u)=\frac{\overline{W}\,L}{2\pi}
  = \frac{\sqrt{1-k^2}\,K(k)}{\pi},
  \qquad k^2=\frac{4\ell_0^2}{u^2+4\ell_0^2}.
\]

Limits: \(\xi(u)\to 0\) as \(u\to 0^+\) and \(\xi(u)\to 1/2\) as
\(u\to\infty\).  The closed form matches a direct quadrature of
\((u/4\pi)\int_0^{2\pi} dv/f\) to \(\sim 10^{-15}\).  This \(\xi\) is
recorded so the \(W\neq 0\) calculation is reproducible; it is *not*
fed into the product-collar index.

Code: `code/aps_index_theorem.py`.
Tests: `tests/test_aps_index_theorem.py`.
JSON: `reproducibility/aps_index_theorem.json`.

A fully Hermitian 2D disk discretisation that reproduces Falomir’s
nonzero-flux zero-mode counts is still **not** in hand (doc 43).  The
index theorem above does not depend on that discretisation.

---

## 3. Unification-derivation attempts

Each attempt is classified honestly.  All current attempts **failed**.

| Attempt | Verdict | Why |
|---------|---------|-----|
| Gauge group from isometries of \(f\) | **Failed** | The exact isometry group is discrete \(C_4\).  \(A_5\) is not an isometry (counterexample).  \(C_4\) is not \(\mathrm{SU}(3)\times\mathrm{SU}(2)\times\mathrm{U}(1)\).  In almost-commutative geometry the SM gauge group comes from a finite algebra, which is not derived from the conoid. |
| Three generations from the APS index | **Failed** for the untwisted operator | Product-collar index \(=0\) (bounding spin structure).  Index 3 needs an underived flux \(\kappa\in(2,3]\) or a finite triple that already contains three summands. |
| SM mass ratios from \(E_0(m)/E_0(n)\) | **Failed** | The ratios are exact and \(U\)-independent, but they are \(O(1)\) (\(\approx 1.61, 2.75, 4.19,\ldots\)).  Charged-lepton ratios are \(O(10^2)\)–\(O(10^3)\).  No identification of channel index with a generation is made. |
| Unique geometric \(\omega_0\) and the exponent \(4/13\) | **Failed** | The previous candidate search (doc 43) is confirmed; additional comparisons to \(\ln 2\), \(\xi_\infty=1/2\), and the exact \(E_0\) ratios also fail to produce \(\omega_0\approx 0.927\) or \(4/13\).  Both remain free inputs. |
| Unique spectral-action \(\alpha\) in \(G_N=\alpha\ell_0^2\) | **Failed** (scheme-dependent) | Exact \(C_0=2\pi\ln 2\) removes one uncertainty but not the scheme dependence in the cutoff moment \(\phi_2\) or in the Einstein–Hilbert convention factor.  \(64\pi/45\) remains a convention lock. |
| Coupling unification from the spectral action on conoid \(\times F\) | **Failed** | \(F\) is not derived, and the cutoff moments are the same scheme data that leave \(\alpha\) unfixed.  No unique \(g_1:g_2:g_3\) or \(M_U\). |

Code: `code/unification_derivation_attempts.py`.
Tests: `tests/test_unification_attempts.py`.
JSON: `reproducibility/unification_derivation_attempts.json`.

---

## What remains open

- The Dirac operator at the *singular tip* (\(a\to 0\)), including any
  APS or conic-boundary analysis at the four tip nodes.
- A Hermitian disk discretisation with Falomir flux zero-mode counts
  (numerical, not needed for the index theorem above).
- Any derivation of \(\omega_0\), \(4/13\), \(\alpha\), the SM gauge
  group, coupling unification, or mass ratios from the locked geometry.
