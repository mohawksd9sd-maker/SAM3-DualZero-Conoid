#!/usr/bin/env python3
"""Corrected, non-circular counterpart of zeta_stationarity.py.

The original script is left unchanged at
    code/verification/zeta_stationarity.py
See README_stationarity_flaw.md for the tautology (J depends only on |σ-1/2|
and therefore "passes" at every t, including midpoints and random values).

This script:

  1. Builds J from Dual-Zero + the conoid Dirac spectrum (construction A
     in zeta_identification_test.py). Zeta zeros are not used to build J.
  2. Evaluates the action density S_I = |J|^2 and a numerical gradient at
     known zeros, midpoints, and random t — as a comparison, not as a search.
  3. Also finds 1-D minima of S_I(1/2+it) without using zeros, then compares.

For the full strip search, shuffled-data controls, and all four assemblies
of J, run:

    python code/verification/zeta_identification_test.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

from zeta_identification_test import (  # noqa: E402
    OUT,
    T_MAX,
    T_MIN,
    J_from_prepared,
    S_I,
    compare_feature_list,
    conoid_dirac_spectrum,
    control_sets,
    line_features_at_half,
    load_zeros,
    prepare_spectral,
)

SEED = 20261123


def grad_S(Jfunc, sigma, t, h=1e-5):
    def S(sig, tt):
        return S_I(Jfunc(complex(sig, tt)))

    dsig = (S(sigma + h, t) - S(sigma - h, t)) / (2 * h)
    dt = (S(sigma, t + h) - S(sigma, t - h)) / (2 * h)
    return dsig, dt, float(np.hypot(dsig, dt)), S(sigma, t)


def eval_set(name, ts, Jfunc, sigma=0.5):
    rows = []
    for t in ts:
        dsig, dt, g, Si = grad_S(Jfunc, sigma, float(t))
        rows.append(
            {
                "t": float(t),
                "S_I": Si,
                "dS_dsigma": dsig,
                "dS_dt": dt,
                "grad_norm": g,
            }
        )
    grads = np.array([r["grad_norm"] for r in rows])
    return {
        "name": name,
        "n": len(rows),
        "mean_grad": float(np.mean(grads)),
        "median_grad": float(np.median(grads)),
        "min_grad": float(np.min(grads)),
        "max_grad": float(np.max(grads)),
        "rows": rows,
    }


def main() -> None:
    print("FLAW IN THE ORIGINAL zeta_stationarity.py")
    print("  model_information_current(sigma, t) ignores t and peaks at σ=1/2 by hand.")
    print("  Midpoints and random t therefore get the same YES verdict as zeta zeros.")
    print("  This script uses construction A (Dual-Zero spectral zeta of the conoid Dirac")
    print("  operator) and does not insert zeros into J.\n")

    rng = np.random.default_rng(SEED)
    zeros = load_zeros(80)
    controls = control_sets(zeros, rng)

    spec = conoid_dirac_spectrum()
    prep = prepare_spectral(spec["abs_eigs"], True)
    Jfunc = lambda s, p=prep: J_from_prepared(s, p)

    z_eval = eval_set("zeros", controls["zeros"], Jfunc)
    m_eval = eval_set("midpoints", controls["midpoints"], Jfunc)
    r_eval = eval_set("random_t", controls["random_t"], Jfunc)

    ts = np.linspace(T_MIN, T_MAX, 781)
    line = line_features_at_half(Jfunc, ts)
    matches = compare_feature_list(line["t_local_minima"], controls)

    summary = {
        "construction": "A_dualzero_spectral_zeta",
        "n_dirac_modes": int(spec["n_kept"]),
        "grad_at_sigma_half": {
            "zeros": {k: v for k, v in z_eval.items() if k != "rows"},
            "midpoints": {k: v for k, v in m_eval.items() if k != "rows"},
            "random_t": {k: v for k, v in r_eval.items() if k != "rows"},
        },
        "minima_on_critical_line_without_using_zeros": matches,
        "note": (
            "If zeros were special for this J, mean/median |∇S_I| at zeros would "
            "be clearly smaller than at midpoints and random t, and line minima "
            "would sit closer to zeros than to those controls. See also "
            "identification_results/identification_test.json."
        ),
    }
    path = OUT / "zeta_stationarity_corrected.json"
    # include rows too
    summary["grad_at_sigma_half"]["zeros"] = z_eval
    summary["grad_at_sigma_half"]["midpoints"] = m_eval
    summary["grad_at_sigma_half"]["random_t"] = r_eval
    path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    def brief(ev):
        return (
            f"n={ev['n']}  median |∇S_I|={ev['median_grad']:.4g}  "
            f"mean={ev['mean_grad']:.4g}"
        )

    print("Gradient of S_I at σ=1/2 (smaller would mean 'more stationary'):")
    print("  zeros:     ", brief(z_eval))
    print("  midpoints: ", brief(m_eval))
    print("  random t:  ", brief(r_eval))
    z = matches["zeros_to_features"]
    mid = matches["midpoints_to_features"]
    rnd = matches["random_to_features"]
    print(f"\nMinima of S_I(1/2+it) found without zeros: n={matches['n_features']}")
    print(f"  median distance, each zero     -> nearest minimum: {z.get('median')}")
    print(f"  median distance, each midpoint -> nearest minimum: {mid.get('median')}")
    print(f"  median distance, each random t -> nearest minimum: {rnd.get('median')}")
    print(f"\nWrote {path}")


if __name__ == "__main__":
    main()
