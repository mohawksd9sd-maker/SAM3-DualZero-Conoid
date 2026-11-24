"""Doc 66: coupled 'ripples' -- several internal-geometry moduli that interact while they ring down.

Dimensionless setup (radiation era, H = 1/(2t)): time tau = m1 t, fields in units of the reduced Planck mass M,
potential in units of m1^2 M^2.  Two moduli (e.g. the area/radion phi1 and a shape modulus phi2 of the magnetized
surface; both are flat directions of the tree-level spectral action, doc 65):

    V = 1/2 phi1^2 + 1/2 mu^2 phi2^2 + eps mu phi1 phi2 + g3/2 phi1^2 phi2 + lam/4 phi1^2 phi2^2
    phi_i'' + (3/(2 tau) + Gamma) phi_i' + dV/dphi_i = 0

Part A scans: linear mixing (eps), nonlinear (g3, lam), parametric resonance of a spectator chi (Mathieu),
extra friction/back-reaction (Gamma), degenerate vs hierarchical mu.  Part B: phase coherence of the moduli and
large-angle CMB.  Physical consequences are read off with doc 65's `ripple_modulus.evaluate`.
"""

from __future__ import annotations

import math
from typing import Dict, List

import numpy as np
from scipy.integrate import solve_ivp

import ripple_modulus as rm

TAU0 = 1e-2


def eigen(mu: float, eps: float):
    Mm = np.array([[1.0, eps * mu], [eps * mu, mu * mu]])
    w, v = np.linalg.eigh(Mm)
    return w, v


def simulate(mu=1.0, eps=0.0, g3=0.0, lam=0.0, Gamma=0.0, phi0=(1.0, 1.0), tau_end=600.0, n_out=12000):
    def rhs(t, y):
        p1, p2, v1, v2 = y
        d1 = p1 + eps * mu * p2 + g3 * p1 * p2 + lam * p1 * p2 * p2
        d2 = mu * mu * p2 + eps * mu * p1 + 0.5 * g3 * p1 * p1 + lam * p1 * p1 * p2
        f = 1.5 / t + Gamma
        return [v1, v2, -f * v1 - d1, -f * v2 - d2]
    te = np.linspace(TAU0, tau_end, n_out)
    sol = solve_ivp(rhs, (TAU0, tau_end), [phi0[0], phi0[1], 0.0, 0.0], t_eval=te, rtol=1e-9, atol=1e-12,
                    method="DOP853")
    t = sol.t
    p1, p2, v1, v2 = sol.y
    a3 = t ** 1.5                                     # a ∝ t^{1/2}
    V2 = 0.5 * p1 ** 2 + 0.5 * mu * mu * p2 ** 2 + eps * mu * p1 * p2
    Vn = 0.5 * g3 * p1 * p1 * p2 + 0.25 * lam * p1 * p1 * p2 * p2
    E1 = a3 * (0.5 * v1 ** 2 + 0.5 * p1 ** 2)
    E2 = a3 * (0.5 * v2 ** 2 + 0.5 * mu * mu * p2 ** 2)
    Et = a3 * (0.5 * v1 ** 2 + 0.5 * v2 ** 2 + V2 + Vn)
    return {"t": t, "p1": p1, "p2": p2, "E1": E1, "E2": E2, "Et": Et, "ok": bool(sol.success)}


def _smooth(x, t, width):
    dt = t[1] - t[0]
    n = max(1, int(width / dt))
    k = np.ones(n) / n
    return np.convolve(x, k, mode="same")


def settle_time(t, E, tol=0.05, width=None):
    """First time after which the (period-averaged) comoving energy stays within tol of its final value."""
    width = width or 4 * math.pi
    Es = _smooth(E, t, width)
    cut = len(t) - int(width / (t[1] - t[0]))   # avoid convolution edge
    Es, tt = Es[:cut], t[:cut]
    fin = Es[-1]
    bad = np.where(np.abs(Es - fin) > tol * abs(fin))[0]
    return float(tt[bad[-1]]) if len(bad) else float(tt[0])


def settle_slowest(r, mu, eps):
    """Settle time of the slowest eigenmode: its period-averaged comoving energy reaches a constant (a^{-3} scaling)."""
    w, v = eigen(mu, eps)
    t = r["t"]
    p = np.vstack([r["p1"], r["p2"]])
    dp = np.gradient(p, t, axis=1)
    out = []
    for i in range(2):
        q, dq = v[:, i] @ p, v[:, i] @ dp
        E = t ** 1.5 * (0.5 * dq ** 2 + 0.5 * w[i] * q ** 2)
        out.append(settle_time(t, E, width=4 * math.pi / math.sqrt(max(w[i], 1e-12))))
    return max(out)


def runaway(r) -> bool:
    return bool(np.nanmax(np.abs(np.concatenate([r["p1"], r["p2"]]))) > 1e3 or not r["ok"])


def beat_share(r):
    """Amplitude of the late-time sloshing of energy between the flavour fields (share of E1)."""
    t, E1, E2 = r["t"], r["E1"], r["E2"]
    s = _smooth(E1, t, 4 * math.pi) / np.maximum(_smooth(E1 + E2, t, 4 * math.pi), 1e-300)
    late = s[int(0.5 * len(s)):int(0.95 * len(s))]
    return float(late.max() - late.min()), float(late.mean())


def light_mode(mu, eps, phi0=(1.0, 1.0)):
    """Lightest eigenmass (units m1), its share of the initial displacement and its coupling to alpha
    (alpha couples to phi1 only, beta from doc 65)."""
    w, v = eigen(mu, eps)
    if w[0] <= 0:
        return {"m_light": 0.0, "tachyonic": True}
    u = v[:, 0]
    amp = abs(u @ np.array(phi0))
    return {"m_light": math.sqrt(w[0]), "m_heavy": math.sqrt(w[1]), "amp": amp, "kappa_light": abs(u[0]), "tachyonic": False}


# ------------------------------------------------------------------ Part A
M1_NAT = rm.natural_benchmark()["m_eV"]          # Lambda^2/M (doc 65)


def to_seconds(tau, m1=M1_NAT):
    return tau / m1 * rm.HBAR


def phys_check(m_light_rel, amp, kappa, m1=M1_NAT):
    """Apply doc 65 constraints to the lightest eigenmode (phi_i = amp M, coupling kappa) for m1 natural."""
    m = m_light_rel * m1
    if m <= 1e-34:
        ff = rm.fifth_force(1e-40, kappa)
        return {"m_eV": m, "allowed": bool(ff["ok"]), "failed": [] if ff["ok"] else ["fifth force / EP"]}
    e = rm.evaluate(m, max(amp, 1e-30), max(kappa, 1e-30))
    return {"m_eV": m, "allowed": e["allowed"], "failed": e["failed"]}


def var_linear(eps_list=(0.0, 0.1, 0.5, 0.9, 0.99, 0.9999)) -> List[Dict]:
    out = []
    for eps in eps_list:
        lm = light_mode(1.3, eps)
        te = min(max(400.0, 30 / lm["m_light"]), 3e4)
        r = simulate(mu=1.3, eps=eps, tau_end=te, n_out=int(min(6e5, 40 * te)))
        ts = settle_slowest(r, 1.3, eps)
        bamp, _ = beat_share(r)
        dm = lm["m_heavy"] - lm["m_light"]
        out.append({"eps": eps, "m_light": lm["m_light"], "beat_period": 2 * math.pi / dm, "share_slosh": bamp,
                    "settle_tau_total": ts, "settle_tau_estimate_1_over_mlight": 1 / (2 * lm["m_light"]),
                    "doc65_light_mode": phys_check(lm["m_light"], lm["amp"], lm["kappa_light"])})
    return out


NONLIN_CASES = ((2.0, 0.3, 0.0), (2.0, 1.0, 0.0), (2.0, 3.0, 0.0), (1.0, 0.0, 1.0), (1.0, 0.0, 10.0), (1.0, 0.0, 100.0),
                (1.3, 0.0, 10.0))


def var_nonlinear(cases=NONLIN_CASES) -> List[Dict]:
    """mu = 2: cubic phi1^2 phi2 is 2:1 resonant (phi1 pumps phi2); mu = 1: quartic 1:1.  phi2 starts at 0.01."""
    out = []
    for mu, g3, lam in cases:
        lin = simulate(mu=mu, phi0=(1.0, 0.01), tau_end=400)
        r = simulate(mu=mu, g3=g3, lam=lam, phi0=(1.0, 0.01), tau_end=400)
        row = {"mu": mu, "g3": g3, "lam": lam, "runaway": runaway(r)}
        if not row["runaway"]:
            b, sh = beat_share(r)
            _, sh0 = beat_share(lin)
            row.update({"settle_tau": settle_time(r["t"], r["Et"]), "settle_tau_exchange": settle_time(r["t"], r["E2"]), "settle_tau_linear": settle_time(lin["t"], lin["Et"]),
                        "late_share_phi2": 1 - sh, "late_share_phi2_linear": 1 - sh0, "share_slosh": b,
                        "final_comoving_E_over_linear": float(r["Et"][-1] / lin["Et"][-1])})
        else:
            row["note"] = "cubic term unbounded below: modulus destabilized (decompactification/runaway)"
        out.append(row)
    return out


def mathieu(q0: float, k_grid=None, tau_end=60.0, mchi=0.0) -> Dict:
    """Spectator chi with g^2 phi1^2 chi^2/2: chi_k'' + 3/(2t) chi_k' + (k^2/a^2 + mchi^2 + 4 q0 phi1(t)^2) chi_k = 0,
    with phi1 the single-mode background (phi1(TAU0) = 1, so q0 = g^2 Phi^2/(4 m^2) at onset)."""
    bg = simulate(mu=1.0, phi0=(1.0, 0.0), tau_end=tau_end, n_out=20000)
    t, p1 = bg["t"], bg["p1"]
    if k_grid is None:
        k_grid = np.linspace(0.01, 2.5 * max(1.0, q0 ** 0.25), 30)
    best = (-np.inf, None)
    lnn = []
    for k in k_grid:
        def rhs(tt, y):
            ph = np.interp(tt, t, p1)
            w2 = k * k / tt + mchi ** 2 + 4 * q0 * ph * ph      # a^2 = t (a(1) = 1)
            return [y[2], y[3], -1.5 / tt * y[2] - w2 * y[0], -1.5 / tt * y[3] - w2 * y[1]]
        t_start = 0.5
        w0 = math.sqrt(k * k / t_start + mchi ** 2 + 4 * q0 * np.interp(t_start, t, p1) ** 2)
        y0 = [1 / math.sqrt(2 * w0), 0.0, 0.0, -w0 / math.sqrt(2 * w0)]
        s = solve_ivp(rhs, (t_start, tau_end), y0, rtol=1e-8, atol=1e-12, method="DOP853", max_step=0.05)
        c, ci, d, di = s.y[:, -1]
        te = s.t[-1]
        w = math.sqrt(k * k / te + mchi ** 2 + 4 * q0 * np.interp(te, t, p1) ** 2)
        a3 = te ** 1.5
        n = a3 * 0.5 * (w * (c * c + ci * ci) + (d * d + di * di) / w) - 0.5
        v = math.log(max(n, 1e-30))
        lnn.append(v)
        if v > best[0]:
            best = (v, k)
    return {"q0": q0, "ln_n_max": best[0], "k_peak": best[1], "k_grid": list(map(float, k_grid)), "ln_n": lnn}


def var_parametric(qs=(0.1, 1.0, 10.0, 100.0, 1000.0)) -> List[Dict]:
    """Back-reaction needs n_k ~ (M/m)^2 ~ 1.5e13 (ln n ~ 30) for the natural modulus.
    GW from resonance: f0 ~ 4e10 Hz (k_phys/rho^{1/4}) at production, Omega_GW h^2 ~ 1e-5 (frac)^2 (H/k)^2."""
    out = []
    need = 2 * math.log(rm.M / M1_NAT)
    rho14 = (3 * rm.M ** 2 * M1_NAT ** 2) ** 0.25
    for q in qs:
        r = mathieu(q)
        frac = min(1.0, math.exp(r["ln_n_max"] - need)) if r["ln_n_max"] > 0 else 0.0
        kph = r["k_peak"] * M1_NAT
        f0 = 4e10 * kph / rho14
        omega = 1e-5 * frac ** 2 * (M1_NAT / max(kph, 1e-300)) ** 2
        out.append({"q0": q, "ln_n_max": r["ln_n_max"], "k_peak": r["k_peak"], "ln_n_needed_backreaction": need,
                    "energy_fraction_drained": frac, "GW_f0_Hz": f0, "GW_Omega_h2": omega})
    return out


def var_friction(cs=(1.0, 10.0, 1e3, 1e6)) -> List[Dict]:
    """Extra dissipation (back-reacting / reflected waves, decay into radiation): Gamma = c * Gamma_grav.
    Lowest mass for which a phi_i = M modulus is safe (doc 65 rules with kappa_eff = sqrt(c))."""
    out = []
    for c in cs:
        k = math.sqrt(c)
        lo, hi = 8.0, 22.0
        for _ in range(40):
            mid = 0.5 * (lo + hi)
            if rm.evaluate(10 ** mid, 1.0, k)["allowed"]:
                hi = mid
            else:
                lo = mid
        out.append({"c": c, "m_min_eV": 10 ** hi, "m_min_TeV": 10 ** hi / 1e12})
    # dimensionless illustration: settle time vs Gamma (units m1)
    ill = []
    for G in (0.0, 0.01, 0.1, 1.0):
        r = simulate(mu=1.0, Gamma=G, phi0=(1.0, 0.0), tau_end=300)
        E = r["E1"] * np.exp(G * r["t"])          # remove the Gamma loss to define the ringing envelope
        ill.append({"Gamma_over_m": G, "E_comoving_final_over_initial": float(r["Et"][-1] / r["Et"][np.searchsorted(r["t"], 3.0)]),
                    "e_fold_tau": (1 / G if G > 0 else float("inf"))})
    return out + ill


def var_spectrum(cases=((1.0 + 1e-2, 0.0), (1.0 + 0.05, 0.0), (1e-2, 0.0), (1e-6, 0.0), (1e-12, 0.0), (1e-30, 0.0))) -> List[Dict]:
    out = []
    for mu, eps in cases:
        lm = light_mode(mu, eps)
        row = {"mu": mu, "m_light": lm["m_light"], "beat_period_tau": 2 * math.pi / abs(lm["m_heavy"] - lm["m_light"]),
               "settle_tau_estimate": 1 / (2 * min(lm["m_light"], 1.0))}
        if mu > 0.5:
            te = min(1.5 * row["beat_period_tau"], 1.2e4)
            r = simulate(mu=mu, tau_end=te, n_out=int(30 * te))
            a = r["p1"] + r["p2"]                     # alpha ∝ beta (phi1 + phi2) if both couple
            env = np.abs(a) * r["t"] ** 0.75
            late = env[len(env) // 2:]
            row["alpha_beat_contrast"] = float((late.max() - np.percentile(late, 2)) / late.max())
        row["doc65_light_mode"] = phys_check(lm["m_light"], lm["amp"], 1.0)
        out.append(row)
    return out


# ------------------------------------------------------------------ Part B: CMB large angles
def cmb_phases(m_eV: float = 1e-19, phi_i: float = 1e-2, H_inf_GeV: float = 1e10, n_modes: int = 2) -> Dict:
    """(i) Homogeneous moduli: phases are global (same in every Hubble patch) -> interference changes alpha(t)
    only: a monopole at last scattering (doc 65), zero for l >= 2.
    (ii) Light during inflation (m < H_inf): delta phi = H_inf/2pi per mode -> CDM isocurvature.
         Correlated modes (one field direction): S = 2 delta phi/phi; random (independent): S^2 / n_modes.
    (iii) Random phases set per Hubble patch at oscillation onset average over a CMB-scale patch as (k/k_osc)^{3/2}."""
    H_inf = H_inf_GeV * 1e9
    dphi = H_inf / (2 * math.pi) / rm.M
    S_corr = 2 * dphi / phi_i
    S_rand = S_corr / math.sqrt(n_modes)
    P_R = 2.1e-9
    beta_corr = S_corr ** 2 / (S_corr ** 2 + P_R)
    beta_rand = S_rand ** 2 / (S_rand ** 2 + P_R)
    # Planck 2018: uncorrelated CDM isocurvature beta_iso < 0.038 (k = 0.002/Mpc)
    lim = 0.038
    phi_min_corr = 2 * dphi / math.sqrt(lim / (1 - lim) * P_R)
    # (iii) comoving horizon at onset H = m (radiation era): k_osc = a H
    N = rm.background_table()[0]
    lnH = rm.background_table()[1]
    i = int(np.argmin(np.abs(lnH - math.log(m_eV))))
    k_osc_eV = math.exp(N[i]) * m_eV                                # comoving, today's units
    k_l2 = 2 / (14000 * 3.0857e22 / rm.HBARC)                       # l=2: k ~ 2/D_A, D_A ~ 14 Gpc, in eV
    supp = (k_l2 / k_osc_eV) ** 1.5
    return {"m_eV": m_eV, "phi_i": phi_i, "H_inf_GeV": H_inf_GeV, "dphi_over_M": dphi, "S_correlated": S_corr,
            "S_random": S_rand, "beta_iso_correlated": beta_corr, "beta_iso_random": beta_rand, "planck_beta_iso_max": lim,
            "phi_i_min_correlated_for_planck": phi_min_corr,
            "H_inf_max_GeV_correlated": H_inf_GeV * phi_i / phi_min_corr,
            "homogeneous_modes_l_ge_2": 0.0, "random_patch_phase_suppression_l2": supp,
            "heavy_natural_modulus": "m >> H_inf ~ no fluctuations; if m < H_inf it decays to radiation -> curvaton-like, "
                                     "converts to adiabatic, isocurvature erased"}


def hierarchy_threshold() -> Dict[str, float]:
    """Smallest mass ratio mu = m2/m1 for which a light partner (phi_i = M, kappa = 1) survives doc 65, m1 natural."""
    lo, hi = -12.0, 0.0
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if rm.evaluate(10 ** mid * M1_NAT, 1.0, 1.0)["allowed"]:
            hi = mid
        else:
            lo = mid
    return {"mu_min": 10 ** hi, "m2_min_eV": 10 ** hi * M1_NAT}


def report() -> Dict[str, object]:
    return {"hierarchy_threshold": hierarchy_threshold(), "linear": var_linear(), "nonlinear": var_nonlinear(), "parametric": var_parametric(),
            "friction": var_friction(), "spectrum": var_spectrum(),
            "cmb": {"dm_1e-19": cmb_phases(1e-19, 1e-2, 1e10), "dm_1e-3": cmb_phases(1e-3, 1.4e-6, 1e8, 4)},
            "m1_natural_eV": M1_NAT, "tau_to_seconds_natural": to_seconds(1.0)}
