import json
from pathlib import Path

from market_microcosm.checkpoint_rotation import checkpoint_rotation_report_payload


def main() -> None:
    e016 = json.loads(
        Path("artifacts/e016/adaptive-guard-report.json").read_text()
    )
    payload = checkpoint_rotation_report_payload(
        generation_a=e016["same_generation"]["fingerprint"],
        generation_b=e016["changed_generation"]["fingerprint"],
    )

    out = Path("artifacts/e020")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "checkpoint-rotation-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print("reference=" + json.dumps(payload["reference"], sort_keys=True))
    print("attacks=" + json.dumps(payload["attacks"], sort_keys=True))
    print(
        "promotion-gate="
        + json.dumps(payload["promotion_gate"], sort_keys=True)
    )
    print(f"promoted-rotation={payload['promoted_rotation_contract']}")


if __name__ == "__main__":
    main()
