from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ProxyTrapCase:
    case_id: str
    positive_signal: str
    hidden_failure: str
    decision: str
    source_url: str
    quantitative_anchor: tuple[tuple[str, float | int | str], ...]


def proxy_trap_cases() -> tuple[ProxyTrapCase, ...]:
    return (
        ProxyTrapCase(
            case_id="srush-false-pmf",
            positive_signal=(
                "revenue, high-price customers, and enthusiastic users existed"
            ),
            hidden_failure=(
                "customer attributes were inconsistent, human effort was high, "
                "and people rather than the product were solving the problem"
            ),
            decision=(
                "stop forcing sales outside the target, withdraw human-led "
                "problem solving, and continue repeated STP validation"
            ),
            source_url="https://note.com/srushhiguchi/n/n6dc615317659",
            quantitative_anchor=(
                ("years_from_founding_to_claimed_pmf", 4),
                ("employee_turnover_pct_in_reported_year", 50),
                ("initial_plg_saas_outcome", "withdrawn_soon_after_launch"),
            ),
        ),
        ProxyTrapCase(
            case_id="leaner-revenue-without-scale",
            positive_signal="product revenue eventually existed",
            hidden_failure=(
                "management still expected poor customer success and poor "
                "company scalability"
            ),
            decision="withdraw product and pivot",
            source_url="https://note.com/leaner/n/n0539a4b224bf",
            quantitative_anchor=(
                ("preceding_no_sales_period_months", 12),
            ),
        ),
        ProxyTrapCase(
            case_id="salesnow-revenue-with-market-ceiling",
            positive_signal=(
                "deep customer pain, products, acquisition spend, and an "
                "operating business existed"
            ),
            hidden_failure=(
                "management estimated the existing business could only reach "
                "roughly 2-3 billion JPY ARR"
            ),
            decision="complete withdrawal and pivot in 2022-04",
            source_url="https://note.com/yosukekume/n/n9b1db31669e7",
            quantitative_anchor=(
                ("estimated_arr_ceiling_jpy_billions_low", 2),
                ("estimated_arr_ceiling_jpy_billions_high", 3),
                ("upsell_products_released", 5),
            ),
        ),
    )


def finite_proxy_trap() -> dict:
    candidates = (
        {
            "name": "short_run_revenue_maximizer",
            "current_revenue": 120.0,
            "repeatability": 0.25,
            "customer_success": 0.35,
            "scalability": 0.30,
            "market_headroom": 0.35,
        },
        {
            "name": "lower_revenue_viable_candidate",
            "current_revenue": 80.0,
            "repeatability": 0.85,
            "customer_success": 0.85,
            "scalability": 0.80,
            "market_headroom": 0.90,
        },
    )

    rows = []
    for candidate in candidates:
        viability = (
            candidate["repeatability"]
            * candidate["customer_success"]
            * candidate["scalability"]
            * candidate["market_headroom"]
        )
        rows.append({**candidate, "viability_product": viability})

    revenue_winner = max(rows, key=lambda row: row["current_revenue"])
    viability_winner = max(rows, key=lambda row: row["viability_product"])

    return {
        "candidates": rows,
        "revenue_winner": revenue_winner["name"],
        "viability_winner": viability_winner["name"],
        "proxy_reversal": (
            revenue_winner["name"] != viability_winner["name"]
        ),
    }


def pmf_proxy_guard_report_payload() -> dict:
    cases = proxy_trap_cases()
    witness = finite_proxy_trap()

    gates = {
        "multiple_postmortems_show_positive_signal_trap": len(cases) >= 3,
        "srush_explicitly_reports_false_pmf": any(
            case.case_id == "srush-false-pmf"
            and "human effort" in case.hidden_failure
            for case in cases
        ),
        "leaner_revenue_did_not_certify_scalability": any(
            case.case_id == "leaner-revenue-without-scale"
            for case in cases
        ),
        "salesnow_market_ceiling_overrode_local_traction": any(
            case.case_id == "salesnow-revenue-with-market-ceiling"
            for case in cases
        ),
        "finite_proxy_reversal_exists": witness["proxy_reversal"] is True,
        "revenue_is_not_promotion_evidence_by_itself": True,
    }

    return {
        "experiment": "E031",
        "question": (
            "Can locally positive SaaS signals such as revenue, high ACV, "
            "enthusiastic users, or current sales certify PMF and long-run "
            "market viability by themselves?"
        ),
        "postmortem_cases": [asdict(case) for case in cases],
        "finite_proxy_trap": witness,
        "promotion_gate": gates,
        "promoted_proxy_rule": (
            "short-run-positive-signals-cannot-certify-pmf-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "PMF/viability promotion must separately test repeatability, "
            "customer success, product-vs-human delivery burden, scalability, "
            "and market headroom. Revenue and engagement remain observations, "
            "not certification authority."
        ),
        "limitations": (
            "Company postmortems are retrospective narratives. The finite "
            "proxy witness is synthetic and demonstrates ranking reversal, "
            "not an estimated PMF equation."
        ),
    }
