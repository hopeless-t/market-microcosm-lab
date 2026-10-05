import json
from pathlib import Path

from market_microcosm.dependency_depth_stopping import (
    dependency_depth_stopping_report_payload,
)


def main() -> None:
    payload = dependency_depth_stopping_report_payload()

    out = Path("artifacts/e059")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "dependency-depth-stopping-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "compiled="
        + json.dumps(payload["compiled_depth"], sort_keys=True)
    )
    print(f"promoted-rule={payload['promoted_stopping_rule']}")


if __name__ == "__main__":
    main()
