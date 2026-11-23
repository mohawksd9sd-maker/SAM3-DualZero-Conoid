# Two-loop SM → Pati–Salam running and spin-offs (docs 55–58)

Exploratory; not part of the locked SAM-3 core.

| file | content | doc |
|---|---|---|
| `group_theory.py` | exact (Fraction) one- and two-loop gauge β coefficients from Dynkin indices / Casimirs; SM and CCvS Pati–Salam content; SM decomposition of heavy states | 55 |
| `rge.py` | two-loop running, MS-bar matching with thresholds, the no-tuning solve for \(m_R,\Lambda\) | 55 |
| `analysis.py` | input-uncertainty shifts and the ×/÷10 threshold Monte Carlo → `results_doc55.json` | 55 |
| `phenomenology.py` | baryon-number operator table, proton lifetime estimate, \(K_L\to\mu e\), seesaw | 55, 57 |
| `finite_triple.py` | one-generation finite spectral triple: KO-dim, order 0/1, maximality of \(A_{SM}\), isospectral test | 56 |
| `higgs_masses.py` | spectral boundary relations at \(\Lambda\), running of \(y_t,\lambda,\kappa,\lambda_\sigma\), \(M_t\), \(m_H\) | 58 |
| `report_56_58.py` | numbers for docs 56–58 → `results_docs56_58.json` | 56–58 |

Run from the repo root with the venv: `.venv/bin/python experiments/two_loop_pati_salam/analysis.py` (≈2 min) and `.venv/bin/python experiments/two_loop_pati_salam/report_56_58.py`.
