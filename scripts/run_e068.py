import json
from pathlib import Path
from market_microcosm.decision_sufficient_acquisition import decision_sufficient_acquisition_report_payload
def main():
    x=decision_sufficient_acquisition_report_payload()
    out=Path("artifacts/e068");out.mkdir(parents=True,exist_ok=True)
    p=out/"decision-sufficient-acquisition-report.json";p.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
    print(p);print("worlds="+json.dumps(x["world_results"],sort_keys=True))
if __name__=="__main__":main()
