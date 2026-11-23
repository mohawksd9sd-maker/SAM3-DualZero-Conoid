"""Repo-relative import paths for the Dual-Zero model re-runs."""

from __future__ import annotations

import sys
from pathlib import Path

# experiments/dual_zero_toe/ -> repo root
REPO = Path(__file__).resolve().parents[2]
CODE = REPO / "code"
ALT = REPO / "experiments" / "alt_geometries"
PS = REPO / "experiments" / "ps_conoid_product"
MP = REPO / "experiments" / "missing_principle"
FC = REPO / "experiments" / "further_candidates"
EXPERIMENTS = REPO / "experiments"


def ensure_imports() -> None:
    for p in (REPO, CODE, ALT, PS, MP, FC, EXPERIMENTS):
        s = str(p)
        if s not in sys.path:
            sys.path.insert(0, s)
