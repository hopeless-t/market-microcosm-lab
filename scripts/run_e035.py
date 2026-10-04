import json
from pathlib import Path

from market_microcosm.early_warning import early_warning_report_payload


def main() -> None:
    payload = early_warning_report_payload()

    out = Path("artifacts/e035")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "early-warning-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "scores="
        + json.dumps(payload["rule_scores"], sort_keys=True)
    )
    print(f"promoted-rule={payload['promoted_warning_rule']}")


if __name__ == "__main__":
    main()
