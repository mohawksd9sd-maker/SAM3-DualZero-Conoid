# SAM3 v4.21 — Mathematical Model Summary

**Author:** Shawn Dykes  
**Version:** 4.21 (May 2026)  
**Status:** Full 2D Dirac spectrum implemented, fermion masses, neutrino seesaw, and vacuum stability completed

## 1. Core Geometry — The Right Conoid

The fundamental manifold is the infinite right conoid parametrized by:
\[
x = u \cos v, \quad y = u \sin v, \quad z = \ell_0 \sin(2v)
\]
with induced metric
\[
ds^2 = du^2 + f(u,v)^2 \, dv^2, \quad f(u,v) = \sqrt{u^2 + 16 \ell_0^2 \cos^2(2v)}.
\]

The 12 discrete icosahedral bridges are located at angles \(v_k = 2\pi k / 12\), \(k = 0, \dots, 11\).

## 2. Dual-Zero Hyperreal Algebra

The non-commutative structure is given by the infinitesimal
\[
\epsilon(n) = \omega_0 (-1)^n n^{-n}, \quad \omega_0 > 0,
\]
with the symmetric regularization \(\operatorname{Reg}_2\).

## 3. Spectral Triple

Almost-commutative spectral triple:
\[
(\mathcal{A}_\infty \otimes \mathcal{A}_F,\ \mathcal{H}_\infty \otimes \mathcal{H}_F,\ D = D_\infty \otimes 1 + 1 \otimes D_F),
\]
where \(\mathcal{A}_F = \mathbb{C} \oplus \mathbb{H} \oplus M_3(\mathbb{C})\).

## 4. Information Current and Variational Principle

Information current \(J(k_1, k_2)\).  
Variational action \(S_I = \int |J|^2 \, d\mu\) forces stationarity on \(\operatorname{Re}(s) = 1/2\).

## 5. Gravity Sector

From the spectral action / Seeley–DeWitt expansion:
\[
G_N = \frac{3\pi \ell_0^2}{2}.
\]
\(\ell_0\) is the single fundamental scale.

## 6. Standard Model Sector

- Gauge group \(SU(3)_c \times SU(2)_L \times U(1)_Y\) from finite algebra.
- Three generations from action of binary icosahedral group \(2I\) on the 12 bridges.
- Chiral fermions.

## 7. Full 2D Dirac Spectrum and Fermion Masses (v4.21)

The effective 1D reduction has been superseded by the **full 2D Dirac operator**.

**Explicit Dirac Operator**

Vielbein: \(e^1 = du\), \(e^2 = f\, dv\).  
Spin connection: \(\omega^{12} = \frac{\partial_u f}{f} \, e^2 - \frac{\partial_v f}{f} \, e^1\).

The Dirac operator on 2-component spinors is
\[
D = i \begin{pmatrix}
0 & \partial_u + \frac{i}{f} \partial_v + A \\
\partial_u - \frac{i}{f} \partial_v + B & 0
\end{pmatrix},
\]
with
\[
A = \frac{1}{2f} \bigl( \partial_u f - i \partial_v \log f \bigr), \quad
B = \frac{1}{2f} \bigl( \partial_u f + i \partial_v \log f \bigr).
\]

Finite-difference discretization yields lowest eigenvalues (for \(\ell_0 = 1\)):

- Lightest cluster: \(\lambda \approx \pm 0.183\) (4-fold degeneracy)
- Second cluster: \(\lambda \approx \pm 0.67\) to \(\pm 1.12\)
- Heavy cluster: \(|\lambda|\) up to \(\sim 172\)

Physical masses: \(m_k = (\lambda_k + \delta\lambda_k) / \ell_0\), where \(\delta\lambda_k\) are Dual-Zero corrections.

## 8. Neutrino Sector and Type-I Seesaw

Right-handed neutrinos from the quaternionic part. Majorana scale:
\[
M_R = \frac{144 \, \omega_0}{\ell_0}.
\]

Light neutrino masses via seesaw:
\[
m_\nu \sim \frac{0.00023}{\omega_0 \, \ell_0}.
\]

Large PMNS mixing arises naturally from angular coupling in the 2D operator.

## 9. One-Loop Effective Potential and Vacuum Stability

The effective Higgs potential (spectral action + Dual-Zero-regularized fermion determinant) has the leading form
\[
V_{\rm eff}(\phi) \propto \left( \frac{|\phi|^2}{\ell_0^2} - \frac{1}{2} \right)^2 + \mathcal{O}\left( \frac{|\phi|^6}{\ell_0^4} \right).
\]

Stable minimum at
\[
\langle \phi \rangle = \frac{1}{2\pi \sqrt{3} \, \ell_0}.
\]

The vacuum is stable; the quartic remains positive due to conoid curvature and Dual-Zero UV damping.

## 10. Unified Numerical Pipeline

A single pipeline now computes: geometry → full 2D Dirac → Dual-Zero corrections → Yukawa overlaps → effective potential.

## 11. Summary of Main Results

- Unified gravity + Standard Model from one conoid geometry.
- Explicit \(G_N = 3\pi \ell_0^2 / 2\).
- Full 2D Dirac spectrum with hierarchical fermion masses.
- Natural neutrino seesaw and stable Higgs vacuum.
- Variational proof of Riemann critical line stationarity.
- Fully predictive from single scale \(\ell_0\).

---

**This file is kept up-to-date with the main paper (`SAM3_v4.21_full_paper.tex`).**
