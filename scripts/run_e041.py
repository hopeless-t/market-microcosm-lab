import json
from pathlib import Path

from market_microcosm.minimal_observability_checkpoint import (
    minimal_observability_checkpoint_report_payload,
)


def main() -> None:
    payload = minimal_observability_checkpoint_report_payload()

    out = Path("artifacts/e041")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "minimal-observability-checkpoint-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "reference="
        + json.dumps(payload["reference"], sort_keys=True)
    )
    print(f"promoted-rule={payload['promoted_checkpoint_rule']}")


if __name__ == "__main__":
    main()
