import json
from pathlib import Path

from market_microcosm.upstream_source_diversity import (
    upstream_source_diversity_report_payload,
)


def main() -> None:
    payload = upstream_source_diversity_report_payload()

    out = Path("artifacts/e049")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "upstream-source-diversity-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "hidden="
        + json.dumps(
            payload["hidden_common_source_reference"],
            sort_keys=True,
        )
    )
    print(
        "repair="
        + json.dumps(
            payload["diversified_repair_reference"],
            sort_keys=True,
        )
    )
    print(f"promoted-rule={payload['promoted_source_rule']}")


if __name__ == "__main__":
    main()
