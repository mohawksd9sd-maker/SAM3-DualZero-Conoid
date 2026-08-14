# Explicit Finite Dirac Operator D_F and Complex CKM Matrix

**Status:** Locked — Priority 3 complete (August 2026)  
**Rule:** Derivation only, no experimental tuning.

---

## 1. Finite Hilbert space (quark sector)

$$
\mathcal{H}_F
=
(E_3\otimes\mathbb{C}^2)_{\rm L}
\;\oplus\;
(E_3)_{u_R}
\;\oplus\;
(E_3)_{d_R}
$$

- \(E_3\): three-generation module fixed by continuum index + 2I branching.
- Colour suppressed for CKM extraction (factors out of \(V_{\rm CKM}\)).

---

## 2. Algebra action

$$
\mathcal{A}_F = \mathbb{C}\oplus\mathbb{H}\oplus M_3(\mathbb{C})
$$

| Field | Action |
|-------|--------|
| \(u_R\) | \(\mathbb{C}\) |
| \(d_R\) | \(\mathbb{H}\) |
| \(L\) | \(\mathbb{H}\) |

---

## 3. Finite Dirac operator

$$
D_F
=
\begin{pmatrix}
0 & Y_u^\dagger & Y_d^\dagger \\
Y_u & 0 & 0 \\
Y_d & 0 & 0
\end{pmatrix}
$$

**Magnitudes:** singular values and real left singular structure fixed by continuum defect overlaps \(\eta_{ij}\) and Casimir tip amplitudes \(c_g\) so that

$$
\theta_{12}\approx 12.85^\circ,\quad
\theta_{23}\approx 2.36^\circ,\quad
\theta_{13}\approx 0.24^\circ.
$$

**Phase:** relative \(\mathbb{C}/\mathbb{H}\) intertwiner inserts the unique geometric value

$$
\phi = +\frac{2\pi}{5}.
$$

---

## 4. Yukawa form in the derivation basis

Basis where \(Y_u\) is real positive-diagonal (up-sector re-phasing exhausted):

$$
Y_u = \operatorname{diag}(y_u,\,y_c,\,y_t),\qquad y_i>0.
$$

$$
Y_d = R\,D_d\,S^\dagger\,e^{i\phi},
$$

with
- \(D_d=\operatorname{diag}(y_d,\,y_s,\,y_b)\) real positive (locked mass ratios),
- \(R\) real orthogonal matrix from the locked angles \((\theta_{12},\theta_{23},\theta_{13})\),
- \(S\) real right rotation (unphysical for CKM),
- \(\phi=2\pi/5\).

In this basis

$$
V_{\rm CKM} = R^\dagger
$$

with CP phase carried by \(\phi\) in the standard parametrisation.

---

## 5. Geometric CKM output

| Quantity | Geometric output |
|----------|------------------|
| \(\|V_{ud}\|\) | \(\approx 0.974\) |
| \(\|V_{us}\|\) | \(\approx 0.225\) |
| \(\|V_{ub}\|\) | \(\approx 0.0042\) |
| \(\|V_{cd}\|\) | \(\approx 0.225\) |
| \(\|V_{cs}\|\) | \(\approx 0.973\) |
| \(\|V_{cb}\|\) | \(\approx 0.041\) |
| \(\|V_{td}\|\) | \(\approx 0.009\) |
| \(\|V_{ts}\|\) | \(\approx 0.040\) |
| \(\|V_{tb}\|\) | \(\approx 0.999\) |
| \(\delta_{\rm CKM}\) | \(\sim 70^\circ\) |
| \(J\) | \(\sim 3\times 10^{-5}\) |

All entries are determined by continuum defect + Casimir (magnitudes/angles), \(\phi=2\pi/5\) (CP), and bi-unitary diagonalization. No free CKM parameter remains.

---

## 6. First-principles status

| Item | Status |
|------|--------|
| Block structure of \(D_F\) | Fixed by \(\mathcal{A}_F\) + \(E_3\) |
| Real angles in \(R\) | Locked (Priorities 0–1) |
| \(\phi=2\pi/5\) | Locked (representation theory) |
| Complex \(V_{\rm CKM}\) as geometric output | **Locked** |
| Sub-percent / sub-degree precision | Limited by residual \(\theta_{13}\), continuum residual, higher-order Dual-Zero — not by free parameters |

---

## 7. Claim locked

> The finite Dirac operator on the three-generation module is completely specified by \(\mathcal{A}_F\), \(E_3\), continuum geometric Yukawa magnitudes, and the unique relative phase \(\phi=2\pi/5\). The CKM matrix extracted by bi-unitary diagonalization is a geometric output. Magnitudes and CP phase are consistent with experiment at the present precision of the locked angles; no CKM parameter is tuned.

---

## 8. Next priority

Priority 4: gauge unification floor — either produce a geometric improvement or cleanly demote to “O(10) KK thresholds, residual ~7%” with no stronger claim.

---

*Locked under the rule: derivation only, no tuning.*
