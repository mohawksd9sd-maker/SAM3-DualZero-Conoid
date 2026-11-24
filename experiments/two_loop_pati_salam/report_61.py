"""Numbers quoted in doc 61 (run: python report_61.py, ~40 s)."""

from __future__ import annotations

import json
import math
from pathlib import Path

import top_yukawa_search as ts


def kk_identity() -> dict:
    """Per Landau level: Higgs-wavefunction Yukawa term vs universal gauge term in d ln(y_t/g)/dt.

    With y_t^2 (3+n) = 4 g^2 (spectral relation, b, tau dropped) and one Dirac copy of the
    three-generation matter per level: 2 (3 + n) y_t^2 = 8 g^2 = (8/3) * 3 g^2 = Delta b_level g^2.
    """
    out = {}
    for n in (0.0, 1.0, 2.0, 3.0):
        yt2 = 4.0 / (3 + n)
        out[str(n)] = {"yukawa_term": 2 * (3 + n) * yt2, "gauge_term": 8.0 / 3.0 * 3}
    return out


def main() -> Path:
    vl = {}
    for m, lab in ((1, "VL lepton doublet+singlet"), (3, "VL quark doublet+singlet"), (4, "VL PS 16+16bar pair"),
                   (8, "two VL 16 pairs"), (12, "three VL 16 pairs")):
        x = ts.solve_for(lambda x: ts._mt(ts.Cand(x=x, x4=x * x / m)), 172.5, 0.0, 8.0, 17)
        r = ts.predict(ts.Cand(x=x, x4=x * x / m))
        vl[lab] = {"multiplicity": m, "x": x, "c=y_X/y_t": math.sqrt(x / m), "Mt": r["Mt"], "Mh": r["Mh"],
                   **ts.pulls(r), "seesaw": ts.seesaw_check(r)}
    r = ts.predict(ts.Cand(x=2.1, x4=0.0))
    vl["limit x4 -> 0 (many tiny Yukawas)"] = {"x": 2.1, "Mt": r["Mt"], "Mh": r["Mh"]}
    kk = ts.cand4()
    kk["higgs_not_on_towers"] = {}
    for f in (0.5, 0.3):
        rr = ts.predict(ts.Cand(kk_Mc_over_Lambda=f, kk_yukawa_factor=0.0))
        kk["higgs_not_on_towers"][str(f)] = {"Mt": rr["Mt"], "Mh": rr["Mh"]}
    kk["identity"] = kk_identity()
    base = ts.predict(ts.Cand())
    out = {
        "baseline_doc60": {"Mt": base["Mt"], "Mh": base["Mh"], "yt_B": base["yt_B"], "yt_B_data": base["yt_B_data"],
                           "g_B": base["g_B"], "m_R": base["m_R"], "Lambda": base["Lambda"], "seesaw": ts.seesaw_check(base)},
        "c1_large_ynu": ts.cand1(),
        "c2_vector_like": vl,
        "c2_trace_vs_quartic": ts.cand2(),
        "c3_lambda_chain": ts.cand3(),
        "c4_flux_towers": kk,
        "c5_numerology": ts.cand5(),
        "c6_sm_group_BF": ts.cand6(),
        "c7_twisted_grand": ts.cand7(),
        "combo_VL16_plus_ynu": ts.combo(4),
        "combo_VLquark_plus_ynu": ts.combo(3),
    }
    path = Path(__file__).with_name("results_doc61.json")
    path.write_text(json.dumps(out, indent=1, default=float))
    return path


if __name__ == "__main__":
    print(main())
