import json
from pathlib import Path

from market_microcosm.hidden_common_mode import hidden_common_mode_report_payload


def main() -> None:
    payload = hidden_common_mode_report_payload()

    out = Path("artifacts/e023")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "hidden-common-mode-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print("nominal=" + json.dumps(payload["nominal_model"], sort_keys=True))
    print("hidden=" + json.dumps(payload["hidden_common_mode_model"], sort_keys=True))
    print("comparison=" + json.dumps(payload["comparison"], sort_keys=True))
    print("promotion-gate=" + json.dumps(payload["promotion_gate"], sort_keys=True))
    print(f"promoted-rule={payload['promoted_dependency_rule']}")


if __name__ == "__main__":
    main()
