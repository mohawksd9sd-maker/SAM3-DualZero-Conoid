# 46 — The singular tip \(u\to 0\)

**Date:** 23 November 2026 (America/Chicago)
**SSOT:** `STATUS_CLAIMS_AND_RESIDUALS.md`
**Rule:** derivation only; verified citations only; null results stay null.

No standalone paper was written.  This is the analysis that the
product-collar APS theorem (doc 44) does not cover.

---

## 1. Local geometry

The abstract surface is the coordinate cylinder with the locked metric
\(ds^2=du^2+f^2\,dv^2\), \(f=\sqrt{u^2+4\ell_0^2\cos^2(2v)}\).  For \(u>0\),
\(f>0\) and the metric is smooth and positive definite.  It is
**incomplete**: the curves of constant \(v\) are unit-speed geodesics
(\(\Gamma^u_{uu}=\Gamma^v_{uu}=0\)), so \(\mathrm{dist}((u,v),\{u=0\})=u\).

The metric tensor, in coordinates \((u,v)\), extends as a \(C^\infty\)
tensor to the closed cylinder \([0,U]\times S^1\): \(g_{vv}=u^2+4\ell_0^2\cos^2(2v)\)
is a trigonometric polynomial.  It is positive definite except at the four
**nodes**
\[
  v_k=\pi/4+k\pi/2,\qquad u=0,
\]
where \(g_{vv}=0\).  The metric completion adds the circle \(u=0\), of length
\[
  L(0)=\int_0^{2\pi} 2\ell_0\lvert\cos(2v)\rvert\,dv=8\ell_0.
\]
Away from the nodes, \(f(0,v)=2\ell_0\lvert\cos(2v)\rvert>0\) and
\(f_u=u/f=0\), so the metric is a smooth product-type collar and the
geodesic curvature of \(u=0\) vanishes: the regular tip is a **geodesic
boundary**.

**Singularity type (derived).** The tip is a geodesic boundary circle of
length \(8\ell_0\) with four isolated degeneracy points of a \(C^\infty\)
metric on a compact surface with boundary.  A neighbourhood of a node in
the completion is a half-disk, not a full cone.  The local model
\(du^2+(u^2+\alpha^2 s^2)\,ds^2\) (\(\alpha=4\ell_0\), \(s=v-v_k\)) is
**anisotropic**: it is not Cheeger’s metric cone \(dr^2+r^2 g_N\), and it
is not an incomplete edge (no positive-dimensional singular stratum with
a conical normal plane).  Those frameworks are cited only to record that
they do not apply (Cheeger, *J. Diff. Geom.* 18 (1983); Mazzeo, *J. Diff.
Geom.* 1991; Albin–Gell-Redman, *SIGMA* 12 (2016)).

Numerical observation, not a theorem: metric circles of radius
\(\varepsilon\) about a node have \(L(\varepsilon)/\varepsilon\approx 3.09,\,3.06,\,3.03,\,2.99\)
at \(\varepsilon=0.06,0.04,0.03,0.02\), of order \(\pi\) and far from a cusp
(\(0\)) or a full cone (\(2\pi\)).

**Embedding (separate from the abstract metric).** The map
\(r(u,v)=(u\cos v,\,u\sin v,\,\ell_0\sin(2v))\) is an embedding for
\(u>0\).  At \(u=0\) the image is the segment \(\{0\}\times\{0\}\times[-\ell_0,\ell_0]\):
a self-intersection along the open segment, with the four nodes mapping
to the two endpoints (two preimages each).  That is a statement about
\(r\), not a cone-point structure on the abstract surface.

**Curvature (derived).** \(K=-4\ell_0^2\cos^2(2v)/f^4\le 0\).  \(K\) is
**unbounded** near the nodes: for each fixed \(u\in(0,2\ell_0]\),
\[
  \max_v\lvert K(u,\cdot)\rvert=\frac1{4u^2},
\]
attained where \(4\ell_0^2\cos^2(2v)=u^2\).  The older claim
\(\lVert K\rVert_{\max}=1/(4\ell_0^2)\) is only the value of \(\lvert K\rvert\)
at the mid-arcs \(u=0\), \(\lvert\cos(2v)\rvert=1\); it is **not a global
bound** (already at \(u=\ell_0/2\) the maximum is four times larger).
Nonetheless \(K\) is integrable: \(\int K\,dA=-2\pi\) on the complete
surface, so \(\int\lvert K\rvert\,dA=2\pi\), and the mass of \(\lvert K\rvert\)
in a coordinate half-disk of radius \(R\) about a node is \(O(R)\)
(\(\pi R/(8\ell_0)\) in the local model).  Combined with
\(\int_0^{2\pi}(a/f(a,v))\,dv\to 0\) as \(a\to 0\), there is **no residual
\(\delta\)-mass of curvature** at the tip circle or at the four nodes.

The area of a tip neighbourhood \(\{u\le a\}\) is finite and
\(\sim 8\ell_0 a\) as \(a\to 0\).

A consequence for \(\omega_0\): the prescription \(R=1/\lVert K\rVert_{\max}\)
is not well-defined, because \(\lvert K\rvert\) is unbounded.

---

## 2. Dirac operator

Chernoff (*J. Funct. Anal.* 12 (1973); *Pacific J. Math.* 72 (1977)) and
Wolf (*Indiana Univ. Math. J.* 22 (1973)): the Dirac operator on a
*complete* Riemannian spin manifold is essentially self-adjoint on
compactly supported smooth spinors.  The present surface is incomplete,
with a boundary at finite distance, so essential self-adjointness
**fails**, for the same reason it fails on any compact surface with
boundary.

Away from the four nodes the metric is a smooth product collar, and the
Dirac operator has the standard APS form \(\sigma(\partial_u+A)\).  Each
mode of the boundary operator \(A\) is a regular (limit-circle) endpoint
of a 1D Dirac system: a boundary condition is required.  The space of
self-adjoint extensions is the usual infinite-dimensional Grassmannian of
elliptic boundary conditions on the tip circle (and at the outer end).
The four nodes are a measure-zero subset of that circle; they do not
convert the problem into a Cheeger cone-point deficiency calculation,
and we do not invent a finite deficiency index \((n_+,n_-)\) for each
node.

---

## 3. Index, and whether the tip can give three generations

For every \(a>0\), the product-collar APS index of \(X_{a,U}\) is \(0\)
(doc 44), independently of \(a\).  The inner boundary operator, for the
bounding spin structure, has no kernel at any \(a>0\): there is **no
spectral flow** as \(a\downarrow 0\).  This is strong evidence that the
limiting problem, with APS or the Friedrichs (minimal) extension at the
tip, still has index 0.  We do *not* claim a new theorem that “APS on a
circle with four metric degeneracies” is already in the literature.

Cheeger’s cone-point analysis and the incomplete-edge index theorem of
Albin–Gell-Redman (under a Witt condition on the link) are for different
singularity types and are not applied.

**Verdict: the tip does not give three generations.**  Every positive-cut
APS index is 0, there is no spectral flow, there is no curvature delta
and no cone-deficit to feed a Cheeger correction, and the natural
extensions (APS, Friedrichs) are the same classes already used on the
truncations.  An extension with index 3 would be an additional choice of
boundary condition, put in by hand, not forced by the metric.

---

## 4. Spectral-action / heat-kernel consequences

- \(a_0\) (area) is finite near the tip; there is no area divergence.
- Standard boundary Seeley terms involve the geodesic curvature of the
  boundary.  On the regular tip \(k_g=0\), so those terms vanish there.
- Conical-defect corrections of the form
  \((\beta/6)\bigl((2\pi/\beta)^2-1\bigr)\) at a cone of angle \(\beta\)
  (e.g. Fursaev, *hep-th/9405143*; De Nardo–Fursaev–Miele,
  *hep-th/9605153*) are for metric cones and **do not apply**.
- We do not invent a 0-dimensional coefficient at the four nodes.

---

## Code and tests

- `code/singular_tip_analysis.py`
- `tests/test_singular_tip.py`
- `reproducibility/singular_tip_analysis.json`
