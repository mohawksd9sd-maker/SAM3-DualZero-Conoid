# Doc 76: stau LSP, two-loop soft running, m_A vs LHC, M_h theory error

SAM-3 / Dual-Zero originator: Shawn Dykes. Write-up: `docs/hardening/76_Stau_LSP_TwoLoop_Soft_and_mA.md`.

1. Build SOFTSUSY 4.1.13 (https://softsusy.hepforge.org; needs gfortran), apply `softsusy-4.1.13-doc76.patch`, then `make softpoint.x`.
2. Run `SOFTPOINT=/path/softpoint.x python softsusy_2loop.py`. This writes `results_softsusy_2loop.json`.
3. Run `python rerun76.py`. It takes about 8 min on 8 cores and writes `results_rerun76.json`.
4. Run `python gravitino76.py` and `python lhc76.py`.

Tests: `tests/test_doc76.py`. They read the committed JSON and need no SOFTSUSY.
