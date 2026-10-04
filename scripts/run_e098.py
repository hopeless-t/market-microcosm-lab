import json
from pathlib import Path

from market_microcosm.empirical_warning_tournament import (
    empirical_warning_tournament_report_payload,
)


def main() -> None:
    payload = empirical_warning_tournament_report_payload()
    out = Path("artifacts/e098")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "empirical-warning-tournament-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(path)
    print("scalar=" + json.dumps(payload["scalar_sign_rule"], sort_keys=True))
    print("typed=" + json.dumps(payload["typed_mechanism_rule"], sort_keys=True))


if __name__ == "__main__":
    main()
