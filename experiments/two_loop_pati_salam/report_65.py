"""Numbers and figure for doc 65 (run: python report_65.py, ~30 s)."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import numpy as np

import ripple_modulus as rm

HERE = Path(__file__).resolve().parent
FIG = HERE / "fig_doc65_ripple_settle.png"
FIG_DOC = HERE.parents[1] / "docs" / "hardening" / "figures" / "65_ripple_settle.png"


def figure(out) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(2, 2, figsize=(12, 9))
    # (a) phi(t)/phi_i, exact ODE (no WKB switch)
    a = ax[0, 0]
    N = np.linspace(-20, 0, 4000)
    t = rm.t_N(N) * rm.HBAR / rm.YR / 1e9
    for m in (2e-33, 1e-32, 4e-32, 1.5e-31):
        tr = rm.transfer(m, switch=1e9)
        a.plot(t, tr.phi(N), label=f"m = {m:.1e} eV")
    a.set_xscale("log"); a.set_xlim(1e-4, 14)
    a.axvline(0.051, ls=":", c="k"); a.text(0.055, 0.5, "matter-radiation\nequality", fontsize=8)
    a.set_xlabel("cosmic time t [Gyr]"); a.set_ylabel(r"$\phi(t)/\phi_i$")
    a.set_title("(a) displaced modulus: frozen, then rings and settles (Hubble friction)")
    a.legend(fontsize=8)
    # (b) |Delta alpha/alpha|(z) envelope vs limits
    b = ax[0, 1]
    z = np.logspace(-3, 9.3, 400)
    bm = out["dm_benchmarks"]["1e-19"]
    tr = rm.transfer(1e-19)
    for k, ls in ((1.0, "-"), (bm["kappa_max"], "--")):
        b.plot(1 + z, abs(k * rm.BETA_ALPHA) * tr.delta(z) * bm["phi_i_for_all_DM"], ls,
               label=rf"m=1e-19 eV, all DM, $\kappa$={k:.2g}")
    lims = [("BBN", 4e8, 2e-2), ("CMB", 1100, 5e-3), ("Oklo", 0.14, 2e-8), ("clocks (osc.)", 1e-3, 1e-17)]
    for nm, zz, l in lims:
        b.errorbar(1 + zz, l, yerr=0.5 * l, uplims=True, fmt="v", c="r")
        b.text((1 + zz) * 1.3, l, nm, fontsize=8, color="r")
    b.plot([2, 5], [3e-6, 3e-6], "r-", lw=3); b.text(5.5, 3e-6, "quasars", fontsize=8, color="r")
    b.set_xscale("log"); b.set_yscale("log"); b.set_ylim(1e-24, 10)
    b.set_xlabel("1+z"); b.set_ylabel(r"$|\Delta\alpha/\alpha|$ envelope (vs today)")
    b.set_title(r"(b) $\Delta\alpha/\alpha(z)$ vs limits")
    b.legend(fontsize=8, loc="lower right")
    # (c) allowed region, kappa = 1
    c = ax[1, 0]
    A = rm.allowed_map(1.0)
    c.pcolormesh(np.log10(rm.MASSES), np.log10(rm.PHIS), A, cmap="RdYlGn", shading="auto", vmin=0, vmax=1)
    nb = out["natural_benchmark"]
    c.plot(np.log10(nb["m_eV"]), 0, "k*", ms=14)
    c.text(np.log10(nb["m_eV"]) - 14, -1.0, r"natural $m\sim\Lambda^2/M_{Pl}$", fontsize=8)
    c.axvline(np.log10(5e-3), c="k", ls=":"); c.text(-22, -12.5, "fifth force / EP excluded", fontsize=8)
    c.set_xlabel(r"$\log_{10} m_\phi$ [eV]"); c.set_ylabel(r"$\log_{10}\phi_i/M_{Pl}$")
    c.set_title(r"(c) allowed (green) at spectral coupling $\kappa=1$")
    # (d) max kappa if phi is all of DM
    d = ax[1, 1]
    ms = np.logspace(-20, 3, 24)
    ks = [rm.dm_benchmark(float(m))["kappa_max"] for m in ms]
    d.loglog(ms, np.maximum(ks, 1e-30), "o-")
    d.axhline(1.0, c="k", ls=":"); d.text(1e-19, 3.0, r"spectral/KK value $\kappa=1$", fontsize=8)
    d.set_xlabel(r"$m_\phi$ [eV]"); d.set_ylabel(r"max allowed $\kappa$")
    d.text(2e-21, 1e-26, "m < 2e-20 eV:\nLyman-alpha", fontsize=8)
    d.set_title(r"(d) if the ringing field is all of dark matter")
    fig.tight_layout()
    fig.savefig(FIG, dpi=130)
    FIG_DOC.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(FIG, FIG_DOC)
    plt.close(fig)
    return FIG


def main() -> Path:
    out = rm.report()
    out["dm_kappa_max_curve"] = {f"{m:.3g}": rm.dm_benchmark(float(m))["kappa_max"] for m in np.logspace(-20, 3, 24)}
    figure(out)
    path = HERE / "results_doc65.json"
    path.write_text(json.dumps(out, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o)))
    return path


if __name__ == "__main__":
    print(main())
