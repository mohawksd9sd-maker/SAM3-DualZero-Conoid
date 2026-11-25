"""Figure for doc 71."""
import json
import math
import shutil

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import time_medium as tm
from report_71 import OUT, FIG, FIG_DOC


def figure():
    d = json.load(open(OUT))
    fig, ax = plt.subplots(2, 3, figsize=(19, 10))
    a = ax[0, 0]
    for kind, col, lab in (("lin", "tab:blue", "mirror at a past time (linear osc.)"),
                           ("log", "tab:red", "mirror at a fixed energy (log osc.)")):
        c = d["cmb"][kind]
        a.plot(c["omega"], c["dchi2"], color=col, lw=0.8, label=f"{lab}: best $\\Delta\\chi^2$={c['best_dchi2']:.1f}")
        a.axhline(c["sims_max_dchi2_95"], color=col, ls="--", lw=1)
    a.set_xscale("log"); a.set_xlabel("$\\omega$ (Planck 2018 X convention)"); a.set_ylabel("$\\Delta\\chi^2$ improvement")
    a.set_title("(a) Echo features in Planck TT: improvement vs frequency\n(dashed: 95% of best-of-scan in no-echo simulations)")
    a.legend(fontsize=8)
    b = ax[0, 1]
    for kind, col in (("lin", "tab:blue"), ("log", "tab:red")):
        c = d["cmb"][kind]
        b.bar(kind, c["p_global"], color=col)
        b.text(kind, c["p_global"] + 0.02, f"p = {c['p_global']:.2f}", ha="center")
    b.axhline(0.05, color="k", ls=":"); b.set_ylim(0, 1.05); b.set_ylabel("global p-value (look-elsewhere)")
    b.set_title("(b) Is the best echo fit better than chance?")
    c = ax[0, 2]
    r = d["rings"]
    keys = ["n_low", "n_family3", "z_min"]
    for i, k in enumerate(keys):
        s = r["sims"]["LCDM"][k]
        c.errorbar(i, s["sims_mean"], yerr=2 * s["sims_std"], fmt="o", color="gray", capsize=6,
                   label="Gaussian sims (mean $\\pm2\\sigma$)" if i == 0 else None)
        c.plot(i, r["data"][k], "r*", ms=14, label="WMAP 9-yr ILC" if i == 0 else None)
    c.set_xticks(range(3)); c.set_xticklabels(["# low-variance rings", "# centres with $\\geq$3", "min ring z"])
    c.set_yscale("symlog"); c.legend(fontsize=8)
    c.set_title("(c) CCC-style concentric low-variance rings")
    e = ax[1, 0]
    M = np.geomspace(5, 300, 60)
    for a_ in (0.0, 0.7, 0.9):
        e.loglog(M, [tm.echo_delay(m, a_) for m in M], label=f"spin a = {a_}")
    for x in d["echoes"]:
        if x["ADA_2016_s"]:
            e.plot(x["M_det"], x["ADA_2016_s"], "k^")
    e.set_xlabel("remnant mass (detector frame, $M_\\odot$)"); e.set_ylabel("echo spacing $\\Delta t$ (s)")
    e.set_title("(d) Planck-length 'bank' near a horizon: echo spacing\n(triangles: Abedi et al. 2017 values)")
    e.legend(fontsize=8)
    f = ax[1, 1]
    disp = d["dispersion"]
    labs = ["GW170817\n|c_g-c|/c", "Fermi GRB090510\n|n-1| @31 GeV", "LHAASO GRB221009A\n|n-1| @10 TeV", "GWTC-3 m_g\n|v-c|/c @100 Hz"]
    vals = [3e-15, disp["GRB090510_linear"]["dn_at_31GeV"], disp["GRB221009A_linear"]["dn_at_10TeV"],
            disp["graviton_mass_100Hz"]["dv_over_c"]]
    f.bar(range(4), vals, color="tab:purple"); f.set_yscale("log")
    f.set_xticks(range(4)); f.set_xticklabels(labs, fontsize=7)
    f.set_ylabel("upper bound on a speed difference"); f.set_title("(e) Time as a dispersive medium: bounds")
    g = ax[1, 2]
    al = d["alpha"]
    for i, x in enumerate(al):
        g.errorbar(i, x["eps"], yerr=2 * x["err"], fmt="o", capsize=6)
    g.set_yscale("symlog", linthresh=1e-9); g.axhline(0, color="k", lw=0.5)
    g.set_xticks(range(len(al))); g.set_xticklabels([x["probe"].replace(" (", "\n(") for x in al], fontsize=7)
    g.set_ylabel("$\\epsilon$ in $\\Delta\\alpha/\\alpha = \\epsilon\\,\\ln(1+z)$ (2$\\sigma$)")
    g.set_title("(f) Epoch-dependent 'refractive index' of time (via $\\alpha$)")
    fig.tight_layout()
    fig.savefig(FIG, dpi=110)
    shutil.copy(FIG, FIG_DOC)
    print("figure", FIG_DOC)
