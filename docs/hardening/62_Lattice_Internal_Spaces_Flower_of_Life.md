# 62. Lattice internal spaces: hexagonal T² and its orbifolds ("Flower of Life"), and D₄ T⁴ / T⁴/ℤ₃ ("4D Flower of Life") (exploratory)

**Date:** 23 November 2026 (America/Chicago)
**Status:** exploratory. The **Dual-Zero regulator is untouched**: nothing here uses or changes \(\varepsilon(n)=\omega_0(-1)^nn^{-n}\) or \(\operatorname{Reg}_2\).
**Code:** `experiments/two_loop_pati_salam/lattice_geometries.py` and `report_62.py`; numbers in `results_doc62.json`.
**Tests:** `tests/test_lattice_geometries.py`.
**Context:** two further rows for the doc 61 structure search (Shawn asked about the "Flower of Life", then approved the 4D version).

> **Plain note.** The Flower of Life pattern itself is 2D decoration: circles drawn on a plane carry no Dirac operator, flux or spectrum. Only the lattice it is built on can be tested. That is the hexagonal lattice \(A_2\), which gives the torus with \(\tau=e^{i\pi/3}\) and its ℤ₃/ℤ₆ orbifolds. The "4D Flower of Life" is likewise tested as the \(D_4\) lattice (24-cell, kissing number 24), which gives \(T^4=\mathbb R^4/D_4\) and its ℤ₃ orbifold. Nothing below depends on the drawing.

---

## Plain-language summary (for Shawn)

- **Hexagonal ("Flower of Life") surface.**
  - **Generations.** It does not force three generations. On the plain hexagonal torus, the number of generations equals the magnetic flux, so 3 is a choice. On the ℤ₃ and ℤ₆ folded versions, a 3-generation sector appears at several fluxes (M = 6, 8, 10 for ℤ₃; M = 12, 14, 16 for ℤ₆). My mode counts reproduce the published tables exactly.
  - **Heavy extra fermions.** It forces none.
  - **Top coupling.** One surprise: the Yukawa pattern it produces is "democratic", with all three generations at similar strength. That share would pull the top coupling down by about the 20% needed, giving a top near 172–174 GeV for typical Higgs directions. **But** the same pattern makes the charm quark about 60% as heavy as the top instead of 0.3%. Read honestly, it is ruled out.
  - **Using the share via heavy partners.** The only way to keep the share would be to make two of the three geometric modes heavy partners, not the charm and up quarks. That is extra structure plus free choices, and the Higgs still comes out at 140–146 GeV.
- **D₄ ("4D Flower of Life") space.**
  - **What I checked.** The lattice facts all check out: 24 unit vectors, a 3-fold symmetry with 9 fixed points, and a smoothed version that is the K3 surface (Euler number 24, the same 24).
  - **Generations.** It does not force three generations either. On \(T^4\) the count is a flux determinant that can be any integer. On \(T^4/\mathbb Z_3\) or K3, three generations come out for ten different flux and fixed-point choices.
  - **Heavy extra fermions.** None are forced.
  - **Result.** Top 190.4 GeV and Higgs 180.5 GeV, unchanged from doc 60.
  - **Size of the space.** This makes spacetime 8-dimensional. The Pati–Salam unification survives only if the D₄ space is as small as the cutoff length. If even one layer of its extra modes (24 of them) sat below the unification scale, the unification would shift by about 5%.
- **Bottom line.** Neither lattice is a fix. The hexagonal one shows a pattern that *would* fix the top, but only by making the charm as heavy as the top. The D₄ one changes nothing. Dual-Zero is untouched in both.

---

## 1. Hexagonal \(T^2\), \(\tau=e^{i\pi/3}\), and \(T^2/\mathbb Z_3\), \(T^2/\mathbb Z_6\)

### 1.1 Zero-mode counting

**Method.**
- The flux-\(M\) zero modes are the CIM wavefunctions (`alt_geometries/magnetized_torus.py`).
- The ℤ_N rotation \(z\mapsto\rho z\), \(\rho=e^{2\pi i/N}\), is obtained numerically by least squares from \(\psi^j(\rho z)=\sum_k\psi^k(z)C_{kj}\).
- For even \(M\) the action closes: residual \(\sim10^{-15}\) and \(C^N\propto1\). Its eigenvalue multiplicities give the sector dimensions.
- The **Kobayashi–Nagamoto tables (arXiv:1709.09784) are reproduced exactly** for ℤ₃ and ℤ₆ at \(M=2,\dots,12\).
- For odd \(M\) the action does not close at zero Scherk–Schwarz phase (residual ≈ 0.8). Odd fluxes need non-zero SS phases, which are not computed here.

| ℤ_N | \(M\) with a 3-dim invariant sector | \(M\) with some 3-dim sector |
|---|---|---|
| ℤ₃ | 6, 8, 10 | 6, 8, 10, 12 |
| ℤ₆ | 12, 14, 16 | 12–24 (all even) |
| none (plain \(T^2\)) | \(M=3\) (index = flux) | — |

- **Three generations are allowed for several fluxes, not forced.** This matches doc 49 for the other ℤ_N.
- The index counts only net chirality, and for \(M>0\) there are no opposite-chirality zero modes. **No vector-like zero modes are forced, so no fixed count of heavy fermions.**
- The massive Landau levels are the towers of doc 61 (4), whose contribution to \(y_t/g\) cancels identically.

### 1.2 Yukawa texture

Triple overlaps \(Y_{ijk}=\int\psi_i^{(I)}\psi_j^{(J)}\overline{\psi_k^{(I+J)}}\) are computed at the hexagonal point with no Wilson lines. Ratios \(\sigma_2/\sigma_1,\ \sigma_3/\sigma_1\) of the 3×3 Yukawa:

| geometry | Higgs directions | ratios (per Higgs basis direction) | random Higgs direction: median \(\sigma_2/\sigma_1\), min |
|---|---|---|---|
| \(T^2\), flux (3,3,6) | 6 | (0.162, 0.162) or (1.000, 0.053) | 0.63, 0.24 |
| \(T^2/\mathbb Z_3\), \(M=6\) invariant (3×3×5) | 5 | (0.31, 0.20), (0.78, 0.23), (0.54, 0.30), (0.61, 0.28), (0.66, 0.26) | 0.65, 0.24 |

- The symmetric point produces exact degeneracies (ℤ₃ symmetry of the overlaps).
- In 200 random Higgs directions, none gives \(\sigma_2/\sigma_1<0.01\). The data need \(y_c/y_t\approx2.6\times10^{-3}\) at \(10^{15}\) GeV.
- **The texture is O(1), not hierarchical.**

### 1.3 Through the two-loop pipeline

The spectral boundary sees the light generations only through their share of \(\operatorname{Tr}Y^\dagger Y\). Here \(x=(3+n)\,(\sigma_2^2+\sigma_3^2)/\sigma_1^2\) (doc 61 notation, quarks plus PS leptons).

| case | light share | \(M_t\) (GeV) | \(M_h\) (GeV) | implied \(m_c/m_t\) |
|---|---|---|---|---|
| measured hierarchy (any geometry) | \(7\times10^{-6}\) | 190.36 | 180.5 | 0.0026 (data) |
| \(T^2\) (3,3,6), Higgs basis direction A | 0.053 | 188.3 | 175.6 | 0.16 (and \(m_u=m_c\)) |
| \(T^2\) (3,3,6), Higgs basis direction B | 1.003 | 160.0 | 133.4 | 1.0 |
| \(T^2\) (3,3,6), median random Higgs | 0.49 | **173.5** | 145.3 | 0.63 |
| \(T^2/\mathbb Z_3\), Higgs basis directions | 0.14–0.65 | 185.1–168.8 | 168.4–140.6 | 0.31–0.78 |
| \(T^2/\mathbb Z_3\), median random Higgs | 0.55 | **171.7** | 142.1 | 0.65 |

**Reading.**
- The democratic hexagonal texture supplies almost exactly the extra trace that doc 61 needed (\(x\approx2.1\)). This is a genuine, non-tuned observation.
- But it is the trace of the *light generations*, and it implies \(m_c/m_t\approx0.6\), about 240 times the data. **As a model of the three SM generations it is excluded.**
- Using the share legitimately would require the second and third geometric modes to be heavy partners (paired with a mirror flux sector, Dirac mass ≥ \(m_R\)) rather than \(c\) and \(u\). The light generations would then have to come from elsewhere.
- That is the doc 61 vector-like row with extra unforced structure and a free Higgs direction. It gives \(M_h\approx140\)–146 GeV, which fails like doc 61 (2).

**Row verdict.**
- Added parameters: flux \(M\) (discrete) and the Higgs direction (continuous).
- \(M_t\): 190.4 with data-consistent textures; 160–188 with geometric textures, which are excluded by \(m_c/m_t\).
- \(M_h\): 133–181.
- Dual-Zero: intact.

## 2. D₄ lattice: \(T^4=\mathbb R^4/D_4\) and \(T^4/\mathbb Z_3\) (8D total)

### 2.1 Lattice facts (computed)

- **Units.** \(D_4\) is realized as the Hurwitz quaternions. There are **24** units, the vertices of the 24-cell and the kissing number. The shell counts are 24, 24, 96, 24, 144, 96 for norms 1–6.
- **ℤ₃ action.** Left multiplication by \(\omega=(-1+i+j+k)/2\) is an integer matrix of order 3 with eigen-angles ±120° (each twice). It is fixed-point-free on \(\mathbb R^4\), the SU(2)-type action.
- **Fixed points.** \(|\det(1-L_\omega)|=9\).
- **Euler numbers.** \(\chi(T^4/\mathbb Z_3)=6\). Resolving the nine \(A_2\) singularities gives \(\chi=24\): **this is the K3 surface**. The match \(\chi(\mathrm{K3})=24\) = kissing number of \(D_4\) is noted, but nothing below uses it.
- **Not a product of two hexagonal lattices.** \(D_4\neq A_2\oplus A_2\): with roots of norm 2, \(\det D_4=4\) and \(\det(A_2\oplus A_2)=9\), so the index squared, 9/4, is not an integer.

### 2.2 Index counting

- **On \(T^4\).** For an integer flux 2-form \(n_{ab}\), \(\operatorname{Ind}=\operatorname{Pf}(n)\). Over all \(n_{ab}\in\{-2,\dots,2\}\) (15 625 fluxes), \(|\operatorname{Pf}|=3\) occurs for 10.9%. **Not forced.**
- **On \(T^4/\mathbb Z_3\)** (Lefschetz fixed-point formula, each fixed point contributing \(\chi_p/3\) per twist):
  - \(n_{\rm inv}=\tfrac13[\operatorname{Pf}+a-3]\), where \(a\) is the number of fixed points with trivial flux phase.
  - Check: with no flux, \(n_{\rm inv}=2=\hat A(\mathrm{K3})\).
  - Three generations occur for **ten** \((\operatorname{Pf},a)\) pairs: (3,9), (4,8), …, (12,0). **Not forced.**
- **On K3 with a line bundle.** \(\operatorname{Ind}=2+c_1^2/2\), with \(c_1^2\) even, so any integer is possible and 3 occurs at \(c_1^2=2\).
- **Vector-like states.** None are forced. The index fixes only net chirality, and twisted or blow-up modes are not fixed in number by the index.

### 2.3 Yukawa structure and the pipeline

- **Texture.** \(D_4\) is not a product lattice, so the overlaps are genus-2 theta functions on a non-factorizable abelian surface, which are not computed here. For the closest factorizable ℤ₃-symmetric choice, \(T^2_{\rm hex}\times T^2_{\rm hex}\) with flux (3,1), the texture is that of §1.2, so the conclusion of §1.3 applies.
- **Data-consistent texture.** Any texture consistent with the measured hierarchy gives \(x\approx0\).

| row | added params | \(M_t\) | \(M_h\) |
|---|---|---|---|
| D₄ \(T^4\) / \(T^4/\mathbb Z_3\) / K3, chiral index only | flux, fixed-point phases (discrete), \(M_c\) | **190.4** | **180.5** |

### 2.4 Does Pati–Salam unification survive in 8D?

**Gauge KK modes.** Each KK momentum carries a massive vector plus 3 real adjoint scalars:
- \(\Delta b=-3C_2(G)\);
- \(\Delta(\alpha_4^{-1}-\alpha_L^{-1})=6\,\ln(\Lambda/m_k)/2\pi\) per state.

| \(M_c/\Lambda\) | KK states below \(\Lambda\) | shift of \(\alpha_4^{-1}-\alpha_L^{-1}\) | relative to \(\alpha_4^{-1}\approx44.6\) |
|---|---|---|---|
| 1.0 | 0 | 0 | 0 |
| 0.9 | 24 (first shell) | 2.4 | 5% |
| 0.7 | 48 | 8.4 | 19% |
| 0.5 | 144 | 37 | 83% |

**Consequences.**
- The doc 55 two-loop meeting survives only if \(M_c\gtrsim\Lambda\), meaning the internal \(D_4\) torus is no larger than the cutoff length.
- In that regime the spectral action over the internal space is a lattice sum rather than a heat-kernel expansion. The gauge and Higgs kinetic terms of constant zero-mode fields get the same internal factor, so the boundary relation \(y_t^2a=4g^2\) and the PS spectral content are unchanged. That is why the row reproduces doc 60.
- The 4D Planck mass picks up the internal volume. This is not studied here.

**Row verdict.**
- Added parameters: flux matrix, fixed-point phases, \(M_c\ge\Lambda\).
- \(M_t\) 190.4, \(M_h\) 180.5.
- No forced 3 generations and no forced vector-like count.
- Dual-Zero intact.

## 3. Rows added to the doc 61 ranking

| structure | added params | \(M_t\) (GeV) | \(M_h\) (GeV) | forced 3 gens? | forced VL count? | testable output | Dual-Zero |
|---|---|---|---|---|---|---|---|
| hex \(T^2\) / \(T^2/\mathbb Z_{3,6}\) ("Flower of Life" lattice) | flux (discrete), Higgs direction | 190.4 (data texture); 160–188 (geometric texture) | 133–181 | no (M = 3; 6, 8, 10; 12, 14, 16) | no | geometric texture implies \(m_c/m_t\approx0.2\)–1: **excluded** | intact |
| D₄ \(T^4\) / \(T^4/\mathbb Z_3\) → K3 ("4D Flower of Life", 8D) | flux, fixed-point phases, \(M_c\ge\Lambda\) | 190.4 | 180.5 | no (10 solutions on \(T^4/\mathbb Z_3\)) | no | unification requires \(M_c\gtrsim\Lambda\) | intact |

Both rows rank below the doc 61 vector-like candidate. Neither supplies a forced extra Higgs-coupled trace. The hexagonal texture supplies the right *size* of trace, but in the wrong place: in the light generations, where the data forbid it.

## 4. Approximations

- Overlaps are computed on a 36×36 grid (ratios agree with a 48×48 grid to better than \(10^{-6}\)). Odd-flux orbifold sectors and non-zero Wilson lines and SS phases are not computed.
- The \(T^4/\mathbb Z_3\) count uses the Lefschetz formula with the stated fixed-point normalization, checked only against \(\hat A(\mathrm K3)=2\).
- The \(D_4\) Yukawa overlaps are not computed (non-factorizable).
- The KK-shift estimate uses one-loop, universal adjoint content per KK momentum, and no matter KK modes.
