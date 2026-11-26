"""Doc 76 items (b)-(d): re-solve exact unification (M_t, M_h) for the doc-75 route-2 points after
  'soft2L' : two-loop soft running  -- doc-75 Spec x (SOFTSUSY 2L-soft / 1L-soft) per parameter
             (xt additive shift), from results_softsusy_2loop.json;
  'ewsb1L' : soft2L + one-loop-tadpole EWSB -- mu^2 and m_A^2 shifted additively by SOFTSUSY's
             (loop - tree) difference at its own Q = M_S (tree evaluated from its mHu2, mHd2, tan beta);
  'Qhalf' / 'Qtwo' : matching-scale variation of the ewsb1L point: every mass in the Spec divided by
             c = 1/2 or 2, so the same physical spectrum is matched at Q = c * M_S.
Writes results_rerun76.json."""
import json, math, os, sys
from dataclasses import asdict, replace
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "higgs_routes_75"))
import h75                      # noqa: E402
import route2_run as R2         # noqa: E402
from h75 import T               # noqa: E402

MASS = ("xt", "mQ", "mU", "mD", "msf", "msl", "M1", "M2", "M3", "mu", "mA")
SS2SPEC = dict(mQ="mQ", mU="mU", mD="mD", msf="msq1", msl="msl1", M1="M1", M2="M2", M3="M3", mu="mu_over_MS", mA="mA_over_MS")


def tree_ewsb(s):
    t2 = s["tanb_run"] ** 2
    mu2 = (s["mhd2_MS2"] - s["mhu2_MS2"] * t2) / (t2 - 1)
    return mu2, s["mhu2_MS2"] + s["mhd2_MS2"] + 2 * mu2


def specs_for(row, spec0):
    s1, s2 = row["ss1"], row["ss2"]
    d = dict(spec0)
    out = {}
    b = dict(d)
    for k, kk in SS2SPEC.items():
        b[k] = d[k] * s2[kk] / s1[kk]        # SLHA MSOFT entries are masses (21/22 are m^2_H)
    b["xt"] = d["xt"] + (s2["Xt_hat"] - s1["Xt_hat"])
    out["soft2L"] = b
    e = dict(b)
    mu2t, mA2t = tree_ewsb(s2)
    mu2 = b["mu"] ** 2 + (s2["mu_over_MS"] ** 2 - mu2t)
    mA2 = b["mA"] ** 2 + (s2["mA_over_MS"] ** 2 - mA2t)
    e["mu"] = math.copysign(math.sqrt(mu2), b["mu"])
    e["mA"] = math.sqrt(mA2)
    out["ewsb1L"] = e
    for tag, c in (("Qhalf", 0.5), ("Qtwo", 2.0)):
        q = dict(e)
        for k in MASS:
            q[k] = e[k] / c
        out[tag] = q
    return out


def job(a):
    tag, var, spd = a
    sp = T.Spec(**spd)
    lo, hi = (2e2, 2e4) if var == "Qhalf" else ((8e2, 1e5) if var == "Qtwo" else (4e2, 4e4))
    r = R2.unif(sp, "doc60", 0.1180, lo=lo, hi=hi, n=9)
    keep = {k: r.get(k) for k in ("ok", "M_S", "Mt", "Mh", "tanb", "Lambda", "pull_Mt", "pull_Mh", "Delta_b")}
    return dict(tag=tag, var=var, spec=spd, res=h75.clean(keep))


if __name__ == "__main__":
    rows = json.load(open(os.path.join(HERE, "results_softsusy_2loop.json")))
    from softsusy_2loop import POINTS, load_point
    jobs, meta = [], {}
    for row, (tag, f, idx) in zip(rows, POINTS):
        b, R, i = load_point(f, idx)
        spec0 = R["spec"]
        meta[tag] = {"doc75": {"M_S": R["M_S"], "Mt": R["Mt"], "Mh": R["Mh"], "mA_over_MS": i["mA_over_MS"], "mu_over_MS": i["mu_over_MS"]}}
        for var, spd in specs_for(row, spec0).items():
            jobs.append((tag, var, spd))
    with Pool(8) as p:
        out = p.map(job, jobs)
    for o in out:
        r = o["res"]
        meta[o["tag"]][o["var"]] = o
        if r.get("ok"):
            print(o["tag"], o["var"], "M_S=%.0f Mt=%.2f Mh=%.2f tanb=%.1f mA/MS=%.3f mu/MS=%.3f" % (r["M_S"], r["Mt"], r["Mh"], r["tanb"], o["spec"]["mA"], o["spec"]["mu"]), flush=True)
        else:
            print(o["tag"], o["var"], "FAILED", flush=True)
    json.dump(meta, open(os.path.join(HERE, "results_rerun76.json"), "w"), indent=1, default=float)
