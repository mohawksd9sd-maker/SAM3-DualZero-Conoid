# 54. Dual-Zero re-run of SAM-2 / SAM-3 numerical claims

**Date:** 23 November 2026 (America/Chicago)  
**Status:** exploratory; honest null for “rounding hid a TOE”  
**Code:** `experiments/dual_zero_toe/`  
**Tests:** `tests/test_dual_zero_toe.py`  
**Arithmetic used:** `dual_zero_arith/` (doc 53)

Honesty rule: exact arithmetic cannot change a mathematically exact result.  Dual-Zero arithmetic removes rounding / truncation loss only, not modelling error, discretisation error, or a missing principle.  Original SAM-2 / desktop source files are not in this repository; only the claims that were re-run, and the scripts, are recorded here.

Shawn’s charge, as clarified: use Dual-Zero arithmetic on the earlier math-model lines and look for a unified theory of everything — one consistent framework for gravity, the gauge forces, and matter — while preserving Dual-Zero.  Three generations is welcome if it appears, not a requirement.  Rank by how far a line gets toward that framework (anomaly freedom, a correct low-energy limit, no free-parameter fits), with Dual-Zero kept or improved.

---

## 1. What was re-run

Each item was evaluated in at least two of: naive float64 (or a numerical integral), Dual-Zero arithmetic (`visible + exact residual`), and exact `Fraction` / `mpmath` (40–50 dps) as ground truth.

| Claim or computation | Source line | Why it might have been rounding |
|----------------------|-------------|----------------------------------|
| “Zero Yukawa overlaps due to phase cancellation” | May 2026 Yukawa discussion: \(\int_0^{2\pi} e^{i(m_i-m_j)\theta}\,d\theta=2\pi\delta_{m_i m_j}\) | A leftover \(\sim 10^{-16}\) could be mistaken for “almost zero” |
| \(C_0=2\pi\ln 2\), and the numerical integral \(C_0(U)\) | Locked SAM-3 core | Finite cutoff \(U\) and float64 |
| \(G_N/\ell_0^2=64\pi/45\) | Convention lock in docs 18/42 | Float evaluation of a multiple of \(\pi\) |
| \(\omega_0=(R/D)^{4/13}\approx 0.927\) | Doc 18 / `omega0_search.py` | High-precision power might hit \(0.927\) for a natural \(R\) |
| SAM-2 kernel and \(1/\alpha=137.035999084\) | SAM-2 v2.21 text (quoted, not uploaded) | Finite-digit evaluation of a running formula |
| One-loop PS scales \(m_R,\Lambda\) from PDG inputs | Doc 48 `rge_pipeline` | ODE / log running in float64 |
| CIM Yukawa overlaps and Gram matrices, fluxes \((3,3,6)\) | Docs 47–48 | Grid sums; entries at \(10^{-16}\) |
| \(\det'\Delta\) ranking of \(\tau\); magnetized \(\det'\|D\|\) vs \(M,A\); \(T^2/\mathbb{Z}_4\) sector counts; index \(=M\) | Docs 49–52 | Floating-point extrema or “almost 3” |
| 2I character table, \(E_8\) Casimir \(=30\), \(10/3\times 3\) in \(\mathbb{Q}\) | Docs 51 and 53 | Already exact; listed for completeness |

---

## 2. What changed

**No genuine change.**  No earlier failure or success in these models was an artifact of rounding loss that Dual-Zero arithmetic repairs.

### Phase cancellation

The character integral is identically \(0\) for \(m\neq 0\) and \(2\pi\) for \(m=0\).  A 2048-point Riemann sum, naive float64 vs Dual-Zero vs `mpmath`, gives off-diagonal maxima \(\approx 4.0\times 10^{-16}\) (naive), \(\approx 3.0\times 10^{-16}\) (Dual-Zero), and \(\sim 10^{-41}\) (`mpmath`).  Those leftovers are quadrature / roundoff of a true zero.  Dual-Zero does **not** un-zero them.  Later fitted CKM figures (for example a quoted \(\sin\theta_{12}=0.2248\) against an experimental \(0.225\)) remain fits.

### \(C_0\) and \(G_N\)

- \(2\pi\ln 2\): float64 and 50-digit `mpmath` agree to the last bit of float64.
- The numerical integral \(C_0(U)\) differs from the exact value by \(1.47\times 10^{-5}\) at \(U=400\), \(5.88\times 10^{-7}\) at \(U=2000\), \(3.58\times 10^{-8}\) at \(U=8000\).  That is **cutoff error**, shrinking as \(U\to\infty\), not rounding loss.
- \(64\pi/45\): float64 and `mpmath` agree at double precision.  The prefactor remains a convention lock.

### \(\omega_0\) and \(4/13\)

Re-evaluation of \((R/D)^{4/13}\) for the documented natural radii (\(1/|K|_{\max}\), \(1/\sqrt{|K|_{\max}}\), \(\ell_0\), \(2\ell_0\)) still gives \(1.87\), \(1.51\), \(1.22\), \(1.51\), not \(0.927\).  Hitting \(0.927\) still requires \(R/D\approx 0.7816\), hence \(R\approx 0.409\), which is not singled out by the geometry.  \(\omega_0\) remains an input.

### SAM-2 \(\alpha\)

The written kernel at \(m_Z\) is \(f\approx 513283.615346553\); float64 and 50-digit `mpmath` differ by \(4\times 10^{-10}\).  Changing \(\beta\) from \(0.04\) to \(0.06\), or \(k_{\mathrm{GUT}}\) from \(10^{15}\) to \(10^{17}\), moves \(f\) by hundreds.  The quoted \(1/\alpha=137.035999084\) is the CODATA 2018 experimental value.  The coefficient \(0.05\) is still not the \(E_8\) adjoint Casimir (that is \(30\)).  Dual-Zero arithmetic does not turn this into a derivation.

### RGE / Pati–Salam meeting

The one-loop PDG determination remains \(m_R\approx 4.205\times 10^{13}\,\mathrm{GeV}\), \(\Lambda\approx 2.399\times 10^{15}\,\mathrm{GeV}\).  The relative difference of \(\log m_R\) between float64 and `mpmath` is \(1.8\times 10^{-17}\).  The scales are still a fit of the meeting condition to measured couplings.

### Magnetized \(T^2\) Yukawas

Gram matrices for flux \(3\) agree with the identity at the \(10^{-15}\) level (quadrature).  For fluxes \((I,J,K)=(3,3,6)\) at \(\tau=i\) and vanishing Wilson lines, \(36\) of \(54\) Yukawa entries lie below \(10^{-12}\).  Refining the grid from \(48^2\) to \(80^2\) changes those tensors by at most \(8\times 10^{-16}\); the tiny entries stay tiny.  They behave as structural zeros at that modulus point.  Turning on Wilson lines (\(\zeta_J=0.2\), \(\zeta_K=0.1+0.15i\)) makes every entry \(O(0.03)\)–\(O(0.75)\).  That is a change of moduli, already documented, not a restoration of lost bits.

### Flux, area, \(\tau\), index

Unchanged from docs 49–52.  \(\det'\Delta\) still prefers the hexagonal torus (\(F(\rho)=0.596450\ldots>F(i)=0.590170\ldots\)).  The magnetized determinant still prefers \(M=1\) at area \(1\), and \(M=3\) only at the tuned area \(A=2e\cdot 3\).  \(T^2/\mathbb{Z}_4\) still has an invariant sector of dimension \(3\) for \(M=8,9,10,11\).  The index is still \(M\).  Dual-Zero arithmetic does not select a unique flux or area without a hand-chosen scale.

---

## 3. Ranked answer

Criterion: a consistent unified framework for gravity, gauge forces, and matter, with Dual-Zero preserved or enhanced; anomaly freedom; a correct low-energy limit; no free-parameter fits.  Three generations is not required.

**1. Best consistent unified framework.**  
Current SAM-3 Dual-Zero — the definition \(\varepsilon(n)=\omega_0(-1)^n n^{-n}\) with symmetric \(\operatorname{Reg}_2\) on functions of a spectral parameter, \(\omega_0\) an input, plus the arithmetic residual channel — together with a 4D almost-commutative product

\[
  (\text{spacetime factor})
  \;\times\;
  (\text{compact magnetized surface }\Sigma)
  \;\times\;
  (\text{Pati–Salam or CCM finite triple }F).
\]

The shape of the spacetime factor is negotiable.  The locked right conoid is mathematically in order, but it is not what supplies the gauge group or the matter index, and it is not required for Dual-Zero.  This is the only line in the corpus that is internally consistent and already has standard, checkable mechanisms for all three pieces of a unification, while keeping Dual-Zero.

Concretely:

- **Dual-Zero.**  Kept as a regulator definition (not a uniqueness theorem, not a heat-trace weight \(\sum\varepsilon(n)e^{-t\lambda_n^2}\), and not the SAM-2 ultrafilter entity).  Enhanced, for numerical work, by the paired-zero arithmetic of `dual_zero_arith/`.
- **Gravity.**  The spectral action produces an Einstein–Hilbert term, a cosmological term, and Yang–Mills / Higgs-like terms.  Structurally \(G_N=\alpha\ell_0^2\).  The recorded \(\alpha=64\pi/45\) is a convention lock.
- **Gauge group.**  The finite triple \(F\) is Pati–Salam \(\mathrm{SU}(2)_L\times\mathrm{SU}(2)_R\times\mathrm{SU}(4)\), or the Chamseddine–Connes–Marcolli algebra that yields the Standard Model.  The group is still a *choice* of finite geometry, not an output of Dual-Zero.  With the standard fermion embedding the gauge-plus-matter content is anomaly-free in the usual sense.
- **Matter.**  A magnetized compact surface (or a line bundle of degree \(M\)) gives \(M\) chiral zero modes by the index theorem.  \(M\) is an integer choice.  Three generations would correspond to \(M=3\), which is allowed but not selected.
- **Low-energy limit.**  Running down from a meeting scale can recover the Standard Model (or a PS parent of it) *if* the embeddings and the breaking pattern are the standard ones.  The measured couplings at \(M_Z\) are inputs to that run, not predictions.

**What is still missing** before this is a theory of everything, rather than a consistent unification *scheme*, is written as research targets in [`ROADMAP_TOE_GUT.md`](../../ROADMAP_TOE_GUT.md).  In short: a principle that fixes \(\omega_0\), the \(G_N\) prefactor, the flux and the moduli, and (if uniqueness is required) the choice of \(F\); masses, mixings, and a unique Higgs mass as outputs; and a derivation of the low-energy couplings rather than a determination of \((m_R,\Lambda)\) from those couplings.  Dual-Zero arithmetic does not supply these.

**2.** May 2026 SAM-3, keeping only the regulator definition and discarding the 2I “proof” of three generations, the uniqueness / \(10\div 3\) / RH claims, and the fitted CKM/Yukawa numbers.  Those extras do not survive an honest check, and Dual-Zero arithmetic does not save them.

**3.** SAM-2 v2.21 and the desktop hybrid lines (\(E_8\) / \(\mathrm{SO}(10)\), “20 exact parameters”).  The ultrafilter Dual-Zero is not well-defined, \(0.05\) is not an \(E_8\) Casimir, and the constants (including \(1/\alpha=137.035999084\)) are experimental values restated with free inputs.  Dual-Zero arithmetic does not repair a definitional failure or a fit.

**4.** HSTO / HSC is software, not a unification framework.

---

## 4. Plain-language bottom line

Using Dual-Zero arithmetic on every numerical claim we could honestly re-run did not uncover a hidden theory of everything, and it did not flip any earlier verdict.  The May “zero Yukawa overlaps” were true zeros from symmetry, not information lost at zero.  Constants that were already exact stayed exact.  Constants that were fits stayed fits, just with more digits of confirmation that rounding was not the issue.

The furthest honest unification, with Dual-Zero preserved, is still a 4D almost-commutative geometry with a Pati–Salam or CCM finite algebra, a magnetized compact surface, and the current Dual-Zero regulator (and, for computation, the residual arithmetic).  That package can describe gravity, a consistent gauge group, and chiral matter in one spectral framework, and it can have the Standard Model as a low-energy limit if one chooses the standard embeddings.  What it cannot yet do is *derive* the remaining free numbers — the Dual-Zero scale, Newton’s prefactor, the flux and moduli, or the masses — without fitting.  That is what still stands in the way of a theory of everything.  Three generations would be a special case of a derived flux, not a separate goal, and it has not appeared.
