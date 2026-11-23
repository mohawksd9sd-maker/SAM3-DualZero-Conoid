"""Search for a mechanism that fixes flux M=3 and the moduli of Σ.

Exploratory, not part of the locked SAM-3 core.

Each candidate is checked and given a verdict.  Null results stay null.
Number-matching that is only a count is flagged as numerology.

The exact Dirac spectrum on a flat magnetized T² is standard (CIM,
hep-th/0404229, and the Landau-level analysis on T²): for flux M > 0
and area A,

    dim ker D_+ = M,   dim ker D_- = 0,
    E_n = ± sqrt(4π n |M| / A),   n = 1, 2, ... ,

with degeneracy |M| at each signed level.  The heat kernel is therefore
closed-form:

    Tr exp(-t D_Σ²) = |M| coth(2π t |M| / A).

This is checked against the small-t Weyl limit A/(2π t) and is used to
test whether the spectral action selects M=3 or a particular area.
"""

from __future__ import annotations

import math
from typing import Callable, Dict, List, Optional, Tuple


def landau_energies(n_max: int, flux: int, area: float) -> List[float]:
    """Positive Landau energies E_n = sqrt(4π n |M| / A), n=1..n_max."""
    if flux == 0:
        return []
    if area <= 0:
        raise ValueError("area must be positive")
    m = abs(int(flux))
    pref = math.sqrt(4.0 * math.pi * m / area)
    return [pref * math.sqrt(n) for n in range(1, n_max + 1)]


def heat_kernel_exact(t: float, flux: int, area: float) -> float:
    """Tr e^{-t D²} = |M| coth(2π t |M| / A) for M ≠ 0.

    For M=0 the constant-flux formula does not apply (no gap, continuous
    torus momenta).  We do not use M=0 as a special closed form here
    beyond the Weyl term.
    """
    if t <= 0 or area <= 0:
        raise ValueError("t and area must be positive")
    m = abs(int(flux))
    if m == 0:
        raise ValueError("exact coth formula requires M != 0")
    x = 2.0 * math.pi * t * m / area
    # coth(x) = cosh/sinh, stable for moderate x; for tiny x use 1/x + x/3
    if x < 1e-8:
        return m * (1.0 / x + x / 3.0)
    return m * math.cosh(x) / math.sinh(x)


def heat_kernel_weyl_leading(t: float, area: float) -> float:
    """Leading small-t term A/(2π t) for a 2-component 2D Dirac operator."""
    return area / (2.0 * math.pi * t)


def heat_kernel_from_spectrum(t: float, flux: int, area: float, n_max: int = 400) -> float:
    """Direct sum over Landau levels, as a check of the coth formula."""
    m = abs(int(flux))
    zero = float(m)
    pos = landau_energies(n_max, flux, area)
    return zero + 2.0 * m * sum(math.exp(-t * e * e) for e in pos)


def spectral_action_cutoff(
    flux: int,
    area: float,
    lam: float,
    f: Optional[Callable[[float], float]] = None,
    n_max: Optional[int] = None,
) -> float:
    """Tr f(D/Λ) for the magnetized torus, with a stated cutoff function.

    Default f(x) = exp(-x²), a standard positive even test function.
    The sum is cut at a level where E_n / Λ is large enough that f is
    negligible, or at a stated n_max.
    """
    if lam <= 0 or area <= 0:
        raise ValueError("Λ and area must be positive")
    if f is None:
        def f(x: float) -> float:
            return math.exp(-x * x)
    m = abs(int(flux))
    if m == 0:
        # No discrete Landau tower; we do not invent a spectral action
        # for the untwisted torus here (continuous momenta, area-dependent
        # Weyl term only).  Return a sentinel and let the caller handle M=0.
        return float("nan")
    if n_max is None:
        # f(sqrt(4π n M / A)/Λ) = exp(-4π n M /(A Λ²)); go until exponent ~ 40
        denom = 4.0 * math.pi * m / (area * lam * lam)
        n_max = max(20, int(40.0 / max(denom, 1e-12)) + 5)
        n_max = min(n_max, 20000)
    total = m * f(0.0)
    for n in range(1, n_max + 1):
        e = math.sqrt(4.0 * math.pi * n * m / area)
        total += 2.0 * m * f(e / lam)
    return total


def action_density_per_conoid_area(
    flux: int,
    area_sigma: float,
    lam: float,
    area_X: float = 1.0,
) -> Dict[str, float]:
    """A schematic action *density* used only to test minimization over (M, A).

    Because vol(Y) and the flux term diverge with Area(X), it is the
    density per unit Area(X) that could conceivably be extremized over
    the moduli of Σ.  We take:

        s = Tr f(D_Σ / Λ)   +   c_YM * (2π M)² / Area(Σ)

    The first piece is the exact Σ spectral action (already contains the
    Landau tower / flux).  The second is *not* added in the genuine
    product spectral action (that would double-count); it is recorded
    separately so one can see that an extra Maxwell term, if anyone
    included it, is also minimized at M=0.  Default f(x)=exp(-x²).
    """
    sa = spectral_action_cutoff(flux, area_sigma, lam)
    ym = (2.0 * math.pi * flux) ** 2 / area_sigma
    return {
        "Tr_f_D_Sigma": sa,
        "maxwell_M2_over_A": ym,
        "sum_if_double_counted": sa + ym,
        "area_X_used_only_as_a_unit": area_X,
    }


def scan_flux_and_area(
    lam: float = 1.0,
    fluxes: Tuple[int, ...] = (1, 2, 3, 4, 5, 6),
    areas: Tuple[float, ...] = (0.25, 0.5, 1.0, 2.0, 4.0, 8.0),
) -> Dict[str, object]:
    """Scan Tr f(D_Σ/Λ) over integer flux and area, in units Λ = 1.

    Areas are in units of 1/Λ².  The scan is a search for a local minimum
    at (M,A)=(3, A_*).  We also record, at each fixed area, which M
    minimizes the action, and at each fixed M, whether the action is
    monotone in A.
    """
    table = []
    for a in areas:
        row = {"area": a, "by_flux": {}}
        for m in fluxes:
            row["by_flux"][str(m)] = spectral_action_cutoff(m, a, lam)
        table.append(row)

    minimizer_at_fixed_area = []
    for row in table:
        best_m = min(fluxes, key=lambda m: row["by_flux"][str(m)])
        minimizer_at_fixed_area.append({"area": row["area"], "argmin_M": int(best_m)})

    monotone_in_area = {}
    for m in fluxes:
        vals = [row["by_flux"][str(m)] for row in table]
        increasing = all(vals[i] <= vals[i + 1] + 1e-12 for i in range(len(vals) - 1))
        decreasing = all(vals[i] >= vals[i + 1] - 1e-12 for i in range(len(vals) - 1))
        monotone_in_area[str(m)] = {
            "values": vals,
            "nondecreasing_in_A": increasing,
            "nonincreasing_in_A": decreasing,
        }

    any_min_at_3 = any(item["argmin_M"] == 3 for item in minimizer_at_fixed_area)
    # The global minimum on the scanned grid
    best = min(
        ((row["area"], m, row["by_flux"][str(m)]) for row in table for m in fluxes),
        key=lambda z: z[2],
    )
    return {
        "cutoff_function": "exp(-x^2)",
        "Lambda": lam,
        "table": table,
        "minimizer_at_fixed_area": minimizer_at_fixed_area,
        "any_fixed_area_prefers_M_3": any_min_at_3,
        "all_fixed_area_prefers_minimal_M": all(
            item["argmin_M"] == min(fluxes) for item in minimizer_at_fixed_area
        ),
        "monotone_in_area": monotone_in_area,
        "grid_minimum": {"area": best[0], "M": best[1], "value": best[2]},
        "grid_minimum_is_M_3": best[1] == 3,
    }


def attempt_dirac_quantization() -> Dict[str, object]:
    return {
        "attempt": "Dirac quantization",
        "gives": "M ∈ Z",
        "selects_3": False,
        "note": "The smallest positive integer is 1, not 3.",
        "verdict": "failed",
    }


def attempt_anomaly_cancellation() -> Dict[str, object]:
    return {
        "attempt": "Anomaly cancellation",
        "selects_3": False,
        "reason": (
            "In the product with a single U(1) bundle on Σ, every PS "
            "representation in one generation is tensored with the same "
            "space of zero modes, so all gauge representations have the "
            "same multiplicity M.  The Pati-Salam (and SM) one-generation "
            "content is already anomaly-free; copying it M times remains "
            "anomaly-free for every integer M.  There is no condition that "
            "forces M=3.  (Relative fluxes for different representations "
            "are not part of this product: they would be an extra choice, "
            "and even then anomaly cancellation constrains linear combinations, "
            "not a unique M=3, and is not derived from the locked conoid.)"
        ),
        "verdict": "failed",
    }


def attempt_ko_and_J() -> Dict[str, object]:
    return {
        "attempt": "KO-dimension or the real structure J",
        "selects_3": False,
        "reason": (
            "KO-dimension of Y × F is 2+2+6 ≡ 2, independently of the "
            "choice of connection on Σ.  J is the product real structure "
            "and does not see the integer flux."
        ),
        "verdict": "failed",
    }


def attempt_tadpole() -> Dict[str, object]:
    return {
        "attempt": "Tadpole / equation of motion for the background flux",
        "selects_3": False,
        "reason": (
            "There is no string-theory tadpole condition in the spectral "
            "action of Y × F_PS; imposing one would be an import from a "
            "different framework, not derived here.  The Maxwell equation "
            "d * F = 0 is satisfied by a constant flux on T² or a monopole "
            "on S², for every integer M.  That is quantization plus a "
            "classical solution, not a selection of 3."
        ),
        "verdict": "failed",
    }


def attempt_tip_length_or_C4() -> Dict[str, object]:
    """Matching 8ℓ0 or C4 to the torus lattice.

    These are recorded in order to reject them as unprincipled.
    """
    tip = 8.0  # in units ℓ0 = 1
    coincidences = [
        {
            "match": "tip length 8ℓ0 = 2π R  ⇒  R = 4ℓ0/π",
            "flag": (
                "numerology / unprincipled: the tip circle is a boundary of "
                "the conoid factor, not a cycle of the torus factor.  There "
                "is no identification of those circles in the product metric."
            ),
        },
        {
            "match": "C4 is an isometry of the square torus τ=i",
            "flag": (
                "The C4 of the locked conoid rotates the conoid's angular "
                "coordinate, not a coordinate of Σ.  The product isometry "
                "group is C4(X) × Isom(Σ).  Requiring Isom(Σ) to contain a "
                "C4 (i.e. τ=i, up to SL(2,Z)) is a symmetry wish, not a "
                "consistency condition of the product, and even then it "
                "fixes at most the shape of T², not the flux."
            ),
        },
        {
            "match": "12-bridge spacing 2π/12 against 3 generations",
            "flag": "numerology, already rejected in doc 47; the 12-bridge spacing is a convention",
        },
    ]
    return {
        "attempt": "Matching the tip length 8ℓ0 or C4 to the torus lattice",
        "tip_length_over_ell0": tip,
        "selects_flux_3": False,
        "selects_moduli_uniquely": False,
        "coincidences": coincidences,
        "verdict": "failed (unprincipled / numerology)",
    }


def attempt_conoid_curvature_as_flux() -> Dict[str, object]:
    return {
        "attempt": "Identify |∫_X K dA| / 2π = 1 with the flux on Σ",
        "gives": 1,
        "selects_3": False,
        "flag": (
            "Even as an identification, this would give flux 1, not 3.  "
            "Treating the curvature of the conoid as a flux on a different "
            "factor is not forced by the product connection."
        ),
        "verdict": "failed",
    }


def attempt_spectral_minimization(lam: float = 1.0) -> Dict[str, object]:
    scan = scan_flux_and_area(lam=lam)
    return {
        "attempt": "Minimization of the magnetized-T² spectral action over (M, A)",
        "selects_3": False,
        "selects_a_unique_area": False,
        "scan": scan,
        "analytic_reason": (
            "The exact heat kernel is |M| coth(2π t |M|/A) = A/(2π t) + "
            "(2π t M²)/(3A) + O(t³).  The first M-dependent term is "
            "positive and minimized, at fixed area, by the smallest |M|.  "
            "The Weyl term A/(2π t) grows with A.  For a positive cutoff "
            "function the spectral action therefore prefers smaller |M| "
            "and has no interior minimum at M=3.  τ does not enter the "
            "spectrum of a constant-flux Dirac operator on a flat torus, "
            "so this action cannot fix the complex structure either."
        ),
        "wilson_lines": (
            "A common Wilson line is a translation and does not change "
            "eigenvalues.  Relative Wilson lines among several stacks "
            "are not present in a single-bundle product; they would be "
            "an extra choice and affect Yukawas, not the Dirac spectrum "
            "of one bundle."
        ),
        "S2": (
            "On S² the local small-t expansion is the same in structure: "
            "the leading volume term 4π R² / (2π t), a curvature term "
            "fixed by χ=2, and a monopole term that costs energy ~ n² / R².  "
            "The distinguished bundles (Hopf, n=1; tangent, n=2) are not "
            "n=3, and the energy cost prefers smaller |n| at fixed R.  "
            "We do not invent an exact monopole-harmonic spectral action "
            "beyond this local argument and the index n."
        ),
        "verdict": "failed",
    }


def report() -> Dict[str, object]:
    attempts = [
        attempt_dirac_quantization(),
        attempt_anomaly_cancellation(),
        attempt_ko_and_J(),
        attempt_tadpole(),
        attempt_tip_length_or_C4(),
        attempt_conoid_curvature_as_flux(),
        attempt_spectral_minimization(),
    ]
    return {
        "exploratory": True,
        "locked_core": False,
        "any_attempt_fixes_flux_3": False,
        "any_attempt_fixes_moduli_uniquely": False,
        "attempts": attempts,
        "headline": (
            "Nothing in the combined geometry fixes the flux to 3, or "
            "uniquely fixes the area, complex structure, or Wilson lines "
            "of Σ.  The spectral action of a magnetized torus prefers "
            "smaller |M|, not M=3, and does not depend on τ."
        ),
    }
