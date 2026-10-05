from market_microcosm.early_warning import (
    early_warning_report_payload,
    score_warning_rule,
)


def test_revenue_and_churn_proxies_have_expected_blind_spots() -> None:
    revenue = score_warning_rule("revenue_only")
    churn = score_warning_rule("churn_only")

    assert revenue["confusion"]["false_negative"] >= 4
    assert churn["confusion"]["false_negative"] >= 4
    assert churn["confusion"]["false_positive"] >= 1


def test_multi_signal_rule_matches_reference_oracle() -> None:
    row = score_warning_rule("multi_signal")

    assert row["accuracy"] == 1.0
    assert row["precision"] == 1.0
    assert row["recall"] == 1.0
    assert row["specificity"] == 1.0


def test_e035_promotion_contract() -> None:
    payload = early_warning_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_warning_rule"] == (
        "negative-evidence-multi-signal-early-warning-v1"
    )
