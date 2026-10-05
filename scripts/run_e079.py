import json
from pathlib import Path

from market_microcosm.informative_kpi_withdrawal import (
    informative_missingness_report_payload,
)


def main() -> None:
    payload = informative_missingness_report_payload()
    out = Path("artifacts/e079")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "informative-kpi-withdrawal-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(path)
    print("withdrawal=" + json.dumps(payload["withdrawal_event"], sort_keys=True))
    print("aware=" + json.dumps(payload["withdrawal_aware_handler"], sort_keys=True))
    print("promoted-rule=" + str(payload["promoted_missingness_rule"]))


if __name__ == "__main__":
    main()
