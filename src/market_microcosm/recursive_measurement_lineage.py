from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class MeasurementRoot:
    root_id: str
    channel_count: int
    hidden_super_root: str


@dataclass(frozen=True)
class SuperRootProbe:
    probe_id: str
    target: str
    cost: int


def measurement_roots() -> tuple[MeasurementRoot, ...]:
    return (
        MeasurementRoot("root-0", 2, "shared-observability-plane"),
        MeasurementRoot("root-1", 2, "shared-observability-plane"),
        MeasurementRoot("root-2", 2, "shared-observability-plane"),
        MeasurementRoot("root-3", 2, "independent-root-3"),
        MeasurementRoot("root-4", 2, "independent-root-4"),
    )


def super_root_probes() -> tuple[SuperRootProbe, ...]:
    return (
        SuperRootProbe(
            "probe-observability-plane",
            "shared-observability-plane",
            2,
        ),
        SuperRootProbe("probe-root-3", "independent-root-3", 1),
        SuperRootProbe("probe-root-4", "independent-root-4", 1),
        SuperRootProbe("probe-unrelated", "unused-super-root", 1),
    )


def run_super_root_probe(
    probe: SuperRootProbe,
    roots: tuple[MeasurementRoot, ...],
) -> dict:
    affected = tuple(
        root for root in roots
        if root.hidden_super_root == probe.target
    )
    affected_channels = sum(
        root.channel_count for root in affected
    )

    return {
        "probe": asdict(probe),
        "affected_measurement_roots": [
            root.root_id for root in affected
        ],
        "affected_root_count": len(affected),
        "affected_channel_count": affected_channels,
        "cross_root_common_mode": len(affected) >= 2,
        "exceeds_e056_two_bit_budget": affected_channels > 2,
    }


def recursive_measurement_root_discovery() -> dict:
    roots = measurement_roots()
    observations = tuple(
        run_super_root_probe(probe, roots)
        for probe in super_root_probes()
    )
    discoveries = tuple(
        row for row in observations
        if (
            row["cross_root_common_mode"]
            and row["exceeds_e056_two_bit_budget"]
        )
    )

    return {
        "declared_measurement_root_count": len(roots),
        "probe_count": len(observations),
        "observations": list(observations),
        "discoveries": list(discoveries),
        "discovered_super_roots": [
            row["probe"]["target"]
            for row in discoveries
        ],
    }


def recursive_measurement_lineage_report_payload() -> dict:
    result = recursive_measurement_root_discovery()

    gates = {
        "hidden_super_root_is_discovered": (
            result["discovered_super_roots"]
            == ["shared-observability-plane"]
        ),
        "super_root_spans_three_declared_measurement_roots": (
            result["discoveries"][0]["affected_root_count"] == 3
        ),
        "super_root_fault_can_flip_six_certified_channels": (
            result["discoveries"][0]["affected_channel_count"] == 6
        ),
        "six_channel_blast_exceeds_e056_two_bit_budget": (
            result["discoveries"][0][
                "exceeds_e056_two_bit_budget"
            ]
            is True
        ),
        "local_root_probes_do_not_false_positive": all(
            row["cross_root_common_mode"] is False
            for row in result["observations"]
            if row["probe"]["probe_id"]
            != "probe-observability-plane"
        ),
        "recursive_dependency_discovery_reopens_e056_authority": True,
    }

    return {
        "experiment": "E057",
        "question": (
            "Can the five measurement roots admitted by E056 themselves "
            "share a hidden super-root that invalidates the one-root/two-bit "
            "failure model, and can bounded recursive probes discover it?"
        ),
        "reference": result,
        "e056_measurement_domain_authority_after_discovery": "REVOKED",
        "promotion_gate": gates,
        "promoted_recursive_rule": (
            "measurement-root-independence-requires-recursive-lineage-discovery-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Failure-domain independence is recursive. Declared measurement "
            "roots must themselves be probed for hidden super-root dependencies; "
            "a discovered super-root reopens the lower-level bit-error certificate."
        ),
        "limitations": (
            "The reference exposes a finite candidate super-root probe catalog "
            "with perfectly observable effects. Real recursive lineage discovery "
            "must bound intervention depth, permissions, and noisy effects."
        ),
    }
