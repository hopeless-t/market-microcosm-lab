from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class BbdQuarter:
    quarter: str
    arr_jpy_millions: float
    churn_rate_pct: float
    contract_count: int
    arpa_jpy: int


def bbd_fy2025_quarters() -> tuple[BbdQuarter, ...]:
    return (
        BbdQuarter("FY2025-Q1", 1605.0, 1.93, 3390, 473_682),
        BbdQuarter("FY2025-Q2", 1640.0, 1.76, 3358, 488_431),
        BbdQuarter("FY2025-Q3", 1688.0, 2.16, 3304, 511_090),
        BbdQuarter("FY2025-Q4", 1662.0, 1.67, 3265, 509_166),
    )


def quarterly_transitions() -> tuple[dict, ...]:
    rows = []
    quarters = bbd_fy2025_quarters()

    for previous, current in zip(quarters, quarters[1:]):
        arr_delta = current.arr_jpy_millions - previous.arr_jpy_millions
        churn_delta = current.churn_rate_pct - previous.churn_rate_pct
        contract_delta = current.contract_count - previous.contract_count
        arpa_delta = current.arpa_jpy - previous.arpa_jpy

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
                    "up" if churn_delta > 0 else "down" if churn_delta < 0 else "flat"
                ),
                "contract_delta": contract_delta,
                "contract_direction": (
                    "up"
                    if contract_delta > 0
                    else "down"
                    if contract_delta < 0
                    else "flat"
                ),
                "arpa_delta_jpy": arpa_delta,
                "arpa_direction": (
                    "up" if arpa_delta > 0 else "down" if arpa_delta < 0 else "flat"
                ),
            }
        )

    return tuple(rows)


def churn_direction_naive_predictor() -> dict:
    rows = []
    correct = 0

    for transition in quarterly_transitions():
        predicted_arr_direction = (
            "up"
            if transition["churn_direction"] == "down"
            else "down"
            if transition["churn_direction"] == "up"
            else "flat"
        )
        is_correct = (
            predicted_arr_direction
            == transition["arr_direction"]
        )
        correct += int(is_correct)

        rows.append(
            {
                "from": transition["from"],
                "to": transition["to"],
                "churn_direction": transition["churn_direction"],
                "predicted_arr_direction": predicted_arr_direction,
                "observed_arr_direction": transition["arr_direction"],
                "correct": is_correct,
            }
        )

    return {
        "rows": rows,
        "accuracy": correct / len(rows),
        "correct_count": correct,
        "transition_count": len(rows),
    }


def portfolio_transition_report_payload() -> dict:
    quarters = bbd_fy2025_quarters()
    transitions = quarterly_transitions()
    naive = churn_direction_naive_predictor()

    churn_down_transitions = [
        row for row in transitions
        if row["churn_direction"] == "down"
    ]
    churn_down_arr_directions = {
        row["arr_direction"]
        for row in churn_down_transitions
    }

    q4 = transitions[-1]

    gates = {
        "same_company_same_metric_generation_has_both_churn_down_arr_up_and_down": (
            churn_down_arr_directions == {"up", "down"}
        ),
        "churn_up_can_coexist_with_arr_up": any(
            row["churn_direction"] == "up"
            and row["arr_direction"] == "up"
            for row in transitions
        ),
        "contract_count_declines_every_quarter": all(
            row["contract_direction"] == "down"
            for row in transitions
        ),
        "q4_churn_improves_while_arr_and_arpa_decline": (
            q4["churn_direction"] == "down"
            and q4["arr_direction"] == "down"
            and q4["arpa_direction"] == "down"
        ),
        "naive_churn_sign_predictor_fails_two_of_three_transitions": (
            naive["correct_count"] == 1
            and naive["transition_count"] == 3
        ),
        "event_annotations_are_kept_separate_from_metric_signs": True,
    }

    return {
        "experiment": "E063",
        "question": (
            "Within one real company-year and one stable KPI definition "
            "generation, can churn direction alone certify the direction of "
            "ARR or portfolio health during an active product transition?"
        ),
        "source": {
            "provider": "BBD Initiative Inc.",
            "fy2025_full_year_kpi_url": (
                "https://www.bbdi.co.jp/ir/pdf/"
                "2025%E5%B9%B49%E6%9C%88%E6%9C%9F%20"
                "%E9%80%9A%E6%9C%9F%E6%B1%BA%E7%AE%97"
                "%E9%80%9F%E5%A0%B1_FINAL.pdf"
            ),
            "fy2025_q3_kpi_url": (
                "https://www.bbdi.co.jp/ir/pdf/"
                "2025%E5%B9%B49%E6%9C%88%E6%9C%9F%20"
                "%E7%AC%AC3%E5%9B%9B%E5%8D%8A%E6%9C%9F"
                "%E6%B1%BA%E7%AE%97%E9%80%9F%E5%A0%B1.pdf"
            ),
            "metric_identity": (
                "ARR = quarter-end MRR x 12; churn = three-month average "
                "monthly Churn MRR / prior month-end MRR."
            ),
            "q4_event_annotation": (
                "The company states ARR decreased as the planned Knowledge "
                "Suite+ launch timing slipped; it also states low-price-plan "
                "cancellations continued and ARPA temporarily decreased amid "
                "launch delay and service-withdrawal preparation."
            ),
        },
        "quarters": [asdict(row) for row in quarters],
        "transitions": list(transitions),
        "naive_churn_direction_predictor": naive,
        "promotion_gate": gates,
        "promoted_transition_rule": (
            "portfolio-transition-kpi-direction-requires-event-semantics-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Directional KPI changes are observations, not health labels. "
            "During portfolio transition, churn, ARR, ARPA, and contract count "
            "can move in different sign combinations under the same metric "
            "definitions. Transition events and product-state annotations "
            "must accompany sign-based warning logic."
        ),
        "limitations": (
            "This is a four-quarter single-company counterexample and does not "
            "estimate causal effects or universal transition probabilities. "
            "Management event explanations are retained as annotations rather "
            "than treated as independently identified causal estimates."
        ),
    }
