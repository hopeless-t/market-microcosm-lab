from market_microcosm.probe_robustness_compiler import (
    compile_probe_portfolio,
    robustness_compiler_report_payload,
)


def test_zero_error_budget_matches_minimum_noiseless_portfolio() -> None:
    row = compile_probe_portfolio(0)

    assert row["status"] == "SAT"
    assert row["selected"]["probe_ids"] == ["ab", "ac", "bc"]
    assert row["selected"]["total_cost"] == 4


def test_one_error_budget_requires_full_probe_code() -> None:
    row = compile_probe_portfolio(1)

    assert row["status"] == "SAT"
    assert row["selected"]["probe_count"] == 6
    assert row["selected"]["total_cost"] == 12
    assert row["selected"]["minimum_hamming_distance"] == 3


def test_two_error_budget_fails_closed() -> None:
    row = compile_probe_portfolio(2)

    assert row["status"] == "UNSAT"
    assert row["selected"] is None
    assert row["required_hamming_distance"] == 5


def test_e054_promotion_contract() -> None:
    payload = robustness_compiler_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_compiler_rule"] == (
        "lineage-probe-authority-compiled-from-declared-error-budget-v1"
    )
