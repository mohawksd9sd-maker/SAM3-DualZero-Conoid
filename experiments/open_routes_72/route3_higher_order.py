"""Doc 72 route 3: higher orders with no new dials, applied to candidate #10 (and the route-1 point).
Cumulative steps; each row is a full re-solve of the spectral boundary (M_t, tan beta), then M_h."""
import math, sys
from multiprocessing import Pool
from common import *
import susy_thresholds as st
import thr72 as T

STEPS = [
    ("0 pre-erratum doc 70 (X^5/4 bug, 173.10 ref)", "t72", dict(fix_x5=False, at2=False, sqcd2=False), dict(_m="prefix")),
    ("1 + X_t^5 coefficient fix (BGSS/FS)", "t72", dict(at2=False, sqcd2=False), dict(_m="prefix")),
    ("2 + matching ref fix 173.34 (= corrected doc 70)", "t72", dict(at2=False, sqcd2=False), dict()),
    ("2' corrected doc 70 repo code (check)", "doc70", {}, {}),
    ("3 + O(alpha_t^2) 2-loop lambda", "t72", dict(sqcd2=False), dict()),
    ("4 + 2-loop SQCD y_t matching", "t72", dict(), dict()),
    ("5 + 3-loop SM RGEs below M_S", "t72", dict(), dict(sm3=True)),
    ("6 + 3-loop MSSM RGEs above M_S", "t72", dict(), dict(sm3=True, mssm3=True)),
    ("7 alt.: SMDR v1.3 matching instead of Buttazzo v4", "t72", dict(), dict(sm3=True, mssm3=True, _m="smdr")),
]

def job(a):
    label, kind, spk, kw, M_S, xt, sgn = a
    kw = dict(kw)
    set_matching(kw.pop("_m", "doc60"))
    if kind == "doc70":
        set_matching("doc60")
        r = st.solve_thr(M_S, st.Spectrum(xt=xt, sgn_mu=sgn))
        r["pull_Mt"], r["pull_Mh"] = pulls(r["Mt"], r["Mh"])
    else:
        r = T.solve72(M_S, T.Spec(xt=xt, mu=sgn, **spk), **kw)
    r.update(label=label, bench=(M_S, xt, sgn))
    return clean(r)

BENCH = [(29.6e3, 0.0, 1.0, "doc 70 #10: M_S fitted to M_h, X_t = 0"),
         (2.66e3, 0.0, 1.0, "route 1: unification M_S, X_t = 0"),
         (2.53e3, -2.0, 1.0, "route 1: unification M_S, X_t = -2 M_S")]

if __name__ == "__main__":
    jobs = [(lab, k, spk, kw, M, x, s) for (M, x, s, _) in BENCH for (lab, k, spk, kw) in STEPS]
    with Pool(8) as p:
        out = p.map(job, jobs)
    for (M, x, s, name) in BENCH:
        print("==", name, f"(M_S={M:.3g})")
        for o in out:
            if tuple(o["bench"]) == (M, x, s):
                if o.get("ok"):
                    print(f"  {o['label']:60s} Mt={o['Mt']:.2f} Mh={o['Mh']:.2f} tanb={o['tanb']:.1f} mis={o['unif_mismatch']:+.4f}")
                else:
                    print(f"  {o['label']:60s} FAILED")
    save("results_route3.json", out)
