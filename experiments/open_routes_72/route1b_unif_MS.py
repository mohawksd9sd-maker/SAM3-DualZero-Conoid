"""Doc 72 route 1b: M_S from exact triple unification (alpha1 = alpha2 = alpha3 with the spectral traces).
Mismatch recomputed independently: m3 = a3/a2 - 1 at the a1 = a2 point (doc 70 definition).
Then: (i) X_t = 0 prediction; (ii) X_t fitted to M_h = 125.1 *with M_S re-derived at each X_t*
(1 fitted number for 1 observable, M_t a prediction); (iii) sensitivities (alpha_s, gluino ratio)."""
import math
from multiprocessing import Pool
import numpy as np
from scipy.optimize import brentq
from common import *
import susy_thresholds as st

def at(M_S, xt=0.0, sgn=1.0, r3=1.0, alpha_s=0.1180):
    r = st.solve_thr(M_S, st.Spectrum(xt=xt, sgn_mu=sgn, r3=r3), alpha_s=alpha_s)
    return r

def ms_unif(xt=0.0, sgn=1.0, r3=1.0, alpha_s=0.1180, lo=4e2, hi=6e4):
    f = lambda lm: (lambda r: r["unif_mismatch"] if r.get("ok") else float("nan"))(at(math.exp(lm), xt, sgn, r3, alpha_s))
    xs = np.linspace(math.log(lo), math.log(hi), 9)
    vs = [f(x) for x in xs]
    for a, b, va, vb in zip(xs[:-1], xs[1:], vs[:-1], vs[1:]):
        if np.isfinite(va) and np.isfinite(vb) and va * vb < 0:
            lm = brentq(f, a, b, xtol=1e-3)
            r = at(math.exp(lm), xt, sgn, r3, alpha_s)
            r["pull_Mt"], r["pull_Mh"] = pulls(r["Mt"], r["Mh"])
            return r
    return {"ok": False, "xt": xt, "sgn": sgn, "r3": r3, "alpha_s": alpha_s, "vals": vs}

def job(a):
    kind, kw = a
    r = ms_unif(**kw)
    r["kind"], r["kw"] = kind, kw
    return clean(r)

if __name__ == "__main__":
    jobs = [("xt_scan", dict(xt=x, sgn=s)) for s in (1.0, -1.0) for x in (-2.449, -2.2, -2.0, -1.5, -1.0, 0.0, 1.0, 2.0, 2.449)]
    jobs += [("alpha_s", dict(alpha_s=a)) for a in (0.1171, 0.1189)]
    jobs += [("r3", dict(r3=r, lo=1e2, hi=3e5)) for r in (0.3, 3.0)]
    jobs += [("alpha_s_xt-2", dict(xt=-2.0, alpha_s=a)) for a in (0.1171, 0.1189)]
    with Pool(8) as p:
        out = p.map(job, jobs)
    for o in out:
        if o.get("ok"):
            print(o["kind"], o["kw"], f"M_S={o['M_S']:.4g}", "Mt=%.2f Mh=%.2f tanb=%.1f mis=%.1e pulls %.2f %.2f" %
                  (o["Mt"], o["Mh"], o["tanb"], o["unif_mismatch"], o["pull_Mt"], o["pull_Mh"]))
        else:
            print(o["kind"], o["kw"], "no root", o.get("vals"))
    save("results_route1b.json", out)
