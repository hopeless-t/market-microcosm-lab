from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations


SOURCES = ("a", "b", "c", "d")


@dataclass(frozen=True)
class HiddenRootHypothesis:
    hypothesis_id: str
    shared_members: frozenset[str]


@dataclass(frozen=True)
class PairProbe:
    left: str
    right: str
    cost: int

    @property
    def probe_id(self) -> str:
        return f"{self.left}{self.right}"


def hypotheses() -> tuple[HiddenRootHypothesis, ...]:
    rows = [
        HiddenRootHypothesis("none", frozenset())
    ]
    for triple in combinations(SOURCES, 3):
        rows.append(
            HiddenRootHypothesis(
                "shared-" + "".join(triple),
                frozenset(triple),
            )
        )
    return tuple(rows)


def probes() -> tuple[PairProbe, ...]:
    cost = {
        ("a", "b"): 1,
        ("a", "c"): 1,
        ("a", "d"): 2,
        ("b", "c"): 2,
        ("b", "d"): 3,
        ("c", "d"): 3,
    }
    return tuple(
        PairProbe(left, right, cost[(left, right)])
        for left, right in combinations(SOURCES, 2)
    )


def probe_result(
    hypothesis: HiddenRootHypothesis,
    probe: PairProbe,
) -> bool:
    return (
        probe.left in hypothesis.shared_members
        and probe.right in hypothesis.shared_members
    )


def signature(
    hypothesis: HiddenRootHypothesis,
    selected: tuple[PairProbe, ...],
) -> tuple[bool, ...]:
    return tuple(
        probe_result(hypothesis, probe)
        for probe in selected
    )


def distinguishes_all_hypotheses(
    selected: tuple[PairProbe, ...],
) -> bool:
    signatures = [
        signature(hypothesis, selected)
        for hypothesis in hypotheses()
    ]
    return len(set(signatures)) == len(signatures)


def exact_minimum_probe_portfolio() -> dict:
    catalog = probes()
    candidates: list[dict] = []

    for size in range(1, len(catalog) + 1):
        for selected in combinations(catalog, size):
            if not distinguishes_all_hypotheses(selected):
                continue

            total_cost = sum(probe.cost for probe in selected)
            candidates.append(
                {
                    "probe_ids": [
                        probe.probe_id for probe in selected
                    ],
                    "probe_count": len(selected),
                    "total_cost": total_cost,
                    "signatures": {
                        hypothesis.hypothesis_id: list(
                            signature(hypothesis, selected)
                        )
                        for hypothesis in hypotheses()
                    },
                }
            )

    if not candidates:
        raise ValueError("no identifying probe portfolio")

    selected = min(
        candidates,
        key=lambda row: (
            row["total_cost"],
            row["probe_count"],
            row["probe_ids"],
        ),
    )

    return {
        "hypothesis_count": len(hypotheses()),
        "probe_catalog_count": len(catalog),
        "identifying_portfolio_count": len(candidates),
        "selected": selected,
    }


def minimum_probe_portfolio_report_payload() -> dict:
    result = exact_minimum_probe_portfolio()
    selected = result["selected"]

    gates = {
        "portfolio_identifies_none_plus_four_shared_triples": (
            result["hypothesis_count"] == 5
        ),
        "selected_portfolio_uses_three_probes": (
            selected["probe_count"] == 3
        ),
        "selected_portfolio_has_minimum_cost_four": (
            selected["total_cost"] == 4
        ),
        "selected_probe_ids_are_exact_reference": (
            selected["probe_ids"] == ["ab", "ac", "bc"]
        ),
        "all_hypothesis_signatures_are_unique": (
            len(
                {
                    tuple(value)
                    for value in selected["signatures"].values()
                }
            )
            == result["hypothesis_count"]
        ),
        "probe_selection_is_exact_not_greedy_claim": True,
    }

    return {
        "experiment": "E052",
        "question": (
            "What is the minimum-cost bounded probe portfolio that can "
            "distinguish no shared root from each possible three-of-four "
            "hidden-root hypothesis in the reference world?"
        ),
        "reference": result,
        "promotion_gate": gates,
        "promoted_probe_rule": (
            "lineage-discovery-probes-use-exact-minimum-identifying-portfolio-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Active lineage discovery becomes an experiment-design problem. "
            "Probe portfolios are scored by whether their response signatures "
            "separate all admissible dependency hypotheses, then by total "
            "declared intervention cost."
        ),
        "limitations": (
            "The hypothesis family is small and finite, probe outcomes are "
            "binary, and costs are synthetic. Larger graphs require bounded "
            "search, adaptive testing, and noisy information-gain methods."
        ),
    }
