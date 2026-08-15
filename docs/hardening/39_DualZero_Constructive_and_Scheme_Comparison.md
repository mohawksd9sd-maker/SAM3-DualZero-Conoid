# 39 — Dual-Zero: Constructive Realization + Scheme Comparison

**Status:** Hardening of Dual-Zero for numerical work and scheme independence  
**Date:** August 2026  
**Canonical definition:** docs 18, 35

---

## 1. Canonical sequence (unchanged)

$$
\varepsilon(n)=\omega_0(-1)^n n^{-n},
\qquad \omega_0\approx 0.927,
\qquad
\operatorname{Reg}_2(a)_n=\frac{a_{2n}+a_{2n+1}}{2}.
$$

Hyperreal ultrapower language in older papers is **interpretive**. Numerical and spectral-action work uses the **constructive truncation** below.

---

## 2. Constructive / algorithmic realization

### 2.1 Finite-N truncation (production)

For mode sums / spectral weights:

```text
Input: N_max, omega0, observable functional F[{w_n}]
For n = 1..N_max:
  eps[n] = omega0 * (-1)**n * n**(-n)
  w[n]   = abs(eps[n])           # or signed where grading requires
Optionally Reg2-pair: w2[k] = 0.5*(w[2k]+w[2k+1])
Return F[w] or F[w2]
```

| Property | Statement |
|----------|-----------|
| Non-constructive ultrafilter | **Not required** for production numbers |
| $n^{-n}$ decay | $N_{\rm max}\le 30$ already machine-underflow for tails |
| Standard part | Replaced by explicit $\sum_{n=1}^{N_{\rm max}}$ with tail bound |

**Tail bound:** for $n\ge N$, $\lvert\varepsilon(n)\rvert\le \omega_0 e^{-n\ln n}$; series of poly-growth test data absolute-converge beyond $N\sim 20$.

### 2.2 Code reference

`code/dual_zero_constructive.py` — weights, Reg₂, tail estimates, scheme probes.

---

## 3. Comparison to standard spectral-action cutoffs

| Scheme | UV definition | SAM3 use |
|--------|---------------|----------|
| **Dual-Zero** | $\varepsilon(n)$, Reg₂ | Mode weights on discrete/infinite towers |
| **Heat kernel** | $\mathrm{Tr}\,e^{-tD^2}$, Seeley $a_{2k}$ | $G_N$, $m_H$ class, continuum $\eta$ |
| **Zeta** | $\zeta_D(s)=\mathrm{Tr}\lvert D\rvert^{-s}$ | Equivalent spectral language |
| **Hard cutoff** $\Lambda$ | $\theta(\Lambda-\lvert\lambda\rvert)$ | **Not** the Dual-Zero philosophy |
| **Exponential** $e^{-\lvert\lambda\rvert/\Lambda}$ | Smooth cutoff | Benchmark only |

### 3.1 Scheme independence at claimed precision

| Observable | Leading scheme | Dual-Zero role | Claimed precision |
|------------|----------------|----------------|-------------------|
| $G_N$ | Heat kernel $a_2$ | Subleading mode weight | Formula locked; O(1–few %) scheme |
| $m_H$ class | Heat kernel $a_4$ | UV silence; **not** digit tuner | Class (124–127 GeV) |
| $\eta_{ij}$ | Continuum heat-kernel / defect | Optional shifts; $\omega_0$ fixed | RMS $\sim 0.008$ vs archive |
| Yukawa hierarchy | Tip Casimir + geometry | Super-exponential UV | Ratios locked class |
| Unification residual | β-functions + thresholds | Reweight only | ~7% floor baseline |

**Policy:** Switching heat-kernel ↔ zeta must not change locked **class** claims. Dual-Zero must not be retuned to absorb scheme mismatch.

### 3.2 What is *not* claimed

- Digit-level equality of $m_H$ across all cutoff schemes
- Percent-level unification from Dual-Zero reweighting alone
- That ultrapower language is required for any production number

---

## 4. Hyperreal methods — discipline

| Allowed | Not allowed |
|---------|-------------|
| Motivating information-conservation narrative | Hiding non-constructive steps inside locked digits |
| Ultrafilter as optional idealization | Requiring non-principal ultrafilters in `code/` |
| Reg₂ + finite-$N$ as production definition | Fitting $\omega_0$ per scheme |

---

*Constructive Dual-Zero + scheme comparison — August 2026.*
