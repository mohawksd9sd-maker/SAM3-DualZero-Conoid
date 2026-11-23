# Conoid × magnetized surface × Pati–Salam (exploratory)

**This directory is not part of the locked SAM-3 core.**

It develops the top-ranked direction of doc 47: the almost-commutative
geometry \(Y\times F_{\mathrm{PS}}\) with \(Y=\) (truncated right conoid) \(\times\Sigma^2\),
where \(\Sigma^2\) is a magnetized \(T^2\) or \(S^2\), and \(F_{\mathrm{PS}}\) is the
Pati–Salam finite spectral triple of Chamseddine–Connes–van Suijlekom.

Documentation: [`docs/hardening/48_PS_Conoid_Product.md`](../../docs/hardening/48_PS_Conoid_Product.md).

Reproduce:

```bash
python experiments/ps_conoid_product/report.py
pytest -q tests/test_ps_conoid_product.py
```

Honesty rule: unproven statements are labelled.  Fits are labelled as fits.
Null results stay null.
