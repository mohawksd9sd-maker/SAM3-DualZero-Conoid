"""Doc 72 shared helpers (exploratory). Dual-Zero regulator untouched: nothing here uses
eps(n) = omega0 (-1)^n n^-n or Reg_2.  Reuses the doc 60 / doc 70 pipeline unchanged."""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
TLP = os.path.join(HERE, "..", "two_loop_pati_salam")
sys.path.insert(0, TLP)
SIG_MT, SIG_MH = 1.218, 1.763          # doc 60 combined pulls
MT_OBS, MH_OBS = 172.5, 125.1

def pulls(Mt, Mh):
    return (Mt - MT_OBS) / SIG_MT, (Mh - MH_OBS) / SIG_MH

def clean(x):
    import numpy as np
    if isinstance(x, dict): return {k: clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [clean(v) for v in x]
    if isinstance(x, (np.floating, np.integer)): return float(x)
    if isinstance(x, np.ndarray): return clean(x.tolist())
    return x

def save(name, obj):
    p = os.path.join(HERE, name)
    json.dump(clean(obj), open(p, "w"), indent=1, default=float)
    return p


# ------------------------------------------------------------------ pole <-> MS-bar matching variants (route 3)
import math as _m
import two_loop_higgs as _th
_ORIG = (_th.msbar_at_Mt, _th.Mt_from_yt, _th.Mh_from_lambda)

def _v4(p):
    """Buttazzo et al. v4 fits with their own reference point M_t = 173.34 (doc 60 used 173.10)."""
    dt = p.Mt - 173.34
    da = (p.alpha_s - 0.1184) / 0.0007
    dw = (p.MW - 80.384) / 0.014
    v = 246.22
    return {"lambda": 0.12604 + 0.00206 * (p.Mh - 125.15) - 0.00004 * dt, "yt": 0.93690 + 0.00556 * dt - 0.00042 * da,
            "g2": 0.64779 + 0.00004 * dt + 0.00011 * dw, "gY": 0.35830 + 0.00011 * dt - 0.00020 * dw,
            "g3": 1.1666 + 0.00314 * da - 0.00046 * dt, "yb": _m.sqrt(2) * 2.75 / v, "ytau": _m.sqrt(2) * p.mtau / v}

# SMDR v1.3 (Martin-Robertson arXiv:1907.02500; 2025 reference inputs, alpha_s(MZ)=0.1180, MZ=91.1876),
# calc_fit run here at (Mt, Mh) = (171.5,125.1), (172.5,124.1/125.1/126.1), (173.5,125.1), Q = Mt:
SMDR = {"yt": (0.931530, 0.0055620), "lambda": (0.126087, 0.0020510, -0.0000435), "g3": (1.163455, -0.000464),
        "g2": (0.647595, 0.0000070), "gY": (0.358595, 0.0000025), "yb": 0.015507, "ytau": 0.00999492}

def _smdr(p):
    dt, dh = p.Mt - 172.5, p.Mh - 125.1
    da = (p.alpha_s - 0.1180) / 0.0007       # alpha_s slopes taken from Buttazzo (SMDR run only at 0.1180)
    return {"lambda": SMDR["lambda"][0] + SMDR["lambda"][1] * dh + SMDR["lambda"][2] * dt,
            "yt": SMDR["yt"][0] + SMDR["yt"][1] * dt - 0.00042 * da,
            "g2": SMDR["g2"][0] + SMDR["g2"][1] * dt, "gY": SMDR["gY"][0] + SMDR["gY"][1] * dt,
            "g3": SMDR["g3"][0] + SMDR["g3"][1] * dt + 0.00314 * da, "yb": SMDR["yb"], "ytau": SMDR["ytau"]}

def set_matching(mode="doc60"):
    if mode == "doc60":   # repo matching (after the 2026-11-26 erratum this equals "v4ref")
        _th.msbar_at_Mt, _th.Mt_from_yt, _th.Mh_from_lambda = _ORIG
    elif mode == "prefix":  # pre-erratum doc 60 matching: v4 couplings expanded around 173.10
        _th.msbar_at_Mt = lambda p: _v4(type(p)(**{**p.__dict__, "Mt": p.Mt + 0.24}))
        _th.Mt_from_yt = lambda yt, alpha_s=0.1180: 173.10 + (yt - 0.93690 + 0.00042 * (alpha_s - 0.1184) / 0.0007) / 0.00556
        _th.Mh_from_lambda = lambda lam, Mt: 125.15 + (lam - 0.12604 + 0.00004 * (Mt - 173.10)) / 0.00206
    elif mode == "v4ref":
        _th.msbar_at_Mt = _v4
        _th.Mt_from_yt = lambda yt, alpha_s=0.1180: 173.34 + (yt - 0.93690 + 0.00042 * (alpha_s - 0.1184) / 0.0007) / 0.00556
        _th.Mh_from_lambda = lambda lam, Mt: 125.15 + (lam - 0.12604 + 0.00004 * (Mt - 173.34)) / 0.00206
    elif mode == "smdr":
        _th.msbar_at_Mt = _smdr
        _th.Mt_from_yt = lambda yt, alpha_s=0.1180: 172.5 + (yt - SMDR["yt"][0] + 0.00042 * (alpha_s - 0.1180) / 0.0007) / SMDR["yt"][1]
        _th.Mh_from_lambda = lambda lam, Mt: 125.1 + (lam - SMDR["lambda"][0] - SMDR["lambda"][2] * (Mt - 172.5)) / SMDR["lambda"][1]
    else:
        raise ValueError(mode)
