from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path

from .adaptive_sampling import (
    failure_surface,
    monotonicity_violations,
    staircase_inference,
)


CERTIFIED_SOURCE_PATHS = (
    "spec/ROOT_OF_TRUST.md",
    "src/market_microcosm/ecology.py",
    "src/market_microcosm/ecological_evaluation.py",
    "src/market_microcosm/sensitivity.py",
    "src/market_microcosm/interactions.py",
    "src/market_microcosm/adaptive_sampling.py",
    "src/market_microcosm/adaptive_guard.py",
    "scripts/run_e014.py",
    "scripts/run_e015.py",
    "scripts/run_e016.py",
)


@dataclass(frozen=True)
class AdaptiveCertificate:
    generation_fingerprint: str
    source_report_digest: str
    source_experiment: str
    issued_by: str
    contract: dict


@dataclass(frozen=True)
class AdversarialProbe:
    pair_key: str
    mechanism_name: str
    mutated_point: tuple[int, int]
    original_failed: bool
    mutated_failed: bool
    monotonicity_violation_count: int
    naive_classification_accuracy: float
    naive_frontier_exact: bool
    naive_queried_points: int
    total_points: int


def canonical_digest(value: object) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def generation_fingerprint(
    root: Path,
    *,
    contract: dict,
    source_paths: tuple[str, ...] = CERTIFIED_SOURCE_PATHS,
) -> str:
    payload = {
        "contract": contract,
        "files": {
            relative: file_digest(root / relative)
            for relative in source_paths
        },
    }
    return canonical_digest(payload)


def source_report_digest(report: dict) -> str:
    return canonical_digest(report)


def default_certification_contract(report: dict) -> dict:
    return {
        "source_experiment": str(report["experiment"]),
        "grid_max_level": int(report["grid_max_level"]),
        "pairs": report["pairs"],
        "survival_threshold": 0.90,
        "horizon": 60,
        "evaluation_seed_start": 15000,
        "evaluation_seed_stop_exclusive": 15012,
        "biopsy_seed_start": 16000,
        "biopsy_seed_stop_exclusive": 16040,
    }


def issue_certificate(
    root: Path,
    *,
    report: dict,
    contract: dict | None = None,
) -> AdaptiveCertificate:
    contract = contract or default_certification_contract(report)
    return AdaptiveCertificate(
        generation_fingerprint=generation_fingerprint(
            root,
            contract=contract,
        ),
        source_report_digest=source_report_digest(report),
        source_experiment=str(report["experiment"]),
        issued_by="E014-exhaustive-audit",
        contract=contract,
    )


def guarded_mode(
    certificate: AdaptiveCertificate | None,
    *,
    current_generation_fingerprint: str,
) -> str:
    if certificate is None:
        return "exhaustive"
    if certificate.generation_fingerprint != current_generation_fingerprint:
        return "exhaustive"
    return "adaptive"


def _first_frontier(surface: dict[tuple[int, int], bool]) -> tuple[int, int] | None:
    failing = [point for point, failed in surface.items() if failed]
    if not failing:
        return None
    return min(
        failing,
        key=lambda point: (
            point[0] + point[1],
            max(point),
            abs(point[0] - point[1]),
            point[0],
            point[1],
        ),
    )


def inject_hidden_nonmonotone_island(
    surface: dict[tuple[int, int], bool],
    *,
    max_level: int,
) -> tuple[dict[tuple[int, int], bool], tuple[int, int]]:
    queried, _, _ = staircase_inference(surface, max_level=max_level)
    queried_set = set(queried)

    candidates = sorted(
        (
            point
            for point, failed in surface.items()
            if failed and point not in queried_set
        ),
        key=lambda point: (
            -(point[0] + point[1]),
            -max(point),
            point[0],
            point[1],
        ),
    )

    for candidate in candidates:
        mutated = dict(surface)
        mutated[candidate] = False
        violations = monotonicity_violations(mutated, max_level=max_level)
        mutated_queries, _, inferred = staircase_inference(
            mutated,
            max_level=max_level,
        )
        accuracy = sum(
            inferred[point] == failed
            for point, failed in mutated.items()
        ) / len(mutated)
        if (
            violations
            and candidate not in set(mutated_queries)
            and accuracy < 1.0
        ):
            return mutated, candidate

    raise ValueError("could not construct hidden non-monotone island")


def adversarial_probe(
    report: dict,
    *,
    pair_key: str,
    mechanism_name: str,
) -> AdversarialProbe:
    max_level = int(report["grid_max_level"])
    original = failure_surface(
        report,
        pair_key=pair_key,
        mechanism_name=mechanism_name,
    )
    mutated, point = inject_hidden_nonmonotone_island(
        original,
        max_level=max_level,
    )
    queried, _, inferred = staircase_inference(
        mutated,
        max_level=max_level,
    )
    violations = monotonicity_violations(
        mutated,
        max_level=max_level,
    )
    accuracy = sum(
        inferred[p] == failed
        for p, failed in mutated.items()
    ) / len(mutated)

    return AdversarialProbe(
        pair_key=pair_key,
        mechanism_name=mechanism_name,
        mutated_point=point,
        original_failed=original[point],
        mutated_failed=mutated[point],
        monotonicity_violation_count=len(violations),
        naive_classification_accuracy=accuracy,
        naive_frontier_exact=(
            _first_frontier(mutated) == _first_frontier(inferred)
        ),
        naive_queried_points=len(queried),
        total_points=len(mutated),
    )


def guard_report_payload(
    root: Path,
    *,
    e014_report: dict,
    e015_report: dict,
) -> dict:
    certificate = issue_certificate(root, report=e014_report)
    current_fingerprint = generation_fingerprint(
        root,
        contract=certificate.contract,
    )
    same_generation_mode = guarded_mode(
        certificate,
        current_generation_fingerprint=current_fingerprint,
    )

    mutated_contract = dict(certificate.contract)
    mutated_contract["horizon"] = int(mutated_contract["horizon"]) + 1
    changed_generation_fingerprint = generation_fingerprint(
        root,
        contract=mutated_contract,
    )
    changed_generation_mode = guarded_mode(
        certificate,
        current_generation_fingerprint=changed_generation_fingerprint,
    )

    pair_key = "subscription_price_multiplier__platform_cost_multiplier"
    mechanism_name = "creator-heavy"
    probe = adversarial_probe(
        e014_report,
        pair_key=pair_key,
        mechanism_name=mechanism_name,
    )

    revoked_mode = "exhaustive" if probe.monotonicity_violation_count > 0 else "adaptive"

    gates = {
        "e015_was_promoted": bool(e015_report["promoted"]),
        "same_generation_allows_adaptive": same_generation_mode == "adaptive",
        "generation_change_falls_back_to_exhaustive": (
            changed_generation_mode == "exhaustive"
        ),
        "adversarial_nonmonotonicity_detected_by_exhaustive_audit": (
            probe.monotonicity_violation_count > 0
        ),
        "naive_adaptive_is_imperfect_on_adversarial_surface": (
            probe.naive_classification_accuracy < 1.0
        ),
        "audit_revokes_adaptive_path": revoked_mode == "exhaustive",
    }

    return {
        "experiment": "E016",
        "source_experiments": ["E014", "E015"],
        "certificate": asdict(certificate),
        "same_generation": {
            "fingerprint": current_fingerprint,
            "mode": same_generation_mode,
        },
        "changed_generation": {
            "fingerprint": changed_generation_fingerprint,
            "mutated_contract": mutated_contract,
            "mode": changed_generation_mode,
        },
        "adversarial_probe": asdict(probe),
        "post_audit_mode": revoked_mode,
        "promotion_gate": gates,
        "guard_contract_passed": all(gates.values()),
        "limitation": (
            "Sparse adaptive queries cannot prove global monotonicity. "
            "The certificate is generation-scoped and exhaustive audit remains authoritative."
        ),
    }
