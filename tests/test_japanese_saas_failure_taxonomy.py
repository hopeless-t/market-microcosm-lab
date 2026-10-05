from market_microcosm.japanese_saas_failure_taxonomy import (
    case_fingerprints,
    taxonomy_report_payload,
)


def test_three_cases_have_distinct_mechanism_fingerprints() -> None:
    fingerprints = case_fingerprints()
    vectors = {tuple(values.values()) for values in fingerprints.values()}
    assert len(vectors) == 3
    assert fingerprints["BBD_portfolio_transition"]["exit_decided"] is False
    assert fingerprints["Allied_overseas_saas_exit"]["reporting_kernel_break"] is True
    assert fingerprints["Jooto_business_exit"]["runoff_transition"] is True


def test_e096_promotion_contract() -> None:
    payload = taxonomy_report_payload()
    assert all(payload["promotion_gate"].values())
    assert payload["promoted_taxonomy_rule"] == (
        "japanese-saas-negative-evidence-requires-typed-mechanism-vector-v1"
    )
