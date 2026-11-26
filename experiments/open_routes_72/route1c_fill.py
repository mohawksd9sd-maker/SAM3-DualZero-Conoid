"""Fill the route-1c points whose coarse bracket hit the low-M_S overflow region (finer bracket 1.0-4.0 TeV)."""
from multiprocessing import Pool
from common import *
from route1c_unif_full import ms_unif

def job(kw):
    r = ms_unif(lo=1.0e3, hi=4.0e3, **kw); r["kw"] = kw; return clean(r)

if __name__ == "__main__":
    jobs = [dict(xt=-2.0, sgn=1.0), dict(xt=-1.5, sgn=-1.0), dict(xt=2.0, sgn=-1.0), dict(xt=2.0, sgn=1.0), dict(xt=-2.0, alpha_s=0.1189)]
    with Pool(5) as p:
        out = p.map(job, jobs)
    for o in out:
        print(o["kw"], ("M_S=%.4g Mt=%.2f Mh=%.2f tanb=%.1f pulls %+.2f %+.2f" % (o["M_S"], o["Mt"], o["Mh"], o["tanb"], o["pull_Mt"], o["pull_Mh"])) if o.get("ok") else ("no root", o.get("vals")))
    save("results_route1c_fill.json", out)
