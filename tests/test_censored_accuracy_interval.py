from market_microcosm.censored_accuracy_interval import (
    censored_accuracy_interval_report_payload,
    full_population_accuracy_interval,
    threshold_decision,
)


def test_full_population_accuracy_interval() -> None:
    row = full_population_accuracy_interval()
    assert row["accuracy_lower_bound"] == 0.8
    assert row["accuracy_upper_bound"] == 1.0


def test_threshold_authority_is_decision_scoped() -> None:
    assert threshold_decision(0.75)["decision"] == "CERTIFIED_PASS"
    assert threshold_decision(0.90)["decision"] == "ABSTAIN_CENSORED_LABELS"


def test_e084_promotion_contract() -> None:
    payload = censored_accuracy_interval_report_payload()
    assert all(payload["promotion_gate"].values())
    assert payload["promoted_interval_rule"] == (
        "censored-evaluation-uses-full-population-performance-intervals-v1"
    )
