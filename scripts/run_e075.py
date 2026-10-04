import json
from pathlib import Path
from market_microcosm.interval_dependence_ambiguity import (
    interval_dependence_report_payload,
)

def main():
    x=interval_dependence_report_payload()
    out=Path("artifacts/e075");out.mkdir(parents=True,exist_ok=True)
    p=out/"interval-dependence-ambiguity-report.json"
    p.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
    print(p)
    print("selected="+json.dumps(x["search"]["selected"],sort_keys=True))
if __name__=="__main__":main()
