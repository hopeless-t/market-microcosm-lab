import json
from pathlib import Path
from market_microcosm.sequential_evidence_acquisition import sequential_acquisition_report_payload

def main():
    x=sequential_acquisition_report_payload()
    out=Path("artifacts/e069");out.mkdir(parents=True,exist_ok=True)
    p=out/"sequential-evidence-acquisition-report.json"
    p.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
    print(p)
    print("optimal="+json.dumps(x["optimal_policy"],sort_keys=True))
    print("baselines="+json.dumps(x["baselines"],sort_keys=True))
if __name__=="__main__":main()
