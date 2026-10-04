from market_microcosm.active_lineage_discovery import (
    active_lineage_discovery_report_payload,
    discover_hidden_common_roots,
)


def test_hidden_master_root_is_discovered() -> None:
    row = discover_hidden_common_roots()

    assert row["discovered_root_ids"] == ["master-warehouse"]
    assert row["discoveries"][0]["affected_sources"] == [
        "source-a",
        "source-b",
        "source-c",
    ]


def test_local_probes_do_not_create_common_mode_false_positive() -> None:
    row = discover_hidden_common_roots()

    local = [
        observation
        for observation in row["observations"]
        if observation["probe"]["probe_id"] != "probe-master"
    ]
    assert all(
        observation["cross_domain_common_mode"] is False
        for observation in local
    )


def test_e051_promotion_contract() -> None:
    payload = active_lineage_discovery_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_discovery_rule"] == (
        "hidden-lineage-roots-require-active-intervention-discovery-v1"
    )
