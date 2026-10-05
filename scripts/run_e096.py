import json
from pathlib import Path

from market_microcosm.japanese_saas_failure_taxonomy import taxonomy_report_payload


def main() -> None:
    payload = taxonomy_report_payload()
    out = Path("artifacts/e096")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "japanese-saas-failure-taxonomy-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(path)
    print("vectors=" + json.dumps(payload["vectors"], sort_keys=True))
    print("distances=" + json.dumps(payload["pairwise_hamming_distance"], sort_keys=True))


if __name__ == "__main__":
    main()
