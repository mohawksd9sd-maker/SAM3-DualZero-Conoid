#!/usr/bin/env python3
"""
SAM3 — Production-path 2D Dirac on the right conoid (P1–P4)
===========================================================
- Explicit metric + spin connection
- 2-component spinor on (u,v)
- APS boundary penalty (P1) + optional spectral APS projector (P2)
- Residual diagnostics + gap-vs-u_max tables (P3)
- 2I Fourier/isotype projectors and overlap matrix (P4)

omega0 = 0.927 geometric only. No experimental retuning.

Usage:
  python code/dirac_conoid_aps.py
  python code/dirac_conoid_aps.py --gap-scan
  python code/dirac_conoid_aps.py --overlaps
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
    from sam3_geometry_constants import OMEGA0_GEOMETRIC, N_BRIDGES, ETA_12, ETA_13, ETA_23
except ImportError:
    OMEGA0_GEOMETRIC = 0.927
    N_BRIDGES = 12
    ETA_12, ETA_13, ETA_23 = 0.8607, 0.5439, 0.4789


@dataclass
class DiracConfig:
    Nu: int = 40
    Nv: int = 48
    u_max: float = 6.0
    l0: float = 1.0
    omega0: float = OMEGA0_GEOMETRIC
    aps_strength: float = 25.0
    spectral_aps: bool = True  # P2
    n_eigs: int = 8
    fourth_order: bool = False  # default stable 2nd-order; 4th optional


def _metric_f(u: np.ndarray, v: np.ndarray, l0: float) -> np.ndarray:
    return np.sqrt(u[:, None] ** 2 + 4.0 * l0**2 * np.cos(2.0 * v[None, :]) ** 2)


def _spin_connection_coeff(u: np.ndarray, v: np.ndarray, l0: float) -> np.ndarray:
    f = _metric_f(u, v, l0)
    dlogf_du = u[:, None] / (f**2 + 1e-15)
    return 0.5 * dlogf_du


def build_dirac_matrix(cfg: DiracConfig) -> Tuple[sparse.csr_matrix, np.ndarray, np.ndarray]:
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

    f = _metric_f(u, v, cfg.l0)
    inv_f = 1.0 / (f + 1e-15)
    omega = _spin_connection_coeff(u, v, cfg.l0)

    if cfg.fourth_order:
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

    for i in range(Nu):
        for j in range(Nv):
            p = idx(i, j)
            r0, r1 = p, N + p
            om = float(omega[i, j])
            invf = float(inv_f[i, j])

            for off, w in zip(offsets_u, weights_u):
                ii = i + off
                if ii < 0 or ii >= Nu:
                    continue
                q = idx(ii, j)
                add(r0, N + q, w)
                add(r1, q, w)

            add(r0, N + p, om)
            add(r1, p, om)

            for off, w in zip(offsets_v, weights_v):
                jj = (j + off) % Nv
                q = idx(i, jj)
                add(r0, N + q, -invf * w)
                add(r1, q, +invf * w)

            soft = 1e-8 * cfg.omega0 * (1.0 + (abs(u[i]) / cfg.u_max) ** 2)
            add(r0, r0, soft)
            add(r1, r1, soft)

    # P1 quadratic APS penalty
    pen = cfg.aps_strength / max(du, 1e-12)
    for j in range(Nv):
        for i_b in (0, Nu - 1):
            p = idx(i_b, j)
            add(p, p, pen)
            add(N + p, N + p, pen)

    # P2 spectral APS: additional penalty on wrong-chirality combination at boundary
    # (ψ0 - sign(u) ψ1) content suppressed — discrete proxy for APS spectral condition
    if cfg.spectral_aps:
        for j in range(Nv):
            for i_b, sgn in ((0, -1.0), (Nu - 1, +1.0)):
                p = idx(i_b, j)
                # penalty on (ψ0 - sgn ψ1)^2 expanded into matrix elements
                s = 0.5 * pen
                add(p, p, s)
                add(N + p, N + p, s)
                add(p, N + p, -sgn * s)
                add(N + p, p, -sgn * s)

    D = sparse.coo_matrix((data, (rows, cols)), shape=(2 * N, 2 * N)).tocsr()
    D = 0.5 * (D + D.T)
    return D, u, v


def lowest_eigenpairs(
    D: sparse.csr_matrix, k: int = 8
) -> Tuple[np.ndarray, np.ndarray]:
    k = min(k, max(2, D.shape[0] - 2))
    # Shift-invert at 0 targets smallest-magnitude eigenvalues (required for convergence)
    evals, evecs = eigsh(D, k=k, sigma=0.0, which="LM", tol=1e-8, maxiter=10000)
    order = np.argsort(np.abs(evals))
    return evals[order], evecs[:, order]


def residual_norms(D: sparse.csr_matrix, evals: np.ndarray, evecs: np.ndarray) -> np.ndarray:
    res = []
    for n in range(evals.shape[0]):
        v = evecs[:, n]
        nv = np.linalg.norm(v) + 1e-30
        r = np.linalg.norm(D @ v - evals[n] * v) / nv
        res.append(float(r))
    return np.asarray(res, dtype=float)


def run_spectrum(cfg: DiracConfig) -> dict:
    D, u, v = build_dirac_matrix(cfg)
    evals, evecs = lowest_eigenpairs(D, k=cfg.n_eigs)
    res = residual_norms(D, evals, evecs)
    abs_min = float(np.min(np.abs(evals))) if evals.size else None
    return {
        "config": asdict(cfg),
        "evals": [float(x) for x in evals],
        "abs_min": abs_min,
        "residuals": res.tolist(),
        "max_residual": float(np.max(res)) if res.size else None,
        "mean_residual": float(np.mean(res)) if res.size else None,
        "Nu": cfg.Nu,
        "Nv": cfg.Nv,
        "u_max": cfg.u_max,
        "matrix_size": int(D.shape[0]),
        "status": "production_path_P1_P2",
        "_evecs_shape": list(evecs.shape),
        # evecs not written to JSON by default (large); available in-process
    }, D, u, v, evals, evecs


def gap_scan(
    u_max_list: Optional[List[float]] = None,
    Nu_base: int = 32,
    Nv: int = 40,
    l0: float = 1.0,
) -> dict:
    if u_max_list is None:
        u_max_list = [3.0, 4.0, 5.0, 6.0, 8.0]
    rows = []
    for um in u_max_list:
        Nu = max(20, int(Nu_base * um / 6.0))
        cfg = DiracConfig(Nu=Nu, Nv=Nv, u_max=um, l0=l0, n_eigs=6, fourth_order=False)
        out, *_ = run_spectrum(cfg)
        rows.append(
            {
                "u_max": um,
                "Nu": Nu,
                "abs_min": out["abs_min"],
                "max_residual": out["max_residual"],
            }
        )
    xs, ys = [], []
    for r in rows:
        if r["abs_min"] and r["abs_min"] > 0:
            xs.append(math.log(r["u_max"]))
            ys.append(math.log(r["abs_min"]))
    slope = float(np.polyfit(xs, ys, 1)[0]) if len(xs) >= 2 else None
    return {
        "rows": rows,
        "log_log_slope_abs_min_vs_umax": slope,
        "expected_slope_near": -1.0,
        "note": "slope ~ -1 supports gap ∝ 1/u_max (doc 10)",
        "status": "P3_gap_table",
    }


def bridge_isotype_projectors(Nv: int, n_bridges: int = N_BRIDGES) -> np.ndarray:
    """Fourier projectors onto 12-fold bridge harmonics (proxy for 2I isotypes).

    Returns array P[b, j] for bridge sector b=0..n_bridges-1 on angular grid j.
    """
    j = np.arange(Nv)
    P = np.zeros((n_bridges, Nv), dtype=float)
    for b in range(n_bridges):
        # localized angular window around bridge angle + discrete Fourier content
        center = b * Nv / n_bridges
        dist = np.minimum(np.abs(j - center), Nv - np.abs(j - center))
        P[b] = np.exp(-0.5 * (dist / (Nv / (2 * n_bridges))) ** 2)
        P[b] /= np.linalg.norm(P[b]) + 1e-15
    return P


def overlap_matrix_from_evecs(
    evecs: np.ndarray,
    Nu: int,
    Nv: int,
    n_modes: int = 3,
) -> dict:
    """P4: project lowest modes onto bridge windows and form overlap matrix η_ij proxy."""
    N = Nu * Nv
    P = bridge_isotype_projectors(Nv)
    # Use density summed over spinor components and radial coordinate
    mode_bridge = np.zeros((n_modes, N_BRIDGES))
    for m in range(min(n_modes, evecs.shape[1])):
        psi0 = evecs[:N, m].reshape(Nu, Nv)
        psi1 = evecs[N:, m].reshape(Nu, Nv)
        dens_v = np.mean(np.abs(psi0) ** 2 + np.abs(psi1) ** 2, axis=0)
        dens_v /= np.linalg.norm(dens_v) + 1e-15
        for b in range(N_BRIDGES):
            mode_bridge[m, b] = float(np.dot(dens_v, P[b]))

    # Generation proxies: three combinations of bridge clusters (0-3, 4-7, 8-11)
    gen = np.zeros((3, N_BRIDGES))
    gen[0, 0:4] = 1.0
    gen[1, 4:8] = 1.0
    gen[2, 8:12] = 1.0
    for g in range(3):
        gen[g] /= np.linalg.norm(gen[g]) + 1e-15

    # Overlap between generation windows using mode-averaged bridge weights
    w = np.mean(np.abs(mode_bridge), axis=0)
    w /= np.linalg.norm(w) + 1e-15
    eta = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            eta[i, j] = float(np.dot(gen[i] * w, gen[j] * w))
    # Normalize to diagonal 1
    for i in range(3):
        if eta[i, i] > 0:
            eta[i, :] /= math.sqrt(eta[i, i])
            eta[:, i] /= math.sqrt(eta[i, i] + 1e-30)
            eta[i, i] = 1.0

    return {
        "eta_matrix": eta.tolist(),
        "eta_12_num": float(eta[0, 1]),
        "eta_13_num": float(eta[0, 2]),
        "eta_23_num": float(eta[1, 2]),
        "eta_12_locked": ETA_12,
        "eta_13_locked": ETA_13,
        "eta_23_locked": ETA_23,
        "note": "P4 numerical bridge-window overlaps; locked η_ij remain the continuum reference",
        "status": "P4_isotype_overlaps",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="SAM3 conoid Dirac P1–P4")
    parser.add_argument("--gap-scan", action="store_true")
    parser.add_argument("--overlaps", action="store_true")
    parser.add_argument("--Nu", type=int, default=40)
    parser.add_argument("--Nv", type=int, default=48)
    parser.add_argument("--u-max", type=float, default=6.0)
    args = parser.parse_args()

    out_dir = Path(__file__).resolve().parent.parent / "pipeline_output"
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.gap_scan:
        print("Running gap scan...")
        result = gap_scan()
        path = out_dir / "05_gap_scan.json"
        path.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(json.dumps(result, indent=2))
        print(f"Wrote {path}")
        return

    cfg = DiracConfig(Nu=args.Nu, Nv=args.Nv, u_max=args.u_max)
    print(f"Building Dirac Nu={cfg.Nu} Nv={cfg.Nv} u_max={cfg.u_max} spectral_aps={cfg.spectral_aps}")
    result, D, u, v, evals, evecs = run_spectrum(cfg)
    # strip private
    result.pop("_evecs_shape", None)
    path = out_dir / "05_dirac_aps_spectrum.json"
    path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"|λ|_min = {result['abs_min']}")
    print(f"max residual = {result['max_residual']}")
    print(f"Wrote {path}")

    if args.overlaps:
        ov = overlap_matrix_from_evecs(evecs, cfg.Nu, cfg.Nv)
        path2 = out_dir / "06_isotype_overlaps.json"
        path2.write_text(json.dumps(ov, indent=2), encoding="utf-8")
        print(json.dumps(ov, indent=2))
        print(f"Wrote {path2}")


if __name__ == "__main__":
    main()
