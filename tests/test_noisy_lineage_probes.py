from market_microcosm.noisy_lineage_probes import (
    exact_one_error_tolerant_portfolio,
    exhaustive_single_error_decode_check,
    minimal_portfolio_noise_counterexample,
    noisy_lineage_probe_report_payload,
)


def test_e052_minimal_portfolio_breaks_on_one_error() -> None:
    row = minimal_portfolio_noise_counterexample()

    assert row["minimum_hamming_distance"] == 1
    assert row["single_error_causes_exact_alias"] is True


def test_exact_robust_portfolio_uses_all_six_probes() -> None:
    row = exact_one_error_tolerant_portfolio()["selected"]

    assert row["probe_count"] == 6
    assert row["total_cost"] == 12
    assert row["minimum_hamming_distance"] == 3


def test_all_single_error_patterns_decode_correctly() -> None:
    row = exhaustive_single_error_decode_check()

    assert row["case_count"] == 35
    assert row["all_correct"] is True


def test_e053_promotion_contract() -> None:
    payload = noisy_lineage_probe_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_noise_rule"] == (
        "lineage-probe-error-tolerance-requires-distance-three-signatures-v1"
    )
