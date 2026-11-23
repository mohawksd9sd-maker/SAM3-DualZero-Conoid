#!/usr/bin/env python3
"""Corrected, non-circular counterpart of zeta_stationarity_enhanced.py.

The original script is left unchanged at
    code/zeta_stationarity_enhanced.py
See code/verification/README_stationarity_flaw.md.

Flaws in the original:

  * j_gradient shifts k1 and conjugate(k2) by the same real δ, so k1-k2
    is invariant and the finite-difference gradient is identically zero
    whenever J is finite.
  * For larger t, sin(12*(k1-k2)) overflows (k1-k2 = 2it), which is why
    the original printed 3/20 YES rather than 20/20.
  * The "Dual-Zero" helper in the original is not the locked generator
    ε(n) = ω₀ (-1)^n n^{-n} from doc 18.

This script uses constructions A and C from
code/verification/zeta_identification_test.py: the Dual-Zero spectral zeta
of the conoid Dirac operator, and the 12-bridge overlap Dirichlet series.
J is built without zeta zeros. Stationarity is tested by a genuine 2-D
gradient of S_I = |J|^2, and zeros are compared to midpoints and random t.

For the full strip search and shuffled-data controls, run:

    python code/verification/zeta_identification_test.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code" / "verification"))
sys.path.insert(0, str(ROOT / "code"))

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
    prepare_overlap_dirichlet,
    prepare_spectral,
    twelve_bridge_overlap_matrix,
)

SEED = 20261123


def grad_S(Jfunc, sigma, t, h=1e-5):
    def S(sig, tt):
        return S_I(Jfunc(complex(sig, tt)))

    dsig = (S(sigma + h, t) - S(sigma - h, t)) / (2 * h)
    dt = (S(sigma, t + h) - S(sigma, t - h)) / (2 * h)
    return float(np.hypot(dsig, dt)), S(sigma, t)


def eval_set(name, ts, Jfunc, sigma=0.5):
    rows = []
    for t in ts:
        g, Si = grad_S(Jfunc, sigma, float(t))
        rows.append({"t": float(t), "S_I": Si, "grad_norm": g})
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


def run_one(label, Jfunc, controls):
    z_eval = eval_set("zeros", controls["zeros"], Jfunc)
    m_eval = eval_set("midpoints", controls["midpoints"], Jfunc)
    r_eval = eval_set("random_t", controls["random_t"], Jfunc)
    ts = np.linspace(T_MIN, T_MAX, 781)
    line = line_features_at_half(Jfunc, ts)
    matches = compare_feature_list(line["t_local_minima"], controls)
    return {
        "label": label,
        "grad_at_sigma_half": {"zeros": z_eval, "midpoints": m_eval, "random_t": r_eval},
        "minima_on_critical_line": matches,
    }


def main() -> None:
    print("FLAW IN THE ORIGINAL zeta_stationarity_enhanced.py")
    print("  The finite-difference shift leaves k1-k2 unchanged, so ∇J is identically")
    print("  zero when finite. Overflow, not a failed test, produced the 3/20 count.")
    print("  This script uses a genuine 2-D gradient of S_I = |J|^2 and does not")
    print("  insert zeros into J.\n")

    rng = np.random.default_rng(SEED)
    zeros = load_zeros(80)
    controls = control_sets(zeros, rng)

    spec = conoid_dirac_spectrum()
    C = twelve_bridge_overlap_matrix()
    results = {
        "A_dualzero_spectral_zeta": run_one(
            "A_dualzero_spectral_zeta",
            lambda s, p=prepare_spectral(spec["abs_eigs"], True): J_from_prepared(s, p),
            controls,
        ),
        "C_overlap_dirichlet": run_one(
            "C_overlap_dirichlet",
            lambda s, p=prepare_overlap_dirichlet(C, True): J_from_prepared(s, p),
            controls,
        ),
    }

    path = OUT / "zeta_stationarity_enhanced_corrected.json"
    path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    for label, block in results.items():
        g = block["grad_at_sigma_half"]
        print(f"=== {label} ===")
        for key in ("zeros", "midpoints", "random_t"):
            ev = g[key]
            print(
                f"  {key:<10} n={ev['n']}  median |∇S_I|={ev['median_grad']:.4g}  "
                f"mean={ev['mean_grad']:.4g}"
            )
        m = block["minima_on_critical_line"]
        print(
            f"  line minima n={m['n_features']}; median dist "
            f"zeros={m['zeros_to_features'].get('median')}, "
            f"mids={m['midpoints_to_features'].get('median')}, "
            f"rand={m['random_to_features'].get('median')}"
        )
    print(f"\nWrote {path}")


if __name__ == "__main__":
    main()
