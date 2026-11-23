# Missing-principle survey (exploratory)

**This directory is not part of the locked SAM-3 core.**

The locked core, and the bottom line of the unification experiments, are stated in [`BOTTOM_LINE.md`](../../BOTTOM_LINE.md).  Docs 47–48 already found that the integer 3 and the surface moduli are not derived.  This folder tests a broader list of mathematical mechanisms that might supply the missing principle, and records the results in [`docs/hardening/49_Missing_Principle_Survey.md`](../../docs/hardening/49_Missing_Principle_Survey.md).

Reproduce:

```bash
python experiments/missing_principle/report.py
pytest -q tests/test_missing_principle.py
```

Honesty rule: unproven statements are labelled.  Null results stay null.  Number-matching is flagged as numerology when it is only a count.
