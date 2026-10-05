from market_microcosm.japan_failure_corpus import (
    TARGET_FAILURE_MECHANISMS,
    exact_minimum_failure_portfolio,
    japan_failure_corpus,
    japanese_failure_corpus_report_payload,
)


def test_failure_corpus_has_typed_limits() -> None:
    corpus = {row.case_id: row for row in japan_failure_corpus()}

    assert corpus["rickcloud-sunset-2026"].event_type == "planned_sunset"
    assert corpus["leaner-first-product-pivot"].event_type == (
        "product_withdrawal_and_pivot"
    )
    assert "not a SaaS-only cohort" in (
        corpus["tdb-software-bankruptcy-2025fy"].limitation
    )


def test_exact_failure_portfolio_covers_declared_mechanisms() -> None:
    row = exact_minimum_failure_portfolio()

    assert set(row["covered_mechanisms"]) == set(TARGET_FAILURE_MECHANISMS)
    assert row["selected_count"] >= 4


def test_e028_promotion_contract() -> None:
    payload = japanese_failure_corpus_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_failure_rule"] == (
        "negative-evidence-corpus-required-for-market-calibration-v1"
    )
    assert payload["survivorship_gap"]["new_mechanism_count"] == 10
