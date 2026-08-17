# Mathematical Note XXX — Production Pipeline Specification

**Date:** August 2026  
**Purpose:** Outsider-runnable continuum support with documented grids, error budgets, and no private parameters.

---

## 1. What the pipeline certifies

| Quantity | Method | Analytic status |
|----------|--------|-----------------|
| $E_0(2)<E_0(3)$ | Variational (HT1) | **Proved** |
| 3+0 isolation | HT3 | **Proved** given dictionary |
| Size of $\Delta(U)$ | Sturm–Liouville FD | Numeric illustration |
| Smoothing continuity of $E_0(\delta)$ | FD in $\delta$ | Numeric support of CS1 |

The pipeline **does not prove** isolation; it **illustrates** analytic theorems and regression-tests the code.

---

## 2. Frozen public parameters

| Name | Value | Location |
|------|-------|----------|
| `U_LIST` | `(10, 20, 40, 80)` | `code/production_channel_pipeline.py` |
| `N_GRID` | `4000` | same |
| Soft $m$ | `0,1,2` | same |
| Heavy $m$ | `3,4,5,6` | same |
| Tip model | $V=m^2/(u+10^{-4})^2 + 1/(u^2+1)^2$ | same |
| Threshold | mid-gap | same |

**No private parameters.** All constants are in the script header.

---

## 3. Error budget (FD)

| Source | Estimate |
|--------|----------|
| Grid spacing $du=U/N$ | $O(du^2)$ for 2nd-order FD eigenvalues |
| At $U=80$, $N=4000$ | $du\sim 0.02$; relative EV error $\ll 10^{-3}$ on low modes |
| Soft floor $\epsilon=10^{-4}$ | Changes $E_0$ by $O(\epsilon)$ relative to $\epsilon=0^+$ cutoff |
| Boundary condition | Dirichlet; APS outer collar changes $O(1/U)$ |

**Regression:** exit code 0 requires isolation $(3,0)$ and $\Delta>0$ at every $U$.

---

## 4. How an outsider runs it

```bash
git clone https://github.com/mohawksd9sd-maker/SAM3-DualZero-Conoid
cd SAM3-DualZero-Conoid
pip install numpy scipy
python code/production_channel_pipeline.py   # expect ok: true
python code/prho_projectors.py
python code/volume_regularisation.py
```

---

## 5. Full 2D APS solver status

Unreduced 2D APS FD remains optional cross-check. Load-bearing continuum isolation is **channel-reduced**, matching the pure-math proof structure. Claims that require unreduced 2D residuals should be marked numeric-optional in STATUS.

---

*Note XXX — production pipeline spec.*
