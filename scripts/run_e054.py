import json
from pathlib import Path

from market_microcosm.probe_robustness_compiler import (
    robustness_compiler_report_payload,
)


def main() -> None:
    payload = robustness_compiler_report_payload()

    out = Path("artifacts/e054")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "probe-robustness-compiler-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "compiled="
        + json.dumps(
            payload["compiled_error_budgets"],
            sort_keys=True,
        )
    )
    print(f"promoted-rule={payload['promoted_compiler_rule']}")


if __name__ == "__main__":
    main()
