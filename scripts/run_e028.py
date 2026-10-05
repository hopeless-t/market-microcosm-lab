import json
from pathlib import Path

from market_microcosm.japan_failure_corpus import (
    japanese_failure_corpus_report_payload,
)


def main() -> None:
    payload = japanese_failure_corpus_report_payload()

    out = Path("artifacts/e028")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "japan-failure-corpus-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "portfolio="
        + json.dumps(payload["exact_failure_portfolio"], sort_keys=True)
    )
    print(
        "gap="
        + json.dumps(payload["survivorship_gap"], sort_keys=True)
    )
    print(
        "promotion-gate="
        + json.dumps(payload["promotion_gate"], sort_keys=True)
    )
    print(f"promoted-rule={payload['promoted_failure_rule']}")


if __name__ == "__main__":
    main()
