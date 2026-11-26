# open_routes_72: docs 72 and 73 (top / Higgs open routes for candidate #10)

The SAM-3 / Dual-Zero framework is by Shawn Dykes. The scripts here are exploratory checks; see `docs/hardening/72_*.md` and `73_*.md`.

Third-party pieces are not committed. They are rebuilt locally from free sources:
- `fs_ext/`: FlexibleSUSY (GPL-3) `src/mssm_twoloop_mt.{cpp,hpp}`, `Li2.{cpp,hpp}`, `horner.hpp` and `log.hpp`, plus a small C wrapper (`wrap.cpp`, exposing the 2L SQCD Δm_t). Build with `g++ -O2 -shared -fPIC -o libdmt.so *.cpp`. Used by `sqcd2l.py`. Only needed for `sqcd2=True`.
- `smdr/`: SMDR v1.3 (Martin–Robertson, arXiv:1907.02500), from https://www.niu.edu/spmartin/SMDR/. Its `calc_fit` was run at (M_t, M_h) = (171.5, 125.1), (172.5, 124.1/125.1/126.1) and (173.5, 125.1). The fitted coefficients are hard-coded in `common.py` (`SMDR`).
- `refs/`: arXiv sources of the cited papers.

Run any script with `PYTHONPATH=. ../../.venv/bin/python <script>.py`.

Note: `results_route1.json` and `results_route1b.json` were made with the pre-erratum repo code (doc 70 X^5/4 bug, 173.10 reference). `route3`, `route1c`, `route1d` and `route2` use the corrected physics (thr72 has always used -X^5; the matching is stated per run).
