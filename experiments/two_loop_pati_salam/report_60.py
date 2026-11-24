"""Numbers quoted in doc 60 (run: python report_60.py, ~1 min)."""

from __future__ import annotations

import json
import math
from dataclasses import replace

import two_loop_higgs as th


def summary(o, label, thr):
    e = th.error_budget(o)
    c = e["central"]
    err = e["errors"]
    mt_tot = math.sqrt(err["dMt_theory"] ** 2 + err["dMt_parametric"] ** 2 + thr["Mt_std"] ** 2)
    mh_tot = math.sqrt(err["dMh_theory"] ** 2 + err["dMh_parametric"] ** 2 + thr["Mh_std"] ** 2)
    return {
        "label": label, "Mt_pred": c["Mt_pred"], "Mh_pred": c["Mh_pred"],
        "Mh_pred_at_obs_Mt": c["Mh_pred_at_obs_Mt"],
        "Mt_err_total": mt_tot, "Mh_err_total": mh_tot,
        "Mt_pull_sigma": (c["Mt_pred"] - 172.5) / math.sqrt(mt_tot ** 2 + 0.3 ** 2),
        "Mh_pull_sigma": (c["Mh_pred"] - 125.1) / math.sqrt(mh_tot ** 2 + 0.11 ** 2),
        "budget": e["shifts"], "errors": err, "m_R": c["m_R"], "Lambda": c["Lambda"], "g_U": c["g_U"],
    }


def report():
    thr = th.threshold_spread(10)
    out = {
        "benchmark_two_loop_qcd3": th.benchmark(2, True),
        "benchmark_two_loop": th.benchmark(2, False),
        "benchmark_one_loop": th.benchmark(1, False),
        "closure_yt_from_data": th.predict(th.Options(yt_from_data=True)),
        "one_loop_SM_below_mR": th.predict(th.Options(loops_sm=1)),
        "threshold_spread": thr,
        "composite_sigma": summary(th.Options(), "composite + sigma (n=1)", thr),
        "composite_no_sigma": summary(th.Options(sigma=False), "composite, no sigma", thr),
        "with2215_sigma": summary(th.Options(scenario="with2215"), "(2,2,15) light + sigma", thr),
        "ext_b_fit_n": {
            "yN0": th.fit_n_to_mh(th.Options()),
            "yN=2g": th.fit_n_to_mh(th.Options(yN_over_g=2.0)),
            "with2215": th.fit_n_to_mh(th.Options(scenario="with2215")),
        },
    }
    return out


if __name__ == "__main__":
    print(json.dumps(report(), indent=1, default=float))
