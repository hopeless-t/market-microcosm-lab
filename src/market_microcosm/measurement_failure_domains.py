from __future__ import annotations

from dataclasses import dataclass
from math import ceil

from market_microcosm.lineage_probe_portfolio import hypotheses, probes
from market_microcosm.redundant_probe_synthesis import (
    exact_redundancy_synthesis,
    expanded_signature,
    nearest_hypothesis,
)


@dataclass(frozen=True)
class MeasurementChannel:
    channel_id: str
    probe_id: str
    failure_root: str


def selected_probe_channels() -> tuple[str, ...]:
    selected = exact_redundancy_synthesis()["selected"]
    channels = []
    for probe in probes():
        count = selected["repetition_counts"][probe.probe_id]
        for index in range(count):
            channels.append(f"{probe.probe_id}-{index}")
    return tuple(channels)


def correlated_bad_topology() -> tuple[MeasurementChannel, ...]:
    channels = selected_probe_channels()
    shared_ids = {
        "ab-0",
        "ac-0",
        "ac-1",
        "bc-0",
        "bc-1",
    }
    rows = []
    for channel_id in channels:
        probe_id = channel_id.split("-")[0]
        root = (
            "shared-collector"
            if channel_id in shared_ids
            else f"root-{channel_id}"
        )
        rows.append(MeasurementChannel(channel_id, probe_id, root))
    return tuple(rows)


def diversified_topology() -> tuple[MeasurementChannel, ...]:
    channels = selected_probe_channels()
    rows = []
    for index, channel_id in enumerate(channels):
        probe_id = channel_id.split("-")[0]
        root = f"root-{index // 2}"
        rows.append(MeasurementChannel(channel_id, probe_id, root))
    return tuple(rows)


def repetition_counts() -> tuple[int, ...]:
    selected = exact_redundancy_synthesis()["selected"]
    return tuple(
        selected["repetition_counts"][probe.probe_id]
        for probe in probes()
    )


def apply_root_fault(
    signature_bits: tuple[bool, ...],
    topology: tuple[MeasurementChannel, ...],
    root: str,
) -> tuple[bool, ...]:
    observed = list(signature_bits)
    for index, channel in enumerate(topology):
        if channel.failure_root == root:
            observed[index] = not observed[index]
    return tuple(observed)


def bad_common_mode_counterexample() -> dict:
    counts = repetition_counts()
    none = next(
        h for h in hypotheses()
        if h.hypothesis_id == "none"
    )
    abc = next(
        h for h in hypotheses()
        if h.hypothesis_id == "shared-abc"
    )
    true_signature = expanded_signature(none, counts)
    abc_signature = expanded_signature(abc, counts)
    topology = correlated_bad_topology()
    observed = apply_root_fault(
        true_signature,
        topology,
        "shared-collector",
    )
    decoded = nearest_hypothesis(observed, counts)

    flipped = sum(
        a != b for a, b in zip(true_signature, observed)
    )

    return {
        "true_hypothesis": "none",
        "fault_root": "shared-collector",
        "flipped_channel_count": flipped,
        "observed_equals_shared_abc_signature": (
            observed == abc_signature
        ),
        "decoded_hypothesis": decoded["decoded_hypothesis"],
        "misdecoded": (
            decoded["decoded_hypothesis"] != "none"
        ),
    }


def diversified_root_fault_check() -> dict:
    counts = repetition_counts()
    topology = diversified_topology()
    roots = sorted({row.failure_root for row in topology})
    checks = []

    for hypothesis in hypotheses():
        true_signature = expanded_signature(hypothesis, counts)
        for root in roots:
            observed = apply_root_fault(
                true_signature,
                topology,
                root,
            )
            decoded = nearest_hypothesis(observed, counts)
            flipped = sum(
                a != b
                for a, b in zip(true_signature, observed)
            )
            checks.append(
                {
                    "hypothesis_id": hypothesis.hypothesis_id,
                    "fault_root": root,
                    "flipped_channel_count": flipped,
                    "correct": (
                        decoded["unique"]
                        and decoded["decoded_hypothesis"]
                        == hypothesis.hypothesis_id
                    ),
                }
            )

    return {
        "root_count": len(roots),
        "maximum_channels_per_root": max(
            sum(1 for row in topology if row.failure_root == root)
            for root in roots
        ),
        "case_count": len(checks),
        "all_correct": all(row["correct"] for row in checks),
        "checks": checks,
    }


def measurement_failure_domain_report_payload() -> dict:
    bad = bad_common_mode_counterexample()
    good = diversified_root_fault_check()
    channel_count = len(selected_probe_channels())
    max_channels_per_root = 2
    lower_bound_roots = ceil(
        channel_count / max_channels_per_root
    )

    gates = {
        "one_common_root_can_flip_five_channels": (
            bad["flipped_channel_count"] == 5
        ),
        "common_root_can_create_exact_wrong_codeword": (
            bad["observed_equals_shared_abc_signature"] is True
            and bad["misdecoded"] is True
        ),
        "two_bit_certificate_requires_root_faults_to_flip_at_most_two_bits": True,
        "ten_channels_need_at_least_five_roots_under_size_two_bound": (
            lower_bound_roots == 5
        ),
        "diversified_reference_uses_five_roots": (
            good["root_count"] == 5
        ),
        "every_single_root_fault_decodes_correctly": (
            good["all_correct"] is True
            and good["case_count"] == 25
        ),
    }

    return {
        "experiment": "E056",
        "question": (
            "Does E055's two-bit error certificate remain valid when repeated "
            "measurement channels share a common failure root, and what "
            "failure-domain constraint is sufficient for one-root tolerance?"
        ),
        "bad_common_mode_counterexample": bad,
        "diversified_root_fault_check": good,
        "channel_count": channel_count,
        "maximum_channels_per_root_for_declared_bit_budget": (
            max_channels_per_root
        ),
        "minimum_root_count_lower_bound": lower_bound_roots,
        "promotion_gate": gates,
        "promoted_domain_rule": (
            "redundant-probe-channels-must-diversify-measurement-failure-roots-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Bit-level probe robustness is valid only when the measurement "
            "failure-domain topology bounds how many certified bits one root "
            "failure can corrupt. Repetition count alone is not redundancy."
        ),
        "limitations": (
            "The repair protects against one declared measurement-root fault. "
            "Multiple simultaneous roots or hidden common infrastructure can "
            "exceed the two-bit budget and require another robustness compile."
        ),
    }
