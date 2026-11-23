"""Dual-Zero information-conserving arithmetic (Shawn's paired-zero regulator).

A working-format value is paired with an exact residual channel that holds
whatever truncation or rounding would have flushed to zero.  Reconstruction
is the sum of the two channels.

This package does not implement Kahan summation, TwoSum, or double-double.
Exactness is proved against ``fractions.Fraction``.
"""

from .pairing import DualZero, restore, split_decimal, split_float64

__all__ = ["DualZero", "restore", "split_decimal", "split_float64"]
