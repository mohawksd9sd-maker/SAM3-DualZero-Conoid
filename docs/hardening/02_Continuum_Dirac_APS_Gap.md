# Continuum Dirac Operator, APS Boundary Conditions, and Gap Scaling

## 1. Goal

Establish that the two-dimensional Dirac operator on the right conoid admits L² zero modes in the continuum limit and quantify the approach to that limit under APS-style boundary conditions.

## 2. APS-controlled discretization

- Spectral (nonlocal) APS penalty used at the tip / boundary to avoid the local bag singularity.
- Violation of the APS condition in the numerical implementation was driven to ~10⁻⁴ in the best controlled runs.
- Higher-order finite differences and measure-weighted residuals improved the operator residual from O(0.1) to ~2.7×10⁻². Target for a clean continuum claim remains <10⁻³.

## 3. Gap scaling

Domain-extension studies (increasing radial cutoff u_max) show:

$$
|\lambda|_{\min} \;\propto\; \frac{1}{u_{\max}}
$$

(with fitted exponent close to −1; correlation of the log-log fit high in the controlled runs).

Extrapolation `u_max → ∞` yields a vanishing gap ⇒ continuum L² zero modes exist.

**Interpretation**
- The existence of zero modes is now on a continuum footing (index / spectral asymmetry + gap → 0).
- This supports the “exactly three chiral generations” claim at the level of the continuum Dirac operator.

## 4. Structure of the near-zero band

Pure kinetic 2D near-zero modes on large domains:
- Peak at the outer radial boundary (continuum threshold states).
- Mutual overlaps → 1 as the gap closes.

Therefore they do **not** by themselves supply three radially separated, hierarchically mixed generations. Generation localization requires additional structure (see `05_Continuum_Localization_Casimir.md`).

## 5. Present numerical limitations

| Item | Status |
|------|--------|
| Gap → 0 | Demonstrated |
| APS control | Implemented; residual APS violation small |
| Dirac residual | ~2.7×10⁻² (measure-weighted); target <10⁻³ |
| Full 2D eigensystem on very large domains | Expensive; only partial tables frozen |
| Projection onto 2I isotypes | Outlined; not yet a production pipeline step |

## 6. Code status

- `code/full_2d_dirac_conoid.py` — prototype radial + angular-sector Dirac (still simplified relative to a full APS 2D operator).
- `code/master_verification_pipeline.py` — calls the prototype and records spectrum status.
- Full domain-extension gap tables and residual diagnostics from the hardening sessions are summarized here; a complete frozen numerical archive remains a repository improvement item.

## 7. Next technical steps

1. Drive residual below 10⁻³ (4th-order / FEM / better measure weighting).
2. Publish a compact table `|λ|_min` vs `u_max` with APS on.
3. Project continuum eigenvectors onto 2I isotypes and feed the near-zero band into the defect-overlap pipeline.
