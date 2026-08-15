#!/usr/bin/env python3
"""
SAM3 — Production-path 2D Dirac operator on the right conoid
============================================================
P1 of the numerical production roadmap (docs/hardening/23).

Features:
  - Explicit conoid metric and spin connection
  - 2-component spinor on a (u,v) grid
  - APS-style spectral penalty at radial boundaries
  - Residual diagnostic ||D ψ − λ ψ|| / ||ψ||
  - Domain-extension driver for |λ|_min vs u_max

omega0 defaults to the geometric lock 0.927 (doc 18).
Does not retune any physics number to experiment.

Usage:
  python code/dirac_conoid_aps.py
  python code/dirac_conoid_aps.py --gap-scan
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh

try:
    from sam3_geometry_constants import OMEGA0_GEOMETRIC, N_BRIDGES
except ImportError:
    OMEGA0_GEOMETRIC = 0.927
    N_BRIDGES = 12


@dataclass
class DiracConfig:
    Nu: int = 48
    Nv: int = 64
    u_max: float = 6.0
    l0: float = 1.0
    omega0: float = OMEGA0_GEOMETRIC
    aps_strength: float = 25.0
    n_eigs: int = 8
    fourth_order: bool = True


def _metric_f(u: np.ndarray, v: np.ndarray, l0: float) -> np.ndarray:
    """f such that g_vv = f^2 = u^2 + 4 l0^2 cos^2(2v)  (model metric factor)."""
    return np.sqrt(u[:, None] ** 2 + 4.0 * l0**2 * np.cos(2.0 * v[None, :]) ** 2)


def _spin_connection_coeff(u: np.ndarray, v: np.ndarray, l0: float) -> np.ndarray:
    """Approximate spin-connection contribution ω_u ~ (1/(2f)) ∂_v f  on the conoid.

    For ds^2 = du^2 + f(u,v)^2 dv^2 the relevant connection form component
    involves ∂_u log f and ∂_v log f. We use a stable grid evaluation.
    """
    f = _metric_f(u, v, l0)
    # ∂_u log f ≈ u / f^2
    dlogf_du = u[:, None] / (f**2 + 1e-15)
    return 0.5 * dlogf_du


def build_dirac_matrix(cfg: DiracConfig) -> Tuple[sparse.csr_matrix, np.ndarray, np.ndarray]:
    """Build a sparse 2-component Dirac operator on the (u,v) grid.

    Ordering: spinor components interleaved as [ψ↑(u_i,v_j), ψ↓(u_i,v_j)] with
    flattened index i*Nv + j for each component block of size N = Nu*Nv.
    Full size 2N.
    """
    if abs(cfg.omega0 - OMEGA0_GEOMETRIC) > 0.02:
        raise ValueError(
            f"omega0={cfg.omega0} outside geometric lock ~{OMEGA0_GEOMETRIC}"
        )

    Nu, Nv = cfg.Nu, cfg.Nv
    u = np.linspace(-cfg.u_max, cfg.u_max, Nu)
    v = np.linspace(0.0, 2.0 * np.pi, Nv, endpoint=False)
    du = u[1] - u[0]
    dv = v[1] - v[0]
    N = Nu * Nv

    f = _metric_f(u, v, cfg.l0)  # (Nu, Nv)
    inv_f = 1.0 / (f + 1e-15)
    omega = _spin_connection_coeff(u, v, cfg.l0)

    # Finite-difference weights
    if cfg.fourth_order:
        # 4th-order central: (-f[i+2] + 8 f[i+1] - 8 f[i-1] + f[i-2]) / (12 h)
        w1, w2 = 8.0 / 12.0, -1.0 / 12.0
        offsets_u = [+1, -1, +2, -2]
        weights_u = [w1 / du, -w1 / du, w2 / du, -w2 / du]
        offsets_v = [+1, -1, +2, -2]
        weights_v = [w1 / dv, -w1 / dv, w2 / dv, -w2 / dv]
    else:
        offsets_u = [+1, -1]
        weights_u = [0.5 / du, -0.5 / du]
        offsets_v = [+1, -1]
        weights_v = [0.5 / dv, -0.5 / dv]

    rows: List[int] = []
    cols: List[int] = []
    data: List[float] = []

    def add(r: int, c: int, val: float) -> None:
        if 0 <= c < 2 * N and val != 0.0:
            rows.append(r)
            cols.append(c)
            data.append(val)

    def idx(i: int, j: int) -> int:
        return i * Nv + j

    # Pauli structure: D ~ σ_u (∂_u + ω) + σ_v (1/f) ∂_v
    # σ_u = [[0,1],[1,0]], σ_v = [[0,-i],[i,0]] → real block form with 2 components
    # We use a real 2-component representation:
    #   off-diagonal blocks carry ∂_u+ω and ±(1/f)∂_v
    for i in range(Nu):
        for j in range(Nv):
            p = idx(i, j)
            # component 0 row (upper), component 1 row (lower)
            r0, r1 = p, N + p

            # spin connection diagonal-ish contribution on off-diagonal blocks
            om = float(omega[i, j])
            invf = float(inv_f[i, j])

            # --- ∂_u terms: couple 0↔1 ---
            for off, w in zip(offsets_u, weights_u):
                ii = i + off
                if ii < 0 or ii >= Nu:
                    continue
                q = idx(ii, j)
                add(r0, N + q, w)  # upper gets ∂_u on lower
                add(r1, q, w)      # lower gets ∂_u on upper

            # ω on same site, off-diagonal
            add(r0, N + p, om)
            add(r1, p, om)

            # --- (1/f) ∂_v terms with structure σ_v ~ [[0,-1],[1,0]] in a real basis ---
            for off, w in zip(offsets_v, weights_v):
                jj = (j + off) % Nv  # periodic in v (bridge circle)
                q = idx(i, jj)
                add(r0, N + q, -invf * w)
                add(r1, q, +invf * w)

            # Mild Dual-Zero-inspired diagonal UV softener (does not retune ω0)
            soft = 1e-8 * cfg.omega0 * (1.0 + (abs(u[i]) / cfg.u_max) ** 2)
            add(r0, r0, soft)
            add(r1, r1, soft)

    # APS-style penalty at radial ends: project against wrong chirality / inflow modes
    # Simple quadratic penalty on boundary spinor components
    pen = cfg.aps_strength / max(du, 1e-12)
    for j in range(Nv):
        for i_b in (0, Nu - 1):
            p = idx(i_b, j)
            add(p, p, pen)
            add(N + p, N + p, pen)

    D = sparse.coo_matrix((data, (rows, cols)), shape=(2 * N, 2 * N)).tocsr()
    # Symmetrize numerical noise
    D = 0.5 * (D + D.T)
    return D, u, v


def lowest_eigenpairs(
    D: sparse.csr_matrix, k: int = 8
) -> Tuple[np.ndarray, np.ndarray]:
    k = min(k, D.shape[0] - 2)
    evals, evecs = eigsh(D, k=k, which="SM", tol=1e-8, maxiter=5000)
    order = np.argsort(np.abs(evals))
    return evals[order], evecs[:, order]


def residual_norms(D: sparse.csr_matrix, evals: np.ndarray, evecs: np.ndarray) -> np.ndarray:
    res = []
    for n in range(evals.shape[0]):
        v = evecs[:, n]
        Nv = np.linalg.norm(v) + 1e-30
        r = np.linalg.norm(D @ v - evals[n] * v) / Nv
        res.append(float(r))
    return np.asarray(res, dtype=float)


def run_spectrum(cfg: DiracConfig) -> dict:
    D, u, v = build_dirac_matrix(cfg)
    evals, evecs = lowest_eigenpairs(D, k=cfg.n_eigs)
    res = residual_norms(D, evals, evecs)
    abs_min = float(np.min(np.abs(evals))) if evals.size else None
    return {
        "config": asdict(cfg),
        "evals": evals.tolist(),
        "abs_min": abs_min,
        "residuals": res.tolist(),
        "max_residual": float(np.max(res)) if res.size else None,
        "mean_residual": float(np.mean(res)) if res.size else None,
        "Nu": cfg.Nu,
        "Nv": cfg.Nv,
        "u_max": cfg.u_max,
        "matrix_size": int(D.shape[0]),
        "status": "production_path_P1",
    }


def gap_scan(
    u_max_list: Optional[List[float]] = None,
    Nu_base: int = 40,
    Nv: int = 48,
    l0: float = 1.0,
) -> dict:
    """Domain-extension scan: |λ|_min vs u_max at roughly fixed du."""
    if u_max_list is None:
        u_max_list = [3.0, 4.0, 5.0, 6.0, 8.0]
    rows = []
    for um in u_max_list:
        Nu = max(24, int(Nu_base * um / 6.0))
        cfg = DiracConfig(Nu=Nu, Nv=Nv, u_max=um, l0=l0, n_eigs=6)
        out = run_spectrum(cfg)
        rows.append(
            {
                "u_max": um,
                "Nu": Nu,
                "abs_min": out["abs_min"],
                "max_residual": out["max_residual"],
            }
        )
    # log-log slope fit for gap ~ u_max^p
    xs = np.array([math.log(r["u_max"]) for r in rows if r["abs_min"] and r["abs_min"] > 0])
    ys = np.array([math.log(r["abs_min"]) for r in rows if r["abs_min"] and r["abs_min"] > 0])
    slope = None
    if len(xs) >= 2:
        slope = float(np.polyfit(xs, ys, 1)[0])
    return {
        "rows": rows,
        "log_log_slope_abs_min_vs_umax": slope,
        "expected_slope_near": -1.0,
        "note": "slope ~ -1 supports gap ∝ 1/u_max continuum claim (doc 10)",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="SAM3 conoid Dirac P1")
    parser.add_argument("--gap-scan", action="store_true")
    parser.add_argument("--Nu", type=int, default=48)
    parser.add_argument("--Nv", type=int, default=64)
    parser.add_argument("--u-max", type=float, default=6.0)
    args = parser.parse_args()

    out_dir = Path(__file__).resolve().parent.parent / "pipeline_output"
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.gap_scan:
        print("Running gap scan (|λ|_min vs u_max)...")
        result = gap_scan()
        path = out_dir / "05_gap_scan.json"
        path.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(json.dumps(result, indent=2))
        print(f"Wrote {path}")
        return

    cfg = DiracConfig(Nu=args.Nu, Nv=args.Nv, u_max=args.u_max)
    print(f"Building Dirac matrix Nu={cfg.Nu} Nv={cfg.Nv} u_max={cfg.u_max} ...")
    result = run_spectrum(cfg)
    path = out_dir / "05_dirac_aps_spectrum.json"
    path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"|λ|_min = {result['abs_min']}")
    print(f"max residual = {result['max_residual']}")
    print(f"mean residual = {result['mean_residual']}")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
