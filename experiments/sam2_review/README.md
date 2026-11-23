# SAM-2 / math-model / May-clone review checks

Exploratory honesty checks for [`docs/hardening/51_SAM2_Lines_Review.md`](../../docs/hardening/51_SAM2_Lines_Review.md).

This folder does **not** contain Shawn’s original SAM-2 PDFs, math-model RTFs, or the May 14, 2026 clone.  Those sources were read locally and are not part of the repository.

Run:

```
.venv/bin/python -m pytest tests/test_sam2_review.py
```

Nothing here locks a new core theorem.  The Dual-Zero generator used by the locked project remains the definition in doc 18: \(\varepsilon(n)=\omega_0(-1)^n n^{-n}\), with \(\omega_0\) an input.
