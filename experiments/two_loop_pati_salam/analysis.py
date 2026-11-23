"""Uncertainty bands and the full doc-55 report for the two-loop solve."""

from __future__ import annotations

import json
import math
from dataclasses import replace
from typing import Dict

import numpy as np

from rge import PDG, PDG_ALPHA_INV_127930, Inputs, SMRun, heavy_spectrum, solve_unification

INPUT_SIGMAS = {
    "alpha_s": 0.0009,
    "sin2w": 0.00006,
    "alpha_em_inv": 0.010,
    "mt_pole": 0.3,
}


def central(scenario="composite") -> Dict[str, Dict]:
    return {
        "one_loop": solve_unification(PDG, scenario, 1),
        "two_loop": solve_unification(PDG, scenario, 2),
        "two_loop_no_msbar_constant": solve_unification(PDG, scenario, 2, msbar_constant=False),
        "one_loop_alpha_inv_127.930(repo inputs)": solve_unification(PDG_ALPHA_INV_127930, scenario, 1),
        "two_loop_alpha_inv_127.930": solve_unification(PDG_ALPHA_INV_127930, scenario, 2),
    }


def input_shifts(scenario="composite", loops=2) -> Dict[str, Dict[str, float]]:
    base = solve_unification(PDG, scenario, loops)
    out = {}
    for k, s in INPUT_SIGMAS.items():
        row = {}
        for sign in (+1, -1):
            r = solve_unification(replace(PDG, **{k: getattr(PDG, k) + sign * s}), scenario, loops)
            row["+1sigma" if sign > 0 else "-1sigma"] = {
                "dlog10_mR": math.log10(r["m_R_GeV"] / base["m_R_GeV"]),
                "dlog10_Lambda": math.log10(r["Lambda_GeV"] / base["Lambda_GeV"]),
            }
        out[k] = row
    # quadrature (half the +/- spread)
    q_m = math.sqrt(sum(((v["+1sigma"]["dlog10_mR"] - v["-1sigma"]["dlog10_mR"]) / 2) ** 2 for v in out.values()))
    q_L = math.sqrt(sum(((v["+1sigma"]["dlog10_Lambda"] - v["-1sigma"]["dlog10_Lambda"]) / 2) ** 2 for v in out.values()))
    out["quadrature_1sigma"] = {"dlog10_mR": q_m, "dlog10_Lambda": q_L}
    return out


def threshold_band(scenario="composite", n=400, seed=2026, loops=2) -> Dict[str, object]:
    """Each heavy multiplet mass = m_R * 10^u, u ~ U[-1, 1] independently."""
    names, _, _ = heavy_spectrum(scenario)
    sm = SMRun(PDG, loops)
    rng = np.random.default_rng(seed)
    mR, Lam, aU, fails = [], [], [], 0
    for _ in range(n):
        u = rng.uniform(-1.0, 1.0, len(names))
        r = solve_unification(PDG, scenario, loops, log10_ratios=u, sm=sm)
        if r is None:
            fails += 1
            continue
        mR.append(math.log10(r["m_R_GeV"]))
        Lam.append(math.log10(r["Lambda_GeV"]))
        aU.append(r["alpha_U_inv"])
    single = {}
    for i, nm in enumerate(names):
        row = {}
        for v in (+1.0, -1.0):
            u = np.zeros(len(names))
            u[i] = v
            r = solve_unification(PDG, scenario, loops, log10_ratios=u, sm=sm)
            row["x10" if v > 0 else "/10"] = None if r is None else {
                "log10_mR": math.log10(r["m_R_GeV"]), "log10_Lambda": math.log10(r["Lambda_GeV"])}
        single[nm] = row

    def pct(a):
        a = np.array(a)
        return {"p05": float(np.percentile(a, 5)), "p50": float(np.percentile(a, 50)),
                "p95": float(np.percentile(a, 95)), "min": float(a.min()), "max": float(a.max())}

    return {
        "samples": n, "no_solution": fails,
        "log10_mR": pct(mR), "log10_Lambda": pct(Lam), "alpha_U_inv": pct(aU),
        "one_at_a_time": single,
    }


def report() -> Dict[str, object]:
    out = {}
    for sc in ("composite", "with15"):
        out[sc] = {
            "central": central(sc),
            "input_shifts_two_loop": input_shifts(sc),
            "threshold_band_two_loop": threshold_band(sc, n=300 if sc == "composite" else 150),
        }
    return out


if __name__ == "__main__":
    print(json.dumps(report(), indent=1, default=float))
