# Alternative geometries (exploratory)

**This directory is not part of the locked SAM-3 core.**

The locked core is the right-conoid metric \(f=\sqrt{u^2+4\ell_0^2\cos^2(2v)}\), the theorems \(C_0=2\pi\ln 2\), \(E_0(m;U)=(j_{\nu,1}/U)^2\), the APS index \(0\) of the untwisted Dirac operator on the truncated conoid, and the singular-tip analysis of docs 44–46. Nothing in this folder supersedes those results.

These experiments ask whether a *different* surface or internal space could supply unification-relevant structure that the conoid does not (in particular, three chiral generations). They are documented in [`docs/hardening/47_Alternative_Geometries_Exploratory.md`](../../docs/hardening/47_Alternative_Geometries_Exploratory.md).

Reproduce:

```bash
python experiments/alt_geometries/report.py
pytest -q tests/test_alt_geometries.py
```

Honesty rule: unproven statements are labelled. Null results stay null. Number-matching (4 nodes, 12 bridges, \(\chi\), Hopf, \(TS^2\), \ldots) is flagged as numerology when it is only a count.
