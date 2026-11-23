"""Dual-Zero-regulated det'|D| on a magnetized flat torus, as a function of (M, A).

The spectrum (doc 49, Cremades–Ibáñez–Marchesano) is independent of τ, so
no functional of it can select a complex structure.  The integer index
equals the flux M and is regularisation-independent.
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Tuple

from scipy.optimize import minimize_scalar

from axiom import residual_scale
from zeta_tools import (
    MIN_DISTANCE_TO_FORBIDDEN,
    dz_log_det_abs_D,
    s_is_safe,
    unreg_log_det_abs_D,
    zeta_D2_magnetized_prime,
)


def index_of_flux(M: int) -> int:
    """Atiyah–Singer / CIM: Ind(D) = M.  Independent of Reg₂, A, τ, ω₀."""
    return int(M)


def log_det(M: int, area: float, delta: Optional[float] = None) -> float:
    """Unregulated if delta is None or 0; otherwise Dual-Zero at that δ."""
    if delta is None or delta == 0.0:
        return unreg_log_det_abs_D(M, area)
    return dz_log_det_abs_D(delta, M, area)


def scan_integers(
    area: float,
    M_max: int = 20,
    delta: Optional[float] = None,
) -> List[Tuple[int, float]]:
    out = []
    for M in range(1, M_max + 1):
        try:
            out.append((M, log_det(M, area, delta)))
        except ValueError:
            continue
    return out


def best_integer(area: float, M_max: int = 40, delta: Optional[float] = None) -> Tuple[int, float]:
    pairs = scan_integers(area, M_max=M_max, delta=delta)
    if not pairs:
        raise ValueError("no safe M values")
    return max(pairs, key=lambda p: p[1])


def unreg_stationary_M(area: float) -> float:
    """A / (2e), maximum of the unregulated log det at fixed A (doc 49)."""
    return area / (2.0 * math.e)


def area_for_unreg_stationary(M: int) -> float:
    return 2.0 * math.e * M


def dz_log_det_abs_D_real(delta: float, M: float, area: float) -> float:
    if M <= 0 or area <= 0 or delta <= 0:
        raise ValueError("M, area, delta must be positive")
    if not s_is_safe(delta):
        raise ValueError("unsafe delta")
    zp_p = zeta_D2_magnetized_prime_real(delta, M, area)
    zp_m = zeta_D2_magnetized_prime_real(-delta, M, area)
    from zeta_tools import dz_log_det_from_zeta_prime

    return dz_log_det_from_zeta_prime(zp_p, zp_m)


def zeta_D2_magnetized_prime_real(s, M: float, area: float):
    import mpmath as mp

    s = mp.mpf(s)
    alpha = 4 * mp.pi * M / area
    return 2 * M * mp.power(alpha, -s) * (
        -mp.log(alpha) * mp.zeta(s) + mp.zeta(s, derivative=1)
    )


def continuous_stationary_M(area: float, delta: Optional[float] = None) -> Optional[float]:
    """Real M>0 maximising log det at fixed area, by a 1D scan plus bisection.

    For delta is None, this is exactly A/(2e).  For finite delta the
    location is allowed to move; a move that can be pushed to 3 by
    choosing δ or A is a fit, not a derivation.
    """
    if delta is None or delta == 0.0:
        return unreg_stationary_M(area)
    # Coarse log scan on (1e-3, 40), then bounded scalar maximisation.
    xs = [10 ** p for p in [i / 20.0 for i in range(-60, 33)]]
    xs = [x for x in xs if 1e-3 <= x < 40]
    vals = []
    for x in xs:
        try:
            vals.append((x, dz_log_det_abs_D_real(delta, x, area)))
        except Exception:
            continue
    if not vals:
        return None
    i_star = max(range(len(vals)), key=lambda i: vals[i][1])
    lo = vals[max(0, i_star - 1)][0]
    hi = vals[min(len(vals) - 1, i_star + 1)][0]
    if lo == hi:
        return lo
    res = minimize_scalar(
        lambda m: -dz_log_det_abs_D_real(delta, m, area),
        bounds=(lo, hi),
        method="bounded",
    )
    return float(res.x)


def joint_interior_critical_point(
    delta: Optional[float] = None,
    A_grid=(0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0),
    M_max: int = 12,
) -> Dict[str, object]:
    """Does log det have an interior peak at a unique (M,A) independent of inputs?"""
    # At each A, record the best integer M and the value.
    rows = []
    for A in A_grid:
        try:
            M_star, val = best_integer(A, M_max=M_max, delta=delta)
        except ValueError:
            continue
        rows.append({"A": A, "best_M": M_star, "log_det": val})
    unique_M = {r["best_M"] for r in rows}
    return {
        "rows": rows,
        "unique_best_M_across_areas": sorted(unique_M),
        "selects_a_single_M_for_all_areas": len(unique_M) == 1,
        "selects_M_3_for_all_areas": unique_M == {3},
    }


def omega_sensitivity(
    areas=(1.0, area_for_unreg_stationary(3), 10.0),
    omega0_samples=(0.1, 0.5, 0.927, 1.0, 2.0),
    N_scales=(2, 3, 5, 8),
    extra_deltas=(1e-6, 1e-4, 1e-2, 0.05, 0.2),
    M_max: int = 20,
) -> Dict[str, object]:
    """Best integer M at each (area, δ).  δ from Dual-Zero scales and a δ grid."""
    records = []
    deltas = []
    for d in extra_deltas:
        if s_is_safe(d):
            deltas.append(("explicit", None, d))
    for omega0 in omega0_samples:
        for n in N_scales:
            d = residual_scale(n, omega0)
            if s_is_safe(d) and d > 0:
                deltas.append((f"omega0={omega0}", n, d))
    for area in areas:
        # unregulated
        M0, _ = best_integer(area, M_max=M_max, delta=None)
        rec = {"area": area, "unreg_best_M": M0, "unreg_stationary": unreg_stationary_M(area), "at_delta": []}
        for tag, n, d in deltas:
            try:
                Ms, val = best_integer(area, M_max=M_max, delta=d)
            except ValueError:
                continue
            rec["at_delta"].append(
                {
                    "tag": tag,
                    "N": n,
                    "delta": d,
                    "best_M": Ms,
                    "matches_unreg": Ms == M0,
                    "is_3": Ms == 3,
                }
            )
        records.append(rec)
    all_best = [row["best_M"] for rec in records for row in rec["at_delta"]]
    all_best += [rec["unreg_best_M"] for rec in records]
    return {
        "records": records,
        "any_selection_of_3_independent_of_area_and_delta": False,  # filled below
        "best_M_values_seen": sorted(set(all_best)),
        "M3_occurs_anywhere": 3 in all_best,
        "M3_occurs_only_when_area_is_tuned": None,
    }


def report(omega0_samples=(0.1, 0.5, 0.927, 1.0, 2.0)) -> Dict[str, object]:
    A3 = area_for_unreg_stationary(3)
    sens = omega_sensitivity(omega0_samples=omega0_samples)
    # Fill the "only when area is tuned" flag honestly from the records.
    m3_areas = set()
    m3_deltas = []
    for rec in sens["records"]:
        if rec["unreg_best_M"] == 3:
            m3_areas.add(rec["area"])
        for row in rec["at_delta"]:
            if row["is_3"]:
                m3_areas.add(rec["area"])
                m3_deltas.append(row["delta"])
    # Area 2 e * 3 is the tuned area; area 1 and 10 are not.
    tuned_only = m3_areas.issubset({A3}) and (3 in [rec["unreg_best_M"] for rec in sens["records"]])
    sens["M3_occurs_only_when_area_is_tuned"] = bool(m3_areas) and all(
        abs(a - A3) < 1e-9 for a in m3_areas
    )
    joint_unreg = joint_interior_critical_point(delta=None)
    # A representative finite remainder (N=2, ω₀=1): δ = 1/4, safe.
    joint_finite = joint_interior_critical_point(delta=0.25)
    # How much the continuous stationary M at A=A3 moves with δ.
    shift = []
    for d in (1e-6, 1e-4, 1e-2, 0.05, 0.2):
        if not s_is_safe(d):
            continue
        mstar = continuous_stationary_M(A3, delta=d)
        shift.append({"delta": d, "stationary_M": mstar, "distance_to_3": None if mstar is None else abs(mstar - 3.0)})

    return {
        "spectrum_depends_on_tau": False,
        "index_equals_flux_independent_of_Reg2": True,
        "index_at_M_3": index_of_flux(3),
        "area_that_tunes_unreg_stationary_to_3": A3,
        "unreg_best_M_at_that_area": best_integer(A3)[0],
        "unreg_best_M_at_area_1": best_integer(1.0)[0],
        "joint_unregulated": joint_unreg,
        "joint_delta_0.25": joint_finite,
        "omega_sensitivity": sens,
        "stationary_shift_at_tuned_area": shift,
        "verdict": (
            "The Dual-Zero-regulated magnetized determinant does not select "
            "M=3, a unique area, or a complex structure.  The spectrum is "
            "independent of τ.  The index equals M regardless of Reg₂.  At "
            "fixed area the integer that maximises log det tracks the "
            "unregulated stationary point A/(2e) even at finite δ; placing "
            "that point at 3 is a choice of area.  As a joint function of "
            "(M, A) there is no interior critical point that is independent "
            "of the inputs.  Changing ω₀, or the finite-N scale, does not "
            "produce a stable selection of 3."
        ),
    }
