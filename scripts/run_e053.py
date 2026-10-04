import json
from pathlib import Path

from market_microcosm.noisy_lineage_probes import (
    noisy_lineage_probe_report_payload,
)


def main() -> None:
    payload = noisy_lineage_probe_report_payload()

    out = Path("artifacts/e053")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "noisy-lineage-probe-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "counterexample="
        + json.dumps(
            payload["e052_noise_counterexample"],
            sort_keys=True,
        )
    )
    print(
        "robust="
        + json.dumps(
            payload["one_error_tolerant_search"],
            sort_keys=True,
        )
    )
    print(f"promoted-rule={payload['promoted_noise_rule']}")


if __name__ == "__main__":
    main()
