#!/usr/bin/env python3
"""Scheme-by-scheme recompute of α in G_N = α ℓ0².

Structural relation (math notes 09 and 14; Chamseddine–Connes 1997 for the
origin of the spectral action, not for a unique α on this metric):

    1/(2 κ²) = C_SA * φ2 * Λ² * Vol_reg(F)
    G_N = κ² / (8π) = ℓ0² / (16π C_SA φ2 Vol_reg)     when Λ = 1/ℓ0
    α = 1 / (16π C_SA φ2 Vol_reg)

Every factor is named. Different cutoff functions change φ2. Different
volume regularisations change Vol_reg. C_SA is a Seeley combinatorial
factor; we do not invent a unique value of C_SA for this conoid. We
tabulate α under stated choices, and we record the locked 64π/45 only as
the convention that is equivalent to fixing
    C_SA φ2 Vol_reg = 45/(1024 π²).

The 4D almost-commutative SM Einstein–Hilbert coefficient of
Chamseddine–Connes–Marcolli (e.g. Connes, Séminaire Poincaré X (2007),
eq. (40)–(44)) includes the finite SM Hilbert space and is not a scheme
for the conoid; it is not used to produce an α here.

A 6D product heat-kernel computation of C_SA is not claimed: the Gilkey
a2 convention (sign of E, overall 2 Λ^{n-2} f_{n-2} prefactor) was not
independently settled in this pass to a unique number, so no fake 6D α
is reported.
"""
from __future__ import annotations

import math
from typing import Callable, Dict, List

C0_EXACT = 2.0 * math.pi * math.log(2.0)  # theorem, unit metric
LOCKED_ALPHA = 64.0 * math.pi / 45.0
LOCKED_PRODUCT = 45.0 / (1024.0 * math.pi ** 2)


def phi_moments(name: str) -> Dict[str, float]:
    """Cutoff moments f_k = ∫_0^∞ f(v) v^{k-1} dv, f_0=f(0), for even f.

    These are the CCM / van Suijlekom conventions (f2, f4, f0).
    """
    if name == "sharp_[0,1]":
        # f(v)=1 for v≤1, 0 otherwise (not smooth; moments still defined)
        return {"name": name, "f0": 1.0, "f2": 0.5, "f4": 0.25, "note": "characteristic function, not smooth"}
    if name == "gaussian_e^{-v^2}":
        # f(v)=exp(-v^2); f2=∫_0^∞ e^{-v^2} v dv = 1/2, f4=∫ e^{-v^2} v^3 dv = 1/2
        return {"name": name, "f0": 1.0, "f2": 0.5, "f4": 0.5, "note": "smooth, rapid decay"}
    if name == "exponential_e^{-v}":
        # f(v)=e^{-v} for v>0; f2=Γ(2)=1, f4=Γ(4)=3
        return {"name": name, "f0": 1.0, "f2": 1.0, "f4": 6.0, "note": "f(v)=e^{-v}; not even in the usual D/Λ sense, included as a moment scheme only"}
    raise KeyError(name)


def vol_schemes() -> Dict[str, float]:
    """Regularised internal volumes on the unit metric (ℓ0=1).

    The area of a truncation is π U² + 2π log U + C0 + o(1), with
    C0 = 2π ln 2 (proved). Using the divergent π U² piece as Vol_reg
    makes α depend on an arbitrary cutoff; we list it only to show that
    dependence.
    """
    def vol(U: float) -> float:
        return math.pi * U * U + 2.0 * math.pi * math.log(U) + C0_EXACT

    return {
        "C0_finite_part": C0_EXACT,
        "C0_plus_2pi_log_e": C0_EXACT + 2.0 * math.pi * 1.0,  # U=e
        "C0_plus_2pi_log_10": C0_EXACT + 2.0 * math.pi * math.log(10.0),
        "truncation_U=1": vol(1.0),
        "truncation_U=3": vol(3.0),
        "truncation_U=10": vol(10.0),
    }


def alpha_from(C_SA: float, phi2: float, vol: float) -> float:
    return 1.0 / (16.0 * math.pi * C_SA * phi2 * vol)


def table() -> dict:
    # C_SA is not uniquely derived here. We use two *named hypotheses*:
    #   "placeholder_1/(24 pi^2)": a frequently quoted 4D factor in notes
    #     (the 1/24π² that appears in many 4D heat-kernel EH writeups).
    #     This is a hypothesis, not a computation on the conoid.
    #   "implied_by_64pi/45_with_C0_and_f2=1/2": the C_SA that would make
    #     the locked α true for (Vol=C0, φ2=1/2). Recorded only as the
    #     inverse of the convention lock.
    vols = vol_schemes()
    moments = [phi_moments("sharp_[0,1]"), phi_moments("gaussian_e^{-v^2}"), phi_moments("exponential_e^{-v}")]
    C_SA_hyp = {
        "1/(24*pi^2)_hypothesis": 1.0 / (24.0 * math.pi ** 2),
        "1/(4*pi^2)_hypothesis": 1.0 / (4.0 * math.pi ** 2),
    }
    rows: List[dict] = []
    for cname, CSA in C_SA_hyp.items():
        for mom in moments:
            for vname, vol in vols.items():
                a = alpha_from(CSA, mom["f2"], vol)
                rows.append({
                    "C_SA_name": cname,
                    "C_SA": CSA,
                    "cutoff": mom["name"],
                    "phi2": mom["f2"],
                    "Vol_name": vname,
                    "Vol": vol,
                    "alpha": a,
                    "alpha_over_64pi/45": a / LOCKED_ALPHA,
                })
    # The convention lock: what product C_SA φ2 Vol the recorded 64π/45 requires
    lock = {
        "recorded_alpha": LOCKED_ALPHA,
        "equivalent_product_C_SA_phi2_Vol": LOCKED_PRODUCT,
        "if_Vol=C0_and_phi2=1/2_then_C_SA": LOCKED_PRODUCT / (0.5 * C0_EXACT),
    }
    return {
        "formula": "alpha = 1/(16 pi C_SA phi2 Vol_reg),  Lambda=1/ell0,  G_N=kappa^2/(8 pi)",
        "C0_exact": C0_EXACT,
        "convention_lock": lock,
        "rows": rows,
        "conclusion": (
            "α is scheme-dependent. No row is claimed to be the unique "
            "geometric value. The recorded 64π/45 is a convention lock, "
            "equivalent to fixing C_SA φ2 Vol = 45/(1024 π²)."
        ),
    }


def main() -> None:
    import json
    from pathlib import Path
    t = table()
    print("G_N prefactor schemes")
    print("  recorded 64π/45 =", t["convention_lock"]["recorded_alpha"])
    print("  equivalent C_SA φ2 Vol =", t["convention_lock"]["equivalent_product_C_SA_phi2_Vol"])
    print("  implied C_SA if Vol=C0, φ2=1/2:", t["convention_lock"]["if_Vol=C0_and_phi2=1/2_then_C_SA"])
    # print a compact subset: C0 volume only
    print("  α for Vol=C0 (finite part):")
    for row in t["rows"]:
        if row["Vol_name"] == "C0_finite_part":
            print(f"    {row['C_SA_name']:28s} {row['cutoff']:22s}  α={row['alpha']:.6f}  "
                  f"α/(64π/45)={row['alpha_over_64pi/45']:.4f}")
    print("  ", t["conclusion"])
    out = Path(__file__).resolve().parent.parent / "reproducibility" / "gn_prefactor_schemes.json"
    out.write_text(json.dumps(t, indent=2), encoding="utf-8")
    print("Wrote", out)


if __name__ == "__main__":
    main()
