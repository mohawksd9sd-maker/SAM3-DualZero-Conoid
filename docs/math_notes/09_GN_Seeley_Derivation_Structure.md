# Mathematical Note IX — $G_N$ from Seeley–DeWitt $a_2$: Derivation Structure

**Date:** August 2026  
**Purpose:** Make the $G_N=64\pi\ell_0^2/45$ relation audit-ready: hypotheses, coefficient chain, residuals.  
**Honest status:** The Einstein–Hilbert origin in $a_2$ is standard; the pure number $64\pi/45$ is a **convention-locked normalisation** on the product geometry with the locked internal metric — not a scheme-free universal constant independent of cutoff-moment conventions.

---

## 1. Hypotheses

1. **Product spectral triple.** $D = D_M\otimes 1 + \gamma_5\otimes D_F$ on $L^2(S)\otimes \mathcal{H}_F$ with internal Riemannian factor carrying scale $\ell_0$.  
2. **Locked internal metric.**
   $$
   ds^2=du^2+f^2 dv^2,\quad
   f=\sqrt{u^2+4\ell_0^2\cos^2(2v)}.
   $$
3. **Spectral action.** $S=\mathrm{Tr}\,\chi(D/\Lambda)$ with cutoff moments
   $$
   \phi_{2k} = \int_0^\infty \chi(u)\,u^{k-1}\,du
   $$
   (standard Connes–Chamseddine notation up to normalisation).  
4. **Einstein-frame identification.** After normalising the gravitational term to the Einstein–Hilbert action, $G_N=\kappa^2/(8\pi)$.

---

## 2. Standard $a_2$ structure (textbook layer)

On a closed even-dimensional spin manifold, the heat-kernel / Seeley expansion gives

$$
\mathrm{Tr}\,e^{-tD^2} \sim \sum_{k\ge 0} t^{k-n/2} a_{2k}(D^2).
$$

For the spectral action on a 4D spacetime factor, the coefficient $a_2$ produces the scalar curvature term

$$
S \supset \frac{\Lambda^2 \phi_2}{24\pi^2}\int_S R\,\mathrm{vol}_g + \cdots
$$

(up to the precise conventional factor set by $\chi$ and dimension; cf. Chamseddine–Connes–Marcolli). On a **product** $S\times F$ the internal volume and internal curvature moments multiply this term:

$$
\frac{1}{2\kappa^2}
=
C_{\mathrm{SA}}\,\Lambda^2\,\phi_2\,\mathrm{Vol}(F;\ell_0),
$$

where $C_{\mathrm{SA}}$ is a pure number from the Seeley calculus and $\mathrm{Vol}(F;\ell_0)\propto \ell_0^{\dim F}$ (here internal 2-geometry gives $\propto\ell_0^2$).

---

## 3. Scale identification

Set the spectral cutoff at the geometric UV scale associated with the same $\ell_0$,

$$
\Lambda \sim \Lambda_0 = \frac{1}{\ell_0},
$$

so that $\Lambda^2\,\mathrm{Vol}(F)\propto \ell_0^{0}$ times a dimensionless internal integral over the unit metric $\hat g = g/\ell_0^2$. Then

$$
\frac{1}{2\kappa^2} = \frac{1}{\ell_0^2}\,\mathcal{N}(\hat f,\phi_2),
$$

with $\mathcal{N}$ a dimensionless functional of the unit tip profile $\hat f$ and the cutoff moment $\phi_2$.

Using $G_N=\kappa^2/(8\pi)$,

$$
G_N = \frac{\ell_0^2}{16\pi\,\mathcal{N}(\hat f,\phi_2)}.
$$

---

## 4. The factor $64\pi/45$

The locked relation

$$
G_N = \frac{64\pi\,\ell_0^2}{45}
$$

is equivalent to fixing

$$
\mathcal{N}(\hat f,\phi_2) = \frac{45}{1024\pi^2}
$$

under the repository’s spectral-action normalisation conventions (cutoff moments, trace normalisations, and the locked $\hat f$ with tip coefficient 4).

**Professional status of the pure number:**

| Interpretation | Allowed? |
|----------------|----------|
| “$G_N\propto\ell_0^2$ with proportionality fixed by $a_2$ + locked metric” | **Yes** — structural |
| “$64\pi/45$ is a universal scheme-independent constant of nature from geometry alone” | **No** — convention-dependent residual |
| “Changing tip coefficient $c$ at fixed $\ell_0$ leaves $G_N$ formula invariant” | **No** — $\mathcal{N}$ depends on $\hat f$ |

---

## 5. Dual-Zero does not define $G_N$

Dual-Zero weights enter subleading regulated mode sums. The Einstein–Hilbert term is carried by **heat-kernel / Seeley $a_2$**. Regulator swaps at leading order do not redefine $G_N$ (Note IV, VII).

---

## 6. Residuals (explicit)

1. **Full component expansion** of $a_2$ on the exact nonlinear $f$, published as a standalone calculation with every combinatorial factor.  
2. **Cutoff-moment scheme:** different $\chi$ change $\phi_2$ and thus $\mathcal{N}$; the locked formula absorbs one conventional choice.  
3. **Quantum loops** of gravitons: not included.

---

## 7. Preferred external wording

> Under the locked internal metric and a fixed spectral-action normalisation, the Seeley–DeWitt coefficient $a_2$ implies $G_N\propto\ell_0^2$. The repository records the normalised form $G_N=64\pi\ell_0^2/45$. The proportionality is structural; the pure numerical prefactor is convention-locked and should be recomputed independently from $a_2$ on $f$ before being treated as scheme-free.

---

*Note IX — $G_N$ derivation structure.*
