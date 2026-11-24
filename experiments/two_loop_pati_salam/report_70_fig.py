"""Figure for doc 70."""
import json
import shutil

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from report_70 import OUT, FIG, FIG_DOC


def figure():
    d = json.load(open(OUT))
    fig, ax = plt.subplots(1, 4, figsize=(22, 5.4))
    a = ax[0]
    labs, vals = [], []
    for b in d["breakdown"]:
        r = [x for x in b["rows"] if x.get("ok") and x["M_S"] == 4e4]
        if r:
            labs.append(b["label"].replace(" (", "\n("))
            vals.append(r[0]["Mt"])
    a.barh(range(len(vals)), vals, color=["gray"] + ["tab:blue"] * (len(vals) - 2) + ["tab:orange"])
    a.axvspan(172.5 - 1.218, 172.5 + 1.218, color="gold", alpha=0.5)
    a.axvline(172.5, color="goldenrod")
    for i, v in enumerate(vals):
        a.text(v + 0.05, i, f"{v:.2f}", va="center", fontsize=8)
    a.set_yticks(range(len(vals))); a.set_yticklabels(labs, fontsize=7); a.invert_yaxis()
    a.set_xlim(167, 174); a.set_xlabel("$M_t$ (GeV) at $M_S$ = 40 TeV, degenerate, $X_t$=0")
    a.set_title("(a) candidate #10: what each threshold does")
    b = ax[1]
    sty = {0.3: ":", 1.0: "-", 3.0: "--"}
    for s, col in ((1.0, "tab:blue"), (-1.0, "tab:red")):
        for r3 in (0.3, 1.0, 3.0):
            pts = [(x["xt"], x["cross"]["Mt"]) for x in d["scan"] if x["sgn_mu"] == s and x["r3"] == r3 and x["cross"]]
            if pts:
                pts.sort()
                b.plot(*zip(*pts), sty[r3], color=col, marker="o", ms=3,
                       label=f"sign $\\mu$ = {'+' if s > 0 else '-'}, $M_3/M_S$ = {r3}")
    b.axhspan(172.5 - 1.218, 172.5 + 1.218, color="gold", alpha=0.5)
    b.set_xlabel("$X_t/M_S$ (input)"); b.set_ylabel("$M_t$ (GeV) where $M_h$ = 125.1")
    b.set_title("(b) top mass once $M_S$ is fixed by $M_h$"); b.legend(fontsize=6)
    c = ax[2]
    for s, col in ((1.0, "tab:blue"), (-1.0, "tab:red")):
        for r3 in (0.3, 1.0, 3.0):
            pts = [(x["xt"], x["cross"]["M_S"]) for x in d["scan"] if x["sgn_mu"] == s and x["r3"] == r3 and x["cross"]]
            if pts:
                pts.sort()
                c.semilogy(*zip(*pts), sty[r3], color=col, marker="o", ms=3)
    c.set_xlabel("$X_t/M_S$"); c.set_ylabel("$M_S$ (GeV) giving $M_h$ = 125.1")
    c.set_title("(c) the fitted SUSY scale")
    e = ax[3]
    for M, col in ((2e3, "k"), (1e4, "tab:green"), (2e4, "tab:purple")):
        pts = sorted((v["xt"], v["Mh"]) for v in d["validate"] if v["M_S"] == M)
        e.plot(*zip(*pts), "-o", color=col, label=f"$M_S$ = {M/1e3:.0f} TeV")
    e.axhline(125.1, color="gold", lw=3, alpha=0.7)
    e.set_xlabel("$X_t/M_S$"); e.set_ylabel("$M_h$ (GeV)")
    e.set_title("(d) EFT check: MSSM, tan$\\beta$=20, $M_t$=173.34\n(compare Vega-Villadoro 2015 fig. 3)")
    e.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(FIG, dpi=120)
    shutil.copy(FIG, FIG_DOC)
    print("figure", FIG_DOC)
