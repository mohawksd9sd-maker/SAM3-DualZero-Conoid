# 52 — Dual-Zero axiom and a selection test for flux and moduli

**Date:** 23 November 2026 (America/Chicago)  
**Status:** exploratory.  This document does not lock a new core theorem and does not change the locked conoid geometry.  
**Code:** `experiments/dual_zero_axiom/`, tests in `tests/test_dual_zero_axiom.py`.  
**Authorized by:** Shawn, “Do it.” (the concrete next test proposed in doc 51).

The test is: write Dual-Zero as a standalone axiom, put it on the magnetized-surface × Pati–Salam / CCM product and on other compact surfaces besides the conoid, and compute *without fitting* whether it selects a flux \(M\) or moduli \((A,\tau)\).  \(\omega_0\) is an input; a selection that appears only after tuning \(\omega_0\) (or the area, or the finite shift) is not a derivation.  An honest null is an acceptable outcome.

---

## 1. The axiom, stated precisely

**Generator.** For \(n\in\mathbb{N}\) and an input \(\omega_0>0\),

\[
\varepsilon(n)=\omega_0(-1)^n n^{-n}.
\]

The associated positive scale of the finite approximant is \(\delta_N=\omega_0 N^{-N}=\lvert\varepsilon(N)\rvert\).  \(\omega_0\) is not derived in this document (docs 18, 42).

**Domain of \(\operatorname{Reg}_2\).** Real functions of a spectral parameter \(\lambda\) that have finite left and right limits at the evaluation point (jumps allowed).  Meromorphic functions are included wherever the symmetric average exists; at a simple pole this is the Cauchy finite part, not the residue.

**Action.** The finite approximant and the limit are

\[
\operatorname{Reg}_{2,\delta}(f)(\lambda)=\frac{f(\lambda+\delta)+f(\lambda-\delta)}{2},\qquad
\operatorname{Reg}_2(f)(\lambda)=\lim_{\delta\to 0^+}\operatorname{Reg}_{2,\delta}(f)(\lambda).
\]

The operational Dual-Zero approximant is \(\operatorname{Reg}_{2,\delta_N}\).  For a meromorphic spectral zeta \(Z(s)\), the Dual-Zero-regulated logarithm of a determinant read at \(s=0\) is the even average of the derivative,

\[
\log\det_{\mathrm{DZ}}(\delta)=-\frac{Z'(\delta)+Z'(-\delta)}{2}
\]

(with a factor \(\tfrac12\) when \(Z\) is the zeta of a square, so that the \(\delta\to 0\) limit matches \(\log\det'\lvert D\rvert=-\tfrac12 Z'_{D^2}(0)\) as in doc 49).  Shifts \(\delta\) too close to a pole of \(Z\) (in particular \(\delta=1\), and \(\delta=\tfrac12\) for the Eisenstein expansion of the unfluxed Laplacian) are excluded.

**What \(\operatorname{Reg}_2\) is not.** It is *not* a weight \(\varepsilon(n)\) on a heat trace or a mode sum.  Doc 51 already showed that \(\sum_n\varepsilon(n)\,e^{-t\lambda_n^2}\) fails the Weyl law.  That insertion is forbidden here and is tested only as a documentary negative check.

**Invariances and well-posedness** (all checked in `axiom.py`):

- Linearity on functions.
- Even in the shift \(\delta\).
- Annihilates odd germs at the evaluation point; preserves even germs.
- Recovers \(f(\lambda)\) at a continuity point, with error \(O(\delta^2)\).
- Averages a jump; the value exactly at the jump does not enter.
- At a simple pole, returns the finite part and drops the residue.
- The \(N=8\) approximant already agrees with a smooth \(f\) to machine precision at \(\omega_0=1\).
- Applied to a heat trace as a *function of \(t>0\)* (smooth), it returns the unweighted heat trace.

Consequence, used throughout: if a spectral invariant is already continuous (or \(C^2\)) at the point where it is read, the \(\delta\to 0\) limit of Dual-Zero regulation equals the unregulated value.  Any genuine change of a selection can come only from a *finite* remainder \(\delta>0\).  That remainder is scanned, including the Dual-Zero scales \(\delta_N=\omega_0 N^{-N}\) at \(\omega_0\in\{0.1,0.5,0.927,1,2\}\) and \(N\in\{2,3,5,8\}\), and a grid of explicit \(\delta\).  The value \(\omega_0=0.927\) is included only as a historically quoted input, not as a derived constant.  The scale \(N=2\), \(\omega_0=2\) gives \(\delta=1/2\) and is omitted (unsafe).

---

## 2. Magnetized flat \(T^2\)

The Dirac spectrum with integer flux \(M>0\) and area \(A\) is standard (Cremades–Ibáñez–Marchesano, already used in docs 48–49):

\[
E_n=\pm\sqrt{4\pi n\lvert M\rvert/A},\qquad n=1,2,\ldots,
\]

each with multiplicity \(\lvert M\rvert\), plus \(\lvert M\rvert\) zero modes of one chirality.  The spectrum is independent of \(\tau\).  The index equals \(M\) and does not depend on \(\operatorname{Reg}_2\), \(A\), \(\tau\), or \(\omega_0\).

The zeta of \(D^2\) (zero modes omitted) is the closed form of doc 49, \(Z(s)=2M(4\pi M/A)^{-s}\zeta(s)\), so the Dual-Zero log-determinant is exact at every safe \(\delta\).

**Results.**

- Index: \(\operatorname{Ind}(D)=M\), including \(M=3\).  Dual-Zero does not change it.
- \(\tau\) cannot be selected: it does not enter the spectrum.
- Unregulated, at fixed area, \(\log\det'\lvert D\rvert\) is maximised at the real point \(M=A/(2e)\) (doc 49).  The nearest integer is \(1\) at \(A=1\), and is \(3\) only at the tuned area \(A=2e\cdot 3\approx 16.310\).  Jointly in \((M,A)\) there is no interior critical point.
- At finite \(\delta\), including all Dual-Zero scales above, the preferred *integer* at a generic area is unchanged: \(M=1\) at \(A=1\), \(M=2\) at \(A=10\), and \(M=3\) only at the already-tuned area \(A=2e\cdot 3\).  So \(M=3\) occurs only when the area is chosen to put it there.
- The continuous stationary point at that tuned area moves by a relative \(O(\delta^2)\) amount: a distance \(\sim 6\times 10^{-7}\) from \(3\) at \(\delta=10^{-6}\), and \(0.029\) at \(\delta=0.25\).  It remains nearest to the integer \(3\), which was put in by the choice of area.
- A near-miss, not a derivation: at a *finite* mid-size shift \(\delta=0.25\), the preferred integer at \(A=8\) moves from \(1\) (unregulated) to \(2\).  That is a \(\delta\)- and \(A\)-dependent hop by one unit, not a stable selection of \(3\), and \(0.25\) is a large shift of the zeta argument, not a Dual-Zero scale except for \(\omega_0=1,N=2\).

**Verdict.** No selection of \(M=3\), of a unique area, or of \(\tau\).

---

## 3. Unfluxed flat \(T^2\) (complex structure)

On a unit-area unfluxed torus the zeta-regularised \(\det'\Delta\) is a modular invariant of \(\tau\).  In the \(\delta\to 0\) limit it is the Osgood–Phillips–Sarnak height (doc 49): maximised at the hexagonal modulus \(\tau=e^{2\pi i/3}\) (equivalently \(e^{i\pi/3}\)), with the square torus \(\tau=i\) only a critical point among rectangular tori.  This does not involve a flux and does not fix the overall area.

At finite \(\delta\), \(\log\det_{\mathrm{DZ}}(\delta)=-[Z_\Delta'(\delta)+Z_\Delta'(-\delta)]/2\) is computed from the standard Fourier expansion of the real-analytic Eisenstein series (checked against the square-lattice value \(4\zeta(2)G\) at \(s=2\), and against modular invariance).  Because the spectrum is isometric under \(\mathrm{SL}(2,\mathbb{Z})\), the Dual-Zero functional is modular invariant (checked at a sample point: differences at the \(10^{-19}\) level).  The hexagonal elliptic point therefore remains a critical point.

**Results.**  On every safe \(\delta\) in the scan, including Dual-Zero scales for the listed \(\omega_0\), the hexagonal modulus beats \(\tau=i\), and the two hexagonal points agree.  A modest fundamental-domain grid at \(\delta=0.1\) maximises at \(\tau=e^{2\pi i/3}\), not at \(\tau=i\).  No \(\omega_0\) flips the ranking.

**Verdict.** Dual-Zero does not move the known hexagonal preference and does not select \(\tau=i\), a flux, or an area.

---

## 4. \(T^2/\mathbb{Z}_4\)

The unique modulus in the standard fundamental domain compatible with a \(C_4\) (equivalently \(\mathbb{Z}_4\)) rotation is already \(\tau=i\) (doc 49).  Dual-Zero is not what fixes it.

Zero-mode sector dimensions of a magnetized Dirac operator on the square torus are representation-theoretic integers (Kobayashi–Nagamoto / Abe et al., already implemented in `experiments/missing_principle/z4_orbifold.py`).  An integer kernel dimension is independent of \(\operatorname{Reg}_2\) and of \(\omega_0\).  The invariant sector has dimension \(3\) for the fluxes \(M=8,9,10,11\) (\(\alpha=0\)), not for a unique flux, and not for \(M=3\).

**Verdict.** No Dual-Zero selection of \(M=3\).  \(\tau\) was already fixed by \(C_4\), independently of the regulator.

---

## 5. \(S^2\) with monopole flux (optional)

The twisted Dirac index on the sphere equals the monopole number \(M\) (Riemann–Roch / Atiyah–Singer; `riemann_roch.py`).  Independent of Dual-Zero.

The Seeley–DeWitt integrands on a round sphere of radius \(R\) (area \(A=4\pi R^2\)) are standard: \(\operatorname{vol}=A\), \(\int R_{\mathrm{scalar}}=8\pi\) (Gauss–Bonnet), \(\int\lvert F\rvert^2=(2\pi M)^2/A\).  In a 4D product they enter as for a magnetized torus, plus the constant curvature integral.  For illustrative Wilson coefficients taken as inputs, \(\partial S/\partial M=0\) only at \(M=0\) (unless the Yang–Mills coefficient is set to zero).  A stationary area at fixed \(M\neq 0\) exists and is proportional to \(\lvert M\rvert\); it depends on those underived coefficients and on \(\Lambda\), and is not a unique geometric output.  \(\operatorname{Reg}_2\) does not change these already-smooth densities in the \(\delta\to 0\) limit.

A closed Dirac determinant on the fluxed sphere was not used: no formula was invented for this test.

**Verdict.** No Dual-Zero selection of \(M=3\) or of a unique radius.

---

## 6. Almost-commutative product (magnetized surface × Pati–Salam / CCM)

The Seeley analysis of the product \(Y=X\times\Sigma\) in docs 48–50 is unchanged by the axiom.  The integrands are smooth in \((A,M)\), independent of \(\tau\) on a magnetized flat torus, and the internal finite triple (Pati–Salam or CCM) is a spectator for these terms (docs 45, 48).  In the \(\delta\to 0\) limit, \(\operatorname{Reg}_2\) returns the same action; \(\partial S/\partial M\) still vanishes only at \(M=0\); a stationary area at fixed \(M\) is still proportional to \(\lvert M\rvert\) and depends on underived Wilson coefficients.

At a pole of a spectral zeta, \(\operatorname{Reg}_2\) extracts the finite part and *drops the residue*.  The residue is the Weyl / volume Seeley term.  Using \(\operatorname{Reg}_2\) as a substitute for residue extraction would discard that term.  That is a different, worse truncation, not a new selection principle, and it is not used.  The finite-part functional was already studied in doc 50 and does not select \(M=3\).

**Verdict.** No new selection in the product.

---

## 7. What is selected, and what is not

| Geometry | Index / generations | Flux \(M=3\)? | Area | \(\tau\) |
|----------|---------------------|---------------|------|----------|
| Magnetized \(T^2\) | \(=M\), independent of \(\operatorname{Reg}_2\) | No (only if \(A=2e\cdot 3\) is chosen) | No unique \(A\) | Not in the spectrum |
| Unfluxed \(T^2\) | — | No flux | Unit-area comparison only | Hexagonal, unchanged by Dual-Zero |
| \(T^2/\mathbb{Z}_4\) | Integer sectors, unchanged | No (dim \(3\) at \(M=8,9,10,11\)) | — | Already \(\tau=i\) by \(C_4\) |
| \(S^2\) monopole | \(=M\), unchanged | No (\(\partial S/\partial M=0\) only at \(0\)) | \(A_*\propto\lvert M\rvert\), coefficients not derived | — |
| Product with PS / CCM | Same as the surface | No | Same as docs 48–50 | \(\tau\) does not enter the Seeley terms |

Near-miss: a large finite shift (\(\delta=0.25\)) can move the preferred integer flux by one unit at some intermediate areas on the magnetized torus.  That depends on \(\delta\) and \(A\), does not isolate \(3\), and is not a derivation.

\(\omega_0\)-sensitivity: across the scanned inputs, no selection appears that is stable under a change of \(\omega_0\).  Nothing here is a fit of \(\omega_0\) to force \(M=3\).

---

## 8. Plain-language bottom line

The Dual-Zero regulator can be written as a precise, well-posed axiom, independent of the conoid: a definite sequence, with \(\omega_0\) an input, and a symmetric average on functions of a spectral parameter — not a weight on heat traces.  That axiom was applied, without fitting, to the geometries that actually have a standard generation mechanism.  It does not choose three generations, it does not choose an area, and it does not override the known facts about \(\tau\).  The missing principle recorded in `BOTTOM_LINE.md` is still missing.  Dual-Zero remains a definition of a regularisation, not a principle that finishes a theory of everything.

---

## 9. What this does not change

- Locked conoid geometry, Dual-Zero as a definition with \(\omega_0\) an input, and \(G_N=\alpha\ell_0^2\) with \(64\pi/45\) a convention lock, stand.
- Flux \(M=3\) and the surface moduli are still not derived.
- No standalone paper is implied by this document.
