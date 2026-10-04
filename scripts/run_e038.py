import json
from pathlib import Path

from market_microcosm.real_longitudinal_holdout import (
    real_longitudinal_holdout_report_payload,
)


def main() -> None:
    payload = real_longitudinal_holdout_report_payload()

    out = Path("artifacts/e038")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "real-longitudinal-holdout-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "holdouts="
        + json.dumps(payload["component_holdouts"], sort_keys=True)
    )
    print(
        "shock-context="
        + json.dumps(
            payload["concentration_shock_context"],
            sort_keys=True,
        )
    )
    print(
        f"promoted-rule={payload['promoted_longitudinal_rule']}"
    )


if __name__ == "__main__":
    main()
