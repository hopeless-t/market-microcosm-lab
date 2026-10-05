import json
from pathlib import Path

from market_microcosm.real_portfolio_transition import (
    portfolio_transition_report_payload,
)


def main() -> None:
    payload = portfolio_transition_report_payload()

    out = Path("artifacts/e063")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "real-portfolio-transition-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "transitions="
        + json.dumps(payload["transitions"], sort_keys=True)
    )
    print(
        "naive="
        + json.dumps(
            payload["naive_churn_direction_predictor"],
            sort_keys=True,
        )
    )
    print(f"promoted-rule={payload['promoted_transition_rule']}")


if __name__ == "__main__":
    main()
