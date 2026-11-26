"""Doc 76 item (b): size of two-loop soft running for the doc-75 route-2 boundary.

Runs SOFTSUSY 4.1.13 (Allanach, hep-ph/0104145; built locally, not vendored) with the route-2 boundary
(universal M12, m0, A0 at a FIXED scale Lambda = EXTPAR 0, mu > 0) twice: RGE loop order 1 and 2
(env SS_SOFT_1LOOP drops only the two-loop soft beta terms in softpars.cpp: a 1-line local patch;
gauge/Yukawa running is unchanged between the two runs).  The ratio of the low-scale soft quantities
(2L / 1L) is the two-loop soft-running correction; it is then applied to the doc-75 Spec and the
exact-unification solve is redone (route2_rerun.py).  SOFTSUSY's own Higgs mass is NOT used.
Set SOFTPOINT to the softpoint.x path (default /workspace/tools/softsusy-4.1.13/softpoint.x)."""
import json, math, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOFTPOINT = os.environ.get("SOFTPOINT", "/workspace/tools/softsusy-4.1.13/softpoint.x")

TEMPLATE = """Block MODSEL
    1    1
Block SMINPUTS
    1   1.279340000e+02
    2   1.166378700e-05
    3   {alpha_s:.6e}
    4   9.118760000e+01
    5   4.180000000e+00
    6   {mt:.6e}
    7   1.776860000e+00
Block MINPAR
    1   {m0:.6e}
    2   {m12:.6e}
    3   {tanb:.6e}
    4   1.0
    5   {A0:.6e}
Block EXTPAR
    0   {Lam:.6e}
Block SOFTSUSY
    1   1.0e-04
    2   0
    3   0
    7   2
   12   1
   19   0
   20   0
"""


def parse_slha(txt):
    blocks, cur = {}, None
    for line in txt.splitlines():
        s = line.split("#")[0].strip()
        if not s:
            continue
        if s.upper().startswith("BLOCK"):
            cur = s.split()[1].upper()
            blocks.setdefault(cur, {})
            if "Q=" in s.upper():
                blocks[cur]["Q"] = float(s.upper().split("Q=")[1].split()[0])
            continue
        if cur is None or s.upper().startswith("DECAY"):
            cur = None
            continue
        p = s.split()
        try:
            vals = [float(x) for x in p]
        except ValueError:
            continue
        if len(vals) >= 2:
            blocks[cur][tuple(int(v) for v in vals[:-1])] = vals[-1]
    return blocks


def run_point(m0, A0, M12, tanb, Lam, loops, alpha_s=0.1180, mt=172.57):
    inp = TEMPLATE.format(alpha_s=alpha_s, mt=mt, m0=m0 * M12, m12=M12, tanb=tanb, A0=A0 * M12, Lam=Lam)
    env = dict(os.environ)
    env.pop("SS_SOFT_1LOOP", None)
    if loops == 1:
        env["SS_SOFT_1LOOP"] = "1"     # local patch: drop only the two-loop SOFT beta-function terms
    p = subprocess.run([SOFTPOINT, "leshouches"], input=inp, capture_output=True, text=True, env=env, timeout=600)
    b = parse_slha(p.stdout)
    try:
        ms, hm, au = b["MSOFT"], b["HMIX"], b["AU"]
    except KeyError:
        return {"ok": False, "stdout_tail": p.stdout[-800:], "stderr": p.stderr[-400:]}
    mQ3, mU3 = ms[(43,)], ms[(46,)]
    MS = math.sqrt(mQ3 * mU3)
    mu, tb_run, mA2 = hm[(1,)], hm[(2,)], hm[(4,)]
    At = au[(3, 3)]
    out = dict(ok=True, Q=ms.get("Q"), MS=MS, M12=M12, MS_over_M12=MS / M12, mu_over_MS=mu / MS,
               mA_over_MS=math.copysign(math.sqrt(abs(mA2)), mA2) / MS, At_over_MS=At / MS,
               Xt_hat=(At - mu / tb_run) / MS, tanb_run=tb_run,
               M1=ms[(1,)] / MS, M2=ms[(2,)] / MS, M3=ms[(3,)] / MS,
               mQ=mQ3 / MS, mU=mU3 / MS, mD=ms[(49,)] / MS,
               stau_L=ms[(33,)] / MS, stau_R=ms[(36,)] / MS,
               msq1=(ms[(41,)] * ms[(44,)] * ms[(47,)]) ** (1 / 3) / MS,
               msl1=(ms[(31,)] * ms[(34,)]) ** 0.5 / MS,
               mhu2_MS2=ms[(22,)] / MS ** 2, mhd2_MS2=ms[(21,)] / MS ** 2,
               yt=b.get("YU", {}).get((3, 3)), yb=b.get("YD", {}).get((3, 3)), ytau=b.get("YE", {}).get((3, 3)),
               g3=b.get("GAUGE", {}).get((3,)),
               problem=[l for l in p.stdout.splitlines() if "roblem" in l or "WARNING" in l][:3])
    return out


POINTS = [  # (m0, A0) route-2 boundaries; M12, tanb, Lambda from the doc-75 converged results
    ("r2_0.5_0", "results_route2.json", 1),
    ("r2_0.75_-0.2", "results_route2.json", 5),
    ("b2_0.3_-0.6", "results_route2_batch2.json", 0),
    ("b2_0.8_-0.6", "results_route2_batch2.json", 2),
    ("b2_0_0", "results_route2_batch2.json", 6),
]


def load_point(fname, idx):
    o = json.load(open(os.path.join(HERE, "..", "higgs_routes_75", fname)))[idx]
    assert o["ok"]
    R, i = o["result"], o["info"]
    return o["b"], R, i


if __name__ == "__main__":
    res = []
    for tag, f, idx in POINTS:
        b, R, i = load_point(f, idx)
        M12 = R["M_S"] / i["MS_over_M12"]
        row = {"tag": tag, "b": b, "doc75": {k: i[k] for k in ("MS_over_M12", "mu_over_MS", "mA_over_MS", "Xt_hat", "stau_R", "stau_L")},
               "M_S": R["M_S"], "Lambda": R["Lambda"], "tanb": R["tanb"]}
        for L in (1, 2):
            row["ss%d" % L] = run_point(b["m0"], b["A0"], M12, R["tanb"], R["Lambda"], L)
        res.append(row)
        s1, s2 = row["ss1"], row["ss2"]
        if s1["ok"] and s2["ok"]:
            print(tag, " ".join("%s %.3f->%.3f" % (k, s1[k], s2[k]) for k in ("MS_over_M12", "Xt_hat", "mu_over_MS", "mA_over_MS", "stau_R", "M1")), flush=True)
        else:
            print(tag, "FAILED", s1.get("stdout_tail", "")[-300:], s2.get("stdout_tail", "")[-300:], flush=True)
    json.dump(res, open(os.path.join(HERE, "results_softsusy_2loop.json"), "w"), indent=1)
