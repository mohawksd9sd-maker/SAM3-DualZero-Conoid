# Section 4 — Riemann Hypothesis Direction (Residual Lock)

**Status:** Residual discipline locked (August 2026)  
**Rule:** Derivation only; **no claim of a proof of RH**.

This note closes the ordered §4 block. It supersedes any stronger RH language in older papers or abstracts.

---

## 1. Precise status (one sentence)

The Dual-Zero / information-current structure of SAM3 defines a **variational selection principle** whose stationary configurations satisfy $\operatorname{Re}(s)=1/2$; this is **not** a proof of the classical Riemann Hypothesis.

---

## 2. What the proposal is

### 2.1 Information current and action

From conoid spectral data, 12-bridge overlaps, and the Dual-Zero regulator (doc 18) one constructs an information current $J$ and action

$$
S_I = \int |J|^2\,d\mu
$$

on a suitable space of spectral parameters (Paper 11; `SAM3_RH_Variational_Proposal.tex`).

### 2.2 Variational selection principle (internal to SAM3)

**Statement (model-internal):**  
Critical points of $S_I$ (solutions of $\delta S_I = 0$) satisfy

$$
\operatorname{Re}(k) = \frac12.
$$

**Interpretation:** The geometry + Dual-Zero grading select a critical line for *this* action. That is a property of the SAM3 variational problem.

### 2.3 Error control already present (not a proof of RH)

Core definitions and related notes record Dual-Zero error bounds of the form

$$
|E(1/2+it)| \le \exp(-c\log^2|t|)
$$

and related statements about non-creation of zeros by the error term for large $|t|$. These control the **SAM3 spectral zeta / regularized objects**. They do **not** by themselves identify those objects with the classical Riemann $\zeta(s)$ or prove that every non-trivial zero of $\zeta$ lies on $\operatorname{Re}(s)=1/2$.

---

## 3. What is explicitly **not** claimed

| Not claimed |
|-------------|
| A proof of the Riemann Hypothesis |
| Equivalence $S_I \Leftrightarrow \zeta(s)$ |
| That every non-trivial zero of $\zeta$ is a critical point of $S_I$ |
| That Dual-Zero error estimates alone finish RH |
| That Archimedean recovery of $\zeta_{\rm conoid}$ is already classical $\zeta$ |

Paper 11 already states the negative list carefully; this note elevates it to the **hardening claim surface**.

---

## 4. Gap analysis: what a future proof would require

To upgrade from “variational proposal” to “proof of RH” one would need a chain of the form:

1. **Identification:** Prove that the SAM3 spectral / information object is the classical $\zeta$ (or a function whose zeros coincide with those of $\zeta$) with controlled error.  
2. **Exhaustion:** Prove that every non-trivial zero of $\zeta$ arises as a stationary point of $S_I$ (or as a zero of the identified object).  
3. **Remainder:** Show Dual-Zero / geometric remainders cannot move zeros off the critical line.  
4. **Global:** Close the argument for all $|t|$, not only large-$|t|$ regimes.

**None of (1)–(4) is complete in the locked corpus.** Until they are, RH remains residual.

---

## 5. Why this residual is correct science practice

- RH is a millennium-class problem; geometric motivation is allowed.  
- Overclaiming a proof would destroy credibility of the SM/gravity locks (CKM, $G_N$, generations, etc.).  
- Keeping RH as a **research direction** preserves honesty without discarding a potentially interesting variational structure.

---

## 6. Relation to Dual-Zero and continuum locks

| Ingredient | Role for RH proposal | Role for SM/gravity |
|------------|----------------------|---------------------|
| Dual-Zero $\varepsilon(n)$, $\operatorname{Reg}_2$ | Enters $S_I$ and error bounds | UV regulator for spectral action |
| Conoid geometry | Defines $J$ / overlaps | Dirac, Yukawas, $G_N$ |
| Continuum residual (doc 10) | Numerical stability of spectral data | Zero-mode / generation support |

RH residual status does **not** weaken the locked SM/gravity results in §1–§3.

---

## 7. Public-language rule

**Allowed:**  
“SAM3 contains a Dual-Zero information-current variational principle that selects $\operatorname{Re}(s)=1/2$ for its own critical points.”

**Forbidden:**  
“SAM3 proves the Riemann Hypothesis.”  
“RH follows from Dual-Zero.”  
Any abstract or README line that implies a finished proof.

README / STATUS / paper supersession banners already point here and to doc 17.

---

## 8. Lock statement

> The Riemann Hypothesis appears in SAM3 only as a **variational / information-current proposal**: stationarity of a geometrically defined action $S_I$ forces $\operatorname{Re}(k)=1/2$ for critical points of that action. This is **not** a proof of the classical Riemann Hypothesis. Identification with $\zeta(s)$, exhaustion of all non-trivial zeros, and global remainder control remain open. Dual-Zero error estimates support the internal spectral analysis; they do not close RH. All public claim surfaces must treat RH as residual.

---

## 9. Ordered program completion

| Block | Status |
|-------|--------|
| §1 Foundational mathematical closure (1a–1d) | **Complete** |
| §2 Numerical production readiness (P1–P4) | **Complete** |
| §3 Precision phenomenology residuals | **Complete** |
| §4 Riemann Hypothesis direction | **Complete** (residual-only lock) |

The ordered list from the foundational-closure request is finished under the derivation-only rule.

---

*Locked under the rule: derivation only, no overclaim.*
