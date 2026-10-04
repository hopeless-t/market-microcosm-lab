from market_microcosm.sequential_evidence_acquisition import (
    expected_cost_for_order,
    optimal_expected_cost,
    safe_path_policy,
    sequential_acquisition_report_payload,
)


def test_exact_sequential_policy():
    cost, first = optimal_expected_cost(frozenset())
    assert first == "gtm-pack"
    assert round(cost, 4) == 9.0225
    assert safe_path_policy() == [
        "gtm-pack",
        "signed-strategy-gap-attestation",
        "finance-pack",
    ]


def test_exact_policy_beats_cost_only_bundle_order():
    baseline = expected_cost_for_order(
        ("gtm-pack", "finance-pack", "signed-strategy-gap-attestation")
    )
    optimal, _ = optimal_expected_cost(frozenset())
    assert round(baseline, 5) == 9.32385
    assert optimal < baseline < 14


def test_e069_promotion_contract():
    x = sequential_acquisition_report_payload()
    assert all(x["promotion_gate"].values())
    assert x["promoted_sequential_rule"] == (
        "sequential-warning-acquisition-minimizes-expected-decision-cost-v1"
    )
