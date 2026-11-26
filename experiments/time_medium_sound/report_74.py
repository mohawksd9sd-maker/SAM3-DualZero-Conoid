"""Doc 74 driver (ideas: Shawn Dykes).  python report_74.py [toy tones chirp lowell focus rings]
Writes results_doc74.json (merged per section)."""
from __future__ import annotations

import json
import math
import os
import sys
import time

import numpy as np

import sound_banks as sb
tm = sb.tm

HERE = sb.HERE
OUT = os.environ.get("DOC74_OUT", os.path.join(HERE, "results_doc74.json"))
FC_CACHE = os.path.join(HERE, "fastcls_doc74.npz")   # rebuildable cache (not committed)


def jload():
    return json.load(open(OUT)) if os.path.exists(OUT) else {}


def jsave(d):
    json.dump(d, open(OUT, "w"), indent=1, default=float)


# ------------------------------------------------------------------ S1a toy model
def toy(R):
    out = {"sphere": [], "cube": []}
    for kR in (1.0, 2.0, 3.0, 3.1, 4.4934, 6.0, 9.0):
        x, a, gain = sb.sphere_inphase_solution(kR, gamma=0.0 if abs(math.sin(kR)) > 1e-3 else 0.01)
        out["sphere"].append({"kR": kR, "centre_over_edge": gain})
    for kL in (2.0, 3.7, 5.0):
        g, Phi = sb.cube_inphase_fd(kL, N=41, gamma=0.02)
        c = len(g) // 2
        gain = float(abs(Phi[c, c, c]))
        cen = sb.sky_multipoles_from_field(g, Phi, (0.0, 0.0, 0.0), 0.6)
        off = sb.sky_multipoles_from_field(g, Phi, (0.25, 0.1, 0.0), 0.6)
        out["cube"].append({"kL": kL, "centre_over_edge": gain,
                            "observer_at_focus_frac_power_by_ell": cen["re"],
                            "observer_offcentre_frac_power_by_ell": off["re"]})
    out["sphere_offcentre_frac_by_ell"] = {f"kd={kd},kr={kr}": sb.offcentre_sphere_multipoles(kd, kr)
                                          for kd, kr in ((0.5, 20.0), (2.0, 20.0), (5.0, 40.0))}
    R["toy"] = out


# ------------------------------------------------------------------ FastCls (cached K)
class FC:
    def __init__(self):
        if os.path.exists(FC_CACHE):
            z = np.load(FC_CACHE)
            self.K, self.q, self.L, self.clpp, self.P0, self.D0 = (z[k] for k in ("K", "q", "L", "clpp", "P0", "D0"))
        else:
            f = tm.FastCls()
            self.K, self.q, self.L, self.clpp, self.P0, self.D0 = f.K, f.q, f.L, f.clpp, f.P0, f.D0
            np.savez(FC_CACHE, K=f.K, q=f.q, L=f.L, clpp=f.clpp, P0=f.P0, D0=f.D0)

    def lensed(self, cl_raw):
        from camb import correlations
        arr = np.zeros((2801, 4))
        L = self.L
        arr[L, 0] = cl_raw * L * (L + 1) / (2 * np.pi)
        return correlations.lensed_cls(arr, self.clpp)[:, 0]

    def D(self, P):
        return self.lensed(self.K @ P)


def chi2_fit(cols, D, sig):
    X = np.stack(cols, 1) / sig[:, None]
    c, *_ = np.linalg.lstsq(X, D / sig, rcond=None)
    r = D / sig - X @ c
    return float(r @ r), c


# ------------------------------------------------------------------ S2 tones
def tones(R):
    fc = FC()
    ell, D, sig = tm.planck_tt()
    q = fc.q
    dq = float(np.median(np.diff(q)))
    D0 = fc.D(fc.P0)[ell]
    Dn = fc.D(fc.P0 * np.log(q / tm.KSTAR))[ell]
    chi_lcdm, _ = chi2_fit([D0, Dn], D, sig)
    out = {"n_ell": int(len(ell)), "chi2_LCDM_amp_tilt": chi_lcdm, "dq_Mpc^-1": dq}
    # (a) a single pure tone: primordial line, Gaussian in ln k (width w), amplitude free
    lines = []
    for w in (0.02, 0.05, 0.1, 0.3, 1.0, 3.0):
        best = None
        for k0 in np.logspace(math.log10(0.002), math.log10(0.25), 90):
            weff = max(w, 3 * dq / k0)
            P = sb.gauss_lnk(q, k0, weff)
            c2, c = chi2_fit([fc.D(P)[ell]], D, sig)
            if best is None or c2 < best[0]:
                best = (c2, k0, weff)
        lines.append({"w_lnk": w, "best_k0": best[1], "w_eff": best[2], "chi2": best[0], "dchi2_vs_LCDM": best[0] - chi_lcdm})
    out["single_tone_line"] = lines
    # BAO-matched tones
    rd = 147.09  # Mpc, Planck 2018 VI (TT,TE,EE+lowE+lensing)
    out["bao_tones"] = []
    for name, k0 in (("k=2pi/r_d", 2 * math.pi / rd), ("k=pi/r_d", math.pi / rd)):
        P = sb.gauss_lnk(q, k0, max(0.02, 3 * dq / k0))
        c2, _ = chi2_fit([fc.D(P)[ell]], D, sig)
        out["bao_tones"].append({"tone": name, "k0": k0, "chi2": c2, "dchi2_vs_LCDM": c2 - chi_lcdm})
    # (b) tone + overtones: harmonic comb at n k0 (linear width frac*k0), smooth Planck envelope, amp free
    combs = []
    for frac in (0.1, 0.2, 0.35):
        for k0 in np.logspace(math.log10(4e-4), math.log10(0.05), 60):
            sk = max(frac * k0, 2 * dq)
            n = np.arange(1, int(0.45 / k0) + 2)
            P = np.zeros_like(q)
            for nn in n:
                P += np.exp(-0.5 * ((q - nn * k0) / sk) ** 2)
            P = fc.P0 * P / np.mean(P[(q > 0.01) & (q < 0.2)])
            c2, _ = chi2_fit([fc.D(P)[ell], fc.D(P * np.log(q / tm.KSTAR))[ell]], D, sig)
            combs.append({"frac": frac, "k0": float(k0), "sigma_k": sk, "dchi2_vs_LCDM": c2 - chi_lcdm})
    out["harmonic_comb"] = combs
    # largest fundamental allowed (dchi2 < 9 and < 25) per width
    out["comb_kmax_allowed"] = {}
    for frac in (0.1, 0.2, 0.35):
        rows = [c for c in combs if c["frac"] == frac]
        for thr in (9, 25):
            ok = [c["k0"] for c in rows if c["dchi2_vs_LCDM"] < thr]
            out["comb_kmax_allowed"][f"frac={frac},dchi2<{thr}"] = max(ok) if ok else None
    # (c) a sharp tone on top of LCDM: localized bump P0 (1 + B exp(-ln^2(k/k0)/2w^2)), 95% limit on B
    bumps = []
    for w in (0.03, 0.1, 0.3):
        for k0 in np.logspace(math.log10(0.003), math.log10(0.2), 40):
            weff = max(w, 3 * dq / k0)
            T = fc.D(fc.P0 * sb.gauss_lnk(q, k0, weff))[ell]
            X = np.stack([D0, Dn, T], 1) / sig[:, None]
            c, *_ = np.linalg.lstsq(X, D / sig, rcond=None)
            cov = np.linalg.inv(X.T @ X)
            sB = math.sqrt(cov[2, 2])
            bumps.append({"w": w, "k0": float(k0), "B_hat": float(c[2]), "sigma_B": sB, "B95": abs(float(c[2])) + 1.96 * sB,
                          "dchi2": float((c[2] / sB) ** 2)})
    out["bump_limits"] = bumps
    out["bump_max_dchi2"] = max(b["dchi2"] for b in bumps)
    R["tones"] = out


# ------------------------------------------------------------------ S3 chirps
def chirp(R):
    fc = FC()
    ell, D, sig = tm.planck_tt()
    q = fc.q
    D0 = fc.D(fc.P0)[ell]
    Dn = fc.D(fc.P0 * np.log(q / tm.KSTAR))[ell]
    chi_lcdm, _ = chi2_fit([D0, Dn], D, sig)
    out = {"families": []}
    t = np.linspace(1e-3, 50, 400000)
    fams = {
        "linear sweep w = w0 + b t, A const": (1 + 3.0 * t, np.ones_like(t)),
        "power law w ~ t^2": (t ** 2, np.ones_like(t)),
        "power law w ~ t^-28.5 (fitted)": (t[::-1] ** -28.5 / (t[-1] ** -28.5), np.ones_like(t)),
        "exponential w = e^{t}, A const": (np.exp(0.3 * t), np.ones_like(t)),
        "exponential, rate drifting 3.5%/e-fold": None,
    }
    for name, val in fams.items():
        if val is None:
            # omega = exp(N), dN/dt = H(N), H = H0 exp(eps N): power per ln omega ~ 1/H ~ exp(-eps N) -> n_s - 1 = -eps
            N = np.linspace(0, 15, 20000)
            om = np.exp(N)
            Hn = np.exp(0.0351 * N)
            tt = np.concatenate([[0], np.cumsum(np.diff(N) / Hn[1:])])
            w, P = sb.chirp_spectrum_stationary_phase(tt, om, np.ones_like(om))
        else:
            om, A = val
            o = np.argsort(om)
            w, P = sb.chirp_spectrum_stationary_phase(t[o] if "28.5" not in name else t, om[o] if "28.5" not in name else om, A)
            o = np.argsort(w); w, P = w[o], P[o]
        # scale-free families: map omega -> k with the observable window at the middle of the sweep
        k = w / np.exp(np.mean(np.log(w))) * 0.05
        fit = sb.ns_running_fit(k, P / np.interp(0.05, k, P))
        out["families"].append({"family": name, **fit})
    # spoken phrase (parametric model)
    t, s, f0, env = sb.speech_phrase()
    fs = 16000
    S = np.abs(np.fft.rfft(s * np.hanning(len(s)))) ** 2
    f = np.fft.rfftfreq(len(s), 1 / fs)
    sel = f > 20
    f, S = f[sel], S[sel] * f[sel]          # per ln f
    best = None
    rows = []
    for f_at_kstar in np.logspace(math.log10(30), math.log10(3000), 61):   # which audio frequency maps to k = 0.05
        Pk = np.interp(np.log(q / 0.05 * f_at_kstar), np.log(f), S, left=S[0], right=S[-1])
        Pk = np.maximum(Pk, 1e-12 * S.max())
        c2, _ = chi2_fit([fc.D(Pk)[ell]], D, sig)
        fit = sb.ns_running_fit(q, Pk)
        rows.append({"f_audio_at_k*": float(f_at_kstar), "dchi2_vs_LCDM": c2 - chi_lcdm, **fit})
        if best is None or c2 < best[0]:
            best = (c2, f_at_kstar, fit)
    out["speech_spectral_map"] = {"best_f_audio_at_kstar_Hz": best[1], "best_dchi2_vs_LCDM": best[0] - chi_lcdm,
                                  "ns_running_at_best": best[2], "scan": rows}
    # envelope map: time in the phrase -> ln k (earlier = larger scales), phrase spans N e-folds of k
    from scipy.ndimage import uniform_filter1d
    E = uniform_filter1d(s ** 2, int(0.02 * fs))
    E = E / E[env > 0.5].mean()
    rows = []
    for Nef in (0.5, 2.0, 6.0, 12.0, 25.0):
        bestN = None
        for lnk_start in np.linspace(math.log(1e-4) - Nef, math.log(0.3), 40):
            u = (np.log(q) - lnk_start) / Nef * t[-1]
            mod = np.interp(u, t, E, left=1.0, right=1.0)
            mod = np.maximum(mod, 1e-3)
            P = fc.P0 * mod
            c2, _ = chi2_fit([fc.D(P)[ell], fc.D(P * np.log(q / tm.KSTAR))[ell]], D, sig)
            if bestN is None or c2 < bestN[0]:
                bestN = (c2, lnk_start)
        rows.append({"efolds_spanned": Nef, "best_k_start": math.exp(bestN[1]), "best_dchi2_vs_LCDM": bestN[0] - chi_lcdm})
    out["speech_envelope_map"] = rows
    out["phrase_model"] = {"duration_s": 1.05, "F0_range_Hz": [float(np.nanmin(f0)), float(np.nanmax(f0))]}
    R["chirp"] = out


SECTIONS = {"toy": toy, "tones": tones, "chirp": chirp}



def chirp_lee(R, nsim=2000, seed=7404):
    """Look-elsewhere calibration of the speech-envelope scan: best Delta chi^2 over the same 200 placements for
    Gaussian realisations of the LCDM (amp+tilt) fit, same diagonal likelihood."""
    fc = FC()
    ell, D, sig = tm.planck_tt()
    q = fc.q
    D0 = fc.D(fc.P0)[ell]
    Dn = fc.D(fc.P0 * np.log(q / tm.KSTAR))[ell]
    _, c0 = chi2_fit([D0, Dn], D, sig)
    Dfid = c0[0] * D0 + c0[1] * Dn
    from scipy.ndimage import uniform_filter1d
    t, s, f0, env = sb.speech_phrase()
    E = uniform_filter1d(s ** 2, int(0.02 * 16000)); E = E / E[env > 0.5].mean()
    bases = []
    meta = []
    for Nef in (0.5, 2.0, 6.0, 12.0, 25.0):
        for lnk_start in np.linspace(math.log(1e-4) - Nef, math.log(0.3), 40):
            u = (np.log(q) - lnk_start) / Nef * t[-1]
            mod = np.maximum(np.interp(u, t, E, left=1.0, right=1.0), 1e-3)
            P = fc.P0 * mod
            X = np.stack([fc.D(P)[ell], fc.D(P * np.log(q / tm.KSTAR))[ell]], 1) / sig[:, None]
            Q, _ = np.linalg.qr(X)
            bases.append(Q); meta.append((Nef, math.exp(lnk_start)))
    X0 = np.stack([D0, Dn], 1) / sig[:, None]
    Q0, _ = np.linalg.qr(X0)
    rng = np.random.default_rng(seed)
    def best_dchi(r):
        chi0 = r @ r - np.sum((Q0.T @ r) ** 2, axis=0)
        return max(float(chi0 - (r @ r - np.sum((Q.T @ r) ** 2))) for Q in bases) if r.ndim == 1 else None
    r_data = D / sig
    chi0 = r_data @ r_data - np.sum((Q0.T @ r_data) ** 2)
    dd = [chi0 - (r_data @ r_data - np.sum((Q.T @ r_data) ** 2)) for Q in bases]
    i = int(np.argmax(dd))
    Rs = (Dfid / sig)[:, None] + rng.standard_normal((len(sig), nsim))
    c0s = np.sum(Rs * Rs, 0) - np.sum((Q0.T @ Rs) ** 2, 0)
    best = np.full(nsim, -np.inf)
    for Q in bases:
        best = np.maximum(best, c0s - (np.sum(Rs * Rs, 0) - np.sum((Q.T @ Rs) ** 2, 0)))
    R.setdefault("chirp", {})["speech_envelope_lee"] = {
        "data_best_improvement": float(dd[i]), "best_efolds": meta[i][0], "best_k_start": meta[i][1],
        "p_global": float(np.mean(best >= dd[i])), "sims_median": float(np.median(best)),
        "sims_95": float(np.quantile(best, 0.95)), "nsim": nsim}


SECTIONS["chirp_lee"] = chirp_lee




def chirp_lee_exact(R, nsim=2000, seed=7405, fsky=0.86, lsplit=30):
    """Robustness: same scan, but l < 30 uses the exact full-sky-like (Wishart) likelihood
    -2lnL = nu [Dhat/D + ln(D/Dhat) - 1], nu = (2l+1) fsky, and low-l sims are chi^2_nu/nu draws.
    Nuisance (amp, tilt) fitted on l >= 30 (Gaussian) only, then held fixed."""
    fc = FC()
    ell, D, sig = tm.planck_tt()
    q = fc.q
    hi = ell >= lsplit; lo = ~hi
    nu = (2 * ell[lo] + 1) * fsky
    def model_D(P):
        A, B = fc.D(P)[ell], fc.D(P * np.log(q / tm.KSTAR))[ell]
        return A, B
    def chi2_total(A, B, Dd):
        X = np.stack([A[hi], B[hi]], 1) / sig[hi, None]
        c, *_ = np.linalg.lstsq(X, Dd[hi] / sig[hi], rcond=None)
        r = Dd[hi] / sig[hi] - X @ c
        M = c[0] * A[lo] + c[1] * B[lo]
        x = Dd[lo] / M
        v = float(r @ r + np.sum(nu * (x - np.log(np.abs(x)) - 1))) if np.all(x > 0) else float("inf")
        return v
    A0, B0 = model_D(fc.P0)
    from scipy.ndimage import uniform_filter1d
    t, s, f0, env = sb.speech_phrase()
    E = uniform_filter1d(s ** 2, int(0.02 * 16000)); E = E / E[env > 0.5].mean()
    mods = []
    for Nef in (0.5, 2.0, 6.0, 12.0, 25.0):
        for lnk_start in np.linspace(math.log(1e-4) - Nef, math.log(0.3), 40):
            u = (np.log(q) - lnk_start) / Nef * t[-1]
            mod = np.maximum(np.interp(u, t, E, left=1.0, right=1.0), 1e-3)
            mods.append(((Nef, math.exp(lnk_start)),) + model_D(fc.P0 * mod))
    c_data0 = chi2_total(A0, B0, D)
    dd = [c_data0 - chi2_total(a, b, D) for _, a, b in mods]
    i = int(np.argmax(dd))
    X = np.stack([A0[hi], B0[hi]], 1) / sig[hi, None]
    c, *_ = np.linalg.lstsq(X, D[hi] / sig[hi], rcond=None)
    Dfid = c[0] * A0 + c[1] * B0
    rng = np.random.default_rng(seed)
    best = []
    for k in range(nsim):
        Ds = Dfid.copy()
        Ds[hi] = Dfid[hi] + sig[hi] * rng.standard_normal(hi.sum())
        Ds[lo] = Dfid[lo] * rng.chisquare(nu) / nu
        c0 = chi2_total(A0, B0, Ds)
        best.append(max(c0 - chi2_total(a, b, Ds) for _, a, b in mods))
    best = np.array(best)
    R.setdefault("chirp", {})["speech_envelope_lee_exact_lowl"] = {
        "fsky": fsky, "data_best_improvement": float(dd[i]), "best": list(mods[i][0]),
        "p_global": float(np.mean(best >= dd[i])), "sims_median": float(np.median(best)),
        "sims_95": float(np.quantile(best, 0.95)), "nsim": nsim}


SECTIONS["chirp_lee_exact"] = chirp_lee_exact


if __name__ == "__main__":
    import importlib
    try:
        import lowell_focus_rings as lfr
        SECTIONS.update({"lowell": lfr.lowell, "focus": lfr.focus, "rings": lfr.rings, "rings_obs": lfr.rings_obs})
    except ImportError:
        pass
    R = jload()
    for sec in sys.argv[1:] or list(SECTIONS):
        t0 = time.time()
        SECTIONS[sec](R)
        R.setdefault("_timing_s", {})[sec] = time.time() - t0
        jsave(R)
        print(sec, "done", round(time.time() - t0, 1), "s", flush=True)
