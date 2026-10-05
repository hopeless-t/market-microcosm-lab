from market_microcosm.recursive_lineage_repair import (
    exact_minimum_repartition,
    provider_fault_check,
    recursive_lineage_repair_report_payload,
)


def test_exact_minimum_repartition() -> None:
    row = exact_minimum_repartition()["selected"]

    assert row["migrated_roots"] == ["root-1", "root-2"]
    assert row["migration_count"] == 2
    assert row["total_cost"] == 5
    assert row["maximum_channels_per_provider"] == 2


def test_repaired_topology_handles_every_single_provider_fault() -> None:
    row = provider_fault_check()

    assert row["provider_count"] == 5
    assert row["case_count"] == 5
    assert row["all_within_budget"] is True


def test_e058_promotion_contract() -> None:
    payload = recursive_lineage_repair_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_repair_rule"] == (
        "recursive-lineage-common-mode-repair-by-minimum-cost-repartition-v1"
    )
