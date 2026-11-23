# Flaw in the original zeta-stationarity scripts

These notes apply to the **unmodified** originals, which are left in place:

- `code/verification/zeta_stationarity.py`
- `code/zeta_stationarity_enhanced.py`

Corrected, non-circular counterparts sit beside them:

- `code/verification/zeta_stationarity_corrected.py`
- `code/zeta_stationarity_enhanced_corrected.py`

A direct demonstration that the originals also “pass” at midpoints and random
`t` (i.e. at points that are **not** Riemann zeros) is:

- `code/verification/zeta_stationarity_tautology_demo.py`

The identification test that uses actual Dual-Zero / conoid data and does
**not** feed in zeta zeros while searching is:

- `code/verification/zeta_identification_test.py`

## `zeta_stationarity.py`

`model_information_current(sigma, t)` is a function of `|sigma - 0.5|` only.
It does not depend on `t`, and it does not use Dual-Zero weights, Dirac
eigenvalues, or 12-bridge overlaps. By construction,

    dJ/dσ ≈ 0  at σ = 1/2 for every real t.

Evaluating it at the imaginary parts of zeta zeros therefore cannot test
whether those zeros are critical points of a SAM-3 action. Midpoints between
zeros and random `t` produce the same “YES” verdict, at the same J and the
same derivative.

## `zeta_stationarity_enhanced.py`

`j_gradient(t)` evaluates J at `s0 = 1/2 + i t` and at `s0 ± δ` with the same
shift applied to both `k1` and `conjugate(k2)`. Then

    k1 − k2 = 2 i t

is unchanged, so the finite-difference gradient is identically zero whenever
J is finite. (For larger `t`, `sin(12 * 2 i t) = i sinh(24 t)` overflows and
the script reports `nan` / “NO”. That is an overflow artifact, not a failed
identification test.) The Dual-Zero function in this file is also not the
locked generator `ε(n) = ω₀ (−1)^n n^{-n}` from doc 18.

## What a non-circular test must do

Build J from conoid spectral data, 12-bridge overlaps, and the Dual-Zero
regulator (docs 17 and 27). Search for critical points of `S_I` in the strip
**without** inserting zeta zeros into J. Only afterwards compare those
points to known zeros, and run the same comparison on midpoints, random `t`,
and shuffled spectral data.
