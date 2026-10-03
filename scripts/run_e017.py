import json
from pathlib import Path

from market_microcosm.certificate_lifecycle import lifecycle_report_payload


def main() -> None:
    e015 = json.loads(
        Path("artifacts/e015/adaptive-boundary-report.json").read_text()
    )
    e016 = json.loads(
        Path("artifacts/e016/adaptive-guard-report.json").read_text()
    )
    payload = lifecycle_report_payload(
        e015_report=e015,
        e016_report=e016,
    )

    out = Path("artifacts/e017")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "certificate-lifecycle-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print("stable-summary=" + json.dumps(payload["stable_summary"], sort_keys=True))
    print("drift-summary=" + json.dumps(payload["drift_summary"], sort_keys=True))
    print(
        "failed-audit="
        + json.dumps(payload["failed_audit_decision"], sort_keys=True)
    )
    print("expiry=" + json.dumps(payload["expiry_decision"], sort_keys=True))
    print(
        "promotion-gate="
        + json.dumps(payload["promotion_gate"], sort_keys=True)
    )
    print(f"lifecycle-contract-passed={payload['lifecycle_contract_passed']}")


if __name__ == "__main__":
    main()
