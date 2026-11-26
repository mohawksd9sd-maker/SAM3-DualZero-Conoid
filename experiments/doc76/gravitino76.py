"""Doc 76 item (a): stau-LSP fixes.  Gravitino LSP bookkeeping for the doc-76 corrected points.
Formulas (all standard, cited in doc 76):
  Gamma(stau -> tau G) = m^5 / (48 pi m_G^2 Mbar_P^2) (1 - m_G^2/m^2)^4         [Feng-Su-Takayama hep-ph/0404198]
  Y_stau = kappa * 1e-13 * (m / 100 GeV), kappa in [0.4, 1.5]                  [Pradler-Steffen 0808.2462, Asaka-Hamaguchi-Suzuki]
  Omega_NTP h^2 = m_G * Y / 3.6e-9 GeV                                          [Y = n/s; s0/rho_c h^-2]
  Omega_TP h^2  ~ 0.27 (T_R / 1e10 GeV)(100 GeV / m_G)(m_gluino / 1 TeV)^2      [Bolz-Brandenburg-Buchmuller hep-ph/0012052]
  CBBN: tau_stau <~ 5e3 s                                                       [Pospelov hep-ph/0605215]
m_G 'analogy' value (gaugino-mediation-like, CHOSEN not derived): m_3/2 ~ M12 * Lambda / (sqrt(3) Mbar_P)."""
import json, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
MPBAR = 2.435e18       # reduced Planck mass, GeV
HBAR = 6.582e-25       # GeV s
OMEGA_DM = 0.120       # Planck 2018 Omega_c h^2
KAPPA = (0.4, 1.5)


def width(m, mG):
    return m ** 5 / (48 * math.pi * mG * mG * MPBAR ** 2) * (1 - (mG / m) ** 2) ** 4


def lifetime_s(m, mG):
    return HBAR / width(m, mG)


def yield_stau(m, kappa):
    return kappa * 1e-13 * (m / 100.0)


def omega_ntp(m, mG, kappa):
    return mG * yield_stau(m, kappa) / 3.6e-9


def mG_max_ntp(m, kappa, omega=OMEGA_DM):
    return omega * 3.6e-9 / yield_stau(m, kappa)


def TR_max(mG, mgl, omega=OMEGA_DM):
    return omega / 0.27 * 1e10 * (mG / 100.0) / (mgl / 1000.0) ** 2


def mG_analogy(M12, Lam):
    return M12 * Lam / (math.sqrt(3) * MPBAR)


if __name__ == "__main__":
    ss = {r["tag"]: r for r in json.load(open(os.path.join(HERE, "results_softsusy_2loop.json")))}
    rr = json.load(open(os.path.join(HERE, "results_rerun76.json")))
    out = []
    for tag, d in rr.items():
        e = d["ewsb1L"]
        MS, sp = e["res"]["M_S"], e["spec"]
        s2 = ss[tag]["ss2"]
        mstau = min(s2["stau_R"], s2["stau_L"]) * MS          # 2L-soft ratio x corrected M_S (no L-R mixing)
        mbino = sp["M1"] * MS
        M12 = MS / s2["MS_over_M12"]
        Lam = e["res"]["Lambda"]
        mG = mG_analogy(M12, Lam)
        row = dict(tag=tag, M_S=MS, m_stau=mstau, m_bino=mbino, stau_is_LSP=mstau < mbino, M12=M12, mG_analogy=mG,
                   tau_s_analogy=lifetime_s(mstau, mG), tau_s_mG100=lifetime_s(mstau, 100.0),
                   mG_max_ntp=[mG_max_ntp(mstau, k) for k in KAPPA],
                   omega_ntp_analogy=[omega_ntp(mstau, mG, k) for k in KAPPA],
                   TR_max_analogy=TR_max(mG, sp["M3"] * MS))
        out.append(row)
        print("%-13s m_stau=%5.0f m_bino=%5.0f LSP=%s m_G~%.1f tau=%.2g s (m_G=100: %.2g s) m_G,max(NTP)=%.0f-%.0f Omega_NTP=%.3f-%.3f T_R<%.1e" % (
            tag, mstau, mbino, row["stau_is_LSP"], mG, row["tau_s_analogy"], row["tau_s_mG100"], row["mG_max_ntp"][1], row["mG_max_ntp"][0],
            row["omega_ntp_analogy"][0], row["omega_ntp_analogy"][1], row["TR_max_analogy"]))
    json.dump(out, open(os.path.join(HERE, "results_gravitino76.json"), "w"), indent=1)
