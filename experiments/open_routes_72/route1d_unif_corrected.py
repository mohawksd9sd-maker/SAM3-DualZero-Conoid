"""Doc 73: unification-derived M_S for candidate #10 with the corrected repo matching (Buttazzo v4, ref 173.34)
plus all doc-72 higher orders (X^5 fix, O(at^2), 2L SQCD, 3L SM + 3L MSSM RGEs).  Complements route1c (SMDR)."""
from multiprocessing import Pool
from common import *
from route1c_unif_full import ms_unif

def job(kw):
    r = ms_unif(lo=1.0e3, hi=1.2e4, **kw); r["kw"] = kw; return clean(r)

if __name__ == "__main__":
    jobs = [dict(xt=x, sgn=s, mode="doc60") for s in (1.0, -1.0) for x in (-2.449, -2.2, -2.0, -1.5, -1.0, 0.0)]
    jobs += [dict(xt=x, alpha_s=a, mode=m) for m in ("doc60", "smdr") for x in (0.0, -2.2) for a in (0.1171, 0.1189)]
    jobs += [dict(xt=x, M3=g, mode="doc60") for x in (0.0, -2.2) for g in (0.5, 2.0)]
    jobs += [dict(xt=x, mA=a, mode="doc60") for x in (0.0, -2.2) for a in (0.5, 2.0)]
    with Pool(8) as p:
        out = p.map(job, jobs)
    for o in out:
        print(o["kw"], ("M_S=%.4g Mt=%.2f Mh=%.2f tanb=%.1f pulls %+.2f %+.2f" % (o["M_S"], o["Mt"], o["Mh"], o["tanb"], o["pull_Mt"], o["pull_Mh"])) if o.get("ok") else ("no root", o.get("vals")))
    save("results_route1d.json", out)
