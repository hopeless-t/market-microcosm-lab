from market_microcosm.adaptive_sampling import (
    first_frontier,
    monotonicity_violations,
    staircase_inference,
)


def test_staircase_recovers_monotone_surface() -> None:
    max_level = 3
    thresholds = {0: 4, 1: 3, 2: 2, 3: 1}
    surface = {
        (a, b): b >= thresholds[a]
        for a in range(max_level + 1)
        for b in range(max_level + 1)
    }
    queried, recovered, inferred = staircase_inference(
        surface,
        max_level=max_level,
    )
    assert recovered == thresholds
    assert inferred == surface
    assert len(queried) <= 2 * max_level + 1


def test_monotonicity_violation_is_detected() -> None:
    surface = {
        (0, 0): False,
        (0, 1): True,
        (1, 0): False,
        (1, 1): False,
    }
    violations = monotonicity_violations(surface, max_level=1)
    assert violations


def test_frontier_uses_e014_ordering() -> None:
    surface = {
        (0, 0): False,
        (0, 1): False,
        (0, 2): True,
        (1, 0): False,
        (1, 1): True,
        (1, 2): True,
        (2, 0): True,
        (2, 1): True,
        (2, 2): True,
    }
    assert first_frontier(surface) == (1, 1)
