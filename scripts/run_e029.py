import json
from pathlib import Path

from market_microcosm.strategic_exit import strategic_exit_report_payload


def main() -> None:
    payload = strategic_exit_report_payload()

    out = Path("artifacts/e029")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "strategic-exit-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "grid="
        + json.dumps(payload["finite_decision_grid"], sort_keys=True)
    )
    print(
        "promotion-gate="
        + json.dumps(payload["promotion_gate"], sort_keys=True)
    )
    print(f"promoted-rule={payload['promoted_exit_rule']}")


if __name__ == "__main__":
    main()
