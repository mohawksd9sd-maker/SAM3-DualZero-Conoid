"""Doc 75 route 2: X_t from a universal spectral soft boundary at Lambda, iterated with exact unification.
For each boundary (m0/M12, A0/M12, weights): soft RGEs Lambda -> M_S on the current solution, build the
non-degenerate Spec (mu, m_A from tree EWSB, mu > 0), re-solve M_S from exact unification, repeat."""
import json, math, sys
from multiprocessing import Pool
from dataclasses import asdict
import numpy as np
from scipy.optimize import brentq
import h75
from h75 import T, set_matching, clean, pulls

FULL = dict(sm3=True, mssm3=True)


def unif(sp, mode="doc60", alpha_s=0.1180, lo=4e2, hi=4e4, n=9):
    set_matching(mode)
    def run(lm):
        return T.solve72(math.exp(lm), sp, alpha_s=alpha_s, **FULL)
    def f(lm):
        r = run(lm)
        return r["unif_mismatch"] if r.get("ok") else float("nan")
    xs = np.linspace(math.log(lo), math.log(hi), n)
    vs = [f(x) for x in xs]
    for a, b, va, vb in zip(xs[:-1], xs[1:], vs[:-1], vs[1:]):
        if np.isfinite(va) and np.isfinite(vb) and va * vb < 0:
            lm = brentq(f, a, b, xtol=2e-3)
            r = run(lm)
            r["kw"] = {"mode": mode, "alpha_s": alpha_s}
            return r
    return {"ok": False, "vals": vs}


def job(b):
    m0, A0, w = b["m0"], b["A0"], b["weights"]
    mode, a_s = b.get("mode", "doc60"), b.get("alpha_s", 0.1180)
    if b.get("seed") == "r2":   # batch 2: start from the converged batch-1 point (m0, A0) = (0.5, 0)
        seed = json.load(open(h75.os.path.join(h75.HERE, "results_route2.json")))[1]["result"]
    else:
        seed = json.load(open(h75.os.path.join(h75.HERE, "..", "open_routes_72", "results_route1d.json")))[5]  # doc 73 X_t = 0
    seed["kw"] = {"mode": mode, "alpha_s": a_s}
    r, hist = seed, []
    for it in range(4):
        low, hi_, sm, thr, sp0 = h75.state(r)
        o = h75.soft_run(hi_, r["Lambda"], r["M_S"], m0=m0, A0=A0, weights=w)
        sp, info = h75.spec_from_soft(o, r["tanb"])
        if sp is None:
            return clean({"b": b, "ok": False, "it": it, "info": info, "hist": hist})
        rn = unif(sp, mode, a_s)
        if not rn.get("ok"):
            return clean({"b": b, "ok": False, "it": it, "info": info, "reason": "no unification root", "hist": hist})
        hist.append({"Xt_hat": info["Xt_hat"], "M_S": rn["M_S"], "Mt": rn["Mt"], "Mh": rn["Mh"], "tanb": rn["tanb"]})
        conv = r is not seed and abs(rn["Mh"] - r["Mh"]) < 0.05 and abs(rn["Mt"] - r["Mt"]) < 0.02
        r = rn
        if conv:
            break
    return clean({"b": b, "ok": True, "result": r, "info": info, "soft": o, "hist": hist})


BATCH2 = [dict(m0=m, A0=a, weights=False, seed="r2") for m, a in
          ((0.3, -0.6), (0.3, 0.4), (0.8, -0.6), (0.8, 0.3), (0.5, -0.3), (0.5, 0.2), (0.0, 0.0), (0.15, 0.0))]
BATCH2 += [dict(m0=0.5, A0=0.0, weights=False, seed="r2", mode="smdr"),
           dict(m0=0.5, A0=0.0, weights=False, seed="r2", alpha_s=0.1171),
           dict(m0=0.5, A0=0.0, weights=False, seed="r2", alpha_s=0.1189)]

if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "batch2":
    with Pool(8) as p:
        out = p.map(job, BATCH2)
    for o in out:
        if o["ok"]:
            R = o["result"]
            print(o["b"], "Xt^=%.3f M_S=%.0f Mt=%.2f Mh=%.2f tanb=%.1f mA/MS=%.2f pulls %+.2f %+.2f" % (o["info"]["Xt_hat"], R["M_S"], R["Mt"], R["Mh"], R["tanb"], o["info"]["mA_over_MS"], R["pull_Mt"], R["pull_Mh"]), "iters", len(o["hist"]), flush=True)
        else:
            print(o["b"], "FAILED", o.get("reason"), o.get("info"), o.get("hist"), flush=True)
    json.dump(out, open(h75.os.path.join(h75.HERE, "results_route2_batch2.json"), "w"), indent=1, default=float)
elif __name__ == "__main__":
    B = [dict(m0=m, A0=a, weights=False) for m, a in ((1.0, 0.0), (0.5, 0.0), (1.0, -0.4), (1.5, -0.6), (1.5, 0.8), (0.75, -0.2))]
    B += [dict(m0=1.5, A0=0.0, weights=True), dict(m0=1.0, A0=0.0, weights=False, mode="smdr")]
    with Pool(8) as p:
        out = p.map(job, B)
    for o in out:
        if o["ok"]:
            R = o["result"]
            print(o["b"], "Xt^=%.3f M_S=%.0f Mt=%.2f Mh=%.2f tanb=%.1f pulls %+.2f %+.2f" % (o["info"]["Xt_hat"], R["M_S"], R["Mt"], R["Mh"], R["tanb"], R["pull_Mt"], R["pull_Mh"]), "iters", len(o["hist"]))
        else:
            print(o["b"], "FAILED", o.get("reason"), o.get("info"), o.get("hist"))
    json.dump(out, open(h75.os.path.join(h75.HERE, "results_route2.json"), "w"), indent=1, default=float)
