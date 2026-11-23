# Dual-Zero re-run of SAM-2 / SAM-3 numerical claims

Exploratory.  Not part of the locked core.

These scripts re-evaluate claims that might have been rounding artefacts — constants, \(\alpha\), Yukawa overlaps, spectral sums, one-loop running, flux / moduli rankings — using Dual-Zero arithmetic, naive float64, and exact `Fraction` / `mpmath`.  Original SAM-2 / desktop source files are not in this repository.

Writeup: [`docs/hardening/54_DualZero_Rerun_of_All_Models.md`](../../docs/hardening/54_DualZero_Rerun_of_All_Models.md).

From the repository root:

```bash
pytest -q tests/test_dual_zero_toe.py
PYTHONPATH=.:experiments python experiments/dual_zero_toe/run_report.py
```

The re-run found **no genuine change**: exact zeros stayed zeros, fits stayed fits, and Dual-Zero arithmetic did not select a unique flux, area, or \(\tau\).
