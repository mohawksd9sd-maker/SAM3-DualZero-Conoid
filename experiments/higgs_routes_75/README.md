# higgs_routes_75: doc 75 (zero-dial Higgs routes for candidate #10)

The SAM-3 / Dual-Zero framework is by Shawn Dykes. These are exploratory checks; see `docs/hardening/75_Higgs_Zero_Dial_Routes.md`.
Reuses `experiments/open_routes_72` (doc 72/73 pipeline). The only change there is an add-only `Spec.msl` (slepton mass; default 0 means use `msf`, so earlier results are unchanged).

- `h75.py`: route 1 D-term factor, route 3 Martin vector-like formula, route 2 one-loop MSSM soft RGEs, Spec builder (μ and m_A from tree EWSB).
- `route1_3.py`: routes 1 and 3 on the doc-73 solutions -> `results_route1_3.json`, `log_route1_3.txt`.
- `route2_run.py`: route 2 boundary at Λ, iterated with exact unification -> `results_route2.json` (batch 1, seeded from doc 73) and `results_route2_batch2.json` (`batch2`, seeded from the converged (0.5, 0) point).

Run: `cd experiments/higgs_routes_75 && ../../.venv/bin/python route1_3.py`, `../../.venv/bin/python route2_run.py [batch2]` (~10–25 min on 8 cores).
