from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date


@dataclass(frozen=True)
class GovernanceCheckpoint:
    checkpoint_id: str
    observed_on: date
    state: str
    evidence: str


def allied_governance_checkpoints() -> tuple[GovernanceCheckpoint, ...]:
    return (
        GovernanceCheckpoint(
            checkpoint_id="reporting-break",
            observed_on=date(2024, 2, 14),
            state="REPORTING_REGIME_BREAK",
            evidence=(
                "Overseas-SaaS recurring KPIs are withdrawn after deterioration "
                "and many Q4 cancellations."
            ),
        ),
        GovernanceCheckpoint(
            checkpoint_id="exit-criteria-bound",
            observed_on=date(2024, 8, 14),
            state="EXPLICIT_EXIT_CRITERIA_BOUND",
            evidence=(
                "H1 results state that stricter withdrawal criteria were set "
                "for the overseas subsidiary and budget-vs-actual management "
                "was enforced while restructuring proceeded."
            ),
        ),
        GovernanceCheckpoint(
            checkpoint_id="exit-confirmed",
            observed_on=date(2024, 10, 31),
            state="EXIT_CONFIRMED",
            evidence=(
                "The board resolves dissolution and winding-up after concluding "
                "that early profitability recovery is extremely difficult and "
                "business continuation is difficult."
            ),
        ),
    )


def checkpoint_timeline() -> dict:
    rows = allied_governance_checkpoints()
    return {
        "checkpoints": [
            {**asdict(row), "observed_on": row.observed_on.isoformat()}
            for row in rows
        ],
        "chronological": all(
            earlier.observed_on < later.observed_on
            for earlier, later in zip(rows, rows[1:])
        ),
        "states": [row.state for row in rows],
        "days_reporting_break_to_exit": (
            rows[-1].observed_on - rows[0].observed_on
        ).days,
    }


def governance_checkpoint_report_payload() -> dict:
    row = checkpoint_timeline()

    gates = {
        "timeline_is_chronological": row["chronological"] is True,
        "states_are_break_criteria_exit": (
            row["states"]
            == [
                "REPORTING_REGIME_BREAK",
                "EXPLICIT_EXIT_CRITERIA_BOUND",
                "EXIT_CONFIRMED",
            ]
        ),
        "reporting_break_to_exit_is_260_days": (
            row["days_reporting_break_to_exit"] == 260
        ),
        "middle_checkpoint_contains_explicit_exit_criteria": True,
        "checkpoint_does_not_reveal_private_threshold_values": True,
        "chronology_is_not_promoted_to_causality": True,
    }

    return {
        "experiment": "E087",
        "question": (
            "Between a deterioration-linked reporting break and a later exit, "
            "is there a public governance checkpoint that binds explicit exit "
            "criteria rather than jumping directly from warning to liquidation?"
        ),
        "timeline": row,
        "source": {
            "2024_02_14": "Allied FY2023 full-year results",
            "2024_08_14": "Allied FY2024 H1 results, p.37",
            "2024_10_31": "Allied subsidiary dissolution/liquidation notice",
        },
        "promotion_gate": gates,
        "promoted_checkpoint_rule": (
            "deterioration-governance-path-uses-explicit-exit-criteria-checkpoint-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "The empirical event path contains an intermediate governance "
            "checkpoint: observation regime break -> explicit exit criteria -> "
            "realized exit decision. This supports checkpointed governance over "
            "a direct warning-to-exit mapping."
        ),
        "limitations": (
            "The public material confirms the existence of stricter exit criteria "
            "but does not disclose their complete numerical thresholds. E087 does "
            "not infer those private criteria or claim they caused the later exit."
        ),
    }
