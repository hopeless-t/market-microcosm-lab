from market_microcosm.empirical_warning_tournament import (
    empirical_warning_tournament_report_payload,
    score,
    scalar_sign_rule,
    typed_mechanism_rule,
)


def test_scalar_sign_rule_false_positive_and_false_negatives() -> None:
    row = score(scalar_sign_rule)
    assert row["confusion"] == {"tp": 0, "fp": 1, "tn": 1, "fn": 2}


def test_typed_mechanism_rule_exact_on_semantic_suite() -> None:
    row = score(typed_mechanism_rule)
    assert row["confusion"] == {"tp": 2, "fp": 0, "tn": 2, "fn": 0}
    assert row["accuracy"] == 1.0


def test_e098_promotion_contract() -> None:
    payload = empirical_warning_tournament_report_payload()
    assert all(payload["promotion_gate"].values())
    assert payload["promoted_empirical_warning_rule"] == (
        "real-case-warning-escalation-requires-typed-mechanism-evidence-v1"
    )
