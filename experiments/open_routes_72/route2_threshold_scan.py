"""Doc 72 route 2: full SUSY threshold scan for candidate #10 (doc 70 boundary, n=1, dI=4, da_u=8).
For each spectrum shape (in units of M_S) M_S is fitted to M_h = 125.1 (1 fitted number), and M_t is read off.
All route-3 corrections on, SMDR v1.3 matching.  Each shape parameter that departs from 1 (or X_t from 0)
is one more chosen input."""
import math, itertools
from multiprocessing import Pool
import numpy as np
from scipy.optimize import brentq
from common import *
import thr72 as T

def solve(M_S, kw):
    set_matching("smdr")
    return T.solve72(M_S, T.Spec(**kw), sm3=True, mssm3=True)

def fit_MS(kw, target=125.1, lo=8e2, hi=3e6):
    def f(lm):
        r = solve(math.exp(lm), kw)
        return r["Mh"] - target if r.get("ok") else float("nan")
    xs = np.linspace(math.log(lo), math.log(hi), 8)
    vs = [f(x) for x in xs]
    roots = []
    for a, b, va, vb in zip(xs[:-1], xs[1:], vs[:-1], vs[1:]):
        if np.isfinite(va) and np.isfinite(vb) and va * vb < 0:
            lm = brentq(f, a, b, xtol=3e-3)
            roots.append(solve(math.exp(lm), kw))
    if not roots:
        return {"ok": False, "vals": vs}
    return max(roots, key=lambda r: r["Mt"])  # report the root with the larger M_t

def job(kw):
    r = fit_MS(kw)
    r["kw"] = kw
    r["n_extra"] = sum(1 for k, v in kw.items() if (k == "xt" and v != 0) or (k in ("mU", "mQ", "M3", "mA", "M1", "M2") and v != 1.0) or (k == "mu" and abs(v) != 1.0)) + (1 if kw.get("mu", 1) < 0 else 0)
    return clean(r)

if __name__ == "__main__":
    shapes = [dict()]
    shapes += [dict(xt=x) for x in (-2.449, -2.0, -1.0, 1.0, 2.0, 2.449)]
    shapes += [dict(mu=m) for m in (-1.0, 0.3, 3.0, -3.0, -0.3)]
    shapes += [dict(M3=m) for m in (0.3, 3.0)]
    shapes += [dict(mU=0.5), dict(mU=2.0), dict(mQ=0.5), dict(mQ=2.0)]
    shapes += [dict(mA=0.3), dict(mA=3.0)]
    shapes += [dict(M3=3.0, mu=-1.0), dict(M3=3.0, mu=3.0), dict(M3=0.3, mu=3.0), dict(M3=3.0, xt=2.0), dict(M3=3.0, xt=-2.0),
               dict(mu=3.0, xt=2.0), dict(mu=-3.0, M3=3.0, xt=2.0), dict(mU=0.5, xt=2.0, M3=3.0)]
    with Pool(8) as p:
        out = p.map(job, shapes)
    for o in out:
        if o.get("ok"):
            print(o["kw"], f"+{o['n_extra']}", f"M_S={o['M_S']:.4g}", "Mt=%.2f Mh=%.2f tanb=%.1f mis=%+.3f pullMt %+.2f" %
                  (o["Mt"], o["Mh"], o["tanb"], o["unif_mismatch"], o["pull_Mt"]))
        else:
            print(o["kw"], "no root", o.get("vals"))
    save("results_route2.json", out)
