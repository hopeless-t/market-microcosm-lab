import json
from pathlib import Path

from market_microcosm.provenance_ledger import provenance_report_payload


def main() -> None:
    e016 = json.loads(
        Path("artifacts/e016/adaptive-guard-report.json").read_text()
    )
    payload = provenance_report_payload(
        generation_a=e016["same_generation"]["fingerprint"],
        generation_b=e016["changed_generation"]["fingerprint"],
    )

    out = Path("artifacts/e019")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "provenance-ledger-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "reference="
        + json.dumps(
            {
                "chain_valid": payload["reference"]["chain_valid"],
                "checkpoint_valid": payload["reference"]["checkpoint_valid"],
                "replay_state": payload["reference"]["replay_state"],
            },
            sort_keys=True,
        )
    )
    print(
        "attacks="
        + json.dumps(payload["attacks"], sort_keys=True)
    )
    print(
        "promotion-gate="
        + json.dumps(payload["promotion_gate"], sort_keys=True)
    )
    print(f"promoted-ledger={payload['promoted_ledger_contract']}")


if __name__ == "__main__":
    main()
