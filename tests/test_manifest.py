from market_microcosm.manifests import RunManifest


def test_manifest_identity_is_deterministic_and_sensitive() -> None:
    a = RunManifest(
        generation=1,
        world_version="toy-v1",
        observer_version="full-v1",
        policy_name="p",
        verifier_version="v1",
        scenario_ids=("a", "b"),
    )
    b = RunManifest(
        generation=1,
        world_version="toy-v1",
        observer_version="full-v1",
        policy_name="p",
        verifier_version="v1",
        scenario_ids=("a", "b"),
    )
    c = RunManifest(
        generation=1,
        world_version="toy-v1",
        observer_version="full-v1",
        policy_name="p2",
        verifier_version="v1",
        scenario_ids=("a", "b"),
    )
    assert a.run_id == b.run_id
    assert a.run_id != c.run_id
