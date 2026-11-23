#!/usr/bin/env python3
"""Reproduce every number claimed in the core paper, from definitions.

This is the authoritative reproduction entry point (November 2026).

    python code/core_reproducibility.py
    pytest -q

No experimental input. Unproven quantities are labelled as such. The older
script code/reproduce_status_locked.py mostly asserts hardcoded phenomenology
constants against themselves and is retained only as a historical artefact.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from core_geometry import (  # noqa: E402
    C0_CONVERGED,
    C0_PAPER_BAND,
    C0_finite_part,
    c4_is_not_a5,
    curvature_formula_matches,
    f_metric,
    gaussian_curvature,
    ground_energy_radial,
    has_c4_isometry,
    induced_metric_coeff,
    natural_curvature_radii,
    tip_nodes,
)
from aps_hermitian import (  # noqa: E402
    conoid_spectrum_hermitian,
    convergence_study,
    legacy_symmetrised_torus,
    torus_known_answer,
)


def gn_prefactor_status() -> dict:
    """G_N = 64 π ℓ0² / 45 is a convention lock, not an independent derivation.

    Math note 09 / 16: the Einstein–Hilbert term in a2 implies G_N ∝ ℓ0².
    The pure number 64π/45 is equivalent to fixing a normalisation
    𝒩 = 45/(1024 π²) that absorbs (φ2, C_SA, Vol_reg). It is not scheme-free.
    """
    return {
        "structural": "G_N = alpha * ell0^2, with alpha scheme-dependent",
        "recorded_normalisation": "G_N = 64*pi*ell0^2/45",
        "equivalent_N_cal": 45.0 / (1024.0 * math.pi**2),
        "status": "convention lock, not independently derived",
    }


def main() -> int:
    out_dir = ROOT / "reproducibility"
    out_dir.mkdir(parents=True, exist_ok=True)

    metric = induced_metric_coeff()
    c4 = has_c4_isometry()
    a5 = c4_is_not_a5()
    tips = tip_nodes()
    curv_ok = curvature_formula_matches()
    kmax = gaussian_curvature(0.0, 0.0)  # u=0, |cos(2v)|=1 => K=-1/4

    c0_values = {str(U): C0_finite_part(float(U)) for U in (200, 400, 1000)}
    c0_converged = C0_CONVERGED
    old_band = list(C0_PAPER_BAND)
    c0_reproduces_old_band = any(old_band[0] <= v <= old_band[1] for v in c0_values.values())

    energies = {str(m): ground_energy_radial(m, U=20.0, N=400) for m in (0, 1, 2, 3)}
    mono = list(energies.values()) == sorted(energies.values()) and len(set(energies.values())) == 4

    omega = natural_curvature_radii()
    natural_hit_0927 = any(
        abs(omega[name]["omega0_if_4_13"] - 0.927) < 0.05
        for name in ("1/|K|_max", "1/sqrt(|K|_max)", "ell0", "2*ell0")
    )

    torus = torus_known_answer(N=24, k_compare=8)
    conv = convergence_study(N_list=(8, 12, 16, 24, 32))
    legacy = legacy_symmetrised_torus(N=16)
    conoid = conoid_spectrum_hermitian(Nu=24, Nv=24, u_max=6.0, k=8)

    report = {
        "paper": "papers/SAM3_Core_Geometry_and_Spectral_Results.tex",
        "metric": {
            "tip_coefficient": metric["tip_coefficient"],
            "symbolic_ok": metric.get("symbolic_ok"),
            "g_vv_formula": metric["g_vv_formula"],
            "status": "proposition: follows from the locked embedding",
        },
        "C4_isometry": {"holds": c4, "status": "proposition"},
        "A5_is_not_an_isometry": {**{k: (float(v) if isinstance(v, float) else v) for k, v in a5.items()}, "status": "proposition (counterexample)"},
        "tip_nodes": {"v": tips, "f_at_nodes": [f_metric(0.0, v) for v in tips], "status": "proposition"},
        "gaussian_curvature": {
            "formula": "K = -4 ell0^2 cos^2(2v) / f^4",
            "identity_and_FD_ok": curv_ok,
            "K_at_curvature_max": kmax,
            "status": "proposition",
        },
        "C0": {
            "values": c0_values,
            "converged_value": c0_converged,
            "old_paper_band_4.43_4.45": old_band,
            "old_band_reproduced": c0_reproduces_old_band,
            "status": "existence is a proposition; the number is a numerical observation",
            "note": "The band 4.43--4.45 in earlier drafts does not reproduce under adaptive quadrature.",
        },
        "channel_energies_Dirichlet_cutoff": {
            "E0": energies,
            "strictly_increasing": mono,
            "status": "numerical check of the variational theorem (m=0 indicative only)",
        },
        "G_N": gn_prefactor_status(),
        "omega0_and_4_13": {
            "natural_radii": omega,
            "any_natural_radius_gives_0.927": natural_hit_0927,
            "status": "not derived",
            "missing": [
                "a unique geometric definition of R_curv",
                "a derivation of the exponent 4/13",
                "a reason to pair that R with D_bridge=2π/12",
            ],
        },
        "APS_Dirac": {
            "torus_antiperiodic_N24": {
                "max_abs_error": torus["max_abs_error"],
                "hermiticity_error": torus["hermiticity_error"],
                "numerical": torus["numerical"],
                "nearest_exact": torus["nearest_exact"],
            },
            "convergence": conv,
            "legacy_symmetrised_is_not_Dirac": not legacy["legacy_recovers_first_nonzero_dirac_mode"],
            "legacy": {k: legacy[k] for k in legacy if k != "note"},
            "conoid_truncated_numerical": conoid,
            "status": "Hermitian discretisation verified on the flat torus (known answer, order ≈ 2). Conoid+APS remains truncated numerics, not a continuum index theorem.",
        },
    }

    path = out_dir / "core_results.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("SAM-3 core reproducibility")
    print("=========================")
    print(f"metric tip coefficient 4 (symbolic ok): {metric.get('symbolic_ok')}")
    print(f"C4 isometry: {c4}")
    print(f"A5 is not an isometry: {not a5['equal']}")
    print(f"curvature identity: {curv_ok}")
    print(f"C0(200)={c0_values['200']:.7f}  C0(400)={c0_values['400']:.7f}  C0(1000)={c0_values['1000']:.7f}")
    print(f"C0 converged (recorded): {c0_converged}")
    print(f"old band 4.43--4.45 reproduced? {c0_reproduces_old_band}")
    print(f"E0(m=0,1,2,3) = " + ", ".join(f"{energies[str(m)]:.6f}" for m in (0, 1, 2, 3)))
    print(f"strictly increasing: {mono}")
    print(f"G_N prefactor: {report['G_N']['status']}")
    print(f"natural radii give ω0=0.927? {natural_hit_0927}")
    print(f"torus N=24 max |λ-λ_exact| = {torus['max_abs_error']:.6g}")
    print(f"convergence slope = {conv['log_log_slope']:.4f} (expect -2)")
    print(f"legacy recovers first nonzero Dirac mode? {legacy['legacy_recovers_first_nonzero_dirac_mode']}")
    print(f"Wrote {path}")
    # Fail only if a claimed theorem-level check failed.
    ok = (
        metric.get("symbolic_ok")
        and c4
        and (not a5["equal"])
        and curv_ok
        and (not c0_reproduces_old_band)
        and abs(c0_values["400"] - c0_converged) < 2e-5
        and mono
        and (not natural_hit_0927)
        and torus["max_abs_error"] < 0.01
        and abs(conv["log_log_slope"] + 2.0) < 0.08
        and (not legacy["legacy_recovers_first_nonzero_dirac_mode"])
    )
    if not ok:
        print("FAILED: a core check did not hold. See the JSON report.")
        return 1
    print("OK — theorem-level geometry checks passed; residuals documented.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
