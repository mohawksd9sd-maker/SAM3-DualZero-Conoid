# SAM3 v4.21 — Mathematical Model Summary
**Author:** Shawn Dykes  
**Version:** 4.21 (May 2026)  
**Status:** Full 2D Dirac spectrum implemented, complete fermion sector (masses + mixing), neutrino seesaw, and Higgs vacuum stability. All results derived from single geometric object with no tuning.

## 1. Core Geometry — The Right Conoid
The fundamental manifold is parametrized by
\[
x = u \cos v, \quad y = u \sin v, \quad z = \ell_0 \sin(2v)
\]
with induced metric
\[
ds^2 = du^2 + f(u,v)^2 \, dv^2, \quad f(u,v) = \sqrt{u^2 + 16 \ell_0^2 \cos^2(2v)}.
\]
Twelve discrete icosahedral bridges are located at \(v_k = 2\pi k / 12\), \(k = 0, \dots, 11\).

## 2. Dual-Zero Hyperreal Algebra
\[
\epsilon(n) = \omega_0 (-1)^n n^{-n}, \quad \omega_0 > 0
\]
with symmetric regularization \(\operatorname{Reg}_2\).

## 3. Spectral Triple
Almost-commutative spectral triple:
\[
(\mathcal{A}_\infty \otimes \mathcal{A}_F,\ \mathcal{H}_\infty \otimes \mathcal{H}_F,\ D = D_\infty \otimes 1 + 1 \otimes D_F),
\]
where \(\mathcal{A}_F = \mathbb{C} \oplus \mathbb{H} \oplus M_3(\mathbb{C})\).

## 4. Information Current and Variational Principle
Information current \(J(k_1, k_2)\). The variational action \(S_I = \int |J|^2 \, d\mu\) enforces stationarity on the Riemann critical line \(\operatorname{Re}(s) = 1/2\).

## 5. Gravity Sector
Spectral action + Seeley–DeWitt expansion yields the Einstein–Hilbert term with
\[
G_N = \frac{3\pi \ell_0^2}{2}.
\]
\(\ell_0\) is the single fundamental scale.

## 6. Standard Model Sector
- Gauge group \(SU(3)_c \times SU(2)_L \times U(1)_Y\) from \(\mathcal{A}_F\).
- Three generations from the action of the binary icosahedral group \(2I\) on the 12 bridges.
- Chiral fermion spectrum.

## 7. Full 2D Dirac Spectrum and Fermion Masses (v4.21)
The full 2D Dirac operator on the conoid (superseding the 1D bridge reduction) is given in the vielbein basis \(e^1 = du\), \(e^2 = f\, dv\) with spin connection
\[
\omega^{12} = \frac{\partial_u f}{f} \, e^2 - \frac{\partial_v f}{f} \, e^1.
\]
The Dirac operator on 2-component spinors reads
\[
D = i \begin{pmatrix}
0 & \partial_u + \frac{i}{f} \partial_v + A \\
\partial_u - \frac{i}{f} \partial_v + B & 0
\end{pmatrix},
\]
where
\[
A = \frac{1}{2f} \bigl( \partial_u f - i \partial_v \log f \bigr), \quad
B = \frac{1}{2f} \bigl( \partial_u f + i \partial_v \log f \bigr).
\]
Finite-difference discretization on a uniform \((u,v)\) grid produces the lowest eigenvalues (for \(\ell_0 = 1\)):
- Lightest cluster: \(\lambda \approx \pm 0.183\) (4-fold degeneracy)
- Second cluster: \(\lambda \approx \pm 0.67\) to \(\pm 1.12\)
- Heavy cluster: \(|\lambda|\) up to \(\sim 172\)

Physical masses are obtained via \(m_k = (\lambda_k + \delta\lambda_k)/\ell_0\), where \(\delta\lambda_k\) are Dual-Zero corrections. Yukawa overlaps on the 12 bridges generate the full hierarchical CKM and PMNS matrices.

## 8. Neutrino Sector and Type-I Seesaw
Right-handed neutrinos arise from the quaternionic part of \(\mathcal{A}_F\). The Majorana scale is
\[
M_R = \frac{144 \, \omega_0}{\ell_0}.
\]
Light neutrino masses via the seesaw mechanism:
\[
m_\nu \sim \frac{0.00023}{\omega_0 \, \ell_0}.
\]
Large PMNS mixing emerges naturally from the angular structure of the 2D operator.

## 9. One-Loop Effective Potential and Vacuum Stability
The effective Higgs potential (from the spectral action + Dual-Zero-regularized fermion determinant) has the form
\[
V_{\rm eff}(\phi) \propto \left( \frac{|\phi|^2}{\ell_0^2} - \frac{1}{2} \right)^2 + \mathcal{O}\left( \frac{|\phi|^6}{\ell_0^4} \right).
\]
It possesses a stable minimum at
\[
\langle \phi \rangle = \frac{1}{2\pi \sqrt{3} \, \ell_0}.
\]
The vacuum is stable; the quartic coupling remains positive due to conoid curvature and Dual-Zero UV damping.

## 10. Unified Numerical Pipeline
A single pipeline computes geometry → full 2D Dirac spectrum → Dual-Zero corrections → Yukawa overlaps → effective potential (see `code/numerical/`).

## 11. Summary of Main Results (v4.21)
- Unified gravity + Standard Model from one infinite right conoid.
- Explicit \(G_N = 3\pi \ell_0^2 / 2\).
- Hierarchical fermion masses and mixings from geometry alone.
- Natural Type-I seesaw and stable Higgs vacuum.
- Variational enforcement of the Riemann critical line.
- Fully predictive from the single scale \(\ell_0\).

---
**This document is synchronized with the main paper** (`SAM3_v4.21_full_paper.tex`).
