import json
from pathlib import Path
from market_microcosm.direct_evidence_acquisition import direct_evidence_acquisition_report_payload
def main():
    x=direct_evidence_acquisition_report_payload()
    out=Path("artifacts/e067");out.mkdir(parents=True,exist_ok=True)
    p=out/"direct-evidence-acquisition-report.json";p.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
    print(p);print("naive="+json.dumps(x["naive_cost_only"],sort_keys=True));print("authorized="+json.dumps(x["authorized_search"],sort_keys=True))
if __name__=="__main__":main()
