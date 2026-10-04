from market_microcosm.real_longitudinal_holdout import (
    component_holdouts,
    concentration_shock_context,
    real_longitudinal_holdout_report_payload,
)


def test_standard_component_real_holdout_is_tight() -> None:
    row = component_holdouts()["smart_living_standard"]

    assert row["holdout"] == 216.0
    assert 215.0 < row["predicted_holdout"] < 216.0
    assert row["relative_error"] < 0.01


def test_same_decay_model_is_not_universal_across_components() -> None:
    rows = component_holdouts()

    assert rows["total_arr"]["relative_error"] > (
        rows["smart_living_standard"]["relative_error"]
    )
    assert rows["smart_living_light"]["relative_error"] > 0.20


def test_large_aggregate_shock_is_context_not_causal_identity() -> None:
    row = concentration_shock_context()

    assert row["arr_change_pct"] < -25.0
    assert row["revenue_change_pct"] < -40.0
    assert row["operating_income_swing_jpy_millions"] < -600.0


def test_e038_promotion_contract() -> None:
    payload = real_longitudinal_holdout_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_longitudinal_rule"] == (
        "event-annotated-component-longitudinal-holdout-v1"
    )
