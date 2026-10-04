from market_microcosm.measurement_failure_domains import (
    bad_common_mode_counterexample,
    diversified_root_fault_check,
    measurement_failure_domain_report_payload,
)


def test_one_common_root_breaks_e055_bit_model() -> None:
    row = bad_common_mode_counterexample()

    assert row["flipped_channel_count"] == 5
    assert row["observed_equals_shared_abc_signature"] is True
    assert row["decoded_hypothesis"] == "shared-abc"
    assert row["misdecoded"] is True


def test_diversified_measurement_roots_survive_one_root_fault() -> None:
    row = diversified_root_fault_check()

    assert row["root_count"] == 5
    assert row["maximum_channels_per_root"] == 2
    assert row["case_count"] == 25
    assert row["all_correct"] is True


def test_e056_promotion_contract() -> None:
    payload = measurement_failure_domain_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_domain_rule"] == (
        "redundant-probe-channels-must-diversify-measurement-failure-roots-v1"
    )
