# Further candidate tests (exploratory)

**This directory is not part of the locked SAM-3 core.**

A follow-up to docs 47–49: more candidate principles that might *accidentally* single out three generations or fix the surface moduli, tested without tuning parameters to force a fit.  Documented in [`docs/hardening/50_Further_Candidate_Tests.md`](../../docs/hardening/50_Further_Candidate_Tests.md).

Reproduce:

```bash
python experiments/further_candidates/report.py
pytest -q tests/test_further_candidates.py
```

A “fit” is counted only if 3, or a unique modulus, comes out with no parameter chosen to make it so.  Near-misses and dead ends are reported as such.
