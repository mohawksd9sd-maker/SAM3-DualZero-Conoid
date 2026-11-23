"""GPS-style clock sums and a simple ballistic / rocket trajectory.

These demos compare three arithmetics on the *same* recurrence:

  1. naive working-format arithmetic (decimal truncation, or float64)
  2. Dual-Zero (visible + exact residual, then restore)
  3. exact ``Fraction`` ground truth of the same recurrence

A closed-form physical trajectory, when available, is reported separately.
The gap between the exact-Fraction recurrence and the closed form is
discretization / modelling error.  Dual-Zero does not remove that gap.
It only removes the gap between naive working-format arithmetic and the
exact-Fraction recurrence — i.e. rounding / truncation loss.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import List

from .pairing import DualZero, as_fraction, naive_decimal_add, naive_float64_add


# ---------------------------------------------------------------------------
# GPS-style long sum of tiny clock increments
# ---------------------------------------------------------------------------

@dataclass
class ClockSumResult:
    n_steps: int
    base: Fraction
    increment: Fraction
    exact_total: Fraction
    naive_total: Fraction
    dual_restored: Fraction
    dual_visible: Fraction
    lost_by_naive: Fraction
    restored_minus_exact: Fraction
    kind: str


def gps_clock_sum_float64(
    n_steps: int = 1_000_000,
    base: float = 1_000_000_000.0,  # ~31.7 years in seconds, GPS-like large time
    increment: float = 1e-9,  # one nanosecond, below ULP(1e9) ≈ 1.19e-7
) -> ClockSumResult:
    """Add many nanosecond ticks to a large GPS-style clock in float64.

    ULP at 1e9 is about 1.19e-7 s, so a 1e-9 s increment is invisible to
    naive float64 addition: 1e9 + 1e-9 == 1e9.
    """
    exact_base = Fraction.from_float(base)
    exact_inc = Fraction.from_float(increment)
    exact_total = exact_base + exact_inc * n_steps

    naive = base
    for _ in range(n_steps):
        naive = naive_float64_add(naive, increment)

    acc = DualZero.from_exact_float64(exact_base)
    inc_dz = DualZero.from_exact_float64(exact_inc)
    for _ in range(n_steps):
        acc = acc + inc_dz

    naive_q = Fraction.from_float(naive)
    return ClockSumResult(
        n_steps=n_steps,
        base=exact_base,
        increment=exact_inc,
        exact_total=exact_total,
        naive_total=naive_q,
        dual_restored=acc.exact(),
        dual_visible=acc.visible,
        lost_by_naive=exact_total - naive_q,
        restored_minus_exact=acc.exact() - exact_total,
        kind="float64",
    )


def gps_clock_sum_decimal(
    n_steps: int = 10_000,
    base: Fraction = Fraction(1_000_000_000),
    increment: Fraction = Fraction(1, 1_000_000_000),
    places: int = 6,
) -> ClockSumResult:
    """Same sum in fixed-place decimal (default: 6 digits after the point).

    At 6 decimal places the visible unit is 1e-6 s, so a 1e-9 s tick
    truncates to 0 and is lost unless the residual channel keeps it.
    """
    exact_total = base + increment * n_steps

    naive = truncate_like(base, places)
    vis_inc = truncate_like(increment, places)
    for _ in range(n_steps):
        naive = naive_decimal_add(naive, vis_inc, places)

    acc = DualZero.from_exact_decimal(base, places)
    inc_dz = DualZero.from_exact_decimal(increment, places)
    for _ in range(n_steps):
        acc = acc + inc_dz

    return ClockSumResult(
        n_steps=n_steps,
        base=base,
        increment=increment,
        exact_total=exact_total,
        naive_total=naive,
        dual_restored=acc.exact(),
        dual_visible=acc.visible,
        lost_by_naive=exact_total - naive,
        restored_minus_exact=acc.exact() - exact_total,
        kind=f"decimal/{places}",
    )


def truncate_like(q: Fraction, places: int) -> Fraction:
    from .pairing import truncate_decimal_places

    return truncate_decimal_places(q, places)


# ---------------------------------------------------------------------------
# 1-D ballistic / constant-thrust rocket, explicit Euler
# ---------------------------------------------------------------------------

@dataclass
class TrajectoryResult:
    name: str
    kind: str
    n_steps: int
    dt: Fraction
    # Recurrence results (same Euler scheme)
    naive_x: Fraction
    naive_v: Fraction
    dual_x: Fraction
    dual_v: Fraction
    exact_euler_x: Fraction
    exact_euler_v: Fraction
    # Closed form of the *physical* ODE (not of Euler)
    analytic_x: Fraction
    analytic_v: Fraction
    rounding_drift_x: Fraction  # |naive - exact Euler|
    dual_minus_euler_x: Fraction  # |Dual-Zero restored - exact Euler|, should be 0
    discretization_error_x: Fraction  # |exact Euler - analytic|


def _analytic(x0: Fraction, v0: Fraction, acc: Fraction, t: Fraction) -> tuple[Fraction, Fraction]:
    """x = x0 + v0 t + (1/2) a t²,  v = v0 + a t.  Constant acceleration."""
    return x0 + v0 * t + (acc * t * t) / 2, v0 + acc * t


def euler_trajectory(
    name: str,
    kind: str,
    x0: Fraction,
    v0: Fraction,
    acc: Fraction,
    dt: Fraction,
    n_steps: int,
    places: int | None = None,
) -> TrajectoryResult:
    """Explicit Euler: v += a dt, x += v dt (velocity already updated: semi-implicit).

    Using semi-implicit Euler (v first) is a fixed choice of scheme, used
    identically in all three arithmetics.  Changing the scheme would change
    discretization error; Dual-Zero is not asked to do that.
    """
    t = dt * n_steps
    analytic_x, analytic_v = _analytic(x0, v0, acc, t)

    # Exact-Fraction Euler
    x_e, v_e = x0, v0
    for _ in range(n_steps):
        v_e = v_e + acc * dt
        x_e = x_e + v_e * dt

    if kind == "float64":
        x_n = float(x0)
        v_n = float(v0)
        a_f = float(acc)
        dt_f = float(dt)
        for _ in range(n_steps):
            v_n = v_n + a_f * dt_f
            x_n = x_n + v_n * dt_f
        naive_x = Fraction.from_float(x_n)
        naive_v = Fraction.from_float(v_n)

        x_d = DualZero.from_exact_float64(x0)
        v_d = DualZero.from_exact_float64(v0)
        a_d = DualZero.from_exact_float64(acc)
        dt_d = DualZero.from_exact_float64(dt)
        for _ in range(n_steps):
            v_d = v_d + a_d * dt_d
            x_d = x_d + v_d * dt_d
        dual_x, dual_v = x_d.exact(), v_d.exact()
    elif kind == "decimal":
        if places is None:
            raise ValueError("decimal trajectory needs places")
        x_n = truncate_like(x0, places)
        v_n = truncate_like(v0, places)
        a_t = truncate_like(acc, places)
        dt_t = truncate_like(dt, places)
        for _ in range(n_steps):
            v_n = truncate_like(v_n + a_t * dt_t, places)
            x_n = truncate_like(x_n + v_n * dt_t, places)
        naive_x, naive_v = x_n, v_n

        x_d = DualZero.from_exact_decimal(x0, places)
        v_d = DualZero.from_exact_decimal(v0, places)
        a_d = DualZero.from_exact_decimal(acc, places)
        dt_d = DualZero.from_exact_decimal(dt, places)
        for _ in range(n_steps):
            v_d = v_d + a_d * dt_d
            x_d = x_d + v_d * dt_d
        dual_x, dual_v = x_d.exact(), v_d.exact()
    else:
        raise ValueError("kind must be float64 or decimal")

    return TrajectoryResult(
        name=name,
        kind=kind if places is None else f"decimal/{places}",
        n_steps=n_steps,
        dt=dt,
        naive_x=naive_x,
        naive_v=naive_v,
        dual_x=dual_x,
        dual_v=dual_v,
        exact_euler_x=x_e,
        exact_euler_v=v_e,
        analytic_x=analytic_x,
        analytic_v=analytic_v,
        rounding_drift_x=abs(naive_x - x_e),
        dual_minus_euler_x=abs(dual_x - x_e),
        discretization_error_x=abs(x_e - analytic_x),
    )


def ballistic_float64(
    x0: Fraction = Fraction(6_400_000),  # Earth-scale coordinate, metres
    v0: Fraction = Fraction(100),
    g: Fraction = Fraction("9.80665"),
    dt: Fraction = Fraction(1, 1000),
    n_steps: int = 100_000,  # T = 100 s
) -> TrajectoryResult:
    """Constant gravity, no thrust.  Large position so float64 ULPs are coarser."""
    return euler_trajectory("ballistic", "float64", x0, v0, -g, dt, n_steps)


def rocket_decimal(
    x0: Fraction = Fraction(0),
    v0: Fraction = Fraction(0),
    thrust_over_mass: Fraction = Fraction(20),  # m/s², net before gravity
    g: Fraction = Fraction("9.80665"),
    dt: Fraction = Fraction(1, 100),
    n_steps: int = 20_000,  # T = 200 s
    places: int = 6,
) -> TrajectoryResult:
    """Constant specific thrust minus g, in 6-place decimal (truncation)."""
    acc = thrust_over_mass - g
    return euler_trajectory("rocket", "decimal", x0, v0, acc, dt, n_steps, places=places)


def rocket_float64(
    x0: Fraction = Fraction(6_400_000),
    v0: Fraction = Fraction(0),
    thrust_over_mass: Fraction = Fraction(20),
    g: Fraction = Fraction("9.80665"),
    dt: Fraction = Fraction(1, 1000),
    n_steps: int = 100_000,
) -> TrajectoryResult:
    acc = thrust_over_mass - g
    return euler_trajectory("rocket", "float64", x0, v0, acc, dt, n_steps)


def as_float(q: Fraction) -> float:
    return float(q)
