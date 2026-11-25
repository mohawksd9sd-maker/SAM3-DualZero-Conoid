"""Doc 71 driver: writes results_doc71.json; --figure makes the figure."""
from __future__ import annotations

import json
import math
import os
import sys
import time

import numpy as np

import time_medium as tm

HERE = tm.HERE
OUT = os.path.join(HERE, "results_doc71.json")
TMPL = os.path.join(HERE, "templates_doc71.npz")   # cached CAMB templates (rebuildable, not committed)
FIG = os.path.join(HERE, "fig_doc71_time_medium.png")
FIG_DOC = os.path.join(HERE, "..", "..", "docs", "hardening", "figures", "71_time_medium.png")
OMEGAS = {"lin": np.arange(1.0, 126.0, 0.15), "log": np.arange(1.0, 126.0, 0.10)}

def build_templates():
    fc = tm.FastCls()
    ell = tm.planck_tt()[0]
    out = {}
    for kind, oms in OMEGAS.items():
        T = []
        for w in oms:
            c = fc.response(tm.feature(kind, w, 0.0))
            sn = fc.response(tm.feature(kind, w, -math.pi / 2))
            T.append(np.stack([c[ell], sn[ell]]))
        out[kind] = np.array(T)
    # nuisance: amplitude (D0) and tilt (response to ln(k/k*) * dns)
    dns = fc.response(lambda k: np.log(k / tm.KSTAR))
    np.savez(TMPL, lin=out["lin"], log=out["log"], D0=fc.D0[ell], dns=dns[ell], ell=ell)


def cmb(res_json):
    if not os.path.exists(TMPL):
        build_templates()
    z = np.load(TMPL)
    ell, D, sig = tm.planck_tt()
    base = [z["D0"], z["dns"]]
    out = {}
    for kind in ("lin", "log"):
        dchi, amp, chi0 = tm.scan_chi2(D, sig, base, z[kind])
        i = int(np.argmax(dchi))
        sims = tm.lee_sims(sig, base, z[kind], nsim=2000)
        p_glob = float(np.mean(sims >= dchi[i]))
        A = math.hypot(*amp[i])
        out[kind] = {"omega": OMEGAS[kind].tolist(), "dchi2": dchi.tolist(), "best_omega": float(OMEGAS[kind][i]),
                     "best_log10_omega": math.log10(OMEGAS[kind][i]), "best_dchi2": float(dchi[i]),
                     "best_amplitude": A, "best_phase": math.atan2(-amp[i][1], amp[i][0]),
                     "p_local": float(math.exp(-dchi[i] / 2)), "p_global": p_glob,
                     "sims_max_dchi2_median": float(np.median(sims)), "sims_max_dchi2_95": float(np.quantile(sims, 0.95)),
                     "chi2_null": chi0, "n_ell": int(len(ell)),
                     "amp_95_upper_typical": float(np.quantile([math.hypot(*a) for a in amp], 0.5))}
        if kind == "lin":
            out[kind]["tau_b_Mpc"] = float(OMEGAS[kind][i] / (2 * tm.KSTAR))
    res_json["cmb"] = out


def rings(res_json, nsim=200, seed=7171):
    import healpy as hp
    nside = 128
    m = hp.read_map(os.path.join(HERE, "data", "wmap_ilc_9yr_v5.fits"), verbose=False) if False else \
        hp.read_map(os.path.join(HERE, "data", "wmap_ilc_9yr_v5.fits"))
    mask = hp.read_map(os.path.join(HERE, "data", "wmap_temperature_kq85_analysis_mask_r9_9yr_v5.fits"))
    mlo = hp.ud_grade(m, nside) * 1e3                      # mK -> uK
    mk = (hp.ud_grade(mask, nside) > 0.9).astype(float)
    radii, geo = tm.ring_geometry(nside, mk)
    # remove monopole/dipole outside the mask, as for the sims
    mlo = hp.remove_dipole(np.where(mk > 0, mlo, hp.UNSEEN), verbose=False) if False else \
        hp.remove_dipole(np.where(mk > 0, mlo, hp.UNSEEN))
    S = tm.ring_sigmas(mlo, radii, geo)
    data = tm.ring_stats(S)
    th = np.loadtxt(os.path.join(tm.PLANCK, "COM_PowerSpect_CMB-base-plikHM-TTTEEE-lowl-lowE-lensing-minimum-theory_R3.01.txt"))
    obs = np.loadtxt(os.path.join(tm.PLANCK, "COM_PowerSpect_CMB-TT-full_R3.01.txt"))
    lmax = 3 * 512 - 1
    def cl_from(Dl_l, Dl):
        cl = np.zeros(lmax + 1)
        L = Dl_l.astype(int)
        s = L <= lmax
        cl[L[s]] = Dl[s] * 2 * np.pi / (L[s] * (L[s] + 1))
        return cl
    cl_th = cl_from(th[:, 0], th[:, 1])
    cl_obs = cl_th.copy()
    lo = obs[:, 0] <= 30
    cl_obs[obs[lo, 0].astype(int)] = obs[lo, 1] * 2 * np.pi / (obs[lo, 0] * (obs[lo, 0] + 1))
    rng = np.random.default_rng(seed)
    bl = hp.gauss_beam(math.radians(1.0), lmax=lmax)
    res = {}
    for name, cl in (("LCDM", cl_th), ("observed_low_ell", cl_obs)):
        st = []
        for i in range(nsim):
            np.random.seed(int(rng.integers(1 << 30)))
            s = hp.synfast(cl * bl ** 2, 512, lmax=lmax, pixwin=True)
            s = hp.remove_dipole(np.where(mk > 0, hp.ud_grade(s, nside), hp.UNSEEN))
            st.append(tm.ring_stats(tm.ring_sigmas(s, radii, geo)))
        res[name] = {k: {"sims_mean": float(np.mean([x[k] for x in st])), "sims_std": float(np.std([x[k] for x in st])),
                         "p_ge": float(np.mean([x[k] >= data[k] for x in st])),
                         "p_le": float(np.mean([x[k] <= data[k] for x in st]))} for k in data}
    res_json["rings"] = {"data": data, "sims": res, "nsim": nsim, "n_centres": len(geo), "radii_deg": radii.tolist(),
                         "nside": nside, "drop_uK": 15.0,
                         "profile_data_mean": np.nanmean(S, axis=0).tolist()}


def analytic(res_json):
    ev = [("GW150914", 67.8, 0.68, 0.29559), ("GW151226", 22.6, 0.74, 0.10246), ("LVT151012", 42.0, 0.66, 0.17962),
          ("GW190521 (M_f~142 src, z~0.82)", 142 * 1.82, 0.72, None)]
    res_json["echoes"] = [{"event": e, "M_det": M, "a": a, "dt_echo_s": tm.echo_delay(M, a), "ADA_2016_s": ref} for e, M, a, ref in ev]
    res_json["dispersion"] = tm.dispersion_bounds()
    res_json["future"] = {
        "LCDM_flat": tm.future_of_universe(),
        "LCDM_Ok_-0.0031 (Planck+BAO 2sigma closed)": tm.future_of_universe(Ok=-0.0031),
        "DESI_DR2_w0wa_flat (CPL extrapolated)": tm.future_of_universe(Om=0.3191, w0=-0.752, wa=-0.86),
        "DESI_DR2_w0wa_Ok_-0.0031 (CPL extrapolated)": tm.future_of_universe(Om=0.3191, w0=-0.752, wa=-0.86, Ok=-0.0031)}
    res_json["alpha"] = tm.alpha_bounds()


def main(sections):
    for sec in sections:
        t = time.time()
        part = {}
        {"cmb": cmb, "rings": rings, "analytic": analytic}[sec](part)
        res = json.load(open(OUT)) if os.path.exists(OUT) else {}   # re-read: sections may run concurrently
        res.update(part)
        res.setdefault("timing_s", {})[sec] = time.time() - t
        json.dump(res, open(OUT, "w"), indent=1, default=float)
        print(sec, "done", round(time.time() - t, 1), flush=True)


if __name__ == "__main__":
    if "--figure" in sys.argv:
        from report_71_fig import figure
        figure()
    else:
        main(sys.argv[1:] or ["analytic", "cmb", "rings"])
