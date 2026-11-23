# Core reproducibility output

Run from the repository root, after `pip install -r requirements.txt`:

```bash
python code/core_reproducibility.py
pytest -q
```

`core_results.json` is written by that script. It records every number discussed in the November 2026 core paper, including values that *fail* to match earlier drafts (the $C_0$ band $4.43$–$4.45$, and $\omega_0=0.927$ from natural curvature radii).
