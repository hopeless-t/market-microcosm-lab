import json
from pathlib import Path

from market_microcosm.adaptive_guard import guard_report_payload


def main() -> None:
    root = Path(".").resolve()
    e014 = json.loads(
        Path("artifacts/e014/interaction-surface-report.json").read_text()
    )
    e015 = json.loads(
        Path("artifacts/e015/adaptive-boundary-report.json").read_text()
    )
    payload = guard_report_payload(
        root,
        e014_report=e014,
        e015_report=e015,
    )

    out = Path("artifacts/e016")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "adaptive-guard-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "same-generation="
        + json.dumps(payload["same_generation"], sort_keys=True)
    )
    print(
        "changed-generation="
        + json.dumps(payload["changed_generation"], sort_keys=True)
    )
    print(
        "adversarial-probe="
        + json.dumps(payload["adversarial_probe"], sort_keys=True)
    )
    print(
        "promotion-gate="
        + json.dumps(payload["promotion_gate"], sort_keys=True)
    )
    print(f"guard-contract-passed={payload['guard_contract_passed']}")


if __name__ == "__main__":
    main()
