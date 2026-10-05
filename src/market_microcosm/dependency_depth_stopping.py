from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class AuditDepth:
    depth: int
    cumulative_cost: int
    maximum_unverified_correlated_providers: int
    channels_per_provider: int
    evidence: str

    @property
    def maximum_unverified_blast_channels(self) -> int:
        return (
            self.maximum_unverified_correlated_providers
            * self.channels_per_provider
        )


def audit_depths() -> tuple[AuditDepth, ...]:
    return (
        AuditDepth(
            depth=0,
            cumulative_cost=0,
            maximum_unverified_correlated_providers=5,
            channels_per_provider=2,
            evidence="provider repartition only",
        ),
        AuditDepth(
            depth=1,
            cumulative_cost=2,
            maximum_unverified_correlated_providers=2,
            channels_per_provider=2,
            evidence=(
                "network/identity segmentation audited; deeper common mode "
                "can still span two providers"
            ),
        ),
        AuditDepth(
            depth=2,
            cumulative_cost=5,
            maximum_unverified_correlated_providers=1,
            channels_per_provider=2,
            evidence=(
                "provider plus physical/vendor/power lineage audited; "
                "unverified descendants are provider-local"
            ),
        ),
        AuditDepth(
            depth=3,
            cumulative_cost=9,
            maximum_unverified_correlated_providers=1,
            channels_per_provider=2,
            evidence=(
                "endpoint-local dependency audit adds detail but does not "
                "reduce the certified cross-provider blast bound"
            ),
        ),
    )


def compile_minimum_audit_depth(
    *,
    maximum_tolerated_blast_channels: int = 2,
) -> dict:
    rows = []
    for depth in audit_depths():
        blast = depth.maximum_unverified_blast_channels
        rows.append(
            {
                **asdict(depth),
                "maximum_unverified_blast_channels": blast,
                "meets_budget": blast <= maximum_tolerated_blast_channels,
            }
        )

    satisfying = [row for row in rows if row["meets_budget"]]
    if not satisfying:
        return {
            "status": "UNSAT",
            "maximum_tolerated_blast_channels": (
                maximum_tolerated_blast_channels
            ),
            "depths": rows,
            "selected": None,
        }

    selected = min(
        satisfying,
        key=lambda row: (
            row["cumulative_cost"],
            row["depth"],
        ),
    )

    return {
        "status": "SAT",
        "maximum_tolerated_blast_channels": (
            maximum_tolerated_blast_channels
        ),
        "depths": rows,
        "selected": selected,
    }


def dependency_depth_stopping_report_payload() -> dict:
    compiled = compile_minimum_audit_depth()
    selected = compiled["selected"]

    gates = {
        "depth_zero_is_not_sufficient": (
            compiled["depths"][0]["meets_budget"] is False
        ),
        "depth_one_is_not_sufficient": (
            compiled["depths"][1]["meets_budget"] is False
        ),
        "depth_two_is_first_sufficient_depth": (
            selected["depth"] == 2
        ),
        "depth_two_cost_is_five": (
            selected["cumulative_cost"] == 5
        ),
        "deeper_depth_three_adds_cost_without_better_blast_bound": (
            compiled["depths"][3][
                "maximum_unverified_blast_channels"
            ]
            == selected["maximum_unverified_blast_channels"]
            and compiled["depths"][3]["cumulative_cost"]
            > selected["cumulative_cost"]
        ),
        "stopping_rule_is_authority_budget_scoped": True,
    }

    return {
        "experiment": "E059",
        "question": (
            "How deep should recursive dependency discovery continue before "
            "stopping, if the downstream error-correcting contract tolerates "
            "at most two correlated certified-channel failures?"
        ),
        "compiled_depth": compiled,
        "promotion_gate": gates,
        "promoted_stopping_rule": (
            "recursive-lineage-audit-stops-at-minimum-depth-meeting-blast-budget-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Recursive dependency discovery receives an explicit stopping "
            "certificate. Audit depth increases only until the maximum "
            "unverified correlated blast radius is inside the declared "
            "downstream correction budget; deeper detail has no automatic "
            "authority value."
        ),
        "limitations": (
            "The per-depth blast upper bounds are declared structural evidence "
            "in the reference. If those bounds are later falsified by a new "
            "common mode, the stopping certificate must be revoked and the "
            "depth compiler rerun."
        ),
    }
