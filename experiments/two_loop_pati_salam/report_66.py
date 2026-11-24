"""Numbers and figure for doc 66 (run: python report_66.py, ~3 min; the Mathieu scan dominates)."""

from __future__ import annotations

import json
import math
import shutil
from pathlib import Path

import numpy as np

import coupled_ripples as cr
import finite_universe as fu

HERE = Path(__file__).resolve().parent
FIG = HERE / "fig_doc66_bounded_pond.png"
FIG_DOC = HERE.parents[1] / "docs" / "hardening" / "figures" / "66_bounded_pond.png"


def _j(o):
    if hasattr(o, "item"):
        return o.item()
    return str(o)


def figure(A, B) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(2, 3, figsize=(16, 9))
    # (a) coupled ripples
    a = ax[0, 0]
    r = cr.simulate(mu=1.05, eps=0.0, phi0=(1.0, 1.0), tau_end=300, n_out=30000)
    a.plot(r["t"], (r["p1"] + r["p2"]) * r["t"] ** 0.75, lw=0.6, label=r"$\alpha\propto\phi_1+\phi_2$, $m_2=1.05m_1$ (beats)")
    r2 = cr.simulate(mu=2.0, g3=1.0, phi0=(1.0, 0.01), tau_end=300, n_out=30000)
    a.plot(r2["t"], r2["p2"] * r2["t"] ** 0.75 + 3, lw=0.6, label=r"$\phi_2$ pumped by $\phi_1$ (cubic, 2:1), offset +3")
    a.set_xlabel(r"$m_1 t$"); a.set_ylabel(r"field $\times a^{3/2}$ (WKB-scaled)")
    a.set_title("(a) coupled ripples: beats and energy transfer"); a.legend(fontsize=7)
    # (b) energy share
    b = ax[0, 1]
    for g3 in (0.3, 1.0, 3.0):
        rr = cr.simulate(mu=2.0, g3=g3, phi0=(1.0, 0.01), tau_end=400, n_out=40000)
        sh = cr._smooth(rr["E2"], rr["t"], 4 * math.pi) / cr._smooth(rr["E1"] + rr["E2"], rr["t"], 4 * math.pi)
        b.plot(rr["t"][:-600], sh[:-600], label=f"g3 = {g3}")
    b.set_xscale("log"); b.set_xlabel(r"$m_1 t$"); b.set_ylabel(r"share of comoving energy in $\phi_2$")
    b.set_title("(b) cubic 2:1 transfer: $\\phi_1$ pumps $\\phi_2$ (slow drift, ~$t^{1/4}$)"); b.legend(fontsize=8)
    # (c) Mathieu
    c = ax[0, 2]
    for q, res in A["mathieu_curves"].items():
        c.plot(res["k_grid"], np.maximum(res["ln_n"], -5), label=f"q0 = {q}")
    c.axhline(A["parametric"][0]["ln_n_needed_backreaction"], ls=":", c="k")
    c.text(0.2, A["parametric"][0]["ln_n_needed_backreaction"] - 3, "needed for back-reaction (natural m)", fontsize=8)
    c.set_xlabel(r"comoving $k/m_1$"); c.set_ylabel(r"$\ln n_k$ (spectator)"); c.set_ylim(-5, 35)
    c.set_title("(c) parametric resonance in an expanding universe"); c.legend(fontsize=8)
    # (d) low-l CMB
    d = ax[1, 0]
    D, err, T = fu.planck()
    ls = np.arange(2, 31)
    d.errorbar(ls, [D[l] for l in ls], yerr=[err[l] for l in ls], fmt="ko", ms=3, label="Planck 2018")
    d.plot(ls, [T[l] for l in ls], "k-", label=r"$\Lambda$CDM")
    for lab, R in B["curves"].items():
        d.plot(ls, [T[l] * R[str(l)] if isinstance(R, dict) and str(l) in R else T[l] * R[l] for l in ls], label=lab)
    d.set_xscale("log"); d.set_xlabel(r"$\ell$"); d.set_ylabel(r"$D_\ell$ [$\mu$K$^2$]")
    d.set_title("(d) finite universe: low-$\\ell$ TT"); d.legend(fontsize=7)
    # (e) dchi2 vs size
    e = ax[1, 1]
    t3 = B["T3"]; pds = B["PDS"]
    e.plot([x["L_over_chi"] for x in t3], [x["dchi2"] for x in t3], "o-", label=r"T$^3$ (x: $L/\chi_*$)")
    e.axvline(2.0, c="C0", ls=":"); e.text(2.05, 8, "T3 circles\nfor L<2", fontsize=8, color="C0")
    xp = [x["chi_star"] / (math.pi / 10) * 2 for x in pds]
    e.plot([2 * (math.pi / 10) / x["chi_star"] for x in pds], [x["dchi2"] for x in pds], "s-",
           label=r"PDS (x: $2r_{inj}/\chi_*$)")
    e.axhline(0, c="k", lw=0.5); e.set_ylim(-5, 15); e.set_xlim(0.5, 6)
    e.set_xlabel("domain size / LSS diameter scale"); e.set_ylabel(r"$\Delta\chi^2$ vs $\Lambda$CDM ($\ell\leq30$)")
    e.set_title("(e) size fit; matched circles exist left of x = 2"); e.legend(fontsize=8)
    # (f) phases
    f = ax[1, 2]
    ph = B["phases_T3_L2"]
    ll = sorted(int(k) for k in ph)
    f.bar(np.array(ll) - 0.2, [ph[str(l)]["random_mean"] if str(l) in ph else ph[l]["random_mean"] for l in ll], 0.4,
          yerr=[ph[str(l)]["random_std"] if str(l) in ph else ph[l]["random_std"] for l in ll], label="random phases")
    f.bar(np.array(ll) + 0.2, [max(ph[str(l)]["coherent"] if str(l) in ph else ph[l]["coherent"], 1e-3) for l in ll], 0.4,
          label="coherent ('one stone')")
    f.set_yscale("log"); f.set_ylim(1e-3, 3); f.set_xlabel(r"$\ell$"); f.set_ylabel(r"$C_\ell/C_\ell^{\rm flat}$")
    f.set_title(r"(f) T$^3$ ($L=2\chi_*$): mode-phase interference"); f.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG, dpi=120)
    FIG_DOC.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(FIG, FIG_DOC)
    plt.close(fig)
    return FIG


def main() -> Path:
    A = cr.report()
    A["mathieu_curves"] = {q: cr.mathieu(q) for q in (1.0, 100.0, 1000.0)}
    B = {"LCDM": fu.lcdm(),
         "T3": fu.scan_T3(np.round(np.arange(1.0, 5.01, 0.25), 3)),
         "PDS": fu.scan_S3(tuple(-x for x in (0.001, 0.003, 0.005, 0.007, 0.0099, 0.011, 0.012, 0.013, 0.014,
                                               0.016, 0.02, 0.03)), pds=True),
         "S3": fu.scan_S3((-0.005, -0.0099, -0.013, -0.044), pds=False),
         "phases_T3_L2": fu.t3_phase_realisations(n_real=300),
         "PDS_first_modes_beta": [int(k + 1) for k in np.nonzero(fu.molien_I(60))[0]]}
    B["best_T3"] = min(B["T3"], key=lambda r: r["dchi2"])
    B["best_T3_no_circles"] = min([r for r in B["T3"] if not r["matched_circles"]], key=lambda r: r["dchi2"])
    B["best_PDS"] = min(B["PDS"], key=lambda r: r["dchi2"])
    B["best_PDS_no_circles"] = min([r for r in B["PDS"] if not r["matched_circles"]], key=lambda r: r["dchi2"])
    B["curves"] = {
        r"T$^3$ $L=1.5\chi_*$": {l: fu.ratio_T3(l, 1.5) for l in range(2, 31)},
        r"T$^3$ $L=2\chi_*$": {l: fu.ratio_T3(l, 2.0) for l in range(2, 31)},
        r"PDS $\Omega_k=-0.013$": {l: fu.ratio_S3(l, fu.chi_star(-0.013), True) for l in range(2, 31)},
    }
    out = {"A": A, "B": B}
    path = HERE / "results_doc66.json"
    path.write_text(json.dumps(out, indent=1, default=_j))
    figure(A, json.loads(path.read_text())["B"] | {"curves": B["curves"], "phases_T3_L2": B["phases_T3_L2"]})
    return path


if __name__ == "__main__":
    import sys
    if "--figure-only" in sys.argv:
        d = json.loads((HERE / "results_doc66.json").read_text())
        print(figure(d["A"], d["B"]))
    else:
        print(main())
