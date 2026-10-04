from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import combinations


@dataclass(frozen=True)
class FailureEvidence:
    case_id: str
    subject: str
    evidence_class: str
    event_type: str
    quantitative_anchors: tuple[tuple[str, float | int | str], ...]
    mechanisms: tuple[str, ...]
    source_url: str
    limitation: str


TARGET_FAILURE_MECHANISMS = (
    "acquisition_burn",
    "cash_conversion_lag",
    "customer_success_non_scalability",
    "data_compounding_misalignment",
    "engineering_maintenance_burden",
    "labor_cost_pressure",
    "market_ceiling",
    "platform_substitution",
    "portfolio_pruning",
    "product_sprawl",
)


def japan_failure_corpus() -> tuple[FailureEvidence, ...]:
    return (
        FailureEvidence(
            case_id="bbd-portfolio-pruning-2024",
            subject="BBD Initiative SaaS portfolio",
            evidence_class="official_ir",
            event_type="portfolio_pruning",
            quantitative_anchors=(
                ("fy2023_q4_arr_jpy_millions", 1593),
                ("fy2024_q3_arr_jpy_millions", 1607),
                ("fy2023_q4_churn_rate_pct", 1.15),
                ("fy2024_q3_churn_rate_pct", 2.33),
                ("fy2023_q4_arpa_jpy", 437545),
                ("fy2024_q3_arpa_jpy", 466303),
                ("fy2023_q4_contracts", 3641),
                ("fy2024_q3_contracts", 3416),
            ),
            mechanisms=("portfolio_pruning",),
            source_url=(
                "https://www.bbdi.co.jp/ir/pdf/"
                "2024%E5%B9%B49%E6%9C%88%E6%9C%9F%20"
                "%E7%AC%AC3%E5%9B%9B%E5%8D%8A%E6%9C%9F"
                "%E6%B1%BA%E7%AE%97%E9%80%9F%E5%A0%B1.pdf"
            ),
            limitation=(
                "Group-level SaaS KPIs mix multiple products and intentional "
                "plan migration; they are not a product-level causal estimate."
            ),
        ),
        FailureEvidence(
            case_id="bbd-restructuring-2026",
            subject="BBD Initiative restructuring",
            evidence_class="official_ir",
            event_type="withdrawal_and_restructuring",
            quantitative_anchors=(
                ("prior_impairment_jpy_millions", 730),
                ("office_fixed_cost_reduction_target_pct", 30),
                ("fy2026_q1_operating_margin_pct", 3.1),
            ),
            mechanisms=("data_compounding_misalignment", "portfolio_pruning"),
            source_url=(
                "https://www.bbdi.co.jp/ir/pdf/"
                "2026%E5%B9%B49%E6%9C%88%E6%9C%9F%20"
                "%E7%AC%AC1%E5%9B%9B%E5%8D%8A%E6%9C%9F"
                "%E6%B1%BA%E7%AE%97%E9%80%9F%E5%A0%B1.pdf"
            ),
            limitation=(
                "The disclosed restructuring is strategic and group-wide; "
                "it does not imply every withdrawn product was independently insolvent."
            ),
        ),
        FailureEvidence(
            case_id="rickcloud-sunset-2026",
            subject="RickCloud",
            evidence_class="official_service_notice",
            event_type="planned_sunset",
            quantitative_anchors=(
                ("new_sales_stop", "2026-12-31"),
                ("price_revision_from", "2027-01-01"),
                ("service_end_planned", "2029-03-28"),
            ),
            mechanisms=(
                "engineering_maintenance_burden",
                "platform_substitution",
            ),
            source_url="https://www.ricksoft.jp/news/n20260724.html",
            limitation=(
                "The notice does not publish customer count, margin, or the "
                "size of the price increase."
            ),
        ),
        FailureEvidence(
            case_id="leaner-first-product-pivot",
            subject="Leaner first product",
            evidence_class="company_postmortem",
            event_type="product_withdrawal_and_pivot",
            quantitative_anchors=(
                ("no_sales_period_months", 12),
            ),
            mechanisms=("customer_success_non_scalability",),
            source_url="https://note.com/leaner/n/n0539a4b224bf",
            limitation=(
                "Founder/team narrative is qualitative and does not disclose "
                "full unit economics or product-level revenue."
            ),
        ),
        FailureEvidence(
            case_id="salesnow-pre-2022-business-pivot",
            subject="SalesNow pre-2022 business portfolio",
            evidence_class="company_postmortem",
            event_type="complete_withdrawal_and_pivot",
            quantitative_anchors=(
                ("estimated_arr_ceiling_jpy_billions_low", 2),
                ("estimated_arr_ceiling_jpy_billions_high", 3),
                ("upsell_products_released", 5),
                ("monthly_ad_spend_description", "tens_of_millions_jpy"),
                ("withdrawal_decision", "2022-04"),
            ),
            mechanisms=("market_ceiling", "acquisition_burn", "product_sprawl"),
            source_url="https://note.com/yosukekume/n/n9b1db31669e7",
            limitation=(
                "The ARR ceiling is management's retrospective estimate, not "
                "an independently identified market-size parameter."
            ),
        ),
        FailureEvidence(
            case_id="tdb-software-bankruptcy-2025fy",
            subject="Japan software industry bankruptcy context",
            evidence_class="industry_aggregate",
            event_type="bankruptcy_context",
            quantitative_anchors=(
                ("bankruptcies_through_feb_2026", 195),
                ("debt_under_100m_share_pct", 84.6),
                ("information_services_labor_shortage_pct", 69.2),
                ("monthly_scheduled_salary_jpy_2025", 383755),
                ("salary_yoy_pct", 2.5),
                ("package_software_bankruptcies_through_feb_2026", 38),
            ),
            mechanisms=("labor_cost_pressure", "cash_conversion_lag"),
            source_url=(
                "https://www.tdb.co.jp/report/industry/"
                "20260309-softwaretousan/"
            ),
            limitation=(
                "TDB's software category includes contract development and "
                "package software; it is contextual evidence, not a SaaS-only cohort."
            ),
        ),
    )


def covered_failure_mechanisms(
    cases: tuple[FailureEvidence, ...],
) -> set[str]:
    covered: set[str] = set()
    for case in cases:
        covered.update(case.mechanisms)
    return covered


def exact_minimum_failure_portfolio(
    targets: tuple[str, ...] = TARGET_FAILURE_MECHANISMS,
) -> dict:
    corpus = japan_failure_corpus()
    target = set(targets)
    feasible: list[tuple[tuple, tuple[FailureEvidence, ...]]] = []

    for size in range(1, len(corpus) + 1):
        for subset in combinations(corpus, size):
            covered = covered_failure_mechanisms(subset)
            if target <= covered:
                score = (
                    size,
                    sum(
                        0 if case.evidence_class.startswith("official") else 1
                        for case in subset
                    ),
                    tuple(case.case_id for case in subset),
                )
                feasible.append((score, subset))
        if feasible:
            break

    if not feasible:
        missing = target - covered_failure_mechanisms(corpus)
        raise ValueError(f"failure corpus cannot cover targets: {sorted(missing)}")

    _, selected = min(feasible, key=lambda row: row[0])
    return {
        "target_mechanisms": sorted(target),
        "selected_case_ids": [case.case_id for case in selected],
        "selected_count": len(selected),
        "covered_mechanisms": sorted(
            covered_failure_mechanisms(selected) & target
        ),
    }


def survivorship_gap() -> dict:
    synthetic_pressure_axes = {
        "subscription_price_pressure",
        "platform_operating_cost_pressure",
        "baseline_user_churn_pressure",
    }
    empirical_failure_axes = set(TARGET_FAILURE_MECHANISMS)
    return {
        "existing_synthetic_pressure_axes": sorted(synthetic_pressure_axes),
        "new_failure_mechanisms": sorted(empirical_failure_axes),
        "new_mechanism_count": len(empirical_failure_axes),
        "interpretation": (
            "The current pressure ladder is not wrong; it is incomplete for "
            "Japanese SaaS/soft-service failure research. Failure evidence "
            "introduces market ceiling, customer-success scalability, "
            "substitution, maintenance burden, data-strategy fit, labor/cash "
            "pressure, acquisition burn, product sprawl, and intentional pruning."
        ),
    }


def japanese_failure_corpus_report_payload() -> dict:
    corpus = japan_failure_corpus()
    portfolio = exact_minimum_failure_portfolio()
    gap = survivorship_gap()

    official_case_count = sum(
        case.evidence_class.startswith("official")
        for case in corpus
    )
    quantitative_case_count = sum(
        bool(case.quantitative_anchors)
        for case in corpus
    )

    gates = {
        "contains_multiple_failure_classes": (
            len({case.event_type for case in corpus}) >= 5
        ),
        "contains_official_primary_evidence": official_case_count >= 3,
        "all_cases_have_quantitative_or_timed_anchor": (
            quantitative_case_count == len(corpus)
        ),
        "covers_all_declared_failure_mechanisms": (
            set(portfolio["covered_mechanisms"])
            == set(TARGET_FAILURE_MECHANISMS)
        ),
        "bankruptcy_context_not_mislabeled_saas_only": (
            any(
                case.case_id == "tdb-software-bankruptcy-2025fy"
                and "not a SaaS-only cohort" in case.limitation
                for case in corpus
            )
        ),
        "survivorship_gap_is_nonempty": gap["new_mechanism_count"] >= 8,
    }

    return {
        "experiment": "E028",
        "question": (
            "What failure mechanisms become visible when Japanese withdrawal, "
            "sunset, pivot, pruning, and bankruptcy evidence is admitted "
            "instead of calibrating only from surviving subscription systems?"
        ),
        "corpus": [asdict(case) for case in corpus],
        "exact_failure_portfolio": portfolio,
        "survivorship_gap": gap,
        "promotion_gate": gates,
        "promoted_failure_rule": (
            "negative-evidence-corpus-required-for-market-calibration-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Future market calibration must evaluate candidate mechanisms "
            "against both surviving and failed/withdrawn systems. Exit reasons "
            "are typed mechanisms, not one generic failure label."
        ),
        "limitations": (
            "The corpus is intentionally small and heterogeneous. Some cases "
            "are company postmortems, and the TDB aggregate is broader than SaaS. "
            "E028 establishes an admission/coverage discipline rather than a "
            "population failure rate."
        ),
    }
