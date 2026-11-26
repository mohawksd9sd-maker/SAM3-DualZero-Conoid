"""Doc 74 map tests (ideas: Shawn Dykes): S1b low-ell anomalies, S1c focus-spot search, S4 rings on Planck."""
from __future__ import annotations

import math
import os

import numpy as np

import sound_banks as sb
tm = sb.tm

HERE = sb.HERE
D = sb.DATA
CACHE = os.path.join(D, "smica_products.npz")   # rebuildable low-res products


def products():
    import healpy as hp
    if os.path.exists(CACHE):
        z = np.load(CACHE)
        return {k: z[k] for k in z.files}
    f = os.path.join(D, "smica.fits")
    inp = hp.read_map(f, field=5, nest=True) * 1e6
    raw = hp.read_map(f, field=0, nest=True) * 1e6
    msk = hp.read_map(os.path.join(D, "mask.fits"), nest=True)
    inp = hp.reorder(inp, n2r=True); raw = hp.reorder(raw, n2r=True); msk = hp.reorder(msk, n2r=True)
    out = {}
    out["inp64"] = hp.ud_grade(inp, 64)                                   # low-ell (full sky, inpainted)
    m512 = hp.ud_grade(raw, 512)
    out["ring1deg_128"] = hp.ud_grade(hp.smoothing(m512, fwhm=math.radians(1.0), lmax=1535), 128)
    out["mask128"] = (hp.ud_grade(msk, 128) > 0.9).astype(float)
    m256 = hp.ud_grade(raw, 256)
    out["focus2deg_64"] = hp.ud_grade(hp.smoothing(m256, fwhm=math.radians(2.0), lmax=767), 64)
    out["mask64"] = (hp.ud_grade(msk, 64) > 0.9).astype(float)
    np.savez(CACHE, **out)
    return out


# ------------------------------------------------------------------ S1b
def lowell(R, nsim=10000, seed=7401, lmax=10):
    import healpy as hp
    P = products()
    grid = 16
    res = {}
    cl = sb.theory_cl(lmax)
    maps = {"Planck_SMICA_inpainted": P["inp64"]}
    wf = os.path.join(HERE, "..", "time_medium", "data", "wmap_ilc_9yr_v5.fits")
    if os.path.exists(wf):
        maps["WMAP9_ILC"] = hp.ud_grade(hp.read_map(wf), 64) * 1e3
    np.random.seed(seed)
    sims = []
    for i in range(nsim):
        alm = hp.synalm(cl, lmax=lmax, new=True)
        st, f0 = sb.ell_stats(alm, lmax, grid)
        S, _ = sb.common_axis_stats(f0, range(2, lmax + 1))
        S23, _ = sb.common_axis_stats(f0, (2, 3))
        sims.append({"planar": [st[l]["planarity"] for l in range(2, lmax + 1)],
                     "f0max": [st[l]["f0_max"] for l in range(2, lmax + 1)],
                     "S_common_2_10": S, "S_common_2_3": S23,
                     "ang23": sb.axis_angle(st[2]["axis_planar"], st[3]["axis_planar"]),
                     "Pmean": float(np.mean([st[l]["planarity"] for l in (2, 3)]))})
    simP = np.array([s["planar"] for s in sims]); simF = np.array([s["f0max"] for s in sims])
    for name, m in maps.items():
        alm = sb.lowell_alm(hp.remove_dipole(m), lmax=lmax)
        st, f0 = sb.ell_stats(alm, lmax, grid)
        S, ipx = sb.common_axis_stats(f0, range(2, lmax + 1))
        S23, ipx23 = sb.common_axis_stats(f0, (2, 3))
        ang23 = sb.axis_angle(st[2]["axis_planar"], st[3]["axis_planar"])
        Pm = float(np.mean([st[2]["planarity"], st[3]["planarity"]]))
        row = {"per_ell": {}, "S_common_axis_2_10": S, "p_S_common_2_10_ge": float(np.mean([s["S_common_2_10"] >= S for s in sims])),
               "S_common_axis_2_3": S23, "p_S_common_2_3_ge": float(np.mean([s["S_common_2_3"] >= S23 for s in sims])),
               "angle_planar_axes_2_3_deg": ang23, "p_angle23_le": float(np.mean([s["ang23"] <= ang23 for s in sims])),
               "p_quad_oct_planar_and_aligned": float(np.mean([(s["ang23"] <= ang23) and (s["Pmean"] >= Pm) for s in sims])),
               "common_axis_2_10_galactic_lb": [float(x) for x in hp.pix2ang(grid, ipx, lonlat=True)],
               "planar_axis_2_galactic_lb": [float(np.ravel(x)[0]) for x in hp.vec2ang(np.array(st[2]["axis_planar"]), lonlat=True)],
               "planar_axis_3_galactic_lb": [float(np.ravel(x)[0]) for x in hp.vec2ang(np.array(st[3]["axis_planar"]), lonlat=True)]}
        for j, l in enumerate(range(2, lmax + 1)):
            row["per_ell"][l] = {"planarity": st[l]["planarity"], "p_planarity_ge": float(np.mean(simP[:, j] >= st[l]["planarity"])),
                                 "f0_max": st[l]["f0_max"], "p_f0max_ge": float(np.mean(simF[:, j] >= st[l]["f0_max"]))}
        res[name] = row
    obs = np.loadtxt(sb.OBS_TT)
    ell = obs[:, 0].astype(int); Dl = obs[:, 1]
    th = np.loadtxt(sb.THEORY); Dth = np.interp(ell, th[:, 0], th[:, 1])
    rngp = np.random.default_rng(seed + 1)
    par = []
    s = ell <= 30
    nu = 2 * ell[s] + 1
    simD = Dth[s][None, :] * rngp.chisquare(nu, size=(20000, len(nu))) / nu
    for lm in range(5, 31):
        r = sb.parity_ratio(Dl, ell, lm)
        rs = np.array([sb.parity_ratio(x, ell[s], lm) for x in simD])
        par.append({"lmax": lm, "R_even_over_odd": r, "p_le": float(np.mean(rs <= r)), "sims_median": float(np.median(rs))})
    res["parity"] = par
    res["nsim"] = nsim
    R["lowell"] = res


# ------------------------------------------------------------------ S1c
def focus(R, nsim=300, seed=7402):
    import healpy as hp
    P = products()
    nside = 64
    mk = P["mask64"]
    M, meta = sb.focus_filter_matrix(nside, mk)
    m = hp.remove_dipole(np.where(mk > 0, P["focus2deg_64"], hp.UNSEEN)); m[mk <= 0] = 0
    a_data = M @ m
    cl = sb.theory_cl(767)
    bl = hp.gauss_beam(math.radians(2.0), lmax=767) * hp.gauss_beam(math.radians(5 / 60), lmax=767)
    np.random.seed(seed)
    A = []
    for i in range(nsim):
        s = hp.ud_grade(hp.synfast(cl * bl ** 2, 256, lmax=767, pixwin=True), nside)
        s = hp.remove_dipole(np.where(mk > 0, s, hp.UNSEEN)); s[mk <= 0] = 0
        A.append(M @ s)
    A = np.array(A)
    sd = A.std(axis=0)
    z_data = a_data / sd
    z_sims = A / sd
    zmax_sims = np.abs(z_sims).max(axis=1)
    i = int(np.argmax(np.abs(z_data)))
    ci, kap = meta[i]
    lon, lat = hp.pix2ang(16, ci, lonlat=True)
    per_kappa = {}
    for kp in sorted(set(k for _, k in meta)):
        sel = np.array([k == kp for _, k in meta])
        zd = np.abs(z_data[sel]).max()
        per_kappa[int(kp)] = {"max_abs_z": float(zd), "p_global_within_kappa": float(np.mean(np.abs(z_sims[:, sel]).max(axis=1) >= zd))}
    R["focus"] = {"n_centres": len(set(c for c, _ in meta)), "kappas": sorted(set(int(k) for _, k in meta)),
                  "best": {"z": float(z_data[i]), "kappa": int(kap), "galactic_lon_lat": [float(lon), float(lat)]},
                  "max_abs_z_data": float(np.abs(z_data).max()), "p_global": float(np.mean(zmax_sims >= np.abs(z_data).max())),
                  "sims_max_abs_z_median": float(np.median(zmax_sims)), "sims_max_abs_z_95": float(np.quantile(zmax_sims, 0.95)),
                  "per_kappa": per_kappa, "nsim": nsim}


# ------------------------------------------------------------------ S4
def rings(R, nsim=200, seed=7403, observed_low_ell=False):
    import healpy as hp
    P = products()
    nside = 128
    mk = P["mask128"]
    radii, geo = tm.ring_geometry(nside, mk)
    m = hp.remove_dipole(np.where(mk > 0, P["ring1deg_128"], hp.UNSEEN))
    S = tm.ring_sigmas(m, radii, geo)
    data = tm.ring_stats(S)
    # Hawking-point-like statistic (ours, not the An et al. pipeline): temperature variance in 4-deg discs
    cvec = np.array(hp.pix2vec(32, np.arange(hp.nside2npix(32)))).T
    nfull = len(hp.query_disc(nside, cvec[0], math.radians(4.0)))
    discs = []
    for v in cvec:
        if mk[hp.vec2pix(nside, *v)] <= 0:
            continue
        idx = hp.query_disc(nside, v, math.radians(4.0))
        idx = idx[mk[idx] > 0]
        if len(idx) > 0.7 * nfull:
            discs.append(idx)

    def hp_stats(mm):
        return np.array([np.var(mm[ix]) for ix in discs])

    vdata = hp_stats(m)
    lmax = 3 * 512 - 1
    cl = sb.theory_cl(lmax)
    if observed_low_ell:      # as doc 71: replace l <= 30 by the observed Planck 2018 TT band powers
        obs = np.loadtxt(sb.OBS_TT); lo = obs[:, 0] <= 30
        cl[obs[lo, 0].astype(int)] = obs[lo, 1] * 2 * np.pi / (obs[lo, 0] * (obs[lo, 0] + 1))
    bl = hp.gauss_beam(math.radians(1.0), lmax=lmax) * hp.gauss_beam(math.radians(5 / 60), lmax=lmax)
    np.random.seed(seed)
    st, vs = [], []
    for i in range(nsim):
        s = hp.synfast(cl * bl ** 2, 512, lmax=lmax, pixwin=True)
        s = hp.remove_dipole(np.where(mk > 0, hp.ud_grade(s, nside), hp.UNSEEN))
        st.append(tm.ring_stats(tm.ring_sigmas(s, radii, geo)))
        vs.append(hp_stats(s))
    vs = np.array(vs)
    thr = np.quantile(vs, 0.999)
    n_hi_data = int(np.sum(vdata > thr)); n_hi_sims = np.sum(vs > thr, axis=1)
    sims = {k: {"sims_mean": float(np.mean([x[k] for x in st])), "sims_std": float(np.std([x[k] for x in st])),
                "p_ge": float(np.mean([x[k] >= data[k] for x in st])), "p_le": float(np.mean([x[k] <= data[k] for x in st]))}
            for k in data}
    R["rings_observed_low_ell" if observed_low_ell else "rings"] = {"map": "Planck PR3 SMICA, 1 deg, common mask", "data": data, "sims": sims, "nsim": nsim,
                  "n_centres": len(geo),
                  "hawking_like": {"n_discs": len(discs), "threshold_var_uK2": float(thr), "n_high_data": n_hi_data,
                                   "sims_mean": float(n_hi_sims.mean()), "p_ge": float(np.mean(n_hi_sims >= n_hi_data)),
                                   "max_var_data": float(vdata.max()), "p_maxvar_ge": float(np.mean(vs.max(axis=1) >= vdata.max()))}}


def rings_obs(R):
    rings(R, observed_low_ell=True)
