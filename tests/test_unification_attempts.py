"""Unification-derivation attempts: all current attempts fail honestly."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))

from unification_derivation_attempts import report, attempt_mass_ratios_from_E0


def test_all_current_attempts_fail():
    r = report()
    assert len(r["attempts"]) == 6
    for attempt, verdict in r["verdicts"].items():
        assert "failed" in verdict, (attempt, verdict)


def test_gauge_group_is_C4_not_SM():
    a = next(x for x in report()["attempts"] if "gauge" in x["attempt"])
    assert a["C4_check_samples"] is True
    assert a["A5_is_isometry"] is False


def test_mass_ratios_are_order_one_not_SM():
    a = attempt_mass_ratios_from_E0()
    r = a["geometric_ratios"]
    # published exact ratios, loosely checked
    assert 1.6 < r["E0(1)/E0(0)"] < 1.62
    assert 2.75 < r["E0(2)/E0(0)"] < 2.76
    assert a["min_absolute_mismatch_to_those_SM_ratios"] > 10.0


def test_untwisted_index_is_zero_in_unification_report():
    a = next(x for x in report()["attempts"] if "three generations" in x["attempt"])
    assert a["untwisted_AP_AP_index"] == 0
    assert a["kappa_derived"] is False
    assert a["analytic_disk_index_at_kappa_2.5"] == 3
