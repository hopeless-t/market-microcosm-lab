import json
from pathlib import Path

from market_microcosm.certificate_ledger import (
    ledger_jsonl,
    ledger_report_payload,
)


def main() -> None:
    reports = {
        experiment: json.loads(Path(path).read_text())
        for experiment, path in {
            "e015": "artifacts/e015/adaptive-boundary-report.json",
            "e016": "artifacts/e016/adaptive-guard-report.json",
            "e017": "artifacts/e017/certificate-lifecycle-report.json",
            "e018": "artifacts/e018/audit-portfolio-report.json",
        }.items()
    }

    payload, ledger = ledger_report_payload(
        e015_report=reports["e015"],
        e016_report=reports["e016"],
        e017_report=reports["e017"],
        e018_report=reports["e018"],
    )

    out = Path("artifacts/e019")
    out.mkdir(parents=True, exist_ok=True)

    report_path = out / "certificate-ledger-report.json"
    report_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )

    ledger_path = out / "certificate-ledger.jsonl"
    ledger_path.write_text(ledger_jsonl(ledger))

    print(report_path)
    print(ledger_path)
    print(
        "verification="
        + json.dumps(payload["clean_verification"], sort_keys=True)
    )
    print(
        "tamper-probes="
        + json.dumps(payload["tamper_probes"], sort_keys=True)
    )
    print(
        "promotion-gate="
        + json.dumps(payload["promotion_gate"], sort_keys=True)
    )
    print(f"ledger-contract-passed={payload['ledger_contract_passed']}")


if __name__ == "__main__":
    main()
