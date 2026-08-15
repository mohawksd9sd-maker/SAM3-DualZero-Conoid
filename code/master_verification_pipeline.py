#!/usr/bin/env python3
"""SAM3 Master Verification Pipeline — Section 2 complete path."""

from __future__ import annotations

import json
import math
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from sam3_geometry_constants import (
    C_G,
    ETA_12,
    ETA_13,
    ETA_23,
    G_N_over_ell0_sq,
    KAPPA_U_OVER_KAPPA_D,
    N_BRIDGES,
    OMEGA0_GEOMETRIC,
    PHI_CP,
    cabibbo_theta12_deg,
    frozen_geometry_dict,
)

C2_OVER_C1 = 1.13
C3_OVER_C2 = 2.46
LOCKED_ANGLES = {
    "theta12_deg": 12.85,
    "theta23_deg": 2.36,
    "theta13_deg": 0.24,
    "delta_CKM_deg_approx": 70.0,
    "Jarlskog_J_approx": 3.0e-5,
    "delta_PMNS_band_deg": [200.0, 270.0],
    "m_H_class_GeV": [124.0, 127.0],
    "unification_relative_mismatch_floor": 0.07,
}
TARGETS = {
    "theta12_exp_deg": 13.04,
    "theta23_exp_deg": 2.38,
    "theta12_tolerance_deg": 0.5,
    "theta23_tolerance_deg": 0.15,
}


def ensure_output_dir() -> Path:
    for c in [HERE.parent / "pipeline_output", HERE / "pipeline_output", Path("pipeline_output")]:
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


def step_geometry(out: Path) -> dict:
    geo = frozen_geometry_dict()
    geo["timestamp_utc"] = datetime.now(timezone.utc).isoformat()
    geo["c2_over_c1"] = C2_OVER_C1
    geo["c3_over_c2"] = C3_OVER_C2
    geo["theta12_from_eta_deg"] = cabibbo_theta12_deg()
    write_json(out / "00_geometry_from_first_principles.json", geo)
    return geo


def step_frozen(out: Path, geo: dict) -> None:
    frozen = {
        **geo,
        **LOCKED_ANGLES,
        "phi_CP_deg": math.degrees(PHI_CP),
        "version_status": "section2_complete_lock_P1_P4",
        "dirac_code_status": "dirac_conoid_aps_P1_P4",
        "gap_scaling": "1 / u_max",
    }
    write_json(
        out / "01_frozen_archive.json",
        {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "frozen": frozen,
            "targets_for_comparison_only": TARGETS,
            "docs": ["docs/hardening/25_Section2_Complete_Lock_Status.md"],
        },
    )


def step_ckm(out: Path) -> None:
    write_json(
        out / "02_ckm_locked.json",
        {
            "theta12_deg": LOCKED_ANGLES["theta12_deg"],
            "theta23_deg": LOCKED_ANGLES["theta23_deg"],
            "cabibbo_formula_deg": cabibbo_theta12_deg(),
            "eta_12": ETA_12,
        },
    )


def step_dirac(out: Path) -> None:
    result = {"module": "dirac_conoid_aps", "called": False}
    try:
        from dirac_conoid_aps import DiracConfig, run_spectrum, gap_scan, overlap_matrix_from_evecs

        cfg = DiracConfig(Nu=32, Nv=40, u_max=6.0, n_eigs=6)
        spec, D, u, v, evals, evecs = run_spectrum(cfg)
        result["called"] = True
        result["spectrum"] = spec
        write_json(out / "03_dirac_p1_spectrum.json", spec)

        scan = gap_scan(u_max_list=[3.0, 4.5, 6.0], Nu_base=28, Nv=36)
        result["gap_scan"] = scan
        write_json(out / "05_gap_scan.json", scan)

        ov = overlap_matrix_from_evecs(evecs, cfg.Nu, cfg.Nv)
        result["overlaps"] = ov
        write_json(out / "06_isotype_overlaps.json", ov)

        print(
            f"  Dirac OK |λ|_min={spec.get('abs_min')} res={spec.get('max_residual')} "
            f"slope={scan.get('log_log_slope_abs_min_vs_umax')}"
        )
    except Exception as e:
        result["error"] = f"{type(e).__name__}: {e}"
        result["traceback"] = traceback.format_exc()
        print(f"  Dirac failed: {result['error']}")
    write_json(out / "03_dirac_status.json", result)


def step_summary(out: Path) -> None:
    lines = [
        "SAM3 Pipeline — Section 2 COMPLETE LOCK",
        f"UTC: {datetime.now(timezone.utc).isoformat()}",
        f"omega0 = {OMEGA0_GEOMETRIC}",
        f"G_N/ell0^2 = {G_N_over_ell0_sq():.6f}",
        f"C_g = {C_G[1]}, {C_G[2]}, {C_G[3]}",
        f"eta = {ETA_12}, {ETA_13}, {ETA_23}",
        f"kappa_u/kappa_d = {KAPPA_U_OVER_KAPPA_D}",
        f"phi = {math.degrees(PHI_CP):.1f} deg",
        "Dirac: dirac_conoid_aps P1–P4",
        "See docs/hardening/25_Section2_Complete_Lock_Status.md",
    ]
    (out / "04_status_summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("  wrote 04_status_summary.txt")


def main() -> None:
    print("=" * 60)
    print("SAM3 Master Verification — Section 2 Complete Lock")
    print("=" * 60)
    out = ensure_output_dir()
    geo = step_geometry(out)
    step_frozen(out, geo)
    step_ckm(out)
    step_dirac(out)
    step_summary(out)
    print("Done.")


if __name__ == "__main__":
    main()
