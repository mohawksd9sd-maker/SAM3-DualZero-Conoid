"""Declared-list numerical coincidences with the recorded SAM-3 constants.

Exploratory: not part of the locked SAM-3 core.

Targets (inputs or locked constants, not outputs to be fitted):
  - ω0 ≈ 0.927, quoted to three digits in docs 18 and 42, and not derived.
  - the exponent 4/13, also not derived.
  - the integer 3, as a generation count.

Source numbers are predeclared: locked geometric constants of the conoid,
plus the new spectral/modular numbers of docs 49–50.  The integer 13 is
*not* included among the sources, because it appears only inside the
underived exponent 4/13.  The recorded (also underived) bridge scale
D=2π/12 is included and flagged.

A hit is reported if the relative error is < 0.5%, or, for the
three-digit target 0.927, if the absolute error is < 0.001 (half a unit
in the last quoted digit).  Because many simple combinations are
compared, a hit is a coincidence until a derivation exists; the size of
the search is reported (look-elsewhere).
"""

from __future__ import annotations

import itertools
import math
from typing import Dict, List, Tuple

# --- predeclared sources ------------------------------------------------------

def source_constants() -> Dict[str, float]:
    return {
        "pi": math.pi,
        "e": math.e,
        "ln2": math.log(2.0),
        "C0": 2.0 * math.pi * math.log(2.0),
        "int_K": -2.0 * math.pi,
        "tip_over_ell0": 8.0,
        "n_nodes": 4.0,
        "C4_order": 4.0,
        "D_bridge_recorded": 2.0 * math.pi / 12.0,  # not derived; uses 12
        "F_i": _F_i(),
        "F_rho": _F_rho(),
        "abs_eta_i": _abs_eta_i(),
        "one_over_2e": 1.0 / (2.0 * math.e),
        "sqrt2": math.sqrt(2.0),
        "sqrt3": math.sqrt(3.0),
    }


def _abs_eta_i() -> float:
    # Dedekind product at τ=i; a few terms suffice (Im τ = 1).
    q = math.exp(-2.0 * math.pi)
    log_eta = -2.0 * math.pi / 24.0
    qn = q
    for _ in range(80):
        log_eta += math.log(1.0 - qn)
        qn *= q
        if qn < 1e-18:
            break
    return math.exp(log_eta)


def _F_i() -> float:
    return 1.0 * (_abs_eta_i() ** 2)  # √(Im i)=1


def _F_rho() -> float:
    # τ = -1/2 + i √3/2, η from the product, F = √(Im τ) |η|²
    tau_im = math.sqrt(3.0) / 2.0
    # q = exp(2πi τ) = exp(2πi(-1/2) - 2π √3/2) = -exp(-π √3)
    abs_q = math.exp(-math.pi * math.sqrt(3.0))
    # |η| = |q|^{1/24} * ∏ |1-q^n|; q is negative real.
    q = -abs_q
    log_abs = math.log(abs_q) / 24.0
    qn = q
    for _ in range(80):
        log_abs += math.log(abs(1.0 - qn))
        qn *= q
        if abs(qn) < 1e-18:
            break
    return math.sqrt(tau_im) * math.exp(2.0 * log_abs)


TARGETS = {
    "omega0_quoted": 0.927,
    "four_thirteenths": 4.0 / 13.0,
    "three": 3.0,
}


def combinations(sources: Dict[str, float]) -> List[Tuple[str, float, str]]:
    """Predeclared simple combinations: (name, value, note)."""
    out: List[Tuple[str, float, str]] = []
    items = list(sources.items())
    # The numbers themselves (absolute value, for int_K).
    for n, v in items:
        out.append((n, v, "source"))
        if v < 0:
            out.append((f"|{n}|", abs(v), "abs"))
        if v > 0 and abs(v - 1.0) > 1e-15:
            out.append((f"1/{n}", 1.0 / v, "reciprocal"))
            out.append((f"sqrt(|{n}|)" if v < 0 else f"sqrt({n})", math.sqrt(abs(v)), "sqrt"))
            if v > 0:
                out.append((f"ln({n})" if v > 1 else f"ln(1/{n}) if {n}<1", math.log(v) if v > 1 else math.log(1.0 / v), "log"))
                out.append((f"exp(-{n})", math.exp(-v), "exp_minus"))
    # Ratios of two distinct positive sources.
    pos = [(n, v) for n, v in items if v > 0]
    for (n1, v1), (n2, v2) in itertools.combinations(pos, 2):
        out.append((f"{n1}/{n2}", v1 / v2, "ratio"))
        out.append((f"{n2}/{n1}", v2 / v1, "ratio"))
        out.append((f"({n1}/{n2})^(4/13)", (v1 / v2) ** (4.0 / 13.0), "ratio_to_4_13"))
        # The last family uses the underived exponent as a *probe*, and is
        # flagged; a hit here would still not derive 4/13.
    # A few linear combos of O(1) numbers that already appear as sums of
    # geometric quantities (not an open-ended polynomial search).
    if "F_i" in sources and "F_rho" in sources:
        out.append(("F_rho - F_i", sources["F_rho"] - sources["F_i"], "difference"))
        out.append(("F_rho / F_i", sources["F_rho"] / sources["F_i"], "ratio"))
    return out


def classify(value: float, target: float, target_name: str) -> str:
    if abs(target) < 1e-15:
        return "skip"
    rel = abs(value - target) / abs(target)
    if target_name == "omega0_quoted" and abs(value - target) < 0.001:
        return "abs_hit_on_3_digit_target"
    if rel < 0.005:
        return "rel_hit_0.5pct"
    if rel < 0.02:
        return "near_2pct"
    return "no"


def scan() -> Dict[str, object]:
    sources = source_constants()
    combos = combinations(sources)
    hits = []
    nears = []
    for name, val, kind in combos:
        for tname, tval in TARGETS.items():
            tag = classify(val, tval, tname)
            rec = {
                "expression": name,
                "value": val,
                "target": tname,
                "target_value": tval,
                "rel_error": abs(val - tval) / abs(tval),
                "abs_error": abs(val - tval),
                "kind": kind,
                "tag": tag,
            }
            if tag in ("abs_hit_on_3_digit_target", "rel_hit_0.5pct"):
                hits.append(rec)
            elif tag == "near_2pct":
                nears.append(rec)
    # Exact integer 3 among sources or simple integer counts already known:
    exact_3 = [h for h in hits if h["target"] == "three" and h["abs_error"] < 1e-12]
    return {
        "n_sources": len(sources),
        "n_combinations": len(combos),
        "n_comparisons": len(combos) * len(TARGETS),
        "sources": sources,
        "hits": hits,
        "near_misses_2pct": nears,
        "exact_hits_on_integer_3": exact_3,
        "look_elsewhere": (
            f"{len(combos)} predeclared combinations were compared to "
            f"{len(TARGETS)} targets ({len(combos)*len(TARGETS)} tests).  "
            "A hit at the 0.5% level is a coincidence until it has a derivation; "
            "the three-digit target 0.927 is particularly loose."
        ),
    }


def report() -> Dict[str, object]:
    s = scan()
    return {
        "n_sources": s["n_sources"],
        "n_combinations": s["n_combinations"],
        "n_comparisons": s["n_comparisons"],
        "sources": s["sources"],
        "n_hits": len(s["hits"]),
        "hits": s["hits"],
        "n_near_misses_2pct": len(s["near_misses_2pct"]),
        "near_misses_2pct": s["near_misses_2pct"],
        "exact_hits_on_integer_3": s["exact_hits_on_integer_3"],
        "look_elsewhere": s["look_elsewhere"],
        "verdict": (
            "Any numerical proximity of a predeclared combination to the "
            "quoted ω0≈0.927, to 4/13, or to 3 is a coincidence until it is "
            "derived.  The search size is reported.  No such proximity is "
            "promoted to a derivation here."
        ),
    }
