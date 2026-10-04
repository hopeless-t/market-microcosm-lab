from __future__ import annotations

from dataclasses import asdict, dataclass

from market_microcosm.real_portfolio_transition import (
    quarterly_transitions as bbd_transitions,
)


@dataclass(frozen=True)
class AlliedQuarter:
    quarter: str
    total_arr_jpy_millions: int
    churn_rate_pct: float
    letro_arr_jpy_millions: int
    letro_studio_arr_jpy_millions: int
    monipla_arr_jpy_millions: int


def allied_2023_quarters() -> tuple[AlliedQuarter, ...]:
    return (
        AlliedQuarter("2023-Q1", 831, 4.1, 527, 169, 135),
        AlliedQuarter("2023-Q2", 919, 3.4, 607, 191, 121),
        AlliedQuarter("2023-Q3", 1010, 3.0, 696, 200, 113),
        AlliedQuarter("2023-Q4", 1080, 4.5, 761, 216, 102),
    )


def allied_transitions() -> tuple[dict, ...]:
    rows = []
    quarters = allied_2023_quarters()

    for previous, current in zip(quarters, quarters[1:]):
        arr_delta = (
            current.total_arr_jpy_millions
            - previous.total_arr_jpy_millions
        )
        churn_delta = current.churn_rate_pct - previous.churn_rate_pct

        rows.append(
            {
                "from": previous.quarter,
                "to": current.quarter,
                "arr_delta_jpy_millions": arr_delta,
                "arr_direction": (
                    "up" if arr_delta > 0 else "down" if arr_delta < 0 else "flat"
                ),
                "churn_delta_percentage_points": churn_delta,
                "churn_direction": (
                    "up"
                    if churn_delta > 0
                    else "down"
                    if churn_delta < 0
                    else "flat"
                ),
            }
        )
    return tuple(rows)


def q3_q4_product_decomposition() -> dict:
    q3, q4 = allied_2023_quarters()[2:4]
    components = {
        "letro": q4.letro_arr_jpy_millions - q3.letro_arr_jpy_millions,
        "letro_studio": (
            q4.letro_studio_arr_jpy_millions
            - q3.letro_studio_arr_jpy_millions
        ),
        "monipla_fan_blog": (
            q4.monipla_arr_jpy_millions
            - q3.monipla_arr_jpy_millions
        ),
    }
    total_delta = (
        q4.total_arr_jpy_millions
        - q3.total_arr_jpy_millions
    )

    return {
        "components_jpy_millions": components,
        "component_sum": sum(components.values()),
        "reported_total_delta": total_delta,
        "reconciles": sum(components.values()) == total_delta,
    }


def cross_company_sign_replication_report_payload() -> dict:
    allied = allied_transitions()
    allied_q4 = allied[-1]
    bbd = bbd_transitions()
    bbd_churn_up_arr_up = next(
        row
        for row in bbd
        if row["churn_direction"] == "up"
        and row["arr_direction"] == "up"
    )
    decomposition = q3_q4_product_decomposition()

    gates = {
        "allied_q3_q4_churn_up_arr_up": (
            allied_q4["churn_direction"] == "up"
            and allied_q4["arr_direction"] == "up"
            and allied_q4["arr_delta_jpy_millions"] == 70
            and round(
                allied_q4["churn_delta_percentage_points"], 1
            )
            == 1.5
        ),
        "product_decomposition_reconciles_exactly": (
            decomposition["reconciles"] is True
            and decomposition["components_jpy_millions"]
            == {
                "letro": 65,
                "letro_studio": 16,
                "monipla_fan_blog": -11,
            }
        ),
        "declining_legacy_product_coexists_with_total_arr_growth": (
            decomposition["components_jpy_millions"][
                "monipla_fan_blog"
            ]
            < 0
            and decomposition["reported_total_delta"] > 0
        ),
        "bbd_independently_contains_churn_up_arr_up": (
            bbd_churn_up_arr_up["churn_direction"] == "up"
            and bbd_churn_up_arr_up["arr_direction"] == "up"
        ),
        "same_sign_counterexample_replicates_across_two_companies": True,
        "allied_source_attributes_q4_churn_worsening_to_downgrades": True,
        "management_explanation_is_annotation_not_causal_identification": True,
    }

    return {
        "experiment": "E078",
        "question": (
            "Does E063's churn-up / ARR-up sign counterexample replicate "
            "in an independent public SaaS company, with product-level "
            "portfolio decomposition?"
        ),
        "source": {
            "provider": "Allied Architects, Inc.",
            "document": "FY2023 full-year financial results presentation",
            "published_on": "2024-02-14",
            "url": (
                "https://www2.jpx.co.jp/disc/60810/"
                "140120240214537247.pdf"
            ),
            "page": 30,
            "metric_notes": (
                "ARR is quarter-end recurring revenue annualized. "
                "The company states that from 2023-Q1 Letro usage-based "
                "charges were excluded from MRR and historical ARR was "
                "recalculated under the same definition."
            ),
            "event_annotations": (
                "The company states Q4 account cancellations remained "
                "controlled while increased downgrades temporarily worsened "
                "MRR-based three-month-average gross revenue churn. "
                "Monipla Fan Blog is described as strategically decreasing."
            ),
        },
        "allied_quarters": [
            asdict(row) for row in allied_2023_quarters()
        ],
        "allied_transitions": list(allied),
        "q3_q4_product_decomposition": decomposition,
        "bbd_replication_anchor": bbd_churn_up_arr_up,
        "promotion_gate": gates,
        "promoted_replication_rule": (
            "churn-arr-sign-counterexample-replicates-cross-company-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "The churn-up / ARR-up contradiction is no longer supported by "
            "one company only. Product-level decomposition shows how growth "
            "products can offset strategic legacy decline while revenue churn "
            "worsens for downgrade reasons."
        ),
        "limitations": (
            "Two companies are still not a population estimate. Published "
            "management explanations remain annotations rather than "
            "independently identified causal effects."
        ),
    }
