from market_microcosm.human_delivery_cost import (
    delivery_cost_ranking_reversal,
    human_delivery_cost_report_payload,
)


def test_hidden_human_cost_reverses_margin_ranking() -> None:
    row = delivery_cost_ranking_reversal()

    assert row["apparent_margin_winner"] == "human_heavy_high_acv"
    assert row["fully_loaded_margin_winner"] == "product_led_lower_acv"
    assert row["ranking_reversal"] is True


def test_e034_promotion_contract() -> None:
    payload = human_delivery_cost_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_delivery_rule"] == (
        "fully-loaded-human-delivery-cost-required-v1"
    )
