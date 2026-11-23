#!/usr/bin/env python3
"""Demonstrate that the original stationarity scripts are tautological.

Uses the original J / derivative formulas verbatim, then evaluates them at:
  - the imaginary parts of known zeta zeros
  - midpoints between consecutive zeros
  - random t in the same range

If those three sets all "pass" at the same rate, the test is not identifying
zeros. This script does not modify the originals.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "identification_results"
OUT.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Exact copies of the original formulas (do not "improve" them here)
# ---------------------------------------------------------------------------

def original_model_information_current(sigma, t, omega0=1.0):
    """Copied from code/verification/zeta_stationarity.py."""
    delta = abs(sigma - 0.5) * 2.0
    damping = omega0 / (1 + delta / omega0)
    bridge_factor = 1.0 + np.exp(-delta)
    J_proxy = damping * bridge_factor
    return J_proxy


def original_variational_derivative(sigma, t, h=1e-6):
    """Copied from code/verification/zeta_stationarity.py."""
    J_plus = original_model_information_current(sigma + h, t)
    J_minus = original_model_information_current(sigma - h, t)
    return (J_plus - J_minus) / (2 * h)


def original_dual_zero_reg2(delta):
    """Copied from code/zeta_stationarity_enhanced.py."""
    eps = 1e-8 * np.exp(-np.abs(delta) / 10)
    return (np.real(delta) + eps * np.sin(12 * delta)) / (1 + np.abs(delta))


def original_information_current(k1, k2):
    """Copied from code/zeta_stationarity_enhanced.py."""
    diff = k1 - k2
    reg = original_dual_zero_reg2(diff)
    bridge_factor = 1.0 + 0.5 * np.sin(12 * np.angle(diff + 1j))
    return np.abs(reg) * bridge_factor * 2.0 / (1 + np.abs(diff))


def original_j_gradient(t):
    """Copied from code/zeta_stationarity_enhanced.py."""
    s0 = 0.5 + 1j * t
    delta = 1e-6
    J_c = original_information_current(s0, np.conj(s0))
    J_l = original_information_current(s0 - delta, np.conj(s0 - delta))
    J_r = original_information_current(s0 + delta, np.conj(s0 + delta))
    grad = np.abs((J_r - J_l) / (2 * delta))
    return grad, J_c


def load_zeros(n=50):
    import mpmath

    mpmath.mp.dps = 25
    return np.array([float(mpmath.zetazero(k).imag) for k in range(1, n + 1)])


def summarize(name, t_values, kind):
    rows = []
    if kind == "v4_stationarity":
        for t in t_values:
            J = original_model_information_current(0.5, t)
            deriv = original_variational_derivative(0.5, t)
            # Same threshold as the original script
            ok = abs(deriv) < 1e-4
            rows.append(
                {
                    "t": float(t),
                    "J": float(J),
                    "deriv": float(deriv),
                    "stationary": bool(ok),
                }
            )
    elif kind == "enhanced":
        for t in t_values:
            grad, Jval = original_j_gradient(t)
            j = float(Jval) if np.isfinite(Jval) else None
            g = float(grad) if np.isfinite(grad) else None
            ok = (g is not None) and (g < 1e-5)
            rows.append({"t": float(t), "J": j, "grad": g, "stationary": bool(ok)})
    else:
        raise ValueError(kind)
    n = len(rows)
    n_yes = sum(1 for r in rows if r["stationary"])
    return {"name": name, "n": n, "n_yes": n_yes, "fraction_yes": n_yes / n, "rows": rows}


def main() -> None:
    rng = np.random.default_rng(20261123)
    zeros = load_zeros(50)
    midpoints = 0.5 * (zeros[:-1] + zeros[1:])
    random_t = np.sort(rng.uniform(float(zeros[0]), float(zeros[-1]), size=len(midpoints)))

    # Independence check for the first original: J and dJ/dσ must not depend on t
    t_probe = np.array([0.0, 1.0, 14.134725, 100.0, 1000.0])
    J_probe = np.array([original_model_information_current(0.5, t) for t in t_probe])
    d_probe = np.array([original_variational_derivative(0.5, t) for t in t_probe])
    j_independent = bool(np.allclose(J_probe, J_probe[0]))
    d_independent = bool(np.allclose(d_probe, d_probe[0], atol=1e-12, equal_nan=True))

    # Analytic identity for the enhanced script: k1-k2 is invariant under the shift
    t_ex = 14.134725
    s0 = 0.5 + 1j * t_ex
    delta = 1e-6
    d_center = s0 - np.conj(s0)
    d_left = (s0 - delta) - np.conj(s0 - delta)
    d_right = (s0 + delta) - np.conj(s0 + delta)
    invariant = bool(np.isclose(d_center, d_left) and np.isclose(d_center, d_right))

    report = {
        "script_a": "code/verification/zeta_stationarity.py",
        "script_b": "code/zeta_stationarity_enhanced.py",
        "formula_independence": {
            "J_independent_of_t_on_critical_line": j_independent,
            "deriv_independent_of_t_on_critical_line": d_independent,
            "J_values_at_probe_t": J_probe.tolist(),
            "deriv_values_at_probe_t": [float(x) for x in d_probe],
            "probe_t": t_probe.tolist(),
        },
        "enhanced_k1_minus_k2_invariant_under_shift": invariant,
        "enhanced_k1_minus_k2_at_example": {
            "center": [d_center.real, d_center.imag],
            "left": [d_left.real, d_left.imag],
            "right": [d_right.real, d_right.imag],
        },
        "stationarity_v4": {
            "zeros": summarize("zeros", zeros, "v4_stationarity"),
            "midpoints": summarize("midpoints", midpoints, "v4_stationarity"),
            "random_t": summarize("random_t", random_t, "v4_stationarity"),
        },
        "stationarity_enhanced": {
            "zeros": summarize("zeros", zeros[:20], "enhanced"),
            "midpoints": summarize("midpoints", midpoints[:19], "enhanced"),
            "random_t": summarize("random_t", random_t[:19], "enhanced"),
        },
        "note": (
            "v4 script: every t at σ=1/2 is 'YES' because J depends only on |σ-1/2|. "
            "Enhanced script: gradient is identically 0 when finite, because the "
            "finite difference does not change k1-k2. Overflow to nan for larger t "
            "is why the original printed 3/20 YES rather than 20/20."
        ),
    }

    # Compact printable tables (drop per-row dumps from stdout; keep them in JSON)
    def brief(block):
        out = {}
        for key, val in block.items():
            out[key] = {
                "n": val["n"],
                "n_yes": val["n_yes"],
                "fraction_yes": val["fraction_yes"],
            }
        return out

    printable = {
        "formula_independence": report["formula_independence"],
        "enhanced_k1_minus_k2_invariant_under_shift": invariant,
        "v4_yes_counts": brief(report["stationarity_v4"]),
        "enhanced_yes_counts": brief(report["stationarity_enhanced"]),
        "note": report["note"],
    }
    print(json.dumps(printable, indent=2))

    path = OUT / "tautology_demo.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {path}")

    print("\n=== Tautology verdict ===")
    v4 = report["stationarity_v4"]
    print(
        f"Original zeta_stationarity.py at σ=1/2: "
        f"zeros {v4['zeros']['n_yes']}/{v4['zeros']['n']}, "
        f"midpoints {v4['midpoints']['n_yes']}/{v4['midpoints']['n']}, "
        f"random t {v4['random_t']['n_yes']}/{v4['random_t']['n']}."
    )
    en = report["stationarity_enhanced"]
    print(
        f"Original zeta_stationarity_enhanced.py: "
        f"zeros {en['zeros']['n_yes']}/{en['zeros']['n']}, "
        f"midpoints {en['midpoints']['n_yes']}/{en['midpoints']['n']}, "
        f"random t {en['random_t']['n_yes']}/{en['random_t']['n']} "
        f"(YES only where the original overflow does not produce nan)."
    )
    if (
        v4["zeros"]["fraction_yes"] == 1.0
        and v4["midpoints"]["fraction_yes"] == 1.0
        and v4["random_t"]["fraction_yes"] == 1.0
    ):
        print("This is not a test of Riemann zeros. The v4 formula passes for every t.")


if __name__ == "__main__":
    main()
