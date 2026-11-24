"""Numbers and figure for doc 67 (run: python report_67.py, ~15 s)."""

from __future__ import annotations

import json
import math
import shutil
from pathlib import Path

import numpy as np

import derived_mechanisms as dm
import top_yukawa_search as ts

HERE = Path(__file__).resolve().parent
FIG = HERE / "fig_doc67_dial.png"
FIG_DOC = HERE.parents[1] / "docs" / "hardening" / "figures" / "67_dial_and_derived_mechanisms.png"


def all_rows(out):
    rows = [out["baseline"]] + out["c1_sigma"] + out["c2_no_first_order"]["rows"] + out["c3_heat_kernel"]["rows"] \
        + out["c4_traces"] + out["c5_gravity"]["rows"] + out["c6_thresholds"]["rows"] + out["c7_cutoff"] + out["outliers"]
    return rows


def figure(out) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 3, figsize=(17, 5.5))
    a = ax[0]
    for r in all_rows(out):
        if r["Mh"] < 60:
            continue
        c = "C2" if r["derived"] else "C3"
        a.errorbar(r["Mt"], r["Mh"], xerr=r["dMt"], yerr=r["dMh"], fmt="o", c=c, ms=4, alpha=0.7)
    a.errorbar([], [], fmt="o", c="C2", label="derived (no hand input)")
    a.errorbar([], [], fmt="o", c="C3", label="needs input / not spectral")
    a.add_patch(plt.Rectangle((172.5 - 1.4, 125.1 - 0.4), 2.8, 0.8, color="k"))
    a.text(173.5, 122, "data", fontsize=9)
    a.set_xlabel(r"$M_t$ [GeV]"); a.set_ylabel(r"$M_h$ [GeV]"); a.set_xlim(165, 205); a.set_ylim(115, 215)
    a.set_title("(a) all tested mechanisms (doc 60 pipeline)"); a.legend(fontsize=8, loc="upper left")
    b = ax[1]
    sc = out["c2_no_first_order"]["scan"]
    th_ = [s["theta"] for s in sc]
    b.plot(th_, [s["Mt"] for s in sc], "o-", label=r"$M_t$")
    b.plot(th_, [max(s["Mh"], -50) for s in sc], "s-", label=r"$M_h$ (floor -50: $\lambda<0$)")
    b.axhline(172.5, c="C0", ls=":"); b.axhline(125.1, c="C1", ls=":")
    b.set_xlabel(r"$(1,2,2)$-$(15,2,2)$ mixing angle $\theta$"); b.set_ylabel("GeV")
    b.set_title("(b) PS without first order: Higgs bidoublet mixing (1 free angle)"); b.legend(fontsize=8)
    c = ax[2]
    ds = np.linspace(-0.45, 0.05, 21)
    mts = [ts.predict(ts.Cand(r_yuk=math.sqrt(1 + d), r_quartic_power=2))["Mt"] for d in ds]
    c.plot(ds, mts, "-", c="k")
    c.axhline(172.5, ls=":", c="r"); c.axvline(out["c3_heat_kernel"]["needed_delta_yt2_over_g2"], ls=":", c="r")
    for r in out["c3_heat_kernel"]["rows"]:
        dlt = float(r["note"].split("=")[1])
        c.plot(dlt, r["Mt"], "o", label=r["name"].replace("a6 correction, f = ", "")[:38])
    c.set_xlabel(r"$\delta(y_t^2/g^2)$ at $\Lambda$ from $a_6$ ($c_6\approx-0.03$ estimate)")
    c.set_ylabel(r"$M_t$ [GeV]"); c.set_title("(c) higher heat-kernel terms vs the needed -36%")
    c.legend(fontsize=7, loc="lower right")
    fig.tight_layout(); fig.savefig(FIG, dpi=120)
    FIG_DOC.parent.mkdir(parents=True, exist_ok=True); shutil.copy(FIG, FIG_DOC); plt.close(fig)
    return FIG


def main() -> Path:
    out = dm.report()
    path = HERE / "results_doc67.json"
    path.write_text(json.dumps(out, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o)))
    figure(out)
    return path


if __name__ == "__main__":
    print(main())
