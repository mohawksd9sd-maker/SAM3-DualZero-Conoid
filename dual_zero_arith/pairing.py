"""Paired-zero / Dual-Zero arithmetic.

Every exact quantity x is written

    x = visible + residual

where ``visible`` is the truncated or rounded representative in a working
format (fixed-place decimal, or IEEE float64) and ``residual`` is *exactly*
x − visible, stored as a rational.  The residual is the information that
ordinary arithmetic would send to zero.  Reconstruction is

    restore(visible, residual) = visible + residual = x.

That is the arithmetic analogue of not discarding the other side of a Dual
pair.  It is not the spectral operator Reg₂(f)(λ) = [f(λ+δ)+f(λ−δ)]/2,
and it does not use the spectral generator ε(n)=ω₀(−1)ⁿ n^{−n}; those
belong to a different Dual-Zero use (mode regularization) and are not
pretended to be rounding residuals.

The invariant ``Fraction(visible) + residual == exact`` is maintained by
every operation and is the correctness criterion.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
from typing import Optional, Union

Number = Union[int, float, Fraction, Decimal, "DualZero"]


def as_fraction(x: Number) -> Fraction:
    """Exact rational of a Python number, a Decimal, or a restored DualZero."""
    if isinstance(x, DualZero):
        return x.exact()
    if isinstance(x, Fraction):
        return x
    if isinstance(x, Decimal):
        return Fraction(x)
    if isinstance(x, int):
        return Fraction(x)
    if isinstance(x, float):
        return Fraction.from_float(x)
    raise TypeError(f"cannot convert {type(x)!r} to Fraction")


def truncate_decimal_places(exact: Fraction, places: int) -> Fraction:
    """Truncate toward 0 to a fixed number of digits after the decimal point.

    Example: 10/3 at 5 places becomes 3.33333 = 333333/100000.
    This is truncation, not rounding: it matches the 3.33333… fallacy.
    """
    if places < 0:
        raise ValueError("places must be >= 0")
    scale = 10**places
    scaled = exact * scale
    # Integer truncation toward zero.
    num, den = scaled.numerator, scaled.denominator
    if num >= 0:
        vis_int = num // den
    else:
        vis_int = -((-num) // den)
    return Fraction(vis_int, scale)


def split_decimal(exact: Number, places: int) -> tuple[Fraction, Fraction]:
    """Return (visible, residual) with visible truncated to ``places`` decimals."""
    q = as_fraction(exact)
    visible = truncate_decimal_places(q, places)
    residual = q - visible
    return visible, residual


def split_float64(exact: Number) -> tuple[float, Fraction]:
    """Return (visible float64, exact residual).  visible is IEEE-754 round-to-nearest."""
    q = as_fraction(exact)
    visible = float(q)
    residual = q - Fraction.from_float(visible)
    return visible, residual


def restore(visible: Number, residual: Number) -> Fraction:
    """Symmetric reconstruction: pair the working value with the dual residual."""
    return as_fraction(visible) + as_fraction(residual)


@dataclass(frozen=True)
class DualZero:
    """A Dual-Zero pair: working-format visible value plus exact residual.

    ``kind`` is ``"decimal"`` (fixed fractional places) or ``"float64"``.
    """

    visible: Fraction  # exact rational of the working-format representative
    residual: Fraction
    kind: str
    places: Optional[int] = None  # used when kind == "decimal"

    def __post_init__(self) -> None:
        if self.kind not in {"decimal", "float64"}:
            raise ValueError("kind must be 'decimal' or 'float64'")
        if self.kind == "decimal" and self.places is None:
            raise ValueError("decimal DualZero requires places")
        if self.kind == "float64" and self.places is not None:
            raise ValueError("float64 DualZero does not use places")

    # --- constructors -----------------------------------------------------

    @classmethod
    def from_exact_decimal(cls, exact: Number, places: int) -> "DualZero":
        vis, res = split_decimal(exact, places)
        return cls(visible=vis, residual=res, kind="decimal", places=places)

    @classmethod
    def from_exact_float64(cls, exact: Number) -> "DualZero":
        vis_f, res = split_float64(exact)
        return cls(visible=Fraction.from_float(vis_f), residual=res, kind="float64")

    @classmethod
    def from_visible_decimal(cls, visible: Number, places: int) -> "DualZero":
        """A working-format number with an empty residual (already truncated)."""
        vis = truncate_decimal_places(as_fraction(visible), places)
        return cls(visible=vis, residual=Fraction(0), kind="decimal", places=places)

    @classmethod
    def zero_decimal(cls, places: int) -> "DualZero":
        return cls(visible=Fraction(0), residual=Fraction(0), kind="decimal", places=places)

    @classmethod
    def zero_float64(cls) -> "DualZero":
        return cls(visible=Fraction(0), residual=Fraction(0), kind="float64")

    # --- reconstruction ---------------------------------------------------

    def exact(self) -> Fraction:
        """Restored value: visible + residual.  This is the Dual-Zero output."""
        return self.visible + self.residual

    def visible_float(self) -> float:
        return float(self.visible)

    def visible_decimal_string(self) -> str:
        if self.kind != "decimal" or self.places is None:
            raise ValueError("visible_decimal_string is for decimal pairs")
        return format_fixed(self.visible, self.places)

    def invariant_holds(self) -> bool:
        return self.visible + self.residual == self.exact()

    # --- arithmetic: exact on restored values, then re-split --------------
    # The working-format "naive" operation is available separately so tests
    # can compare lost-information vs restored results.

    def _resplit(self, exact: Fraction) -> "DualZero":
        if self.kind == "decimal":
            assert self.places is not None
            return DualZero.from_exact_decimal(exact, self.places)
        return DualZero.from_exact_float64(exact)

    def __add__(self, other: Number) -> "DualZero":
        return self._resplit(self.exact() + as_fraction(other))

    def __radd__(self, other: Number) -> "DualZero":
        return self.__add__(other)

    def __sub__(self, other: Number) -> "DualZero":
        return self._resplit(self.exact() - as_fraction(other))

    def __rsub__(self, other: Number) -> "DualZero":
        return self._resplit(as_fraction(other) - self.exact())

    def __mul__(self, other: Number) -> "DualZero":
        return self._resplit(self.exact() * as_fraction(other))

    def __rmul__(self, other: Number) -> "DualZero":
        return self.__mul__(other)

    def __truediv__(self, other: Number) -> "DualZero":
        return self._resplit(self.exact() / as_fraction(other))

    def __rtruediv__(self, other: Number) -> "DualZero":
        return self._resplit(as_fraction(other) / self.exact())

    def __neg__(self) -> "DualZero":
        return self._resplit(-self.exact())

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DualZero):
            return self.exact() == other.exact()
        if isinstance(other, (int, float, Fraction, Decimal)):
            return self.exact() == as_fraction(other)
        return NotImplemented

    def __repr__(self) -> str:
        if self.kind == "decimal":
            return (
                f"DualZero(visible={format_fixed(self.visible, self.places or 0)}, "
                f"residual={self.residual}, places={self.places})"
            )
        return f"DualZero(visible={self.visible_float()!r}, residual={self.residual}, kind='float64')"


def format_fixed(q: Fraction, places: int) -> str:
    """Fixed-place decimal string of a rational already truncated to those places."""
    scale = 10**places
    n = q * scale
    if n.denominator != 1:
        # Not an exact fixed-place value; still print rounded toward zero for display.
        vis = truncate_decimal_places(q, places)
        n = vis * scale
    sign = "-" if n < 0 else ""
    n = abs(int(n))
    whole, frac = divmod(n, scale)
    return f"{sign}{whole}.{frac:0{places}d}"


def naive_decimal_mul(visible_a: Fraction, visible_b: Fraction, places: int) -> Fraction:
    """Multiply two already-truncated visibles and truncate the product (no residual)."""
    return truncate_decimal_places(visible_a * visible_b, places)


def naive_decimal_add(visible_a: Fraction, visible_b: Fraction, places: int) -> Fraction:
    return truncate_decimal_places(visible_a + visible_b, places)


def naive_float64_add(a: float, b: float) -> float:
    return a + b


def naive_float64_mul(a: float, b: float) -> float:
    return a * b
