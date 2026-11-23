#!/usr/bin/env python3
"""Numerical identification test: SAM-3 information current vs Riemann zeros.

This script follows the *ingredients* named in docs 17 and 27:

  - conoid Dirac spectral data
  - 12-bridge overlap matrix
  - Dual-Zero generator ε(n) = ω₀ (-1)^n n^{-n} and Reg₂
  - action S_I = ∫ |J|² dμ, evaluated here as the density S_I(k) = |J(k)|²
    on the space of spectral parameters k = σ + i t

It does **not** feed zeta zeros into the construction of J. Zeros are used
only after critical points have been found, as a comparison list.

The locked corpus does not give a unique formula that assembles those
ingredients into J (Paper 11 and SAM3_RH_Variational_Proposal.tex are
supersession stubs). Every assembly choice is documented in the
ASSUMPTIONS section of the JSON / markdown report. A null or inconclusive
result is an acceptable and expected outcome.

Usage (from the repository root):

    python code/verification/zeta_identification_test.py
"""
from __future__ import annotations

import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Dict, List, Sequence, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from dirac_conoid_aps import DiracConfig, build_dirac_matrix  # noqa: E402
from dual_zero_constructive import epsilon, reg2  # noqa: E402
from sam3_geometry_constants import N_BRIDGES, OMEGA0_GEOMETRIC  # noqa: E402

OUT = ROOT / "identification_results"
OUT.mkdir(parents=True, exist_ok=True)

SEED = 20261123
N_ZEROS = 80
# Cover a little past the 80th zero (t_80 ≈ 182.2, t_100 ≈ 236.5)
T_MIN = 5.0
T_MAX = 200.0


# ---------------------------------------------------------------------------
# Data from the repo
# ---------------------------------------------------------------------------

def twelve_bridge_overlap_matrix(u_max: float = 8.0) -> np.ndarray:
    """12×12 overlap matrix, formula taken from code/overlap_integrals.py.

    That module runs plots on import, so the integrand is reproduced here
    rather than imported. It is the same projector_overlap kernel:
        dist = |i-j| * u * 0.15
        kernel = 1/(1+dist^2) * (1 + 0.4 cos(12 (θ_i-θ_j)))
    integrated in u from 0 to u_max and normalised by u_max, then
    symmetrised and scaled so max|C| = 1, as in the original script.
    """
    from scipy.integrate import quad

    theta = np.linspace(0.0, 2.0 * np.pi, N_BRIDGES, endpoint=False)
    C = np.zeros((N_BRIDGES, N_BRIDGES), dtype=float)
    for i in range(N_BRIDGES):
        for j in range(N_BRIDGES):
            def integrand(u, i=i, j=j):
                dist = abs(i - j) * u * 0.15
                kernel = 1.0 / (1.0 + dist**2) * (1 + 0.4 * np.cos(12 * (theta[i] - theta[j])))
                return kernel

            overlap, _ = quad(integrand, 0.0, u_max)
            C[i, j] = overlap / u_max
    C = 0.5 * (C + C.T)
    C /= np.max(np.abs(C))
    return C


def conoid_dirac_spectrum(
    Nu: int = 24,
    Nv: int = 32,
    u_max: float = 6.0,
    l0: float = 1.0,
    drop_aps_artifacts: bool = True,
) -> dict:
    """Full finite Dirac spectrum on the locked right-conoid metric.

    Uses dirac_conoid_aps.build_dirac_matrix (metric coefficient 4, ω₀ lock,
    APS boundary penalty). A dense Hermitian diagonalisation is used so the
    mode tower is complete on this truncation — the production helper only
    returns a handful of eigenvalues nearest to zero, which is not enough
    for a spectral-zeta style sum.

    APS-penalty artifact: the discrete operator includes a large diagonal
    penalty of size aps_strength/du at the u-boundaries. Those eigenvalues
    sit in a tight cluster far above the bulk spectrum and are dropped by
    default (documented assumption).
    """
    cfg = DiracConfig(Nu=Nu, Nv=Nv, u_max=u_max, l0=l0, omega0=OMEGA0_GEOMETRIC)
    D, u, v = build_dirac_matrix(cfg)
    dense = D.toarray()
    # D was already symmetrised in build_dirac_matrix
    evals = np.linalg.eigvalsh(dense)
    abs_eigs = np.abs(evals)
    du = float(u[1] - u[0])
    penalty_scale = float(cfg.aps_strength / max(du, 1e-12))
    # Drop the far APS cluster: values above half the penalty scale, and in
    # any case above 20 on this dimensionless (ℓ₀=1) grid.
    cutoff = min(0.5 * penalty_scale, 20.0) if drop_aps_artifacts else np.inf
    keep = abs_eigs < cutoff
    kept = np.sort(abs_eigs[keep])
    kept = kept[kept > 1e-12]
    return {
        "config": {
            "Nu": Nu,
            "Nv": Nv,
            "u_max": u_max,
            "l0": l0,
            "omega0": OMEGA0_GEOMETRIC,
            "matrix_size": int(D.shape[0]),
            "penalty_scale": penalty_scale,
            "artifact_cutoff": cutoff if np.isfinite(cutoff) else None,
        },
        "n_total": int(len(evals)),
        "n_kept": int(len(kept)),
        "n_dropped_aps": int(np.sum(~keep)),
        "abs_min": float(kept[0]) if kept.size else None,
        "abs_max": float(kept[-1]) if kept.size else None,
        "abs_eigs": kept,
        "signed_eigs": np.sort(evals[keep]),
    }


# ---------------------------------------------------------------------------
# Assemblies of J  (each is an assumption; none is unique in the corpus)
# ---------------------------------------------------------------------------

def _dual_zero_weights(n_max: int, omega0: float = OMEGA0_GEOMETRIC) -> np.ndarray:
    return np.array([epsilon(n, omega0) for n in range(1, n_max + 1)], dtype=float)


def _reg2_sum(seq: np.ndarray) -> complex:
    """Sum of Reg₂(seq), using the constructive pairing in dual_zero_constructive.py."""
    # reg2 is written for real lists; apply to real and imag parts, or
    # pair complex values with the same rule (the definition is linear).
    paired = reg2(list(seq))
    return complex(np.sum(paired))


@dataclass
class PreparedSeries:
    """Precomputed mode data so J can be evaluated cheaply on a grid."""
    logs: np.ndarray  # shape (N,)
    weights: np.ndarray  # Dual-Zero ε(n), shape (N,)
    coeffs: np.ndarray  # extra real coefficients, shape (N,)
    kind: str


def prepare_spectral(abs_eigs: np.ndarray, use_dualzero: bool = True) -> PreparedSeries:
    ev = np.asarray(abs_eigs, dtype=float)
    logs = np.log(ev)
    n = len(ev)
    w = _dual_zero_weights(n) if use_dualzero else np.ones(n)
    return PreparedSeries(logs=logs, weights=w, coeffs=np.ones(n), kind="spectral")


def prepare_overlap_dirichlet(C: np.ndarray, use_dualzero: bool = True) -> PreparedSeries:
    n = C.shape[0]
    logs = []
    coeffs = []
    for i in range(n):
        for j in range(n):
            d = min(abs(i - j), n - abs(i - j))
            logs.append(math.log(1.0 + d) if d > 0 else 0.0)
            coeffs.append(C[i, j])
    logs_a = np.array(logs, dtype=float)
    coeffs_a = np.array(coeffs, dtype=float)
    w = _dual_zero_weights(len(logs_a)) if use_dualzero else np.ones(len(logs_a))
    return PreparedSeries(logs=logs_a, weights=w, coeffs=coeffs_a, kind="overlap_dirichlet")


def prepare_overlap_laplace(C: np.ndarray, use_dualzero: bool = False) -> PreparedSeries:
    # Ĉ(s) = Σ C_ij exp(-s Δθ_ij). Encode signed angles as "logs".
    theta = np.linspace(0.0, 2.0 * np.pi, C.shape[0], endpoint=False)
    dtheta = (theta[:, None] - theta[None, :]).ravel()
    coeffs = C.ravel().astype(float)
    logs = dtheta.astype(float)
    w = _dual_zero_weights(len(logs)) if use_dualzero else np.ones(len(logs))
    return PreparedSeries(logs=logs, weights=w, coeffs=coeffs, kind="overlap_laplace")


def J_from_prepared(s: complex, prep: PreparedSeries) -> complex:
    """J(s) = sum of c_n ε(n) exp(-s log_n), with Reg₂ pairing unless plain spectral zeta.

    Construction B (plain unweighted spectral zeta) skips Reg₂ so it is exactly Tr|D|^{-s}.
    """
    s = complex(s)
    terms = prep.coeffs * prep.weights * np.exp(-s * prep.logs)
    if prep.kind == "spectral" and np.allclose(prep.weights, 1.0):
        return complex(np.sum(terms))
    return _reg2_sum(terms)


def J_spectral_zeta_dualzero(s: complex, abs_eigs: np.ndarray) -> complex:
    """Construction A (primary, closest to docs 18 and 37)."""
    return J_from_prepared(s, prepare_spectral(abs_eigs, True))


def J_spectral_zeta_plain(s: complex, abs_eigs: np.ndarray) -> complex:
    """Construction B (sensitivity): unweighted Tr |D|^{-s}."""
    return J_from_prepared(s, prepare_spectral(abs_eigs, False))


def J_overlap_dirichlet(s: complex, C: np.ndarray, use_dualzero: bool = True) -> complex:
    """Construction C: Dirichlet-like series from 12-bridge overlaps."""
    return J_from_prepared(s, prepare_overlap_dirichlet(C, use_dualzero))


def J_overlap_laplace(s: complex, C: np.ndarray, use_dualzero: bool = False) -> complex:
    """Construction D: Laplace–Fourier transform of the overlap matrix."""
    return J_from_prepared(s, prepare_overlap_laplace(C, use_dualzero))


# ---------------------------------------------------------------------------
# Action, grids, critical points
# ---------------------------------------------------------------------------

def S_I(J: complex) -> float:
    """Density of the information action S_I = ∫ |J|² dμ at a single k."""
    return float(abs(J) ** 2)


def eval_grid(
    Jfunc: Callable[[complex], complex],
    sigmas: np.ndarray,
    ts: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """Return J and S_I arrays of shape (n_sigma, n_t)."""
    Jg = np.empty((len(sigmas), len(ts)), dtype=complex)
    for i, sig in enumerate(sigmas):
        for j, t in enumerate(ts):
            Jg[i, j] = Jfunc(complex(sig, t))
    return Jg, np.abs(Jg) ** 2


def _finite_diff_grad(S: np.ndarray, sigmas: np.ndarray, ts: np.ndarray) -> np.ndarray:
    dsig = np.gradient(S, sigmas, axis=0)
    dt = np.gradient(S, ts, axis=1)
    return np.hypot(dsig, dt)


def local_minima_2d(field: np.ndarray) -> List[Tuple[int, int]]:
    """Indices that are strictly smaller than all 8 neighbours (no edges)."""
    hits = []
    a = field
    ny, nx = a.shape
    for i in range(1, ny - 1):
        for j in range(1, nx - 1):
            patch = a[i - 1 : i + 2, j - 1 : j + 2]
            if a[i, j] <= np.min(patch) and a[i, j] < np.min(
                [a[i - 1, j], a[i + 1, j], a[i, j - 1], a[i, j + 1]]
            ):
                # require it to be a unique interior min in the 3x3
                if np.sum(patch <= a[i, j] + 1e-30) == 1:
                    hits.append((i, j))
    return hits


def refine_point(
    Jfunc: Callable[[complex], complex],
    sigma0: float,
    t0: float,
    mode: str,
) -> Tuple[float, float, float, float]:
    """Local refinement. mode='action' minimises S_I; mode='grad' minimises |∇S_I|."""
    from scipy.optimize import minimize

    def Sxy(x):
        return S_I(Jfunc(complex(x[0], x[1])))

    def Gxy(x):
        h = 1e-5
        s, t = float(x[0]), float(x[1])
        dsig = (S_I(Jfunc(complex(s + h, t))) - S_I(Jfunc(complex(s - h, t)))) / (2 * h)
        dt = (S_I(Jfunc(complex(s, t + h))) - S_I(Jfunc(complex(s, t - h)))) / (2 * h)
        return dsig * dsig + dt * dt

    fun = Sxy if mode == "action" else Gxy
    res = minimize(
        fun,
        x0=np.array([sigma0, t0], dtype=float),
        method="L-BFGS-B",
        bounds=[(0.02, 0.98), (T_MIN, T_MAX)],
        options={"maxiter": 80, "ftol": 1e-12},
    )
    sig, t = float(res.x[0]), float(res.x[1])
    J = Jfunc(complex(sig, t))
    return sig, t, S_I(J), abs(J)


def collect_critical_points(
    Jfunc: Callable[[complex], complex],
    sigmas: np.ndarray,
    ts: np.ndarray,
    Jg: np.ndarray,
    Sg: np.ndarray,
) -> dict:
    grad = _finite_diff_grad(Sg, sigmas, ts)
    # (1) near-zeros of J: local minima of |J| (equivalently of S_I)
    zero_idx = local_minima_2d(Sg)
    # (2) stationary points of S_I: local minima of |∇S_I|
    stat_idx = local_minima_2d(grad)

    def refine_list(idxs, mode, cap=200):
        # Prefer the deepest grid wells / smallest gradients if there are many hits.
        scored = []
        src = Sg if mode == "action" else grad
        for i, j in idxs:
            scored.append((float(src[i, j]), i, j))
        scored.sort()
        idxs = [(i, j) for _, i, j in scored[:cap]]
        out = []
        seen = []
        for i, j in idxs:
            sig, t, Si, absJ = refine_point(Jfunc, float(sigmas[i]), float(ts[j]), mode)
            # de-duplicate after refinement
            if any(abs(sig - s0) < 0.02 and abs(t - t0) < 0.15 for s0, t0, *_ in seen):
                continue
            seen.append((sig, t, Si, absJ))
            out.append({"sigma": sig, "t": t, "S_I": Si, "abs_J": absJ})
        return out

    zeros_j = refine_list(zero_idx, "action")
    stats = refine_list(stat_idx, "grad")
    return {
        "n_grid_minima_of_S": len(zero_idx),
        "n_grid_minima_of_grad": len(stat_idx),
        "near_zeros_of_J": zeros_j,
        "stationary_points_of_S_I": stats,
        "grad_min": float(np.min(grad)),
        "grad_median": float(np.median(grad)),
        "S_min": float(np.min(Sg)),
        "S_max": float(np.max(Sg)),
        "S_on_critical_line_min": float(np.min(Sg[np.argmin(np.abs(sigmas - 0.5)), :])),
        "S_on_critical_line_max": float(np.max(Sg[np.argmin(np.abs(sigmas - 0.5)), :])),
    }


def line_features_at_half(
    Jfunc: Callable[[complex], complex],
    ts: np.ndarray,
) -> dict:
    """1-D features of S_I(1/2 + i t), found without using zeta zeros."""
    S = np.array([S_I(Jfunc(complex(0.5, t))) for t in ts])
    # local minima and maxima of S along the line
    mins, maxs = [], []
    for j in range(1, len(ts) - 1):
        if S[j] < S[j - 1] and S[j] < S[j + 1]:
            mins.append(float(ts[j]))
        if S[j] > S[j - 1] and S[j] > S[j + 1]:
            maxs.append(float(ts[j]))
    # dS/dt zeros ≈ stationary points on the line (mins and maxs)
    return {
        "t_local_minima": mins,
        "t_local_maxima": maxs,
        "n_minima": len(mins),
        "n_maxima": len(maxs),
        "S": S,
    }


# ---------------------------------------------------------------------------
# Matching and controls
# ---------------------------------------------------------------------------

def nearest_dists(queries: Sequence[float], references: Sequence[float]) -> np.ndarray:
    if len(references) == 0:
        return np.full(len(queries), np.nan)
    ref = np.asarray(references, dtype=float)
    q = np.asarray(queries, dtype=float)
    return np.array([float(np.min(np.abs(ref - qi))) for qi in q])


def match_stats(queries: Sequence[float], references: Sequence[float], labels_for: str) -> dict:
    d = nearest_dists(queries, references)
    finite = d[np.isfinite(d)]
    if finite.size == 0:
        return {
            "compared": labels_for,
            "n_queries": int(len(queries)),
            "n_references": int(len(references)),
            "mean": None,
            "median": None,
            "frac_lt_0.25": None,
            "frac_lt_0.5": None,
            "frac_lt_1.0": None,
            "frac_lt_2.0": None,
        }
    return {
        "compared": labels_for,
        "n_queries": int(len(queries)),
        "n_references": int(len(references)),
        "mean": float(np.mean(finite)),
        "median": float(np.median(finite)),
        "frac_lt_0.25": float(np.mean(finite < 0.25)),
        "frac_lt_0.5": float(np.mean(finite < 0.5)),
        "frac_lt_1.0": float(np.mean(finite < 1.0)),
        "frac_lt_2.0": float(np.mean(finite < 2.0)),
    }


def load_zeros(n: int = N_ZEROS) -> np.ndarray:
    import mpmath

    mpmath.mp.dps = 25
    return np.array([float(mpmath.zetazero(k).imag) for k in range(1, n + 1)])


def control_sets(zeros: np.ndarray, rng: np.random.Generator) -> dict:
    mid = 0.5 * (zeros[:-1] + zeros[1:])
    # only midpoints / random t that lie in the search window
    mid = mid[(mid >= T_MIN) & (mid <= T_MAX)]
    zwin = zeros[(zeros >= T_MIN) & (zeros <= T_MAX)]
    rand = np.sort(rng.uniform(T_MIN, T_MAX, size=len(zwin)))
    return {"zeros": zwin, "midpoints": mid, "random_t": rand}


def compare_feature_list(features: Sequence[float], controls: dict) -> dict:
    """How well does a list of discovered t-values match zeros vs controls?"""
    feat = [t for t in features if T_MIN <= t <= T_MAX]
    return {
        "n_features": len(feat),
        "zeros_to_features": match_stats(controls["zeros"], feat, "each zero -> nearest feature"),
        "midpoints_to_features": match_stats(controls["midpoints"], feat, "each midpoint -> nearest feature"),
        "random_to_features": match_stats(controls["random_t"], feat, "each random t -> nearest feature"),
        "features_to_zeros": match_stats(feat, controls["zeros"], "each feature -> nearest zero"),
    }


def sigma_preference(points: List[dict]) -> dict:
    if not points:
        return {"n": 0, "mean_sigma": None, "median_sigma": None, "frac_within_0.05_of_half": None}
    sigs = np.array([p["sigma"] for p in points], dtype=float)
    return {
        "n": int(len(sigs)),
        "mean_sigma": float(np.mean(sigs)),
        "median_sigma": float(np.median(sigs)),
        "frac_within_0.05_of_half": float(np.mean(np.abs(sigs - 0.5) < 0.05)),
        "frac_within_0.10_of_half": float(np.mean(np.abs(sigs - 0.5) < 0.10)),
    }


# ---------------------------------------------------------------------------
# Reporting / plots
# ---------------------------------------------------------------------------

def make_plots(
    name: str,
    sigmas: np.ndarray,
    ts: np.ndarray,
    Sg: np.ndarray,
    line: dict,
    zeros: np.ndarray,
    points: List[dict],
) -> List[str]:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    paths = []
    i_half = int(np.argmin(np.abs(sigmas - 0.5)))

    fig, ax = plt.subplots(figsize=(11, 4.2))
    ax.plot(ts, Sg[i_half], lw=1.2, label=r'$S_I(1/2+it)$')
    zwin = zeros[(zeros >= ts[0]) & (zeros <= ts[-1])]
    ax.scatter(zwin, np.interp(zwin, ts, Sg[i_half]), c="crimson", s=18, zorder=3, label="known zeta zeros")
    if line["t_local_minima"]:
        tm = np.array(line["t_local_minima"])
        ax.scatter(tm, np.interp(tm, ts, Sg[i_half]), c="k", marker="x", s=28, zorder=4, label="minima of $S_I$ on the line")
    ax.set_xlabel("t")
    ax.set_ylabel(r"$S_I$")
    ax.set_title(f"{name}: action density on the critical line (zeros overplotted after the search)")
    ax.legend(loc="best", fontsize=8)
    ax.grid(True, alpha=0.3)
    p = OUT / f"{name}_S_on_critical_line.png"
    fig.tight_layout()
    fig.savefig(p, dpi=160)
    plt.close(fig)
    paths.append(str(p))

    fig, ax = plt.subplots(figsize=(11, 4.8))
    # log scale if dynamic range is large
    data = Sg
    if np.max(data) > 0 and np.max(data) / max(np.min(data), 1e-30) > 50:
        plot = np.log10(np.clip(data, 1e-30, None))
        label = r"$\log_{10} S_I$"
    else:
        plot = data
        label = r"$S_I$"
    im = ax.imshow(
        plot,
        aspect="auto",
        origin="lower",
        extent=[ts[0], ts[-1], sigmas[0], sigmas[-1]],
        cmap="magma",
    )
    fig.colorbar(im, ax=ax, label=label)
    ax.axhline(0.5, color="white", ls="--", lw=0.8, alpha=0.8, label=r"$\sigma=1/2$")
    if points:
        ax.scatter([p["t"] for p in points], [p["sigma"] for p in points], c="cyan", s=12, label="refined critical points")
    ax.scatter(zwin, np.full_like(zwin, 0.5), c="lime", s=8, marker="|", label="zeta zeros at σ=1/2")
    ax.set_xlabel("t")
    ax.set_ylabel(r"$\sigma$")
    ax.set_title(f"{name}: " + r"$S_I(\sigma,t)$ in the strip")
    ax.legend(loc="upper right", fontsize=7, framealpha=0.8)
    p = OUT / f"{name}_S_strip.png"
    fig.tight_layout()
    fig.savefig(p, dpi=160)
    plt.close(fig)
    paths.append(str(p))
    return paths


def drop_arrays(obj):
    """JSON-friendly copy: drop large arrays."""
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if k in {"abs_eigs", "signed_eigs", "S", "Jg", "Sg"}:
                continue
            out[k] = drop_arrays(v)
        return out
    if isinstance(obj, list):
        return [drop_arrays(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.floating, np.integer)):
        return obj.item()
    return obj


def run_construction(
    name: str,
    Jfunc: Callable[[complex], complex],
    sigmas: np.ndarray,
    ts: np.ndarray,
    zeros: np.ndarray,
    controls: dict,
    description: str,
) -> dict:
    print(f"\n=== Construction {name} ===")
    print(description)
    Jg, Sg = eval_grid(Jfunc, sigmas, ts)
    crit = collect_critical_points(Jfunc, sigmas, ts, Jg, Sg)
    line = line_features_at_half(Jfunc, ts)
    # Feature lists used for matching (t only)
    t_from_S_mins = line["t_local_minima"]
    t_from_stat = [p["t"] for p in crit["stationary_points_of_S_I"]]
    t_from_nearzero = [p["t"] for p in crit["near_zeros_of_J"]]
    # Combined unique t from 2D critical points
    t_2d = sorted(set(np.round(t_from_stat + t_from_nearzero, 5)))

    matches = {
        "line_minima_of_S": compare_feature_list(t_from_S_mins, controls),
        "twoD_stationary_t": compare_feature_list(t_from_stat, controls),
        "twoD_near_zeros_t": compare_feature_list(t_from_nearzero, controls),
        "twoD_combined_t": compare_feature_list(t_2d, controls),
    }
    pref = {
        "near_zeros_of_J": sigma_preference(crit["near_zeros_of_J"]),
        "stationary_points_of_S_I": sigma_preference(crit["stationary_points_of_S_I"]),
    }
    plots = make_plots(name, sigmas, ts, Sg, line, zeros, crit["stationary_points_of_S_I"] + crit["near_zeros_of_J"])

    # Honest one-line read of the match vs control
    z = matches["line_minima_of_S"]["zeros_to_features"]
    m = matches["line_minima_of_S"]["midpoints_to_features"]
    r = matches["line_minima_of_S"]["random_to_features"]
    print(
        f"  line minima of S_I: n={line['n_minima']}; "
        f"median dist zeros={z.get('median')}, midpoints={m.get('median')}, random={r.get('median')}"
    )
    print(
        f"  2D stationary pts: n={pref['stationary_points_of_S_I']['n']}, "
        f"median σ={pref['stationary_points_of_S_I']['mean_sigma']}"
    )
    print(f"  plots: {plots}")

    # Keep S on the line for optional later inspection (downsample)
    return {
        "name": name,
        "description": description,
        "critical": {k: v for k, v in crit.items()},
        "line": {k: v for k, v in line.items() if k != "S"},
        "matches": matches,
        "sigma_preference": pref,
        "plots": plots,
        "S_line_min": float(np.min(line["S"])),
        "S_line_max": float(np.max(line["S"])),
    }


def main() -> None:
    rng = np.random.default_rng(SEED)
    print("Loading Riemann zeros (comparison list only)...")
    zeros_all = load_zeros(N_ZEROS)
    controls = control_sets(zeros_all, rng)
    print(f"  {len(zeros_all)} zeros; {len(controls['zeros'])} inside t in [{T_MIN}, {T_MAX}]")

    print("Computing 12-bridge overlap matrix (overlap_integrals kernel)...")
    C = twelve_bridge_overlap_matrix()
    np.save(OUT / "overlap_matrix.npy", C)

    print("Computing conoid Dirac spectrum (full dense eigensolve on a modest grid)...")
    spec = conoid_dirac_spectrum()
    abs_eigs = spec["abs_eigs"]
    print(
        f"  matrix {spec['config']['matrix_size']}, kept {spec['n_kept']} of {spec['n_total']} "
        f"(|λ| in [{spec['abs_min']:.4g}, {spec['abs_max']:.4g}]), "
        f"dropped {spec['n_dropped_aps']} APS-penalty modes"
    )
    np.save(OUT / "dirac_abs_eigs.npy", abs_eigs)

    # Shuffled / permuted spectral data (same values, destroyed order / pairings)
    shuf = abs_eigs.copy()
    rng.shuffle(shuf)
    # Replace spectrum with a log-uniform draw of the same length and similar range
    fake = np.sort(np.exp(rng.uniform(np.log(abs_eigs[0]), np.log(abs_eigs[-1]), size=len(abs_eigs))))
    C_perm = C.copy()
    # Permute off-diagonal pairings while keeping symmetry and diagonal
    idx = rng.permutation(C.shape[0])
    C_perm = C[np.ix_(idx, idx)]

    sigmas = np.linspace(0.10, 0.90, 33)
    ts = np.linspace(T_MIN, T_MAX, 781)  # step 0.25

    constructions = []

    prep_A = prepare_spectral(abs_eigs, True)
    prep_B = prepare_spectral(abs_eigs, False)
    prep_C = prepare_overlap_dirichlet(C, True)
    prep_D = prepare_overlap_laplace(C, False)
    prep_A_shuf = prepare_spectral(shuf, True)
    prep_B_fake = prepare_spectral(fake, False)
    prep_C_perm = prepare_overlap_dirichlet(C_perm, True)

    constructions.append(
        run_construction(
            "A_dualzero_spectral_zeta",
            lambda s, p=prep_A: J_from_prepared(s, p),
            sigmas,
            ts,
            zeros_all,
            controls,
            "Primary: Dual-Zero Reg₂ of |λ_n|^{-s} ε(n) on the ordered Dirac mode tower.",
        )
    )
    constructions.append(
        run_construction(
            "B_plain_spectral_zeta",
            lambda s, p=prep_B: J_from_prepared(s, p),
            sigmas,
            ts,
            zeros_all,
            controls,
            "Sensitivity: unweighted Tr|D|^{-s} on the same Dirac eigenvalues.",
        )
    )
    constructions.append(
        run_construction(
            "C_overlap_dirichlet",
            lambda s, p=prep_C: J_from_prepared(s, p),
            sigmas,
            ts,
            zeros_all,
            controls,
            "12-bridge overlaps as a Dirichlet series C_ij (1+d_ij)^{-s}, Dual-Zero / Reg₂ summed.",
        )
    )
    constructions.append(
        run_construction(
            "D_overlap_laplace",
            lambda s, p=prep_D: J_from_prepared(s, p),
            sigmas,
            ts,
            zeros_all,
            controls,
            "Laplace–Fourier transform of the overlap matrix, Ĉ(s)=Σ C_ij exp(-s(θ_i-θ_j)).",
        )
    )

    # Controls that destroy the geometric data
    print("\n=== Shuffled / fake-spectrum controls on construction A and B ===")
    constructions.append(
        run_construction(
            "A_shuffled_mode_order",
            lambda s, p=prep_A_shuf: J_from_prepared(s, p),
            sigmas,
            ts,
            zeros_all,
            controls,
            "Control: construction A after randomly permuting the |λ_n| list (Dual-Zero still uses n).",
        )
    )
    constructions.append(
        run_construction(
            "B_fake_loguniform_spectrum",
            lambda s, p=prep_B_fake: J_from_prepared(s, p),
            sigmas,
            ts,
            zeros_all,
            controls,
            "Control: construction B on a fake log-uniform spectrum with the same count and range.",
        )
    )
    constructions.append(
        run_construction(
            "C_permuted_bridges",
            lambda s, p=prep_C_perm: J_from_prepared(s, p),
            sigmas,
            ts,
            zeros_all,
            controls,
            "Control: construction C after a joint permutation of bridge labels.",
        )
    )

    assumptions = {
        "repo_definitions_used": [
            "Locked metric f=sqrt(u^2+4 ℓ_0^2 cos^2(2v)) in dirac_conoid_aps._metric_f",
            "ω₀ = 0.927 from sam3_geometry_constants / doc 18",
            "ε(n)=ω₀(-1)^n n^{-n} and Reg₂(a)_n=(a_{2n}+a_{2n+1})/2 from dual_zero_constructive.py and doc 18",
            "ζ_D(s)=Tr|D|^{-s} named in docs/hardening/37_Regulator_Comparison_DZ_vs_HeatKernel_Zeta.md",
            "S_I = ∫ |J|^2 dμ and 'critical points of S_I' from docs/hardening/27_RH_Variational_Residual_Lock.md",
            "12-bridge overlap kernel from code/overlap_integrals.py",
            "N_BRIDGES = 12",
        ],
        "assumptions_required_because_J_is_not_uniquely_defined": [
            "Paper 11 and SAM3_RH_Variational_Proposal.tex are stubs and do not supply a formula for J.",
            "The old stationarity scripts' J is a proxy that hard-codes a peak at σ=1/2 and is not used here as a definition.",
            "S_I is evaluated as the density |J(k)|^2 at a point k in the strip, not as a fully specified integral over a measure μ.",
            "Dirac spectrum is a finite APS-truncated discrete operator at Nu=24, Nv=32, u_max=6, ℓ₀=1; continuum residual is acknowledged in the repo.",
            "Eigenvalues above min(20, 0.5*aps_penalty/du) are dropped as APS-boundary artifacts.",
            "Modes are ordered by increasing |λ| before applying ε(n). That ordering is an assumption.",
            "Construction C flattens the 12×12 overlap matrix row-major and treats that as a mode tower for Dual-Zero.",
            "Construction D uses Ĉ(s)=Σ C_ij exp(-s(θ_i-θ_j)); the old comment |C(k1-k2)| does not fix this kernel.",
            "Search window t ∈ [5, 200], σ ∈ [0.10, 0.90], grid steps Δσ≈0.025, Δt=0.25, then L-BFGS-B refinement.",
            "Identification is judged by whether discovered t-values sit closer to known zeros than to midpoints or random t of the same count.",
        ],
        "seed": SEED,
        "n_zeros_requested": N_ZEROS,
        "t_window": [T_MIN, T_MAX],
    }

    payload = {
        "assumptions": assumptions,
        "spectrum": drop_arrays(spec),
        "overlap_shape": list(C.shape),
        "overlap_diag_mean": float(np.mean(np.diag(C))),
        "n_zeros": int(len(zeros_all)),
        "n_zeros_in_window": int(len(controls["zeros"])),
        "first_and_last_zero_in_window": [
            float(controls["zeros"][0]),
            float(controls["zeros"][-1]),
        ] if len(controls["zeros"]) else None,
        "constructions": drop_arrays(constructions),
    }
    path = OUT / "identification_test.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nWrote {path}")

    # Compact stdout conclusion
    print("\n===== COMPACT MATCH TABLE (median distance of each zero to nearest feature) =====")
    print(f"{'construction':<32} {'feat':<22} {'n':>4} {'d_zeros':>10} {'d_mids':>10} {'d_rand':>10}")
    for c in constructions:
        for key in ("line_minima_of_S", "twoD_combined_t"):
            m = c["matches"][key]
            z = m["zeros_to_features"]
            mid = m["midpoints_to_features"]
            rnd = m["random_to_features"]
            def fmt(x):
                return "    n/a" if x is None else f"{x:10.3f}"
            print(
                f"{c['name']:<32} {key:<22} {m['n_features']:>4} "
                f"{fmt(z.get('median'))} {fmt(mid.get('median'))} {fmt(rnd.get('median'))}"
            )


if __name__ == "__main__":
    main()
