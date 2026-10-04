from market_microcosm.lineage_probe_portfolio import (
    exact_minimum_probe_portfolio,
    minimum_probe_portfolio_report_payload,
)


def test_exact_minimum_probe_portfolio() -> None:
    row = exact_minimum_probe_portfolio()
    selected = row["selected"]

    assert selected["probe_ids"] == ["ab", "ac", "bc"]
    assert selected["probe_count"] == 3
    assert selected["total_cost"] == 4


def test_selected_signatures_identify_all_hypotheses() -> None:
    row = exact_minimum_probe_portfolio()
    signatures = row["selected"]["signatures"]

    assert len({tuple(value) for value in signatures.values()}) == 5


def test_e052_promotion_contract() -> None:
    payload = minimum_probe_portfolio_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_probe_rule"] == (
        "lineage-discovery-probes-use-exact-minimum-identifying-portfolio-v1"
    )
