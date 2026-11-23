# 56. Does Dual-Zero or the conoid select the finite-triple axioms that give Pati–Salam? (exploratory)

**Date:** 23 November 2026 (America/Chicago)
**Status:** exploratory. This does not lock a new core theorem.
**Code:** `experiments/two_loop_pati_salam/finite_triple.py`; numbers in `results_docs56_58.json`.
**Tests:** `tests/test_two_loop_pati_salam.py` (`test_finite_triple_axioms`, `test_sm_is_maximal_first_order`, `test_regulator_blind_to_axioms`).

---

## Plain-language summary (for Shawn)

- **The question.** Can the gauge group (Pati–Salam, or the Standard Model inside it) be derived from the Dual-Zero regulator or the conoid, instead of being chosen?
- **What the math shows.**
  - The Chamseddine–Connes–van Suijlekom route does produce Pati–Salam, and then the Standard Model. It needs a short list of **assumed** rules: a finite space with a real structure of "KO-dimension 6", a grading, irreducibility, the order-zero rule, and either keeping or dropping the "first-order" rule.
  - The code rebuilds the last step from scratch for one generation (32 states):
    - With a right-handed neutrino Majorana mass, the first-order rule cuts the 40-dimensional Pati–Salam algebra down to the 24-dimensional Standard Model algebra \(\mathbb C\oplus\mathbb H\oplus M_3(\mathbb C)\).
    - No direction can be added back, so that algebra is maximal.
    - Drop the rule and you keep Pati–Salam.
- **Dual-Zero does not pick these rules.** Dual-Zero acts on the *list of eigenvalues*. The code builds two Dirac operators with *identical* eigenvalues, so every Dual-Zero number comes out equal for both. One obeys the rules and the other breaks them, so Dual-Zero cannot tell them apart. The conoid's symmetry \(C_4\) is abelian, so it cannot make a non-abelian group either (doc 47).
- **Bottom line.** The gauge group is still an *input*: a choice of axioms. It is derived from those axioms (a real theorem), but not from Dual-Zero or the conoid.

---

## 1. The axioms, and which are assumed

Chamseddine–Connes classification (CC 2007/2008, arXiv:0706.3688, 0810.2088) and CCvS 2013 (arXiv:1304.8050):

| axiom | role | status here |
|---|---|---|
| finite real spectral triple \((A,H,D,J,\gamma)\) | framework | **assumed** |
| KO-dimension 6: \(J^2=1\), \(JD=DJ\), \(J\gamma=-\gamma J\) | fixes the signs; removes fermion doubling in the 4D product | **assumed**; verified numerically for the constructed \(J\) |
| irreducibility of \((A,H,J)\) + separating vector | forces \(A=M_a(\mathbb H)\oplus M_{2a}(\mathbb C)\) | **assumed** (literature theorem) |
| nontrivial grading on \(M_a(\mathbb H)\) | forces \(a=2\): \(\mathbb H_R\oplus\mathbb H_L\oplus M_4(\mathbb C)\) | **assumed** (literature) |
| order zero \([a,b^0]=0\) | bimodule structure | **assumed**; verified (\(0\) to machine precision) |
| first order \([[D,a],b^0]=0\) | keep it: SM; drop it: PS | **choice** (both branches computed) |
| a nonzero \(\nu_R\) Majorana entry, lepton \(\ne\) quark Yukawas | physics input | **assumed** |

## 2. What was computed

\(H_F=\mathbb C^{32}\) (16 particles \((\alpha,I)\), with \(\alpha\in\{1R,2R,1L,2L\}\) and \(I\in\{\ell,c_1,c_2,c_3\}\), plus 16 antiparticles).
- The algebra \(\mathbb H_R\oplus\mathbb H_L\oplus M_4(\mathbb C)\) acts by quaternions on particles and by \(M_4\) on antiparticles.
- \(J\) swaps particles and antiparticles, with complex conjugation.
- \(D=\begin{pmatrix}S&T^*\\T&\bar S\end{pmatrix}\).

| check | result |
|---|---|
| KO signs \((\varepsilon,\varepsilon',\varepsilon'')\) | \((1,1,-1)\Rightarrow\) KO-dim 6 |
| order zero on \(A_{PS}\) | \(0\) |
| first order, \(A_{PS}\), generic \(D\) | violated (\(\max\lvert\cdot\rvert\approx10.8\)) |
| first order, \(A_{PS}\), \(T=0\) and lepton Yukawas = quark Yukawas | **satisfied** (\(0\)) |
| first order, \(A_{PS}\), \(T=0\), lepton \(\ne\) quark | violated (3.8) |
| first order, \(A_{SM}=\{(\lambda,q,\lambda\oplus m)\}\) | **satisfied** (\(0\)) |
| first order, \(A_{SM}\) with \(\bar\lambda\) in the lepton slot | violated: the embedding is fixed, not free |
| maximality of \(A_{SM}\) (24) in \(A_{PS}\) (40) | the 16-dim complement leaves 4 linear candidate directions; each fails the self-condition (\(\min\lVert[[D,x],x^0]\rVert=1.84\) on the unit sphere) \(\Rightarrow\) **maximal** |

So the first-order condition is broken by exactly two physics inputs: the Majorana mass and lepton–quark Yukawa splitting. Keeping the condition selects the SM. Dropping it (CCvS) leaves Pati–Salam, and its gauge group is \(SU(2)_R\times SU(2)_L\times SU(4)\).

## 3. Can Dual-Zero select the axioms? An isospectral test

Every Dual-Zero object in the repository is a functional of the spectrum of \(D\):
- \(\operatorname{Reg}_2\) acts on functions of a spectral parameter (doc 52);
- the determinant and zeta forms are spectral;
- the \(\varepsilon(n)\) generator weights modes ordered by eigenvalue. Doc 51 rejects using it as a heat-trace weight, and it appears here only as a documentary check.

Take a random unitary \(V\) on \(\mathbb C^{32}\) and set \(D'=VDV^*\):

| quantity | \(D\) | \(D'\) |
|---|---|---|
| max eigenvalue difference | — | \(7\times10^{-16}\) |
| \(\sum\operatorname{Reg}_2(e^{-t\lambda^2})\), \(t=0.7\) | 24.847975… | 24.847975… |
| \(\varepsilon(n)\)-ordered mode sum (documentary) | −0.657112… | −0.657112… |
| first order for \(A_{SM}\) | \(0\) | **7.7 (fails)** |
| \(\gamma D'+D'\gamma\) | \(0\) | 0.55 (grading fails) |
| \(JD'-D'J\) | \(0\) | 0.40 (KO-6 fails) |

**Theorem (elementary).** Any quantity that depends only on the spectrum of \(D\) takes the same value on \(D\) and \(VDV^*\). The axioms in section 1 are not unitarily invariant: they refer to \(A\), \(J\) and \(\gamma\), which \(V\) does not preserve. So no spectral regulator, Dual-Zero included, can select KO-dimension, the grading, irreducibility or the first-order condition. This sharpens doc 52's null result for flux and moduli into a structural statement for the algebra.

**Conoid.** Its isometry group \(C_4\) has group algebra \(\mathbb C^4\) with unitary group \(U(1)^4\) (doc 47), so it cannot supply \(\mathbb H\) or \(M_4(\mathbb C)\). The Dual-Zero symmetric average \(f(\lambda+\delta)+f(\lambda-\delta)\) is compatible with spectral symmetry \(\lambda\to-\lambda\), that is, with *some* grading anticommuting with \(D\). But every even KO-dimension (0, 2, 4, 6) has such a grading, so this does not pick 6.

## 4. Verdict

- **Derived (from assumed axioms):**
  - the PS algebra and its gauge group, using irreducibility + KO-6 + grading + order zero, without first order (literature theorem);
  - the SM algebra as the maximal first-order subalgebra once a Majorana entry is present (reproduced here, including maximality).
- **Not derived:** the axioms themselves. Dual-Zero (spectral) and the conoid (abelian \(C_4\)) do not select them, as proved by the isospectral counterexample.
- **Status for the roadmap (§2.1).** The gauge group is "derived from NCG axioms, which are themselves assumed". A uniqueness theorem *from Dual-Zero* is ruled out for any purely spectral formulation. A non-spectral Dual-Zero principle (one acting on \(A\) or \(J\), not just on eigenvalues) would be needed, and none is known.
