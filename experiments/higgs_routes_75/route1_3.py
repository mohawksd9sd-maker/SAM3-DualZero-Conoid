"""Doc 75 routes 1 and 3 on the doc-73 unification solutions (results_route1d.json, results_route1c*.json).
lambda does not enter the M_t / tan beta / M_S solve, so M_t, M_S and unification are unchanged by these
delta-lambda shifts (checked in tests); only M_h is recomputed."""
import json, math, os
import h75
from h75 import clean, pulls

OR = os.path.join(h75.HERE, "..", "open_routes_72")


def rows():
    d = json.load(open(os.path.join(OR, "results_route1d.json")))
    pick = [o for o in d if o.get("ok") and o["kw"].get("sgn", 1.0) > 0 and set(o["kw"]) <= {"xt", "sgn", "mode"}]
    return pick


def route1(r, st):
    x_der = (r["M_S"] / r["Lambda"]) ** 2       # m_Sigma ~ M_S (universal soft scale), M_V ~ v_R ~ Lambda
    out = {"x_derived": x_der}
    for lab, x in (("derived", x_der), ("x=1 [C]", 1.0), ("x->inf [C]", 1e12)):
        for fr in (False, True):
            dl = h75.route1_dlam(r, x, st, frozen=fr)
            mh, _ = h75.mh_with(r, dl, st)
            out[f"{lab}|{'frozen' if fr else 'tracking'}"] = {"dlam": dl, "Mh": mh, "dMh": mh - r["Mh"], "pull_Mh": pulls(r["Mt"], mh)[1]}
    return out


def route3(r, st):
    low, hi, sm, thr, sp = st
    tb = r["tanb"]
    k_L = float(hi.sol(math.log(r["Lambda"]))[3])            # k = y_t at Lambda (spectral boundary, universal hypothesis)
    MS, Lam = r["M_S"], r["Lambda"]
    # model setting (doc 68/69: VL masses at Lambda): M_F = Lambda, scalar^2 = Lambda^2 + M_S^2
    d2 = h75.martin_dmh2(k_L, tb, Lam, Lam ** 2, eps=(MS / Lam) ** 2)
    d2h = h75.martin_dmh2(k_L, 1 / tb, Lam, Lam ** 2, eps=(MS / Lam) ** 2)   # second chain (H_d, h = y_t): hbar = h cos(beta) -> sin^4 -> cos^4
    model = {"k_Lambda": k_L, "dmh2_GeV2": d2 + d2h, "dMh_GeV": (d2 + d2h) / (2 * r["Mh"])}
    # counterfactual [C]: VL pair at the TeV scale, M_F = M_S, soft = M_S (x = 2), k = y_t^MSSM(M_S)
    k_S = float(hi.sol(math.log(MS))[3])
    cf = {}
    for lab, Xk in (("Xk=0", 0.0), ("Xk max", math.sqrt(2 * MS ** 2 * (3 * 2 - 1)))):
        d2 = h75.martin_dmh2(k_S, tb, MS, 2 * MS ** 2, Xk=Xk)
        mh, _ = h75.mh_with(r, h75.dlam_from_dmh2(d2), st)
        cf[lab] = {"k_MS": k_S, "dmh2_GeV2": d2, "Mh_pipeline": mh, "Mh_quadrature": math.sqrt(r["Mh"] ** 2 + d2)}
    return {"model": model, "counterfactual_TeV_VL": cf}


if __name__ == "__main__":
    out = []
    for r in rows():
        st = h75.state(r)
        mh0, _ = h75.mh_with(r, 0.0, st)
        o = {"kw": r["kw"], "M_S": r["M_S"], "Mt": r["Mt"], "Mh_doc73": r["Mh"], "Mh_recomputed": mh0, "tanb": r["tanb"],
             "pull_Mt": r["pull_Mt"], "route1": route1(r, st), "route3": route3(r, st)}
        out.append(clean(o))
        print(r["kw"], "Mt=%.2f Mh73=%.2f (re %.2f)" % (r["Mt"], r["Mh"], mh0))
        for k, v in o["route1"].items():
            if k != "x_derived":
                print("   R1", k, "dlam=%.5f Mh=%.2f dMh=%+.2f pull=%+.2f" % (v["dlam"], v["Mh"], v["dMh"], v["pull_Mh"]))
        print("   R1 x_derived=%.2e" % o["route1"]["x_derived"])
        m = o["route3"]["model"]
        print("   R3 model: k(L)=%.3f dmh2=%.3e GeV^2 dMh=%.3e GeV" % (m["k_Lambda"], m["dmh2_GeV2"], m["dMh_GeV"]))
        for k, v in o["route3"]["counterfactual_TeV_VL"].items():
            print("   R3 [C] TeV VL", k, "k=%.3f dmh2=%.0f Mh_pipe=%.2f Mh_quad=%.2f" % (v["k_MS"], v["dmh2_GeV2"], v["Mh_pipeline"], v["Mh_quadrature"]))
    json.dump(out, open(os.path.join(h75.HERE, "results_route1_3.json"), "w"), indent=1, default=float)
