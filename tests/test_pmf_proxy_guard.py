from market_microcosm.pmf_proxy_guard import (
    finite_proxy_trap,
    pmf_proxy_guard_report_payload,
    proxy_trap_cases,
)


def test_postmortems_include_three_distinct_proxy_failures() -> None:
    cases = proxy_trap_cases()
    assert len(cases) == 3
    assert {row.case_id for row in cases} == {
        "srush-false-pmf",
        "leaner-revenue-without-scale",
        "salesnow-revenue-with-market-ceiling",
    }


def test_revenue_ranking_can_reverse_viability_ranking() -> None:
    row = finite_proxy_trap()

    assert row["revenue_winner"] == "short_run_revenue_maximizer"
    assert row["viability_winner"] == "lower_revenue_viable_candidate"
    assert row["proxy_reversal"] is True


def test_e031_promotion_contract() -> None:
    payload = pmf_proxy_guard_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_proxy_rule"] == (
        "short-run-positive-signals-cannot-certify-pmf-v1"
    )
