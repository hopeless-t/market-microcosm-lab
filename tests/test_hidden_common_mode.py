from market_microcosm.hidden_common_mode import (
    exact_forge_probability,
    hidden_common_mode_report_payload,
    hidden_common_mode_shocks,
    minimum_shocks_to_forge,
    nominal_independent_shocks,
)


def test_hidden_dependency_collapses_minimum_shock_count() -> None:
    nominal = nominal_independent_shocks(probability=0.01)
    hidden = hidden_common_mode_shocks(probability=0.01)

    assert minimum_shocks_to_forge(nominal) == 3
    assert minimum_shocks_to_forge(hidden) == 1


def test_hidden_dependency_inflates_exact_probability() -> None:
    nominal = exact_forge_probability(
        nominal_independent_shocks(probability=0.01)
    )
    hidden = exact_forge_probability(
        hidden_common_mode_shocks(probability=0.01)
    )

    assert abs(nominal - 0.0000098506) < 1e-12
    assert abs(hidden - 0.010009752094) < 1e-12
    assert hidden / nominal > 1000


def test_e023_promotion_contract() -> None:
    payload = hidden_common_mode_report_payload()
    assert all(payload["promotion_gate"].values())
    assert (
        payload["promoted_dependency_rule"]
        == "declared-domain-independence-requires-hidden-dependency-audit-v1"
    )
