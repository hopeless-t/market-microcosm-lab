from market_microcosm.phase_e079_e098 import phase_report_payload


def test_phase_e079_e098_integrates_all_promoted_rules() -> None:
    payload = phase_report_payload()
    assert payload["phase"] == "E079-E098"
    assert payload["experiment_count"] == 20
    assert payload["all_experiments_promoted"] is True
    assert all(payload["phase_invariants"].values())
    assert [row["experiment"] for row in payload["experiments"]] == [
        f"E{number:03d}" for number in range(79, 99)
    ]
