from market_microcosm.redundant_probe_synthesis import (
    exact_redundancy_synthesis,
    exhaustive_two_error_decode_check,
    redundancy_synthesis_report_payload,
)


def test_exact_redundancy_design() -> None:
    row = exact_redundancy_synthesis()["selected"]

    assert row["repetition_counts"] == {
        "ab": 1,
        "ac": 2,
        "ad": 2,
        "bc": 2,
        "bd": 2,
        "cd": 1,
    }
    assert row["channel_count"] == 10
    assert row["total_cost"] == 20
    assert row["minimum_hamming_distance"] == 5


def test_all_up_to_two_bit_errors_decode_correctly() -> None:
    row = exhaustive_two_error_decode_check()

    assert row["case_count"] == 280
    assert row["all_correct"] is True


def test_e055_promotion_contract() -> None:
    payload = redundancy_synthesis_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_redundancy_rule"] == (
        "unsat-probe-robustness-may-expand-independent-measurement-channels-v1"
    )
