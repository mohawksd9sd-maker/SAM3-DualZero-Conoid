"""Doc 72 route 3: three-loop RGEs.
SM: Buttazzo et al. arXiv:1307.3536 appendix A (3-loop terms for g1, g2, g3, y_t, lambda in the top-only
approximation; 4-loop pure-QCD g3 term), added on top of the doc 60 two-loop SM betas (which keep y_b, y_tau).
MSSM (DR-bar): Jack-Jones-Kord arXiv:hep-ph/0408128 eqs. for beta_g^(3) and gamma^(3) (n5 = n10 = 0,
third-family Yukawas only), added to the doc 70 two-loop MSSM RGEs (susy_thresholds.mssm_rhs2).
Conventions: our lambda has V = lambda |H|^4 (same as Buttazzo); g1 GUT-normalised inside the formulas."""
import math
import numpy as np
from scipy.integrate import solve_ivp
from common import *
import two_loop_higgs as th
import susy_thresholds as st

Z3 = 1.2020569031595942
L16 = 16 * math.pi ** 2


def sm3_terms(s):
    """Three-loop (and 4-loop QCD) pieces of d(coupling)/d ln mu for (gY, g2, g3, yt, yb, ytau, lam)."""
    gY, g2, g3, yt, yb, ytau, lam = s
    g1s, g2s, g3s, t = 5 / 3 * gY * gY, g2 * g2, g3 * g3, yt * yt
    k3 = 1 / L16 ** 3
    # d g1^2 / d ln mu^2
    G1 = g1s ** 2 * k3 * (t * (189 / 16 * t - 29 / 5 * g3s - 471 / 32 * g2s - 2827 / 800 * g1s) + lam * (-9 / 5 * lam + 9 / 10 * g2s + 27 / 50 * g1s)
                          + 297 / 5 * g3s ** 2 + 789 / 64 * g2s ** 2 - 388613 / 24000 * g1s ** 2 - 3 / 5 * g3s * g2s - 137 / 75 * g3s * g1s + 123 / 160 * g2s * g1s)
    G2 = g2s ** 2 * k3 * (t * (147 / 16 * t - 7 * g3s - 729 / 32 * g2s - 593 / 160 * g1s) + lam * (-3 * lam + 3 / 2 * g2s + 3 / 10 * g1s)
                          + 81 * g3s ** 2 + 324953 / 1728 * g2s ** 2 - 5597 / 1600 * g1s ** 2 + 39 * g3s * g2s - 1 / 5 * g3s * g1s + 873 / 160 * g2s * g1s)
    G3 = g3s ** 2 * k3 * (t * (15 * t - 40 * g3s - 93 / 8 * g2s - 101 / 40 * g1s)
                          + 65 / 2 * g3s ** 2 + 109 / 8 * g2s ** 2 - 523 / 120 * g1s ** 2 + 21 * g3s * g2s + 77 / 15 * g3s * g1s - 3 / 40 * g2s * g1s) \
        + g3s ** 5 / L16 ** 4 * (-2472.28)
    l = lam
    LAM = k3 * (l ** 3 * (6011.35 * l + 873 * t - 387.452 * g2s - 77.490 * g1s)
                + l ** 2 * t * (1768.26 * t + 160.77 * g3s - 359.539 * g2s - 63.869 * g1s)
                + l ** 2 * (-790.28 * g2s ** 2 - 185.532 * g1s ** 2 - 316.64 * g2s * g1s)
                + l * t ** 2 * (-223.382 * t - 662.866 * g3s - 5.470 * g2s - 21.015 * g1s)
                + l * t * (356.968 * g3s ** 2 - 319.664 * g2s ** 2 - 74.8599 * g1s ** 2 + 15.1443 * g3s * g2s + 17.454 * g3s * g1s + 5.615 * g2s * g1s)
                + l * g2s ** 2 * (-57.144 * g3s + 865.483 * g2s + 79.638 * g1s)
                + l * g1s ** 2 * (-8.381 * g3s + 61.753 * g2s + 28.168 * g1s)
                + t ** 3 * (-243.149 * t + 250.494 * g3s + 74.138 * g2s + 33.930 * g1s)
                + t ** 2 * (-50.201 * g3s ** 2 + 15.884 * g2s ** 2 + 15.948 * g1s ** 2 + 13.349 * g3s * g2s + 17.570 * g3s * g1s - 70.356 * g2s * g1s)
                + t * g3s * (16.464 * g2s ** 2 + 1.016 * g1s ** 2 + 11.386 * g2s * g1s)
                + t * g2s ** 2 * (62.500 * g2s + 13.041 * g1s)
                + t * g1s ** 2 * (10.627 * g2s + 11.117 * g1s)
                + g3s * (7.536 * g2s ** 3 + 0.663 * g1s ** 3 + 1.507 * g2s ** 2 * g1s + 1.105 * g2s * g1s ** 2)
                - 114.091 * g2s ** 4 - 1.508 * g1s ** 4 - 37.889 * g2s ** 3 * g1s + 6.500 * g2s ** 2 * g1s ** 2 - 1.543 * g2s * g1s ** 3)
    YT = t * k3 * (t ** 2 * (58.6028 * t + 198 * l - 157 * g3s - 1593 / 16 * g2s - 2437 / 80 * g1s)
                   + l * t * (15 / 4 * l + 16 * g3s - 135 / 2 * g2s - 127 / 10 * g1s)
                   + t * (363.764 * g3s ** 2 + 16.990 * g2s ** 2 - 24.422 * g1s ** 2 + 48.370 * g3s * g2s + 18.074 * g3s * g1s + 34.829 * g2s * g1s)
                   + l ** 2 * (-36 * l + 45 * g2s + 9 * g1s) + l * (-171 / 16 * g2s ** 2 - 1089 / 400 * g1s ** 2 + 117 / 40 * g2s * g1s)
                   - 619.35 * g3s ** 3 + 169.829 * g2s ** 3 + 16.099 * g1s ** 3 + 73.654 * g3s ** 2 * g2s - 15.096 * g3s ** 2 * g1s
                   - 21.072 * g3s * g2s ** 2 - 22.319 * g3s * g1s ** 2 - 321 / 20 * g3s * g2s * g1s - 4.743 * g2s ** 2 * g1s - 4.442 * g2s * g1s ** 2)
    # convert d x^2/d ln mu^2 -> d x / d ln mu  (= X/x);  g1 -> gY: d gY = sqrt(3/5) d g1
    dgY = (G1 / math.sqrt(g1s)) * math.sqrt(3 / 5)
    dg2 = G2 / g2
    dg3 = G3 / g3
    dyt = YT / yt
    dl = 2 * LAM
    return np.array([dgY, dg2, dg3, dyt, 0.0, 0.0, dl])


def sm_beta3(s):
    return th.sm_beta(s, 2, False) + sm3_terms(s)


def run_sm3(s0, mu0, mu1, dense=False):
    return solve_ivp(lambda t, s: sm_beta3(s), (math.log(mu0), math.log(mu1)), s0,
                     method="DOP853", rtol=1e-10, atol=1e-13, dense_output=dense)


# ------------------------------------------------------------------ MSSM 3-loop (DR-bar), third family only
K6 = 6 * Z3


def mssm3_terms(s):
    g1, g2, g3, yt, yb, ytau, yn = s
    a, b, c = g1 * g1, g2 * g2, g3 * g3          # g1 GUT normalised (as in mssm_rhs2 state)
    T, B, E = yt * yt, yb * yb, ytau * ytau
    k = K6
    # gauge (n5 = n10 = 0); traces of third-family-only matrices: trT = T, trT^2 = T^2, tr(TB) = T B ...
    bg1 = g1 ** 3 * (84 / 5 * T * T + 18 * T * T + 54 / 5 * B * B + 36 / 5 * B * B + 58 / 5 * T * B + 54 / 5 * E * E + 24 / 5 * E * E + 84 / 5 * E * B
                     - (169 / 75 * a + 87 / 5 * b + 352 / 15 * c) * T - (49 / 75 * a + 33 / 5 * b + 256 / 15 * c) * B - (81 / 25 * a + 63 / 5 * b) * E
                     + 484 / 15 * c * c - (24 / 5 * b + 1096 / 75 * a) * c - 81 / 5 * b * b - 69 / 25 * a * b - 32117 / 375 * a * a)
    bg2 = g2 ** 3 * (24 * (T * T + B * B) + 18 * (T * T + B * B) + 12 * B * T + 12 * B * E + 8 * E * E + 2 * E * E
                     - (32 * c + 33 * b) * (T + B) - a * (29 / 5 * T + 11 / 5 * B) - (11 * b + 21 / 5 * a) * E
                     + 44 * c * c + (24 * b - 8 / 5 * a) * c + 35 * b * b + 9 / 5 * a * b - 457 / 25 * a * a)
    bg3 = g3 ** 3 * (18 * T * T + 12 * T * T + 8 * B * T + 18 * B * B + 12 * B * B + 6 * E * B
                     - (104 / 3 * c + 12 * b) * (T + B) - a * (44 / 15 * T + 32 / 15 * B)
                     + 347 / 3 * c * c + (6 * b + 22 / 15 * a) * c - 27 * b * b - 3 / 5 * a * b - 1702 / 75 * a * a)
    Xi = (b ** 3 * (345 / 4 + k * 105 / 4) + a ** 3 * (1839 / 100 - k * 597 / 500) + a * a * b * (27 / 100 - 81 / 100 * k)
          + a * a * c * (66 / 5 - 66 / 25 * k) + a * b * b * (9 / 4 - 27 / 20 * k) + b * b * c * (90 - 18 * k))
    # gamma_Q^(3) restricted to the (3,3) entry; matrices commute (diagonal), T^n -> T^n
    gQ = (k * (T ** 3 + B ** 3) + 4 * B * T * B + 4 * T * B * T + 6 * T * T * T + B * B * (6 * B + 2 * E)
          + B * (6 * T * B - 9 * B * B - 6 * B * E + 18 * B * B - E * E + 6 * E * E)
          - 9 * T * T * T + 18 * T * T * T + 6 * T * T * B
          + a * (T * T * (11 / 3 - k) + B * B * (7 / 15 - k / 5))
          + ((3 * k - 3) * b + 64 / 3 * c) * (T * T + B * B)
          + ((2 - 4 / 5 * k) * a + 18 * b + (8 * k - 8) * c) * T * T
          + a * B * ((16 / 5 - 4 / 5 * k) * B + (2 / 5 * k - 8 / 5) * E) + b * B * (18 * B + 6 * E) + 8 * c * B * ((k - 1) * B + E)
          + a * a * T * (143 / 900 * k - 3767 / 300) + a * a * B * (7 / 180 * k - 633 / 100) - (13 / 30 * T + 7 / 30 * B + 3 / 10 * E) * a * a
          + (1.5 * k - 59 / 10) * a * b * T + (0.3 * k - 41 / 10) * a * b * B + a * c * T * (64 / 45 * k - 68 / 5) + a * c * B * (64 / 45 * k - 76 / 15)
          - b * b * ((T + B) * (45 / 4 + 21 / 4 * k) + 45 / 2 * (T + B) + 15 / 2 * E) - 4 * b * c * (T + B)
          + c * c * ((T + B) * (8 / 3 - 136 / 9 * k) - 80 / 3 * (T + B))
          + (25 / 4 - 27 / 20 * k) * a * b * b - 8 / 5 * a * b * c
          + a ** 3 * (28457 / 13500 - k * 199 / 1500) + a * a * b * (11 / 100 - 9 / 100 * k) + a * a * c * (194 / 225 - 22 / 75 * k)
          + a * c * c * (608 / 45 - 44 / 15 * k) + b * b * c * (50 - 18 * k) + b * c * c * (8 - 12 * k)
          + b ** 3 * (345 / 4 + 105 / 4 * k) + c ** 3 * (2720 / 27 + 160 / 3 * k))
    gt = ((6 + 2 * k) * T ** 3 + 6 * T * T * T - 2 * T * B * T - 2 * T * T * B + 6 * T * B * B
          + T * (36 * T * T + 12 * T * B - 18 * T * T) + T * B * (-6 * T + 12 * B + 4 * E)
          + a * (T * T * (-1 / 3 + k) + 7 * (1 + k / 5) * T * T + T * B * (19 / 15 + 3 / 5 * k))
          + b * ((9 - 3 * k) * T * T + (27 - 9 * k) * T * T + (9 - 3 * k) * T * B)
          + c * (16 * (k - 1) * T * T + 64 / 3 * (T * T + T * B))
          + a * a * (T * (-799 / 50 - 247 / 450 * k) - 104 / 15 * T - 56 / 15 * B - 24 / 5 * E)
          + a * c * T * (-8 / 15 - 112 / 45 * k) + a * b * T * (-67 / 5 + 13 / 5 * k)
          + b * b * T * (-87 / 2 - 1.5 * k) + b * c * T * (-88 + 16 * k)
          + c * c * (T * (16 / 3 - 272 / 9 * k) - 80 / 3 * T - 80 / 3 * B)
          + a * c * c * (-172 / 45 - 44 / 15 * k) + a * a * b * (36 / 5 - 36 / 25 * k) + a * a * c * (2144 / 225 - 352 / 75 * k)
          + c ** 3 * (2720 / 27 + 160 / 3 * k) + a ** 3 * (106868 / 3375 - k * 796 / 375) + b * c * c * (60 - 12 * k))
    gH2 = (54 * T * T * T + 3 * (k + 1) * T ** 3 + 18 * B * T * B + 9 * B * T * B + 6 * E * T * B
           + a * ((57 / 5 - 3 / 5 * k) * T * T + (6 / 5 + k / 5) * T * B) + b * ((9 + 9 * k) * T * T + 18 * T * B)
           + c * ((72 - 24 * k) * T * T + (24 - 8 * k) * T * B)
           - a * a * ((2123 / 60 + 13 / 60 * k) * T + 21 / 10 * B + 27 / 10 * E)
           + (a * b * (21 / 10 * k - 57 / 10) + a * c * (104 / 15 * k - 124 / 3) + b * c * (24 * k - 132)) * T
           + b * b * (T * (-225 / 4 - 63 / 4 * k) - 45 / 2 * B - 15 / 2 * E)
           - c * c * (160 / 3 * T + 8 / 3 * k * T) + Xi)
    # bottom / tau (gamma_b^(3), gamma_H1^(3), gamma_L^(3), gamma_tau^(3))
    gb = ((2 * k + 6) * B ** 3 + 6 * B * T * T - 2 * B * B * T + B * T * (12 * T - 6 * B - 2 * E) - 2 * B * T * B + B * B * (6 * B + 2 * E)
          + B * (12 * T * B - 18 * B * B - 12 * B * E + 36 * B * B - 2 * E * E + 12 * E * E)
          + a * B * T * (-29 / 15 + 3 / 5 * k) + a * B * B * (-1 / 3 + k / 5) + a * B * ((7 - k) * B + (k - 3) * E)
          + b * B * T * (9 - 3 * k) + b * B * B * (9 - 3 * k) + b * B * ((27 - 9 * k) * B + (9 - 3 * k) * E)
          + 64 / 3 * c * B * T + 64 / 3 * c * B * B + c * B * ((16 * k - 16) * B + 16 * E)
          + a * a * (B * (-337 / 30 - 7 / 450 * k) - 26 / 15 * T - 14 / 15 * B - 6 / 5 * E)
          + a * b * B * (-43 / 5 + 7 / 5 * k) + a * c * B * (-24 / 5 + 16 / 9 * k) + b * c * B * (-88 + 16 * k) + b * b * B * (-87 / 2 - 1.5 * k)
          + c * c * (B * (16 / 3 - 272 / 9 * k) - 80 / 3 * T - 80 / 3 * B)
          + c ** 3 * (2720 / 27 + 160 / 3 * k) + a ** 3 * (5629 / 675 - k * 199 / 375) + a * a * b * (9 / 5 - 9 / 25 * k)
          + a * a * c * (728 / 225 - 88 / 75 * k) + a * c * c * (452 / 45 - 44 / 15 * k) + b * c * c * (60 - 12 * k))
    gH1 = ((k + 1) * (3 * B ** 3 + E ** 3) + 9 * T * T * B + 18 * T * T * B + 6 * (E + 3 * B) * (E * E + 3 * B * B)
           + (24 - 8 * k) * c * (T * B + 3 * B * B) + b * (18 * T * B + (9 * k + 9) * B * B + (3 * k + 3) * E * E)
           + a * (-12 / 5 * T * B + 7 / 5 * k * T * B + 3 * B * B + 9 / 5 * k * B * B + 9 * E * E - 9 / 5 * k * E * E)
           + a * a * (-39 / 10 * T - B * (175 / 12 + 77 / 300 * k) + E * (27 / 100 * k - 603 / 20))
           + a * b * (-3 / 10 * B - 1.5 * k * B - 81 / 10 * E + 27 / 10 * k * E)
           + B * (a * c * (-284 / 15 + 56 / 15 * k) + b * c * (-132 + 24 * k))
           + b * b * (-45 / 2 * T - B * (225 / 4 + 63 / 4 * k) - E * (75 / 4 + 21 / 4 * k))
           - c * c * B * (160 / 3 + 8 / 3 * k) + Xi)
    gL = (k * E ** 3 + E * E * (6 * B + 2 * E) + E * (6 * T * B - 9 * B * B - 6 * B * E + 18 * B * B - E * E + 6 * E * E)
          + a * E * E * (9 - 9 / 5 * k) + (8 - 2 * k) * a * E * B + (3 * k - 3) * b * E * E + b * E * (18 * B + 6 * E)
          + (8 * k - 32) * c * E * B + a * a * E * (-549 / 20 + 27 / 100 * k) + a * a * (-39 / 10 * T - 21 / 10 * B - 27 / 10 * E)
          + a * b * E * (-81 / 10 + 27 / 10 * k) + b * b * E * (-45 / 4 - 21 / 4 * k) + b * b * (-45 / 2 * T - 45 / 2 * B - 15 / 2 * E) + Xi)
    gtau = ((6 + 2 * k) * E ** 3 + (6 * B + 2 * E) * E * E + E * (12 * T * B - 18 * B * B - 12 * B * E + 36 * B * B - 2 * E * E + 12 * E * E)
            + a * E * E * (9 / 5 + 9 / 5 * k) + b * E * E * (9 - 3 * k) + a * E * ((107 / 5 + 7 / 5 * k) * B + (9 / 5 + 9 / 5 * k) * E)
            + c * E * B * (16 * k - 64) + b * E * (B * (27 - 9 * k) + E * (9 - 3 * k))
            + a * a * E * (-1503 / 50 - 27 / 10 * k) + a * b * E * (-27 + 27 / 5 * k) + a * a * (-78 / 5 * T - 42 / 5 * B - 54 / 5 * E)
            + b * b * E * (-87 / 2 - 1.5 * k)
            + a ** 3 * (7899 / 125 - 597 / 125 * k) + a * a * b * (81 / 5 - 81 / 25 * k) + a * a * c * (264 / 5 - 264 / 25 * k))
    k3 = 1 / L16 ** 3
    return k3 * np.array([bg1, bg2, bg3, yt * (gQ + gt + gH2), yb * (gQ + gb + gH1), ytau * (gL + gtau + gH1), 0.0])


def mssm_rhs3(t, s, nu_on):
    return st.mssm_rhs2(t, s, nu_on) + mssm3_terms(s)
