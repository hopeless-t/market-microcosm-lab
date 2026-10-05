from market_microcosm.reporting_kernel_state import (
    cross_kernel_estimator_authority,
    degraded_kernel,
    metric_status,
    reporting_kernel_report_payload,
    rich_kernel,
)


def test_kernel_transition_changes_metric_visibility() -> None:
    assert metric_status("arr", rich_kernel()) == "OBSERVED_UNDER_ACTIVE_KERNEL"
    assert metric_status("arr", degraded_kernel()) == "NOT_OBSERVED_UNDER_ACTIVE_KERNEL"
    assert degraded_kernel().generation == 2


def test_cross_kernel_arr_estimator_fails_closed() -> None:
    row = cross_kernel_estimator_authority({"arr"})
    assert row["old_kernel_visible"] is True
    assert row["new_kernel_visible"] is False
    assert row["authorized"] is False
    assert row["decision"] == "ABSTAIN_KERNEL_BREAK"


def test_e080_promotion_contract() -> None:
    payload = reporting_kernel_report_payload()
    assert all(payload["promotion_gate"].values())
    assert payload["promoted_kernel_rule"] == (
        "reporting-policy-change-creates-new-observation-kernel-generation-v1"
    )
