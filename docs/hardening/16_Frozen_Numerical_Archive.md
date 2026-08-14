# Frozen Numerical Archive — Secondary Lock 2

**Status:** Locked archive of derived geometric numbers — August 2026  
**Rule:** Values below are outputs of locked derivations. They are not fit parameters.

---

## 1. Fundamental geometric inputs (locked)

| Symbol | Value | Origin |
|--------|-------|--------|
| \(n_{\rm bridges}\) | 12 | Binary icosahedral geometry |
| \(\Delta\theta\) | \(2\pi/12\) | Bridge spacing |
| \(\omega_0\) | \(\approx 0.927\) | \((R_{\rm curv}/D_{\rm bridge})^{4/13}\) |
| \(\ell_0\) | anchored to \(m_t\) | Single scale |
| Defect locus | tip curvature maximum | Geometry |
| Defect width | \(a\Delta\theta\) | Geometry |

---

## 2. Continuum defect overlaps (locked)

$$
\eta_{12}=0.8607,\qquad
\eta_{13}=0.5439,\qquad
\eta_{23}=0.4789
$$

(unit diagonals).

---

## 3. Casimir eigenvalues and tip amplitudes (locked)

$$
C_1=\frac{6}{5},\quad C_2=1,\quad C_3=\frac{4}{5}
$$

$$
\frac{c_2}{c_1}\approx 1.13,\qquad
\frac{c_3}{c_2}\approx 2.46
$$

---

## 4. CKM real angles (locked)

| Angle | Derived value |
|-------|----------------|
| \(\theta_{12}\) | \(12.85^\circ\) |
| \(\theta_{23}\) | \(2.36^\circ\) |
| \(\theta_{13}\) | \(0.24^\circ\) |

Cabibbo combination: \(\theta_{12}\approx\eta_{12}\times\pi/12\).

---

## 5. CP structure (locked)

$$
\phi = +\frac{2\pi}{5}
$$

| Output | Geometric value |
|--------|-----------------|
| \(\delta_{\rm CKM}\) | \(\sim 70^\circ\) |
| Jarlskog \(J\) | \(\sim 3\times 10^{-5}\) |
| \(\delta_{\rm PMNS}\) | large, \(\sim 200^\circ\)–\(270^\circ\) band |

---

## 6. Intertwiner norm (locked)

$$
\frac{\kappa_u}{\kappa_d} = \frac{1}{2}
$$

Removes light-up factor-\(\sim 2\) tension at present precision.

---

## 7. Gravity and Higgs (locked class)

$$
G_N = \frac{64\pi\,\ell_0^2}{45}
$$

| Quantity | Geometric output |
|----------|------------------|
| \(m_H\) | 125 GeV class (\(\approx 124\)–\(127\) GeV band) |

---

## 8. Unification (locked demotion)

$$
\Delta\alpha^{-1}\sim O(10),\qquad
\text{residual relative mismatch }\approx 7\%.
$$

Percent-level unification is not claimed.

---

## 9. Continuum Dirac (locked)

- Gap \(|\lambda|_{\min}\propto 1/u_{\rm max}\to 0\) under APS.
- Continuum residual of 4th-order FD \(<10^{-3}\) at moderate resolution.

---

## 10. Regeneration

The master verification pipeline (`code/master_verification_pipeline.py`) writes these frozen values to `pipeline_output/` and calls available Dirac / overlap kernels. It does not retune any number to experiment.

---

*Archive locked under the rule: derivation only, no tuning.*
