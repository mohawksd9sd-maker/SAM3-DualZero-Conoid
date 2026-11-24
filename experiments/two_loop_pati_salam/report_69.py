"""Doc 69 report: routes 2 (multi-stage), 3 (SUSY spectral), 4 (top-first), combinations."""

from __future__ import annotations

import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results_doc69.json")


def _clean(x):
    if isinstance(x, dict):
        return {k: _clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_clean(v) for v in x]
    if isinstance(x, (np.floating, np.integer)):
        return float(x)
    if isinstance(x, np.bool_):
        return bool(x)
    return x


def compute(sections=None):
    import multistage as msg
    import susy_spectral as ss
    res = json.load(open(OUT)) if os.path.exists(OUT) else {}
    todo = sections or ["multistage", "radiative", "susy_scan", "susy_variants", "susy_needed"]
    for sec in todo:
        t = time.time()
        if sec == "multistage":
            res[sec] = [msg.predict(r) for r in (0.001, 0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0)]
        elif sec == "radiative":
            res[sec] = msg.radiative_check()
        elif sec == "susy_scan":
            out = []
            for n in (0.0, 1.0):
                for MS in (1e3, 3e3, 1e4, 1e5, 1e6, 1e8, 1e10, 1e12, 1e14):
                    out.append(ss.solve(MS, n=n))
            res[sec] = out
        elif sec == "susy_variants":
            out = []
            for MS in (1e3, 1e4):
                for db in (-0.3, 0.3):
                    out.append(ss.solve(MS, Delta_b=db))
                out.append(ss.solve(MS, which="23"))
                for tr in ("S1 BvdBvS: + gauginos + 1 higgsino copy", "S2 BvdBvS Remark 2: + 2 higgsino copies"):
                    for w in ("23", "12"):
                        out.append(ss.solve(MS, trace=tr, which=w))
                for a_s in (0.1170, 0.1190):
                    out.append({**ss.solve(MS, alpha_s=a_s), "alpha_s": a_s})
            res[sec] = out
        elif sec == "combo":
            uni = [{**ss.solve(MS, n=1.0, dI=4.0, da_u=8.0), "label": "universal y=y_t, 1 VL pair, 2 chains"}
                   for MS in (1e3, 3e3, 1e4, 3e4, 1e5, 1e6, 1e7, 1e8)]
            fit = [ss.combo_fit(MS) for MS in (1e3, 1e4, 1e5)]
            res[sec] = {"universal": uni, "fit": fit}
        elif sec == "combo_fit":
            res.setdefault("combo", {})["fit"] = _clean([ss.combo_fit(MS) for MS in (1e3, 1e4, 1e5)])
            res["timing_s"][sec] = time.time() - t
            json.dump(res, open(OUT, "w"), indent=1, default=float)
            print(sec, "done", flush=True)
            continue
        elif sec == "susy_needed":
            out = []
            for MS in (1e3, 1e4, 1e6):
                for tb in (5.0, 10.0, 30.0, 50.0):
                    out.append({"M_S": MS, "tanb": tb, "yt_over_g_needed": ss.needed_yt_over_g(MS, tb)})
            res[sec] = out
        res[sec] = _clean(res[sec])
        res.setdefault("timing_s", {})[sec] = time.time() - t
        json.dump(res, open(OUT, "w"), indent=1, default=float)
        print(sec, "done", round(time.time() - t, 1), flush=True)
    return res




FIG = os.path.join(HERE, "fig_doc69_multistage_susy.png")
FIG_DOC = os.path.join(HERE, "..", "..", "docs", "hardening", "figures", "69_multistage_susy_topfirst.png")


def figure():
    import shutil
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    d = json.load(open(OUT))
    fig, ax = plt.subplots(1, 4, figsize=(21, 5.2))
    a = ax[0]
    ms_ = [x for x in d["multistage"] if x.get("ok")]
    a.plot([x["r"] for x in ms_], [x["Mt"] for x in ms_], "b-o", label="$M_t$")
    a.plot([x["r"] for x in ms_], [x["Mh"] for x in ms_], "r-s", label="$M_h$")
    a.axhline(172.5, color="gold", lw=3, alpha=0.7); a.axhline(125.1, color="gold", lw=3, alpha=0.7)
    a.set_xlabel("$\\log_{10}(M_C/m_R)$  (input)"); a.set_ylabel("GeV")
    a.set_title("(a) PS $\\to$ LR $\\to$ SM: flat at 191 GeV")
    a.set_ylim(115, 200); a.legend(fontsize=8)
    b = ax[1]
    for n, col in ((0.0, "tab:blue"), (1.0, "tab:green")):
        xs = [x for x in d["susy_scan"] if x.get("ok") and x["n"] == n]
        b.semilogx([x["M_S"] for x in xs], [x["Mt"] for x in xs], "-o", color=col, label=f"SUSY, CCM traces, n={int(n)} (y$_t$/g={1.155 if n == 0 else 1.0})")
    u = [x for x in d["combo"]["universal"] if x.get("ok")]
    b.semilogx([x["M_S"] for x in u], [x["Mt"] for x in u], "-D", color="tab:red", label="SUSY + 1 VL pair, universal y=y$_t$ (y$_t$/g=0.745)")
    fz = [x for x in d["combo"].get("fit", []) if x.get("ok")]
    if fz:
        b.semilogx([x["M_S"] for x in fz], [x["Mt"] for x in fz], "k*", ms=12, label="SUSY + VL pair, share fitted (2 params)")
        c_fit = fz
    b.axhline(172.5, color="gold", lw=3, alpha=0.7)
    b.set_xlabel("$M_S$ (GeV)"); b.set_ylabel("$M_t$ (GeV)")
    b.set_title("(b) SUSY spectral boundary: $M_t$ vs $M_S$\n(tan$\\beta\\approx$55-66 fixed by $m_b$)")
    b.legend(fontsize=7)
    c = ax[2]
    for n, col in ((0.0, "tab:blue"), (1.0, "tab:green")):
        xs = [x for x in d["susy_scan"] if x.get("ok") and x["n"] == n]
        c.fill_between([x["M_S"] for x in xs], [x["Mh"] for x in xs], [x["Mh_maxmix"] for x in xs], color=col, alpha=0.3,
                       label=f"n={int(n)}: $X_t$=0 ... $\\sqrt{{6}} M_S$")
    c.fill_between([x["M_S"] for x in u], [x["Mh"] for x in u], [x["Mh_maxmix"] for x in u], color="tab:red", alpha=0.3,
                   label="SUSY + VL pair (universal)")
    if fz:
        c.vlines([x["M_S"] for x in fz], [x["Mh"] for x in fz], [x["Mh_maxmix"] for x in fz], color="k", lw=3, label="fitted share ($M_t$=172.5)")
    c.set_xscale("log"); c.axhline(125.1, color="gold", lw=3, alpha=0.7)
    c.set_xlabel("$M_S$ (GeV)"); c.set_ylabel("$M_h$ (GeV) at the predicted $M_t$")
    c.set_title("(c) SUSY Higgs (EFT, stop mixing band)"); c.legend(fontsize=7)
    e = ax[3]
    labels = ["PS non-SUSY\n(doc 60)", "SUSY tan$\\beta$=50\n$M_S$=1 TeV", "SUSY tan$\\beta$=10\n$M_S$=1 TeV"]
    need = [0.803] + [next(x["yt_over_g_needed"] for x in d["susy_needed"] if x["M_S"] == 1e3 and x["tanb"] == tb) for tb in (50.0, 10.0)]
    e.bar(np.arange(3) - 0.2, need, 0.4, color="gold", label="needed for $M_t$=172.5")
    e.bar(np.arange(3) + 0.2, [1.0, 1.0, 1.0], 0.4, color="tab:gray", label="spectral, 3 generations, $y_\\nu=y_t$")
    e.scatter([1.2, 2.2], [1.155, 1.155], marker="_", s=600, color="k", label="spectral, no $\\nu$ Yukawa")
    e.scatter([0.2, 1.2], [0.745, 0.745], marker="*", s=150, color="tab:red", label="+1 VL pair, universal y")
    e.set_xticks(range(3)); e.set_xticklabels(labels, fontsize=8)
    e.set_ylabel("$y_t/g$ at the spectral boundary"); e.set_ylim(0.5, 1.25)
    e.set_title("(d) top-first: the required ratio"); e.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(FIG, dpi=125)
    shutil.copy(FIG, FIG_DOC)
    print("figure", FIG_DOC)


if __name__ == "__main__":
    if "--figure" in sys.argv:
        figure()
    else:
        compute(sys.argv[1:] or None)
