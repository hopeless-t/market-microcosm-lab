from __future__ import annotations


def delivery_margin_candidates() -> tuple[dict, ...]:
    candidates = (
        {
            "name": "human_heavy_high_acv",
            "revenue": 100.0,
            "software_infra_cost": 20.0,
            "human_delivery_cost": 70.0,
        },
        {
            "name": "product_led_lower_acv",
            "revenue": 80.0,
            "software_infra_cost": 20.0,
            "human_delivery_cost": 10.0,
        },
    )

    rows = []
    for row in candidates:
        apparent_gross_margin = (
            row["revenue"] - row["software_infra_cost"]
        ) / row["revenue"]
        fully_loaded_gross_margin = (
            row["revenue"]
            - row["software_infra_cost"]
            - row["human_delivery_cost"]
        ) / row["revenue"]
        rows.append(
            {
                **row,
                "apparent_gross_margin": apparent_gross_margin,
                "fully_loaded_gross_margin": fully_loaded_gross_margin,
                "human_delivery_share_of_revenue": (
                    row["human_delivery_cost"] / row["revenue"]
                ),
            }
        )

    return tuple(rows)


def delivery_cost_ranking_reversal() -> dict:
    rows = delivery_margin_candidates()
    apparent = max(
        rows,
        key=lambda row: row["apparent_gross_margin"],
    )
    fully_loaded = max(
        rows,
        key=lambda row: row["fully_loaded_gross_margin"],
    )

    return {
        "candidates": list(rows),
        "apparent_margin_winner": apparent["name"],
        "fully_loaded_margin_winner": fully_loaded["name"],
        "ranking_reversal": apparent["name"] != fully_loaded["name"],
    }


def human_delivery_cost_report_payload() -> dict:
    reversal = delivery_cost_ranking_reversal()
    heavy = next(
        row
        for row in reversal["candidates"]
        if row["name"] == "human_heavy_high_acv"
    )

    gates = {
        "high_acv_can_hide_high_human_delivery_share": (
            heavy["human_delivery_share_of_revenue"] >= 0.70
        ),
        "apparent_margin_looks_healthy": (
            heavy["apparent_gross_margin"] >= 0.75
        ),
        "fully_loaded_margin_collapses": (
            heavy["fully_loaded_gross_margin"] <= 0.10
        ),
        "margin_ranking_reverses_after_human_cost": (
            reversal["ranking_reversal"] is True
        ),
        "human_delivery_burden_is_not_free": True,
        "product_and_service_value_delivery_are_separate_state": True,
    }

    return {
        "experiment": "E034",
        "question": (
            "Can high ACV and apparently strong software gross margin hide "
            "a non-scalable human-delivery burden that reverses the preferred "
            "product ranking once fully loaded cost is included?"
        ),
        "empirical_anchor": {
            "source": "Srush founder postmortem",
            "observation": (
                "The founder explicitly describes a false-PMF signal as "
                "high unit price combined with substantial human work, and "
                "notes that people were solving customer problems instead "
                "of the product."
            ),
            "source_url": "https://note.com/srushhiguchi/n/n6dc615317659",
        },
        "finite_cost_witness": reversal,
        "promotion_gate": gates,
        "promoted_delivery_rule": (
            "fully-loaded-human-delivery-cost-required-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Future empirical SaaS worlds must distinguish product-delivered "
            "value from recurring human delivery/implementation/CS burden. "
            "ACV and software-only gross margin cannot certify scalability."
        ),
        "limitations": (
            "The cost values are synthetic structural witnesses. Srush's "
            "postmortem motivates the hidden-cost mechanism but does not "
            "publish the actual fully loaded service cost per account."
        ),
    }
