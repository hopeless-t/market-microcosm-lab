from market_microcosm.witness_quorum import (
    detect_equivocation,
    quorum_intersection_report,
    sign,
    verify_quorum,
    witness_quorum_report_payload,
    witness_registry,
)


def test_three_of_five_intersects_but_two_of_five_does_not() -> None:
    strong = quorum_intersection_report(5, 3)
    weak = quorum_intersection_report(5, 2)

    assert strong["minimum_intersection"] >= 1
    assert strong["disjoint_quorum_pairs"] == 0
    assert weak["disjoint_quorum_pairs"] > 0


def test_compromise_threshold_is_three() -> None:
    witnesses = witness_registry(5)
    sequence = 3
    forged_hash = "f" * 64

    for count in (1, 2):
        attestations = tuple(
            sign(
                witnesses[index],
                sequence=sequence,
                checkpoint_hash=forged_hash,
            )
            for index in range(count)
        )
        result = verify_quorum(
            attestations,
            sequence=sequence,
            checkpoint_hash=forged_hash,
            witnesses=witnesses,
            threshold=3,
        )
        assert result.valid is False

    attestations = tuple(
        sign(
            witnesses[index],
            sequence=sequence,
            checkpoint_hash=forged_hash,
        )
        for index in range(3)
    )
    assert verify_quorum(
        attestations,
        sequence=sequence,
        checkpoint_hash=forged_hash,
        witnesses=witnesses,
        threshold=3,
    ).valid is True


def test_conflicting_quorums_leave_equivocation_evidence() -> None:
    witnesses = witness_registry(5)
    sequence = 3
    hash_a = "a" * 64
    hash_b = "b" * 64

    view_a = tuple(
        sign(
            witnesses[index],
            sequence=sequence,
            checkpoint_hash=hash_a,
        )
        for index in (0, 1, 2)
    )
    view_b = tuple(
        sign(
            witnesses[index],
            sequence=sequence,
            checkpoint_hash=hash_b,
        )
        for index in (2, 3, 4)
    )

    evidence = detect_equivocation(view_a + view_b)
    assert "witness-2@3" in evidence


def test_e021_promotion_contract() -> None:
    payload = witness_quorum_report_payload(
        generation_a="g1",
        generation_b="g2",
    )
    assert (
        payload["promoted_witness_contract"]
        == "three-of-five-witness-quorum-with-equivocation-detection-v1"
    )
    assert all(payload["promotion_gate"].values())
