import json
from pathlib import Path

from market_microcosm.post_exit_horizon_guard import (
    post_exit_horizon_report_payload,
)


def main() -> None:
    payload = post_exit_horizon_report_payload()
    out = Path("artifacts/e092")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "post-exit-horizon-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(path)
    print("authority=" + json.dumps(payload["authority"], sort_keys=True))


if __name__ == "__main__":
    main()
