from market_microcosm.replacement_kpi_bridge import (
    comparability,
    new_revenue_per_employee_metric,
    old_arr_metric,
    replacement_kpi_bridge_report_payload,
)


def test_new_metric_backfill_is_internally_comparable() -> None:
    metric = new_revenue_per_employee_metric()
    assert metric.retrospective_backfill is True
    assert comparability(metric, metric)["decision"] == "COMPARABLE"


def test_backfill_does_not_bridge_old_arr_construct() -> None:
    row = comparability(old_arr_metric(), new_revenue_per_employee_metric())
    assert row["same_construct"] is False
    assert row["same_scope"] is False
    assert row["authorized"] is False
    assert row["decision"] == "REJECT_CONSTRUCT_BRIDGE"


def test_e091_promotion_contract() -> None:
    payload = replacement_kpi_bridge_report_payload()
    assert all(payload["promotion_gate"].values())
    assert payload["promoted_bridge_rule"] == (
        "replacement-kpi-backfill-does-not-bridge-different-constructs-v1"
    )
