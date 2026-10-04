import json
from pathlib import Path

from market_microcosm.withdrawal_exit_holdout import (
    withdrawal_exit_holdout_report_payload,
)


def main() -> None:
    payload = withdrawal_exit_holdout_report_payload()
    out = Path("artifacts/e085")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "withdrawal-exit-holdout-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(path)
    print("timeline=" + json.dumps(payload["timeline"], sort_keys=True))
    print("promoted-rule=" + str(payload["promoted_holdout_rule"]))


if __name__ == "__main__":
    main()
