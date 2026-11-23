"""Z4-orbifold zero-mode counts on a magnetized square torus (τ = i).

Exploratory: not part of the locked SAM-3 core.

The conoid has a C4 isometry.  The unique modulus in the standard
fundamental domain whose torus admits a compatible Z4 rotation is τ = i.
The orbifold T²/Z4 is the corresponding quotient.  Zero modes of a
magnetized Dirac operator on T², of flux M, transform under that rotation,
and split into four charge sectors η ∈ {1, i, −1, −i}.

Literature (fetched, not invented)
---------------------------------
- T. Kobayashi and S. Nagamoto, "Zero-modes on orbifolds: magnetized
  orbifold models by modular transformation", Phys. Rev. D 96 (2017)
  096011, arXiv:1709.09784.  The S modular transformation at τ = i is
  the Z4 rotation.  On the basis of M fluxed zero modes it acts by the
  (unitary) discrete Fourier / Gauss-sum matrix whose trace is
      tr C = M^{-1/2} ∑_{k=0}^{M-1} exp(2π i k² / M)
  (their (53)).  Their Table III gives the sector counts for vanishing
  Scherk–Schwarz phases, and they record that the number of Z_N-invariant
  zero modes is ⌊M/N⌋+1 except in one Z3 case.
- T.-h. Abe, Y. Fujimoto, T. Kobayashi, T. Miura, K. Nishiwaki,
  M. Sakamoto, Nucl. Phys. B 890 (2015) 442–480, Table 5 (α=0) and
  Table 6 (α=1/2).  Independent wavefunction count, consistent with the
  later modular-transformation table.

This module constructs C_{jk} = M^{-1/2} exp(2π i j k / M), checks that
it is a unitary 4th-root representation (C^4 = I), and counts projector
ranks in each sector.  Those ranks are compared with Kobayashi–Nagamoto
Table III.  The Scherk–Schwarz sector α = 1/2 is not recomputed here; it
is cited from Abe et al., Table 6, only as literature.

A sector of dimension 3 is a construction, not a derivation of the
integer 3: it appears for a range of fluxes (M = 8,9,10,11 in the
invariant sector, for α = 0).
"""

from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np

ETAS = (("+1", 1.0 + 0.0j), ("+i", 1.0j), ("-1", -1.0 + 0.0j), ("-i", -1.0j))


def s_matrix(M: int) -> np.ndarray:
    """Unitary DFT matrix C_{jk} = M^{-1/2} exp(2π i j k / M), j,k = 0..M-1.

    This is the standard S-action on the flux-M zero-mode basis at τ = i
    (Kobayashi–Nagamoto; the overall constant phase that can appear in
    the modular transformation is omitted, since it does not change C^4 = I
    up to a phase that we check and, if needed, strip).
    """
    if M <= 0:
        raise ValueError("M must be a positive integer")
    j = np.arange(M)
    phase = np.exp(2j * np.pi * np.outer(j, j) / M)
    return phase / np.sqrt(M)


def _unitarity_error(C: np.ndarray) -> float:
    M = C.shape[0]
    return float(np.linalg.norm(C.conj().T @ C - np.eye(M)))


def _fourth_power_error(C: np.ndarray) -> float:
    M = C.shape[0]
    C4 = np.linalg.matrix_power(C, 4)
    # Allow a global phase, then compare to I.
    # If C^4 = e^{iφ} I, the (0,0) entry has modulus 1.
    phase = C4[0, 0]
    if abs(phase) < 1e-14:
        return float(np.linalg.norm(C4 - np.eye(M)))
    phase = phase / abs(phase)
    return float(np.linalg.norm(C4 / phase - np.eye(M)))


def sector_counts(M: int) -> Dict[str, int]:
    """Dimension of each Z4 eigenspace, from projector ranks / traces."""
    C = s_matrix(M)
    # C^4 should be I for the unitary DFT; if a leftover phase appears,
    # absorb it into C so that the eigenvalues are exact 4th roots of unity.
    C4 = np.linalg.matrix_power(C, 4)
    phase = C4[0, 0]
    if abs(phase) > 1e-14:
        # C^4 = e^{iφ} I  ⇒  replace C by C * e^{-iφ/4}
        C = C * np.exp(-1j * np.angle(phase) / 4.0)
    powers = [np.eye(M, dtype=complex), C, C @ C, C @ C @ C]
    out: Dict[str, int] = {}
    for name, eta in ETAS:
        P = np.zeros((M, M), dtype=complex)
        eta_bar = np.conj(eta)
        factor = 1.0
        for pwr in powers:
            P = P + factor * pwr
            factor *= eta_bar
        P /= 4.0
        # For an orthogonal projector the trace equals the rank and is an integer.
        tr = float(np.real(np.trace(P)))
        out[name] = int(round(tr))
    if sum(out.values()) != M:
        raise RuntimeError(f"sector counts for M={M} sum to {sum(out.values())}, not M")
    return out


def literature_counts_alpha0(M: int) -> Dict[str, int]:
    """Kobayashi–Nagamoto, PRD 96 (2017) 096011, Table III, α = 0.

    M = 4n, 4n+1, 4n+2, 4n+3 (n ≥ 0; the −i entry n−1 is used only for n ≥ 1,
    and equals 0 for M = 4).
    """
    if M <= 0:
        raise ValueError("M must be a positive integer")
    n, r = divmod(M, 4)
    if r == 0:
        return {"+1": n + 1, "-1": n, "+i": n, "-i": n - 1}
    if r == 1:
        return {"+1": n + 1, "-1": n, "+i": n, "-i": n}
    if r == 2:
        return {"+1": n + 1, "-1": n + 1, "+i": n, "-i": n}
    return {"+1": n + 1, "-1": n + 1, "+i": n + 1, "-i": n}


def invariant_count(M: int) -> int:
    """The η = +1 count, equal to ⌊M/4⌋ + 1 for α = 0."""
    return sector_counts(M)["+1"]


def fluxes_with_sector_dimension(dim: int, M_max: int = 24) -> Dict[str, List[int]]:
    out = {name: [] for name, _ in ETAS}
    for M in range(1, M_max + 1):
        counts = sector_counts(M)
        for name, n in counts.items():
            if n == dim:
                out[name].append(M)
    return out


def report() -> Dict[str, object]:
    sample = {M: sector_counts(M) for M in range(1, 17)}
    mismatches = []
    for M, counts in sample.items():
        lit = literature_counts_alpha0(M)
        if counts != lit:
            mismatches.append({"M": M, "computed": counts, "literature": lit})
    three = fluxes_with_sector_dimension(3, M_max=24)
    # Unitary / 4th-power checks at a few M.
    checks = []
    for M in (1, 3, 4, 8, 9, 11, 12):
        C = s_matrix(M)
        checks.append(
            {
                "M": M,
                "unitarity_error": _unitarity_error(C),
                "fourth_power_error": _fourth_power_error(C),
                "trC_minus_gauss_sum": _trace_versus_gauss(C, M),
            }
        )
    return {
        "tau": "i  (required for a Z4 rotation of T^2)",
        "Scherk_Schwarz": "alpha = (0,0)  (computed); alpha = 1/2 is literature only",
        "sample_counts_alpha0": {str(M): c for M, c in sample.items()},
        "mismatches_with_Kobayashi_Nagamoto_Table_III": mismatches,
        "fluxes_with_a_3-dimensional_sector_M_le_24": three,
        "invariant_sector_has_3_for_M": three["+1"],
        "matrix_checks": checks,
        "literature_alpha_half_note": (
            "Abe et al., Nucl. Phys. B 890 (2015) Table 6, for "
            "alpha=(1/2,1/2): the +1 sector has dimension 3 at M=10,11,12,13.  "
            "Not recomputed in this repository."
        ),
        "verdict": (
            "The Z4 orbifold redistributes the M torus zero modes into four "
            "sectors.  A 3-dimensional invariant sector occurs for a range of "
            "fluxes (M=8,9,10,11 at alpha=0), not for a unique M, and not for "
            "M=0.  This is a construction of three modes after a choice of M, "
            "not a principle that fixes the flux at 3."
        ),
    }


def _trace_versus_gauss(C: np.ndarray, M: int) -> float:
    tr = np.trace(C)
    gauss = sum(np.exp(2j * np.pi * (k * k) / M) for k in range(M)) / np.sqrt(M)
    return float(abs(tr - gauss))
