from pathlib import Path

from market_microcosm.adaptive_guard import (
    AdaptiveCertificate,
    canonical_digest,
    generation_fingerprint,
    guarded_mode,
    inject_hidden_nonmonotone_island,
)
from market_microcosm.adaptive_sampling import (
    monotonicity_violations,
    staircase_inference,
)


def test_generation_fingerprint_changes_with_contract(tmp_path: Path) -> None:
    (tmp_path / "x.txt").write_text("same")
    first = generation_fingerprint(
        tmp_path,
        contract={"horizon": 60},
        source_paths=("x.txt",),
    )
    second = generation_fingerprint(
        tmp_path,
        contract={"horizon": 61},
        source_paths=("x.txt",),
    )
    assert first != second


def test_guard_fails_closed_on_generation_mismatch() -> None:
    certificate = AdaptiveCertificate(
        generation_fingerprint="abc",
        source_report_digest=canonical_digest({"x": 1}),
        source_experiment="E014",
        issued_by="test",
        contract={"horizon": 60},
    )
    assert guarded_mode(
        certificate,
        current_generation_fingerprint="abc",
    ) == "adaptive"
    assert guarded_mode(
        certificate,
        current_generation_fingerprint="def",
    ) == "exhaustive"
    assert guarded_mode(
        None,
        current_generation_fingerprint="abc",
    ) == "exhaustive"


def test_hidden_nonmonotone_island_breaks_naive_inference() -> None:
    max_level = 4
    surface = {
        (a, b): a + b >= 5
        for a in range(max_level + 1)
        for b in range(max_level + 1)
    }
    assert not monotonicity_violations(surface, max_level=max_level)

    mutated, point = inject_hidden_nonmonotone_island(
        surface,
        max_level=max_level,
    )
    violations = monotonicity_violations(mutated, max_level=max_level)
    queried, _, inferred = staircase_inference(
        mutated,
        max_level=max_level,
    )

    assert point not in set(queried)
    assert violations
    assert inferred != mutated
