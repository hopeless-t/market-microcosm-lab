from market_microcosm.recursive_measurement_lineage import (
    recursive_measurement_lineage_report_payload,
    recursive_measurement_root_discovery,
)


def test_hidden_measurement_super_root_is_discovered() -> None:
    row = recursive_measurement_root_discovery()

    assert row["discovered_super_roots"] == [
        "shared-observability-plane"
    ]
    discovery = row["discoveries"][0]
    assert discovery["affected_root_count"] == 3
    assert discovery["affected_channel_count"] == 6


def test_local_root_probes_do_not_false_positive() -> None:
    row = recursive_measurement_root_discovery()

    locals_ = [
        observation
        for observation in row["observations"]
        if observation["probe"]["probe_id"]
        != "probe-observability-plane"
    ]
    assert all(
        observation["cross_root_common_mode"] is False
        for observation in locals_
    )


def test_e057_promotion_contract() -> None:
    payload = recursive_measurement_lineage_report_payload()

    assert payload["e056_measurement_domain_authority_after_discovery"] == (
        "REVOKED"
    )
    assert all(payload["promotion_gate"].values())
    assert payload["promoted_recursive_rule"] == (
        "measurement-root-independence-requires-recursive-lineage-discovery-v1"
    )
