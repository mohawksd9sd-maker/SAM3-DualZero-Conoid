"""T²/Z₄: Dual-Zero cannot change integer sector counts or force M = 3.

The C₄-compatible modulus is already τ = i (doc 49).  Zero-mode sector
dimensions on a magnetized square torus are representation-theoretic
integers (Kobayashi–Nagamoto / Abe et al., implemented in
experiments/missing_principle/z4_orbifold.py).  An integer kernel
dimension is independent of Reg₂, of ω₀, and of a spectral-parameter
shift.  Sectors of dimension 3 exist for a range of fluxes (M = 8, 9,
10, 11 in the invariant sector at α = 0); that range is not narrowed
by Dual-Zero.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict

_ROOT = Path(__file__).resolve().parents[2]
_MP = _ROOT / "experiments" / "missing_principle"
if str(_MP) not in sys.path:
    sys.path.insert(0, str(_MP))

from z4_orbifold import literature_counts_alpha0, sector_counts  # noqa: E402


def invariant_sector_dimension(M: int) -> int:
    return sector_counts(M)["+1"]


def fluxes_with_invariant_dimension(target: int, M_max: int = 24) -> list[int]:
    return [M for M in range(1, M_max + 1) if invariant_sector_dimension(M) == target]


def report() -> Dict[str, object]:
    dim3 = fluxes_with_invariant_dimension(3)
    # Reg₂ has no argument to vary here: the counts are exact integers.
    # Record that they match the literature table and do not depend on ω₀.
    matches = all(sector_counts(M) == literature_counts_alpha0(M) for M in range(4, 16))
    return {
        "tau_already_fixed_to_i_by_C4": True,
        "index_or_sector_counts_depend_on_Reg2": False,
        "index_or_sector_counts_depend_on_omega0": False,
        "literature_agreement_M_4_to_15": matches,
        "fluxes_with_invariant_sector_dimension_3": dim3,
        "unique_flux_with_dimension_3": len(dim3) == 1,
        "verdict": (
            "On T²/Z₄ the complex structure is already fixed to τ = i by "
            "C₄ compatibility, independently of Dual-Zero.  Sector "
            "dimensions are integers and are unchanged by Reg₂.  A "
            "3-dimensional invariant sector occurs for several fluxes "
            f"({dim3}), so Dual-Zero does not single out M=3."
        ),
    }
