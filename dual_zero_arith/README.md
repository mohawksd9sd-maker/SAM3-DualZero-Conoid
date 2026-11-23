# Dual-Zero information-conserving arithmetic

Shawn’s paired-zero idea: a working-format value is stored as

\[
  x = \mathrm{visible} + \mathrm{residual},
\]

where `visible` is the truncated or rounded representative and `residual` is the exact discarded complement (a `Fraction`).  Reconstruction is the sum of the two channels.  Operations act on the restored values and then re-split.

This package does **not** implement Kahan summation, TwoSum, or double-double.  Exactness is proved against `fractions.Fraction`.  It removes rounding and truncation loss only, not modelling or discretisation error.

Honest comparison with prior art: [`NOVELTY.md`](NOVELTY.md).  Summary: [`docs/hardening/53_DualZero_Information_Conserving_Arithmetic.md`](../docs/hardening/53_DualZero_Information_Conserving_Arithmetic.md).

Tests live in `tests/test_dual_zero_arith_*.py` and are collected by `pytest`.
