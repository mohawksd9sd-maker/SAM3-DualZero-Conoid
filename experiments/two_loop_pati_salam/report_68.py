"""Doc 68 report: matter-content search (route 1).  Writes results_doc68.json and the figure."""

from __future__ import annotations

import json
import math
import os
import sys
import time

import numpy as np

import content_engine as ce
import matter_search as ms

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results_doc68.json")
FIG = os.path.join(HERE, "fig_doc68_matter_search.png")
FIG_DOC = os.path.join(HERE, "..", "..", "docs", "hardening", "figures", "68_matter_content_search.png")


def _clean(x):
    if isinstance(x, dict):
        return {k: _clean(v) for k, v in x.items() if k not in ("pw", "sm")}
    if isinstance(x, (list, tuple)):
        return [_clean(v) for v in x]
    if isinstance(x, (np.floating, np.integer)):
        return float(x)
    if isinstance(x, np.bool_):
        return bool(x)
    return x


def compute(sections=None):
    res = json.load(open(OUT)) if os.path.exists(OUT) else {}
    todo = sections or ["screen", "fine_screen", "catalogue", "sm_catalogue", "higgs_coupled", "requirement", "fourth",
                        "r_sector", "extra_rows"]
    for sec in todo:
        t = time.time()
        if sec == "screen":
            res[sec] = ms.screen(12)
        elif sec == "fine_screen":
            out = []
            for dR in range(0, 5):
                for dL in range(0, 5):
                    for d4 in range(0, 5):
                        r = ms.predict_trace_only([6 + dR, 6 + dL, 6 + d4])
                        rec = {"dI": [dR, dL, d4], "ok": r.get("ok", False)}
                        if r.get("ok"):
                            rec.update({k: float(r[k]) for k in ("Mt", "Mh", "Lambda", "m_R", "yt_over_g", "yt_over_g_needed")})
                            rec["unif_ok"] = bool(r["Lambda"] < ce.M_PL_RED and r["m_R"] < r["Lambda"])
                        out.append(rec)
            res[sec] = out
        elif sec == "catalogue":
            res[sec] = ms.catalogue()
        elif sec == "sm_catalogue":
            res[sec] = ms.sm_catalogue()
        elif sec == "higgs_coupled":
            res[sec] = ms.higgs_coupled_rows()
        elif sec == "requirement":
            res[sec] = ms.requirement_curve()
        elif sec == "r_sector":
            res[sec] = ms.r_sector_scan()
        elif sec == "extra_rows":
            res[sec] = ms.extra_rows()
        elif sec == "fourth":
            res[sec] = ms.fourth_generation()
        res[sec] = _clean(res[sec])
        res.setdefault("timing_s", {})[sec] = time.time() - t
        json.dump(res, open(OUT, "w"), indent=1, default=float)
        print(sec, "done", round(time.time() - t, 1), "s", flush=True)
    return res




def figure():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import shutil
    d = json.load(open(OUT))
    fig, ax = plt.subplots(1, 3, figsize=(17, 5.2))
    a = ax[0]
    groups = [("trace-only screen (0 params)", [x for x in d["screen"] + d["fine_screen"] if x.get("ok")], "lightgray", "o"),
              ("single entries, 0 params", [x for x in d["catalogue"] if x.get("ok")], "tab:blue", "s"),
              ("SU(2)_R-only direction, 0 params", [x for x in d["r_sector"] if x.get("ok")], "tab:green", "^"),
              ("SM algebra + VL (mass input)", [x for x in d["sm_catalogue"] if x.get("ok")], "tab:purple", "v"),
              ("Higgs-coupled, share fitted (1 param)", [x for x in d["higgs_coupled"] if x.get("ok") and x["params"] == 1], "tab:red", "D"),
              ("universal-Yukawa / formal rows", [x for x in d["extra_rows"] + [y for y in d["higgs_coupled"] if y.get("ok") and y["params"] == 0] if x.get("ok")], "tab:orange", "*")]
    for lab, xs, col, mk in groups:
        a.scatter([x["Mt"] for x in xs], [x["Mh"] for x in xs], c=col, marker=mk, s=40 if mk != "*" else 110, label=lab, alpha=0.85, edgecolor="k", lw=0.3)
    a.add_patch(plt.Rectangle((172.5 - 2 * 1.38, 125.1 - 2 * 1.77), 4 * 1.38, 4 * 1.77, color="gold", alpha=0.5, label="data (2$\\sigma$ incl. theory)"))
    a.set_xlim(150, 215); a.set_ylim(120, 240)
    a.set_xlabel("$M_t$ (GeV)"); a.set_ylabel("$M_h$ (GeV)")
    a.set_title("(a) every route-1 content: $M_t$ vs $M_h$")
    a.legend(fontsize=7, loc="upper left")
    b = ax[1]
    for key, col in (("(3,1,1)", "tab:green"), ("(2,1,1)", "tab:olive")):
        for mass, ls in (("Lambda", "-"), ("mR", "--")):
            xs = [x for x in d["r_sector"] if x.get("ok") and x["entry"].startswith(key) and x["mass"] == mass]
            dI = [x["I"][0] - 6 for x in xs]
            b.plot(dI, [x["Mt"] for x in xs], ls, color=col, marker="o", label=f"{key} at {mass}: $M_t$")
            b.plot(dI, [x["Mh"] - 0 for x in xs], ls, color=col, marker="x", alpha=0.5)
    b.axhline(172.5, color="gold", lw=3, alpha=0.7)
    b.axhline(125.1, color="gold", lw=3, alpha=0.7)
    b.set_xlabel("$\\Delta I_R$ (extra SU(2)$_R$ trace)"); b.set_ylabel("GeV  (o: $M_t$, x: $M_h$)")
    b.set_title("(b) best zero-parameter direction stops at $M_t\\approx185.5$\n($m_R$ pushed to 30 TeV, then no solution)")
    b.legend(fontsize=7)
    c = ax[2]
    req = d["requirement"]
    dn = np.array([x["dN"] for x in req]); da = np.array([x["da_needed"] for x in req])
    c.plot(dn, da, "k-o", label="needed $\\Delta a$ for $M_t=172.5$")
    c.plot(dn, 2.208 + 2.072 * dn, "k:", lw=1, label="$2.21+2.07\\,\\Delta N$")
    pts = [(2, 4, "1 VL 16-pair, 1 chain, y=y$_t$"), (2, 8, "1 pair, 2 chains, y=y$_t$"), (4, 8, "2 pairs, 1 chain"),
           (4, 16, "2 pairs, 2 chains"), (1, 4, "4th gen, up-type y=y$_t$"), (1, 8, "4th gen, all y=y$_t$")]
    for x, y, lab in pts:
        c.scatter([x], [y], marker="*", s=120, color="tab:orange", edgecolor="k")
        c.annotate(lab, (x, y), fontsize=7, xytext=(4, 2), textcoords="offset points")
    c.set_xlabel("$\\Delta N$ (added universal gauge trace, generation units)")
    c.set_ylabel("$\\Delta a$ (added Higgs-coupled Yukawa trace, $y_t^2$ units)")
    c.set_title("(c) inversion: what content would give $y_t/g\\approx0.80$")
    c.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(FIG, dpi=130)
    shutil.copy(FIG, FIG_DOC)
    print("figure", FIG_DOC)


if __name__ == "__main__":
    if "--figure" in sys.argv:
        figure()
    else:
        compute(sys.argv[1:] or None)
        figure()
