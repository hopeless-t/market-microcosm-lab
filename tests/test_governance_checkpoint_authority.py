from market_microcosm.governance_checkpoint_authority import (
    exact_minimum_checkpoint_set,
    governance_checkpoint_authority_report_payload,
)


def test_predicate_specific_minimum_checkpoint_sets() -> None:
    assert exact_minimum_checkpoint_set("REVIEW_REQUIRED")["selected"][
        "checkpoints"
    ] == ["reporting-break"]
    assert exact_minimum_checkpoint_set("EXIT_CRITERIA_EXIST")["selected"][
        "checkpoints"
    ] == ["exit-criteria-bound"]
    assert exact_minimum_checkpoint_set("EXIT_CONFIRMED")["selected"][
        "checkpoints"
    ] == ["exit-confirmed"]


def test_full_path_requires_all_three_checkpoints() -> None:
    row = exact_minimum_checkpoint_set("CHECKPOINTED_GOVERNANCE_PATH")[
        "selected"
    ]
    assert row["count"] == 3
    assert row["cost"] == 3


def test_e089_promotion_contract() -> None:
    payload = governance_checkpoint_authority_report_payload()
    assert all(payload["promotion_gate"].values())
    assert payload["promoted_checkpoint_authority_rule"] == (
        "governance-checkpoints-carry-predicate-specific-minimum-authority-v1"
    )
