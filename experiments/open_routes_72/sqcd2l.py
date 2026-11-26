"""Doc 72 route 3 piece: two-loop O(alpha_s^2) SUSY-QCD matching of the top Yukawa at M_S.
Uses FlexibleSUSY's implementation (GPL-3) of Bednyakov et al. hep-ph/0210258, hep-ph/0507139:
  M_t = m_t^{MSSM,DR}(Q) [1 + D1q + D1s + D2q + D2s]           (FlexibleSUSY dMt_over_mt_*)
and the SM MS-bar pole relation (6-flavour, Gray-Broadhurst K2 = 13.4434 - 1.0414*5, logs from RG):
  M_t = m_t^{SM,MS}(Q) [1 + a(4/3 + L) + a^2 (8.236 + c1 L + c2 L^2)],  a = alpha_s^SM(Q)/pi.
The matching ratio R = m^{DR}_{MSSM}(Q)/m^{MS}_{SM}(Q) is extracted in the limit m_t << M_S
(checked numerically to be m_t-independent) and split into 1-loop and 2-loop parts."""
import ctypes, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
_L = ctypes.CDLL(os.path.join(HERE, "fs_ext", "libdmt.so"))
_L.dmt.argtypes = [ctypes.c_double] * 8 + [ctypes.POINTER(ctypes.c_double)]

def fs(g3, mt, mg, m1, m2, ms, xt, Q):
    o = (ctypes.c_double * 4)()
    _L.dmt(g3, mt, mg, m1, m2, ms, xt, Q, o)
    return list(o)

NF = 6
B0 = (11 - 2 * NF / 3) / 4
G1 = (202 / 3 - 20 * NF / 9) / 16
C2 = (1 + B0) / 2
C1 = G1 + 4 / 3 * (1 + B0) - 2
K2 = 13.4434 - 1.0414 * 5

def stop_masses(mQ, mU, mt, Xt):
    a, b, c = mQ ** 2 + mt ** 2, mU ** 2 + mt ** 2, mt * Xt
    tr, d = (a + b) / 2, math.sqrt(((a - b) / 2) ** 2 + c * c)
    return math.sqrt(tr - d), math.sqrt(tr + d)

def ratio(g3_sm, M_S, mQ_r=1.0, mU_r=1.0, r3=1.0, xt=0.0, mt_ms=1.0, loops=2):
    """R = m_t^{MSSM DR}/m_t^{SM MS} at Q = M_S; mt_ms is a probe top mass (EFT limit: small)."""
    Q = M_S
    mQ, mU, mg = mQ_r * M_S, mU_r * M_S, r3 * M_S
    K = 1 / (16 * math.pi ** 2)
    lg = lambda m: math.log(m * m / (Q * Q))
    fg3 = 1 + K * g3_sm ** 2 * (0.5 - lg(mg) - (2 * lg(mQ) + lg(mU) + lg(mU)) / 12)   # BGSS (dg3), mD ~ mU here
    g3M = g3_sm * fg3
    a = g3_sm ** 2 / (4 * math.pi ** 2)
    L = math.log(Q * Q / mt_ms ** 2)
    num = 1 + a * (4 / 3 + L) + (a * a * (K2 + C1 * L + C2 * L * L) if loops >= 2 else 0)
    mt_dr = mt_ms
    for _ in range(30):
        m1, m2 = stop_masses(mQ, mU, mt_dr, xt * M_S)
        d = fs(g3M, mt_dr, mg, m1, m2, M_S, xt * M_S, Q)
        den = 1 + d[0] + d[1] + ((d[2] + d[3]) if loops >= 2 else 0)
        R = num / den
        mt_dr = mt_ms * R
    return R

if __name__ == "__main__":
    g3 = 1.03
    for xt in (0.0, -2.0, 2.0):
        for mt in (173.0, 40.0, 10.0, 2.0):
            r1 = ratio(g3, 3000.0, xt=xt, mt_ms=mt, loops=1)
            r2 = ratio(g3, 3000.0, xt=xt, mt_ms=mt, loops=2)
            print(f"xt={xt:+.1f} mt={mt:6.1f}  R1-1={r1-1:+.5f}  R2-1={r2-1:+.5f}  2L part={r2-r1:+.5f}")

def expansion(g3_sm, M_S, mt_ms=2.0, **kw):
    """Fit R - 1 = c1 a + c2 a^2 + c3 a^3 by scaling g3 (strict alpha_s expansion); returns (c1 a, c2 a^2)."""
    import numpy as np
    lams = np.array([0.15, 0.25, 0.35, 0.5, 0.7, 1.0])
    a0 = g3_sm ** 2 / (4 * math.pi ** 2)
    aa = a0 * lams ** 2
    y = np.array([ratio(g3_sm * l, M_S, mt_ms=mt_ms, **kw) - 1 for l in lams])
    A = np.vstack([aa, aa ** 2, aa ** 3, aa ** 4]).T
    c = np.linalg.lstsq(A, y, rcond=None)[0]
    return c[0] * a0, c[1] * a0 ** 2, c[2] * a0 ** 3
