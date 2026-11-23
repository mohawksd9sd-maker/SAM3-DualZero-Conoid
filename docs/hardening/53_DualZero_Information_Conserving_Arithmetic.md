# 53. Dual-Zero information-conserving arithmetic

**Date:** 23 November 2026 (America/Chicago)  
**Status:** exploratory numerical tool; not a core geometric theorem  
**Code:** `dual_zero_arith/`  
**Tests:** `tests/test_dual_zero_arith_*.py`  
**Novelty note:** `dual_zero_arith/NOVELTY.md`

Honesty rule: this package removes rounding and truncation loss only.  It does not reduce modelling error, discretisation error, or a missing physical principle, and it is not a derivation of a constant, a flux, or a theory of everything.

---

## 1. The idea

A working-format number is a pair

\[
  x = \mathrm{visible} + \mathrm{residual},
\]

where `visible` is the truncated or rounded representative in the working format (fixed-place decimal, or IEEE-754 binary64), and `residual` is the exact discarded complement, stored as a `fractions.Fraction`.  Reconstruction is the sum of the two channels.  Arithmetic is performed on the restored values and the result is re-split, so the invariant

\[
  \mathrm{visible} + \mathrm{residual} = x_{\mathrm{exact}}
\]

is maintained and is proved against `Fraction` as ground truth.

The pedagogical source is the finite-decimal fallacy \(10/3 \to 3.33333\), then \(3.33333\times 3 = 9.99999\).  In \(\mathbb{Q}\) and in \(\mathbb{R}\) there is no such loss: \(10/3\times 3=10\).  The residual \(1/300000\) is exactly what six-place truncation removed, and pairing it back yields \(10\).

This is an *account* of truncation as information moving into a second channel, not a claim that \(10/3\times 3\neq 10\) in the reals, and not a use of IEEE signed zero \(\pm 0\) as a residual register.  The spectral objects \(\varepsilon(n)=\omega_0(-1)^n n^{-n}\) and the symmetric average \(\operatorname{Reg}_2\) act on functions of a spectral parameter; they are **not** identified with this residual.  They share a slogan — do not throw away the other side of a dual pair — in a different domain.

---

## 2. Tests and numbers

All of the following are reproduced by the wired test suite.

- **\(10/3\times 3\), six-digit decimal truncation.**  Naive arithmetic yields \(9.99999\).  Dual-Zero keeps residual \(1/300000\) and restores exactly \(10\).
- **\(10/3\times 3\) in float64.**  The visible product is a float just below \(10\); the residual restores exactly \(10\), matching `Fraction(10, 3) * 3`.
- **GPS-style clock sum.**  One hundred thousand increments of \(10^{-16}\) added to a large offset (\(\sim 1.2\times 10^{9}\), a GPS-week scale in seconds).  Naive float64 drops the increments (the visible running total does not move).  Dual-Zero and exact `Fraction` agree, and recover the lost sum.
- **Ballistic / rocket trajectory.**  On a simple explicit Euler step, Dual-Zero agrees with an exact-`Fraction` recurrence for the rounding part of the error.  It does **not** cancel the Euler discretisation error relative to the closed-form trajectory.  Those two errors are reported as different numbers, and only the first is claimed.

---

## 3. Novelty (honest)

The implementation is original *as Shawn’s paired-zero regulator*: truncation writes a dual residual, reconstruction restores it, and the \(10/3\) fallacy plus long accumulators are the intended tests.

It is **not** a reimplementation of Kahan / Neumaier compensated summation, Dekker–Knuth error-free transforms (TwoSum / TwoProd), or double-double arithmetic.  Those are two-component *floating-point* methods.  Here the second component is an exact rational `x − visible`.  A mathematician would fairly say: “this is exact rational arithmetic with a truncated shadow.”  That sentence is true, and it is why restoration is correct.

Full comparison table: [`dual_zero_arith/NOVELTY.md`](../../dual_zero_arith/NOVELTY.md).

---

## 4. What this does not do

- It does not change a mathematically exact theorem, an identically zero overlap, or a fit that was already a fit.
- It does not select the flux, the moduli, \(\omega_0\), or \(G_N\).
- It is not part of the locked conoid core.

Doc 54 records what happens when this arithmetic is applied to the model lines.
