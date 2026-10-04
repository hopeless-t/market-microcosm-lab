import json
from pathlib import Path

from market_microcosm.witness_quorum import witness_quorum_report_payload


def main() -> None:
    e016 = json.loads(
        Path("artifacts/e016/adaptive-guard-report.json").read_text()
    )
    payload = witness_quorum_report_payload(
        generation_a=e016["same_generation"]["fingerprint"],
        generation_b=e016["changed_generation"]["fingerprint"],
    )

    out = Path("artifacts/e021")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "witness-quorum-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "honest-quorum="
        + json.dumps(payload["honest_quorum"], sort_keys=True)
    )
    print(
        "compromise-boundary="
        + json.dumps(payload["compromise_boundary"], sort_keys=True)
    )
    print(
        "quorum-geometry="
        + json.dumps(payload["quorum_geometry"], sort_keys=True)
    )
    print(
        "split-view="
        + json.dumps(payload["split_view"], sort_keys=True)
    )
    print(
        "promotion-gate="
        + json.dumps(payload["promotion_gate"], sort_keys=True)
    )
    print(f"promoted-witness={payload['promoted_witness_contract']}")


if __name__ == "__main__":
    main()
