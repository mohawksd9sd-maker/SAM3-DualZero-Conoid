"""Put the repo root and code/ directory on sys.path for pytest."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODE = ROOT / "code"
for p in (ROOT, CODE):
    s = str(p)
    if s not in sys.path:
        sys.path.insert(0, s)
