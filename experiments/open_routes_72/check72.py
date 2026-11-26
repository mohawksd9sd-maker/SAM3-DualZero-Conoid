"""Validation of thr72 against doc 70 (st.thresholds) in the degenerate limit, and of the 2-loop pieces."""
from common import *
import susy_thresholds as st
import thr72 as T
import math
sm = dict(gY=0.36, g2=0.62, g3=1.03, yt=0.80, yb=0.012, ytau=0.010)
for xt, s in ((0.0, 1.0), (-2.0, 1.0), (2.449, -1.0), (1.0, 1.0)):
    a = st.thresholds(sm, 60.0, st.Spectrum(xt=xt, sgn_mu=s))
    b = T.thresholds72(sm, 60.0, T.Spec(xt=xt, mu=s, fix_x5=False, at2=False, sqcd2=False), 3000.0)
    print(f"xt={xt:+} mu={s:+}: dyt {a['dyt']:.6f} {b['dyt']:.6f} | Db {a['Delta_b']:.5f} {b['Delta_b']:.5f} | Dtau {a['Delta_tau']:.5f} {b['Delta_tau']:.5f}"
          f" | lam {a['lam']:.6f} {b['lam']:.6f} | fg3 {a['fg3']:.6f} {b['fg3']:.6f} fg2 {a['fg2']:.6f} {b['fg2']:.6f} fg1 {b['fg1']:.6f}")
# 2-loop at-as: general formula vs degenerate limit
for xt in (0.0, -2.0, 2.0, 2.449):
    d = T.lam2l_atas_deg(1.03, 0.8, xt)
    f = T.lam2l_atas_full(1.03, 0.8, 3000.0, 3000.0, 3000.0, xt * 3000.0, 3000.0)
    print("2L at-as deg vs full", xt, d, f)
print("2L at^2 (tanb 60, mu=MS, xt 0/-2):", T.lam2l_at2(0.8, 60, 3000., 3000., 0., 3000.), T.lam2l_at2(0.8, 60, 3000., 3000., -6000., 3000.))
