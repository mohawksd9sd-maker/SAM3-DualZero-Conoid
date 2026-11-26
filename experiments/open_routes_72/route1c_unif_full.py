"""Doc 72 route 1c: unification-derived M_S rerun with every route-3 correction on
(X^5 fix, O(at^2), 2L SQCD y_t, 3L SM + 3L MSSM RGEs, SMDR v1.3 matching)."""
import math, sys
from multiprocessing import Pool
import numpy as np
from scipy.optimize import brentq
from common import *
import thr72 as T

FULL = dict(sm3=True, mssm3=True)

def at(M_S, xt, sgn, alpha_s=0.1180, M3=1.0, mA=1.0, mode="smdr"):
    set_matching(mode)
    return T.solve72(M_S, T.Spec(xt=xt, mu=sgn, M3=M3, mA=mA), alpha_s=alpha_s, **FULL)

def ms_unif(xt=0.0, sgn=1.0, alpha_s=0.1180, M3=1.0, mA=1.0, mode="smdr", lo=3e2, hi=8e4):
    def f(lm):
        r = at(math.exp(lm), xt, sgn, alpha_s, M3, mA, mode)
        return r["unif_mismatch"] if r.get("ok") else float("nan")
    xs = np.linspace(math.log(lo), math.log(hi), 7)
    vs = [f(x) for x in xs]
    for a, b, va, vb in zip(xs[:-1], xs[1:], vs[:-1], vs[1:]):
        if np.isfinite(va) and np.isfinite(vb) and va * vb < 0:
            lm = brentq(f, a, b, xtol=2e-3)
            r = at(math.exp(lm), xt, sgn, alpha_s, M3, mA, mode)
            return r
    return {"ok": False, "vals": vs}

def job(kw):
    r = ms_unif(**kw)
    r["kw"] = kw
    return clean(r)

if __name__ == "__main__":
    jobs = [dict(xt=x, sgn=s) for s in (1.0, -1.0) for x in (-2.449, -2.2, -2.0, -1.5, 0.0, 2.0, 2.449)]
    jobs += [dict(xt=x, alpha_s=a) for x in (0.0, -2.0) for a in (0.1171, 0.1189)]
    jobs += [dict(xt=0.0, mode="v4ref"), dict(xt=-2.0, mode="v4ref")]
    with Pool(16) as p:
        out = p.map(job, jobs)
    for o in out:
        if o.get("ok"):
            print(o["kw"], f"M_S={o['M_S']:.4g}", "Mt=%.2f Mh=%.2f tanb=%.1f mis=%.1e pulls %+.2f %+.2f" %
                  (o["Mt"], o["Mh"], o["tanb"], o["unif_mismatch"], o["pull_Mt"], o["pull_Mh"]))
        else:
            print(o["kw"], "no root", o.get("vals"))
    save("results_route1c.json", out)
