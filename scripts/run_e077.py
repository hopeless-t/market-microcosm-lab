import json
from pathlib import Path
from market_microcosm.calibration_frontier import calibration_frontier_report_payload

def main():
    x=calibration_frontier_report_payload()
    out=Path("artifacts/e077");out.mkdir(parents=True,exist_ok=True)
    p=out/"calibration-frontier-report.json"
    p.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
    print(p)
    print("frontier="+json.dumps(x["frontier"],sort_keys=True))
    print("targets="+json.dumps(x["compiled_targets"],sort_keys=True))
if __name__=="__main__":main()
