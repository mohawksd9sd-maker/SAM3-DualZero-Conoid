"""Doc 68, route 1: systematic matter-content search (exploratory).

Dual-Zero untouched.  For every admissible finite content (Krajewski bimodule
entries of M_2(H)+M_2(H)+M_4(C), optionally +C, and of the CCM algebra
C+H+M_3(C)) compute the trace-derived boundary y_t/g at Lambda, re-solve
unification with the content's own (two-loop) beta functions and the
generalised gauge boundary alpha_a^-1/I_a = const, then M_t and M_h.
"""

from __future__ import annotations

import math
from fractions import Fraction as Fr
from functools import lru_cache
from typing import Dict, List, Sequence, Tuple

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

import content_engine as ce
import top_yukawa_search as tys
import two_loop_higgs as th
from rge import match_to_ps

E = ce.Extra

# ------------------------------------------------------------------ admissible PS bimodule entries, (R, L, 4) order
# (Weyl content of one entry n_i (x) n_j^o; VL = entry + its conjugate; real reps may stand alone)
PS_ENTRIES = {
    "(1,2,4)+cc  [H_L x M4^o, VL]": [("1", "F", "F"), ("1", "F", "Fbar")],
    "(2,1,4)+cc  [H_R x M4^o, VL]": [("F", "1", "F"), ("F", "1", "Fbar")],
    "(2,2,1)     [H_L x H_R^o]": [("F", "F", "1")],
    "(3,1,1)+(1) [H_R x H_R^o]": [("adj", "1", "1")],
    "(1,3,1)+(1) [H_L x H_L^o]": [("1", "adj", "1")],
    "(1,1,15)+(1)[M4 x M4^o]": [("1", "1", "adj")],
    "(1,1,4)+cc  [C x M4^o, needs C summand]": [("1", "1", "F"), ("1", "1", "Fbar")],
    "(1,2,1)x2   [H_L x C^o, needs C summand]": [("1", "F", "1"), ("1", "F", "1")],
    "(2,1,1)x2   [H_R x C^o, needs C summand]": [("F", "1", "1"), ("F", "1", "1")],
}


def ps_extras(key: str, k: int = 1, mass="Lambda", da: float = 0.0, da4: float = 0.0) -> Tuple[ce.Extra, ...]:
    reps = PS_ENTRIES[key]
    out = []
    for i, r in enumerate(reps):
        out.append(E(f"{key}#{i}", "PS", r, "weyl", k, mass, True, da if i == 0 else 0.0, da4 if i == 0 else 0.0))
    return tuple(out)


def entry_index(key: str) -> List[float]:
    return list(sum(e.index() for e in ps_extras(key)))


# ------------------------------------------------------------------ fast screen for trace-only content (masses at Lambda)


@lru_cache(maxsize=1)
def _ps_grid():
    sm = ce._sm_cached((), 172.5, 0.1180)
    lms = np.linspace(4.0, 16.5, 301)
    sols = []
    for lm in lms:
        s0 = match_to_ps(sm.at(10 ** lm), "composite", None, True)
        sols.append(ce.ps_run(s0, lm * math.log(10), math.log(1e21), ()))
    return sm, lms, sols


def _unify_trace_only(I: Sequence[float]):
    sm, lms, sols = _ps_grid()
    I = np.asarray(I, float)

    def meet(pw, tR):
        def gap(t):
            g = pw(t)[:3]
            return (4 * math.pi / g[0] ** 2) / I[0] - (4 * math.pi / g[1] ** 2) / I[1]
        ts = np.linspace(tR + 1e-6, math.log(1e21) - 1e-6, 120)
        vs = [gap(t) for t in ts]
        for t0, t1, v0, v1 in zip(ts[:-1], ts[1:], vs[:-1], vs[1:]):
            if v0 * v1 <= 0:
                tL = brentq(gap, t0, t1, xtol=1e-12)
                g = pw(tL)[:3]
                return tL, (4 * math.pi / g[2] ** 2) / I[2] - (4 * math.pi / g[1] ** 2) / I[1]
        return None
    vals = []
    for lm, pw in zip(lms, sols):
        r = meet(pw, lm * math.log(10))
        vals.append(r)
    for i in range(len(lms) - 1):
        if vals[i] and vals[i + 1] and vals[i][1] * vals[i + 1][1] < 0:
            def f(lm):
                s0 = match_to_ps(sm.at(10 ** lm), "composite", None, True)
                pw = ce.ps_run(s0, lm * math.log(10), math.log(1e21), ())
                r = meet(pw, lm * math.log(10))
                return float("nan") if r is None else r[1]
            root = brentq(f, lms[i], lms[i + 1], xtol=1e-10)
            s0 = match_to_ps(sm.at(10 ** root), "composite", None, True)
            pw = ce.ps_run(s0, root * math.log(10), math.log(1e21), ())
            tL, _ = meet(pw, root * math.log(10))
            return {"m_R": 10 ** root, "Lambda": math.exp(tL), "pw": pw, "sm": sm, "I": I}
    return None


def predict_trace_only(I: Sequence[float], da: float = 0.0, da4: float = 0.0, n: float = 1.0) -> Dict[str, object]:
    """Same as content_engine.predict_ps for extras with masses at Lambda (only traces change)."""
    orig = ce.unify_ps
    try:
        ce.unify_ps = lambda c, Mt=172.5, alpha_s=0.118: _unify_trace_only(I)
        dummy = ce.Content("trace-only", (E("x", "PS", ("1", "1", "1"), "weyl", 1, "Lambda", True, da, da4),), n=n)
        return ce.predict_ps(dummy)
    finally:
        ce.unify_ps = orig


def screen(max_each: int = 12) -> List[Dict[str, object]]:
    """All integer Delta I = (dI_R, dI_L, dI_4) in [0, max]^3 (reachable with the C-extended entries)."""
    out = []
    for dR in range(0, max_each + 1, 2):
        for dL in range(0, max_each + 1, 2):
            for d4 in range(0, max_each + 1, 2):
                I = [6 + dR, 6 + dL, 6 + d4]
                r = predict_trace_only(I)
                rec = {"dI": [dR, dL, d4], "ok": r.get("ok", False)}
                if r.get("ok"):
                    rec.update({k: float(r[k]) for k in ("Mt", "Mh", "Lambda", "m_R", "yt_over_g", "yt_over_g_needed")})
                    rec["unif_ok"] = bool(r["Lambda"] < ce.M_PL_RED and r["m_R"] < r["Lambda"])
                out.append(rec)
    return out


# ------------------------------------------------------------------ catalogue of single entries (with running) + SM-algebra entries


def catalogue() -> List[Dict[str, object]]:
    rows = []
    rows.append(ce.row(ce.Content("PS baseline (3 generations, doc 60)"), ce.predict_ps(ce.Content("b")), I=[6, 6, 6]))
    for key in PS_ENTRIES:
        for mass in ("Lambda", "mR"):
            for k in (1, 2, 3):
                c = ce.Content(f"{key} x{k}, mass {mass}", ps_extras(key, k, mass), derived=True, params=0,
                               note="no Higgs Yukawa (Dirac/Majorana mass in D_F)")
                r = ce.predict_ps(c)
                rows.append(ce.row(c, r, I=list(c.I()), entry=key, k=k, mass=mass))
    return rows


SM_ENTRIES = {
    "vector doublet (1,2,-1/2)+cc (Stephan 2007)": [(Fr(3, 20), "F", "1"), (Fr(3, 20), "F", "1")],
    "VL quark doublet (3,2,1/6)+cc": [(Fr(3, 5) / 36, "F", "F"), (Fr(3, 5) / 36, "F", "Fbar")],
    "VL up singlet (3,1,2/3)+cc": [(Fr(3, 5) * Fr(4, 9), "1", "F"), (Fr(3, 5) * Fr(4, 9), "1", "Fbar")],
    "VL down singlet (3,1,-1/3)+cc": [(Fr(3, 5) / 9, "1", "F"), (Fr(3, 5) / 9, "1", "Fbar")],
    "VL charged lepton (1,1,1)+cc (Stephan 2005)": [(Fr(3, 5), "1", "1"), (Fr(3, 5), "1", "1")],
    "wino-like triplet (1,3,0)": [(Fr(0), "adj", "1")],
    "gluino-like octet (8,1,0)": [(Fr(0), "1", "adj")],
}


def sm_extras(key, k=1, mass=1e4, da=0.0, da4=0.0):
    return tuple(E(f"{key}#{i}", "SM", r, "weyl", k, mass, True, da if i == 0 else 0.0, da4 if i == 0 else 0.0)
                 for i, r in enumerate(SM_ENTRIES[key]))


def sm_catalogue() -> List[Dict[str, object]]:
    rows = [ce.row(ce.Content("CCM SM algebra, boundary g2=g3 (doc 61)"), ce.predict_sm(ce.Content("ccm")), I=[6, 6, 6])]
    for key in SM_ENTRIES:
        for mass in (1e4, 1e13):
            for k in (1, 2, 3):
                c = ce.Content(f"SM-alg + {key} x{k}, mass {mass:.0e} GeV", sm_extras(key, k, mass), derived=False, params=1,
                               note="Dirac mass is a free D_F modulus")
                r = ce.predict_sm(c)
                rows.append(ce.row(c, r, I=list(ce.sm_index(c.extras)), entry=key, k=k, mass=mass,
                                   g1_mismatch=r.get("g1_mismatch")))
    return rows


# ------------------------------------------------------------------ Higgs-coupled content (Yukawa = free D_F modulus) and inversion


def fit_share(make, lo=0.0, hi=30.0, n=31):
    """Solve the Yukawa share Delta a that gives M_t = 172.5 for a content family make(da)."""
    f = lambda x: (lambda r: r["Mt"] if r.get("ok") else float("nan"))(ce.predict_ps(make(x)))
    return tys.solve_for(f, 172.5, lo, hi, n)


HIGGS_COUPLED = {
    # name: (entries, multiplicity-of-components m so that da4 = da^2 / m, mass)
    "VL 16+16bar pair, one chain L H R (doc 63)": (["(1,2,4)+cc  [H_L x M4^o, VL]", "(2,1,4)+cc  [H_R x M4^o, VL]"], 4),
    "VL 16+16bar pair, two chains (doc 63)": (["(1,2,4)+cc  [H_L x M4^o, VL]", "(2,1,4)+cc  [H_R x M4^o, VL]"], 8),
    "electroweakino-like (2,2,1)+singlet, y psi Phi S": (["(2,2,1)     [H_L x H_R^o]"], 2),
    "(2,2,1)+(3,1,1)+(1,3,1), y psi Phi T": (["(2,2,1)     [H_L x H_R^o]", "(3,1,1)+(1) [H_R x H_R^o]", "(1,3,1)+(1) [H_L x H_L^o]"], 6),
    "VL lepton-like (1,2,1)x2 + C-singlets, y L H E": (["(1,2,1)x2   [H_L x C^o, needs C summand]"], 2),
}


def higgs_coupled_rows() -> List[Dict[str, object]]:
    rows = []
    for name, (keys, m) in HIGGS_COUPLED.items():
        for mass in ("Lambda", "mR"):
            def make(da, keys=keys, m=m, mass=mass):
                ex = []
                for j, kk in enumerate(keys):
                    ex += list(ps_extras(kk, 1, mass, da if j == 0 else 0.0, da * da / m if j == 0 else 0.0))
                return ce.Content(f"{name}, mass {mass}", tuple(ex), derived=False, params=1, note="Yukawa share fitted to M_t")
            x = fit_share(make)
            if not np.isfinite(x):
                c = make(0.0)
                rows.append({"name": c.name, "derived": False, "params": 1, "ok": False,
                             "reason": "no Yukawa share reaches M_t = 172.5 (perturbative range)"})
                continue
            c = make(x)
            r = ce.predict_ps(c)
            rows.append(ce.row(c, r, I=list(c.I()), share=x, c_over_yt=math.sqrt(x / m)))
            # zero-parameter 'universal Yukawa' hypothesis: every Higgs-coupled component has y = y_t
            cu = make(float(m))
            cu = ce.Content(f"{name}, mass {mass}, universal y = y_t", cu.extras, derived=True, params=0,
                            note="hypothesis: universal D_F Yukawa")
            rows.append(ce.row(cu, ce.predict_ps(cu), I=list(cu.I()), share=float(m)))
    return rows


def requirement_curve() -> List[Dict[str, float]]:
    """Inversion: Delta a needed for M_t = 172.5 vs the added universal trace Delta N (masses at Lambda)."""
    out = []
    for dN in (0, 1, 2, 3, 4, 6):
        I = [6 + 2 * dN] * 3
        f = lambda x: (lambda r: r["Mt"] if r.get("ok") else float("nan"))(predict_trace_only(I, x, x * x / 4))
        x = tys.solve_for(f, 172.5, 0.0, 40.0, 21)
        r = predict_trace_only(I, x, x * x / 4) if np.isfinite(x) else {}
        out.append({"dN": dN, "da_needed": x, "Mh": float(r.get("Mh", float("nan")))})
    return out


def fourth_generation() -> Dict[str, object]:
    """Chiral 4th PS generation: Delta I = (2,2,2); masses only from the Higgs (m <= y v/sqrt2)."""
    # requirement at Delta N = 1 from the inversion; PS Yukawas: share 4 c_u^2 + 4 c_d^2
    return {"dI": [2, 2, 2], "share_needed_note": "from requirement_curve at dN=1",
            "status": "excluded: a chiral 4th generation gets its mass only from v; LHC Higgs rates (gg->h x~9) "
                      "and direct searches exclude it (e.g. Djouadi-Lenz PLB 715 (2012) 310; Eberhardt et al. PRL 109 (2012) 241802)"}


def r_sector_scan(kmax: int = 24) -> List[Dict[str, object]]:
    """Zero-parameter direction found by the screen: only I_R grows (SU(2)_R-charged, colourless,
    Higgs-blind fermions).  y_t/g_L stays 1, Lambda and m_R fall.  Scan the multiplicity."""
    out = []
    for key in ("(3,1,1)+(1) [H_R x H_R^o]", "(2,1,1)x2   [H_R x C^o, needs C summand]"):
        for mass in ("Lambda", "mR"):
            for k in range(1, kmax + 1):
                c = ce.Content(f"{key} x{k}, mass {mass}", ps_extras(key, k, mass), derived=True, params=0,
                               note="integer multiplicity k is a discrete choice")
                r = ce.predict_ps(c)
                rec = ce.row(c, r, I=list(c.I()), entry=key, k=k, mass=mass)
                if r.get("ok"):
                    rec["leptoquark_bound_ok"] = bool(r["m_R"] > 1e6)   # PS leptoquark (= m_R here): K_L -> mu e
                out.append(rec)
                if not r.get("ok") and k > 3:
                    break
    return out


def extra_rows() -> List[Dict[str, object]]:
    rows = []
    # zero-parameter 'universal Yukawa' hypothesis for k VL 16-pairs, one or two chains (masses at Lambda)
    for k in (1, 2, 3):
        for chains in (1, 2):
            da = 4.0 * k * chains
            I = [6 + 4 * k] * 3
            r = predict_trace_only(I, da, da * da / (4 * k * chains))
            c = ce.Content(f"{k} VL 16-pair(s), {chains} chain(s), universal y = y_t (masses at Lambda)",
                           derived=True, params=0, note="hypothesis: universal D_F Yukawa on the new block")
            rows.append(ce.row(c, r, I=I, share=da))
    # chiral 4th generation (formal: boundary + running as if heavy; excluded experimentally)
    for label, da in (("4th PS generation, y_u4 = y_nu4 = y_t, y_d4 = y_e4 = 0 (formal)", 4.0),
                      ("4th PS generation, all Yukawas = y_t (formal)", 8.0)):
        r = predict_trace_only([8, 8, 8], da, da)
        c = ce.Content(label, derived=False, params=0, note="excluded: chiral 4th generation (LHC h rates, direct searches)")
        rows.append(ce.row(c, r, I=[8, 8, 8], share=da))
    # SO(10)-like single-Higgs Yukawa unification y_b = y_tau = y_t (formal; inadmissible algebra; m_b = m_t)
    r = predict_trace_only([6, 6, 6], 4.0, 4.0)
    c = ce.Content("SO(10)-like 10_H: y_t = y_b = y_tau = y_nu, one light Higgs (formal)", derived=False, params=0,
                   note="inadmissible (Lizzi-Mangano-Miele-Sparano 1996) and m_b = m_t at tree level")
    rows.append(ce.row(c, r, I=[6, 6, 6], share=4.0))
    return rows
