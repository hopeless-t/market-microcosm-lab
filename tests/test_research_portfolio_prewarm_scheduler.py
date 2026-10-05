from market_microcosm.research_portfolio_prewarm_scheduler import rpe005_report_payload


def test_rpe005_prewarm_scheduler_contract() -> None:
    payload = rpe005_report_payload()
    assert payload["experiment"] == "RPE-005"
    assert all(payload["promotion_gate"].values())

    deadline = payload["portfolios"]["deadline_trap"]
    density = payload["portfolios"]["density_trap"]

    assert deadline["oracle"]["total_value"] == 17
    assert deadline["greedy_value"]["total_value"] == 14
    assert deadline["greedy_arrival"]["total_value"] == 14
    assert deadline["greedy_density"]["total_value"] == 17

    assert density["oracle"]["total_value"] == 22
    assert density["greedy_value"]["total_value"] == 22
    assert density["greedy_density"]["total_value"] == 16
    assert density["greedy_arrival"]["total_value"] == 16

    assert payload["claim_ceiling"].startswith("EXACT_SMALL_SYNTHETIC")
