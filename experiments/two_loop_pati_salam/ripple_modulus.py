"""Doc 65: 'stone in a still pond' -- a displaced internal-geometry modulus that rings and settles.

Model
-----
* phi = canonical radion of the magnetized internal surface (d = 2), in units of the reduced Planck mass M.
  Area A = A0 exp(2 sigma), canonical phi = sqrt(d(d+2)/2) M sigma = 2 M sigma.
* Spectral action (Chamseddine-Connes): after the Weyl rescaling to the Einstein frame the overall scale
  modulus has an exactly FLAT tree-level potential (scale invariance).  The mass m_phi therefore is NOT derived;
  it is a free parameter.  The natural stabilized value m ~ Lambda^2/M is used as a benchmark.
* Couplings (per unit phi/M, all multiplied by an overall strength kappa; kappa = 1 is the spectral/KK value):
    1/alpha_U ∝ A  -> delta(1/alpha_i(Lambda)) = (1/alpha_U) phi/M for every gauge group (tree level);
    Delta alpha/alpha (low energy) = -(8/3)(alpha_em/alpha_U) phi/M                 = beta_alpha phi/M;
    Lambda_QCD / M: one-loop transmutation (b3 = 7) + universal -1/2              = beta_p phi/M;
    m_e / M: Yukawa ~ g (spectral relation) -> -1/2 (O(1), model-dependent)        = beta_e phi/M.
* Dynamics: phi'' + 3 H phi' + m^2 phi = 0 through radiation (g_* steps) and matter eras with Planck 2018
  parameters; switch to the exact WKB envelope (amplitude ∝ a^{-3/2}) once m/H > 100.

Everything is linear in phi_i, so one solve per mass suffices.  The texts that inspired this
(the stone in the pond) are inspiration only; the test is the mathematics below.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, List, Optional

import numpy as np
from scipy.integrate import solve_ivp, cumulative_trapezoid
from scipy.interpolate import interp1d
from scipy.optimize import brentq

# ------------------------------------------------------------------ constants (natural units, eV)
M = 2.435e27                    # reduced Planck mass [eV]
HBAR = 6.582119569e-16          # eV s
HBARC = 1.973269804e-7          # eV m
YR = 3.15576e7                  # s
GEV = 1e9
# Planck 2018 (TT,TE,EE+lowE+lensing): h, Omega_m; T0 = 2.7255 K; N_eff = 3.046
h = 0.674
OM = 0.315
T0 = 2.7255 * 8.617333e-5      # eV
H0 = h * 2.13317e-33            # eV
RHO_C = 3 * M * M * H0 * H0
GSTAR0 = 2 * (1 + 7 / 8 * (4 / 11) ** (4 / 3) * 3.046)
GSTARS0 = 2 + 7 / 8 * 2 * 3.046 * 4 / 11
OMEGA_DM_H2 = 0.120
ALPHA_EM = 1 / 137.035999
G_U = 0.531                      # doc 60 unified coupling at Lambda
ALPHA_U = G_U ** 2 / (4 * math.pi)
LAMBDA_GEV = 1.24e15             # doc 60 spectral cutoff

# g_*(T), g_*s(T): standard SM values at a few temperatures (log-interpolated), T in eV
_GT = np.array([1e16, 2e11, 1e10, 2e9, 4e8, 1.5e8, 1e8, 3e7, 1e7, 1e6, 3e5, 1e5, 3e4, 1e-6])
_GS = np.array([106.75, 106.75, 86.25, 75.75, 61.75, 17.25, 14.25, 10.75, 10.75, 10.75, 8.0, 4.5, GSTAR0, GSTAR0])
_GSS = np.array([106.75, 106.75, 86.25, 75.75, 61.75, 17.25, 14.25, 10.75, 10.75, 10.75, 9.0, 5.5, GSTARS0, GSTARS0])


def gstar(T: float) -> float:
    return float(np.interp(math.log(T), np.log(_GT[::-1]), _GS[::-1]))


def gstars(T: float) -> float:
    return float(np.interp(math.log(T), np.log(_GT[::-1]), _GSS[::-1]))


def T_of_a(a: float) -> float:
    T = T0 / a
    for _ in range(6):
        T = T0 / a * (GSTARS0 / gstars(T)) ** (1 / 3)
    return T


def rho_rad(T: float) -> float:
    return math.pi ** 2 / 30 * gstar(T) * T ** 4


def entropy(T: float) -> float:
    return 2 * math.pi ** 2 / 45 * gstars(T) * T ** 3


def H_of_a(a: float) -> float:
    rho = rho_rad(T_of_a(a)) + OM * RHO_C / a ** 3 + (1 - OM - rho_rad(T0) / RHO_C) * RHO_C
    return math.sqrt(rho / (3 * M * M))


@lru_cache(maxsize=1)
def background_table():
    N = np.linspace(-78.0, 0.0, 6001)
    H = np.array([H_of_a(math.exp(n)) for n in N])
    lnH = np.log(H)
    eps = np.gradient(lnH, N)
    t = cumulative_trapezoid(1 / H, N, initial=0.0) + 1 / (2 * H[0])   # radiation era start: t = 1/(2H)
    return N, lnH, eps, t


def H_N(N):
    Ng, lnH, _, _ = background_table()
    return np.exp(np.interp(N, Ng, lnH))


def eps_N(N):
    Ng, _, eps, _ = background_table()
    return np.interp(N, Ng, eps)


def t_N(N):
    Ng, _, _, t = background_table()
    return np.interp(N, Ng, t)


def t0_s() -> float:
    return float(t_N(0.0)) * HBAR


def N_of_z(z):
    return -np.log1p(z)


# ------------------------------------------------------------------ couplings
BETA_ALPHA = -(8 / 3) * ALPHA_EM / ALPHA_U          # Delta alpha/alpha per phi/M
BETA_QCD = -(2 * math.pi / 7) / ALPHA_U             # Delta ln(Lambda_QCD/Lambda) per phi/M
BETA_UNIV = -0.5                                    # Delta ln(m/M) universal (Planck-mass rescaling)
BETA_P = BETA_UNIV + BETA_QCD                       # nucleon mass / M
BETA_E = -0.5                                       # electron mass / M (O(1), model-dependent)
BETA_MU = BETA_P - BETA_E                           # mu = m_p/m_e
BETA_XQ = BETA_E - BETA_P                           # m_q/Lambda_QCD (quark Yukawas scale like m_e)


def couplings() -> Dict[str, float]:
    return {"beta_alpha": BETA_ALPHA, "beta_p": BETA_P, "beta_e": BETA_E, "beta_mu": BETA_MU, "beta_mq_over_LQCD": BETA_XQ,
            "alpha_U": ALPHA_U, "dln_yt": -0.5, "dln_lambda": -1.0,
            "boundary_ratios_yt_over_g_lambda_over_g2": 0.0,
            "note": "per unit phi/M_Pl(reduced); multiply by kappa. y_t and lambda at Lambda move with g (y_t^2, lambda ∝ g^2), "
                    "so the boundary ratios that fix M_t, M_h do not move"}


def spectral_potential_einstein(sigma, f2: float = 1.0, f4: float = 1.0, Lam: float = 1.0):
    """Tree-level spectral action with D -> e^{-sigma} D: Jordan-frame Einstein term ∝ f2 Lam^2 e^{2 sigma},
    cosmological term ∝ f4 Lam^4 e^{4 sigma}.  Einstein-frame potential V_E = V_J / (M_J^2/M^2)^2 is flat."""
    sigma = np.asarray(sigma, float)
    MJ2 = f2 * Lam ** 2 * np.exp(2 * sigma)
    VJ = f4 * Lam ** 4 * np.exp(4 * sigma)
    return VJ / MJ2 ** 2


# ------------------------------------------------------------------ field evolution (phi_i = 1)
@dataclass
class Transfer:
    m: float
    N_sw: Optional[float]            # WKB switch (None: never oscillates fast before today)
    A_sw: float
    sol: object                      # dense ODE solution in N (phi, dphi/dN)
    N0: float

    def phi(self, N):
        N = np.atleast_1d(np.asarray(N, float))
        out = np.empty_like(N)
        for i, n in enumerate(N):
            if n <= self.N0:
                out[i] = 1.0
            elif self.N_sw is None or n <= self.N_sw:
                out[i] = self.sol.sol(n)[0]
            else:  # fast oscillation: return envelope (phase is irrelevant for envelope bounds)
                out[i] = self.A_sw * math.exp(-1.5 * (n - self.N_sw))
        return out

    def envelope(self, N):
        N = np.atleast_1d(np.asarray(N, float))
        out = np.empty_like(N)
        for i, n in enumerate(N):
            if self.N_sw is not None and n > self.N_sw:
                out[i] = self.A_sw * math.exp(-1.5 * (n - self.N_sw))
            elif n <= self.N0:
                out[i] = 1.0
            else:
                y = self.sol.sol(n)
                out[i] = math.hypot(y[0], y[1] * float(H_N(n)) / self.m)
        return out

    @property
    def oscillating_today(self) -> bool:
        return self.N_sw is not None

    def delta(self, z):
        """|phi(z) - phi(today)| (per phi_i): field-difference relevant for measured variations."""
        Nz = N_of_z(np.atleast_1d(z))
        if self.oscillating_today:
            return self.envelope(Nz) + self.envelope(0.0)[0]
        return np.abs(self.phi(Nz) - self.phi(0.0)[0])

    def today(self) -> Dict[str, float]:
        if self.oscillating_today:
            A0 = self.envelope(0.0)[0]
            return {"A0": A0, "phidot_max": self.m * A0, "rho": 0.5 * self.m ** 2 * A0 ** 2}
        y = self.sol.sol(0.0)
        pd = y[1] * H0
        return {"A0": abs(y[0]), "phidot_max": abs(pd), "rho": 0.5 * pd ** 2 + 0.5 * self.m ** 2 * y[0] ** 2}

    def rho_over_s(self) -> float:
        """Energy per entropy after the onset of oscillation (constant), per phi_i^2, in eV (times M^2)."""
        if not self.oscillating_today:
            return float("nan")
        n = self.N_sw
        T = T_of_a(math.exp(n))
        return 0.5 * self.m ** 2 * self.A_sw ** 2 * M ** 2 / entropy(T)


def _rhs(N, y, m):
    H = H_N(N)
    return [y[1], -(3 + eps_N(N)) * y[1] - (m / H) ** 2 * y[0]]


@lru_cache(maxsize=512)
def transfer(m: float, switch: float = 100.0) -> Transfer:
    Ng, lnH, _, _ = background_table()
    r = m / np.exp(lnH)
    # start where m/H = 1e-3 (field frozen at phi_i), or at the grid start
    idx = np.where(r > 1e-3)[0]
    N0 = float(Ng[idx[0]]) if len(idx) else -12.0
    N0 = max(N0, float(Ng[0]))
    isw = np.where(r > switch)[0]
    N_end = float(Ng[isw[0]]) if len(isw) else 0.0
    if N_end <= N0:
        N_end = N0 + 1e-6
    sol = solve_ivp(_rhs, (N0, N_end), [1.0, 0.0], args=(m,), dense_output=True, rtol=1e-8, atol=1e-11,
                    method="DOP853", max_step=0.02)
    if len(isw):
        y = sol.y[:, -1]
        A = math.hypot(y[0], y[1] * float(H_N(N_end)) / m)
        return Transfer(m, N_end, A, sol, N0)
    return Transfer(m, None, 1.0, sol, N0)


# ------------------------------------------------------------------ data (representative 2-sigma limits; see doc 65)
LIMITS = {
    # name: (z, quantity, limit, integration time [s] over which a fast oscillation averages)
    "BBN alpha": (4.0e8, "alpha", 2e-2, 1.0),
    "BBN m_q/L_QCD": (4.0e8, "mq", 2e-2, 1.0),
    "BBN G m_p^2": (4.0e8, "p", 5e-2, 1.0),
    "CMB alpha": (1100.0, "alpha", 5e-3, 4e4 * YR),
    "CMB m_e": (1100.0, "e", 1.4e-2, 4e4 * YR),
    "QSO alpha z=1-4": (2.0, "alpha", 3e-6, 0.0),
    "QSO mu z=0.89": (0.89, "mu", 3e-7, 0.0),
    "Oklo alpha": (0.14, "alpha", 2e-8, 1e5 * YR),
}
CLOCK_DRIFT = 5e-19 / YR            # |alpha_dot/alpha| [1/s] (Yb+ E3/E2 vs Cs, 2023), 2 sigma
CLOCK_OSC = 1e-17                   # representative oscillation-amplitude limit, periods 1 h .. 10 yr
MICROSCOPE_ETA = 5.5e-15
EOT_WASH_ETA = 3.6e-13


def _beta(q: str) -> float:
    return {"alpha": BETA_ALPHA, "mq": BETA_XQ, "p": BETA_P, "e": BETA_E, "mu": BETA_MU}[q]


def decay_time_s(m: float, kappa: float) -> float:
    """Gravitational-strength decay (to gauge bosons), Gamma ~ kappa^2 m^3 / (4 pi M^2); O(1) uncertain."""
    if kappa == 0:
        return float("inf")
    G = kappa ** 2 * m ** 3 / (4 * math.pi * M ** 2)
    return HBAR / G


def fifth_force(m: float, kappa: float) -> Dict[str, object]:
    """Dilaton-charge model: Q_A = beta_p + beta_alpha f_EM + (beta_e - beta_p) f_e (Ti vs Pt; Earth ~ Fe)."""
    def fem(Z, A):
        return 0.71 * Z * (Z - 1) / A ** (1 / 3) / (931.494 * A)
    def Q(Z, A):
        return BETA_P + BETA_ALPHA * fem(Z, A) + (BETA_E - BETA_P) * (Z / A) * 5.446e-4
    QE, dQ = Q(26, 56), abs(Q(22, 48) - Q(78, 195))
    eta = 2 * kappa ** 2 * abs(QE) * dQ
    alpha5 = 2 * kappa ** 2 * QE ** 2
    lam = HBARC / m if m > 0 else float("inf")
    if lam > 6.4e6:
        ok, test, lim = eta < MICROSCOPE_ETA, "MICROSCOPE eta", MICROSCOPE_ETA
    elif lam > 1.0:
        ok, test, lim = (eta < EOT_WASH_ETA and alpha5 < 1e-3), "Eot-Wash EP + inverse-square", EOT_WASH_ETA
    elif lam > 5e-5:
        amax = 10 ** (-3 * (math.log10(lam) - math.log10(5e-5)) / (math.log10(1.0) - math.log10(5e-5)))
        ok, test, lim = alpha5 < amax, "inverse-square (sub-mm..m)", amax
    else:
        ok, test, lim = True, "range < 50 um: unconstrained", None
    return {"range_m": lam, "eta": eta, "alpha5": alpha5, "test": test, "limit": lim, "ok": bool(ok)}


def evaluate(m: float, phi_i: float, kappa: float = 1.0) -> Dict[str, object]:
    """All constraints for mass m [eV], initial displacement phi_i [M], coupling strength kappa."""
    tr = transfer(m)
    tau = decay_time_s(m, kappa)
    out: Dict[str, object] = {"m_eV": m, "phi_i": phi_i, "kappa": kappa, "tau_s": tau, "checks": {}}
    ch = out["checks"]

    # --- energy density / moduli problem
    tz = t0_s()
    dominated, TRH = False, None
    if tr.oscillating_today or tr.N_sw is not None:
        rs = tr.rho_over_s() * phi_i ** 2                        # eV
        out["rho_over_s_GeV"] = rs / GEV
        # temperature at decay (radiation era): H = 1/(2t)
        Hdec = HBAR / (2 * tau) if tau < float("inf") else 0.0
        # does phi dominate before decay?  rho_phi/rho_rad = (3/4) (rho/s) / T
        Tdec = None
        if Hdec > 0 and tau < 1e12:
            Tdec = brentq(lambda lt: math.log(math.sqrt(rho_rad(math.exp(lt)) / 3) / M) - math.log(Hdec), -60, 90)
            Tdec = math.exp(Tdec)
            dominated = 0.75 * rs / Tdec > 1
            if dominated:
                TRH = (90 / (math.pi ** 2 * 10.75)) ** 0.25 * math.sqrt(HBAR / tau * M)
        out["dominates_before_decay"] = bool(dominated)
        out["T_RH_MeV"] = None if TRH is None else TRH / 1e6
        if tau < 0.1 and (not dominated or (TRH is not None and TRH > 5e6)):
            ch["moduli problem"] = (True, "decays before BBN" + (f", T_RH = {TRH/1e6:.3g} MeV" if TRH else ""))
        elif dominated:
            ch["moduli problem"] = (False, f"dominates and reheats to {TRH/1e6:.3g} MeV < 5 MeV" if TRH else "dominates")
        elif tau < 1e2:
            ch["moduli problem"] = (rs / GEV < 1e-9, "late decay 0.1-100 s (hadronic BBN), rho/s < 1e-9 GeV")
        elif tau < 1e12:
            ch["moduli problem"] = (rs / GEV < 1e-14, "late decay 1e2-1e12 s (BBN photodissociation), rho/s < 1e-14 GeV")
        elif tau < tz:
            ch["moduli problem"] = (rs / GEV < 1e-15, "decay before today (CMB/diffuse photons), rho/s < 1e-15 GeV")
    if tau >= tz or tr.N_sw is None:
        rho0 = tr.today()["rho"] * phi_i ** 2 * M ** 2
        Oh2 = rho0 / RHO_C * h * h
        out["Omega_h2_today"] = Oh2
        ok = Oh2 <= OMEGA_DM_H2 * 1.02
        note = "Omega_phi h^2 <= 0.12"
        if ok and Oh2 > 0.012 and tr.oscillating_today and m < 2e-20:
            ok, note = False, "fuzzy DM > 10% of DM with m < 2e-20 eV (Lyman-alpha)"
        if ok and tr.oscillating_today and tau < 1e26 and Oh2 > 1e-6 and m > 1e3:
            ok, note = False, "decaying relic, tau < 1e26 s (X/gamma lines)"
        ch["energy density"] = (bool(ok), note)

    # --- variations of constants (field must still exist at that epoch: amplitude e^{-t/2tau})
    def alive(z):
        return math.exp(-float(t_N(N_of_z(z))) * HBAR / (2 * tau)) if tau < float("inf") else 1.0
    for name, (z, q, lim, Tint) in LIMITS.items():
        d = float(tr.delta(z)[0]) * phi_i * alive(z)
        avg = 1.0
        if Tint > 0 and m * Tint / HBAR > 2 * math.pi:
            avg = 1.0 / (m * Tint / HBAR)                      # linear signal averages over the measurement
        val = abs(kappa * _beta(q)) * d * avg
        ch[name] = (val < lim, f"|{q}| = {val:.3g} vs {lim:g}")
    today = tr.today()
    a_today = alive(0.0)
    per = 2 * math.pi * HBAR / m
    if per > 10 * YR:
        rate = abs(kappa * BETA_ALPHA) * today["phidot_max"] * phi_i * a_today / HBAR
        ch["clocks"] = (rate < CLOCK_DRIFT, f"alpha_dot/alpha = {rate*YR:.3g}/yr vs {CLOCK_DRIFT*YR:g}/yr")
    elif per > 3600:
        amp = abs(kappa * BETA_ALPHA) * today["A0"] * phi_i * a_today
        ch["clocks"] = (amp < CLOCK_OSC, f"oscillation amplitude {amp:.3g} vs {CLOCK_OSC:g}")
    ff = fifth_force(m, kappa)
    ch["fifth force / EP"] = (ff["ok"], f"{ff['test']}: eta = {ff['eta']:.3g}, alpha5 = {ff['alpha5']:.3g}")
    out["allowed"] = all(v[0] for v in ch.values())
    out["failed"] = [k for k, v in ch.items() if not v[0]]
    return out


# ------------------------------------------------------------------ scans
MASSES = np.logspace(-33.5, 22, 112)
PHIS = np.logspace(-14, 0, 57)


def allowed_map(kappa: float = 1.0, masses=MASSES, phis=PHIS) -> np.ndarray:
    A = np.zeros((len(phis), len(masses)), bool)
    for j, m in enumerate(masses):
        for i, p in enumerate(phis):
            A[i, j] = evaluate(float(m), float(p), kappa)["allowed"]
    return A


def max_kappa(m: float, phi_i: float = 1.0) -> float:
    """Largest kappa in [1e-30, 1] allowed (bisection in log kappa; 0 if even 1e-30 fails)."""
    lo, hi = -30.0, 0.0
    if evaluate(m, phi_i, 10 ** hi)["allowed"]:
        return 1.0
    if not evaluate(m, phi_i, 10 ** lo)["allowed"]:
        return 0.0
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if evaluate(m, phi_i, 10 ** mid)["allowed"]:
            lo = mid
        else:
            hi = mid
    return 10 ** lo


def max_phi(m: float, kappa: float = 1.0) -> float:
    lo, hi = -30.0, 0.0
    if evaluate(m, 1.0, kappa)["allowed"]:
        return 1.0
    if not evaluate(m, 10 ** lo, kappa)["allowed"]:
        return 0.0
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if evaluate(m, 10 ** mid, kappa)["allowed"]:
            lo = mid
        else:
            hi = mid
    return 10 ** lo


def natural_benchmark() -> Dict[str, object]:
    m = (LAMBDA_GEV * GEV) ** 2 / M
    r = evaluate(m, 1.0, 1.0)
    return {"m_eV": m, "m_GeV": m / GEV, **{k: r[k] for k in ("tau_s", "allowed", "failed", "dominates_before_decay", "T_RH_MeV")}}


def massless_spectral() -> Dict[str, object]:
    """Flat spectral-action potential: m -> H0-ish; fifth force with kappa = 1."""
    ff = fifth_force(1e-40, 1.0)
    return {"eta": ff["eta"], "alpha5": ff["alpha5"], "MICROSCOPE": MICROSCOPE_ETA, "kappa_max": math.sqrt(MICROSCOPE_ETA / ff["eta"])}


def dm_benchmark(m: float = 1e-19) -> Dict[str, object]:
    """Field is all of DM: phi_i fixed by Omega h^2 = 0.12; largest kappa allowed."""
    tr = transfer(m)
    rho1 = tr.today()["rho"] * M ** 2
    phi_i = math.sqrt(OMEGA_DM_H2 / (rho1 / RHO_C * h * h))
    k = max_kappa(m, phi_i)
    tr_z = {z: float(tr.envelope(N_of_z(z))[0]) * phi_i for z in (0.0, 0.14, 2.0, 1100.0)}
    return {"m_eV": m, "phi_i_for_all_DM": phi_i, "kappa_max": k, "amplitude_phi_over_M": tr_z,
            "dalpha_alpha_amp_today_at_kappa_max": abs(k * BETA_ALPHA) * tr_z[0.0],
            "period_s": 2 * math.pi * HBAR / m}


# ------------------------------------------------------------------ top / Higgs
def top_higgs() -> Dict[str, object]:
    """A settled minimum sigma_min rescales the internal scale uniformly: the spectral boundary relations
    y_t^2 = 4 g^2 (..)/a, lambda = 4 g^2 b/a^2 are ratios of traces of D_F and do not depend on it.
    The only lever is where the boundary applies relative to the gauge-meeting scale (mu_B/Lambda)."""
    import top_yukawa_search as ts
    base = ts.predict(ts.Cand())
    scan = {}
    for f in (0.1, 0.3, 1.0, 3.0):
        r = ts.predict(ts.Cand(mu_B_over_Lambda=f))
        if r.get("ok", True) and "Mt" in r:
            scan[str(f)] = {"Mt": r["Mt"], "Mh": r["Mh"]}
    return {"settled_minimum": {"Mt": base["Mt"], "Mh": base["Mh"],
                                "reason": "sigma_min cancels in trace ratios; its value is fixed by today's measured alpha"},
            "boundary_scale_shift_scan": scan,
            "extra_parameters": {"m_phi": 1, "phi_i": 1, "kappa": 1, "sigma_min": "fixed by data"}}


def report(fast: bool = False) -> Dict[str, object]:
    out = {"couplings": couplings(), "natural_benchmark": natural_benchmark(), "massless_spectral": massless_spectral(),
           "dm_benchmarks": {str(m): dm_benchmark(m) for m in (1e-19, 1e-12, 1e-3)},
           "top_higgs": top_higgs(), "t0_Gyr": t0_s() / YR / 1e9}
    ms = np.logspace(-33, 22, 23 if fast else 56)
    out["max_phi_kappa1"] = {f"{m:.3g}": max_phi(float(m), 1.0) for m in ms}
    out["max_kappa_phi1"] = {f"{m:.3g}": max_kappa(float(m), 1.0) for m in ms}
    return out
