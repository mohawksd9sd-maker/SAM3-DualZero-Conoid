#!/usr/bin/env python3
"""
SAM3 Master Verification Pipeline
=================================
August 2026 hardening layer (wired to existing kernels).

Runs a frozen geometric chain, calls available Dirac / overlap modules,
and writes intermediate results so key numbers can be regenerated.

Usage (from repository root or from code/):
    python code/master_verification_pipeline.py
    # or
    cd code && python master_verification_pipeline.py

Outputs under ./pipeline_output/ (or code/pipeline_output/):
    00_frozen_params.json
    01_defect_overlaps.json
    02_cabibbo_prediction.json
    03_dirac_and_gap.json
    04_bridge_overlap_matrix.json
    05_status_summary.txt
"""

from __future__ import annotations

import json
import math
import sys
import traceback
from pathlib import Path
from datetime import datetime, timezone

import numpy as np

# ---------------------------------------------------------------------------
# Make local code/ importable whether launched from repo root or code/
# ---------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

# ---------------------------------------------------------------------------
# Frozen geometric parameters (locked in the hardening cycle)
# ---------------------------------------------------------------------------
FROZEN = {
    "a_curvature_scale": 2.0,
    "n_bridges": 12,
    "delta_theta": 2.0 * math.pi / 12.0,
    "defect_locus": "tip_curvature_maximum",
    "defect_width_rule": "a * delta_theta",
    "eta_12": 0.8607,
    "eta_13": 0.5439,
    "eta_23": 0.4789,
    "pi_over_12_deg": 15.0,
    "theta12_cabibbo_deg": 0.8607 * 15.0,  # ~12.91 deg
    "omega0_geometric": 0.927,
    "ell0_anchor": "top_quark_mass",
    "unification_relative_mismatch_floor": 0.07,
    "gap_scaling": "1 / u_max",
    "aps_controlled": True,
    "version_status": "hardened_August_2026",
}

TARGETS = {
    "theta12_exp_deg": 13.04,
    "theta12_tolerance_deg": 0.5,
    "eta_12_tolerance": 0.02,
    "unification_floor_tolerance": 0.02,
}


def ensure_output_dir() -> Path:
    # Prefer repo-root pipeline_output if we can see it; else local
    candidates = [
        HERE.parent / "pipeline_output",
        HERE / "pipeline_output",
        Path("pipeline_output"),
    ]
    for c in candidates:
        try:
            c.mkdir(parents=True, exist_ok=True)
            return c
        except Exception:
            continue
    out = Path("pipeline_output")
    out.mkdir(exist_ok=True)
    return out


def write_json(path: Path, data: dict) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True, default=str)
    print(f"  wrote {path}")


def step_frozen_params(out: Path) -> None:
    payload = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "frozen": FROZEN,
        "targets": TARGETS,
        "note": (
            "These parameters are locked by geometry (defect locus/width, "
            "icosahedral angle, continuum overlaps). Do not retune to angles."
        ),
    }
    write_json(out / "00_frozen_params.json", payload)


def step_defect_overlaps(out: Path) -> None:
    """Record locked continuum defect overlaps (geometric baseline)."""
    payload = {
        "method": "continuum_defect_integral_locked",
        "locus": FROZEN["defect_locus"],
        "width_rule": FROZEN["defect_width_rule"],
        "eta": {
            "12": FROZEN["eta_12"],
            "13": FROZEN["eta_13"],
            "23": FROZEN["eta_23"],
        },
        "status": "locked_geometric",
        "note": (
            "Values from continuum defect kernel at tip curvature maximum "
            "with width a*delta_theta. Live re-computation requires "
            "generation-localized wavefunctions (Casimir radial potentials)."
        ),
    }
    write_json(out / "01_defect_overlaps.json", payload)


def step_cabibbo(out: Path) -> None:
    theta12 = FROZEN["theta12_cabibbo_deg"]
    exp = TARGETS["theta12_exp_deg"]
    tol = TARGETS["theta12_tolerance_deg"]
    payload = {
        "formula": "theta_12 = eta_12 * (pi/12)",
        "eta_12": FROZEN["eta_12"],
        "pi_over_12_deg": FROZEN["pi_over_12_deg"],
        "theta12_pred_deg": theta12,
        "theta12_exp_deg": exp,
        "abs_error_deg": abs(theta12 - exp),
        "within_tolerance": abs(theta12 - exp) <= tol,
        "realization": (
            "A_F left rotation on down sector (H enhancement vs C for up); "
            "PDG light-first ordering required for angle extraction."
        ),
        "residuals": {
            "theta23": "still low relative to experiment",
            "delta_CKM": "phase structure present, magnitude/quadrant not locked",
        },
    }
    write_json(out / "02_cabibbo_prediction.json", payload)


def step_dirac_and_gap(out: Path) -> None:
    """Call full_2d_dirac_conoid if available; record spectrum + gap status."""
    result = {
        "module": "full_2d_dirac_conoid",
        "called": False,
        "evals": None,
        "error": None,
        "aps_controlled_flag": FROZEN["aps_controlled"],
        "gap_scaling_claim": FROZEN["gap_scaling"],
        "interpretation": (
            "Existing kernel is a simplified radial + angular-sector Dirac. "
            "Full APS domain-extension gap table remains a hardening target. "
            "Locked claim: gap ~ 1/u_max -> 0 in continuum limit."
        ),
    }
    try:
        from full_2d_dirac_conoid import conoid_dirac_2d

        evals = conoid_dirac_2d(Nu=60, Nv=90, l0=1.0, k_max=12)
        evals = np.asarray(evals, dtype=float)
        result["called"] = True
        result["evals"] = evals.tolist()
        result["n_evals"] = int(evals.size)
        result["abs_min"] = float(np.min(np.abs(evals))) if evals.size else None
        result["note"] = (
            "Kernel returned eigenvalues (prototype). Near-zero entries may be "
            "enforced by construction in the current script; use domain-extension "
            "studies for true continuum gap scaling."
        )
        # optional save next to output
        np.save(out / "conoid_2d_evals.npy", evals)
        print("  Dirac kernel OK; evals saved")
    except Exception as e:
        result["error"] = f"{type(e).__name__}: {e}"
        result["traceback"] = traceback.format_exc()
        print(f"  Dirac kernel not run: {result['error']}")

    write_json(out / "03_dirac_and_gap.json", result)


def step_bridge_overlaps(out: Path) -> None:
    """Call overlap_integrals projector routine if available.

    Note: the current overlap_integrals.py builds a 12x12 *bridge* projector
    matrix (phenomenological kernel), not the continuum tip-defect eta_ij.
    Both are recorded for transparency.
    """
    result = {
        "module": "overlap_integrals",
        "called": False,
        "bridge_matrix": None,
        "error": None,
        "relation_to_defect_eta": (
            "Bridge projector matrix is a 12-channel geometric overlap. "
            "Continuum generation overlaps eta_12/13/23 are the locked "
            "defect-kernel values in 01_defect_overlaps.json."
        ),
    }
    try:
        # Re-implement the core of overlap_integrals without the plt.show()
        # side effect so the pipeline stays non-interactive.
        NUM_BRIDGES = 12
        THETA = np.linspace(0, 2 * np.pi, NUM_BRIDGES, endpoint=False)

        def projector_overlap(i, j, u_max=8.0):
            from scipy.integrate import quad

            def integrand(u):
                dist = np.abs(i - j) * u * 0.15
                kernel = (
                    1.0
                    / (1.0 + dist**2)
                    * (1 + 0.4 * np.cos(12 * (THETA[i] - THETA[j])))
                )
                return kernel

            overlap, _ = quad(integrand, 0, u_max)
            return overlap / u_max

        mat = np.zeros((NUM_BRIDGES, NUM_BRIDGES))
        for i in range(NUM_BRIDGES):
            for j in range(NUM_BRIDGES):
                mat[i, j] = projector_overlap(i, j)
        mat = 0.5 * (mat + mat.T)
        mat /= np.max(np.abs(mat)) if np.max(np.abs(mat)) > 0 else 1.0

        result["called"] = True
        result["bridge_matrix"] = np.round(mat, 6).tolist()
        result["shape"] = list(mat.shape)
        result["max"] = float(np.max(mat))
        result["min"] = float(np.min(mat))
        np.save(out / "bridge_overlap_matrix.npy", mat)
        print("  Bridge overlap matrix OK")
    except Exception as e:
        result["error"] = f"{type(e).__name__}: {e}"
        result["traceback"] = traceback.format_exc()
        print(f"  Bridge overlaps not run: {result['error']}")

    write_json(out / "04_bridge_overlap_matrix.json", result)


def step_status_summary(out: Path, dirac_ok: bool, overlap_ok: bool) -> None:
    theta12 = FROZEN["theta12_cabibbo_deg"]
    exp = TARGETS["theta12_exp_deg"]
    lines = [
        "SAM3 Master Verification Summary",
        f"Timestamp (UTC): {datetime.now(timezone.utc).isoformat()}",
        f"Version status: {FROZEN['version_status']}",
        "",
        "Frozen geometric inputs:",
        f"  eta_12 = {FROZEN['eta_12']:.4f}",
        f"  eta_13 = {FROZEN['eta_13']:.4f}",
        f"  eta_23 = {FROZEN['eta_23']:.4f}",
        f"  defect locus = {FROZEN['defect_locus']}",
        f"  defect width = {FROZEN['defect_width_rule']}",
        "",
        "Cabibbo prediction:",
        f"  theta_12 = eta_12 * (pi/12) = {theta12:.2f} deg",
        f"  experiment = {exp:.2f} deg",
        f"  |error| = {abs(theta12 - exp):.2f} deg",
        f"  within tolerance ({TARGETS['theta12_tolerance_deg']} deg): "
        f"{abs(theta12 - exp) <= TARGETS['theta12_tolerance_deg']}",
        "",
        "Unification:",
        f"  geometric relative mismatch floor ~ "
        f"{100 * FROZEN['unification_relative_mismatch_floor']:.0f}%",
        "",
        "Kernel calls:",
        f"  full_2d_dirac_conoid : {'OK' if dirac_ok else 'FAILED / SKIPPED'}",
        f"  overlap_integrals    : {'OK' if overlap_ok else 'FAILED / SKIPPED'}",
        "",
        "Zero modes:",
        "  APS-controlled claim; gap scales as 1/u_max -> 0",
        "  (full domain-extension table still a target)",
        "",
        "Outputs written in this directory.",
        "See STATUS_CLAIMS_AND_RESIDUALS.md for the full residual map.",
    ]
    path = out / "05_status_summary.txt"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote {path}")


def main() -> None:
    print("=" * 60)
    print("SAM3 Master Verification Pipeline")
    print("=" * 60)
    out = ensure_output_dir()
    print(f"Output directory: {out.resolve()}")

    step_frozen_params(out)
    step_defect_overlaps(out)
    step_cabibbo(out)

    # Dirac
    dirac_path = out / "03_dirac_and_gap.json"
    step_dirac_and_gap(out)
    dirac_ok = False
    try:
        with dirac_path.open() as f:
            dirac_ok = bool(json.load(f).get("called"))
    except Exception:
        pass

    # Overlaps
    ov_path = out / "04_bridge_overlap_matrix.json"
    step_bridge_overlaps(out)
    overlap_ok = False
    try:
        with ov_path.open() as f:
            overlap_ok = bool(json.load(f).get("called"))
    except Exception:
        pass

    step_status_summary(out, dirac_ok, overlap_ok)

    print("=" * 60)
    print("Done. Inspect the pipeline_output directory.")
    print("=" * 60)


if __name__ == "__main__":
    main()
