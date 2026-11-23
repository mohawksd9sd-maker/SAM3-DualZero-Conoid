# Dual-Zero axiom and flux/moduli selection tests

Exploratory checks for [`docs/hardening/52_DualZero_Axiom_Selection_Test.md`](../../docs/hardening/52_DualZero_Axiom_Selection_Test.md).

This package states the Dual-Zero regulator as a standalone axiom
(sequence \(\varepsilon(n)=\omega_0(-1)^n n^{-n}\), symmetric \(\operatorname{Reg}_2\)
on functions of a spectral parameter) and asks whether that axiom, without
fitting, selects a flux \(M\) or moduli \((A,\tau)\) on:

- a magnetized flat torus (and the almost-commutative product with a
  Pati–Salam / CCM finite triple),
- an unfluxed flat torus,
- the orbifold \(T^2/\mathbb{Z}_4\),
- a round sphere with monopole flux (index and Seeley terms only).

\(\omega_0\) is an input.  Mode-sum weighting by \(\varepsilon(n)\) is not used.

Run:

```
.venv/bin/python -m pytest tests/test_dual_zero_axiom.py
.venv/bin/python experiments/dual_zero_axiom/report.py
```

Nothing here locks a new core theorem.
