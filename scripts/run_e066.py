import json
from pathlib import Path
from market_microcosm.partial_public_evidence import partial_public_evidence_report_payload

def main():
    x=partial_public_evidence_report_payload()
    out=Path("artifacts/e066"); out.mkdir(parents=True,exist_ok=True)
    p=out/"partial-public-evidence-report.json"
    p.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
    print(p); print("portfolio="+json.dumps(x["portfolio"],sort_keys=True)); print("decision="+json.dumps(x["prospective_warning"],sort_keys=True))
if __name__=="__main__": main()
