# SAM-3 / Riemann zeros: identification test results

**Date:** Monday, Nov 23, 2026, about 10:35 AM CT (America/Chicago)  
**Work copy:** `/workspace/sam3-work` (clone of https://github.com/mohawksd9sd-maker/SAM3-DualZero-Conoid, commit `b671e8b`).  
**Nothing was pushed, and the GitHub repo was not edited.**

This is a numerical test of whether the information current in SAM-3 can be identified with the Riemann zeta function, or whether its critical points coincide with the nontrivial zeros. The locked documents already treat that identification as an open gap, not a theorem (`docs/hardening/27_RH_Variational_Residual_Lock.md`, `STATUS_CLAIMS_AND_RESIDUALS.md`).

## 1. The original scripts are tautological

Both originals were run unchanged (`MPLBACKEND=Agg`).

### `code/verification/zeta_stationarity.py`

It reported **50/50 YES**, every zero “stationary,” with the same values every time: `J = 2.0000` and `dJ/dσ = -2.22e-10`. That already shows `J` does not depend on `t`.

The tautology demo evaluates the *same* formula at midpoints between zeros and at random `t` on the line `σ = 1/2`:

| set        | n  | “YES” (`|dJ/dσ| < 1e-4`) |
|------------|----|---------------------------|
| zeros      | 50 | 50/50                     |
| midpoints  | 49 | 49/49                     |
| random `t` | 49 | 49/49                     |

`J(σ,t)` is a function of `|σ - 1/2|` only. It never uses Dual-Zero weights, Dirac eigenvalues, or 12-bridge overlaps. Anything with real part `1/2` “passes,” including points that are not zeros.

### `code/zeta_stationarity_enhanced.py`

The original run printed **3/20 YES**. That is not a real rejection of the other 17 zeros. The finite-difference shift moves `k1` and `conjugate(k2)` by the same real amount, so `k1 - k2 = 2it` never changes and the gradient is identically zero whenever `J` is finite. For larger `t`, `sin(12 · 2it) = i sinh(24t)` overflows to `nan`, and those rows are scored “NO.”

The same formula, applied to the first 20 zeros’ window:

| set        | n  | “YES” (finite and `grad = 0`) |
|------------|----|--------------------------------|
| zeros      | 20 | 3/20                           |
| midpoints  | 19 | 3/19                           |
| random `t` | 19 | 10/19                          |

Random `t` “passed” more often than the zeros, because more of those samples happened to be small enough to avoid overflow. Logs: `identification_results/tautology_demo.json`, `zeta_stationarity_original.out`, `zeta_stationarity_enhanced_original.out`.

Corrected counterparts sit beside the originals and use a genuine 2-D gradient of a Dual-Zero / conoid `J` (sections 3–4).

## 2. What was built for a non-circular test

Script: `code/verification/zeta_identification_test.py`.

**Repo definitions used**

- Locked metric `f = √(u² + 4ℓ₀² cos²(2v))` in `code/dirac_conoid_aps.py`.
- `ω₀ = 0.927` from `code/sam3_geometry_constants.py` / doc 18.
- Dual-Zero generator `ε(n) = ω₀ (-1)ⁿ n^{-n}` and `Reg₂(a)_n = (a_{2n}+a_{2n+1})/2` from `code/dual_zero_constructive.py` and doc 18.
- Spectral zeta language `ζ_D(s) = Tr |D|^{-s}` from `docs/hardening/37_Regulator_Comparison_DZ_vs_HeatKernel_Zeta.md`.
- Action density `S_I = |J|²` as the pointwise form of `S_I = ∫ |J|² dμ` in doc 27.
- 12-bridge overlap kernel from `code/overlap_integrals.py` (reproduced, because that module plots on import).
- `N_BRIDGES = 12`.

**Assumptions required because `J` is not uniquely defined**

Paper 11 and `SAM3_RH_Variational_Proposal.tex` are supersession stubs. They do not give a formula that turns “conoid spectral data + overlaps + Dual-Zero” into `J(k)`. Four assemblies were therefore tested, none of which hard-codes a peak at `σ = 1/2` or inserts zeta zeros into `J`. Zeros enter only afterwards, as a comparison list, together with midpoints and random `t`.

| ID | Assembly |
|----|----------|
| A (primary) | Ordered Dirac mode tower, `J_A(s) = sum Reg₂( |λ_n|^{-s} ε(n) )` |
| B | Same eigenvalues, unweighted `Tr |D|^{-s}` (so Dual-Zero cannot be blamed for a null result by erasing the tower) |
| C | Overlaps as a Dirichlet series `C_{ij} (1+d_{ij})^{-s}`, Dual-Zero / Reg₂ summed in row-major order |
| D | Laplace–Fourier transform `Ĉ(s) = Σ C_{ij} exp(-s(θ_i-θ_j))`, `θ_k = 2π k/12` |

Dirac data: full dense spectrum of the APS matrix at `Nu=24`, `Nv=32`, `u_max=6`, `ℓ₀=1` (1536 eigenvalues). 128 APS-penalty modes with `|λ| > 20` were dropped; 1408 modes were kept, with `|λ| ∈ [0.084, 10.32]`. Search window: `σ ∈ [0.10, 0.90]`, `t ∈ [5, 200]` (79 of the first 80 zeros fall in that window; `t_1 = 14.13`, `t_79 = 198.02`). Grid steps `Δσ ≈ 0.025`, `Δt = 0.25`, then L-BFGS-B refinement. Seed `20261123`.

**Controls:** midpoints between consecutive zeros; random `t` in the same window (same count); shuffled `|λ_n|` order for A; a fake log-uniform spectrum with the same count and range for B; a joint permutation of bridge labels for C.

Identification would require discovered `t`-values to sit *clearly closer* to known zeros than to those controls, and 2-D critical points to prefer `σ = 1/2` if one takes doc 27’s internal selection principle at face value.

## 3. Results

Median distance from each known zero (and from each control point) to the nearest discovered feature, along `σ = 1/2` unless noted:

| construction | # minima of `S_I(1/2+it)` | median dist, zeros | midpoints | random `t` |
|--------------|---------------------------|--------------------|-----------|------------|
| A Dual-Zero spectral zeta | 1 | 57.05 | 56.40 | 74.35 |
| B plain `Tr\|D\|^{-s}` | 68 | 0.815 | 0.798 | 0.744 |
| C overlap Dirichlet + Dual-Zero | 22 | 2.580 | 2.596 | 2.108 |
| D overlap Laplace–Fourier | 178 | 0.229 | 0.288 | 0.286 |
| A, shuffled mode order | 15 | 3.330 | 3.012 | 4.052 |
| B, fake log-uniform spectrum | 82 | 0.599 | 0.599 | 0.574 |
| C, permuted bridge labels | 22 | 2.580 | 2.596 | 2.108 |

### A (primary, closest to docs 18 and 37)

`S_I(1/2+it)` is almost flat: it falls slowly from about 1.5667 to 1.5643, a change in the fourth decimal place, with a single shallow minimum near `t = 180`. Zeros simply lie on that smooth curve and have no special status. Dual-Zero’s `n^{-n}` weights already kill the tower by `n ≈ 8`, so only the lowest few Dirac modes matter. No 2-D critical points were found in the strip. Gradient of `S_I` at `σ = 1/2` is the same at zeros, midpoints, and random `t` (median `|∇S_I| ≈ 7.75` for all three). **No evidence of identification.**

### B (unweighted spectral zeta)

Many oscillations, 68 line minima. Median distances to zeros, midpoints, and random `t` are all about 0.7–0.8. Random `t` is slightly *closer* than the zeros. A fake log-uniform spectrum of the same size matches zeros just as well as the real Dirac spectrum (median 0.599 vs 0.599 vs 0.574). 2-D stationary points have median `σ ≈ 0.41`, not `1/2`. **No evidence of identification; the apparent “nearness” is the spacing of a crowded feature list.**

### C (overlap Dirichlet)

The line signal is nearly periodic with period `≈ 9.06 = 2π / log 2`, which is exactly the period of `(1+d)^{-it}` for the first off-diagonal distance `d = 1`. Zeros land at essentially random phases of that oscillation; many sit near peaks, not minima. Median distances: zeros 2.58, midpoints 2.60, random `t` 2.11 (random is closer). Permuting bridge labels barely changes the minima, because Dual-Zero again keeps only the first few flattened entries. **No evidence of identification. The pattern is the arithmetic of `2^{-s}`, not the Riemann zeros.**

### D (overlap Laplace–Fourier)

`S_I(1/2+it)` is a train of sharp spikes with period **12**, the 12-bridge angular spacing. Minima fill the valleys and sit at nearly every integer in `[6, 199]` (178 of them). A feature list that dense will fall within `≈ 0.25` of almost any comparison set; the slightly smaller median for zeros (0.229 vs 0.286) is a fractional-part accident, not a match. Several zeros land on the *peaks*, not the minima. In the strip, refined near-zeros of `J` have mean `σ ≈ 0.71` and **0%** within 0.10 of `1/2`; stationary points of `S_I` have median `σ ≈ 0.35`, also **0%** near the critical line. **This assembly does not even obey the model’s internal claim that critical points lie on `Re(s) = 1/2`, and it does not track the zeros.**

## 4. Honest conclusion

**There is no evidence that the SAM-3 information current, as it can be built from the repo’s actual Dual-Zero / conoid / overlap data, is the Riemann zeta function, or that its critical points are the nontrivial zeros.**

A stronger statement — that no such `J` exists — is not justified. The locked corpus does not define `J` concretely enough for a unique test (Paper 11 is a stub; doc 27 only names the ingredients). Every faithful assembly we could write from those ingredients fails the controls: zeros are not closer than midpoints or random `t`, and a fake or shuffled spectrum performs as well as the real one. Where distances look small (B, D), it is because the feature list is dense or periodic, not because it prefers zeros.

The original “50/50 stationarity” and “3/20 stationarity” outputs are artifacts and should not be cited as numerical support for the RH proposal.

What would still be needed for a real identification, unchanged from doc 27: a unique, derived formula for `J` from the locked geometry; a search that does not insert zeros into `J`; a match to zeros that beats midpoints, random `t`, and shuffled data; remainder control; and exhaustion of all zeros, not only a finite window.

## 5. Files

- Results writeup: `/workspace/sam3-work/RESULTS_zeta_identification.md`
- Patch and zip: see the packaging note at the bottom of this folder after `git format-patch` / `/workspace/sam3-work-results.zip`
- New / accompanying code (originals were not overwritten):
  - `code/verification/zeta_identification_test.py`
  - `code/verification/zeta_stationarity_tautology_demo.py`
  - `code/verification/zeta_stationarity_corrected.py`
  - `code/zeta_stationarity_enhanced_corrected.py`
  - `code/verification/README_stationarity_flaw.md`
- Outputs: `identification_results/` (JSON, logs, and plots for each construction)

Python environment: a local venv at `/workspace/sam3-work/.venv` with `numpy`, `scipy`, `matplotlib`, and `mpmath` (mpmath is not in the repo `requirements.txt`; it is required for `zetazero` and was already imported by the original stationarity script).
