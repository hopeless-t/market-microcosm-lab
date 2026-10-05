from market_microcosm.regional_complexity import (
    discovery_complexity_frontier,
    minimum_admissible_complexity,
    one_quarter_forward_holdout,
    regional_complexity_report_payload,
)


def test_exact_complexity_frontier_has_expected_knee() -> None:
    frontier = discovery_complexity_frontier()

    assert frontier[1]["worst_max_relative_error"] > 0.50
    assert frontier[2]["worst_max_relative_error"] > 0.20
    assert frontier[3]["worst_max_relative_error"] < 0.09
    assert frontier[4]["worst_max_relative_error"] == 0.0


def test_three_group_partition_is_selected() -> None:
    selection = minimum_admissible_complexity()
    assert selection["minimum_group_count"] == 3
    assert selection["selected"]["partition"] == [
        ["APAC", "LATAM"],
        ["EMEA"],
        ["UCAN"],
    ]


def test_selected_topology_survives_one_quarter_forward_holdout() -> None:
    partition = (
        ("APAC", "LATAM"),
        ("EMEA",),
        ("UCAN",),
    )
    row = one_quarter_forward_holdout(partition)

    assert row["calibration_quarter"] == "Q1-2024"
    assert row["holdout_quarter"] == "Q2-2024"
    assert row["max_relative_error"] < 0.10


def test_e025_promotion_contract() -> None:
    payload = regional_complexity_report_payload()

    assert all(payload["promotion_gate"].values())
    assert (
        payload["promoted_regional_rule"]
        == "regional-arm-complexity-knee-k3-v1"
    )
