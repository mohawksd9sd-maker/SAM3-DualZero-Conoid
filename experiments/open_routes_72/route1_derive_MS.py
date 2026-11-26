"""Doc 72 route 1: can M_S be *derived* (not fitted to M_h)?

Candidates tested (each is a principle that fixes M_S without using M_h or M_t):
 (a) exact triple gauge unification at the spectral scale (the spectral action demands
     g1 = g2 = g3 with its own traces; with MSSM running below Lambda the only free scale left
     that moves alpha_3 relative to alpha_1,2 is M_S)  -> solve unif_mismatch(M_S) = 0;
     done for both read-offs ("12": Lambda from a1=a2, mismatch in a3; "23": Lambda from a2=a3).
 (b) no hierarchy: soft masses from the f_2 Lambda^2 moment of the spectral action, M_S ~ Lambda.
 (c) the Higgs-mass-fitted value (doc 70), for reference only (FITTED).
Spectrum held at doc 70 'no-extra-number' choice: degenerate, X_t = 0, M3 = M_S, |mu| = M_S."""
import math, sys
from multiprocessing import Pool
import numpy as np
from common import *
import susy_thresholds as st

def job(a):
    M_S, sgn, which = a
    try:
        r = st.solve_thr(M_S, st.Spectrum(sgn_mu=sgn), which=which)
    except Exception as e:
        r = {"ok": False, "err": str(e)}
    r.update({"M_S": M_S, "sgn": sgn, "which": which})
    return clean(r)

def root(rows, key, target=0.0):
    rows = [r for r in rows if r.get("ok")]
    rows.sort(key=lambda r: r["M_S"])
    out = []
    for a, b in zip(rows[:-1], rows[1:]):
        fa, fb = a[key] - target, b[key] - target
        if fa * fb <= 0 and fa != fb:
            w = fa / (fa - fb)
            lm = math.log(a["M_S"]) + w * (math.log(b["M_S"]) - math.log(a["M_S"]))
            out.append({"M_S": math.exp(lm), **{k: a[k] + w * (b[k] - a[k]) for k in
                        ("Mt", "Mh", "tanb", "unif_mismatch", "Lambda", "Delta_b")}})
    return out

if __name__ == "__main__":
    grid = list(np.geomspace(2.5e2, 1e14, 30))
    jobs = [(M, s, w) for s in (1.0, -1.0) for w in ("12", "23") for M in grid]
    with Pool(8) as p:
        rows = p.map(job, jobs)
    res = {"grid": rows, "unif_roots": {}, "MS_eq_Lambda": {}, "mh_fit": {}}
    for s in (1.0, -1.0):
        for w in ("12", "23"):
            sub = [r for r in rows if r["sgn"] == s and r["which"] == w]
            key = f"mu{'+' if s > 0 else '-'}_{w}"
            rr = root(sub, "unif_mismatch")
            for x in rr:
                x["pull_Mt"], x["pull_Mh"] = pulls(x["Mt"], x["Mh"])
            res["unif_roots"][key] = rr
            res["mh_fit"][key] = root(sub, "Mh", 125.1)
            ok = [r for r in sub if r.get("ok")]
            res["MS_eq_Lambda"][key] = {"largest_ok_M_S": max([r["M_S"] for r in ok]) if ok else None,
                                         "row": max(ok, key=lambda r: r["M_S"]) if ok else None}
    print(save("results_route1.json", res))
    for k, v in res["unif_roots"].items():
        print(k, "unif roots:", [(f"{x['M_S']:.3g}", round(x['Mt'], 2), round(x['Mh'], 2), round(x['tanb'], 1)) for x in v])
        print(k, "Mh fit:", [(f"{x['M_S']:.3g}", round(x['Mt'], 2)) for x in res['mh_fit'][k]])
        r = res["MS_eq_Lambda"][k]["row"]
        if r: print(k, "largest M_S ok", f"{r['M_S']:.3g}", "Lambda", f"{r['Lambda']:.3g}", round(r['Mt'], 2), round(r['Mh'], 2))
