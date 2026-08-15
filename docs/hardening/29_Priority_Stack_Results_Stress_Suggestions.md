# Priority Stack — Results, Stress Tests, Suggestions

**Status:** Executed and recorded (August 2026)  
**Rule:** Derivation only; no experimental retuning; no overclaim.

Script: `code/priority_stack.py` → `pipeline_output/08_priority_stack_report.json`

---

## 1. What was run

1. Hierarchical $\theta_{13}$ + CKM reconstruction  
2. High-resolution P4 overlap diagnostics + Dirac residual check  
3. Warped / geometric Higgs band path  
4. RH radial hierarchy → $\delta_{\rm PMNS}$ band narrowing  
5. Stress tests: $\eta\pm 2\%$, Casimir ratios $\pm 5\%$, $\omega_0\in\{0.91,0.927,0.94\}$

---

## 2. Results (baseline)

### 2.1 $\theta_{13}$ + CKM

| Quantity | Value | Notes |
|----------|-------|-------|
| Locked $\theta_{13}$ | $0.24^\circ$ | Bi-unitary archive (authoritative) |
| Hierarchical reduced formula | $\approx 4.87^\circ$ | Overestimates |
| 1–2–3 chain formula | $\approx 0.70^\circ$ | Closer but not equal |
| Geometric mean blend | $\approx 1.84^\circ$ | Still $\gg 0.24^\circ$ |
| **CKM with locked angles** | $\delta\approx 71.8^\circ$, $J\approx 3.55\times 10^{-5}$ | **Good** |
| $\|V_{us}\|,\|V_{cb}\|,\|V_{ub}\|$ | $0.222$, $0.041$, $0.0042$ | Consistent with locks |

**Critical stress finding:** Replacing locked $\theta_{13}$ by the blend ($1.84^\circ$) **spoils** CKM:

- $J\to 2.7\times 10^{-4}$ (too large)  
- $\|V_{ub}\|\to 0.032$ (far above data)

**Conclusion:** Reduced $\eta$–$C_g$ formulas explain *smallness* of $\theta_{13}$ only qualitatively. The **bi-unitary lock $0.24^\circ$ must stay**. Do not promote the blend to a replacement angle.

### 2.2 P4 overlaps / light Yukawa residual

| Check | Result |
|-------|--------|
| Dirac P4 residual | $\sim 10^{-10}$ on accepted runs — **excellent** |
| $\|\lambda\|_{\min}$ | $\sim 0.065$ at $u_{\max}=6$ |
| Live evec overlaps vs locked $\eta$ | Still $O(0.2)$–$O(0.6)$ off |
| Synthetic high-res windows | Symmetric $\eta_{ij}\sim 0.26$; not yet locked continuum integrals |
| $\kappa_u/\kappa_d=1/2$ | Still the structural light-up fix |

**Conclusion:** Operator quality is production-path grade. **Overlap→locked $\eta$ regeneration is not closed.** Light Yukawa digit residual remains continuum/Dual-Zero limited.

### 2.3 Higgs band

| $\omega_0$ | Band (GeV) |
|-----------|------------|
| $0.927$ (lock) | **[123, 127]** |
| $0.91$ | [120.4, 124.5] |
| $0.94$ | [124.9, 129.0] |

**Conclusion:** Class claim stable at geometric $\omega_0$. Digit claim still forbidden. Stress shows band moves $O(\mathrm{GeV})$ if $\omega_0$ is forced off lock — another reason not to retune $\omega_0$.

### 2.4 RH hierarchy → $\delta_{\rm PMNS}$

| Quantity | Value |
|----------|-------|
| RH proxies $(r_1,r_2,r_3)$ | $(1.0,\,0.885,\,0.360)$ |
| Previous band | $200^\circ$–$270^\circ$ |
| **Narrowed band** | $\approx 194^\circ$–$255^\circ$ |
| Center | $\approx 224^\circ$ |
| Narrowed? | **Yes** (geometry only) |

**Conclusion:** First successful **parameter-free narrowing** of the PMNS CP band from Casimir-derived RH hierarchy. Still a band, not a degree-level prediction.

---

## 3. Stress-test summary

| Window | Behavior |
|--------|----------|
| $\eta\pm 2\%$ | $\theta_{13}$ blend stable under pure $\eta$ rescaling in current formula (ratio-driven); $J$ from blend stays wrong vs lock |
| Casimir $\pm 5\%$ | $\theta_{13}$ blend moves $\sim\pm 0.05^\circ$; PMNS band edges move $<1^\circ$ |
| $\omega_0$ off lock | Higgs band shifts $O(\mathrm{GeV})$ — **do not move $\omega_0$** |

No stress case justified retuning to PDG. Locked angles + geometric $\omega_0$ remain the stable core.

---

## 4. Honest scorecard after the push

| Priority | Outcome |
|----------|---------|
| 1. $\theta_{13}$ + CKM precision | CKM with **locked** angles is solid; reduced $\theta_{13}$ formula **not** ready to replace lock |
| 2. P4 → light Yukawa | Dirac residual excellent; $\eta$ regeneration **open** |
| 3. Warped $a_4$ / Higgs | Band path confirmed; sub-GeV **not** achieved |
| 4. RH hierarchy → $\delta_{\rm PMNS}$ | **Band narrowed** geometrically — real progress |
| Unification / $\Lambda$ / RH proof | Left residual (correct) |

---

## 5. Suggestions (ordered by leverage, still derivation-only)

### A — Highest leverage next math

1. **Full bi-unitary $\theta_{13}$ derivation write-up**  
   Expand the explicit $Y_u,Y_d$ singular-vector calculation that produces $0.24^\circ$ so the reduced formula can be *corrected* by hierarchical eigenvalues, not replaced by a wrong blend.

2. **Defect overlaps from continuum zero-mode density with Casimir localization**  
   Live P4 fails to hit locked $\eta$ because generation localization is not pure angular windows. Insert Casimir radial weights into the overlap integrand (doc 09 + P4).

3. **Freeze RH hierarchy eigenvalues from the same radial ODE as quark Casimirs**  
   Replace proxy $(r_2,r_3)$ with solutions of the radial tip potential for RH modes; then recompute the PMNS band.

### B — Medium leverage

4. Symbolic / numerical warped-product $a_4$ terms that enter $\lambda$ and $Z_H$ only — shrink band if the residual budget is truly reduced.  
5. Commit high-resolution gap/residual tables as static artifacts for offline reproducibility.

### C — Do not do

6. Do **not** replace locked $\theta_{13}$ with the $1.84^\circ$ blend.  
7. Do **not** move $\omega_0$ to chase $m_H=125.1$.  
8. Do **not** claim percent-level unification or RH proof from this stack.

---

## 6. Bottom line

**Tested and stress-tested.**  

- **Win:** CKM observables from locked angles; Dirac residuals; PMNS band narrowed by geometric RH hierarchy.  
- **Open:** True first-principles $\theta_{13}$ reduced formula; live $\eta_{ij}$ regeneration; sub-GeV Higgs.  
- **Stable under stress:** locked core ($\omega_0$, angles, $\phi$) — residual windows do not force retuning.

---

*Derivation only. Run: `python code/priority_stack.py`.*
