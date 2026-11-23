# Novelty assessment (honest)

This note compares the Dual-Zero arithmetic in this folder with prior
art.  It does not claim a new theorem of floating-point arithmetic, a
faster sum than Kahan, or a replacement for a computer-algebra field.

## What is Shawn's idea, as implemented

1. Truncation is treated as *information moving into a second channel*,
   not as an irreversible flush to zero.  The second channel is the
   “dual zero”: it holds exactly the discarded complement.
2. The working value and that complement form a pair
   `x = visible + residual`, reconstructed by adding the two sides.
3. The pedagogical source is the finite-decimal fallacy
   `10/3 → 3.33333`, `3.33333 × 3 = 9.99999`.  In `Q` and in `R` there
   is no such loss; the residual `1/300000` is what the truncation
   removed, and pairing it back yields `10`.
4. The intended use is accumulators that quietly drop small increments
   (GPS clocks, long trajectory recurrences) — again, only the
   rounding / truncation part of the error.

The spectral objects `ε(n)` and `Reg₂` on functions of a spectral
parameter are **not** claimed to be this residual.  They share a
slogan — do not throw away the other side of a dual pair — in a
different domain.

## Prior art, and where this overlaps

| Prior art | What it does | Overlap with this package |
|-----------|--------------|---------------------------|
| Kahan summation (1965) and Neumaier's improvement | A running compensation term estimates bits lost while adding in *the same floating-point format* | Same *purpose* for long sums (keep what a large addend would wash out). **Not** the same algorithm: this code does not use Kahan's recurrence, `y = x − compensation`, or a floating-point compensation term. |
| Dekker (1971), Knuth, Shewchuk error-free transforms; TwoSum / TwoProd | Use IEEE rounding properties to split `fl(a+b)` and the exact `a+b − fl(a+b)` into two floats | Same *shape* of a two-component representation of a sum or product. **Not** the same method: residuals here are exact rationals computed as `x − visible`, not recovered from a floating-point EFT. |
| Double-double / quad-double (Dekker, Bailey, QD) | A number is stored as `hi + lo` in two (or more) floats, with a carefully rounded arithmetic | Again a two-part number. This package's second part is a `Fraction`, so the pair is an exact rational, not a 106-bit floating value. |
| Interval arithmetic | Enclose a value in `[lo, hi]` to bound rounding | Different goal: intervals *bound* error; Dual-Zero *stores* the exact discarded complement and restores a point value. |
| Exact rationals / computer algebra (`Fraction`, `Q`, MPQ) | Compute in `Q` and never truncate | This is the real source of exactness here. Once the residual is an exact rational, `visible + residual` is ordinary arithmetic in `Q`. We do not pretend otherwise. |

## What is genuinely distinct

- The *account* of the operation: a visible world that is allowed to
  look like `9.99999`, and a dual-zero register whose job is to hold
  the tail that made it so, then restore `10`.  That is a truncation
  pairing, not a compensated-sum loop and not a 2-ulps-accurate EFT.
- The working format can be *decimal truncation* (the form of the
  motivating fallacy), not only binary floating point.
- Reconstruction is defined as pairing the kept representative with
  its exact complement, with a maintained invariant proved against
  `Fraction`.
- Applications are written so that rounding loss and discretization
  error are reported as *different numbers*, and only the first is
  claimed.

None of that makes this a new, faster, or hardware-ready floating-point
system.  A mathematician would fairly say: “You are doing exact
rational arithmetic and displaying a truncated shadow.”  That sentence
is true, and it is why the restoration is correct.

## What is not claimed

- Not a new IEEE-754 format, and not a use of IEEE signed zero `±0`
  as a residual register (`±0` does not store a discarded tail).
- Not a proof that Kahan or double-double are unnecessary.
- Not a method that reduces modelling error, ODE discretization
  error, sensor noise, or “lost transference particles.”  Those are
  not rounding residuals.
- Not a derivation of a physical constant, a flux, or a theory of
  everything.
- Not a claim that `10/3 × 3 ≠ 10` in the reals.  The opposite is true.

## Bottom line on novelty

The implementation is original *as Shawn's paired-zero regulator*:
truncation writes a dual residual, reconstruction restores it, and the
`10/3` fallacy plus GPS/rocket accumulators are the intended tests.
The exactness is not a new floating-point miracle; it is exact bookkeeping
of the discarded complement in `Q`.  In purpose it overlaps compensated
summation and two-part expansions; in algorithm it is not a copy of
them.  That is the accurate claim, and no more.
