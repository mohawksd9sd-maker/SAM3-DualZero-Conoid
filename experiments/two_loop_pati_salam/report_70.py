"""Doc 70: SUSY thresholds for doc-69 candidate #10.  Writes results_doc70.json and the figure."""
from __future__ import annotations

import json
import math
import os
import sys
import time
from dataclasses import replace
from multiprocessing import Pool

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results_doc70.json")
FIG = os.path.join(HERE, "fig_doc70_susy_thresholds.png")
FIG_DOC = os.path.join(HERE, "..", "..", "docs", "hardening", "figures", "70_susy_thresholds.png")

MS_GRID = (5e3, 1e4, 2e4, 4e4, 8e4, 1.6e5)
XT = (-2.449, -2.0, -1.0, 0.0, 1.0, 2.0, 2.449)
R3 = (0.3, 1.0, 3.0)


def _clean(x):
    if isinstance(x, dict):
        return {k: _clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_clean(v) for v in x]
    if isinstance(x, (np.floating, np.integer)):
        return float(x)
    return x


def _job(args):
    import susy_thresholds as st
    M_S, kw, extra = args
    r = st.solve_thr(M_S, st.Spectrum(**kw), **extra)
    r["kw"] = kw
    r["extra"] = extra
    return _clean(r)


def crossing(rows, target=125.1):
    """Interpolate in log M_S the point where M_h = target; return (M_S*, M_t*, tanb*, unif*)."""
    rows = sorted([r for r in rows if r.get("ok")], key=lambda r: r["M_S"])
    for a, b in zip(rows[:-1], rows[1:]):
        if (a["Mh"] - target) * (b["Mh"] - target) <= 0 and a["Mh"] != b["Mh"]:
            w = (target - a["Mh"]) / (b["Mh"] - a["Mh"])
            lm = math.log(a["M_S"]) + w * (math.log(b["M_S"]) - math.log(a["M_S"]))
            f = lambda k: a[k] + w * (b[k] - a[k])
            return {"M_S": math.exp(lm), "Mt": f("Mt"), "tanb": f("tanb"), "unif_mismatch": f("unif_mismatch"),
                    "Delta_b": f("Delta_b"), "dyt": f("dyt")}
    return None


def compute(sections=None):
    res = json.load(open(OUT)) if os.path.exists(OUT) else {}
    todo = sections or ["validate", "breakdown", "scan", "variants", "plain"]
    pool = Pool(8)
    for sec in todo:
        t = time.time()
        if sec == "validate":
            import susy_thresholds as st
            v = []
            for M in (2e3, 1e4, 2e4):
                for x in (-2.449, -2.0, 0.0, 2.0, 2.449):
                    v.append({"M_S": M, "xt": x, "tanb": 20.0, "Mt": 173.34, "Mh": st.mh_only(M, 173.34, 20.0, st.Spectrum(xt=x))})
            res[sec] = v
        elif sec == "breakdown":
            steps = [("doc 69 pipeline (no thresholds, 2-loop SM)", dict(yuk_thr=False, db_thr=False, lam_thr=False), dict(qcd3=False)),
                     ("+ 3-loop QCD in SM running", dict(yuk_thr=False, db_thr=False, lam_thr=False), {}),
                     ("+ y_t, y_b(non-enh), gauge thresholds", dict(db_thr=False, lam_thr=False), {}),
                     ("+ Delta_b, Delta_tau (mu > 0)", dict(lam_thr=False), {}),
                     ("+ Higgs quartic loops (full, mu > 0)", {}, {}),
                     ("full, mu < 0", dict(sgn_mu=-1.0), {})]
            jobs = [(M, kw, ex) for _, kw, ex in steps for M in (2e4, 4e4)]
            out = pool.map(_job, jobs)
            res[sec] = [{"label": lab, "rows": [o for o in out if o["kw"] == kw and o["extra"] == ex]} for lab, kw, ex in steps]
        elif sec == "scan":
            jobs = [(M, dict(xt=x, r3=r, sgn_mu=s), {}) for s in (1.0, -1.0) for r in R3 for x in XT for M in MS_GRID]
            out = pool.map(_job, jobs)
            spectra = []
            for s in (1.0, -1.0):
                for r in R3:
                    for x in XT:
                        rows = [o for o in out if o["kw"] == dict(xt=x, r3=r, sgn_mu=s)]
                        spectra.append({"sgn_mu": s, "r3": r, "xt": x, "rows": rows, "cross": crossing(rows)})
            res[sec] = spectra
        elif sec == "scan_low":
            # extend the scan to M_S = 2, 3 TeV (crossings below 5 TeV at large negative X_t)
            jobs = [(M, dict(xt=x, r3=r, sgn_mu=s), {}) for s in (1.0, -1.0) for r in R3 for x in XT for M in (2e3, 3e3)]
            out = pool.map(_job, jobs)
            for sp in res["scan"]:
                kw = dict(xt=sp["xt"], r3=sp["r3"], sgn_mu=sp["sgn_mu"])
                sp["rows"] = sorted([o for o in out if o["kw"] == kw] + [r for r in sp["rows"] if r["M_S"] >= 5e3],
                                    key=lambda r: r["M_S"])
                sp["cross"] = crossing(sp["rows"])
            res[sec] = {"added_M_S": [2e3, 3e3]}
        elif sec == "variants":
            base = dict(xt=0.0, r3=1.0, sgn_mu=1.0)
            var = [("baseline", base, {}), ("no 2-loop lambda", {**base, "two_loop_lam": False}, {}),
                   ("Delta_tau x0", {**base, "tau_scale": 0.0}, {}), ("Delta_tau x2", {**base, "tau_scale": 2.0}, {}),
                   ("no sbottom/stau in lambda", {**base, "sbottom_stau_lam": False}, {}),
                   ("alpha_s 0.1170", base, {"alpha_s": 0.1170}), ("alpha_s 0.1190", base, {"alpha_s": 0.1190}),
                   ("unification via alpha2=alpha3", base, {"which": "23"})]
            jobs = [(M, kw, ex) for _, kw, ex in var for M in (2e4, 4e4)]
            out = pool.map(_job, jobs)
            res[sec] = [{"label": lab, "rows": [o for o in out if o["kw"] == kw and o["extra"] == ex], } for lab, kw, ex in var]
            for v in res[sec]:
                v["cross"] = crossing(v["rows"])
        elif sec == "plain":
            jobs = [(M, dict(sgn_mu=s), dict(dI=0.0, da_u=0.0, n=nn)) for nn in (1.0, 0.0) for s in (1.0, -1.0) for M in (3e3, 1e4)]
            res[sec] = pool.map(_job, jobs)
        res[sec] = _clean(res[sec])
        res.setdefault("timing_s", {})[sec] = time.time() - t
        json.dump(res, open(OUT, "w"), indent=1, default=float)
        print(sec, "done", round(time.time() - t, 1), flush=True)
    pool.close()
    return res


if __name__ == "__main__":
    if "--figure" in sys.argv:
        from report_70_fig import figure
        figure()
    else:
        compute(sys.argv[1:] or None)
