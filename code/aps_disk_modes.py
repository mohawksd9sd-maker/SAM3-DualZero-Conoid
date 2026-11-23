#!/usr/bin/env python3
"""Mode-by-mode APS Dirac on the flat disk (known-answer tests).

Analytic facts, from Falomir, Gamboa Saraví and Santangelo,
J. Math. Phys. 39 (1998) 532–544 (arXiv:hep-th/9609194):

* For flux κ = 0 (k = −1) there are no zero modes, and the nonzero
  eigenvalues are ± j_{n,l}/R, n = 0,1,2,…, l = 1,2,… (zeros of J_n).
* For k < κ ≤ k+1 the index is k+1 and there are |k+1| zero modes of
  one chirality (JMP 39, §III and eq. (79)).

The numerical method is a radial first-order scheme (2nd-order SBP in r,
SAT enforcement of the Falomir spectral conditions mode by mode). The
operator is not exactly Hermitian; eigenvalues with a substantial
imaginary part are discarded. The nearly-real spectrum is compared to
the Bessel zeros. A numerical reproduction of the *nonzero* Falomir
index (κ ≠ 0 zero-mode count) is not claimed: that test did not hold
for this scheme and is left open.
"""
from __future__ import annotations

import math
from typing import Dict, List, Tuple

import numpy as np
from scipy.special import jn_zeros


def aps_k(kappa: float) -> int:
    return int(math.ceil(kappa) - 1)


def analytic_disk_index(kappa: float) -> int:
    return aps_k(kappa) + 1


def unique_bessel_positives(R: float, n_max: int = 6, l_max: int = 6) -> np.ndarray:
    vals = []
    for n in range(0, n_max + 1):
        vals.extend((jn_zeros(n, l_max) / R).tolist())
    return np.sort(np.array(vals, dtype=float))


def _sbp2(n_intervals: int, h: float) -> Tuple[np.ndarray, np.ndarray]:
    N = n_intervals
    m = N + 1
    H = np.ones(m) * h
    H[0] = H[-1] = 0.5 * h
    D = np.zeros((m, m))
    D[0, 0], D[0, 1] = -1 / h, 1 / h
    D[-1, -2], D[-1, -1] = -1 / h, 1 / h
    for i in range(1, N):
        D[i, i - 1] = -0.5 / h
        D[i, i + 1] = 0.5 / h
    return D, H


def mode_evals(n: int, R: float = 1.0, N: int = 160, kappa: float = 0.0, sat: float = 2.0) -> np.ndarray:
    k = aps_k(kappa)
    h = R / N
    r = h * np.arange(1, N + 1)
    m = len(r)
    D, H = _sbp2(m - 1, h)
    nu = (n - kappa) + 0.5
    Rinv = np.diag(1.0 / r)
    Op1 = D - nu * Rinv
    Op2 = D + nu * Rinv
    eR = np.zeros(m)
    eR[-1] = 1.0
    SAT = sat * (np.diag(1.0 / H) @ np.outer(eR, eR))
    if n >= k + 1:
        Op1 = Op1 - SAT
    if n + 1 <= k + 1:
        Op2 = Op2 - SAT
    Dmat = np.zeros((2 * m, 2 * m), dtype=complex)
    Dmat[:m, m:] = 1j * Op2
    Dmat[m:, :m] = 1j * Op1
    Hs = np.sqrt(np.concatenate([H, H]))
    Ds = (Hs[:, None] * Dmat) / Hs[None, :]
    return np.linalg.eigvals(Ds)


def nearly_real(ev: np.ndarray, imag_abs: float = 0.02) -> np.ndarray:
    return ev[np.abs(ev.imag) <= imag_abs].real


def collect_spectrum(n_max: int, R: float, N: int, kappa: float = 0.0) -> Dict:
    evs: List[np.ndarray] = []
    n_drop = 0
    n_tot = 0
    for n in range(-n_max, n_max + 1):
        ev = mode_evals(n, R=R, N=N, kappa=kappa)
        n_tot += ev.size
        good = nearly_real(ev)
        n_drop += ev.size - good.size
        evs.append(good)
    ev = np.concatenate(evs) if evs else np.zeros(0)
    return {"evals": ev, "n_dropped_nonreal": n_drop, "n_total": n_tot}


def disk_bessel_report(N: int = 120, R: float = 1.0, n_max: int = 8, n_unique: int = 6) -> dict:
    packed = collect_spectrum(n_max=n_max, R=R, N=N, kappa=0.0)
    ev = packed["evals"]
    pos = np.sort(ev[ev > 0.5])  # κ=0 has no zero modes; floor cuts junk
    unique_num = []
    for x in pos:
        if not unique_num or abs(x - unique_num[-1]) > 0.05:
            unique_num.append(float(x))
    exact = unique_bessel_positives(R, n_max=8, l_max=6)
    k = min(n_unique, len(unique_num), len(exact))
    errs = [abs(unique_num[i] - exact[i]) for i in range(k)]
    return {
        "N": N,
        "R": R,
        "lowest_numerical": unique_num[0] if unique_num else None,
        "lowest_exact": float(exact[0]),
        "lowest_abs_error": abs(unique_num[0] - exact[0]) if unique_num else None,
        "unique_numerical": unique_num[:n_unique],
        "unique_exact": exact[:n_unique].tolist(),
        "unique_abs_errors": errs,
        "max_unique_abs_error": max(errs) if errs else None,
        "n_below_1": int(np.sum(np.abs(ev) < 1.0)),
        "n_dropped_nonreal": packed["n_dropped_nonreal"],
        "n_total": packed["n_total"],
        "analytic_index": 0,
    }


def disk_convergence(Ns: Tuple[int, ...] = (40, 80, 120, 160), R: float = 1.0) -> dict:
    rows = []
    for N in Ns:
        r = disk_bessel_report(N=N, R=R, n_unique=4)
        rows.append({
            "N": N,
            "lowest_numerical": r["lowest_numerical"],
            "lowest_exact": r["lowest_exact"],
            "lowest_abs_error": r["lowest_abs_error"],
            "max_unique_abs_error": r["max_unique_abs_error"],
            "n_below_1": r["n_below_1"],
        })
    Ns_a = np.array([row["N"] for row in rows if row["lowest_abs_error"]], dtype=float)
    err = np.array([row["lowest_abs_error"] for row in rows if row["lowest_abs_error"]], dtype=float)
    slope = float(np.polyfit(np.log(Ns_a), np.log(err), 1)[0]) if len(err) >= 2 and np.all(err > 0) else None
    return {"rows": rows, "lowest_error_log_log_slope": slope, "exact_j01": float(jn_zeros(0, 1)[0]) / R}


if __name__ == "__main__":
    print("Disk APS, κ=0, Bessel known answers")
    conv = disk_convergence()
    for row in conv["rows"]:
        print(f"  N={row['N']:3d}  lowest={row['lowest_numerical']:.5f}  "
              f"err={row['lowest_abs_error']:.4e}  n_|λ|<1={row['n_below_1']}")
    print("  slope (lowest err) =", conv["lowest_error_log_log_slope"])
    r = disk_bessel_report(N=120)
    print("  unique num ", [round(x, 4) for x in r["unique_numerical"]])
    print("  unique exact", [round(x, 4) for x in r["unique_exact"]])
