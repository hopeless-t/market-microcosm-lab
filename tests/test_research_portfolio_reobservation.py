from market_microcosm.research_portfolio_reobservation import rpe007_report_payload


def test_rpe007_reobservation_contract() -> None:
    payload = rpe007_report_payload()
    assert payload["experiment"] == "RPE-007"
    assert all(payload["promotion_gate"].values())

    stale = payload["stale_event"]
    assert stale["wake_succeeded"] is True
    assert stale["freshness_check"] == "STALE"
    assert stale["old_projection_authority_after_check"] == "REVOKED"

    static = payload["policies"]["static_commitment"]
    greedy = payload["policies"]["immediate_reobserve_greedy"]
    adaptive = payload["policies"]["exact_safe_replan"]

    assert static["captured_value"] == 13
    assert static["mandatory_preserved"] is True

    assert greedy["captured_value"] == 22
    assert greedy["mandatory_preserved"] is False

    assert adaptive["captured_value"] == 15
    assert adaptive["mandatory_preserved"] is True
    assert adaptive["selected"] == [
        "fresh-C",
        "mandatory-verification",
        "reobserve-stale-A",
    ]
    assert adaptive["schedule"] == {
        "mandatory-verification": 2,
        "reobserve-stale-A": 3,
        "fresh-C": 4,
    }
    assert adaptive["work_units"] == 16
    assert payload["claim_ceiling"].startswith("EXACT_SMALL_SYNTHETIC")
