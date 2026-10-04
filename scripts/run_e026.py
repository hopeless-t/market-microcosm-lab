import json
from pathlib import Path

from market_microcosm.sampling_observation import (
    sampling_observation_report_payload,
)


def main() -> None:
    payload = sampling_observation_report_payload()

    out = Path("artifacts/e026")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "sampling-observation-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "srs-reference="
        + json.dumps(
            payload["hypothetical_srs_reference"],
            sort_keys=True,
        )
    )
    print(
        "adversarial="
        + json.dumps(
            payload["adversarial_unknown_design"],
            sort_keys=True,
        )
    )
    print(
        "promotion-gate="
        + json.dumps(payload["promotion_gate"], sort_keys=True)
    )
    print(f"promoted-rule={payload['promoted_observation_rule']}")


if __name__ == "__main__":
    main()
